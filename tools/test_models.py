#!/usr/bin/env python3
"""
test_models.py -- solve library models with CoolSolve and compare with their committed .sol.

Two kinds of targets are tested; each is copied to a temporary folder, solved
with the CoolSolve CLI, and its fresh solution is compared with the `.sol`
committed next to it (the regression baseline):

  * the main file of every model whose status is verified / runs / modified,
    reported as `CSL-xxxx` (blocked / failing / stub native files are skipped);
  * every other `*.eescode` file of a model folder that has a sibling `.sol` of
    the same stem -- a runnable variant such as `<name>_coolsolve.eescode`,
    `<name>_simplified.eescode` -- whatever the status of the model (the
    runnable variant of a *blocked* native file is the one that is tested).
    Variants are reported as `CSL-xxxx:variant` (the stem without the
    `<name>_` prefix). A variant without `.sol` is not tested (listed at the end).

    python3 tools/test_models.py --coolsolve ../CoolSolve/build/coolsolve
    python3 tools/test_models.py CSL-0001 CSL-0007          # selected models (+ their variants)
    python3 tools/test_models.py CSL-0009:coolsolve         # one variant only
    python3 tools/test_models.py --no-variants              # main files only
    python3 tools/test_models.py --exclude CSL-0009:coolsolve   # skip the slowest target (about 3 min)
    COOLSOLVE=/path/to/coolsolve python3 tools/test_models.py --rtol 1e-6

Exit status 1 if any target fails to solve or deviates from its baseline.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNNABLE = {"verified", "runs", "modified"}


def read_sol(path):
    sol = {}
    rx = re.compile(r'^\s*([^=\s]+)\s*=\s*([-+0-9.eEinfINFnaN]+)\s*(?:"[^"]*")?\s*$')
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        m = rx.match(line)
        if m:
            try:
                sol[m.group(1).lower()] = float(m.group(2))
            except ValueError:
                pass
    return sol


def compare(new, ref, rtol, atol):
    bad = []
    for k, a in ref.items():
        if k not in new:
            bad.append("%s missing" % k)
            continue
        b = new[k]
        if abs(b - a) > atol + rtol * max(abs(a), abs(b)):
            bad.append("%s: %.6g -> %.6g" % (k, a, b))
    return bad


def targets(folder, meta, with_variants=True):
    """(variant label or None, eescode file name, baseline path or None) of a model folder.

    The main file comes first (label None); then every other `*.eescode` file, labelled with
    its stem minus the `<main stem>_` prefix. The baseline is the sibling `.sol` of the same
    stem, None when it does not exist.
    """
    main = meta["main_file"]
    main_stem = Path(main).stem
    out = [(None, main, (folder / (main_stem + ".sol")) if (folder / (main_stem + ".sol")).exists() else None)]
    if with_variants:
        for f in sorted(folder.glob("*.eescode")):
            if f.name == main:
                continue
            label = f.stem[len(main_stem) + 1:] if f.stem.startswith(main_stem + "_") else f.stem
            sol = f.with_suffix(".sol")
            out.append((label, f.name, sol if sol.exists() else None))
    return out


def run_target(exe, folder, main, baseline, label, name, args):
    """Solve `main` in a copy of `folder` and compare with `baseline` (None: only solve). True when OK."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / folder.name
        shutil.copytree(folder, work, ignore=shutil.ignore_patterns("original", "figures", "*_coolsolve"))
        sol = work / (Path(main).stem + ".sol")
        if sol.exists():
            sol.unlink()
        try:
            proc = subprocess.run([exe, "./" + main, "-o", os.devnull], cwd=work,
                                  capture_output=True, text=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            print("%-22s %-45s FAIL (timeout)" % (label, name))
            return False
        if proc.returncode != 0 or not sol.exists():
            msg = [l for l in (proc.stdout + proc.stderr).splitlines() if "Message" in l or "rror" in l]
            print("%-22s %-45s FAIL (solve) %s" % (label, name, msg[:1]))
            return False
        if baseline is None:
            print("%-22s %-45s OK (no baseline .sol committed)" % (label, name))
            return True
        bad = compare(read_sol(sol), read_sol(baseline), args.rtol, args.atol)
        if bad:
            print("%-22s %-45s DIFF (%d): %s" % (label, name, len(bad), "; ".join(bad[:5])))
            return False
        print("%-22s %-45s OK" % (label, name))
        return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ids", nargs="*", help="model IDs to test, with their variants (default: all runnable "
                    "models and variants); CSL-xxxx:variant selects one variant")
    ap.add_argument("--no-variants", action="store_true", help="test the main files only")
    ap.add_argument("--exclude", nargs="+", default=[], metavar="LABEL",
                    help="targets to skip, e.g. the slow CSL-0009:coolsolve (18 000 integration steps, 2-3 min)")
    ap.add_argument("--coolsolve", default=os.environ.get("COOLSOLVE", "coolsolve"),
                    help="CoolSolve executable (default: $COOLSOLVE or 'coolsolve' on PATH)")
    ap.add_argument("--rtol", type=float, default=1e-6)
    ap.add_argument("--atol", type=float, default=1e-9)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args(argv)

    exe = shutil.which(args.coolsolve) or args.coolsolve
    if not Path(exe).exists():
        sys.exit("CoolSolve executable not found: %s (use --coolsolve or $COOLSOLVE)" % args.coolsolve)

    wanted = {}                                   # model id -> None (every target) or set of variant labels
    for item in args.ids:
        mid, _, var = item.partition(":")
        if var:
            if wanted.get(mid, set()) is not None:
                wanted.setdefault(mid, set()).add(var)
        else:
            wanted[mid] = None
    failures, tested, n_variants, untested, seen = 0, 0, 0, [], set()
    for mj in sorted((ROOT / "models").rglob("model.json")):
        meta = json.loads(mj.read_text(encoding="utf-8"))
        if wanted and meta["id"] not in wanted:
            continue
        seen.add(meta["id"])
        folder = mj.parent
        sel = wanted.get(meta["id"])              # None: every target of the model
        for variant, main, baseline in targets(folder, meta, not args.no_variants):
            label = meta["id"] + (":" + variant if variant else "")
            if sel is not None and (variant or "") not in sel:
                continue
            if label in args.exclude:
                continue
            if variant is None and meta["status"] not in RUNNABLE:
                if wanted:
                    print("%-22s %-45s SKIP (native file, status %s)" % (label, meta["name"], meta["status"]))
                continue
            if variant is not None and baseline is None:
                untested.append(label)            # a variant without .sol has no baseline: not tested
                if sel is not None:
                    print("%-22s %-45s SKIP (no .sol baseline)" % (label, meta["name"]))
                continue
            tested += 1
            n_variants += variant is not None
            if not run_target(exe, folder, main, baseline, label, meta["name"], args):
                failures += 1
        if sel:
            known = {v for v, _, _ in targets(folder, meta)}
            for v in sorted(sel - known):
                print("%s:%s: no such variant" % (meta["id"], v))
                failures += 1
    for item in sorted(set(wanted) - seen):
        print("%s: no such model" % item)
        failures += 1
    if untested and not wanted:
        print("note: variants without .sol baseline (not tested): " + ", ".join(untested))
    print("%d target(s) tested (%d model main file(s), %d variant(s)), %d failure(s)" % (
        tested, tested - n_variants, n_variants, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

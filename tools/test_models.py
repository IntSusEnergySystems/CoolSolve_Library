#!/usr/bin/env python3
"""
test_models.py -- solve library models with CoolSolve and compare with their committed .sol.

Every model whose status is verified / runs / modified is copied to a temporary
folder, solved with the CoolSolve CLI, and its fresh solution is compared with
the `<name>.sol` committed in the model folder (the regression baseline).

    python3 tools/test_models.py --coolsolve ../CoolSolve/build/coolsolve
    python3 tools/test_models.py CSL-0001 CSL-0007          # selected models
    COOLSOLVE=/path/to/coolsolve python3 tools/test_models.py --rtol 1e-6

Exit status 1 if any model fails to solve or deviates from its baseline.
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ids", nargs="*", help="model IDs to test (default: all runnable models)")
    ap.add_argument("--coolsolve", default=os.environ.get("COOLSOLVE", "coolsolve"),
                    help="CoolSolve executable (default: $COOLSOLVE or 'coolsolve' on PATH)")
    ap.add_argument("--rtol", type=float, default=1e-6)
    ap.add_argument("--atol", type=float, default=1e-9)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args(argv)

    exe = shutil.which(args.coolsolve) or args.coolsolve
    if not Path(exe).exists():
        sys.exit("CoolSolve executable not found: %s (use --coolsolve or $COOLSOLVE)" % args.coolsolve)

    failures, tested = 0, 0
    for mj in sorted((ROOT / "models").rglob("model.json")):
        meta = json.loads(mj.read_text(encoding="utf-8"))
        if args.ids and meta["id"] not in args.ids:
            continue
        if meta["status"] not in RUNNABLE:
            if args.ids:
                print("%s %-45s SKIP (status %s)" % (meta["id"], meta["name"], meta["status"]))
            continue
        folder, main = mj.parent, meta["main_file"]
        baseline = folder / (Path(main).stem + ".sol")
        tested += 1
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
                print("%s %-45s FAIL (timeout)" % (meta["id"], meta["name"]))
                failures += 1
                continue
            if proc.returncode != 0 or not sol.exists():
                msg = [l for l in (proc.stdout + proc.stderr).splitlines() if "Message" in l or "rror" in l]
                print("%s %-45s FAIL (solve) %s" % (meta["id"], meta["name"], msg[:1]))
                failures += 1
                continue
            if not baseline.exists():
                print("%s %-45s OK (no baseline .sol committed)" % (meta["id"], meta["name"]))
                continue
            bad = compare(read_sol(sol), read_sol(baseline), args.rtol, args.atol)
            if bad:
                failures += 1
                print("%s %-45s DIFF (%d): %s" % (meta["id"], meta["name"], len(bad), "; ".join(bad[:5])))
            else:
                print("%s %-45s OK" % (meta["id"], meta["name"]))
    print("%d model(s) tested, %d failure(s)" % (tested, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

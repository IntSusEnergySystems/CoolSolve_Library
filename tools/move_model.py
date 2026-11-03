#!/usr/bin/env python3
"""
move_model.py -- move/rename library models by ID (taxonomy changes, T-TAXO).

Models are found by ID (model.json), never by path. A move relocates the model
folder to another category of taxonomy.json and may rename the folder; the
files named after the folder (`<name>.eescode`, `<name>_<variant>.eescode`,
`.sol`, `.initials`, `<name>-<table>.csv`) follow the rename and `model.json`
is updated (`name`, `main_file`, `category` if present, path mentions, and the
old path appended to `previous_paths` -- minimal text edits, the formatting of
the file is kept). Links to the old path are rewritten in every other model's
README.md/model.json, in docs/*.md and in sources/*/README.md (relative
Markdown links and plain path mentions); the count is reported per file. After
a real run, tools/build_index.py regenerates the index files (library.json,
library.html, redirects.csv).

Tracked folders are moved with `git mv` (staged for the maintainer); untracked
folders are moved plainly. New categories of a plan are declared in
taxonomy.json only with --declare-new (placeholder title and description, to
review); otherwise the tool stops and lists them. The tool refuses to run when
the git tree contains conflict files (`*.lane-*`). Use --dry-run first: the
tool never asks for confirmation.

Usage:

    python3 tools/move_model.py CSL-0123 components/compressors_turbo [--name new_folder_name] [options]
    python3 tools/move_model.py --plan plan.csv [options]        # CSV: id,new_category[,new_name]
    python3 tools/move_model.py --plan docs/taxonomy_v0.3.md [options]

A Markdown plan (.md) holds the moves as table rows `| CSL-NNNN | ... | new_category |`
(first cell the ID, last cell the target) and the complete new taxonomy as a
```json block with a "categories" key. The tool then checks that every model of
the library, moved or not, ends in a category of that taxonomy, and a real run
writes it to taxonomy.json before moving the folders (no --declare-new needed).

Options:

    --dry-run      print the full plan (moves, renames, link rewrites, new
                   categories) and change nothing
    --declare-new  add the undeclared categories of the plan to taxonomy.json
                   as placeholder entries (to review)
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
TAXONOMY = ROOT / "taxonomy.json"
ID_RE = re.compile(r"^CSL-\d{4}$")
# Characters allowed in the path tail that may follow the folder path in a
# mention (`/<file>.eescode`, ...); conservative on purpose.
TAIL_RE = r"(?:/[A-Za-z0-9_.+()\-]+)*"
LINK_TARGETS = "docs/*.md", "sources/*/README.md"


def find_model(mid):
    """Folder of the model with this ID; None when unknown, error on duplicates."""
    found = [f.parent for f in MODELS.rglob("model.json")
             if json.loads(f.read_text(encoding="utf-8")).get("id") == mid]
    if len(found) > 1:
        raise SystemExit("ERROR: model id %s used by several folders: %s"
                         % (mid, ", ".join(f.relative_to(ROOT).as_posix() for f in found)))
    return found[0] if found else None


def tracked(folder):
    """True when the folder has files tracked by git."""
    try:
        out = subprocess.run(["git", "ls-files", "--", folder.relative_to(ROOT).as_posix()],
                             cwd=ROOT, capture_output=True, text=True)
        return bool(out.stdout.strip())
    except OSError:
        return False


def read_plan(path):
    """(entries, new_taxonomy|None) from a CSV plan or a Markdown plan."""
    text = path.read_text(encoding="utf-8")
    entries = []
    if path.suffix.lower() != ".md":
        for i, row in enumerate(csv.reader(text.splitlines())):
            if not row or not row[0].strip():
                continue
            if i == 0 and not ID_RE.match(row[0].strip()):
                continue  # header line
            if len(row) < 2:
                raise SystemExit("ERROR: plan line %d needs at least id,new_category" % (i + 1))
            entries.append((row[0].strip(), row[1].strip().strip("/ "),
                            row[2].strip() if len(row) > 2 and row[2].strip() else None))
        return entries, None
    for line in text.splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and ID_RE.match(cells[0]):
            entries.append((cells[0], cells[-1].strip("/ "), None))
    blocks = [b for b in re.findall(r"```json\n(.*?)\n```", text, re.S) if '"categories"' in b]
    if len(blocks) != 1:
        raise SystemExit("ERROR: %s needs exactly one ```json block with the new taxonomy (found %d)" % (path, len(blocks)))
    return entries, json.loads(blocks[0])


def has_lane_conflicts():
    return sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.lane-*"))


def load_taxonomy():
    return json.loads(TAXONOMY.read_text(encoding="utf-8"))


def declared_categories(tax):
    paths = set()
    for top in tax["categories"]:
        paths.add(top["key"])
        for sub in top.get("children", []):
            paths.add(top["key"] + "/" + sub["key"])
    return paths


def declare_category(tax, cat):
    """Add `cat` to the taxonomy as a placeholder (in memory); True when changed."""
    if cat in declared_categories(tax):
        return False
    entry = {"key": cat, "title": cat.replace("_", " ").capitalize() + " (placeholder, to review)",
             "description": "Placeholder created by tools/move_model.py --declare-new; "
                            "review the title, description and placement."}
    if "/" in cat:
        top_key, sub_key = cat.split("/", 1)
        for top in tax["categories"]:
            if top["key"] == top_key:
                top.setdefault("children", []).append(
                    {"key": sub_key, "title": entry["title"], "description": entry["description"]})
                return True
        raise SystemExit("ERROR: cannot declare '%s': top category '%s' does not exist" % (cat, top_key))
    tax["categories"].append(entry)
    return True


def files_to_rename(folder, old_name):
    """Files named after the folder: <name>*.(eescode|sol|initials) and <name>-<table>.csv."""
    return sorted(p for p in folder.iterdir() if p.is_file() and p.name.startswith(old_name)
                  and len(p.name) > len(old_name) and p.name[len(old_name)] in ".-_"
                  and p.suffix.lower() in {".eescode", ".sol", ".initials", ".csv"})


def path_rewrite(move):
    """Regex + replacement rewriting the mentions of one old path (with or
    without a models/ prefix, optional /<file> tail)."""
    old_cat, new_cat = move["old_cat"], move["new_cat"]
    old_name, new_name = move["old_name"], move["new_name"]
    pattern = re.compile(r"(models/)?" + re.escape(old_cat) + "/" + re.escape(old_name) + r"(" + TAIL_RE + r")")

    def repl(m):
        tail = m.group(2)
        if old_name != new_name:  # first tail segment named after the folder follows the rename
            tail = re.sub(r"^/" + re.escape(old_name) + r"(?=[./]|$)", "/" + new_name, tail, count=1)
        return (m.group(1) or "") + new_cat + "/" + new_name + tail
    return pattern, repl


def rewrite_text(text, moves):
    """Rewrite the old-path mentions of a text; returns (new text, count)."""
    n = 0
    for move in moves:
        pattern, repl = path_rewrite(move)
        text, k = pattern.subn(repl, text)
        n += k
    return text, n


def scan_link_files():
    """Every file whose links to the old paths must be rewritten."""
    files = [p for p in MODELS.rglob("*") if p.name in ("README.md", "model.json") and p.is_file()]
    for pat in LINK_TARGETS:
        files += ROOT.glob(pat)
    return sorted(set(files))


def rewrite_one_file(f, moves, write=False):
    """Rewrite the old-path mentions of one file (Markdown links and plain
    path mentions). Returns the number of occurrences rewritten (written back
    only when > 0 and `write`)."""
    text = f.read_text(encoding="utf-8")
    text, n = rewrite_text(text, moves)
    if n and write:
        f.write_text(text, encoding="utf-8")
    return n


def collect_rewrites(moves, skip=None):
    """(path, count) per file containing at least one old-path mention."""
    out = []
    for f in scan_link_files():
        if skip and f.resolve() == skip.resolve():
            continue
        n = rewrite_one_file(f, moves)
        if n:
            out.append((f.relative_to(ROOT).as_posix(), n))
    return out


def update_model_json_text(path, move):
    """Minimal text edits of model.json for one move (byte-preserving
    otherwise): path mentions, name/main_file/category fields, and the old
    path appended to previous_paths. Returns the number of path mentions."""
    text = path.read_text(encoding="utf-8")
    text, n = rewrite_text(text, [move])  # mentions first: previous_paths does not hold the old path yet
    if move["old_name"] != move["new_name"]:
        text = re.sub(r'"name":\s*"%s"' % re.escape(move["old_name"]),
                      '"name": "%s"' % move["new_name"], text, count=1)
        text = re.sub(r'"main_file":\s*"%s' % re.escape(move["old_name"]),
                      '"main_file": "%s' % move["new_name"], text, count=1)
    text = re.sub(r'"category":\s*"%s"' % re.escape(move["old_cat"]),
                  '"category": "%s"' % move["new_cat"], text, count=1)
    m = re.search(r'"previous_paths":\s*\[[^\]]*\]', text, re.S)
    if m and '"%s"' % move["old_rel"] not in m.group(0):
        if '"previous_paths": []' in text:
            text = text.replace('"previous_paths": []',
                                '"previous_paths": ["%s"]' % move["old_rel"], 1)
        else:  # non-empty array: append before the closing bracket
            body = m.group(0)[:-1].rstrip().rstrip(",")
            text = text[:m.start()] + body + ', "%s"]' % move["old_rel"] + text[m.end():]
    path.write_text(text, encoding="utf-8")
    return n


def git_or_move(src, dst):
    """Move src to dst with `git mv` when src is tracked, plain move otherwise."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if tracked(src):
        subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)
        return "git mv"
    shutil.move(str(src), str(dst))
    return "plain move"


def git_rename(path, old_name, new_name):
    """Rename one file named after the folder (git mv when tracked)."""
    new = path.with_name(new_name + path.name[len(old_name):])
    if tracked(path):
        subprocess.run(["git", "mv", str(path), str(new)], cwd=ROOT, check=True)
    else:
        path.rename(new)


def prune_empty_dirs(folder):
    """Remove the now-empty category folders above a moved-out model (within models/)."""
    d = folder.parent
    while d != MODELS and d.is_dir():
        try:
            d.rmdir()
        except OSError:
            break
        d = d.parent


def build_plan(tax, entries):
    """entries: list of (id, new_cat, new_name|None); resolves the models by ID."""
    tax_paths = declared_categories(tax)
    plan, seen = [], set()
    for mid, new_cat, new_name in entries:
        if not ID_RE.match(mid):
            raise SystemExit("ERROR: bad model id %r (expected CSL-NNNN)" % mid)
        folder = find_model(mid)
        if folder is None:
            raise SystemExit("ERROR: model %s not found in models/" % mid)
        if mid in seen:
            raise SystemExit("ERROR: model %s listed twice in the plan" % mid)
        seen.add(mid)
        old_cat = folder.parent.relative_to(MODELS).as_posix()
        old_name = folder.name
        new_name = new_name or old_name
        if old_cat == new_cat and old_name == new_name:
            print("note: %s is already in %s/%s, nothing to do" % (mid, new_cat, new_name))
            continue
        move = {"id": mid, "old_cat": old_cat, "new_cat": new_cat,
                "old_name": old_name, "new_name": new_name,
                "old_rel": folder.relative_to(ROOT).as_posix(),
                "new_rel": "models/%s/%s" % (new_cat, new_name),
                "src": folder, "dst": MODELS / new_cat / new_name,
                "tracked": tracked(folder),
                "renames": files_to_rename(folder, old_name) if new_name != old_name else [],
                "undeclared": new_cat not in tax_paths}
        if move["dst"].exists():
            raise SystemExit("ERROR: destination %s already exists" % move["dst"])
        plan.append(move)
    return plan


def report(plan, new_cats, rewrites):
    print("plan: %d move(s)" % len(plan))
    for m in plan:
        print("  %s  %s -> %s  [%s]" % (m["id"], m["old_rel"], m["new_rel"],
                                        "git mv" if m["tracked"] else "plain move (untracked)"))
        for p in m["renames"]:
            print("    rename %s -> %s" % (p.name, p.name.replace(m["old_name"], m["new_name"], 1)))
    print("link rewrites: %d file(s) to change" % len(rewrites))
    for path, n in rewrites:
        print("  %s (%d)" % (path, n))
    if new_cats:
        print("new categories: %s" % ", ".join(sorted(new_cats)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model_id", nargs="?", help="model to move, e.g. CSL-0123")
    ap.add_argument("new_category", nargs="?", help="new category under models/, e.g. components/compressors_turbo")
    ap.add_argument("--name", help="new folder name (rename of the model)")
    ap.add_argument("--plan", type=Path, help="CSV plan (id,new_category[,new_name]) or Markdown plan with the new taxonomy")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, change nothing")
    ap.add_argument("--declare-new", action="store_true",
                    help="declare the new categories of the plan in taxonomy.json (placeholders, to review)")
    args = ap.parse_args(argv)

    conflicts = has_lane_conflicts()
    if conflicts:
        raise SystemExit("ERROR: conflict files in the git tree, resolve them first: " + ", ".join(conflicts))

    if bool(args.model_id) == bool(args.plan):
        ap.error("give a model id and its new category, or --plan (not both)")
    if args.model_id:
        if not args.new_category:
            ap.error("missing the new category of %s" % args.model_id)
        entries = [(args.model_id, args.new_category.strip("/ "), args.name)]
    else:
        entries, new_tax = read_plan(args.plan)
    new_tax = new_tax if args.plan else None

    tax = new_tax or load_taxonomy()
    plan = build_plan(tax, entries)
    if new_tax:
        # every model that does not move must also fit the new taxonomy
        moved = {m["id"] for m in plan} | {e[0] for e in entries}
        paths = declared_categories(new_tax)
        stray = []
        for f in sorted(MODELS.rglob("model.json")):
            mid = json.loads(f.read_text(encoding="utf-8")).get("id")
            cat = f.parent.parent.relative_to(MODELS).as_posix()
            if mid not in moved and cat not in paths:
                stray.append("%s (%s)" % (mid, cat))
        if stray:
            raise SystemExit("ERROR: %d model(s) not in the plan would stay in a category the new taxonomy does not declare: %s"
                             % (len(stray), ", ".join(stray)))
        print("new taxonomy v%s: %d top categories, %d categories; every model ends in a declared category"
              % (new_tax.get("version"), len(new_tax["categories"]), len(paths)))
    new_cats = sorted({m["new_cat"] for m in plan if m["undeclared"]})
    rewrites = collect_rewrites(plan, args.plan)
    report(plan, new_cats, rewrites)
    if not plan:
        return 0
    if new_cats and not args.declare_new:
        raise SystemExit("ERROR: new categories not declared in taxonomy.json: %s\n"
                         "       declare them (T-TAXO) or pass --declare-new (placeholder entries, to review)"
                         % ", ".join(new_cats))
    if args.dry_run:
        print("dry run: nothing changed")
        return 0

    # 1. Write the new taxonomy of a Markdown plan, or declare the new categories (placeholders).
    if new_tax:
        TAXONOMY.write_text(json.dumps(new_tax, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("taxonomy.json: written from %s (v%s)" % (args.plan, new_tax.get("version")))
    tax_changed = False
    for cat in new_cats:
        tax_changed |= declare_category(tax, cat)
    if tax_changed:
        TAXONOMY.write_text(json.dumps(tax, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("taxonomy.json: %d new category(ies) declared as placeholders (to review)" % len(new_cats))

    # 2. Move the folders, rename the files, update model.json.
    for m in plan:
        mode = git_or_move(m["src"], m["dst"])
        for p in m["renames"]:
            git_rename(m["dst"] / p.name, m["old_name"], m["new_name"])
        prune_empty_dirs(m["src"])
        n = update_model_json_text(m["dst"] / "model.json", m)
        print("moved %s -> %s [%s] (%d model.json path mention(s))"
              % (m["old_rel"], m["new_rel"], mode, n))

    # 3. Rewrite the links to the old paths (the moved models' model.json was
    #    already handled in step 2, before their previous_paths grew).
    total, n_files = 0, 0
    moved_json = {m["dst"] / "model.json" for m in plan}
    for f in scan_link_files():
        if f in moved_json or (args.plan and f.resolve() == args.plan.resolve()):
            continue
        n = rewrite_one_file(f, plan, write=True)
        if n:
            print("rewrote %d link(s) in %s" % (n, f.relative_to(ROOT).as_posix()))
            total += n
            n_files += 1
    print("link rewrites: %d occurrence(s) in %d file(s)" % (total, n_files))

    # 4. Rebuild the index.
    build = subprocess.run([sys.executable, str(ROOT / "tools" / "build_index.py")], cwd=ROOT)
    if build.returncode:
        print("ERROR: tools/build_index.py reported errors (see above)", file=sys.stderr)
    return build.returncode


if __name__ == "__main__":
    sys.exit(main())

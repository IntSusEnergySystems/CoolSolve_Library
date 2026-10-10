#!/usr/bin/env python3
"""
build_index.py -- validate the library and regenerate its index files.

The folder tree is the single source of truth: every model folder contains a
`model.json`; its category is its location under `models/`.  This script

  * validates every model folder (required files and fields, unique IDs,
    category declared in taxonomy.json, allowed kind/level/status values);
  * regenerates, at the repository root:
      library.json   the index: one record per model, every FUNCTION/PROCEDURE,
                     the CoolSolve gaps the models list, and the snapshot identity
                     (read by CoolSolve, which embeds the library at compile time)
      library.html   the dashboard: sortable/filterable tables of the models,
                     functions and CoolSolve gaps (self-contained, opens from disk;
                     template tools/library_dashboard.html)
      redirects.csv  previous paths of moved/renamed models -> current ID

The gap descriptions are read from the CoolSolve register
(docs/model_library_support.md of the CoolSolve checkout next to this
repository, or --register PATH); without it the dashboard shows the IDs only.

Model folders contain CoolSolve files and documentation only: source files
(.ees, .lib, .lkt, .py, notebooks, archives) and `original/` or `reference/`
folders are rejected -- the source is referenced by its path (with ~), URL or
library name in model.json.  Authors not known yet are written "TBD"; the
script lists them, and the models without figure, for the maintainer.

IDs are never reused: removed models are listed in `retired.csv`
(id,date,reason,replaced_by) and count when the next free ID is computed.

Never edit the generated files by hand.  Usage:

    python3 tools/build_index.py            # validate + write
    python3 tools/build_index.py --check    # validate only (CI); exit 1 on error
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
REPO_URL = "https://github.com/IntSusEnergySystems/CoolSolve_Library"
REGISTER_URL = "https://github.com/CoolProp/CoolSolve/blob/main/docs/model_library_support.md"
DEFAULT_REGISTER = ROOT.parent / "CoolSolve" / "docs" / "model_library_support.md"

KINDS = {"steady": "⚙️ Steady-state", "dynamic": "⏱️ Dynamic",
         "optimization": "🎯 Optimisation", "function": "🧩 Function library"}
LEVELS = {1: "🟢 Level 1 · Introductory", 2: "🔵 Level 2 · Intermediate",
          3: "🟠 Level 3 · Advanced", 4: "🔴 Level 4 · Research"}
STATUSES = {"verified": "✅ Verified", "runs": "☑️ Runs", "modified": "⚠️ Runs (modified)",
            "blocked": "⛔ Blocked", "failing": "❌ Failing", "stub": "📄 Documented only"}
ORIGIN_TYPES = {"teaching", "research", "textbook", "software_library", "industry", "coolsolve"}
REQUIRED = ["id", "name", "title", "summary", "kind", "level", "status", "main_file", "origin"]
ID_RE = re.compile(r"^CSL-\d{4}$")
GAP_RE = re.compile(r"^CS-(GAP|BUG|FEAT|DOC)-[A-Z0-9-]+$")
SOURCE_EXT = {".ees", ".lib", ".lkt", ".py", ".ipynb", ".m", ".mo", ".zip", ".7z", ".rar", ".xls", ".xlsx"}
FORBIDDEN_DIRS = {"original", "reference"}
FIGURE_EXT = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp"}
FIGURE_MAX_BYTES = 100_000
# Files of a model folder that CoolSolve embeds in its binary (CoolSolve
# docs/model_library_support.md, section 2.1); everything else stays out.
EMBED_FILES = re.compile(r"^(README\.md|model\.json|coolsolve\.conf|[^/]+\.(eescode|initials|sol)|[^/]+-[^/]+\.csv|"
                         r"figures/[^/]+\.(png|svg|jpg|jpeg|webp))$", re.I)


def embedded_files(folder):
    """Files of a model folder that belong to the CoolSolve snapshot."""
    return sorted(p for p in folder.rglob("*")
                  if p.is_file() and EMBED_FILES.match(p.relative_to(folder).as_posix()))


def snapshot_identity(model_folders):
    """Deterministic content hash and size of everything CoolSolve embeds."""
    h, n, size = hashlib.sha256(), 0, 0
    files = [ROOT / "taxonomy.json", ROOT / "docs" / "taxonomy.md"]
    for folder in model_folders:
        files += embedded_files(folder)
    for f in sorted(files):
        data = f.read_bytes()
        h.update(f.relative_to(ROOT).as_posix().encode() + b"\0" + data)
        n, size = n + 1, size + len(data)
    return "sha256:" + h.hexdigest()[:16], n, size

def load_taxonomy():
    tax = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
    paths = {}
    for top in tax["categories"]:
        paths[top["key"]] = top
        for sub in top.get("children", []):
            paths[top["key"] + "/" + sub["key"]] = sub
    return tax, paths


def find_models():
    return sorted(p.parent for p in MODELS.rglob("model.json"))


def functions_in(eescode):
    text = eescode.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"\{[^}]*\}", " ", text)                       # drop brace comments
    out = []
    for m in re.finditer(r"^\s*(FUNCTION|PROCEDURE)\s+([A-Za-z_][A-Za-z0-9_$]*)\s*(\([^)]*\))?",
                         text, flags=re.I | re.M):
        out.append((m.group(1).upper(), m.group(2), re.sub(r"\s+", " ", m.group(3) or "")))
    return out


VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(\+[\w./-]+)?@[0-9a-f]{7,}$")


def check_links_and_versions(rows):
    """Warnings on conventions of workflow section 3 (step 7) that the validation does not enforce."""
    known = {r["id"] for r in rows}
    related = {r["id"]: r["related"] for r in rows}
    prose = sorted(i for i, rel in related.items() if any(not ID_RE.match(x) for x in rel))
    if prose:
        print("warning: 'related' must hold model ids only (prose belongs in the README): " + ", ".join(prose))
    unknown = ["%s->%s" % (i, x) for i, rel in sorted(related.items()) for x in rel
               if ID_RE.match(x) and x not in known]
    if unknown:
        print("warning: 'related' points to a model that is not in the library: " + ", ".join(unknown))
    one_way = ["%s->%s" % (i, x) for i, rel in sorted(related.items()) for x in rel
               if x in known and i not in related.get(x, [])]
    if one_way:
        print("warning: 'related' without back-link: " + ", ".join(one_way))
    old_ver = sorted(r["id"] for r in rows if r["coolsolve_version"] and not VERSION_RE.match(r["coolsolve_version"]))
    if old_ver:
        print("warning: verification.coolsolve_version should be '<version>@<commit>' "
              "(e.g. 0.3.0@536d427): " + ", ".join(old_ver))


def validate(folder, meta, tax_paths, errors):
    rel = folder.relative_to(MODELS).as_posix()
    where = "models/" + rel
    for key in REQUIRED:
        if key not in meta:
            errors.append("%s: missing field '%s'" % (where, key))
    if errors and any(e.startswith(where) for e in errors):
        return
    if not ID_RE.match(meta["id"]):
        errors.append("%s: bad id %r (expected CSL-NNNN)" % (where, meta["id"]))
    if meta["name"] != folder.name:
        errors.append("%s: name %r differs from folder name" % (where, meta["name"]))
    category = folder.parent.relative_to(MODELS).as_posix()
    if category not in tax_paths:
        errors.append("%s: category '%s' is not declared in taxonomy.json" % (where, category))
    if meta["kind"] not in KINDS:
        errors.append("%s: kind %r not in %s" % (where, meta["kind"], sorted(KINDS)))
    if meta["level"] not in LEVELS:
        errors.append("%s: level %r not in 1..4" % (where, meta["level"]))
    if meta["status"] not in STATUSES:
        errors.append("%s: status %r not in %s" % (where, meta["status"], sorted(STATUSES)))
    if not (folder / meta["main_file"]).is_file():
        errors.append("%s: main file %s not found" % (where, meta["main_file"]))
    if not (folder / "README.md").is_file():
        errors.append("%s: README.md missing" % where)
    origin = meta["origin"]
    if origin.get("type") not in ORIGIN_TYPES:
        errors.append("%s: origin.type %r not in %s" % (where, origin.get("type"), sorted(ORIGIN_TYPES)))
    for k in ("source", "authors", "license"):
        if not origin.get(k):
            errors.append("%s: origin.%s is required (attribution)" % (where, k))
    for g in meta.get("missing_features", []):
        if not GAP_RE.match(g):
            errors.append("%s: missing_features entry %r is not a CS-GAP/BUG/FEAT/DOC id" % (where, g))
    if meta["status"] == "blocked" and not meta.get("missing_features"):
        errors.append("%s: status 'blocked' requires missing_features" % where)
    for item in folder.rglob("*"):
        if item.is_dir() and item.name.lower() in FORBIDDEN_DIRS:
            errors.append("%s: folder '%s' is not allowed (reference the source in model.json)" % (where, item.name))
        elif item.is_file() and item.suffix.lower() in SOURCE_EXT:
            errors.append("%s: source file '%s' must not be stored in the library (give its path or URL "
                          "in model.json origin.source_path / origin.url)" % (where, item.relative_to(folder)))


def figures_of(folder):
    fig = folder / "figures"
    return sorted(p.name for p in fig.iterdir() if p.suffix.lower() in FIGURE_EXT) if fig.is_dir() else []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--register", type=Path,
                    default=Path(os.environ.get("COOLSOLVE_REGISTER", DEFAULT_REGISTER)),
                    help="CoolSolve gap register (default: %(default)s)")
    args = ap.parse_args(argv)

    tax, tax_paths = load_taxonomy()
    errors, rows, funcs, redirects, seen = [], [], [], [], {}
    last_update = ""
    for folder in find_models():
        try:
            meta = json.loads((folder / "model.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            errors.append("models/%s/model.json: %s" % (folder.relative_to(MODELS).as_posix(), e))
            continue
        validate(folder, meta, tax_paths, errors)
        if "id" not in meta:
            continue
        if meta["id"] in seen:
            errors.append("duplicate id %s in %s and %s" % (meta["id"], seen[meta["id"]], folder))
        seen[meta["id"]] = folder
        o, v, s = meta.get("origin", {}), meta.get("verification", {}), meta.get("stats", {})
        path = folder.relative_to(ROOT).as_posix()
        rows.append({
            "id": meta["id"], "name": meta.get("name"), "title": meta.get("title"),
            "category": folder.parent.relative_to(MODELS).as_posix(),
            "kind": meta.get("kind"), "level": meta.get("level"), "status": meta.get("status"),
            "summary": meta.get("summary"), "fluids": meta.get("fluids", []),
            "tags": meta.get("tags", []), "n_equations": s.get("n_equations", ""),
            "largest_block": s.get("largest_block", ""), "origin_type": o.get("type"),
            "source": o.get("source"), "source_path": o.get("source_path", ""),
            "authors": o.get("authors", []), "license": o.get("license"),
            "url": o.get("url", ""), "missing_features": meta.get("missing_features", []),
            "related": meta.get("related", []),
            "coolsolve_version": v.get("coolsolve_version", ""), "verified_on": v.get("date", ""),
            "path": path, "main_file": meta.get("main_file"), "figures": len(figures_of(folder)),
        })
        main_file = folder / meta.get("main_file", "")
        if main_file.is_file():
            for kind, name, sig in functions_in(main_file):
                funcs.append({"function": name, "type": kind, "signature": sig,
                              "model_id": meta["id"], "path": path + "/" + meta["main_file"]})
        for h in meta.get("history", []):
            last_update = max(last_update, str(h.get("date", "")))
        for old in meta.get("previous_paths", []):
            redirects.append({"previous_path": old, "id": meta["id"], "current_path": path})

    rows.sort(key=lambda r: (r["category"], r["id"]))
    used = set(seen)
    retired = ROOT / "retired.csv"
    if retired.exists():
        with open(retired, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("id") in seen:
                    errors.append("id %s is both retired and in use" % r["id"])
                used.add(r.get("id", ""))
    nums = [int(i[4:]) for i in used if ID_RE.match(i)]
    print("next free id: CSL-%04d" % (max(nums, default=0) + 1))
    for e in errors:
        print("ERROR: " + e, file=sys.stderr)
    by_name = {}
    for fn in funcs:
        by_name.setdefault(fn["function"].lower(), []).append(fn["model_id"])
    for name, ids in sorted(by_name.items()):
        if len(set(ids)) > 1:
            print("warning: function '%s' is defined in several models (%s): $INCLUDE resolution "
                  "needs unique names" % (name, ", ".join(sorted(set(ids)))))
    for r in rows:
        for fig in (ROOT / r["path"] / "figures").glob("*"):
            if fig.stat().st_size > FIGURE_MAX_BYTES:
                print("warning: %s/figures/%s is %d kB (limit %d kB, embedded in CoolSolve)" % (
                    r["id"], fig.name, fig.stat().st_size // 1000, FIGURE_MAX_BYTES // 1000))
    content_hash, n_files, n_bytes = snapshot_identity([ROOT / r["path"] for r in rows])
    print("snapshot: %d files, %.1f MB, %s" % (n_files, n_bytes / 1e6, content_hash))
    check_links_and_versions(rows)
    todo_authors = [r["id"] for r in rows if any("TBD" in a for a in r["authors"])]
    todo_figures = [r["id"] for r in rows if not r["figures"] and r["status"] in ("verified", "runs", "modified")]
    if todo_authors:
        print("maintainer: authors to complete (TBD): " + ", ".join(todo_authors))
    if todo_figures:
        print("maintainer: runnable models without figure: " + ", ".join(todo_figures))
    print("%d models, %d functions, %d errors" % (len(rows), len(funcs), len(errors)))
    if args.check:
        return 1 if errors else 0

    gaps = read_register(args.register)
    used = sorted({g for r in rows for g in r["missing_features"]})
    unknown_gaps = [g for g in used if gaps and g not in gaps]
    if unknown_gaps:
        print("warning: missing_features not found in the CoolSolve register: " + ", ".join(unknown_gaps))
    funcs.sort(key=lambda r: r["function"].lower())
    snapshot = {"content_hash": content_hash, "files": n_files, "bytes": n_bytes, "models": len(rows),
                "functions": len(funcs), "taxonomy_version": tax.get("version")}
    (ROOT / "library.json").write_text(json.dumps(
        {"snapshot": snapshot, "models": rows, "functions": funcs, "gaps": gaps},
        indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    with open(ROOT / "redirects.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["previous_path", "id", "current_path"])
        w.writeheader()
        w.writerows(redirects)
    categories = {}
    for path, node in tax_paths.items():
        top = path.split("/")[0]
        categories[path] = node["title"] if path == top else tax_paths[top]["title"] + " › " + node["title"]
    write_dashboard({
        "generated": last_update, "snapshot": snapshot, "repo_url": REPO_URL, "register_url": REGISTER_URL,
        "register_found": bool(gaps),
        "labels": {"kinds": KINDS, "levels": {str(k): v for k, v in LEVELS.items()}, "statuses": STATUSES},
        "taxonomy": tax["categories"], "categories": categories, "models": rows, "functions": funcs, "gaps": gaps})
    return 1 if errors else 0


REGISTER_SECTIONS = {"3": "features", "4": "gaps", "5": "bugs", "7": "closed"}
KIND_OF = {"GAP": "gap", "BUG": "bug", "FEAT": "feature", "DOC": "documentation"}


def github_anchor(heading):
    """Anchor GitHub gives to a Markdown heading."""
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", heading.strip().lower()))


def plain(cell):
    """A register cell as short plain Markdown: links unwrapped, escaped pipes restored."""
    cell = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cell.replace("\\|", "|")).strip()
    return re.sub(r"\s+", " ", cell)


def first_sentence(text, limit=260):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(`*])", text)
    out = parts[0]
    if len(out) < 30 and len(parts) > 1:
        out += " " + parts[1]
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0] + " …"
    if out.count("`") % 2:          # never leave an inline code span open
        out = out.replace("`", "")
    return out


def read_register(path):
    """ID -> {kind, state, priority, text, detail, fixed_in, anchor} from the CoolSolve register."""
    if not path or not Path(path).is_file():
        print("warning: CoolSolve register not found (%s): the dashboard shows gap IDs only" % path)
        return {}
    gaps, section, anchor = {}, None, ""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        m = re.match(r"^## (\d+)\.", line)
        if m:
            section, anchor = REGISTER_SECTIONS.get(m.group(1)), github_anchor(line[3:])
            continue
        if not section or not line.startswith("| `CS-"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        gid = cells[0].strip("`")
        if not GAP_RE.match(gid) or len(cells) < 2:
            continue
        prio = next((c for c in reversed(cells[1:]) if re.match(r"^P[123]\b", c)), "")
        entry = {"kind": KIND_OF[gid.split("-")[1]], "state": "closed" if section == "closed" else "open",
                 "priority": plain(prio)[:60], "text": first_sentence(plain(cells[1])), "detail": "",
                 "fixed_in": "", "anchor": anchor}
        if section == "gaps" and len(cells) > 2:
            entry["detail"] = first_sentence(plain(cells[2]), 200)
        if section == "closed":
            entry["priority"], entry["fixed_in"] = "", plain(cells[2]) if len(cells) > 2 else ""
        if gid not in gaps or section == "closed":
            gaps[gid] = entry
    return gaps


def write_dashboard(data):
    """library.html: the template with the index inlined (no network access needed)."""
    template = (ROOT / "tools" / "library_dashboard.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (ROOT / "library.html").write_text(template.replace("/*__LIBRARY_DATA__*/", payload), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())

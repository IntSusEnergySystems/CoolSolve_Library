#!/usr/bin/env python3
"""
backlog_stats.py -- summarise the source inventories (the library backlog).

Reads sources/*/inventory.csv and prints Markdown tables (decisions and
priorities per source, candidates per category) to paste in roadmap.md §1.

    python3 tools/backlog_stats.py
    python3 tools/backlog_stats.py --next thermo_models 10 [--category heat_exchangers]

`--next` lists the next candidates to process: decision 'todo', representatives
first, by priority (wave1, high, medium, low).

The inventories are also checked: a row whose number of cells differs from the header
(typically a `notes` cell containing a comma that was not put between double quotes, which
shifts `decision` and `library_id`) is reported as an ERROR and the exit status is 1.
"""

import argparse
import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS = ["todo", "added", "superseding", "merged", "duplicate", "discarded", "parked"]
PRIORITIES = ["wave1", "high", "medium", "low", "skip", "merged"]


def load(errors=None):
    inv = {}
    for p in sorted((ROOT / "sources").glob("*/inventory.csv")):
        with open(p, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for cells in reader:
                if len(cells) != len(header):
                    if errors is not None:
                        errors.append("%s: row %s has %d cells instead of %d (unquoted comma in a cell?)" % (
                            p.relative_to(ROOT), cells[0] if cells else "?", len(cells), len(header)))
                    cells = (cells + [""] * len(header))[:len(header)]
                rows.append(dict(zip(header, cells)))
            inv[p.parent.name] = rows
    return inv


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--next", nargs=2, metavar=("SOURCE", "N"), help="list the next N candidates of SOURCE")
    ap.add_argument("--category", help="restrict --next to a category_guess")
    args = ap.parse_args(argv)
    errors = []
    inv = load(errors)
    for e in errors:
        print("ERROR: " + e, file=sys.stderr)

    if args.next:
        src, n = args.next[0], int(args.next[1])
        rows = [r for r in inv[src] if (r.get("decision") or "todo") == "todo"
                and r.get("priority") not in ("skip", "merged")
                and (not args.category or r.get("category_guess") == args.category)]
        rank = {p: i for i, p in enumerate(PRIORITIES)}
        rows.sort(key=lambda r: (rank.get(r.get("priority"), 9), r.get("is_representative") != "yes",
                                 r.get("category_guess", ""), r.get("candidate_id")))
        print("| Candidate | Priority | Category | Level | Kind | Title | Path |")
        print("|---|---|---|---|---|---|---|")
        for r in rows[:n]:
            print("| %s | %s | %s | %s | %s | %s | `%s` |" % (
                r["candidate_id"], r.get("priority"), r.get("category_guess"), r.get("level_guess"),
                r.get("kind_guess"), r.get("title", "")[:60], r.get("path", "")[:80]))
        return 0

    print("| Source | Candidates | " + " | ".join(DECISIONS) + " |")
    print("|---|---:|" + "---:|" * len(DECISIONS))
    for src, rows in inv.items():
        c = collections.Counter((r.get("decision") or "todo") for r in rows)
        print("| %s | %d | %s |" % (src, len(rows), " | ".join(str(c.get(d, 0)) for d in DECISIONS)))
    print()
    print("| Source | " + " | ".join(PRIORITIES) + " |")
    print("|---|" + "---:|" * len(PRIORITIES))
    for src, rows in inv.items():
        c = collections.Counter(r.get("priority") for r in rows)
        print("| %s | %s |" % (src, " | ".join(str(c.get(p, 0)) for p in PRIORITIES)))
    print()
    cats = collections.Counter()
    for rows in inv.values():
        for r in rows:
            if r.get("priority") not in ("skip",) and (r.get("decision") or "todo") == "todo":
                cats[r.get("category_guess") or "?"] += 1
    print("| Category (open candidates, all sources) | Count |")
    print("|---|---:|")
    for k, v in cats.most_common():
        print("| %s | %d |" % (k, v))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

# CoolSolve Library — Roadmap

Living work programme of the library. It lists **what has been done** (summary
only — the detailed log of each model is in its README, section *Conversion
log*) and **what remains to be done**, as a sequence of small steps that are
each tested and marked done. *How* each step is executed is described in
[docs/model_workflow.md](docs/model_workflow.md); the classification rules are
in [docs/taxonomy.md](docs/taxonomy.md).

*Last update: 2026-10-05.*

---

## 1. Status at a glance

| Library (2026-10-09, 20:00 — work paused) | Count |
|---|---:|
| Models (`library.csv`) | 148 |
| … verified / runs / blocked | 98 / 7 / 43 |
| … blocked with a verified runnable `_coolsolve` variant / not runnable at all | 36 / 7 |
| … steady / function / dynamic / optimization | 105 / 37 / 5 / 1 |
| Functions and procedures (`functions.csv`) | 432 |
| Regression (`test_models.py`, `CSL-0009:coolsolve` excluded) | 150 targets (105 main files + 45 variants), 0 failure |
| CoolSolve gaps and bugs open (CoolSolve [`docs/model_library_support.md`](https://github.com/CoolProp/CoolSolve/blob/main/docs/model_library_support.md) §4–§5) | 98 (58 gaps, 38 bugs, 2 doc issues) |
| … closed (§7) | 9 (3 gaps, 5 bugs, 1 doc issue) |
| … unverified suggestions (§8 *Unverified by a reviewer*) | 11 |

Not runnable at all (no verified variant): `CSL-0081` (borefield, dynamic), `CSL-0043` (LiBr absorption chiller),
`CSL-0040` (biomass ORC CHP), `CSL-0116` (Vitocal heat pump, catalogue vintage), `CSL-0155` (inverter heat pump, one
coupled block fails — register §8), `CSL-0150` (flame with dissociation, CS-GAP-CHEM-EQUIL), `CSL-0162` (run-around
loop, CS-BUG-NEWTON-CYCLE).

| Backlog (source inventories) | Candidates | todo | added | merged | duplicate | discarded | parked |
|---|---:|---:|---:|---:|---:|---:|---:|
| ULiège collection `thermo_models` | 602 | 322 | 99 | 38 | 92 | 50 | 1 |
| CoolSolve examples | 47 | 1 | 33 | 9 | 1 | 3 | 0 |
| `ht` (Caleb Bell), one row per correlation family | 24 | 0 | 24 | 0 | 0 | 0 | 0 |
| ThermoCycle | 21 | 2 | 4 | 1 | 0 | 14 | 0 |
| LaboThapPy | 74 | 59 | 9 | 6 | 0 | 0 | 0 |
| TESPy | 52 | 49 | 2 | 1 | 0 | 0 | 0 |

The tables count inventory **rows**, not models: a model imported from a
CoolSolve example and from its EES original in `thermo_models` has two `added`
rows (workflow §2). Every library model has its `added` row (cross-check of
2026-10-09).

Priorities of the candidates (wave1 / high / medium / low / skip):
`thermo_models` 38 / 37 / 154 / 268 / 105 · CoolSolve examples 12 / 24 / 7 / 0 / 3 ·
`ht` 4 / 9 / 8 / 3 / 0 · ThermoCycle 1 / 1 / 2 / 3 / 14 · LaboThapPy 9 / 8 / 17 / 26 / 14 ·
TESPy 8 / 8 / 23 / 13 / 0.

Refresh with `python3 tools/build_index.py` (models) and
`python3 tools/backlog_stats.py` (candidates).

### Where to resume (handover, 2026-10-09, 20:00)

- **State:** B-01 … B-10 are closed. **Open batches:**
  - **B-11** (ULiège wave1/high, cards C-140…C-159): all 16 [hard] cards done; open the 4 [std] cards
    `C-140`, `C-146`, `C-156`, `C-157`, then the review `C-160`, and the taxonomy review `C-139` (M2, P6.2).
  - **B-12** (LaboThapPy + TESPy wave1/high, C-170…C-192): done `C-170` … `C-177`, `C-183`; open `C-178` … `C-182`,
    `C-184` … `C-192` (`C-189` [hard]; dependencies `C-185` after `C-180`, `C-191` after `C-184`), then the review
    `C-193`. Worker notes: `b11_extra.txt` / `b12_extra.txt` in `~/llm/scripts/csl/`.
  - After that: plan the next batches from the backlog (`thermo_models` medium, LaboThapPy/TESPy medium) with a
    T-PLAN card as C-137/C-138 did (notes `b11_plan.txt`, `b12_plan.txt`).
- **Work paused by the maintainer on 2026-10-09 at 20:00.** No task is running, the supervisor and the event watcher
  are stopped (`python3 ~/llm/scripts/oc-orch.py up` restarts the supervisor; the opencode server may still run:
  `down --server` stops it). Partial attempts are archived in `~/git/csl-lanes/_results/` (`C-178_bunny_t169`: no
  model yet — restart the card from scratch). Next free IDs: `CSL-0168`, card `C-194`.
- **Worker availability when paused:** z.ai `glm-5.3-flash` weekly limit until **2026-10-14 09:25 CEST** (15:25
  UTC+8; it also has a 5-hour usage window); the opencode free quota (shared by all free models) was exhausted at
  11:00 on 2026-10-09 after ≈ 1.5 h of work and had not come back by 20:00 — it looks like a daily allowance.
  Probe before dispatching: `bash ~/llm/scripts/csl/probe.sh <model> 0`.
- **Queue for the next session (in order):** B-12 `C-178` … `C-182`, `C-184`, `C-185`, `C-186` … `C-188`, `C-189`
  [hard → glm-5.3-flash if back], `C-190`, `C-191`, `C-192`; B-11 `C-140`, `C-146`, `C-156`, `C-157`; reviews
  `C-139`, `C-160`, `C-193`. Routing: [hard] → glm-5.3-flash, [std] → the one opencode worker (bunny, else muse).
- **Worker models, in order of priority** (details, benchmark and lessons:
  `~/Nextcloud/llm/opencode-model-comparison.md`):
  1. z.ai `glm-5.3-flash` — main worker, given the hardest cards (maintainer, 2026-10-07: **never the full
     `glm-5.3`, only the flash model**);
  2. opencode `space-bunny-free` — best free worker; check its gap claims and its header length.
  **Only one opencode (free) worker at a time (maintainer, 2026-10-07/08): space-bunny or muse-spark** — the free
  quota is shared by all free models of the account. Replacements only: `mimo-v2.6-flash-free`,
  `longcat-2.5-preview-free`, `ling-3.1-flash-free` (qualified by the C-10 benchmark), `muse-spark-1.3`.
  Not to be used: `nemotron-3-ultra-free` (fabricated a model), `nemotron-3.5-lightning-free` (overwrote an
  inventory, false gap), `fledge-alpha-free`, `ling-3.0-flash-fin-free` (unavailable). A new model runs the C-10
  benchmark first (`bench_c10_prep.sh`, scored by `bench_score.py`).
- **Lanes:** the cards run in isolated lanes, one per worker model (`~/git/csl-lanes/<lane>`: a copy of the library
  + a CoolSolve folder of symlinks with a private `docs/`), merged 3-way into the main trees by
  `~/llm/scripts/csl/csl.py merge`. `roadmap.md` and the generated index files are never merged from a lane; stray
  files outside the library folders are ignored; **source inventories are merged row by row** (only the rows a
  worker changed; row deletions and decision resets are ignored and logged). IDs are pre-assigned in the card lines.
  The supervisor is capped at 2 parallel tasks (`oc-orch.py config --max-parallel 2`: glm + one opencode worker).
- **Orchestrator loop per card:** `csl.py check <lane>` (folder, **header lines** — rule ≤ ≈ 20, flagged > 25 —,
  build_index, test_models, files changed) → for ULiège imports `src_check.py TM-xxxx <folder>` (equation overlap
  with the extracted EES source, zip members handled, + `compare_solution.py` summary) → review new register rows
  (`diff` of the lane register with the main one: duplicates are folded into the existing ID, rows without
  valid-EES evidence move to §8, cheap claims are reproduced with a 3-line file) → `csl.py save` → `csl.py merge` →
  `ls models/*/*/*/*.lane-*` (conflicts) → `csl.py tick C-xx "C-xx \`CSL-xxxx\`" "<result>"` → next dispatch.
  Corrections go back to the same worker with `oc-orch.py send <task> "<message>"` (it keeps its context).
  Waiting: `cd ~/llm/scripts/csl && python3 wait_event.py; python3 ../oc-orch.py beat; bash glm_probe.sh 30` in the
  background (never kill it with `pkill -f` on a pattern that matches the calling shell).
- **Pending CoolSolve suggestions** not in the register: §8 *Unverified by a reviewer* of
  `~/git/CoolSolve/docs/model_library_support.md`. Bugs reproduced by the orchestrator in this run (priority for a
  CoolSolve agent): `CS-BUG-PI-FUNCTION` (`pi` = 1 in a body, silent), `CS-BUG-CONVERT-UNIT`
  (`convert('lbm/hr','kg/s')` = 1), `CS-BUG-DUPLICATE-INDEX-EXPR` (`T[i+1]` in DUPLICATE), `CS-BUG-DUPLICATE-VAR-BOUND`
  (DUPLICATE with a variable bound dropped), `CS-BUG-NO-SOL-DELETE`, `CS-BUG-LOOKUP-WRITE`, `CS-BUG-COMMON-PROC`,
  `CS-BUG-HASH-IDENT`, `CS-BUG-LOOKUP-COL-ARG`, `CS-BUG-IMPLICIT-PROC`, `CS-BUG-NEWTON-CYCLE`.
- **Repository state:** library committed by the maintainer up to `3f0caaf` (working tree clean at the pause);
  CoolSolve `docs/model_library_support.md` modified by the register rows since `7addbbc` (to commit in CoolSolve).
- **CoolSolve:** use the `main` build `~/git/CoolSolve/build/coolsolve` (`536d427`, docs-only commits since).
  Blocked native files list their gaps in `model.json` (`missing_features`). After a CoolSolve release:
  `T-RECHECK` (workflow §6).
- **Regression:** `python3 tools/test_models.py --coolsolve ~/git/CoolSolve/build/coolsolve`
  (absolute path) solves the main file of every runnable model **and every variant that has a `.sol` next to it**;
  `--exclude CSL-0009:coolsolve` (3 min of integration) for a quick run: 150 targets, 0 failure on 2026-10-09.
- **For the maintainer:** `solar/SETP.LIB` (TM-0591, textbook code of *Solar
  Engineering of Thermal Processes*) is `parked` — publication/licence question;
  pipe friction and two-phase pressure drop are not in `ht` but in its companion
  library [`fluids`](https://github.com/CalebBell/fluids) — clone and triage it if
  wanted; authors still `TBD` in a few models; figures to make (`build_index.py` lists
  them); the taxonomy recommendations at M1 (P6.2).
- **Decisions of the C-14 review** (workflow updated): (1) variants get a
  regression baseline from their sibling `.sol` (workflow §6); (2) the
  `$UnitSystem` line of `ees_extract.py` and `CS-GAP-UNITSYSTEM` as an error:
  recommendation in Phase 5; (3) decoded embedded tables can be false
  positives: verify against the EES file (workflow §3, step 1).
  `tools/backlog_stats.py` now reports malformed inventory rows (an unquoted
  comma in a `notes` cell shifts `decision`/`library_id`; nine rows of B-01/B-02
  were repaired).
- **Earlier maintainer items (still open):** authors `TBD` in `CSL-0003`,
  `CSL-0004`, `CSL-0035` (the assistants named in `CSL-0009`/`CSL-0010` come from
  the inventory, not from the files — same course, choose one policy).
- **Open items of the C-38 review (B-03):** (`CSL-0036`, rearranged by its
  worker, was reworked to the original equations after the review, see §8.) `CSL-0034`: whether EES accepts a
  multi-output `PROCEDURE` in function position (`cpbar`) stays an unverified
  suggestion. `CSL-0028`: the EES `volume(AirH2O,…,w=…)` of `humidair2.EES` is
  0.96 % below the ideal-gas value (unexplained, to check in EES). Authors still
  `TBD` for `CSL-0035` too.
- **How the batches were executed:** one card per worker, one worker at a time
  in B-01, then parallel lanes (see *Lanes*; the orchestrator merges, ticks the
  cards and writes §8), by an orchestrating Claude Code session dispatching to
  opencode workers (maintainer's local set-up: skill
  `~/llm/skill-opencode-orchestrator.md`, helpers `~/llm/scripts/csl/`, see their
  README). Review cards were Claude Sonnet agents up to B-04; since B-05 they are
  light scripted reviews by the orchestrator (build_index, test_models,
  backlog_stats, inventory cross-check, spot checks); Claude agents only for an
  obvious problem or an A/B comparison of two workers, and new sources are explored
  by opencode workers (T-TRIAGE cards), not by Claude. A card takes 5–30 min of
  worker time. Any worker (person or agent) can instead take the next card with the
  prompt of §7.

---

## 2. How the work is organised

- **One step = one task card** (one model, one group of near-duplicate
  candidates, one function library…), executed with the procedure of
  [docs/model_workflow.md](docs/model_workflow.md) and closed when its
  *definition of done* is met: model folder + README + `model.json`, index
  rebuilt without errors, regression test passing (runnable models),
  inventory decision recorded, one line in the progress log (§8). **A model
  that cannot run is done too**, as a documented `blocked`, `failing` or `stub`
  model.
- **Cards are grouped in batches** of 5–15 cards, prepared by the manager from
  the inventories (`python3 tools/backlog_stats.py --next <source> 10`) and
  listed in §6. Each batch ends with a review card: run the checks, read the
  diffs, update §1, refine this roadmap, the workflow and the templates. Since
  B-04 (maintainer decision) the review card is a light scripted check by the
  orchestrator (`build_index`, `backlog_stats`, `test_models`, inventory
  decisions, worker final messages); a deep review by a Claude Sonnet agent is
  used only for an obvious problem or to compare two workers on the same card.
- **Per-candidate progress lives in the inventories** (`sources/*/inventory.csv`,
  columns `decision` and `library_id`), not in this file. The roadmap keeps
  phases, batches and decisions; the inventories keep the hundreds of
  candidates. (`sources/thermo_models/sweep.py` preserves these two columns
  when it is re-run.)
- **Workers**: people or agents (agents: Sonnet-class models, at most two in
  parallel, on different categories, one card at a time — §7).
- **Decisions on candidates** follow the decision tree of
  [docs/model_workflow.md §2](docs/model_workflow.md#2-triage-add-merge-replace-or-discard):
  discard what is not a usable model; park what may not be published; add what
  is new; merge parameter variants into the existing model; supersede when the
  candidate is better (same ID); keep different levels of detail as separate,
  linked models.
- **CoolSolve gaps** are reported in the CoolSolve gap register — only with
  evidence that the EES syntax is valid and a minimal reproducer in valid EES —
  and never worked around by rewriting valid EES code in the native file
  (CoolSolve must read native EES); the affected models are `blocked`, ship a
  separate verified runnable variant when a faithful one exists (regression
  tested as `CSL-xxxx:variant`), and are re-checked when CoolSolve closes the
  gap ([workflow §6](docs/model_workflow.md#6-coolsolve-gaps-blocked-models-and-re-checks)).

### Task card format (used in §6)

```
[ ] C-<nn>  <type>  <candidate id(s)>  → <category>/<suggested name>  — <purpose / notes>
```
Types: `T-TRIAGE`, `T-IMPORT`, `T-FUNC`, `T-TRANSLATE`, `T-MERGE`, `T-RECHECK`,
`T-GAP`, `T-TAXO`, `T-TOOL`, `T-REVIEW` (definitions in the workflow document).

---

## 3. Phases

| Phase | Goal | Status |
|---|---|---|
| 0 | Foundations: repository, taxonomy, templates, tooling, EES import methodology, pilot model | ✅ done |
| 1 | Source inventories and triage set-up | 🔄 in progress |
| 2 | Pilot wave B-01: one card per type of case; adjust the workflow (milestone M1 ≈ 15 models) | ✅ done (14 cards, review `C-14` 2026-10-05) |
| 3 | Production waves, source by source and category by category (M2 = 100, M3 = 300 models) | 🔄 in progress (3A: batches B-02, B-03) |
| 4 | Advanced tracks: dynamic, optimisation/identification, research-grade models | ☐ |
| 5 | CoolSolve integration (browser, import of functions, gap closure) | ☐ (CoolSolve side) |
| 6 | Quality, maintenance and releases | ☐ continuous |

### Phase 0 — Foundations ✅

- [x] P0.1 Repository initialised: MIT license (with third-party clause), README, `.gitignore`, folder structure
- [x] P0.2 Taxonomy: `taxonomy.json`, [docs/taxonomy.md](docs/taxonomy.md) — categories, kinds (steady / dynamic / optimisation / function), complexity levels 1–4 with scoring rubric and icons, status codes, permanent IDs, safe re-organisation rules
- [x] P0.3 Templates (`templates/model/`): README, `model.json`, `.eescode` header; `.eescode` style guide
- [x] P0.4 Library tools: `tools/build_index.py` (validation; `library.csv`, `library.json`, `functions.csv`, `CATALOG.md`, `redirects.csv`; next free ID; `retired.csv`), `tools/test_models.py` (regression against committed `.sol`), `tools/backlog_stats.py`
- [x] P0.5 EES import methodology and tools in CoolSolve: `docs/ees_import.md`; `tools/ees_extract.py` (equations cp1252/RTF, European decimal comma, unit settings, guesses, stored solution, lookup and parametric tables — run on all 457 EES files of the ULiège collection); `tools/compare_solution.py` (with EES-unit conversion). Tested on three files: SI model with parametric table, lookup-table model (blocked), K/kPa/kJ model (unit conversion)
- [x] P0.6 CoolSolve support document and gap register: CoolSolve `docs/model_library_support.md` (library browser, function import, gaps and bugs found during the tests)
- [x] P0.7 Pilot model `CSL-0001` refrigeration cycle with a simple compressor model (faithful import verified against the EES parametric table, then corrected; merges the CoolSolve example `compressor_refrigeration_simple`; diagram-ready state arrays)
- [x] P0.8 Maintainer decisions applied (§4): no source files in the library (`original/`, `reference/` removed, enforced by `build_index.py`), licences, exams, manual unit conversion (CoolSolve `docs/ees_import.md` §6), figure step tested in the CoolSolve GUI on `CSL-0001`

### Phase 1 — Inventories and triage set-up 🔄

- [x] P1.1 Sweep of the ULiège collection → `sources/thermo_models/` (552 rows incl. models inside zip archives, 118 duplicate groups, 341 distinct models; origins and licensing per sub-folder)
- [x] P1.2 Sweep of LaboThapPy → `sources/labothappy/` (74 candidates, Apache-2.0)
- [x] P1.3 Sweep of TESPy → `sources/tespy/` (52 candidates, MIT, strong reference results)
- [x] P1.4 Inventory of the CoolSolve examples → `sources/coolsolve_examples/`
- [x] P1.5 Inventories normalised: `decision`/`library_id` columns; `thermo_models` enriched with the decoded unit system, stored solution and embedded tables; student file names redacted (42 exam submissions, `discarded`)
- [x] P1.6 Taxonomy v0.2 from the sweep (instrumentation category, broader descriptions, tags for control and parameter identification, mapping from inventory categories to folders)
- [x] P1.7 Maintainer decisions recorded (§4) and applied to the inventories (`license_status = own` for the whole local collection; exam questions of August 2022 grouped into one example)
- [ ] P1.8 Cross-source map (`T-TRIAGE`): CoolSolve examples ↔ their EES originals (`CoolSolve/misc/EES_ok.zip`) ↔ `thermo_models` groups (e.g. `rankine1` ↔ DG-0106/`TM-0443`, `scroll_compressor` ↔ `TM-0481`, `condenser_3zones` ↔ `TM-0266`, `cpbar` ↔ `TM-0253`) ↔ LaboThapPy/TESPy overlaps (semi-empirical scroll machines, ε-NTU exchangers, heat pumps, ORC)
- [ ] P1.9 Function backlog (`T-FUNC` cards): `cpbar` (TM-0253, CSX-013), `BrineProp`/`BrineProp2` (TM-0479/0480, needed by 7 models), EES library pipe procedures (`Colebrook`), LaboThapPy correlation families (void fraction, plate HX, parabolic-trough losses, R1233zd(E) conductivity), TESPy ε-NTU relations

### Phase 2 — Pilot wave ✅

Run the full workflow once on each type of case (CoolSolve example + EES
original, unit conversion, merge of a family, function library, copied
functions, semi-empirical model, multi-zone model with RAD trigonometry,
dynamic, optimisation, blocked, embedded lookup table, TESPy and LaboThapPy
translations), then adjust the workflow, templates and tools. Batch B-01 in §6.

Outcome (review `C-14`): 14 models (10 verified; 4 blocked, each with a
verified runnable variant); workflow updated with the procedure for blocked
models (runnable variant, regression of variants, evidence required to
register a gap), the check of decoded tables, the style rules (comments, SI
units, EES fluid names) and the inventory rules; `test_models.py` tests the
variants; `backlog_stats.py` validates the inventories; the taxonomy and the
templates are unchanged apart from comment lines.

### Phase 3 — Production waves 🔄

1. **3A CoolSolve examples** — the remaining 43 physical models (12 wave1,
   24 high, 7 medium), each paired with its EES original when it exists:
   batches B-02… of ~10 cards. Fast, builds the core of verified models.
2. **3B ULiège collection**, sub-folder by sub-folder and category by
   category: *thermodynamique appliquée* (2022–23, very well documented),
   Quoilin's ORC/expander models, the model bank reference models,
   *machines et systèmes thermiques* (92 distinct models), the Laborelec
   toolkit, the engine course (MCI) and the KU Leuven exercises. Within a
   sub-folder: wave1 → high → medium; low/skip candidates are only triaged, in
   bulk, by duplicate group (exams included, D4).
3. **3C Function libraries** (P1.9).
4. **3D LaboThapPy** (9 wave1, 8 high) and **3E TESPy** (8 wave1, 8 high)
   translations, using the reference results of the sources for verification.

Milestones trigger a taxonomy review (P6.2): **M1** ≈ 15 models (end of
B-01, done in `C-14`), **M2** = 100, **M3** = 300.

### Phase 4 — Advanced tracks ☐

- **4A Dynamic models** (`kind = dynamic`): `TM-0095`, `TM-0104`, `TM-0413`,
  `TM-0490` (storage tanks, borefield); CoolSolve examples `ice_storage_tank`,
  `engine_weibe_cycle`, `building_rc_network` (blocked by
  `CS-GAP-INTEGRAL-LOOKUP`).
- **4B Optimisation and identification** (`kind = optimization` or tag
  `parameter identification`): `TM-0101` (EES Min/Max), `TM-0268`, `TM-0290`,
  `TM-0293`, `TM-0295` (error minimisation); LaboThapPy PSO sizing scripts
  are out of scope until CoolSolve has an optimiser (`CS-GAP-OPTIM`). Import at
  the optimum found by EES and document the optimisation problem.
- **4C Research-grade models** (level 3–4): `TM-0274` (inverter heat pump,
  560 equations, 57 functions), `TM-0314` (low-temperature ORC with charge),
  `TM-0494` (condensing boiler), CoolSolve `orc_complex`, `orc_solar_complex`;
  provide simplified variants and curated initials.

### Phase 5 — CoolSolve integration ☐ (tracked in the CoolSolve repository)

Integration design (CoolSolve `docs/model_library_support.md` §2): every
CoolSolve build **embeds the library as it is at compile time**
(`CS-FEAT-LIB-EMBED`) and serves it in an **HTML model explorer**
(`CS-FEAT-EXPLORER`); models import the functions and procedures of any
library model or `.eescode` file with `$INCLUDE library:<name>`
(`CS-FEAT-IMPORT`, no `.lib` files). Order: (1) snapshot + minimal explorer,
(2) imports, (3) library regression in CI, CLI, *Export for EES*.

Gaps and bugs to close first for the library: quick wins
`CS-BUG-LOOKUP-PATH`, `CS-BUG-INTERP-DESC`, `CS-DOC-TRIG` (✅ fixed 2026-10-05,
with the B-01 bugs); then the dynamic-model gaps found in B-01 (`CS-GAP-IF5`,
`CS-GAP-INTEGRAL-LIMITS`, `CS-BUG-INTEGRAL-TABLE-SEP`,
`CS-BUG-INTEGRAL-MAXSTEPS`, `CS-BUG-INTEGRAL-FACTOR`; they block `CSL-0009`
and `CSL-0010`); then native EES `INTERPOLATE` (`CS-GAP-INTERP-EES`) and
`$INCLUDE` (`CS-GAP-INCLUDE`; `CSL-0011`), the `$if` directives, `LOOKUP$ROW`
and string-keyed lookup tables (`CS-GAP-IF-DIRECTIVE`, `CS-GAP-LOOKUPROW`,
`CS-BUG-LOOKUP-STRING`; `CSL-0012`), an error on non-default `$UnitSystem`
(`CS-GAP-UNITSYSTEM`; library models carry no `$UnitSystem` line), unquoted unit names (`CS-GAP-CONVERT-UNQUOTED`),
comments in procedure argument lists (`CS-GAP-PROC-COMMENT`). After each
CoolSolve release: `T-RECHECK` of the blocked models; once `$INCLUDE` exists,
replace the copied function blocks of library models by `$INCLUDE` lines
(`T-MERGE` batch).

Library-side contract, already in place: `library.json` carries the snapshot
identity (content hash of exactly the embedded files, model and function
counts) and the function index; function names are unique; figures are at
most 100 kB.

**Recommendations of the B-01 review (`C-14`) for the CoolSolve repository**
(nothing was changed in CoolSolve by the library review):

- `tools/ees_extract.py`: **drop the line that writes a `$UnitSystem`
  directive** (the block "make the EES settings explicit"): the library workflow
  deletes it and no library model carries one. And make `CS-GAP-UNITSYSTEM` an
  **error** (not a warning) for a non-default `$UnitSystem`: a model in
  kPa/kJ/K must not run silently with wrong results.
- `tools/ees_extract.py`, embedded tables: fix the string-keyed lookup decoder
  (`CS-BUG-EXTRACT-LOOKUP-STRING`); report decoded tables as *unverified* when
  their size is not corroborated by the equations; decode the integral or
  parametric table from the plot objects when present (TM-0413: 18 001 rows).
- `CS-FEAT-LIB-TEST` (library regression in CoolSolve CI): apply the rule of
  `tools/test_models.py` — solve the main file of every runnable model **and
  every `*.eescode` that has a sibling `.sol`** (runnable variants of blocked
  models), so that variants stay green until the gap is closed.
- **Pending list — unverified gap suggestions** (reported by workers without
  evidence that the EES syntax is valid; **not** in the register; to check in
  EES, then register with a reproducer in valid EES or drop; workflow §6):
  `CS-GAP-PROC-MULTIOUT` (a multi-output `PROCEDURE` used inside an expression,
  seen in C-10 / `CSL-0011`: CoolSolve answers "cannot be called as a
  function"); `QUALITY()` above the dome (the stored solution of
  `EES_ok/orc_r245fa.EES` holds `x = 100` at a superheated state, CoolSolve
  returns 0; seen in C-19 / `CSL-0019`, needs a minimal EES run).
- **CoolSolve examples to correct** (found while importing; the library models
  follow the EES originals): `examples/refrigeration_compressor.eescode` line 94
  (`V_dot_su_2 = M_dot_1*v_1_2`: `M_dot_1` should be `M_dot_2`, `CSL-0022`);
  `examples/turbocompressor.eescode` (imposes `r_p_i = 1.25` instead of
  `r_p_i = p_2/p_1`, `CSL-0023`); `examples/cooling_coil.eescode` (simplified
  transcription with provisional values, `CSL-0017`).

### Phase 6 — Quality and maintenance (continuous) ☐

- [ ] P6.0 **Maintainer track** (continuous, after each batch): `T-FIGURE` for the runnable models without figure and completion of the `TBD` authors — both lists are printed by `python3 tools/build_index.py`
- [ ] P6.1 Continuous integration (GitHub Actions): `build_index.py --check`, `test_models.py` with the latest CoolSolve release
- [ ] P6.2 Taxonomy reviews at M1, M2, M3 (split crowded categories — `compressors`, `refrigeration_heat_pumps` and `fundamentals` already hold 60–90 candidates; bump the taxonomy version)
  - **M1 review (`C-14`, 2026-10-05; 24 models in 15 of the 31 leaf categories): taxonomy v0.2 kept, nothing restructured.** The taxonomy covered every case of B-01/B-02 without a new category. Recommendations for the maintainer, to apply at M2 (the ~40-model rule is not reached yet; models are `compressors` 6, `heat_exchangers` 3, `refrigeration_heat_pumps` 3, each other category 1):
    - **`components/compressors`** (52 distinct candidates, 30 wave1/high/medium; already 6 models) is the first to split: `positive_displacement` (piston 9, scroll 5, screw 5, rotary) and `turbomachines` (centrifugal/axial 16); keep two-point identification as the tag `parameter identification` (3 of the 6 models), not as a category.
    - **`cycles/refrigeration_heat_pumps`** (65): split `heat_pumps` (23 titles) from `refrigeration` (chillers, cabinets); 17 titles mention an evaporator or a condenser: route such models to `components/heat_exchangers` when the component, not the cycle, is the main object (existing rule).
    - **`fundamentals/processes`** (48 candidates in `fundamentals`; a keyword scan finds first-law balances 9, second law/exergy 6, ideal-gas processes 3): split by topic at M2 once the models are in.
    - **`hvac`** (42): the three sub-categories fit (cooling towers 19, coils 15). Make the rule explicit: equipment (coils, air-handling units) → `air_handling`, towers → `cooling_towers`, `psychrometrics` = humid-air states and processes without equipment; `CSL-0016` (moist-air coil, contact factor) is the borderline case — move it to `air_handling` at M2 if the maintainer agrees (`CSL-0017` is there).
    - **Mapping table of `docs/taxonomy.md`**: ideal-gas *cycles* (Brayton, Otto…) go to `cycles/gas_turbines` or `cycles/engines`, not to `fundamentals/processes` (single processes, first and second law) — the table says "cycles of ideal gases in exercises" for `fundamentals`; clarify before B-04 (3 candidates concerned).
    - Empty so far: `heat_transfer` (conduction, convection, radiation — 7 candidates, correlation libraries), `renewables`, `energy_systems` (8 each), `absorption_sorption` (3, blocked by the fluids `CS-GAP-FLUIDS-ABS`): keep, they match the backlog. Facets: no level-4 model yet (expected: Phase 4C); kinds dynamic/optimization/function hold 4 models: the facet works and needs no change.
- [ ] P6.3 Library releases: tag the library before each CoolSolve release (CoolSolve pins `COOLSOLVE_LIBRARY_TAG`; `docs/versions.md` records it, as for CoolProp)
- [ ] P6.4 Quality passes: figures (T-s, P-h diagrams) for level 1–2 models, homogeneous naming, README completeness, English paraphrase of textbook statements
- [ ] P6.5 Tooling backlog: `.lkt` decoder in `ees_extract.py`; unit-conversion assistant (kPa/kJ/K → Pa/J/°C); `move_model.py` (git mv + `previous_paths` + rebuild); README results tables and figures generated from `.sol`; use the 326 Python/CoolProp solutions of *thermodynamique appliquée* as extra verification references

---

## 4. Decisions and open questions

Decisions of the maintainer (2026-10-04), applied in the documents and tools:

| # | Decision |
|---|---|
| D1 | **No source files in the library.** A model folder holds only the CoolSolve files, its README, `model.json` and `figures/`. The source is referenced by its path (with `~` for the home directory), its URL, or its name in an existing library. Extraction data live in a temporary work folder (`work/`, git-ignored), deleted after the inclusion. |
| D2 | **Local collection**: every file comes from the maintainer's laboratory and is published under the library license (MIT). Authors are taken from the files; initials: `SB` = Stéphane Bertagnolio, `VL` = Vincent Lemort; unknown authors are written `TBD` and completed by the maintainer. |
| D3 | **Third-party libraries** (LaboThapPy, TESPy): their permissive licenses allow the translation; the translated models are published under the library license with full credits to the authors of the original model. |
| D4 | **Exams** are published as examples (not as exams). An exam built on an exercise with a few values changed is a `duplicate` of that exercise; an exam split in several question files describing one system becomes one example model. Student answers are excluded. |
| D5 | **Unit systems**: a model written in another unit system is converted **by hand**, equation by equation, to SI-°C-Pa-J (procedure: CoolSolve `docs/ees_import.md` §6). |
| D6 | **Figures**: the maintainer runs every included model in CoolSolve and adds a thermodynamic diagram or a relevant plot to its README (`T-FIGURE`, workflow §7). Workers make the models diagram-ready (state arrays) and leave a placeholder. |
| D7 | **Ideal-gas and humid-air models** get a parametric sweep plot as figure until CoolSolve offers ideal-gas diagrams and a psychrometric chart (`CS-FEAT-DIAGRAM-IDEAL`, `CS-FEAT-PSYCHRO`). |
| D8 | **Inventories are published** in the repository, including `sources/thermo_models/` (they may be deleted later; keeping them in the history is fine). |
| D9 | **Commits are made by the maintainer.** Workers and agents never commit: they leave their changes in the working tree for review. |
| D10 | **`MODULE` and `SUBPROGRAM` are flattened** (2026-10-05). CoolSolve will not implement them in the near future (`CS-GAP-MODULE`, not planned): the equations of each module call are flattened into the main program of the library model, the module's internal variables renamed per call (`<variable>_<tag>`), the mapping logged in the header and README; the flattened file is the main model file (valid EES), status according to its verification (workflow §6). |
| D11 | **Property calls with the (T, H) input pair are rewritten** (2026-10-05). The (T, H) input pair will not be added to CoolProp/CoolSolve (`CS-GAP-PROP-TH`, not planned): such calls are rewritten in the model itself with an equivalent (P, H) call — saturation pressure from T for a known two-phase state, or an auxiliary pressure unknown defined by `h = enthalpy(fluid, T, P)` — each rewrite logged; the rewritten file is the main model file, status according to its verification (workflow §6). |

Open questions (from the `C-14` review, for the maintainer):

1. **Authors from the inventory.** `CSL-0009` and `CSL-0010` name the course
   assistants found in the inventory (not in the EES files); `CSL-0003` and
   `CSL-0004` of the same course stay `TBD`. Choose one policy (names only when
   written in the file, or the course teaching staff for all).
2. **Licence of translated models.** `origin.license` holds the library licence
   (MIT) for every model; the original licence of a translation (LaboThapPy:
   Apache-2.0) appears only in the README *Source* row. Add an
   `origin.original_license` field if the library browser should show it.
3. **Taxonomy at M2:** the recommendations of P6.2 (split `compressors` and
   `refrigeration_heat_pumps`, clarify `hvac` and ideal-gas cycles).

---

## 5. Backlog (source inventories)

| Source | Inventory | Summary | Main characteristics |
|---|---|---|---|
| ULiège collection `thermo_models` | [inventory](sources/thermo_models/inventory.csv) | [README](sources/thermo_models/README.md) | 341 distinct models; strong in engines, compressors, refrigeration/heat pumps, fundamentals, HVAC; thin in heat transfer, solar, absorption, storage, buildings. 288 of 540 EES files in SI-C-Pa-J; 230 in decimal-comma format; stored EES values (full or partial solution) in all of them |
| CoolSolve examples | [inventory](sources/coolsolve_examples/inventory.csv) | [README](sources/coolsolve_examples/README.md) | 39 of 45 tested examples solve; 19 have their EES original in `CoolSolve/misc/EES_ok.zip` |
| LaboThapPy | [inventory](sources/labothappy/inventory.csv) | [README](sources/labothappy/README.md) | Components (constant-efficiency, semi-empirical, ε-NTU, moving boundary), correlation libraries, cycles; few reference results |
| TESPy | [inventory](sources/tespy/inventory.csv) | [README](sources/tespy/README.md) | Component equations with doctests, validated plants (CGAM, SEGS vs Ebsilon, sCO2 state table) |
| ThermoCycle | [inventory](sources/thermocycle/inventory.csv) | [README](sources/thermocycle/README.md) | Modelica, 665 files: 441 infrastructure and 123 dynamic models excluded; 7 steady candidates (solar receiver and collector fits, expander/pump maps, flow-boiling and in-cylinder correlations); no stored reference results |

---

## 6. Batches

### B-01 — Pilot wave (Phase 2) ✅


```
[x] C-01  T-IMPORT     CSX-016 + EES_ok/exchangers1.EES   → components/heat_exchangers/counterflow_hx_oil_water        — CoolSolve example + EES original (L1)
[x] C-02  T-IMPORT     TM-0380                            → fundamentals/properties/methane_tank_evaporation           — K/kPa/kJ + decimal comma (tested in ees_import.md, Example 3)
[x] C-03  T-TRIAGE+IMPORT DG-0106 (TM-0443) + CSX-036 + EES_ok/rankine1.EES → cycles/steam_power/rankine_cycle_60mw     — merge of one exercise in several versions/unit systems
[x] C-04  T-FUNC       TM-0253 + CSX-013                → fundamentals/combustion/cpbar_combustion_products          — function library from a .LIB
[x] C-05  T-IMPORT     CSX-004 (+CSX-005, TM-0492)      → components/boilers_burners/boiler_mean_specific_heat       — model using copied library functions (after C-04)
[x] C-06  T-IMPORT     CSX-042 + EES_ok/scroll_compressor.EES + TM-0481 → components/compressors/scroll_compressor_semi_empirical — semi-empirical reference model
[x] C-07  T-IMPORT     CSX-008 + TM-0266 group          → components/heat_exchangers/condenser_three_zones           — level 3, procedures, initials, EES RAD setting
[x] C-08  T-IMPORT     TM-0413                            → components/storage/dhw_tank_dynamic                        — dynamic (INTEGRAL), 761-row time series as reference
[x] C-09  T-IMPORT     TM-0101 (fallback TM-0422)       → components/compressors/…                                    — optimisation (EES Min/Max) imported at the optimum
[x] C-10  T-IMPORT     TM-0150 (DG-0032)               → cycles/gas_turbines/two_shaft_gas_turbine_compressor_map   — blocked case (CS-GAP-INTERP-EES, CS-GAP-INCLUDE), ees_import.md Example 2 — NEXT: two attempts interrupted (usage limit), nothing kept; restart from scratch; CS-BUG-LOOKUP-PATH/INTERP-DESC now fixed
[x] C-11  T-IMPORT     TM-0326                            → buildings/thermal_comfort_pmv_ppd                          — embedded lookup table (74×2)
[x] C-12  T-TRANSLATE  TSP-035                            → cycles/refrigeration_heat_pumps/heat_pump_basic_tespy      — TESPy tutorial, verified against its results
[x] C-13  T-TRANSLATE  LTP-013                            → components/heat_exchangers/hx_constant_pinch               — LaboThapPy component
[x] C-14  T-REVIEW     B-01                                                                                              — update workflow/templates/tools, taxonomy check (M1)
```

### B-02 — CoolSolve examples, first production batch (Phase 3A) ✅

Prepared 2026-10-05 from `python3 tools/backlog_stats.py --next coolsolve_examples 12` (wave1 and high,
steady first). Each card follows the C-01 pattern: the CoolSolve example plus its EES original in
CoolSolve `misc/EES_ok.zip` (when it exists) as the verification reference, and the same exercise looked up in
the `thermo_models` inventory (cross-source map P1.8). IDs are pre-assigned because lanes run in parallel.

```
[x] C-15  T-IMPORT     CSX-038 (+EES original)          → cycles/refrigeration_heat_pumps/…                     — basic R134a refrigeration cycle (L1), link CSL-0001/CSL-0013 — CSL-0015
[x] C-16  T-IMPORT     CSX-021 (+EES original)          → hvac/psychrometrics/…                                  — moist-air cooling coil, contact factor (L1) — CSL-0016
[x] C-17  T-IMPORT     CSX-010 (+EES original)          → hvac/air_handling/…                                    — chilled-water cooling coil, dry and wet regimes (L2) — CSL-0017
[x] C-18  T-IMPORT     CSX-035 (+EES original)          → heat_transfer/pressure_drop/…                          — pipe pressure drop, Colebrook-White (L1; P1.9 Colebrook function) — CSL-0018
[x] C-19  T-IMPORT     CSX-031 (+EES original)          → cycles/organic_rankine/…                               — simple ORC, R245fa, imposed component performance (L3) — CSL-0019
[x] C-20  T-IMPORT     CSX-002 (+EES original)          → components/compressors/…                               — dry air screw compressor with internal leakage (L2) — CSL-0020
[x] C-21  T-IMPORT     CSX-034 (+EES original)          → components/compressors/…                               — piston compressor, parameter identification from two points (L2) — CSL-0021
[x] C-22  T-IMPORT     CSX-041 (+EES original)          → components/compressors/…                               — refrigeration compressor identification from two points (L2) — CSL-0022
[x] C-23  T-IMPORT     CSX-044 (+EES original)          → components/compressors/…                               — centrifugal turbocompressor performance (L2) — CSL-0023
[x] C-24  T-IMPORT     CSX-014 (+EES original)          → cycles/engines/…                                       — single-cylinder engine, Weibe combustion, crank-angle INTEGRAL (L3, dynamic) — CSL-0024
[x] C-25  T-REVIEW     B-02                                                                                      — checks, diffs, §1, workflow/templates; model comparison update
```

### B-03 — CoolSolve examples, second production batch (Phase 3A) ✅

Prepared 2026-10-05 (`backlog_stats.py --next coolsolve_examples 20`): the remaining level 1–3 steady
examples; same notes as B-02. Left for B-04: CSX-023 and CSX-006 (dynamic), CSX-019 (MODULE), CSX-028,
CSX-029, CSX-047 (level 3–4), CSX-046 (LiBr-water).

```
[x] C-26  T-IMPORT     CSX-039 (+EES original)          → cycles/refrigeration_heat_pumps/                    — R22 heat pump cycle, 30 kW (L1) — CSL-0025
[x] C-27  T-IMPORT     CSX-017 (+EES original)          → components/heat_exchangers/                         — crossflow HX, hot gas heating water (L1) — CSL-0026
[x] C-28  T-IMPORT     CSX-018 (+EES original)          → components/heat_exchangers/                         — 1-2 shell-and-tube steam condenser (L1) — CSL-0027
[x] C-29  T-IMPORT     CSX-022 (+EES original)          → hvac/air_handling/                                  — air handling unit, moist-air conditioning (L1) — CSL-0028
[x] C-30  T-IMPORT     CSX-037 (+EES original)          → cycles/steam_power/                                 — steam Rankine cycle with regenerative extraction (L2), link CSL-0004 — CSL-0029
[x] C-31  T-IMPORT     CSX-011 (+EES original)          → hvac/cooling_towers/                                — two-speed cooling tower (L2) — CSL-0030
[x] C-32  T-IMPORT     CSX-015 (+EES original)          → components/heat_exchangers/                         — refrigeration evaporator with moist air, wet regime (L2) — CSL-0031
[x] C-33  T-IMPORT     CSX-009 (+EES original)          → components/heat_exchangers/                         — wet air-cooled condenser, spray evaporative cooling (L2) — CSL-0032
[x] C-34  T-IMPORT     CSX-020 (+EES original)          → cycles/refrigeration_heat_pumps/                    — R22 heat pump with semi-hermetic compressor model (L2) — CSL-0033
[x] C-35  T-IMPORT     CSX-026 (+EES original)          → cycles/engines/                                     — internal combustion engine cycle with cpbar (L2), uses CSL-0005 cpbar — CSL-0034
[x] C-36  T-IMPORT     CSX-045 (+EES original)          → components/compressors/                             — centrifugal compressor with lookup-table map (L2), after C-23 (CSL-0023) — CSL-0035
[x] C-37  T-IMPORT     CSX-030 (+EES original)          → cycles/organic_rankine/                             — ORC with two-stage expander and extraction, R134a (L3) — CSL-0036
[x] C-38  T-REVIEW     B-03                                                                                      — checks, diffs, §1, workflow; plan B-04 (remaining examples: dynamic, L3–L4, absorption)
```

### B-04 — CoolSolve examples, last batch (Phase 3A) ✅

Prepared 2026-10-05: the remaining CoolSolve examples (dynamic, levels 3–4, MODULE, absorption);
same notes as B-02. C-39 is the first application of decision D10 (MODULE flattened).

```
[x] C-39  T-IMPORT     CSX-019 (+EES original)          → components/expanders_turbines/                      — scroll expander semi-empirical model; MODULE → flatten (decision D10, first case) (L3) — CSL-0037
[x] C-40  T-IMPORT     CSX-028 (+EES original)          → cycles/organic_rankine/                             — transcritical/supercritical CO2 power cycle, polynomial correlations (L3) — CSL-0038
[x] C-41  T-IMPORT     CSX-047 (+EES original)          → cycles/refrigeration_heat_pumps/                    — Zorlu geothermal plant, heat pump with PCM storage (L3) — CSL-0039
[x] C-42  T-IMPORT     CSX-029 (+EES original)          → cycles/organic_rankine/                             — complex ORC with procedures and lookup tables (L4; provide curated initials) — CSL-0040
[x] C-43  T-IMPORT     CSX-023 (+EES original)          → components/storage/                                 — ice storage tank discharge with phase change (dynamic, L2) — CSL-0041
[x] C-44  T-IMPORT     CSX-006 (+EES original)          → buildings/                                          — 3R2C building thermal network, weather lookup (dynamic, CS-GAP-INTEGRAL-LOOKUP) (L2) — CSL-0042
[x] C-45  T-IMPORT     CSX-046 (+EES original)          → cycles/absorption_sorption/                         — LiBr-water absorption properties exercise (L2) — CSL-0043
[x] C-46  T-REVIEW     B-04                                                                                      — checks, diffs, §1; close Phase 3A (all CoolSolve examples triaged); plan Phase 3B
```

### B-05 — ULiège collection, *thermodynamique appliquée* (Phase 3B) ✅

Prepared 2026-10-05: the wave1 candidates of the sub-folder plus two high ones (inventory filter:
path `thermodynamique appliquee/…`, representative, `todo`). Most files are in kPa/kJ (hand conversion, D5);
the course's Python/CoolProp solutions are extra verification references (P6.5). Worker notes:
`~/llm/scripts/csl/b05_extra.txt` (maintainer set-up).

```
[x] C-47  T-IMPORT     TM-0378 (DG-0088)                → fundamentals/properties/                            — rigid tank with a liquid-vapour water mixture (L1, kPa) — CSL-0044
[x] C-48  T-IMPORT     TM-0389 (DG-0093)                → fundamentals/processes/                             — steam turbine exergy balance (L1) — CSL-0045
[x] C-49  T-IMPORT     TM-0393 (DG-0095)                → fundamentals/combustion/                            — octane combustion with 400 % theoretical air (L1, kPa) — CSL-0046
[x] C-50  T-IMPORT     TM-0399 (DG-0097)                → fundamentals/properties/                            — non-ideal gas v(P+k/v²)=RT, isothermal work (L1, molar units) — CSL-0047
[x] C-51  T-IMPORT     TM-0382 (DG-0091)                → fundamentals/processes/                             — two R12 tanks connected by a valve (L1, kPa) — CSL-0048
[x] C-52  T-IMPORT     TM-0429 (DG-0102)                → cycles/engines/                                     — air-standard Otto cycle (L2, kPa) — CSL-0049
[x] C-53  T-IMPORT     TM-0441 (DG-0105)                → cycles/gas_turbines/                                — land-based two-shaft gas turbine (L2, kPa), link CSL-0011 — CSL-0050
[x] C-54  T-IMPORT     TM-0442                          → cycles/gas_turbines/                                — ideal turbojet at 260 m/s (L1, kPa) — CSL-0051
[x] C-55  T-IMPORT     TM-0446                          → cycles/gas_turbines/                                — combined gas-steam cycle (L2, kPa) — CSL-0052
[x] C-56  T-IMPORT     TM-0416 (DG-0084)                → cycles/steam_power/                                 — elementary steam power plant (L2, kPa), link CSL-0004 — CSL-0053
[x] C-57  T-IMPORT     TM-0449 (DG-0109)                → cycles/refrigeration_heat_pumps/                    — R410A heat pump with evaporator air side (L2, kPa) — CSL-0054
[x] C-58  T-IMPORT     TM-0451 (DG-0111)                → hvac/psychrometrics/                                — moist air in a room: humidity ratio, dew point (L1, kPa) — CSL-0055
[x] C-59  T-REVIEW     B-05                                                                                      — checks, diffs, §1, unit conversions, use of the Python references; plan B-06
```

### B-06 — *thermodynamique appliquée* (high) and the last CoolSolve examples (Phase 3B/3A) ✅

Prepared 2026-10-05: the high-priority candidates left in *thermodynamique appliquée* (notes as B-05) and
three CoolSolve examples left `todo` by C-46 (notes as B-02; CSX-033 `orc_solar_complex` goes to Phase 4C).

```
[x] C-60  T-IMPORT     TM-0388 (DG-0092)                → fundamentals/processes/                             — hot iron block quenched in a water tank (L1, kPa) — CSL-0056
[x] C-61  T-IMPORT     TM-0390 (DG-0094)                → fundamentals/processes/                             — maximum work from two air tanks at 900 K and 300 K (L1, kPa) — CSL-0057
[x] C-62  T-IMPORT     TM-0395 (DG-0096)                → fundamentals/combustion/                            — diesel engine excess air from exhaust gas analysis (L2, kPa) — CSL-0058
[x] C-63  T-IMPORT     TM-0431 (DG-0103)                → cycles/engines/                                     — ideal Stirling cycle with regenerator, INTEGRAL (L2, kPa) — CSL-0059
[x] C-64  T-IMPORT     TM-0435 (DG-0104)                → cycles/gas_turbines/                                — gas turbine with reheat (L2, kPa) — CSL-0060
[x] C-65  T-IMPORT     TM-0450 (DG-0110)                → cycles/refrigeration_heat_pumps/                    — domestic refrigerator-freezer, R134a (L2, kPa) — CSL-0061
[x] C-66  T-IMPORT     TM-0396                          → hvac/air_handling/                                  — condensate ratio and dry-air flow at a 7 kW cooling coil (L2, kPa) — CSL-0062
[x] C-67  T-IMPORT     TM-0452 (DG-0112)                → hvac/psychrometrics/                                — mixing of room and outdoor air, conditioning process (L1, kPa) — CSL-0063
[x] C-68  T-IMPORT     TM-0453                          → hvac/psychrometrics/                                — mixing with condensation in the mixer (L1, kPa) — CSL-0064
[x] C-69  T-IMPORT     TM-0454                          → hvac/cooling_towers/                                — cooling tower for condenser water (L1, kPa), link CSL-0030 — CSL-0065
[x] C-70  T-IMPORT     TM-0455                          → hvac/psychrometrics/                                — adiabatic saturation and wet-bulb temperature (L1, kPa) — CSL-0066
[x] C-71  T-IMPORT     CSX-025 (+EES original)          → components/compressors/                             — piston compressor with inlet pressure drop and internal leak (L2) — CSL-0067
[x] C-72  T-IMPORT     CSX-040 (+EES original)          → cycles/refrigeration_heat_pumps/                    — scroll compressor heat pump, data consistency check (L2) — CSL-0068
[x] C-73  T-IMPORT     CSX-043 (+EES original)          → components/compressors/                             — centrifugal compressor design and similarity (L2; the example fails to solve: debug) — CSL-0069
[x] C-74  T-REVIEW     B-06                                                                                      — light scripted review (orchestrator)
```

### B-07 — ULiège model data bank (Phase 3B) ✅

Prepared 2026-10-05: the wave1 candidates of `Model data bank` (reference RefSim/ParamID component
models), plus TM-0472 and the BrineProp function library (P1.9). Worker notes: `~/llm/scripts/csl/b07_extra.txt`.

```
[x] C-75  T-IMPORT     TM-0475                          → hvac/air_handling/                                  — adiabatic humidifier, simplified model (L1) — CSL-0070
[x] C-76  T-IMPORT     TM-0251                          → components/pumps_fans/                              — centrifugal fan RefSim model (L1) — CSL-0071
[x] C-77  T-IMPORT     TM-0487                          → components/pumps_fans/                              — centrifugal brine pump RefSim model (L1) — CSL-0072
[x] C-78  T-IMPORT     TM-0472                          → hvac/air_handling/                                  — cooling coil with control, simplified model (L1) — CSL-0073
[x] C-79  T-IMPORT     TM-0471                          → hvac/air_handling/                                  — cooling coil RefSim model, dry and wet regimes (L2), link CSL-0017 — CSL-0074
[x] C-80  T-IMPORT     TM-0255                          → components/instrumentation/                         — ISO 5167 orifice plate flow-rate procedure (L2) — CSL-0075
[x] C-81  T-IMPORT     TM-0489                          → hvac/cooling_towers/                                — direct-contact cooling tower reference model (L2) — CSL-0076
[x] C-82  T-IMPORT     TM-0488                          → cycles/refrigeration_heat_pumps/                    — air-cooled water chiller reference model (L2) — CSL-0077
[x] C-83  T-IMPORT     TM-0495                          → cycles/refrigeration_heat_pumps/                    — brine-to-water heat pump reference model (L2) — CSL-0078
[x] C-84  T-FUNC       TM-0479 (DG-0115)                → fundamentals/properties/                            — BrineProp library: secondary-refrigerant properties (needed by 7 models, P1.9) — CSL-0079
[x] C-85  T-IMPORT     TM-0494                          → components/boilers_burners/                         — condensing boiler reference model, five-step combustion (L3; Phase 4C) — CSL-0080
[x] C-86  T-IMPORT     TM-0490                          → components/heat_exchangers/                         — vertical ground-loop heat exchanger (borefield), dynamic (L3; Phase 4A) — CSL-0081
[x] C-88  T-RECHECK    CSL-0061, CSL-0068 (decision D11)  → (in place)                                          — rewrite the (T, H) property calls with (P, H) in the main file, drop the native/variant split, re-verify
[x] C-87  T-REVIEW     B-07                                                                                      — light scripted review (orchestrator)
```

### B-08 — ThermoCycle translations (Phase 3E-like) ✅

Prepared 2026-10-05 from the ThermoCycle triage (`sources/thermocycle/`, Claude Sonnet): dynamic models and
infrastructure excluded; the five steady-state cards that bring something new. No reference results are stored in the
repository: verification from the papers, a Python/CoolProp re-evaluation and energy balances. Source defects to
correct and document are listed in `sources/thermocycle/README.md` §8. Worker notes: `~/llm/scripts/csl/b08_extra.txt`.

```
[x] C-89  T-TRANSLATE  THC-001  → renewables/solar_thermal/parabolic_trough_receiver_forristal    — steady 1D radial receiver balance (glass, vacuum annulus, wind, sky); verify vs NREL/TP-550-34169, PTR70 heat-loss test, energy-balance closure — CSL-0082
[x] C-90  T-FUNC       THC-002  → renewables/solar_thermal/parabolic_trough_loss_correlations     — Schott PTR70, Sopogy, Soltigua efficiency fits (with LTP-050/LTP-020); verify vs NREL report, datasheets, C-89 — CSL-0083
[x] C-91  T-FUNC       THC-003  → components/expanders_turbines/orc_expander_pump_empirical_maps  — isentropic-efficiency and filling-factor maps (hermetic scroll, open-drive scroll, screw) and pump curves, small ORC demo; verify by Python/CoolProp re-evaluation — CSL-0084
[x] C-92  T-FUNC       THC-004  → heat_transfer/convection/flow_boiling_htc_shah_gungor_cooper    — Shah 1982, Gungor-Winterton, Cooper (after LTP-034/035); verify vs the original papers, Python/CoolProp — CSL-0085  **superseded by C-107** (ht HT-012 is more complete; C-107 adds Shah 1982 / Gungor-Winterton / Cooper from THC-004 if ht lacks them)
[x] C-93  T-FUNC       THC-005  → heat_transfer/convection/in_cylinder_htc_correlations           — Annand, Woschni, Adair, Destoop, Irimescu, Kornhauser (low priority; DTU copyright of the source package to check); verify vs papers, Python — CSL-0086
[x] C-94  T-REVIEW     B-08                                                                                      — light scripted review (orchestrator)
```

### B-09 — Heat-transfer and pressure-drop correlations from `ht` (Caleb Bell) ✅

Maintainer request (2026-10-05): import all the correlations of the Python library
[`ht`](https://github.com/CalebBell/ht) (C. Bell, MIT; local clone `~/git/ht`, commit `85e0ee6`) — convection,
boiling, condensation, heat-exchanger relations, pressure drop… Rules:

- each correlation becomes an EES `FUNCTION` (or `PROCEDURE`), called as an example from the main program of the
  library file where it is implemented (the file solves and is regression-tested);
- correlations that are very similar or describe the same physical process share one `.eescode` file (one card per
  file/family);
- **cite both** the original paper/book of the correlation and the `ht` library (version, module, function) from
  which the equations were taken (comment block of each function, README, `model.json`);
- verification against the `ht` doctests / Python functions.

The exploration of `ht` is itself a worker card (C-95) that writes `sources/ht/` (README + inventory, one row per
family); the translation cards C-96…C-119 come from its result (2026-10-05: 24 families, 222 functions; 23 selectors and 27 table/helper functions excluded). Pipe friction factors and two-phase pressure drop are **not** in `ht` — they live in the companion library [`fluids`](https://github.com/CalebBell/fluids) (not cloned); `ht` only provides the shell-side (HT-017) and air-cooler (HT-013) pressure drops. Worker notes: `~/llm/scripts/csl/b09_triage.txt`,
`~/llm/scripts/csl/b09_extra.txt`.

```
[x] C-95  T-TRIAGE     ht (CalebBell)                     → sources/ht/                                            — list and group the correlations of ht into families (one future .eescode file each); 24 families / 222 functions → C-96…C-119
[x] C-96  T-FUNC       HT-001   → heat_transfer/convection/internal_turbulent_nusselt            — turbulent and turbulent-entry internal Nu (Dittus-Boelter … Bhatti-Shah, Gnielinski) (23 functions, wave1); verify vs ht doctests + Python — CSL-0087
[x] C-97  T-FUNC       HT-002   → heat_transfer/convection/nucleate_boiling_and_chf              — pool nucleate boiling heat flux (9) + critical heat flux (Zuber, Serth-HEDH, HEDH-Montinsky) (12 functions, wave1); verify vs ht doctests + Python — CSL-0088
[x] C-98  T-FUNC       HT-003   → heat_transfer/convection/condensation_film                     — film condensation: Nusselt plate, Boyko-Kruzhilin, Akers-Deans-Crosser, kinetic correction, Cavallini, Shah (6 functions, wave1); verify vs ht doctests + Python — CSL-0089
[x] C-99  T-FUNC       HT-004   → components/heat_exchangers/hx_effectiveness_ntu                — Cmin/Cmax/Cr, NTU↔UA, eps(NTU, Cr) and NTU(eps, Cr) for counterflow, parallel, crossflow, boiler/condenser (8 functions, wave1); verify vs ht doctests + Python — CSL-0090
[x] C-100 T-FUNC       HT-005   → heat_transfer/convection/internal_laminar_and_curved_nu        — laminar (T_wall and q_wall), thermal entry region, rectangular duct, spiral/helical curved ducts (10 functions, high); verify vs ht doctests + Python — CSL-0091
[x] C-101 T-FUNC       HT-006   → heat_transfer/convection/free_conv_cylinders                   — 10 vertical-cylinder + 3 horizontal-cylinder free-convection correlations (13 functions, high); verify vs ht doctests + Python — CSL-0092
[x] C-102 T-FUNC       HT-007   → heat_transfer/convection/free_conv_plates_and_sphere           — Churchill-Chu vertical plate, McAdams/VDI/Rohsenow horizontal plate, Churchill sphere (5 functions, high); verify vs ht doctests + Python — CSL-0093
[x] C-103 T-FUNC       HT-008   → heat_transfer/convection/external_crossflow_cylinder           — single-cylinder crossflow (Zukauskas … Whitaker, Perkins-Leppert) (8 functions, high); verify vs ht doctests + Python — CSL-0094
[x] C-104 T-FUNC       HT-009   → heat_transfer/convection/tube_bank_nusselt                     — tube-bank Nu and row/angle correction factors (Grimison, Zukauskas, ESDU 73031, HEDH) (7 functions, high); verify vs ht doctests + Python — CSL-0095
[x] C-105 T-FUNC       HT-010   → components/heat_exchangers/plate_hx_heat_transfer              — plate HX single-phase Nu (Kumar, Martin, Muley-Manglik, Khan-Khan) + 5 plate two-phase boiling correlations (9 functions, high); verify vs ht doctests + Python — CSL-0096
[x] C-106 T-FUNC       HT-011   → heat_transfer/convection/two_phase_nonboiling_in_tube          — in-tube two-phase non-boiling HTC (Groothuis-Hendal, Martin-Sims, Hughmark, Aggour …) (9 functions, high); verify vs ht doctests + Python — CSL-0097
[x] C-107 T-FUNC       HT-012   → heat_transfer/convection/flow_boiling_in_tubes                 — flow and film boiling in tubes (Lazarek-Black, Li-Wu, Thome, Chen, Liu-Winterton …) (8 functions, high); verify vs ht doctests + Python — CSL-0098 (also covers THC-004, see C-92)
[x] C-108 T-FUNC       HT-013   → heat_transfer/convection/air_cooler_air_side                   — finned-bundle air-side HTC and dP (Briggs-Young, ESDU low/high fin, Ganguli-VDI) + 2 air-cooler noise correlations (8 functions, high); verify vs ht doctests + Python — CSL-0099
[x] C-109 T-FUNC       HT-014   → heat_transfer/convection/free_conv_enclosed_and_jackets        — enclosed plates, critical Rayleigh numbers, helical coils in tanks, vessel jackets (12 functions, medium); verify vs ht doctests + Python — CSL-0100
[x] C-110 T-FUNC       HT-015   → heat_transfer/convection/external_forced_conv_plates           — laminar/turbulent forced convection over a flat plate (4 functions, medium); verify vs ht doctests + Python — CSL-0101
[x] C-111 T-FUNC       HT-016   → components/heat_exchangers/hx_temperature_effectiveness_pntu   — P-NTU temperature effectiveness: TEMA E/G/H/J, plate, air cooler + the inverse NTU(P) relations (15 functions, medium); verify vs ht doctests + Python — CSL-0102
[x] C-112 T-FUNC       HT-017   → heat_transfer/pressure_drop/tube_bank_dp_bell_delaware         — shell-side dP (Kern, Zukauskas) + Bell-Delaware Jc, Jl, Jb, Js, Jr (7 functions, medium); verify vs ht doctests + Python — CSL-0103
[x] C-113 T-FUNC       HT-018   → heat_transfer/convection/supercritical_internal_nu             — near-supercritical internal convection (McAdams, Jackson, Swenson, Kitoh, Petukhov …) (18 functions, medium); verify vs ht doctests + Python — CSL-0104
[x] C-114 T-FUNC       HT-019   → components/heat_exchangers/lmtd_and_f_correction               — LMTD, Fakheri F correction, air-cooler Ft (3 functions, medium); verify vs ht doctests + Python — CSL-0105
[x] C-115 T-FUNC       HT-020   → heat_transfer/conduction/conduction_resistances_and_shapes     — cylindrical/plane-wall resistance, 6 shape factors, R-value conversions (14 functions, medium); verify vs ht doctests + Python — CSL-0106
[x] C-116 T-FUNC       HT-021   → heat_transfer/radiation/radiation_heat_flux                    — blackbody spectral radiance, radiant heat flux with back-radiation, grey transmittance (3 functions, medium); verify vs ht doctests + Python — CSL-0107
[x] C-117 T-FUNC       HT-022   → heat_transfer/convection/packed_bed_nusselt                    — packed-bed forced convection (4 functions, low); verify vs ht doctests + Python — CSL-0108
[x] C-118 T-FUNC       HT-023   → heat_transfer/convection/fin_efficiency_and_wall_factors       — circular-fin efficiency, wall correction factors for Nu and for frictional dP (3 functions, low); verify vs ht doctests + Python — CSL-0109
[x] C-119 T-FUNC       HT-024   → components/heat_exchangers/shell_and_tube_sizing               — tube counts, bundle diameters, TEMA clearances, baffle thickness, unsupported length (13 functions, low); verify vs ht doctests + Python — CSL-0110
[x] C-120 T-REVIEW     B-09                                                                                      — light scripted review (orchestrator)
```








---

### B-10 — New files in the ULiège collection (2026-10-06) ✅

The maintainer added EES files to `~/Nextcloud/thermo_models` (2026-10-06). `sweep.py` now keeps the TM/DG IDs stable
(a path already inventoried keeps its ID, existing rows are kept as they are, new files are appended): 50 new rows
TM-0553…TM-0602 (`procedures EES/` 32, `Steady-state models/` 10, `optim/` 4, `solar/` 4); new files also joined 7
existing rows (new groups DG-0119…DG-0125). The triage card (C-121) decides what is new and worth importing and what is
skipped (duplicates and variants are frequent), and proposes the import cards C-122… (done 2026-10-06: 14 cards C-122…C-135, CSL-0111…0124; details in `sources/thermo_models/README.md` §8). Worker notes:
`~/llm/scripts/csl/b10_triage.txt` (triage), `~/llm/scripts/csl/b10_extra.txt` (import cards).

```
[x] C-121 T-TRIAGE     TM-0553…TM-0602                     → sources/thermo_models/                                 — triage of the 2026-10-06 additions (duplicate / merged / discarded / todo); 22 todo / 18 duplicate / 8 discarded / 1 merged / 1 parked (SETP.LIB, licence) → C-122…C-135
[x] C-122 T-FUNC   TM-0585,TM-0496                          → components/heat_exchangers/plate_hx_correlations        — plate-HX correlations: 10 procedures (bogaerts, han, hsieh, kumar, kuo, martin, muley, thonon, wanniarachchi, yan); verification: TM-0585 stored solution + ht HT-005/HT-010 Python values — CSL-0111
[x] C-123 T-FUNC   TM-0564,TM-0569,TM-0579,TM-0566,TM-0571  → components/heat_exchangers/three_zone_hx_procedures      — 7 procedures (hx_cd, hx_ev, lmtd, single_phase_HX, EV, CD, evaporator2); verification: TM-0564/TM-0569 demo cases (energy balance) + ht HT-004 epsilon-NTU — CSL-0112
[x] C-124 T-IMPORT TM-0563 → components/heat_exchangers/condenser_3_zones_plate_correlations — three-zone plate condenser, Thonon/Kuo, R123+glycol (REFPROP variant TM-0562 described); verification: EES stored solution — CSL-0113
[x] C-125 T-IMPORT TM-0570 (TM-0582 auto-size variant)      → components/heat_exchangers/evaporator_3_zones_plate_correlations — three-zone plate evaporator, Thonon/Hsieh, R245fa+glycol+oil; verification: EES stored solution + TM-0582 parametric table — CSL-0114
[x] C-126 T-IMPORT TM-0575                                  → components/heat_exchangers/hx_fem_evaporator_discretised  — discretised hxfem evaporator, smoothed revision of TM-0275; verification: EES stored solution — CSL-0115
[x] C-127 T-IMPORT TM-0596                                  → cycles/refrigeration_heat_pumps/heat_pump_vitocal_300g  — scroll compressor + two plate HXs (needs CSL-0079 + expander of TM-0597/CSL-0037); verification: EES stored solution — CSL-0116
[x] C-128 T-IMPORT TM-0565                                  → components/expanders_turbines/double_stage_scroll_expander — two-stage hermetic scroll expander (Lemort/Quoilin/Pire correlations, MODULE); verification: EES stored solution — CSL-0117
[x] C-129 T-IMPORT TM-0593                                  → components/valves_nozzles_piping/air_nozzle_ejector      — air ejector, choked primary nozzle + entrainment; verification: EES stored solution — CSL-0118
[x] C-130 T-IMPORT TM-0589                                  → renewables/solar_thermal/solar_geometry_sun_path         — solar geometry (declination, hour angle, altitude, azimuth, sunrise; `nDay_` to check); verification: EES stored solution — CSL-0119
[x] C-131 T-IMPORT TM-0588                                  → components/valves_nozzles_piping/ball_valve_authority   — equivalent opening diameter / valve authority from the ball angle; verification: EES stored solution + Idel'cik p.339 — CSL-0120
[x] C-132 T-FUNC   TM-0574                                  → fundamentals/properties/heat_transfer_fluid_properties     — prop_htf: MEG, Therminol VP-1/66, oil (companion of CSL-0079); verification: HEDH HTF-VP1 sheet values — CSL-0121
[x] C-133 T-FUNC   TM-0558,TM-0559,TM-0587,TM-0581           → components/instrumentation/nozzle_discharge_coefficients  — ASHRAE 41.2/ISO R859 (4 nozzles), ISO 5167 long radius, admission, range checker; verification: ISO 5167 part vs CSL-0075 + ASHRAE 41.2 — CSL-0122
[x] C-134 T-FUNC   TM-0560                                  → components/compressors/copeland_catalogue_correlation   — 3rd-order ARI/Copeland polynomial ZH38K4E-TFD (five 242×2 tables); verification: EES stored solution — CSL-0123  **Then:** CSL-0116 (Vitocal 300-G, C-127) is blocked partly by this missing catalogue table — add its runnable `_coolsolve` variant once the table is in the library.
[x] C-135 T-IMPORT TM-0554                                  → heat_transfer/pressure_drop/plate_hx_pressure_drop_identification — REFPROP mixtures, likely blocked; verification: EES stored solution — CSL-0124
[x] C-136 T-REVIEW     B-10                                                                                      — light scripted review (orchestrator)
```

### B-11 — ULiège collection: remaining wave1/high candidates (Phase 3B) ☐

22 representatives still `todo` at wave1/high (`modeles/` 12, model data bank 4, *machines et systèmes thermiques* 3,
MCI 3). The planning card triages them against the library and proposes the import cards (from C-140), each tagged
[hard] or [std] to route it: [hard] → glm-5.3-flash, [std] → the free worker (one opencode worker at a time,
bunny or muse — maintainer, 2026-10-08). Worker notes: `~/llm/scripts/csl/b11_plan.txt` (plan),
`~/llm/scripts/csl/b11_extra.txt` (imports from the ULiège collection).

```
[x] C-137 T-PLAN       thermo_models wave1/high (22)      → sources/thermo_models/                                 — triage vs the library and 22 rows: 20 todo / 2 merged → 20 cards C-140…C-159 (CSL-0148…0167; 15 [hard])
[ ] C-140 T-IMPORT TM-0042 (DG-0006) → cycles/refrigeration_heat_pumps/scroll_volume_ratio_cycle_r134a — [std] scroll built-in volume ratio vs isentropic efficiency and cycle COP (R134a, saturated); verification: EES stored solution (5/30 vars, dup-group copies) — CSL-0148
[x] C-141 T-IMPORT TM-0136 (DG-0029) → cycles/engines/gas_engine_complete_model — [hard] complete gas engine: throttle, carburettor, pressure drop, combustion, recuperator, water circuits (link CSL-0034); verification: EES stored solution (97/98) + external Lookup 1 — CSL-0149
[x] C-142 T-IMPORT TM-0231 → fundamentals/combustion/adiabatic_flame_dissociation — [hard] CH4/fuel-oil adiabatic flame temperature with/without dissociation (built-in Chem_Equil/NASA → blocked expected); verification: EES stored solution (26/28) — CSL-0150
[x] C-143 T-IMPORT TM-0235 → cycles/engines/engine_derating_iso3046 — [hard] engine derating per ISO 3046/1 (ambient P/T); verification: EES stored solution (17/17) — CSL-0151
[x] C-144 T-IMPORT TM-0240 → components/compressors/turbocharger_combustion_products — [hard] turbocharger matching with combustion products (SUBPROGRAM flatten D10, cpbar lib → CSL-0005); verification: EES stored solution (109/111) — CSL-0152
[x] C-145 T-IMPORT TM-0268 (DG-0122) → cycles/organic_rankine/orc_whr_refprop_cost — [hard] WHR ORC, scroll expander, REFPROP mixtures + cost model (CS-GAP-REFPROP → blocked; Thonon/Kuo/prop_htf → CSL-0113/0114/0121); verification: EES stored solution (386/386) — CSL-0153
[ ] C-146 T-IMPORT TM-0270 (DG-0059) → energy_systems/economics/investment_npv_payback — [std] NPV and simple payback of energy-saving investments; verification: parametric table1 (23x2) + EES stored solution (297/297) — CSL-0154
[x] C-147 T-IMPORT TM-0274 → cycles/refrigeration_heat_pumps/inverter_air_water_heat_pump — [hard] reversible inverter air-to-water heat pump (Daikin Altherma type), 560 eq, SUBPROGRAM flatten; verification: EES stored solution (226/492) — CSL-0155
[x] C-148 T-IMPORT TM-0277 (DG-0064) → components/compressors/refrigeration_screw_compressor_r22 — [hard] screw compressor reference model in an R22 cycle, full-load/part-load (kPa/kJ → convert); verification: EES stored solution (122/122) — CSL-0156
[x] C-149 T-IMPORT TM-0282 (DG-0066) → components/compressors/reciprocating_catalogue_r717 — [hard] reciprocating compressor from catalogue data: RPM/part-load maps (R717, DUPLICATE ≈399 eq; Copeland kin → CSL-0123); verification: EES stored solution (645/645) — CSL-0157
[x] C-150 T-IMPORT TM-0312 (DG-0073) → heat_transfer/pressure_drop/gas_pipe_insulated_pressure_drop — [hard] gas pipe pressure drop and heat gain: Colebrook, insulation, fittings (companion .LKT); verification: EES stored solution (52/52) — CSL-0158
[x] C-151 T-IMPORT TM-0314 (DG-0124) → cycles/organic_rankine/orc_void_fraction_charge — [hard] low-temperature ORC (R134a) with void-fraction charge of the heat exchangers; verification: EES stored solution (298/299) — CSL-0159
[x] C-152 T-IMPORT TM-0316 (DG-0075) → renewables/photovoltaics/pv_module_single_diode — [hard] PV module single-diode I-V curve (embedded 'PVModules' table; UW F-Chart provenance to clear first); verification: parametric table1 (20x2) + EES stored solution (3276/3284) — CSL-0160
[x] C-153 T-IMPORT TM-0319 (DG-0125) → components/heat_exchangers/plate_hx_thermal_resistances — [hard] single-phase plate HX resistance model (Martin), brine side via Brineprop2 (→ CSL-0111/CSL-0079); verification: EES stored solution (38/38) — CSL-0161
[x] C-154 T-IMPORT TM-0321 (DG-0076) → hvac/air_handling/glycol_runaround_recovery_loop — [hard] air-to-air glycol run-around heat-recovery loop (epsilon-NTU coils, Braun hypothesis, pump); verification: EES stored solution (144/144) — CSL-0162
[x] C-155 T-IMPORT TM-0470 → hvac/air_handling/cooling_coil_paramid — [hard] cooling-coil parameter identification (PARAMID reference; measured-data table 3335x2; → CSL-0074); verification: EES stored solution (79/92) + parametric Table 2 — CSL-0163
[ ] C-156 T-IMPORT TM-0474 (DG-0114) → hvac/air_handling/heating_coil_refsim — [std] heating-coil reference simulation model (RefSim; → CSL-0074); verification: EES stored solution (48/48) — CSL-0164
[ ] C-157 T-IMPORT TM-0485 → components/pumps_fans/centrifugal_fan_paramid — [std] centrifugal-fan parameter identification (ParamID reference; → CSL-0071); verification: EES stored solution (113/114) — CSL-0165
[x] C-158 T-IMPORT TM-0491 → components/boilers_burners/boiler_modulating_burner_refsim — [hard] boiler with modulating burner (MODULE flatten D10; cpbar → CSL-0005; 11840x2 table); verification: EES stored solution (116/116) + parametric table1 — CSL-0166
[x] C-159 T-IMPORT TM-0499 (DG-0117) → components/compressors/reciprocating_polynomial_r22 — [hard] reciprocating compressor reference in R22 cycle: polynomial modelling (bar/kJ → convert; → CSL-0022); verification: EES stored solution (102/102) — CSL-0167
[ ] C-160 T-REVIEW     B-11                                                                                      — light scripted review (orchestrator)
[ ] C-139 T-REVIEW     taxonomy at M2 (P6.2)                                                                       — 123 models: propose splits of crowded categories and the taxonomy version bump (maintainer decides)
```

### B-12 — LaboThapPy and TESPy: wave1/high translations (Phases 3D/3E) ☐

≈ 16 LaboThapPy and 15 TESPy candidates at wave1/high (pilots: C-12, C-13). The planning card triages them against
the library (overlaps with ULiège models, `ht` and ThermoCycle are frequent) and proposes the translation cards (from
C-170), tagged [hard]/[std]. Worker notes: `~/llm/scripts/csl/b12_plan.txt` (plan), `~/llm/scripts/csl/b12_extra.txt` (translation cards). Dependencies: C-185 after C-180 (Stodola cone law), C-191 after C-184 (combustion chamber), C-192 uses CSL-0121.

```
[x] C-138 T-PLAN       LaboThapPy + TESPy wave1/high      → sources/labothappy/, sources/tespy/                   — triage vs the library and 31 rows: 24 todo / 7 merged → 23 cards C-170…C-192 (CSL-0125…0147)
[x] C-170 T-TRANSLATE LTP-009 → components/pumps_fans/pump_curve_similarity — [std] pump from manufacturer curves + affinity laws, NPSH, 3 modes; verification: examples/pump/pump_curve_similarity_example.py re-run in a throw-away venv (Q~N, H~N^2 exact) — CSL-0125
[x] C-171 T-TRANSLATE LTP-011 → components/heat_exchangers/hx_constant_effectiveness — [std] enthalpy-based constant-effectiveness HX (recuperator/IHX/gas cooler); verification: hex_csteff_example.py + eta=1 cold-inlet self-check — CSL-0126
[x] C-172 T-TRANSLATE LTP-012 → components/heat_exchangers/hx_constant_effectiveness_discretised — [hard] pinch-limited discretised HX (sCO2 recuperator); verification: hex_csteff_disc_example.py (n_disc 100/Pinch 10 K, 20/0), min_i dT = Pinch — CSL-0127
[x] C-173 T-TRANSLATE LTP-014 → components/heat_exchangers/hx_eps_ntu_plate_pipe — [std] UA from plate/pipe geometry, wall+fouling, Gnielinski; verification: TESPy test_labothappy_reference Q=3961.9 W, 295.54/296.98 K — CSL-0128
[x] C-174 T-TRANSLATE LTP-020 → renewables/solar_thermal/parabolic_trough_collector_discretised — [std] absorber marching over DUPLICATE cells with the Soponova map; verification: collector example (1-50 cells, 10 collectors) vs CSL-0083 — CSL-0129
[x] C-175 T-FUNC LTP-028 → heat_transfer/pressure_drop/pipe_pressure_drop_correlations — [std] 6 friction factors + Friedel/MSH/Choi dP, acceleration, gravity; verification: original papers (Churchill 1977, Friedel 1979, MSH 1986) — CSL-0130
[x] C-176 T-FUNC LTP-033 → heat_transfer/convection/void_fraction_correlations — [std] 13 void-fraction models; verification: void_fraction_example.py re-run in a venv + original papers/ACHP — CSL-0131
[x] C-177 T-FUNC LTP-048 → fundamentals/properties/r1233zd_thermal_conductivity — [std] R1233zd(E) conductivity (CoolProp has none); verification: Perkins & Huber 2017 coefficients (same source as the EES data) — CSL-0132
[ ] C-178 T-TRANSLATE LTP-055 → cycles/refrigeration_heat_pumps/heat_pump_propane_pinch — [std] propane pinch-based HP (IHX case = CSL-0039, cross-check only); verification: fpi_HeatPump_example.py (p_low/p_high, COP) + exact pinch — CSL-0133
[ ] C-179 T-TRANSLATE LTP-056 → cycles/organic_rankine/orc_preheated_recuperated_cyclopentane — [std] preheated+recuperated ORC, Zorlu site (correct the preheater-source bug); verification: fpi_orc_example.py re-run + CSL-0039 states — CSL-0134
[ ] C-180 T-TRANSLATE TSP-003 → components/expanders_turbines/turbine_stodola_offdesign — [std] Stodola cone law + efficiency characteristic; verification: doctest P=-10 452 574 W, x=0.914; test_Turbine 28.8 t/h → 88.6 bar, eta 0.898 — CSL-0135
[ ] C-181 T-TRANSLATE TSP-006 → components/compressors/polynomial_compressor_en12900 — [std] EN12900 10-coeff. eta_is/eta_v polynomials + dissipation; verification: test_polynomial_compressor.py catalogue tables, Bitzer map; cross-check CSL-0123 — CSL-0136
[ ] C-182 T-TRANSLATE TSP-008,TSP-009 → components/heat_exchangers/hx_lmtd_ua — [std] UA/smoothed-LMTD HX with ttd+pinch specs (Condenser as _condenser variant); verification: test_HeatExchanger/test_Condenser doctests — CSL-0137
[x] C-183 T-TRANSLATE TSP-014 → components/heat_exchangers/hx_moving_boundary_bell — [hard] Bell 2015 moving boundary (zone UA, area constraint); verification: bell2015_five_cases.json Q 452-4582 W (0.1 %/0.5 K) — CSL-0138
[ ] C-184 T-TRANSLATE TSP-022 → fundamentals/combustion/combustion_chamber — [std] fuel/air stoichiometry, lambda, flue-gas species; verification: test_combustion.py + cgam-ebsilon-results.csv — CSL-0139
[ ] C-185 T-TRANSLATE TSP-034 → cycles/steam_power/rankine_cycle_part_load — [std] Rankine + cooling water + motor/generator + part load (needs C-180); verification: rankine.py re-run 13.21/0.224/33.69 MW, eta 38.6 %, x 0.866 — CSL-0140
[ ] C-186 T-TRANSLATE TSP-036 → cycles/gas_turbines/gas_turbine_open_cycle — [std] open Brayton with combustion chamber + generator; verification: gas_turbine.py re-run in a venv, blocks vs the CGAM reference — CSL-0141
[ ] C-187 T-TRANSLATE TSP-037 → energy_systems/district_heating/district_heating_loop — [std] DH loop: consumer, feed pump, pipes with dP and heat loss; verification: district_heating.py re-run + loop energy balance — CSL-0142
[ ] C-188 T-TRANSLATE TSP-040 → cycles/steam_power/rankine_cycle_two_extractions — [std] HP/MP/LP plant, two closed FWHs, drains (sweep replaces pymoo); verification: optimization_example.py re-run + balances — CSL-0143
[ ] C-189 T-TRANSLATE TSP-042 → cycles/gas_turbines/sco2_recompression_brayton — [hard] sCO2 recompression, 2 sectioned recuperators; verification: Penkuhn & Tsatsaronis 2018 table (st.1 35 C/75 bar, st.4 600 C/250 bar) — CSL-0144
[ ] C-190 T-TRANSLATE TSP-044 → cycles/refrigeration_heat_pumps/refrigeration_co2_transcritical_booster — [std] CO2 booster supermarket cycle; verification: co2_cycle.ipynb re-run (13/26/32/57.3 bar, 25/75 kW) — CSL-0145
[ ] C-191 T-TRANSLATE TSP-050 → energy_systems/cogeneration/cgam_cogeneration — [std] CGAM cogeneration benchmark (needs C-184); verification: cgam-ebsilon-results.csv, comp 29.66 / turb 59.66 MW < 0.5 % — CSL-0146
[ ] C-192 T-TRANSLATE TSP-051 → cycles/steam_power/segs_solar_power_plant — [hard] SEGS 7-stage plant, 5 FWHs, cooling tower (needs CSL-0121); verification: Ebsilon 31.769 MW, T(c79) 296.254 C — CSL-0147
[ ] C-193 T-REVIEW     B-12                                                                                      — light scripted review (orchestrator)
```

## 7. Dispatching a batch to agents

Prompt for a worker agent (one card per agent; several agents in parallel only
on cards that touch different categories, inventories and pre-assigned IDs, as
in B-02). Kept equal in content to the helper prompt of the maintainer's local
set-up (`~/llm/scripts/csl/base_prompt.txt`); refined during B-01:

```
You are a worker of the CoolSolve Library (~/git/CoolSolve_Library). The CoolSolve repository is ../CoolSolve
(its build, tools, sources and examples).
Read docs/model_workflow.md (procedure + definition of done), docs/taxonomy.md,
the existing model models/cycles/refrigeration_heat_pumps/refrigeration_cycle_simple_compressor/
(as an example of a finished model), and ../CoolSolve/docs/ees_import.md.
Execute this task card of roadmap.md §6:
  <card line from roadmap §6>
<card-specific notes: where the sources are, which group to triage, expected outcome>
Rules:
- Use the CoolSolve build ../CoolSolve/build/coolsolve and the CoolSolve tools
  ../CoolSolve/tools/ees_extract.py and compare_solution.py. The ULiège source collection is ~/Nextcloud/thermo_models
  (reference it as ~/Nextcloud/thermo_models/... in the model files).
- Do not modify other models, the taxonomy, roadmap.md or the CoolSolve sources. Report a CoolSolve gap or bug
  in ../CoolSolve/docs/model_library_support.md only with a minimal reproducer; first read the register and do not
  re-report registered gaps (reference their IDs instead).
- Never copy source files into the library (reference them by ~/ path, URL or library name); work in
  work/<name>/ and delete that folder at the end. Convert other unit systems by hand (ees_import.md §6).
- Edit inventory CSV rows minimally (only the decision/library_id cells of your rows; keep the file format
  byte-identical otherwise). Never run git checkout/reset/stash or revert files you did not create.
- Never copy student names or personal data. Do not commit (git). Do not ask questions: take the most
  reasonable decision, document it in the model README, and mention it in your final message.
- A model that cannot run is still done, as a documented blocked/failing/stub model.
- (T, H) property input pair (decision D11): rewrite such calls with an equivalent (P, H) call in the model itself
  (workflow §6) and log each rewrite.
- MODULE/SUBPROGRAM (decision D10): flatten their equations into the main program, renaming the module's internal
  variables per call (`<variable>_<tag>`), and log the mapping (workflow §6).
- Runnable variant: the rule "never rewrite valid EES code to work around a CoolSolve gap" applies to the native
  file only. When the native file is blocked and a faithful runnable transcription is possible, ship it as a separate
  documented variant `<name>_coolsolve.eescode` (+ .sol) verified against the EES reference, as models CSL-0009/CSL-0010.
- Never call CoolSolve-only syntax "valid EES". A new gap or bug may be registered only with evidence that the EES
  syntax/behaviour is valid (an EES manual/doc reference or an existing EES file that uses it) and a minimal reproducer;
  without such evidence, describe it in your final message as "unverified suggestion" and do not register it.
- model.json `missing_features` lists every registered gap ID that blocks the native file (those of the card included).
  In the inventory, also write a one-line reason in the `notes` cell of every row you decide on.
- Keep the explanatory comment at the top of the .eescode file short (about 10-20 lines); the details go in the
  README.md (maintainer, 2026-10-07).
- Comments must not invent physical meaning: paraphrase the original's own comments or write "as in the original";
  give dimensional quantities their SI unit (never `[-]`).
- EES fluid names: chemical formulas (CO2, N2, O2, H2O, Air) are IDEAL-GAS substances (enthalpy includes the
  formation enthalpy); real fluids use names (R744/CarbonDioxide, Nitrogen, Water, R134a, AirH2O for humid air).
  A CoolProp fluid in a Python source (e.g. 'CO2') therefore becomes the EES real-fluid name (R744) in a translation.
- A runnable variant changes only what the gap forces, keeps the variable names, and logs every change. Any claim
  "EES/CoolSolve cannot / does X" needs a minimal run or a file reference. For a blocked native file with lookup
  tables, ship its tables as EES expects them and separate companion tables for the variant, with agreeing defaults.
- Register rows: follow the column count of the register section you write in; reproducers in valid EES; tool bugs
  (ees_extract.py, compare_solution.py) also go in the register. Quote tolerances exactly as compare_solution.py prints.
- Time budget: aim to finish within about 25 minutes; prefer a documented, verified smaller result to an exhaustive one.
- Bookkeeping you must do: set the `decision` and `library_id` columns of the candidate rows in
  sources/*/inventory.csv; run `python3 tools/build_index.py` (0 errors) and
  `python3 tools/test_models.py <ID> --coolsolve ../CoolSolve/build/coolsolve` (must pass for runnable models).
Final message (short): model ID, folder, status, one-line log entry for roadmap §8, gaps reported (IDs),
suggested CoolSolve corrections, decisions taken / open questions.
```

The manager then checks the folder (README, `model.json`, `.eescode`, `.sol`,
variants), runs `python3 tools/build_index.py`,
`python3 tools/backlog_stats.py` (inventory rows well-formed: a `notes` cell with
a comma must be quoted) and
`python3 tools/test_models.py <ID> --coolsolve ../CoolSolve/build/coolsolve`
(variants of the model are tested too, as `<ID>:variant`), ticks the card in §6
and adds the log line in §8.

---

## 8. Progress log

| Date | Step | Result |
|---|---|---|
| 2026-10-04 | Phase 0 | Repository, taxonomy, templates, tools, EES import methodology and tools (CoolSolve), gap register created |
| 2026-10-04 | `CSL-0001` | Added *refrigeration_cycle_simple_compressor* — verified (faithful import vs EES ≤ 1.4 %), original corrected (superheated suction state); CoolSolve example `compressor_refrigeration_simple` merged |
| 2026-10-04 | P1.1–P1.6 | Inventories of the four sources (725 candidates), enrichment and sanitisation of `thermo_models`, taxonomy v0.2 |
| 2026-10-04 | P0.8, P1.7 | Maintainer decisions D1–D6 applied: source files and extraction data removed from `CSL-0001` and forbidden by `build_index.py`; licences set to `own`; exam rules; manual unit-conversion procedure; figure step tested on `CSL-0001` (P-h diagram of the R22 cycle with the state arrays, PNG export) |
| 2026-10-04 | C-01 `CSL-0002` | Added *counterflow_hx_oil_water* — verified vs the EES stored solution of `EES_ok/exchangers1.EES` (20/20 variables ≤ 0.03 %); CoolSolve example CSX-016 merged |
| 2026-10-04 | C-02 `CSL-0003` | Added *methane_tank_evaporation* — hand-converted from K/kPa/kJ and decimal comma, verified vs EES stored solution (≤ 3e-5 relative) |
| 2026-10-04 | C-03 `CSL-0004` | Added *rankine_cycle_60mw* — verified vs EES stored solution (40/40 ≤ 2e-5, hand kPa/kJ→Pa/J conversion); DG-0106 merged (TM-0519/TM-0547 duplicates, CSX-036 superseded); new gap CS-GAP-MULTILINE-COMMENT |
| 2026-10-04 | C-04 `CSL-0005` | Added *cpbar_combustion_products* — function library kept in native EES, **blocked**: matches EES ≤ 0.24 % only with workarounds; gaps CS-BUG-IF-IGNORED, CS-BUG-MOLARMASS, CS-BUG-SINGLE-INPUT-PAIR, CS-GAP-FORMATION-ENTHALPY, CS-GAP-UNITSYSTEM-FUNC reported |
| 2026-10-05 | C-05 `CSL-0006` | Added *boiler_mean_specific_heat* — **blocked** by the CSL-0005 bugs (CS-BUG-IF-IGNORED/MOLARMASS/SINGLE-INPUT-PAIR); `cpbar` copied from CSL-0005; physics verified vs EES TM-0492 (57/57 ≤ 0.1 %); CSX-005 merged as the on/off variant |
| 2026-10-05 | C-06 `CSL-0007` | Added *scroll_compressor_semi_empirical* — verified vs EES stored solution; CSX-042 and its EES original merged as converted variant, TM-0481 added |
| 2026-10-05 | C-07 `CSL-0008` | Added *condenser_three_zones* — level 3, verified vs EES stored solutions of the 3 originals (duties ≤ 0.23 %; RAD setting without trig: no conversion); DG-0060 merged (TM-0264/65 variants, TM-0258/59/60 duplicates), CSX-008 superseded; curated `.initials` required and shipped |
| 2026-10-05 | C-08 `CSL-0009` | Added *dhw_tank_dynamic* (first dynamic model, level 1) — native file **blocked** (CS-GAP-IF5, CS-GAP-INTEGRAL-LIMITS); runnable variant verified against the EES integral table recovered from the plot objects (18 001 points, ≤ 6.1e-5); new gaps CS-GAP-IF5, CS-GAP-INTEGRAL-LIMITS; bugs CS-BUG-INTEGRAL-TABLE-SEP, CS-BUG-INTEGRAL-MAXSTEPS reported |
| 2026-10-05 | C-09 `CSL-0010` | Added *two_stage_steam_compressor_intercooling* (optimisation, imported at the EES optimum) — native file **blocked**, transcription verified vs EES; bug CS-BUG-INTEGRAL-FACTOR reported |
| 2026-10-05 | T-RECHECK `CSL-0005`, `CSL-0006` | CoolSolve branch `fix/library-gaps` merged in CoolSolve main (CS-BUG-IF-IGNORED, CS-BUG-MOLARMASS, CS-BUG-SINGLE-INPUT-PAIR, CS-GAP-UNITSYSTEM-FUNC, CS-GAP-FORMATION-ENTHALPY, CS-GAP-MULTILINE-COMMENT, CS-BUG-LOOKUP-PATH, CS-BUG-INTERP-DESC, CS-DOC-TRIG fixed) — both models now **verified**; library regression 8/8 OK |
| 2026-10-05 | Convention | No `$UnitSystem` directive in library models (CoolSolve has a single unit system): removed from all `.eescode` files and the header template; workflow §3/§8/§9 updated; regression 8/8 OK |
| 2026-10-05 | C-10 `CSL-0011` | Added *two_shaft_gas_turbine_compressor_map* — native file **blocked** (CS-GAP-INTERP-EES, CS-GAP-INCLUDE); runnable `_coolsolve` (nominal) and `_ambient` (TM-0151) variants verified vs the EES stored solutions (≤ 1.6e-3, enthalpy reference offsets aside); DG-0032 triaged (TM-0151 merged as variant, TM-0149/0175/0176/0177 duplicates). Worker space-bunny, chosen over a muse-spark attempt after review; unverified gap suggestion CS-GAP-PROC-MULTIOUT kept out of the register (to check in EES) |
| 2026-10-05 | C-12 `CSL-0013` | Added *heat_pump_basic_tespy* (TESPy tutorial, MIT, F. Witte) — verified vs TESPy run at commit 19425523 (base case, 3 specification variants, 3×11-point COP sweeps ≤ 6e-9); worker muse-spark |
| 2026-10-05 | C-13 `CSL-0014` | Added *hx_constant_pinch* (LaboThapPy HexCstPinch condenser branch, Apache-2.0, B. Chaudoir, E. Neven, T. Janod) — verified vs the LaboThapPy COND_CO2 example (P_sat 0.33 %, pinch exact; Q 2.8 % traced to a bicubic-table artifact of the original); worker muse-spark (a first version wrongly reported CoolSolve `CO2` = ideal gas as a bug: EES-compatible, corrected to R744) |
| 2026-10-05 | C-15 `CSL-0015` | Added *refrigeration_cycle_basic_r134a* — verified vs EES_ok/refrigeration1.EES stored solution (derived results ≤ 0.013 %); CSX-038 merged (identical equations), TM-0448/0531/0549 duplicates; worker muse-spark |
| 2026-10-05 | C-16 `CSL-0016` | Added *moist_air_cooling_coil_contact_factor* (V. Lemort, 2005) — verified vs EES_ok/humidair1.EES stored solution (25/25; energies ≤ 0.43 %, humidity ratios +0.5 % CoolProp vs EES psychrometrics); CSX-021 imported; worker muse-spark |
| 2026-10-05 | C-17 `CSL-0017` | Added *chilled_water_cooling_coil* — verified vs the EES original TM-0077 (60/60 stored values, design results ≤ 0.07 %); CSX-010 (simplified transcription) and TM-0077 imported, TM-0075/76/80/82 duplicates; curated `.initials`; worker muse-spark |
| 2026-10-05 | C-18 `CSL-0018` | Added *pipe_pressure_drop_colebrook* (n-pentane, Colebrook-White) — verified vs EES_ok stored solution (ΔP ≤ 0.5 %, viscosity/Re ≤ 5.7 % EES vs CoolProp transport properties); CSX-035 merged, TM-0315 added; worker muse-spark |
| 2026-10-05 | C-19 `CSL-0019` | Added *orc_simple_r245fa* (S. Quoilin, screening ORC with recuperator) — verified vs EES_ok/orc_r245fa.EES stored solution (W_net −0.10 %, η −0.27 %; residuals ≤ 2.1 % from R245fa EES vs CoolProp properties); curated `.initials`; CSX-031 imported, CSX-032/TM-0324 merged (air-source, no-recuperator variant), TM-0322 duplicate; worker muse-spark |
| 2026-10-05 | C-20 `CSL-0020` | Added *dry_air_screw_compressor_leakage* — verified vs the EES original TM-0039 stored values and the TM-0032 full solution (derived results ≤ 0.15 %); CSX-002/CSX-003 merged, TM-0039 added, TM-0032 merged (variant), TM-0023–27/33/38/40/41 duplicates; worker muse-spark |
| 2026-10-05 | C-21 `CSL-0021` | Added *piston_compressor_identification* — verified vs the EES original TM-0015 stored solution (predictions ≤ 0.27 %, identified parameters ≤ 1.0 %, EES ideal-gas vs CoolProp air); CSX-034 merged, TM-0015 added, TM-0003/04/07/08/09 duplicates; worker muse-spark |
| 2026-10-05 | C-11 `CSL-0012` | Added *thermal_comfort_pmv_ppd* (Fanger PMV/PPD, level 2) — native file **blocked** (CS-GAP-IF-DIRECTIVE, CS-GAP-LOOKUPROW, CS-BUG-LOOKUP-STRING) with string-keyed tables `activite` 7×2 and `veture` 6×2 recovered by hand (the extractor’s 74×2 is spurious, CS-BUG-EXTRACT-LOOKUP-STRING); runnable `_coolsolve` variant verified vs the EES stored solution (46/57 ≤ 1e-3, 51/57 ≤ 0.5 %; the stored panel mixes two runs); DG-0061 triaged (TM-0263 duplicate); CS-BUG-HINT-FAHRENHEIT also registered. Worker muse-spark, chosen over a space-bunny attempt after review |
| 2026-10-05 | C-22 `CSL-0022` | Added *refrigeration_compressor_identification* (R22, 4 parameters from 2 points) — verified vs the EES original TM-0016 (77/86 ≤ 0.1 %, predictions ≤ 0.08 %); CSX-041 merged — the CoolSolve example derives from the typo’d variant TM-0017 (`M_dot_1` in `V_dot_su_2`, fix suggested); TM-0005/06/10/11/14/17 duplicates; worker muse-spark |
| 2026-10-05 | C-24 `CSL-0024` | Added *single_cylinder_engine_weibe* (dynamic, crank-angle INTEGRAL, level 3) — status **runs**: no EES original exists; reproduces the CoolSolve example solution (75/75) and its regression value; CSX-014 imported; new register row CS-DOC-SQUARE-INTEGRAL (`-d` analysis reports INTEGRAL models as non-square); worker space-bunny |
| 2026-10-05 | C-23 `CSL-0023` | Added *centrifugal_turbocompressor_performance* — verified vs the EES original DG-0013 (TM-0056 imported, TM-0055 stored solution: derived results ≤ 0.02 %); curated `.initials`; CSX-044 merged, TM-0052/54/55 duplicates; worker muse-spark |
| 2026-10-05 | C-26 `CSL-0025` | Added *heat_pump_cycle_r22_30kw* (groundwater-source R22 heat pump) — verified vs EES_ok/refrigeration2.EES stored solution (≤ 0.27 %, COP 0.05 %); CSX-039 imported; worker muse-spark |
| 2026-10-05 | C-27 `CSL-0026` | Added *crossflow_hx_hot_gas_water* — verified vs EES_ok/exchangers2.EES stored solution (28/29 ≤ 1e-3, wall temperature 0.10 %); the original’s non-physical wall block kept faithfully and documented; curated `.initials`; CSX-017 merged; worker muse-spark |
| 2026-10-05 | C-14 review B-01 | Review of CSL-0002…0014: workflow/templates updated (blocked models and variants, evidence for gaps, decoded-table false positives, style, inventory rules); `test_models.py` tests variants as `CSL-x:variant` (30 targets OK); `backlog_stats.py` validates the inventories (9 malformed rows repaired); M1 taxonomy kept, splits recommended at M2 (P6.2); Phase 5 recommendations for CoolSolve (`$UnitSystem` line, table decoder); reviewer Claude Sonnet |
| 2026-10-05 | C-28 `CSL-0027` | Added *shell_and_tube_steam_condenser* (1-2 shell-and-tube, V. Lemort and S. Quoilin) — verified vs EES_ok/exchangers3.EES stored solution (energy results ≤ 0.1 %; sizing 0.76 % from EES vs CoolProp water conductivity); CSX-018 imported; worker muse-spark |
| 2026-10-05 | C-37 `CSL-0036` | Added *orc_extraction_r134a* (R134a ORC, two-stage expander and 13 % extraction, level 3) — verified vs EES_ok/orc_extraction.EES stored solution (derived results ≤ 0.2 %; h/u/s ≤ 0.09 % after removing the constant reference offset); CSX-030 imported; new tool bug CS-BUG-EXTRACT-NUL (trailing NUL byte in extracted RTF equations, confirmed); worker space-bunny |
| 2026-10-05 | C-29 `CSL-0028` | Added *air_handling_unit_moist_air* (V. Lemort, repetition 10) — native file **blocked** by new gap CS-GAP-PSYCHRO-SAT (`TEMPERATURE(AirH2O,P,w,R=1)`, used by the EES original); runnable `_coolsolve` variant (one-line `dewpoint` change, curated `.initials`) verified vs EES_ok/humidair2.EES (per-kg-dry-air ≤ 0.5 %, duties ≤ 1.2 %); CSX-022 imported; worker muse-spark |
| 2026-10-05 | C-30 `CSL-0029` | Added *rankine_cycle_regenerative_extraction* (25 bar extraction, η = 29.85 %) — verified vs EES_ok/rankine2.EES stored solution (44/44 ≤ 1e-3); CSX-037 imported (the example solves a 14-bar case under a 25-bar header, documented), DG-0107 duplicates; worker muse-spark |
| 2026-10-05 | C-25 review B-02 | Review of CSL-0015…0024: 0 equation errors, regression 34/34; fixed `coolsolve_version`, `related` links, authors, README claims (CSL-0024, CSL-0019); CSX-002/034/035/038/041/044 recorded `added` (C-01 pattern), TM-0082 `merged`; workflow/template refined and new build_index warnings (prose `related`, one-way links, `coolsolve_version` format); reviewer Claude Sonnet |
| 2026-10-05 | C-35 `CSL-0034` | Added *gas_engine_full_power_cpbar* — verified vs the EES original TM-0127 stored solution (69 common variables, 3 differ at rtol 1e-3: fuel cp 0.94 % EES ideal-gas CH4 vs CoolProp, entropy reference offset); `cpbar` copied from CSL-0005 and called with `CALL` (the original calls it in function position, see the CS-GAP-PROC-MULTIOUT suggestion); CSX-026 and TM-0127 imported, TM-0131 duplicate; worker space-bunny |
| 2026-10-05 | C-31 `CSL-0030` | Added *two_speed_cooling_tower* — verified vs the EES original TM-0094 stored solution (54/54 ≤ 1e-3, max 7.1e-4 EES vs CoolProp AirH2O); default run at the original’s set point (the example CSX-011 fixes it at 25 °C); TM-0094 added, TM-0088 duplicate; worker glm-5.3-flash |
| 2026-10-05 | C-32 `CSL-0031` | Added *refrigeration_evaporator_wet_coil* (S. Bertagnolio) — verified vs the EES original TM-0078 stored solution (22 common variables, only h_1/h_3 differ by the constant R134a reference offset); CSX-015 and TM-0078 imported; worker space-bunny |
| 2026-10-05 | C-33 `CSL-0032` | Added *wet_air_cooled_condenser* (spray evaporative cooling) — verified vs the EES original TM-0079 stored solution (15/15 ≤ 1e-3, max 7.4e-4); CSX-009 and TM-0079 imported (identical equations); worker glm-5.3-flash |
| 2026-10-05 | C-36 `CSL-0035` | Added *centrifugal_compressor_lookup_map* — native file **blocked** (CS-GAP-INTERP-EES); runnable `_coolsolve` variant verified vs the EES original TM-0061 (w_s 9.6e-4; map table recovered from the exercise statement, the `.lkt` being lost); new gap CS-GAP-INTERP-EXTRAP (EES extrapolates INTERPOLATE linearly, CoolSolve clamps silently); CSX-045 and TM-0061 imported; worker glm-5.3-flash |
| 2026-10-05 | C-34 `CSL-0033` | Added *heat_pump_r22_semihermetic_compressor* (S. Bertagnolio, repetition 10) — verified vs the EES original TM-0154 stored solution (55 common variables, max 6.6e-3 on T_ev from EES 7.458 vs CoolProp R22 and water cp); curated `.initials`; CSX-020 and TM-0154 imported; worker space-bunny |
| 2026-10-05 | C-39 `CSL-0037` | Added *scroll_expander_semi_empirical* (level 3) — first application of decision D10: the EES `MODULE expander` flattened into the main program; verified vs the EES solution report of EES_ok/expander_module (inputs exact, 4 outputs ≤ 1.9e-2, R123 EES vs CoolProp); curated `.initials` and solver settings; CSX-019 imported, TM-0272 merged, TM-0273 duplicate; new tool bug CS-BUG-EXTRACT-STALE (stored variable records can be stale); worker glm-5.3-flash |
| 2026-10-05 | C-40 `CSL-0038` | Added *orc_co2_polynomial_maps* (transcritical CO2 power cycle, level 3) — status **runs**: no EES original exists; curated from the CoolSolve example and checked against its stored solution (140/140 ≤ 1e-3); CSX-028 imported; worker space-bunny |
| 2026-10-05 | C-41 `CSL-0039` | Added *high_temp_heat_pump_pcm_storage* (Zorlu geothermal plant, heat pump with PCM storage, level 3) — status **runs**: no EES original exists; checked against the CoolSolve example stored solution (114/114, max 1.9e-10); CSX-047 imported; worker glm-5.3-flash |
| 2026-10-05 | C-42 `CSL-0040` | Added *orc_biomass_chp* (biomass-boiler ORC on R123 with 5 scroll expanders, level 4) — **blocked** (CS-GAP-IF-DIRECTIVE, CS-GAP-LKT, new CS-GAP-NAME-SYMBOL for names such as `C%`); MODULEs `expander`/`evaporator` and SUBPROGRAM `biomass_burner` flattened (D10); no runnable variant yet (recipe documented); CSX-029 imported; worker space-bunny |
| 2026-10-05 | C-43 `CSL-0041` | Added *ice_storage_tank_discharge_phase_change* (dynamic, level 2) — native file **blocked** (CS-GAP-IF5, CS-GAP-INTEGRAL-LIMITS, CS-BUG-INTEGRAL-TABLE-SEP, CS-BUG-INTEGRAL-MAXSTEPS and two new bugs: CS-BUG-WATER-NEAR-FREEZING, CS-BUG-INTEGRAL-TABLE-CASE); runnable `_coolsolve` variant verified vs the TM-0095 stored solution (18/19 ≤ 6.4e-8) and a closed-form check; TM-0104 and CSX-023 imported, TM-0092/95/123 duplicates; worker glm-5.3-flash |
| 2026-10-05 | C-45 `CSL-0043` | Added *libr_water_absorption_chiller* (LiBr-water chiller with solution heat exchanger, level 2) — **blocked** (CS-GAP-FLUIDS-ABS); no runnable variant (no LiBr property correlation available in CoolSolve); the TM-0167 stored solution (30/30) kept as re-check reference; CSX-046 and TM-0167 imported, 8 rows merged, TM-0170 duplicate; worker glm-5.3-flash |
| 2026-10-05 | C-44 `CSL-0042` | Added *building_rc_network_3r2c* (3R2C building thermal network with weather lookup, dynamic, level 2) — native file **blocked** (CS-GAP-INTEGRAL-LOOKUP); no EES original exists; runnable `_coolsolve` variant verified against an independent RK4 integration (max 0.008 K) and the weather table; CSX-006 imported; worker space-bunny |
| 2026-10-05 | C-47 `CSL-0044` | Added *rigid_tank_water_mixture* — hand-converted from kPa/kJ, verified vs the EES stored solution of TM-0378 (12/12 ≤ 1e-3) and the course’s CoolProp solution; DG-0088 triaged (TM-0383/0540 duplicates, TM-0506 merged); worker glm-5.3-flash |
| 2026-10-05 | C-48 `CSL-0045` | Added *steam_turbine_exergy_balance* — hand-converted, verified vs the EES stored solution of TM-0389 (20/20, max 4.1e-10); DG-0093 triaged; worker space-bunny |
| 2026-10-05 | C-38 review B-03 | Review of CSL-0025…0036: regression 47/47, 11 of 12 models faithful to the EES original; CSL-0036 rearranged on a wrong “over-determined” diagnosis (rework requested); CSL-0034 comments and tolerances corrected; register rows CS-GAP-PSYCHRO-SAT, CS-GAP-INTERP-EXTRAP, CS-BUG-EXTRACT-NUL confirmed and completed; CSX-017 added, TM-0090/91 back to todo, version strings and back-links fixed; workflow updated; reviewer Claude Sonnet |
| 2026-10-05 | Rework `CSL-0036` | Original equations of orc_extraction.EES restored (W_dot_exp = 5000, epsilon_s_pp = 0.5, three Q_dot_hex statements; the worker’s rearranged specification reverted after review C-38); verified vs the EES stored solution (132 variables; max 2.62e-3 after reference-state offsets and quality sentinels); `.initials` required; README and model.json rewritten; Claude Sonnet |
| 2026-10-05 | C-50 `CSL-0047` | Added *nonideal_gas_isothermal_work* (v(P+k/v²)=RT, molar units) — native file **blocked** (CS-GAP-INTEGRAL-LIMITS, CS-BUG-INTEGRAL-FACTOR); runnable `_coolsolve` variant verified vs the EES stored solution of TM-0399 (12/12, max 9.0e-8, EES trapezoidal rule vs RK4); TM-0405 duplicate; worker space-bunny |
| 2026-10-05 | C-51 `CSL-0048` | Added *two_tanks_connected_valve_r12* — hand-converted, verified vs the EES stored solution of TM-0382 (27 common variables, max 1.97e-2 on a quality difference from the R12 saturated vapour volume, CoolProp +1.06 % vs EES; with the EES volumes 2.1e-10); new gap CS-GAP-UNIT-SUBEXPR (unit annotation on a sub-expression, 35 collection files); DG-0091 triaged; worker space-bunny |
| 2026-10-05 | C-46 review B-04 (light) | Scripted checks by the orchestrator: build_index 47 models 0 errors, backlog_stats clean, regression 49/49 targets OK (CSL-0009:coolsolve skipped); Phase 3A: 43 of 47 CoolSolve examples triaged, the 4 left (CSX-025, CSX-033, CSX-040, CSX-043: distinct exercises, reasons in notes) go to B-06; deep review stopped by maintainer decision (Sonnet reviews only for obvious problems or worker comparisons) |
| 2026-10-05 | C-52 `CSL-0049` | Added *otto_cycle_air_standard* — hand-converted from kPa/K/kJ, verified vs an independent Python/CoolProp re-implementation (42 variables, max 2.1e-11) and the meaningful part of the EES stored solution (18 values ≤ 1.5e-5); DG-0102 triaged; worker space-bunny |
| 2026-10-05 | C-49 `CSL-0046` | Added *octane_combustion_400pct_air* — native file **blocked** by new gap CS-GAP-FLUIDS-C8H18 (octane and heavier ideal-gas substances missing); runnable `_coolsolve` variant verified vs the EES stored solution of TM-0393; DG-0095 triaged; worker glm-5.3-flash (interrupted 2 h by the z.ai quota) |
| 2026-10-05 | C-53 `CSL-0050` | Added *gas_turbine_two_shaft_intercooled_regenerative* (land-based two-shaft gas turbine) — hand-converted, verified vs the EES stored solution of TM-0441; new gap CS-GAP-UNIT-NAMEDARG (unit annotation on a named argument of a property call, 19 collection files); DG-0105 triaged; worker space-bunny |
| 2026-10-05 | C-54 `CSL-0051` | Added *turbojet_ideal_260ms* (ideal turbojet, repetition 6) — hand-converted, verified vs the EES stored solution of TM-0442; worker glm-5.3-flash |
| 2026-10-05 | C-56 `CSL-0053` | Added *steam_power_plant_elementary* (pump, boiler, turbine, condenser) — hand-converted, verified vs the EES stored solution of TM-0416 (74 variables, max 7.9e-6); DG-0084 triaged; worker glm-5.3-flash |
| 2026-10-05 | C-55 `CSL-0052` | Added *combined_gas_steam_cycle* (Brayton topping and Rankine bottoming cycle) — hand-converted from K/kPa/kJ, verified vs the EES stored solution of TM-0446 (27/36 ≤ 7.4e-6; the 9 others are air h/s reference offsets whose differences agree to 4.9e-6); worker space-bunny |
| 2026-10-05 | C-57 `CSL-0054` | Added *heat_pump_r410a_air_evaporator* — hand-converted, verified vs the EES stored solution of TM-0449 and the course’s CoolProp solution; new gap CS-GAP-QUALITY-DOME (EES QUALITY returns 100/−100 outside the dome, CoolSolve 0; confirms the C-19 suggestion); DG-0109 triaged; worker glm-5.3-flash |
| 2026-10-05 | C-58 `CSL-0055` | Added *moist_air_room_psychrometrics* — hand-converted, verified vs the EES stored solution of TM-0451 and the course’s Python solution; new tool bug CS-BUG-COMPARE-UNIT-CASE (compare_solution.py misses lower-case EES unit names); DG-0111 triaged; worker space-bunny |
| 2026-10-05 | C-59 review B-05 (light) | Scripted checks: build_index 55 models 0 errors, backlog_stats clean, regression 57/57 targets OK (CSL-0009:coolsolve skipped). B-05 (12 cards, glm-5.3-flash and space-bunny): 9 verified, 3 blocked with verified variants; new register rows CS-GAP-FLUIDS-C8H18, CS-GAP-UNIT-SUBEXPR, CS-GAP-UNIT-NAMEDARG, CS-GAP-QUALITY-DOME, CS-BUG-COMPARE-UNIT-CASE |
| 2026-10-05 | C-60 `CSL-0056` | Added *iron_block_quench_water_tank* — hand-converted, verified vs the EES stored solution of TM-0388; DG-0092 triaged; the compare_solution.py unit-case bug it found duplicated CS-BUG-COMPARE-UNIT-CASE (merged into that row); worker glm-5.3-flash |
| 2026-10-05 | C-61 `CSL-0057` | Added *two_tanks_max_work_air* (maximum work from two air tanks) — status **runs**: hand-converted from K/kJ (absolute temperatures kept in the logarithms), checked against the closed-form solution; DG-0094 triaged; worker space-bunny |
| 2026-10-05 | C-62 `CSL-0058` | Added *diesel_engine_excess_air_exhaust_analysis* — native file **blocked** by new gap CS-GAP-FLUIDS-ALIAS (EES real-fluid name `CarbonMonoxide` unknown to CoolSolve); runnable `_coolsolve` variant (ideal-gas `CO`, only enthalpy differences enter) verified vs the EES stored solution of TM-0395; TM-0394 merged; worker glm-5.3-flash (first version had substituted `CO` in the native file: corrected after orchestrator check) |
| 2026-10-05 | C-63 `CSL-0059` | Added *stirling_cycle_ideal_regenerator* — native file **blocked** by new gap CS-GAP-INTEGRAL-MULTIVAR (several INTEGRAL calls with different integration variables in one model); runnable `_coolsolve` variant verified vs the EES stored solution of TM-0431; DG-0103 triaged; worker space-bunny |
| 2026-10-05 | C-64 `CSL-0060` | Added *gas_turbine_reheat* — hand-converted, verified vs the EES stored solution of TM-0435; DG-0104 triaged (3 variants merged); worker glm-5.3-flash |
| 2026-10-05 | C-66 `CSL-0062` | Added *cooling_coil_condensate_ratio* (7 kW cooling coil, revision question) — hand-converted, verified vs the EES stored solution of TM-0396; worker glm-5.3-flash |
| 2026-10-05 | C-65 `CSL-0061` | Added *refrigerator_freezer_r134a* (domestic refrigerator-freezer) — native file **blocked** by new gap CS-GAP-PROP-TH (property calls with the (T, H) input pair); runnable `_coolsolve` variant verified vs the EES stored solution of TM-0450; DG-0110 triaged; worker space-bunny |
| 2026-10-05 | C-67 `CSL-0063` | Added *moist_air_adiabatic_mixing* (room and outdoor air, conditioning) — hand-converted, verified vs the EES stored solution of TM-0452; TM-0552 duplicate; worker glm-5.3-flash |
| 2026-10-05 | C-68 `CSL-0064` | Added *psychrometric_mixer_condensation* (mixing of room and outdoor air with condensation) — hand-converted, verified vs the EES stored solution of TM-0453; worker space-bunny |
| 2026-10-05 | C-69 `CSL-0065` | Added *cooling_tower_condenser_water* — hand-converted, verified vs the EES stored solution of TM-0454; TM-0536 merged; worker glm-5.3-flash |
| 2026-10-05 | C-70 `CSL-0066` | Added *adiabatic_saturation_wet_bulb* — hand-converted, verified vs the EES stored solution of TM-0455 (max 5.2e-3 on the humidity ratio, EES vs CoolProp humid air); worker space-bunny |
| 2026-10-05 | C-72 `CSL-0068` | Added *heat_pump_scroll_compressor_data_check* (R407C scroll compressor data consistency) — native file **blocked** (CS-GAP-PROP-TH); runnable `_coolsolve` variant verified vs the EES solution report of EES_ok; CSX-040 imported; worker space-bunny |
| 2026-10-05 | C-71 `CSL-0067` | Added *piston_compressor_suction_drop_leakage* — status **runs** (curated CoolSolve example CSX-025, checked against its stored solution); worker glm-5.3-flash |
| 2026-10-05 | C-73 `CSL-0069` | Added *centrifugal_compressor_design_similarity* (air design and methane similarity variant) — verified vs the EES stored solutions; CSX-043 imported (the example’s solve failure resolved); worker space-bunny |
| 2026-10-05 | C-74 review B-06 (light) | Scripted checks: build_index 69 models 0 errors, backlog_stats clean, regression 72/72 targets OK (CSL-0009:coolsolve skipped). B-06 (14 cards, glm-5.3-flash and space-bunny): 9 verified, 2 runs, 3 blocked with verified variants (new gaps CS-GAP-FLUIDS-ALIAS, CS-GAP-INTEGRAL-MULTIVAR, CS-GAP-PROP-TH); one worker substitution (CarbonMonoxide → CO in a native file) caught and corrected; the CoolSolve examples are now all triaged except CSX-033 (Phase 4C) |
| 2026-10-05 | C-75 `CSL-0070` | Added *adiabatic_humidifier_simplified* (model data bank) — verified vs the EES stored solution of TM-0475 (max 4.4e-3, humid-air properties); new tool bug CS-BUG-EXTRACT-FMT-BYTE (ees_extract.py drops EES 7.x variable records); worker glm-5.3-flash |
| 2026-10-05 | C-76 `CSL-0071` | Added *centrifugal_fan_reference_model* (model data bank RefSim) — verified vs the EES stored solution of TM-0251 (max 1.2e-2 on the moist-air cp); worker space-bunny |
| 2026-10-05 | C-88 `CSL-0061`, `CSL-0068` | Decision D11 applied: the (T, H) property calls rewritten with (P, H) in the main files (CSL-0061: saturation pressure of state 4; CSL-0068: auxiliary pressure unknown, the R407C glide forbids the saturation pressure), `_coolsolve` variants deleted; both **verified** (max 7.5e-4 and 3.6e-3); worker space-bunny |
| 2026-10-05 | C-78 `CSL-0073` | Added *cooling_coil_with_control_simplified* (model data bank) — native file **blocked** (CS-GAP-IF5); runnable `_coolsolve` variant (5-argument IF → 3-argument) verified vs the EES stored solution of TM-0472 (max 2.7e-2 on the latent duty, a small difference of two large terms); worker space-bunny |
| 2026-10-05 | C-77 `CSL-0072` | Added *centrifugal_brine_pump_refsim* (model data bank) — native file **blocked** by its copy of the ULiège `Brineprop.lib` (new gaps CS-GAP-ELSEIF-CHAIN, CS-GAP-UPPERCASE, CS-GAP-CALL-EXPR-OUT, CS-GAP-STRING-ARRAY, CS-GAP-LOOKUP-PROC); runnable `_coolsolve` variant verified vs the EES stored solution of TM-0487; worker glm-5.3-flash |
| 2026-10-05 | C-79 `CSL-0074` | Added *cooling_coil_refsim* (model data bank cooling-coil reference model, dry and wet regimes) — native file **blocked** (new gaps CS-GAP-NAME-PIPE for names such as `K|star`, CS-GAP-IFSTR for the string conditional `IF$`); runnable `_coolsolve` variant verified vs the EES stored solution of TM-0471; worker space-bunny |
| 2026-10-05 | C-81 `CSL-0076` | Added *cooling_tower_direct_contact_refsim* (model data bank) — verified vs the EES stored solution of TM-0489 (max 4.5e-3, humid-air properties); new bug CS-BUG-MULTILINE-COMMENT-START (a comment opened by a `"` at the end of a line); worker space-bunny |
| 2026-10-05 | C-80 `CSL-0075` | Added *iso5167_orifice_plate_flow_rate* (model data bank) — native file **blocked** (new rows CS-GAP-ISIDEALGAS, CS-BUG-HUMIDAIR-PROPS — humid-air density silently 1E4 kg/m³ —, CS-BUG-STRING-CASE); runnable `_coolsolve` variant verified vs the EES stored solution of TM-0255; worker glm-5.3-flash |
| 2026-10-05 | C-82 `CSL-0077` | Added *aircooled_chiller_refsim* (model data bank air-cooled water chiller) — verified vs the EES printed solution of TM-0488 (max 6.2e-3); worker space-bunny |
| 2026-10-05 | C-84 `CSL-0079` | Added *brineprop_secondary_refrigerants* (BrineProp secondary-refrigerant property functions) — native file blocked, verified `_coolsolve` variant (max 4.8e-10); back-links to the refsim pump and cooling coil; worker space-bunny |
| 2026-10-05 | C-95 `sources/ht/` | Triage of `ht` 1.2.0 @ 85e0ee6 (MIT): 272 public functions → 222 to translate in 24 families HT-001…HT-024 (cards C-96…C-119, CSL-0087…0110); pipe/two-phase dP is in `fluids`, not `ht`; C-92 (THC-004) folded into C-107; worker space-bunny (7 min) |
| 2026-10-05 | C-83 `CSL-0078` | Added *brine_to_water_heat_pump_refsim* (model data bank) — native file blocked (ELSEIF chain, BrineProp gaps), verified `_coolsolve` variant vs the EES stored solution (derived results 0.4–3.3 %: R407C property differences, h/s reference offsets); new gap CS-GAP-PROP-SV (property calls with (s,v)); GLM-flash attempt lost at the z.ai weekly limit; worker space-bunny (28 min) |
| 2026-10-06 | C-86 `CSL-0081` | Added *vertical_ghes_refsim* (borefield, dynamic L3, model data bank) — blocked, no runnable variant (dynamic); new gaps CS-GAP-INTEGRALVALUE and CS-GAP-GOTO (GOTO + numeric labels in procedures); worker space-bunny (18 min) |
| 2026-10-06 | C-121 `sources/thermo_models/` | Triage of the 50 new files TM-0553…TM-0602 (2026-10-06 upload; sweep.py made ID-stable): 22 todo, 18 duplicate, 8 discarded, 1 merged, 1 parked (SETP.LIB, textbook code: licence question); 14 import cards C-122…C-135 (CSL-0111…0124); worker space-bunny (18 min) |
| 2026-10-06 | C-89 `CSL-0082` | Added *parabolic_trough_receiver_forristal* (ThermoCycle THC-001, Forristall NREL/TP-550-34169) — native file runs, verified vs an independent NumPy re-implementation (2.4e-9) and vs NREL/TP-550-45633 measured heat loss (40 vs 43 W/m), energy-balance closure −0.68 % (source area mismatch, documented); new bug CS-BUG-TINY-VALUE (values below ~1e-16 stored as 0); worker space-bunny (24 min) |
| 2026-10-06 | C-131 `CSL-0120` | Added *ball_valve_authority* (TM-0588, equivalent opening diameter of a ball valve, L1) — native file runs; d_eq matches the EES stored solution (other stored values are procedure locals of another call; mm→m), checked by the orchestrator; probation card of worker nemotron-3.5-lightning (40 min, 1 retry) |
| 2026-10-06 | C-85 `CSL-0080` | Added *condensing_boiler_refsim* (model data bank, L3) — native file blocked by CS-BUG-COMMON-PROC ($COMMON variables of a procedure read as 0) and C8H18; verified `_coolsolve` variant vs the EES stored solution; two invalid gap rows (REDUNDANT-EQ, IMPLICIT-CALL) rejected by the orchestrator and removed; nemotron-3-ultra attempt aborted; worker space-bunny (rework, 1 h 46) |
| 2026-10-06 | C-96 `CSL-0087` | Added *internal_turbulent_nusselt* (ht HT-001: 23 FUNCTIONs, turbulent and entry-region internal Nu) — verified vs the ht 1.2.0 doctests and Python (52 outputs, max 3.2e-13); dual citation (original paper + ht module/version) in each function; pattern for the B-09 cards; worker space-bunny (10 min) |
| 2026-10-06 | C-91 `CSL-0084` | Added *orc_expander_pump_empirical_maps* (ThermoCycle THC-003: 11 isentropic-efficiency / filling-factor polynomials of hermetic and open-drive scroll expanders and pumps) — verified vs an independent Python re-evaluation from the .mo sources + CoolProp (62/62, max 9.7e-11); first real card of worker mimo-v2.6-flash (22 min) |
| 2026-10-06 | C-97 `CSL-0088` | Added *nucleate_boiling_and_chf* (ht HT-002: 12 pool nucleate boiling and critical-heat-flux correlations) — verified vs ht 1.2.0 (32 outputs, 0 differ); worker space-bunny (14 min) |
| 2026-10-06 | C-93 `CSL-0086` | Added *in_cylinder_htc_correlations* (ThermoCycle THC-005: 7 in-cylinder heat-transfer correlations — Annand, Woschni, Adair, Destoop, Irimescu, Kornhauser…) — verified vs an independent Python re-implementation from the .mo files (66/66, max 7.1e-12); worker mimo-v2.6-flash (19 min) |
| 2026-10-06 | C-98 `CSL-0089` | Added *condensation_film* (ht HT-003: 6 film-condensation FUNCTIONs — Nusselt, Boyko-Kruzhilin, Akers-Deans-Crosser, Cavallini-Smith-Zecchin, Shah…) — verified vs ht 1.2.0 (max 2.0e-12); new bug CS-BUG-PI-FUNCTION (pi evaluates to 1 inside a FUNCTION/PROCEDURE body; reproduced by the orchestrator; library scan: only CSL-0081, already blocked, uses pi in a body); worker space-bunny (12 min) |
| 2026-10-06 | C-99 `CSL-0090` | Added *hx_effectiveness_ntu* (ht HT-004: 17 FUNCTIONs — effectiveness-NTU and inverse relations for counterflow, parallel, crossflow, boiler/condenser) — verified vs ht 1.2.0 (50 outputs, 0 differ); worker space-bunny (19 min) |
| 2026-10-06 | C-101 `CSL-0092` | Added *free_conv_cylinders* (ht HT-006: 13 free-convection correlations, vertical and horizontal cylinders) — verified vs ht 1.2.0 (42 values, max 2.8e-13); worker space-bunny (10 min) |
| 2026-10-06 | C-102 `CSL-0093` | Added *free_conv_plates_and_sphere* (ht HT-007: 5 free-convection correlations, plates and sphere) — verified vs ht 1.2.0 (26 values, max 3.4e-13); worker space-bunny (11 min) |
| 2026-10-06 | C-103 `CSL-0094` | Added *external_crossflow_cylinder* (ht HT-008: 8 single-cylinder crossflow Nusselt correlations) — verified vs ht 1.2.0 (max 1.9e-13); worker space-bunny (12 min) |
| 2026-10-06 | C-104 `CSL-0095` | Added *tube_bank_nusselt* (ht HT-009: 6 of 7 tube-bank Nu correlations and row/angle corrections) — verified vs ht 1.2.0 (20 values, max 2.8e-12); Nu_Grimison_tube_bank not translated (ht uses a spline fit of digitised tables; table lookups inside a FUNCTION: CS-GAP-LOOKUP-PROC), documented; worker space-bunny (11 min) |
| 2026-10-06 | C-105 `CSL-0096` | Added *plate_hx_heat_transfer* (ht HT-010: plate-HX single-phase Nu and plate two-phase boiling correlations) — verified vs ht 1.2.0 (24/24, max 3.6e-12); worker space-bunny (21 min) |
| 2026-10-06 | C-106 `CSL-0097` | Added *two_phase_nonboiling_in_tube* (ht HT-011: in-tube two-phase non-boiling HTC correlations) — verified vs ht 1.2.0 (37 values, max 4.0e-12); worker space-bunny (12 min) |
| 2026-10-06 | C-107 `CSL-0098` | Added *flow_boiling_in_tubes* (ht HT-012 flow and film boiling in tubes + THC-004 correlations missing from ht; THC-004 merged, so C-92 is closed) — verified vs ht 1.2.0 (37 values, max 4.2e-12); worker space-bunny (29 min) |
| 2026-10-06 | C-108 `CSL-0099` | Added *air_cooler_air_side* (ht HT-013: 8 finned-bundle air-side HTC / pressure-drop / noise correlations + 3 helpers) — verified vs ht 1.2.0 doctests and Python; worker space-bunny (22 min) |
| 2026-10-06 | C-109 `CSL-0100` | Added *free_conv_enclosed_and_jackets* (ht HT-014: enclosed plates, critical Ra, tank coils, vessel jackets) — verified vs ht 1.2.0 (33 values, max 8.8e-13); worker space-bunny (22 min) |
| 2026-10-06 | C-110 `CSL-0101` | Added *external_forced_conv_plates* (ht HT-015: 4 flat-plate forced-convection correlations) — verified vs ht 1.2.0 (13/13, max 2.5e-13); worker space-bunny (6 min) |
| 2026-10-06 | C-111 `CSL-0102` | Added *hx_temperature_effectiveness_pntu* (ht HT-016: 15 P-NTU / TEMA temperature-effectiveness functions and inverse NTU(P)) — verified vs ht 1.2.0 (81/81); three unverified CoolSolve suggestions in the README (ELSEIF silently wrong, recursive FUNCTION crash, function unreliable with variable arguments); worker space-bunny (31 min) |
| 2026-10-06 | C-112 `CSL-0103` | Added *tube_bank_dp_bell_delaware* (ht HT-017: shell-side ΔP Kern, Zukauskas + Bell-Delaware Jc/Jl/Jb/Js/Jr; one ht B-spline reproduced exactly, Jl/Jb in the HEDH closed forms, bivariate digitised splines documented as not translated) — verified vs ht 1.2.0 (23/23); worker space-bunny (15 min) |
| 2026-10-06 | C-113 `CSL-0104` | Added *supercritical_internal_nu* (ht HT-018: 18 near-supercritical internal-convection correlations) — verified vs ht 1.2.0 (71/71); worker space-bunny (15 min) |
| 2026-10-06 | C-90 `CSL-0083` | Added *parabolic_trough_loss_correlations* (ThermoCycle THC-002: Schott PTR70, Sopogy, Soltigua receiver/collector loss fits) — verified vs an independent Python re-evaluation from the .mo sources (34/34) and the published values; worker longcat-2.5-preview (stopped by the free-usage limit before its final report; result checked and merged by the orchestrator) |
| 2026-10-06 | C-87 review B-07 | Light scripted review (orchestrator): build_index 103 models / 245 functions / 0 errors; test_models 105 targets (81 main files + 24 variants), 0 failure (CSL-0009:coolsolve excluded); inventories cross-checked against the library (every model has its added row, after repairing the ht/thermocycle rows reset by workers); invalid gap rows of C-85 rejected; B-07 closed |
| 2026-10-06 | C-94 review B-08 | Light scripted review (orchestrator): same checks as C-87; B-08 closed (C-89…C-91, C-93 added; C-92 folded into C-107); every translation verified against an independent Python re-implementation of the Modelica sources |
| 2026-10-06 | handover | Work interrupted by the maintainer (all usable free opencode quotas exhausted; GLM weekly limit until 2026-10-07). Free-model benchmark (C-10 re-run): mimo-v2.6-flash, longcat-2.5-preview, ling-3.1-flash qualified; nemotron-3-ultra, nemotron-3.5-lightning rejected; fledge-alpha, ling-3.0-flash-fin unavailable. Repairs: `sweep.py` made ID-stable (+50 rows TM-0553…0602); `ht`/ThermoCycle inventory decisions reset by workers restored (22 rows) and `csl.py merge` now merges inventories row by row; thermo_models inventory restored after a worker rewrote it (C-131). CoolSolve pending suggestions moved to §8 of the register. 103 models, 245 functions, regression 105/105 |
| 2026-10-07 | C-130 `CSL-0119` | Added *solar_geometry_sun_path* (TM-0589, solar angles, L1) — native file blocked by CS-GAP-NDAY (new: EES date function nDay_, evidence: stored n = 338) and CS-GAP-IF-DIRECTIVE; verified `_coolsolve` variant (22/22 vs the EES stored solution, orchestrator src_check: 18/18 source equations); worker muse-spark (9 min) |
| 2026-10-07 | C-124 `CSL-0113` | Added *condenser_3_zones_plate_correlations* (TM-0563, three-zone plate condenser, Thonon/Kuo, R123 + glycol) — native file runs; vs the EES stored solution 17 common variables, 5 outputs within 5.6 % (R123 superheated-region properties of EES 8 vs CoolProp, CoolProp checked against published tables); orchestrator src_check: 163/164 source equations (+ D5 unit tag, + logged state arrays); worker glm-5.3-flash (11 min) |
| 2026-10-07 | C-114 `CSL-0105` | Added *lmtd_and_f_correction* (ht HT-019: LMTD, Fakheri F correction, air-cooler Ft) — verified vs ht 1.2.0 (16/16, max 5.4e-14); worker muse-spark (8 min) |
| 2026-10-07 | C-123 `CSL-0112` | Added *three_zone_hx_procedures* (TM-0564/0569/0579/0566/0571: hx_cd, hx_ev, lmtd, single_phase_HX, EV, CD, evaporator2) — runs; vs the stored solutions max 8.4e-2, explained in the README (status runs); new bug CS-BUG-LOOKUP-WRITE (writing a lookup cell counted as an equation in the main program, silently dropped in a procedure; evidence: EES X9.249 source); worker space-bunny (23 min) |
| 2026-10-07 | C-116 `CSL-0107` | Added *radiation_heat_flux* (ht HT-021: blackbody spectral radiance, radiant heat flux, grey transmittance) — verified vs ht 1.2.0 (8/8, max 7.1e-14); worker muse-spark (5 min) |
| 2026-10-07 | C-100 `CSL-0091` | Added *internal_laminar_and_curved_nu* (ht HT-005: laminar, thermal entry region, rectangular duct, spiral/helical curved ducts) — verified vs ht 1.2.0 (max 3.2e-13); worker longcat-2.5-preview (28 min) |
| 2026-10-07 | C-127 `CSL-0116` | Added *heat_pump_vitocal_300g* (TM-0596, Viessmann Vitocal 300-G brine/water heat pump: Copeland scroll compressor + two plate HXs, L3) — blocked: missing catalogue table and 9 gap IDs, 3 new and evidenced (CS-GAP-INCOMPRESSIBLE: EES glycol/brine libraries with concentration; CS-GAP-GE-ARROW: `=>`; CS-GAP-REPEAT-UNTIL-BARE); no variant yet (revisit after C-134, Copeland catalogue); worker glm-5.3-flash (24 min) |
| 2026-10-07 | C-128 `CSL-0117` | Added *double_stage_scroll_expander* (TM-0565, two-stage hermetic scroll expander, Lemort/Quoilin/Pire, L3) — MODULE flattened per D10 (`_mod` suffix); vs the EES stored solution 46/51 variables matched after the renaming, max 3.1e-2 on derivative diagnostics (explained), the 2 unmatched swept volumes are unsolved EES guesses (= 1); orchestrator check; worker glm-5.3-flash (21 min) |
| 2026-10-07 | C-117 `CSL-0108` | Added *packed_bed_nusselt* (ht HT-022: Gnielinski, Wakao-Kagei, Achenbach, KTA packed-bed correlations) — verified vs ht 1.2.0 (10 values, max 1.4e-12); worker muse-spark (stopped by the opencode free limit before its final report; checked and merged by the orchestrator) |
| 2026-10-07 | C-129 `CSL-0118` | Added *air_nozzle_ejector* (TM-0593, air ejector with choked primary nozzle, L3) — native file blocked (CS-GAP-CALL-WARNING, new CS-GAP-AIR-ENTHALPY-REF: EES references ideal-gas Air enthalpy to 0 at 0 K, ratios of absolute enthalpies are reference-dependent); verified `_coolsolve` variant (offset-corrected ratio equations; remaining differences = reference offsets and stale stored cells, provenance audited on orchestrator request: stored run at FF = 0.1); 59/59 source equations; an earlier nemotron-lightning attempt was rejected; worker glm-5.3-flash (29 min) |
| 2026-10-07 | C-126 `CSL-0115` | Added *hx_fem_evaporator_discretised* (TM-0575, discretised hx-fem evaporator, smoothed revision of TM-0275 → duplicate) — native file blocked (writes a profile to a lookup table inside a PROCEDURE: CS-BUG-LOOKUP-WRITE; the worker's duplicate row CS-GAP-LOOKUP-WRITE folded into it by the orchestrator); verified `_coolsolve` variant (max 2.2e-3 vs the EES stored solution); worker glm-5.3-flash (20 min) |
| 2026-10-07 | C-135 `CSL-0124` | Added *plate_hx_pressure_drop_identification* (TM-0554, optim/, Thonon/Kuo/Hsieh pressure-drop identification) — native file blocked by the new CS-GAP-REFPROP (CALL EES_REFPROP with the R245fa + R134a mixture); `_coolsolve` variant faithful at the stored run (mixture fraction 1 = pure R245fa, the original's commented pure-fluid calls): 29/34 variables agree, 3 q-dependent stored cells shown stale; worker glm-5.3-flash (29 min) |
| 2026-10-07 | C-134 `CSL-0123` | Added *copeland_catalogue_correlation* (TM-0560, ARI/Copeland 3rd-order polynomial ZH38K4E-TFD, tables recovered from the EES binary) — native file blocked by the new CS-BUG-LOOKUP-COL-ARG (lookup with a column name inside a FUNCTION silently returns column 1); verified `_coolsolve` variant; new CS-BUG-CONVERT-UNIT (convert('lbm/hr','kg/s') = 1, silent; reproduced by the orchestrator); CSL-0116 re-checked: stays blocked (catalogue vintage differs from TM-0596's, no faithful variant); worker glm-5.3-flash (45 min) |
| 2026-10-07 | C-125 `CSL-0114` | Added *evaporator_3_zones_plate_correlations* (TM-0570, three-zone plate evaporator, Thonon/Hsieh; TM-0582 autosize as `_autosize` variant) — runs; native file = 164/164 source equations (+ logged state points), variant = 154/154 of TM-0582 (orchestrator src_check; a first review compared the wrong file — src_check fixed); 4 of 19 stored values differ, explained in the README; worker glm-5.3-flash (21 min) |
| 2026-10-07 | C-122 `CSL-0111` | Added *plate_hx_correlations* (TM-0585 + TM-0496: 10 plate-HX procedures — Bogaerts, Han, Hsieh, Kumar, Kuo, Martin, Muley, Thonon, Wanniarachchi, Yan) — verified vs the EES stored solutions and ht; new bug CS-BUG-HASH-IDENT (identifier with # silently dropped inside a procedure body; evidence TM-0585/TM-0496, EES X9.721); worker glm-5.3-flash (23 min) |
| 2026-10-07 | C-132 `CSL-0121` | Added *heat_transfer_fluid_properties* (TM-0574, prop_htf: MEG, Therminol VP-1/66, oil; companion of CSL-0079) — verified vs the EES stored solution (6/6, max 1.9e-10); the HEDH data-sheet cross-check is pending (host unreachable); worker glm-5.3-flash (11 min) |
| 2026-10-07 | C-133 `CSL-0122` | Added *nozzle_discharge_coefficients* (TM-0558/0559/0587/0581: ASHRAE 41.2 / ISO R859 nozzles, ISO 5167 long-radius nozzle, admission, range checker) — verified; new gap CS-GAP-SUM-INDEXED (indexed SUM(x[i], i=1, N); ees_vs_coolsolve.csv lists SUM as supported, only the variadic form is); worker glm-5.3-flash (68 min) |
| 2026-10-07 | C-136 review B-10 | Light scripted review (orchestrator): build_index 120 models / 317 functions / 0 errors; test_models 122 targets (92 main files + 30 variants), 0 failure (CSL-0009:coolsolve excluded); inventories cross-checked (HT-022 row of CSL-0108 set, worker stopped by the quota); every import of the batch checked with src_check (equation overlap with the EES source); B-10 closed: 14 cards, 9 new CoolSolve bugs/gaps registered with evidence, 2 worker claims corrected (C-125 review error on my side, C-126 duplicate gap folded) |
| 2026-10-08 | C-115 `CSL-0106` | Added *conduction_resistances_and_shapes* (ht HT-020: cylindrical and plane-wall resistance, 6 shape factors, R-value conversions) — verified vs ht 1.2.0 (50/50, max 8.0e-11); worker glm-5.3-flash (24 min) |
| 2026-10-08 | C-118 `CSL-0109` | Added *fin_efficiency_and_wall_factors* (ht HT-023: circular-fin efficiency, wall correction factors for Nu and frictional dP) — verified vs ht 1.2.0 (26 values, max 4.0e-12); worker glm-5.3-flash (18 min) |
| 2026-10-08 | C-119 `CSL-0110` | Added *shell_and_tube_sizing* (ht HT-024: 13 tube-count, bundle-diameter, TEMA clearance, baffle and unsupported-length functions) — verified vs ht 1.2.0 (43 values, max 2.4e-13); worker glm-5.3-flash (24 min) |
| 2026-10-08 | C-120 review B-09 | Light scripted review (orchestrator): all 24 ht families translated (CSL-0087…0110, 347 functions in the library); each file cites ht 1.2.0 and the original references and has a verification table vs ht; build_index 123 models / 347 functions / 0 errors; test_models 125 targets (95 main files + 30 variants), 0 failure; inventories consistent; B-09 closed |
| 2026-10-08 | C-138 plan B-12 | Planning of B-12 (LaboThapPy + TESPy wave1/high, 31 rows): 7 merged into existing models (ht, ThermoCycle, CSL-0007, scroll expanders), 24 to translate in 23 cards C-170…C-192 (CSL-0125…0147, 3 [hard]); worker space-bunny (12 min) |
| 2026-10-08 | C-137 plan B-11 | Planning of B-11 (thermo_models wave1/high, 22 rows): 2 merged, 20 import cards C-140…C-159 (CSL-0148…0167, 15 [hard]: engines, REFPROP ORC, MODULE/SUBPROGRAM flattening, catalogue maps, PV tables, parameter identification); worker glm-5.3-flash (15 min) |
| 2026-10-08 | C-170 `CSL-0125` | Added *pump_curve_similarity* (LaboThapPy LTP-009: pump from manufacturer curves + affinity laws, NPSH, 3 modes as main file + 2 variants) — verified vs the LaboThapPy re-run (max 1.1e-9); headers 17–21 lines; worker space-bunny (14 min) |
| 2026-10-08 | C-171 `CSL-0126` | Added *hx_constant_effectiveness* (LaboThapPy LTP-011: enthalpy-based constant-effectiveness HX — recuperator, IHX, gas cooler) — verified vs the LaboThapPy example (max 2.3e-7); worker space-bunny (10 min) |
| 2026-10-08 | C-141 `CSL-0149` | Added *gas_engine_complete_model* (TM-0136, complete gas engine: throttle, carburettor, pressure drop, combustion, recuperator) — native file blocked (CS-GAP-INTERP-EES; cpbar kept in the source function form, see register §8 CS-GAP-PROC-MULTIOUT); verified `_coolsolve` variant (97 variables vs EES, 6 explained, max 9.4e-3); lookup table recovered from TM-0137; headers shortened to 20 lines on review; worker glm-5.3-flash (26 min) |
| 2026-10-08 | C-173 `CSL-0128` | Added *hx_eps_ntu_plate_pipe* (LaboThapPy LTP-014 HexeNTU: eps-NTU with UA from plate/pipe geometry, wall + fouling, Gnielinski) — verified vs the LaboThapPy component (max 1.8e-6) and within the TESPy test tolerances; worker space-bunny (15 min) |
| 2026-10-08 | C-174 `CSL-0129` | Added *parabolic_trough_collector_discretised* (LaboThapPy LTP-020: absorber enthalpy march over discretised cells with the Soponova map) — verified vs the LaboThapPy example; loop unrolled because of CS-BUG-DUPLICATE-INDEX-EXPR (new, P1: index arithmetic T[i+1] in DUPLICATE not evaluated; reproduced and registered by the orchestrator); header trimmed to 20 lines on review; worker space-bunny (23 min) |
| 2026-10-08 | C-142 `CSL-0150` | Added *adiabatic_flame_dissociation* (TM-0231, MCI TP: CH4 / fuel-oil adiabatic flame temperature with and without dissociation) — blocked, no runnable variant (14-species Gibbs equilibrium); new gaps CS-GAP-CHEM-EQUIL (EES built-in chemical-equilibrium procedure) and CS-GAP-NASA (EES NASA species procedure), evidence: the EES 10.589 source; worker glm-5.3-flash (≈ 25 min active, z.ai 5-hour window in between) |
| 2026-10-08 | C-143 `CSL-0151` | Added *engine_derating_iso3046* (TM-0235, MCI TP: engine derating per ISO 3046/1) — native file blocked (CS-GAP-IF-DIRECTIVE, new CS-GAP-ACCENTED-IDENT: accented letters in variable names, frequent in the French ULiège files); verified `_coolsolve` variant (14/14, max 3.9e-6); header trimmed on review; worker glm-5.3-flash (20 min) |
| 2026-10-08 | C-144 `CSL-0152` | Added *turbocharger_combustion_products* (TM-0240, MCI TP4: turbocharger matching with combustion products, SUBPROGRAM flattened per D10, cpbar → CSL-0005) — native file blocked; verified `_coolsolve` variant; new CS-GAP-MOLARMASS-ELEMENT (molarmass of element symbols C, H) and CS-BUG-EXTRACT-DECIMAL-RANGE (ees_extract.py rewrites the range comma of SUM/DUPLICATE as a decimal point); worker glm-5.3-flash (39 min) |
| 2026-10-08 | C-145 `CSL-0153` | Added *orc_whr_refprop_cost* (TM-0268, waste-heat-recovery ORC with scroll expander, REFPROP mixture + cost model) — native file blocked (CS-GAP-REFPROP, CS-GAP-IF5, new CS-GAP-END-PROCEDURE); runnable `_coolsolve` variant built on review (29 EES_REFPROP blocks → CoolProp R245fa, faithful at the stored run MM_fraction = 1), verified vs the EES stored solution (eta_cycle 7.1e-4; max 0.25 explained); worker glm-5.3-flash (44 min) |
| 2026-10-08 | C-147 `CSL-0155` | Added *inverter_air_water_heat_pump* (TM-0274, reversible inverter air-to-water heat pump, L4, ≈ 490 variables; heating branch flattened per D10) — native file blocked (CS-GAP-IF5, new CS-GAP-ENTHALPY-FUSION); `_coolsolve` variant solves 180/181 blocks, the coupled wet/dry block fails (Unknown fluid '' — register §8), no .sol; the EES stored solution is partly self-inconsistent (documented); worker glm-5.3-flash |
| 2026-10-08 | C-148 `CSL-0156` | Added *refrigeration_screw_compressor_r22* (TM-0277, screw compressor reference model in an R22 cycle, full/part load; TM-0276 merged) — native file runs (kPa/kJ → SI by hand, D5; +273 → +273.15 logged); verified vs the EES 6.395 stored solution: Δh agree within 0.24 %, other variables max 1.3e-2 (R22 property backend), absolute h/s carry the reference offset; worker glm-5.3-flash (27 min) |
| 2026-10-08 | C-149 `CSL-0157` | Added *reciprocating_catalogue_r717* (TM-0282, LABORELEC 2002: reciprocating ammonia compressor from catalogue data, RPM and part-load maps) — native file blocked (new CS-GAP-LOOKUP-NONAME: nameless LOOKUP(row, col) on the default table; new CS-BUG-DUPLICATE-VAR-BOUND: DUPLICATE with a variable bound is dropped — reproduced by the orchestrator); verified `_coolsolve` variant; worker glm-5.3-flash (36 min) |
| 2026-10-08 | C-150 `CSL-0158` | Added *gas_pipe_insulated_pressure_drop* (TM-0312: gas pipe pressure drop and heat gain — Colebrook, insulation) — native file blocked; verified `_coolsolve` variant; 5 new register rows with valid-EES evidence (CS-GAP-COLEBROOK, CS-GAP-STRINGPOS, CS-GAP-ARRAY-ARG, CS-BUG-IMPLICIT-PROC, CS-BUG-LOOKUP-COLNAME); a duplicate pi row folded into CS-BUG-PI-FUNCTION by the orchestrator; worker glm-5.3-flash (71 min) |
| 2026-10-08 | C-151 `CSL-0159` | Added *orc_void_fraction_charge* (TM-0314, low-temperature R134a ORC with the void-fraction refrigerant charge of the heat exchangers, L4) — native file blocked (existing CS-BUG-HUMIDAIR-PROPS); verified `_coolsolve` variant (charge M_charge 8.6e-5 vs EES); worker glm-5.3-flash (22 min) |
| 2026-10-08 | C-152 `CSL-0160` | Added *pv_module_single_diode* (TM-0316, PV module single-diode I-V curve, embedded PVModules table hand-decoded from the EES binary; UW F-Chart properties) — native file blocked (existing gaps, evidence added to CS-GAP-END-PROCEDURE); verified `_coolsolve` variant; worker glm-5.3-flash (24 min) |
| 2026-10-08 | C-153 `CSL-0161` | Added *plate_hx_thermal_resistances* (TM-0319, single-phase plate HX resistance model, Martin; brine side through BrineProp) — native file blocked (CS-GAP-IF-DIRECTIVE, CS-BUG-HASH-IDENT, CS-GAP-CALL-EXPR-OUT, CS-GAP-INCLUDE: existing IDs); `_coolsolve` variant for the stored run (fluid$ = 'Water') verified vs the EES stored solution; worker glm-5.3-flash (13 min) |
| 2026-10-08 | C-154 `CSL-0162` | Added *glycol_runaround_recovery_loop* (TM-0321, air-to-air glycol run-around heat-recovery loop, epsilon-NTU coils) — native file blocked (4 existing gap IDs); the variant does not converge: new CS-BUG-NEWTON-CYCLE (long equation cycle with solution values over many orders of magnitude stalls with every solver strategy, 30-link reproducer); verified pointwise (the EES stored point satisfies all 65 block equations), no .sol; worker glm-5.3-flash |
| 2026-10-09 | C-155 `CSL-0163` | Added *cooling_coil_paramid* (TM-0470, cooling-coil parameter identification, model data bank ParamID with a 3335×2 measured-data table; → CSL-0016/CSL-0074 family) — native file blocked (3 existing gaps; evidence added to CS-BUG-EXTRACT-FMT-BYTE); verified `_coolsolve` variant (max 1.05e-2 vs EES); worker glm-5.3-flash (31 min) |
| 2026-10-09 | C-158 `CSL-0166` | Added *boiler_modulating_burner_refsim* (TM-0491, model data bank: boiler with modulating burner, MODULE flattened per D10, cpbar → CSL-0005) — native file blocked; verified `_coolsolve` variant; new CS-BUG-STRING-CALL-OUT (string set only as a CALL output cannot be passed on) and CS-BUG-EXTRACT-TABLE-FP (ees_extract.py decodes a phantom parametric table); evidence appended to 4 rows; variant header trimmed on review; worker glm-5.3-flash (35 min) |
| 2026-10-09 | C-159 `CSL-0167` | Added *reciprocating_polynomial_r22* (TM-0499, model data bank: reciprocating compressor reference in an R22 cycle, polynomial modelling) — native file runs, verified vs the EES stored solution (max 1.8 %, explained); worker glm-5.3-flash (18 min) |
| 2026-10-09 | C-172 `CSL-0127` | Added *hx_constant_effectiveness_discretised* (LaboThapPy LTP-012: pinch-limited discretised constant-effectiveness HX, sCO2 recuperator; gas-cooler case as `_gascooler` variant, L4) — verified vs the LaboThapPy example re-run (deviations explained: the original's 1 % effectiveness steps, bisection tolerance, property backend ~0.02 %); worker glm-5.3-flash (46 min) |
| 2026-10-09 | C-183 `CSL-0138` | Added *hx_moving_boundary_bell* (TESPy TSP-014: Bell 2015 moving-boundary heat exchanger, zone UA with area constraint) — verified vs the Bell 2015 oracle of TESPy (5 cases, re-run in a venv: 7 tests pass); the worker was stopped by the z.ai weekly limit before its final report — result re-run (exact .sol match), inventory row set and merged by the orchestrator; worker glm-5.3-flash |
| 2026-10-09 | C-175 `CSL-0130` | Added *pipe_pressure_drop_correlations* (LaboThapPy LTP-028: 22 FUNCTIONs — 6 friction factors, Friedel / Müller-Steinhagen-Heck / Choi two-phase dP, acceleration and gravity terms) — verified vs the LaboThapPy re-run (0 differ, max 1.0e-12); header trimmed on review; worker space-bunny |
| 2026-10-09 | C-176 `CSL-0131` | Added *void_fraction_correlations* (LaboThapPy LTP-033: 13 void-fraction models) — native file blocked by CS-BUG-IMPLICIT-PROC (evidence appended); verified `_coolsolve` variant vs the LaboThapPy example re-run (130 values, 0 differ, max 2.2e-5); worker space-bunny (29 min) |
| 2026-10-09 | C-177 `CSL-0132` | Added *r1233zd_thermal_conductivity* (LaboThapPy LTP-048: Perkins & Huber R1233zd(E) thermal conductivity, 2 FUNCTIONs) — verified (8/8); note: the CoolSolve build's bundled fluid data now include this conductivity (released CoolProp does not), documented; header trimmed on review; worker space-bunny (25 min) |
| 2026-10-09 | handover | Work paused by the maintainer (opencode free quota exhausted since 11:00; glm-5.3-flash weekly limit until 2026-10-14). Since 2026-10-08: B-11 planned (C-137) and its 16 [hard] cards imported by glm-5.3-flash; B-12 planned (C-138) and 9 cards translated (C-170…C-177, C-183). Orchestrator reproduced and registered CS-BUG-DUPLICATE-INDEX-EXPR, CS-BUG-DUPLICATE-VAR-BOUND, CS-BUG-CONVERT-UNIT; duplicate register rows folded; header-length rule enforced by csl.py check. 148 models, 432 functions, regression 150/150 |

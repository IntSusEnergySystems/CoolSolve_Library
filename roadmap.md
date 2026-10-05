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

| Library | Count |
|---|---:|
| Models | 10 |
| … verified / runs / modified | 8 / 0 / 0 |
| … blocked / failing / documented only | 2 / 0 / 0 |
| CoolSolve gaps and bugs open (CoolSolve [`docs/model_library_support.md`](https://github.com/CoolProp/CoolSolve/blob/main/docs/model_library_support.md)) | 27 (18 gaps, 8 bugs, 1 doc issue) |
| … closed | 9 (3 gaps, 5 bugs, 1 doc issue) — CoolSolve `main` 2026-10-05 |

| Backlog (source inventories) | Candidates | Distinct | todo | added | merged | discarded | parked |
|---|---:|---:|---:|---:|---:|---:|---:|
| ULiège collection `thermo_models` | 552 | 341 | 494 | 8 | 3 (+5 duplicates) | 42 | 0 |
| CoolSolve examples | 47 | 47 | 39 | 2 | 6 | 0 | 0 |
| LaboThapPy | 74 | 74 | 74 | 0 | 0 | 0 | 0 |
| TESPy | 52 | 52 | 52 | 0 | 0 | 0 | 0 |

Priorities of the candidates (wave1 / high / medium / low / skip):
`thermo_models` 38 / 37 / 142 / 241 / 94 · CoolSolve examples 12 / 24 / 7 / 0 / 3 ·
LaboThapPy 9 / 8 / 17 / 26 / 14 · TESPy 8 / 8 / 23 / 13 / 0.

Refresh with `python3 tools/build_index.py` (models) and
`python3 tools/backlog_stats.py` (candidates).

### Where to resume (handover, 2026-10-05)

- **Next card: B-01 `C-10`** (§6), then `C-11` … `C-13`, then the review
  card `C-14`. C-01 … C-09 are done (models `CSL-0002` … `CSL-0010`).
- **Repository state:** C-01 … C-09 and the removal of the `$UnitSystem`
  lines are committed (`d102799`, `0c2597f`); `work/` is empty; no worker is
  running.
- **CoolSolve:** use the `main` build `../CoolSolve/build/coolsolve`
  (contains the B-01 fixes, branch `fix/library-gaps`). The gaps that still
  block `CSL-0009` and `CSL-0010` are listed in Phase 5; after they are fixed,
  run a `T-RECHECK` of both.
- **Items for the C-14 review:** (1) `CSL-0009` and `CSL-0010` are `blocked`
  but ship a verified runnable variant (`*_coolsolve.eescode`) that
  `test_models.py` skips — decide how variants get a regression baseline;
  (2) CoolSolve `tools/ees_extract.py` still writes a `$UnitSystem` line
  (the workflow now deletes it; consider dropping it in the tool and turning
  `CS-GAP-UNITSYSTEM` into an error); (3) inventory decoding false positive
  found in C-08 (the "761×2 table" of TM-0413 was not the integral table;
  the real one was recovered from the plot objects).
- **How B-01 was executed:** one card per worker, one worker at a time, by
  an orchestrating Claude Code session dispatching to opencode/GLM-5.3
  workers (maintainer's local set-up: skill `~/llm/skill-opencode-orchestrator.md`,
  helpers `~/llm/scripts/csl/`). A card takes 5–20 min; the z.ai plan
  allows ≈ 1 h of work per 5-hour window, the supervisor pauses and resumes
  automatically. Any worker (person or agent) can instead take the next card
  with the prompt of §7.

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
  diffs, update §1, refine this roadmap, the workflow and the templates.
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
- **CoolSolve gaps** are reported in the CoolSolve gap register, never worked
  around by rewriting valid EES code (CoolSolve must read native EES); the
  affected models are `blocked` and re-checked when CoolSolve closes the gap.

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
| 2 | Pilot wave B-01: one card per type of case; adjust the workflow (milestone M1 ≈ 15 models) | 🔄 in progress (9/14 cards) |
| 3 | Production waves, source by source and category by category (M2 = 100, M3 = 300 models) | ☐ |
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

### Phase 2 — Pilot wave 🔄

Run the full workflow once on each type of case (CoolSolve example + EES
original, unit conversion, merge of a family, function library, copied
functions, semi-empirical model, multi-zone model with RAD trigonometry,
dynamic, optimisation, blocked, embedded lookup table, TESPy and LaboThapPy
translations), then adjust the workflow, templates and tools. Batch B-01 in §6.

### Phase 3 — Production waves ☐

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
B-01), **M2** = 100, **M3** = 300.

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
and `CSL-0010`); then native EES
`INTERPOLATE` (`CS-GAP-INTERP-EES`), an error on non-default `$UnitSystem`
(`CS-GAP-UNITSYSTEM`; library models carry no `$UnitSystem` line), unquoted unit names (`CS-GAP-CONVERT-UNQUOTED`),
comments in procedure argument lists (`CS-GAP-PROC-COMMENT`). After each
CoolSolve release: `T-RECHECK` of the blocked models; once `$INCLUDE` exists,
replace the copied function blocks of library models by `$INCLUDE` lines
(`T-MERGE` batch).

Library-side contract, already in place: `library.json` carries the snapshot
identity (content hash of exactly the embedded files, model and function
counts) and the function index; function names are unique; figures are at
most 100 kB.

### Phase 6 — Quality and maintenance (continuous) ☐

- [ ] P6.0 **Maintainer track** (continuous, after each batch): `T-FIGURE` for the runnable models without figure and completion of the `TBD` authors — both lists are printed by `python3 tools/build_index.py`
- [ ] P6.1 Continuous integration (GitHub Actions): `build_index.py --check`, `test_models.py` with the latest CoolSolve release
- [ ] P6.2 Taxonomy reviews at M1, M2, M3 (split crowded categories — `compressors`, `refrigeration_heat_pumps` and `fundamentals` already hold 60–90 candidates; bump the taxonomy version)
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

Open questions: none at the moment.

---

## 5. Backlog (source inventories)

| Source | Inventory | Summary | Main characteristics |
|---|---|---|---|
| ULiège collection `thermo_models` | [inventory](sources/thermo_models/inventory.csv) | [README](sources/thermo_models/README.md) | 341 distinct models; strong in engines, compressors, refrigeration/heat pumps, fundamentals, HVAC; thin in heat transfer, solar, absorption, storage, buildings. 288 of 540 EES files in SI-C-Pa-J; 230 in decimal-comma format; stored EES values (full or partial solution) in all of them |
| CoolSolve examples | [inventory](sources/coolsolve_examples/inventory.csv) | [README](sources/coolsolve_examples/README.md) | 39 of 45 tested examples solve; 19 have their EES original in `CoolSolve/misc/EES_ok.zip` |
| LaboThapPy | [inventory](sources/labothappy/inventory.csv) | [README](sources/labothappy/README.md) | Components (constant-efficiency, semi-empirical, ε-NTU, moving boundary), correlation libraries, cycles; few reference results |
| TESPy | [inventory](sources/tespy/inventory.csv) | [README](sources/tespy/README.md) | Component equations with doctests, validated plants (CGAM, SEGS vs Ebsilon, sCO2 state table) |

---

## 6. Batches

### B-01 — Pilot wave (Phase 2) 🔄


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
[ ] C-10  T-IMPORT     TM-0150 (DG-0032)               → cycles/gas_turbines/two_shaft_gas_turbine_compressor_map   — blocked case (CS-GAP-INTERP-EES, CS-GAP-INCLUDE), ees_import.md Example 2 — NEXT: two attempts interrupted (usage limit), nothing kept; restart from scratch; CS-BUG-LOOKUP-PATH/INTERP-DESC now fixed
[ ] C-11  T-IMPORT     TM-0326                            → buildings/thermal_comfort_pmv_ppd                          — embedded lookup table (74×2)
[ ] C-12  T-TRANSLATE  TSP-035                            → cycles/refrigeration_heat_pumps/heat_pump_basic_tespy      — TESPy tutorial, verified against its results
[ ] C-13  T-TRANSLATE  LTP-013                            → components/heat_exchangers/hx_constant_pinch               — LaboThapPy component
[ ] C-14  T-REVIEW     B-01                                                                                              — update workflow/templates/tools, taxonomy check (M1)
```

### B-02 — CoolSolve examples, first production batch (Phase 3A) ☐

To be prepared after B-01 (`python3 tools/backlog_stats.py --next coolsolve_examples 10`).

---

## 7. Dispatching a batch to agents

Prompt for a worker agent (one card per agent, one agent at a time unless the
cards touch different categories and inventories). Refined during B-01:

```
You are a worker of the CoolSolve Library (/home/sylvain/svn/CoolSolve_Library).
Read docs/model_workflow.md (procedure + definition of done), docs/taxonomy.md,
the finished model models/cycles/refrigeration_heat_pumps/refrigeration_cycle_simple_compressor/
as an example, and CoolSolve docs/ees_import.md (../CoolSolve). Execute this task card:
  <card line from roadmap §6>
<card-specific notes: where the sources are, which group to triage, expected outcome>
Rules:
- Use ../CoolSolve/build/coolsolve and the CoolSolve tools tools/ees_extract.py
  and tools/compare_solution.py.
- Do not modify other models, the taxonomy, roadmap.md or the CoolSolve sources.
  Report a CoolSolve gap in ../CoolSolve/docs/model_library_support.md only with a
  minimal reproducer; do not re-report registered gaps, reference their IDs.
- Never copy source files into the library (reference them by ~/ path, URL or
  library name); work in work/<name>/ and delete it at the end. Convert other unit
  systems by hand (ees_import.md §6); no $UnitSystem line in library files.
- Edit inventory CSV rows minimally (only decision/library_id of your rows). Never
  run git checkout/reset/stash or revert files you did not create. Do not commit.
- Never copy student names or personal data. Do not ask questions: take the most
  reasonable decision and document it in the README.
- A model that cannot run is still done, as a documented blocked/failing/stub model.
- Bookkeeping: set decision/library_id in sources/*/inventory.csv; run
  python3 tools/build_index.py (0 errors) and
  python3 tools/test_models.py <ID> --coolsolve ../CoolSolve/build/coolsolve.
Final message (short): model ID, folder, status, one-line log entry for roadmap §8,
gaps reported, decisions taken / open questions.
```

The manager then checks the folder (README, `model.json`, `.eescode`, `.sol`),
runs `python3 tools/build_index.py` and
`python3 tools/test_models.py <ID> --coolsolve ../CoolSolve/build/coolsolve`,
ticks the card in §6 and adds the log line in §8.

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

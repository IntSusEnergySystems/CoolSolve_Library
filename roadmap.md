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
| Models (B-01 + B-02 reviewed; B-03 cards merged so far included, C-25 review 2026-10-05) | 30 |
| … verified / runs / modified | 24 / 1 / 0 |
| … blocked / failing / documented only | 5 / 0 / 0 |
| CoolSolve gaps and bugs open (CoolSolve [`docs/model_library_support.md`](https://github.com/CoolProp/CoolSolve/blob/main/docs/model_library_support.md)) | 35 (21 gaps, 12 bugs, 2 doc issues) |
| … closed | 9 (3 gaps, 5 bugs, 1 doc issue) — CoolSolve `main` 2026-10-05 |

| Backlog (source inventories) | Candidates | Distinct | todo | added | merged | discarded | parked |
|---|---:|---:|---:|---:|---:|---:|---:|
| ULiège collection `thermo_models` | 552 | 341 | 441 | 16 | 7 (+46 duplicates) | 42 | 0 |
| CoolSolve examples | 47 | 47 | 21 | 17 | 9 | 0 | 0 |
| LaboThapPy | 74 | 74 | 73 | 1 | 0 | 0 | 0 |
| TESPy | 52 | 52 | 51 | 1 | 0 | 0 | 0 |

The tables count inventory **rows**, not models: a model imported from a
CoolSolve example and from its EES original in `thermo_models` has two `added`
rows (`CSL-0017`, `0018`, `0020`–`0023`; workflow §2). Regression at the `C-25`
review: 34 targets (24 model main files + 10 variants), 0 failure.

Priorities of the candidates (wave1 / high / medium / low / skip):
`thermo_models` 38 / 37 / 142 / 241 / 94 · CoolSolve examples 12 / 24 / 7 / 0 / 3 ·
LaboThapPy 9 / 8 / 17 / 26 / 14 · TESPy 8 / 8 / 23 / 13 / 0.

Refresh with `python3 tools/build_index.py` (models) and
`python3 tools/backlog_stats.py` (candidates).

### Where to resume (handover, 2026-10-05)

- **State:** batch B-01 is closed by its review card `C-14` (models `CSL-0001`
  … `CSL-0014`, milestone M1 reached, taxonomy reviewed: no change, see
  P6.2). Batch B-02 (CoolSolve examples, `CSL-0015` …) runs in parallel lanes
  and ends with `C-25`; B-03 is prepared in §6. Next cards: those of §6.
- **Repository state:** everything up to `C-09` is committed (`d102799`,
  `0c2597f`, `6dbd578`); the cards since are in the working tree, for the
  maintainer to review and commit; `work/` is empty.
- **CoolSolve:** use the `main` build `../CoolSolve/build/coolsolve`. Native
  files still blocked, with the gaps to close: `CSL-0009` (`CS-GAP-IF5`,
  `CS-GAP-INTEGRAL-LIMITS`, `CS-BUG-INTEGRAL-TABLE-SEP`,
  `CS-BUG-INTEGRAL-MAXSTEPS`), `CSL-0010` (`CS-GAP-INTEGRAL-LIMITS`,
  `CS-BUG-INTEGRAL-FACTOR`), `CSL-0011` (`CS-GAP-INTERP-EES`,
  `CS-GAP-INCLUDE`), `CSL-0012` (`CS-GAP-IF-DIRECTIVE`, `CS-GAP-LOOKUPROW`,
  `CS-BUG-LOOKUP-STRING`). After a CoolSolve release: `T-RECHECK` (workflow §6).
- **Regression:** `python3 tools/test_models.py --coolsolve ../CoolSolve/build/coolsolve`
  solves the main file of every runnable model **and every variant that has a
  `.sol` next to it**, reported as `CSL-xxxx:variant` — so the runnable
  variants of the blocked models (`CSL-0009`…`0012`) and the variants of
  verified ones are covered (30 targets at C-14: 21 main files + 9 variants; 34 at C-25: 24 + 10; all OK). It takes
  about 4 min, 3 of them for `CSL-0009:coolsolve` (18 000 integration steps):
  `--no-variants` or `--exclude CSL-0009:coolsolve` for a quick run.
- **Decisions of the C-14 review** (workflow updated): (1) variants get a
  regression baseline from their sibling `.sol` (workflow §6); (2) the
  `$UnitSystem` line of `ees_extract.py` and `CS-GAP-UNITSYSTEM` as an error:
  recommendation in Phase 5; (3) decoded embedded tables can be false
  positives: verify against the EES file (workflow §3, step 1).
  `tools/backlog_stats.py` now reports malformed inventory rows (an unquoted
  comma in a `notes` cell shifts `decision`/`library_id`; nine rows of B-01/B-02
  were repaired).
- **For the maintainer:** authors still `TBD` (`CSL-0003`, `CSL-0004`; the
  assistants named in `CSL-0009`/`CSL-0010` come from the inventory, not from
  the files — same course, choose one policy); figures to make
  (`build_index.py` lists them); the pending list of unverified gap suggestions
  (Phase 5); the taxonomy recommendations at M1 (P6.2).
- **How the batches were executed:** one card per worker, one worker at a time
  in B-01, then parallel lanes (one git worktree per card, the orchestrator
  merges the folders, ticks the cards and writes §8) in B-02, by an
  orchestrating Claude Code session dispatching to opencode workers
  (maintainer's local set-up: skill `~/llm/skill-opencode-orchestrator.md`,
  helpers `~/llm/scripts/csl/`). A card takes 5–20 min. Any worker (person or
  agent) can instead take the next card with the prompt of §7.

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
[x] C-10  T-IMPORT     TM-0150 (DG-0032)               → cycles/gas_turbines/two_shaft_gas_turbine_compressor_map   — blocked case (CS-GAP-INTERP-EES, CS-GAP-INCLUDE), ees_import.md Example 2 — NEXT: two attempts interrupted (usage limit), nothing kept; restart from scratch; CS-BUG-LOOKUP-PATH/INTERP-DESC now fixed
[x] C-11  T-IMPORT     TM-0326                            → buildings/thermal_comfort_pmv_ppd                          — embedded lookup table (74×2)
[x] C-12  T-TRANSLATE  TSP-035                            → cycles/refrigeration_heat_pumps/heat_pump_basic_tespy      — TESPy tutorial, verified against its results
[x] C-13  T-TRANSLATE  LTP-013                            → components/heat_exchangers/hx_constant_pinch               — LaboThapPy component
[x] C-14  T-REVIEW     B-01                                                                                              — update workflow/templates/tools, taxonomy check (M1)
```

### B-02 — CoolSolve examples, first production batch (Phase 3A) 🔄

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

### B-03 — CoolSolve examples, second production batch (Phase 3A) ☐

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
[ ] C-32  T-IMPORT     CSX-015 (+EES original)          → components/heat_exchangers/                         — refrigeration evaporator with moist air, wet regime (L2) — CSL-0031
[ ] C-33  T-IMPORT     CSX-009 (+EES original)          → components/heat_exchangers/                         — wet air-cooled condenser, spray evaporative cooling (L2) — CSL-0032
[ ] C-34  T-IMPORT     CSX-020 (+EES original)          → cycles/refrigeration_heat_pumps/                    — R22 heat pump with semi-hermetic compressor model (L2) — CSL-0033
[x] C-35  T-IMPORT     CSX-026 (+EES original)          → cycles/engines/                                     — internal combustion engine cycle with cpbar (L2), uses CSL-0005 cpbar — CSL-0034
[ ] C-36  T-IMPORT     CSX-045 (+EES original)          → components/compressors/                             — centrifugal compressor with lookup-table map (L2), after C-23 (CSL-0023) — CSL-0035
[x] C-37  T-IMPORT     CSX-030 (+EES original)          → cycles/organic_rankine/                             — ORC with two-stage expander and extraction, R134a (L3) — CSL-0036
[ ] C-38  T-REVIEW     B-03                                                                                      — checks, diffs, §1, workflow; plan B-04 (remaining examples: dynamic, L3–L4, absorption)
```


---

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
- Runnable variant: the rule "never rewrite valid EES code to work around a CoolSolve gap" applies to the native
  file only. When the native file is blocked and a faithful runnable transcription is possible, ship it as a separate
  documented variant `<name>_coolsolve.eescode` (+ .sol) verified against the EES reference, as models CSL-0009/CSL-0010.
- Never call CoolSolve-only syntax "valid EES". A new gap or bug may be registered only with evidence that the EES
  syntax/behaviour is valid (an EES manual/doc reference or an existing EES file that uses it) and a minimal reproducer;
  without such evidence, describe it in your final message as "unverified suggestion" and do not register it.
- model.json `missing_features` lists every registered gap ID that blocks the native file (those of the card included).
  In the inventory, also write a one-line reason in the `notes` cell of every row you decide on.
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

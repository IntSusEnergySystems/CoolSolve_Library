# Model workflow

How models enter the library, one small, tested step at a time. The
[roadmap](../roadmap.md) says *what* to do next; this page says *how*. It is
written for the people and agents who execute the tasks (workers) and for the
person who prepares and reviews them (manager).

Companion documents in the CoolSolve repository (cloned next to this one, as
`../CoolSolve`):
[`docs/ees_import.md`](https://github.com/CoolProp/CoolSolve/blob/main/docs/ees_import.md)
(EES extraction, manual unit conversion, verification),
[`docs/debugging_models.md`](https://github.com/CoolProp/CoolSolve/blob/main/docs/debugging_models.md)
(convergence problems),
[`docs/model_library_support.md`](https://github.com/CoolProp/CoolSolve/blob/main/docs/model_library_support.md)
(CoolSolve gap register).

---

## 1. Organisation

- **Unit of work = one task card**: one candidate (or one group of
  near-duplicates) taken from a source inventory, processed to a *done* state
  and left in the working tree for review: **only the maintainer commits**. A model that cannot run is still *done* when its folder,
  documentation and status (`blocked`, `failing` or `stub`) are complete.
- **Manager**: selects the next cards from the inventories (`sources/*/inventory.csv`,
  by `priority`), writes them as a batch in the roadmap, reviews the results,
  runs the checks, marks the cards done, refines the roadmap.
- **Workers** (people or agents; at most two in parallel, on different
  categories to avoid ID and folder clashes): execute one card at a time,
  following this page; never change the taxonomy or another model without a
  card saying so.
- **Maintainer** (S. Quoilin): reviews and **commits** the work, completes the
  authors that could not be found (`TBD`), adds a **figure** to every runnable
  model (§7), decides on taxonomy changes and reviews corrections of the
  original models.

### Task types

| Type | Input | Output | Section |
|---|---|---|---|
| `T-TRIAGE` | A group of candidates (same system, near-duplicates, exam variants) | A decision per candidate, recorded in the inventory | §2 |
| `T-IMPORT` | One EES model (`.ees` file or CoolSolve example) | A model folder | §3 |
| `T-FUNC` | An EES `.lib` file or a set of functions | A *function* model folder | §4 |
| `T-TRANSLATE` | A model from another language (LaboThapPy, TESPy, Python, Modelica, paper) | A model folder | §5 |
| `T-MERGE` | A candidate judged equivalent/complementary to a library model | Updated model (variant, better documentation) | §2 |
| `T-RECHECK` | A CoolSolve gap closed in a new release | Re-tested blocked models, statuses updated | §6 |
| `T-GAP` | A CoolSolve limitation met during a task | A row in the CoolSolve gap register | §6 |
| `T-FIGURE` | A runnable model without figure | A diagram or plot in `figures/`, shown in the README (maintainer) | §7 |
| `T-TAXO` | Taxonomy review | Updated `taxonomy.json`, moved folders | [taxonomy.md §6](taxonomy.md#6-changing-the-taxonomy-without-breaking-anything) |
| `T-TOOL` | Tooling need | Script/doc update | – |
| `T-REVIEW` | A finished batch | Checks run (index, regression with variants, inventories), workflow/templates/taxonomy refined, roadmap updated | roadmap §2 |

---

## 2. Triage: add, merge, replace or discard

Process the candidates of one `duplicate_group` (or of one topic) together and
decide for each of them with this decision tree:

1. **Is it a usable model?** Scratch files, empty or broken files, pure
   copies, student answers, files that only make sense with a missing data file
   → `discarded` (state the reason).
2. **Publication.** The local collection (`thermo_models`) comes from the
   maintainer's laboratory and is published under the library license (MIT).
   Models taken from other libraries (LaboThapPy, TESPy…) are translated and
   **credit the authors of the original model** (§5). Never copy personal data
   (student names, student numbers).
3. **Exams** are published as **examples** (titled and described as an example,
   never as an exam). Exams are often built on an exercise with a few values
   changed: such an exam is a `duplicate` of that exercise. An exam split into
   several question files that describe one system becomes **one** example
   model.
4. **Does the library already have a model of the same system and purpose?**
   (same component or cycle, same physics, same inputs/outputs up to
   parameter values — check `library.csv` by category, tags and fluids)
   - **No** → `added` (task `T-IMPORT`/`T-FUNC`/`T-TRANSLATE`).
   - **Yes, and the candidate is better** (by order of importance:
     correctness, documentation, generality, verification data, recency) →
     `superseding`: the candidate's content replaces the model's content
     **under the same ID**; the conversion log explains the replacement.
   - **Yes, equivalent, or only other input values** (typical of exams and of
     yearly versions of an exercise) → `duplicate` (note the library ID).
   - **Yes, same structure but other assumptions that add value** (another
     fluid, part-load instead of design, other geometry) → `merged`: document
     it in the existing model (variant file `<name>_<variant>.eescode` or an
     extra results table) instead of creating a new model.
   - **Yes, but a different level of detail** (constant-efficiency vs
     semi-empirical vs discretised) → `added` as a separate model, linked in
     both `related` fields.
5. Pick the **representative** of the group (best documented, most correct,
   newest EES version) as the file to import; skim the others for better
   comments, data, corrections or author names.

Decide `duplicate` only after comparing the equations (strip comments and
blanks, then diff): identical equations → `duplicate`; same system with other
equations, assumptions or closures → `merged`, and write the difference in the
model README (a variant file or a table, otherwise say that it is described
only). Record every decision in the source inventory, columns `decision`
(`todo`, `added`, `superseding`, `merged`, `duplicate`, `discarded`, `parked`)
and `library_id`, with a **one-line reason in the `notes` cell of every row you
decide on** (duplicates and discarded files included). Edit only these cells of
your rows and keep the rest of the file byte-identical; **put a `notes` cell
that contains a comma between double quotes** — an unquoted comma shifts
`decision` and `library_id` to the wrong columns (`python3 tools/backlog_stats.py`
reports such rows as errors). Edit the cells by line surgery (the last cells of
the line); never rewrite an inventory with a csv writer: `thermo_models` rows
carry extra trailing columns and a rewrite changes the quoting of other rows.
`parked` is reserved for **publication issues** (licence, personal data,
third-party content that may not be published): a candidate that is merely a
different exercise, or not yet processed, stays `todo` (a note is welcome).

**CoolSolve examples** (`coolsolve_examples`; the example stays in the CoolSolve
repository) follow the C-01 pattern: the row of the file the model is imported
from — the example, with its EES original from `misc/EES_ok.zip` or
`thermo_models` as verification reference — is `added` with the new `library_id`;
the other rows of the same system (variants, earlier conversions, copies of the
same exercise) are `merged` or `duplicate` and name that ID. When the EES
original is itself a row of `thermo_models` (the model then follows that file,
`model.json` `origin.candidate_id`), its row is `added` with the same ID too:
two `added` rows, one model (`backlog_stats.py` counts rows, not models). The
note of the example row says where the library model differs from the example
(typo, imposed input, simplified transcription). Never leave a processed row
at `todo`.

---

## 3. `T-IMPORT`: import an EES model

Commands assume the two repositories side by side (`../CoolSolve`) and a
CoolSolve build in `../CoolSolve/build/coolsolve`.

**Source files never enter the library.** The extraction, the reference data
and, if useful, a copy of the source file live in a temporary work folder
`work/<name>/` (ignored by git) during the import and are deleted when the card
is closed. The model folder keeps only the CoolSolve files (`.eescode`,
`.initials`, `-<table>.csv`, `coolsolve.conf`, `.sol`), the README, `model.json`
and `figures/`; the source is referenced in `model.json` (`origin.source_path`
with `~` for the home directory, or `origin.url`, or the model name in an
existing library). `tools/build_index.py` rejects source files and
`original/`/`reference/` folders.

1. **Extract** (never edit the source collection):
   ```bash
   python3 ../CoolSolve/tools/ees_extract.py "<source>/<path>/File.EES" -o work/<name> --name <name>
   ```
   Read `work/<name>/reference/ees_extract_report.md`: EES version, **unit
   system**, lookup/parametric tables, **functions called but not defined**,
   warnings (−9999 values, unsupported features).

   **Embedded tables are decoded by a heuristic: expect false positives.** The
   `tables` column of the inventory and the report may show a table that is not
   one (TM-0413: "761×2" was not the integral table; TM-0326: "74×2" was a
   mis-decoded pair of string-keyed lookup tables, `CS-BUG-EXTRACT-LOOKUP-STRING`)
   or miss one. Never trust a decoded table without checking it against the
   EES file: its row/column counts and a few values (the equations that call
   `LOOKUP`/`INTERPOLATE`, the table names, the stored solution), the **plot
   objects** of the file (a time series or an integral table is often stored
   there, as for TM-0413), or a hand decoding of the binary. State in the README
   how the table was recovered and checked.
2. **Find the authors.** Look in the file: header comments ("Author", "Auteur",
   "par", names, dates), comments next to the equations, the folder and file
   names (initials, see the table below), and the `authors` column of the
   inventory. The `{$ID$…}` tag gives the EES licence holder, not necessarily
   the author. If no author can be identified, write `"TBD"`: the maintainer
   completes it (`tools/build_index.py` lists these models). An institution or a
   course alone is not an author: write `"TBD (<institution, course>)"`.

   | Initials | Author |
   |---|---|
   | SB | Stéphane Bertagnolio |
   | VL | Vincent Lemort |
   | others | to be confirmed by the maintainer before use |

   A header such as `VL050517` is initials + `YYMMDD` (here 2005-05-17); the
   date of the file in the collection (often 2017, the date of a copy) is not
   the date of the exercise.

3. **Faithful run** (in the work folder): complete what EES provided
   implicitly (parametric-table inputs → default run; external lookup files →
   CSV; library functions → copied block), solve, and **verify against the EES
   reference**:
   ```bash
   ../CoolSolve/build/coolsolve ./<name>.eescode          # note the ./ (CS-BUG-LOOKUP-PATH)
   python3 ../CoolSolve/tools/compare_solution.py <name>.sol reference/ees_variables.csv
   ```
   If it does not converge: CoolSolve `docs/debugging_models.md` (debug folder,
   simplified model for initials, *Try Harder*/`coolsolve.conf`). Time-box the
   effort; if it still fails, set `failing` with the diagnosis, or `blocked` if
   a CoolSolve gap is the cause (§6). **Before declaring an EES model over- or
   under-determined (C-37, `CSL-0036`), solve the extraction unmodified** (NUL
   byte and `$UnitSystem` line removed, `.initials` from the stored solution)
   and read the `System square` line of the statistics: when it is square the
   model is faithful as it stands, and variables that look like free inputs
   (`V_s_exp`, `x_ext`…) are outputs of design equations (`W_dot = 5000` sizing
   a displacement, `epsilon_s = 0.5` fixing a work). Never replace equations of
   the original by values taken from the stored solution: stored values of
   unknowns belong in `.initials`. Keep EES syntax in the native file
   (principle: CoolSolve must read native EES); a faithful runnable variant of a
   blocked file is shipped separately (§6). **Quote tolerances exactly as
   `compare_solution.py` prints them** (README, `verification.max_rel_diff`: the
   maximum over all common variables), and explain every deviation above them
   (property backend, reference state…); if you leave variables out of the figure
   (absolute `h`/`s` carrying a reference-state offset, diagnostic outputs), name
   them next to it.
4. **Convert the units by hand** if the report shows anything other than
   `SI MASS DEG PA C J`: every input value, every equation, every constant, the
   tables and the guesses, following CoolSolve `docs/ees_import.md` §6; verify
   again with `compare_solution.py … --ees-units`. Never rely on the
   `$UnitSystem` directive or on automatic scaling, and delete the directive
   (CoolSolve has a single unit system, SI-°C-Pa-J).
5. **Curate** (each change logged in the README conversion log):
   standard header (`templates/model/header.eescode`), comments in English,
   corrections of genuine errors (with their impact on the results), removal
   of dead code. Keep variable names unless they are misleading. **Comments do
   not invent physical meaning**: paraphrase the original's own comments or
   write "as in the original"; give every dimensional quantity its SI unit
   (`[-]` only for dimensionless ones); check a physical word against the
   numbers (a state called "compression" must show a pressure rise, C-35).
   A library `PROCEDURE` that the original calls in function position
   (`c_p = cpbar(...)`) and that the library ships with several outputs is
   transcribed with `CALL`: the form is valid EES and no equation changes, so it
   is not a `_coolsolve` variant — say so in the conversion log (`CSL-0034`;
   whether EES accepts the function form with a multi-output procedure is an open
   suggestion, `CS-GAP-PROC-MULTIOUT`, not registered). Fluid names follow §9. If the model
   is a cycle or a component on a real fluid, make it **diagram-ready**: add at
   the end a block of post-processing equations giving the state points as
   arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (pattern: `CSL-0001`, block *State
   points for the thermodynamic diagrams*), and check that the results of the
   model are unchanged. The automatic overlay of the CoolSolve diagram only
   finds states whose variables share a suffix (`T_1`, `h_1`, `P_1`…), which is
   rarely the case in EES models.
6. **Create the model folder** `models/<category>/<name>/` from
   `templates/model/` and move the model files from the work folder; solve in
   the model folder to produce the `.sol` baseline; delete `*_report.tex` and
   debug folders.
7. **Document**: `README.md` (all template sections, results table, the figure
   placeholder of §7), `model.json` (ID = next free ID printed by
   `tools/build_index.py`; level computed with
   [taxonomy.md §3](taxonomy.md#3-level--complexity-rating); source path with `~`;
   `verification.coolsolve_version` = the version the binary prints plus the
   commit of the CoolSolve checkout that built it, e.g. `0.3.0@fbdb6a7` from
   `git -C ../CoolSolve rev-parse --short HEAD` — not `main <date>`; `build_index.py`
   warns otherwise). `related` holds plain `CSL-xxxx` ids (prose goes to the
   README), with the back-link in the `model.json` of the other model, and
   mentions only models that exist (parallel cards: no "planned"/"forthcoming").
   Write the level justification (score of taxonomy.md §3) in the conversion
   log; check every README sentence about a trajectory or a sweep against the
   output table; label a CoolSolve-only construct (e.g. the three-argument
   `IF`) as such.
8. **Register and test**:
   ```bash
   python3 tools/build_index.py            # must report 0 errors
   python3 tools/test_models.py CSL-XXXX --coolsolve ../CoolSolve/build/coolsolve
   python3 tools/backlog_stats.py          # no ERROR: inventory rows well-formed
   ```
   `test_models.py` also tests the variants of the model that have a `.sol`
   (`CSL-XXXX:variant`, §6); `CSL-XXXX:variant` selects one, `--no-variants` skips them.
9. **Close the card**: inventory `decision`/`library_id`, one line in the
   roadmap progress log, gap register rows if any; **delete `work/<name>/`**.
   Do not commit: the maintainer reviews and commits (suggested message
   `CSL-XXXX: add <name> (<status>)`).

CoolSolve examples (source `coolsolve_examples`) follow the same procedure,
starting from the `.eescode` file and, when the original `.EES` file is in
CoolSolve `misc/EES_ok.zip` or in `thermo_models`, using its stored solution as
reference. The example itself stays in the CoolSolve repository.

---

## 4. `T-FUNC`: function libraries (`.lib`)

1. `.lib` files are plain Windows-1252 text: convert to UTF-8 and remove the
   `{$DS.}` tag.
2. Build one *function model*: all `FUNCTION`/`PROCEDURE` definitions at the
   top (documented: purpose, inputs/outputs with units, validity range,
   reference), then a short main program that calls each of them with typical
   values (and, when possible, checks the result against a published value).
   Pattern: CoolSolve `examples/cpbar.eescode`. Units: SI-°C-Pa-J, converted by
   hand if needed.
3. Name it after the main function or the family (`cpbar_combustion_gases`,
   `two_phase_htc_correlations`), `kind = function`. Its functions are listed
   automatically in `functions.csv`.
4. Function names must be unique across the library (`tools/build_index.py`
   warns otherwise): CoolSolve resolves `$INCLUDE library:<name>` and its
   editor quick-fixes through them.
5. Models that need these functions will write `$INCLUDE library:<name>`
   (CoolSolve `CS-FEAT-IMPORT`: all functions and procedures of the
   `.eescode` file are imported, its demonstration program is ignored). Until
   CoolSolve supports it, copy the definitions in a block
   `{--- Library functions copied from CSL-XXXX ---}`, and list `CSL-XXXX` in
   their `related` field.

---

## 5. `T-TRANSLATE`: models from other tools

For LaboThapPy, TESPy and other Python/Modelica/paper models (see
`sources/<source>/README.md` for source-specific guidelines):

- Translate the **physics**, not the code: iterative loops and numerical
  solvers become simultaneous equations; discretisation loops become
  `DUPLICATE` arrays; `PropsSI` calls become EES property functions (units:
  °C, Pa, J, fluid names as in §9: a CoolProp `'CO2'` becomes `R744`);
  optimiser calls make the model `kind = optimization`.
- Keep the variable naming of the source where possible, and cite equations
  (paper, documentation page).
- Verify against the source's own results (tests, documentation examples,
  notebooks): reproduce their inputs, compare outputs (`verified`), otherwise
  `runs`.
- **Credits are mandatory**: the authors of the original model, the library
  (name, URL, version or commit hash) and the scientific reference (paper,
  thesis) in `model.json` `origin` and in the README *Source and attribution*
  section (ready-made attribution blocks in `sources/labothappy/README.md` and
  `sources/tespy/README.md`). The licenses of these libraries are permissive
  and allow the translation; the model is published under the library license.

---

**Correlations taken from a library** (e.g. `ht`, LaboThapPy, ThermoCycle): cite both the original
paper/book of the correlation and the library (version, module, function) from which the equations were taken,
in the function's comment block, the README and `model.json`.

## 6. CoolSolve gaps, blocked models and re-checks

**Registering a gap or bug (`T-GAP`).** Read the CoolSolve register
(`../CoolSolve/docs/model_library_support.md`) first and reference the ID of an
already registered gap instead of re-reporting it. Register a new one **only
with evidence that the EES syntax or behaviour is valid** — a reference in the
EES manual/help, or an existing EES file that uses it — **and a minimal
reproducer written in valid EES**. Without such evidence, do not register: put
it in your final message as an *unverified suggestion* (the maintainer keeps a
pending list, roadmap Phase 5). Follow the column count of the register section
you write in; bugs of the tools (`ees_extract.py`, `compare_solution.py`) go in
the register too. Any claim "EES/CoolSolve cannot / does X" needs a minimal run
or a file reference.

**Blocked native file.** When a model fails because of CoolSolve, set its status
to `blocked` and put in `missing_features` **every** registered gap ID that
blocks the native file (those of the card and those found later;
`CS-GAP-OPTIM` is also listed for an optimisation model shipped at the optimum,
for information). The native file stays in valid EES: never rewrite it around
a gap. Never call CoolSolve-only syntax "valid EES" (write "CoolSolve-only
syntax, not valid EES").

**Runnable variant.** When a faithful runnable transcription exists, ship it
next to the native file as `<name>_coolsolve.eescode` (+ `.sol`, and `.initials`
or companion tables when needed). This is the only place where the code is
rewritten around a gap, and:

- it changes **only what the gap forces**, keeps the variable names, and **logs
  every change** (header of the variant + README conversion log), stating when
  it uses CoolSolve-only syntax;
- it is verified against the same EES reference as the native file would be
  (README *Verification* says it concerns the variant);
- **lookup tables**: the native file ships its tables as EES expects them
  (e.g. string-keyed `<name>-<table>.csv`); the variant has its own companion
  tables `<name>_coolsolve-<table>.csv`, with default values agreeing with the
  native ones;
- **regression**: `tools/test_models.py` solves every `*.eescode` of a model
  folder that has a sibling `.sol` of the same stem and compares it with that
  baseline (reported as `CSL-xxxx:variant`, e.g. `CSL-0009:coolsolve`),
  whatever the status of the model; blocked native files are skipped. A variant
  without `.sol` is not tested: always commit its `.sol`.

**`MODULE` and `SUBPROGRAM` (decision D10).** CoolSolve will not implement
`MODULE`/`SUBPROGRAM` in the near future (`CS-GAP-MODULE`, not planned). Their
equations are therefore **flattened into the main program** of the library
model:

- each `CALL` of a module/subprogram is replaced by a copy of its equations in
  which the formal inputs and outputs are replaced by the actual arguments of
  the call;
- the internal variables of the module are **renamed per call** with a suffix
  `<variable>_<tag>` (`tag` = short name of the component, or `1`, `2`, … for
  repeated calls; arrays `X[i]` → `X_<tag>[i]`); check that no renamed variable
  collides with an existing one;
- the flattened file is the main model file `<name>.eescode` and stays valid
  EES; no file with the `MODULE` block and no `_coolsolve` variant are made for
  this reason alone (the source is referenced as usual). `FUNCTION`s and
  `PROCEDURE`s are kept as they are;
- the file header and the README conversion log give the mapping (call → tag,
  formal → actual arguments, renamed variables); `language_features` records
  `MODULE flattened` (or `SUBPROGRAM flattened`); `CS-GAP-MODULE` is **not**
  listed in `missing_features`;
- the status follows the verification against the EES reference (`verified`
  when it matches, the stored EES values of the module variables being compared
  under their new names). Other blocking gaps of the flattened file follow the
  blocked/variant rules above.

**Property calls with the (T, H) input pair (decision D11).** CoolProp, hence
CoolSolve, will not get the (T, H) input pair (`CS-GAP-PROP-TH`, not planned).
A property call such as `quality(fluid$,H=h[4],T=T[4])` is therefore
**rewritten in the model itself** through an equivalent input pair:

- two-phase state known from the physics (e.g. after an expansion valve, in an
  evaporator): add `P_<n> = pressure(fluid$,T=T[n],x=0)` (saturation pressure,
  or reuse an existing pressure variable of that state) and call the property
  with (P, H): `x[4] = quality(fluid$,P=P_4,H=h[4])`;
- single-phase or unknown phase: add an auxiliary pressure unknown with the
  implicit equation `h[n] = enthalpy(fluid$,T=T[n],P=P_<n>)` (with a guess in
  `.initials`), then call the property with (P, H);
- keep the variable names, log every rewritten call (file header + README
  conversion log, "decision D11"), keep the file valid EES; the rewritten file
  is the main model file (no native/variant split for this reason alone);
  `CS-GAP-PROP-TH` is **not** listed in `missing_features`; the status follows
  the verification against the EES reference.

**Re-checks (`T-RECHECK`).** When a CoolSolve release closes gaps, filter
`library.csv` on `missing_features`, run the native files, and update status,
`missing_features`, README and baseline (`.sol` of the native file). Keep or
delete the variant as the README decides; while it exists it stays in the
regression.

## 7. Figures (`T-FIGURE`, maintainer)

Every runnable model gets one figure — a thermodynamic diagram or another
relevant plot — made by the maintainer in the CoolSolve GUI after the model is
included (`tools/build_index.py` lists the runnable models without figure):

1. Open `models/<category>/<name>/<name>.eescode` in the CoolSolve GUI and
   solve it.
2. Make the figure:
   - **cycles and components on a real fluid**: *Diagrams* tab → fluid (the
     model's fluids are listed first), T-s / P-h / h-s / T-h, *Generate*; tick
     *Array overlay*, choose the columns (e.g. X = `h`, Y = `P` for a P-h
     diagram, X = `s`, Y = `T` for a T-s diagram), tick *Close loop* for a
     cycle; export with the camera icon of the plot toolbar (*Download plot as
     a PNG*; SVG is also offered);
   - **other models**: *Parametric* tab (sweep of an input, 1D/2D plot) or, for
     dynamic models, the *Integral* tab trajectory; export PNG with the plot
     toolbar (camera icon);
   - **ideal-gas and humid-air models** (air-standard cycles, gas turbines on
     `Air`, HVAC models on `AirH2O`): CoolSolve has no ideal-gas diagram nor
     psychrometric chart yet (`CS-FEAT-DIAGRAM-IDEAL`, `CS-FEAT-PSYCHRO`), so
     their figure is a **parametric sweep plot** (roadmap decision D7), e.g.
     efficiency vs pressure ratio for a Brayton cycle.
3. Save it as `figures/<name>_<type>.png` (or `.svg`), **at most 100 kB** (the
   figures are embedded in the CoolSolve binary; a 900×600 PNG is typically
   70 kB), e.g.
   `figures/refrigeration_cycle_simple_compressor_ph.png`, and replace the
   figure placeholder of the README *Results* section by
   `![P-h diagram of the cycle](figures/<name>_ph.png)` with a one-line caption.
4. Run `python3 tools/build_index.py` (the `figures` column of `library.csv` is
   updated) and commit.

Workers prepare this step: the README contains the placeholder and the model
contains the state-point arrays (§3, step 5). This procedure was tested on
`CSL-0001` (R22 cycle on the P-h diagram, PNG export) on 2026-10-04.

---

## 8. Definition of done (per model)

- [ ] Folder `models/<category>/<name>/` with `README.md`, `model.json` and the
      `.eescode` file — **no source file, no `original/` or `reference/` folder**
- [ ] Source referenced in `model.json` (`~/…` path, URL or library name); authors
      found in the file or `TBD`
- [ ] Header, English comments, no `$UnitSystem` directive, units converted
      by hand when needed
- [ ] Status set and justified: verification table (`verified`), sanity checks
      (`runs`), list of changes (`modified`), gap IDs (`blocked`: **all** the
      gaps blocking the native file in `missing_features`), diagnosis
      (`failing`); tolerances quoted as `compare_solution.py` prints them
- [ ] `.sol` baseline produced for runnable models **and for every runnable
      variant** (`*_coolsolve.eescode`, …); `tools/test_models.py <ID>` passes
      (variants included, reported as `<ID>:variant`)
- [ ] README with the figure placeholder (runnable models)
- [ ] `tools/build_index.py` reports 0 errors; generated files updated (left uncommitted: the maintainer commits)
- [ ] Inventory `decision`, `library_id` and a one-line reason in `notes` for every
      row decided on; roadmap log line, gap register updated (evidence rule, §6);
      work folder deleted

## 9. Style guide for `.eescode` files

- No `$UnitSystem` directive: CoolSolve has a single unit system (SI mass basis,
  °C, Pa, J, degrees for trigonometry); the file starts with the header block.
- Section titles as displayed comments: `"!Compressor model"`.
- One equation per line; explanation and units in a trailing comment:
  `W_dot = W_dot_loss_0 + (1 + alpha)*W_dot_in   "electrical power [W]"`.
- Converted input values keep the original value in their comment:
  `p_t = 500E3 [Pa]  "500 kPa in the original"`.
- EES naming conventions are kept (`T_su`, `P_ex`, `M_dot_r`, `h_ex_s`, `DELTAT_sc`).
- Comments paraphrase the original's or say "as in the original"; they never
  invent physical meaning. Dimensional quantities carry their SI unit; `[-]` is
  for dimensionless ones only.
- **Fluid names**: chemical formulas (`CO2`, `N2`, `O2`, `H2O`, `Air`) are
  **ideal-gas** substances in EES (their enthalpy includes the formation
  enthalpy); real fluids use their names (`R744` or `CarbonDioxide`, `Nitrogen`,
  `Water`, `R134a`; `AirH2O` for humid air). Translating a source that calls
  CoolProp `'CO2'` for the real fluid therefore gives `R744`.
- No EES GUI tags (`{$ID$…}`, `{$PX$…}`), no commented-out dead code unless it
  documents an alternative (then say so).

# <Title>

<level badge> &nbsp;|&nbsp; <kind badge> &nbsp;|&nbsp; <status badge> &nbsp;|&nbsp; `CSL-XXXX`

<!-- Badges (copy exactly, see docs/taxonomy.md):
  🟢 **Level 1 · Introductory** | 🔵 **Level 2 · Intermediate** | 🟠 **Level 3 · Advanced** | 🔴 **Level 4 · Research**
  ⚙️ **Steady-state** | ⏱️ **Dynamic** | 🎯 **Optimisation** | 🧩 **Function library**
  ✅ **Verified** | ☑️ **Runs** | ⚠️ **Runs (modified)** | ⛔ **Blocked** | ❌ **Failing** | 📄 **Documented only**
-->

<One paragraph: what the model represents and what it is useful for.>

| | |
|---|---|
| **Category** | <Top category> › <Sub-category> (titles of `taxonomy.json`, e.g. Cycles and machines › Steam power cycles) |
| **Fluids** | <fluids> |
| **Size** | <n> equations (largest block: <m>) |
| **Source** | <source, with link when public> |
| **Authors** | <authors of the original model, or TBD> |
| **License** | MIT |
| **CoolSolve** | <version> — <runs / verified against … / blocked by CS-GAP-…> |

## Problem statement
<For exercises: the statement, translated. For research/component models: purpose and context.>

## Model
<Assumptions, governing equations (LaTeX allowed), sub-models, correlations; inputs/outputs table.>

## How to run
<GUI / CLI command, notes on guesses (`.initials`), `coolsolve.conf` if any, variants.
 Blocked native file: list the runnable variant(s) `<name>_coolsolve.eescode` — what the gap forces
 (every change is logged in the conversion log), its `.sol` baseline (tested as `CSL-XXXX:coolsolve`).>

## Results
<Main results table.>

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification
<Reference used (EES stored solution, parametric table, publication, other tool), comparison table, tolerance quoted exactly as
 `compare_solution.py` prints it, explained deviations. Blocked model: say it is the variant that was verified.>

## Source and attribution
<Authors of the original model (found in the file, or TBD), institution, course or publication, library and
 version/commit for translated models. Source: `~/…` path of the source file, URL, or name in an existing library.>

## Conversion log
- **YYYY-MM-DD — import**: <tool, unit-system conversion, inputs restored, comments translated…>
- **YYYY-MM-DD — <change>**: <corrections, simplifications, merges, with their impact on results>
- **Level**: <score of docs/taxonomy.md §3, criterion by criterion> → level N

## Limitations and CoolSolve gaps
<Physical limitations; CoolSolve gaps (CS-GAP-… IDs, see CoolSolve docs/model_library_support.md): one line per gap that
 blocks the native file, i.e. every ID of `missing_features`.>

## Related models
<CSL-xxxx (title): how it relates (variant, merged, uses its functions…). The same ids, and only ids, go to
 `model.json` `related`, with the back-link in the other model's `model.json`.>

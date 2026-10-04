# Source: CoolSolve examples

The 47 `.eescode` files of the CoolSolve repository (`examples/`), used by the
CoolSolve test suite (`test_examples.cpp`, report `examples/test_examples.md`).
They **remain in CoolSolve** as regression fixtures; the library classifies them
and holds curated copies (header, English comments, verification, README).

| Item | Value |
|---|---|
| Location | `CoolSolve/examples/*.eescode` (+ `.initials`, `.sol`, `-<table>.csv`) |
| Authors | S. Quoilin and the ULiège Thermodynamics Laboratory (most are exercises or research models from the `thermo_models` collection, already translated to English); CoolSolve developers for the feature demos |
| License | MIT (CoolSolve) |
| Language | English comments, units SI-C-Pa-J |
| Status in CoolSolve (test report of 2026-08-26) | 39 of 45 tested files solve and match their expected values; failures: `building_rc_network` (lookup in an integral model), `cooling_tower2`, `orc_complex` (comments inside procedure argument lists), `simple_centrifugal_compressor`, `turbocompressor_interpolate` (missing lookup table), `water_libr` (LiBr functions); `expander_module` (MODULE) and `orc_solar_complex` are not in the test report |

## Handling rules

- **Skip** the three CoolSolve fixtures that are not thermodynamic models:
  `advanced_features`, `integral_decay`, `lookup_demo` (they stay in CoolSolve
  only).
- 19 examples were translated from the 20 EES files archived in CoolSolve
  `misc/EES_ok.zip` (`exchangers1–3`, `humidair1–2`, `rankine1–2`,
  `refrigeration1–3`, `condenser_3zones`, `expander_module`, `orc_complex`,
  `orc_extraction`, `orc_r245fa`, `orc_simple`, `orc_solar_complex`,
  `pressuredrop`, `scroll_compressor`), together with their EES residuals and
  LaTeX exports (the 20th, `orc_ammonia`, has no example yet). Import each
  example **with its original EES file**: the EES
  file gives the **stored solution** for verification (`ees_extract.py`) and
  the original text; the example gives the existing translation and fixes.
  The research models among them (`condenser_3zones`, `expander_module`,
  `scroll_compressor`) also exist in several versions in `thermo_models`:
  triage them as one group and record the decision for every inventory row.
- Several examples are **rewritten variants** of EES originals (e.g.
  `compressor_refrigeration_simple` computes R22 and R134a side by side to
  emulate an EES parametric table). The library keeps the native EES
  structure; the example is then `merged` into the library model (see
  `CSL-0001`).
- Examples that fail in CoolSolve because of a CoolSolve gap become `blocked`
  library models with the gap IDs of CoolSolve `docs/model_library_support.md`.

## Inventory

[`inventory.csv`](inventory.csv) — one row per example (candidate IDs
`CSX-001`…`CSX-047`), with category, kind, level and priority guesses, test
status and duplicate groups (`G-…`) in `notes`/`duplicate_group`.

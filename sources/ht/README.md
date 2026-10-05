# `ht` (Caleb Bell) — source sweep for the CoolSolve_Library

Quick sweep (not an audit) of the Python library **`ht`**, the heat-transfer component of ChEDL, to build the
backlog of correlations that can be translated into EES-language `FUNCTION`s. The machine-readable backlog is
[`inventory.csv`](inventory.csv) — **24 rows, one per family** (`HT-001` … `HT-024`), covering **222 of the 272 public
functions** of `ht/ht/`.

This is the deliverable of roadmap card **C-95** (`T-TRIAGE`): it produces **no model folder**. The translation
cards are proposed in the final message of that card and go in roadmap §6 (batch B-09).

| | |
|---|---|
| Repository | https://github.com/CalebBell/ht (local clone `~/git/ht`, commit `85e0ee6`, 2025-12-07, checked out on `master`) |
| Version | `1.2.0` (`pyproject.toml`) |
| License | **MIT** (`LICENSE.txt`: "Copyright (C) 2016, Caleb Bell <Caleb.Andrew.Bell@gmail.com>") |
| Author / how to cite | Caleb Bell and Contributors (2016-2025), *ht: Heat transfer component of Chemical Engineering Design Library (ChEDL)*, https://github.com/CalebBell/ht (citation block in `README.rst`) |
| Companion library | [`fluids`](https://github.com/CalebBell/fluids) (same author, MIT): **friction factors, two-phase pressure drop, dimensionless numbers and the numerical helpers live there, not in `ht`** (not cloned, not translated here) |
| Size | 25 modules, 22 756 lines in `ht/ht/`; 272 public module-level functions |
| Tests / CI | one `tests/test_<module>.py` per module (5 912 lines, doctests + regression values) and GitHub Actions CI; the docstrings carry the formula, the validity range, the original reference and a doctest value for most correlations |

## 1. License and attribution

MIT is permissive: the maintainer decision used for TESPy (`sources/tespy/README.md` §1) applies here too —
**translations are published under the library license with full credit** (decision D3). Every function must
carry a **dual citation**: the **original paper/book** of the correlation *and* the `ht` module + function it was
taken from (see §7).

* No `CITATION.cff`; the citation text is in `README.rst` §"To cite ht in publications".
* **Third-party material**: the correlations are transcriptions of published papers (Incropera, Perry's, VDI Heat
  Atlas, HEDH, TEMA, GPSA, ESDU, ASME/AIChE/Int. J. Heat Mass Transfer articles) — the original authors must be
  named in the comment block of each function, as the roadmap rule requires. Some curves were digitised from
  graphs by the author (see §4, "table-lookup" features); the data file itself is never copied into the library
  (tables are recreated as CoolSolve lookup tables when a card needs them).

**Credit block to reuse in the README of a translated family file**:

```text
This CoolSolve model is a translation (EES-compatible language) of the correlations of
ht, the heat-transfer component of ChEDL, file <ht/ht/module.py>, functions <names>,
version 1.2.0, commit 85e0ee6 (2025-12-07).
ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell", MIT License.
Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer component of
Chemical Engineering Design Library (ChEDL), https://github.com/CalebBell/ht.
Changes: translated from Python to CoolSolve; <specific changes>.
Scientific basis (per function): <original paper or book, from the ht docstring>.
```

## 2. What the repository contains

* **Internal convection** `conv_internal.py` (laminar, thermal entry region, 23 turbulent, curved/helical,
  rectangular duct), **external forced convection** `conv_external.py` (single cylinder, flat plate).
* **Free convection** `conv_free_immersed.py` (plates, sphere, vertical/horizontal cylinders, coils),
  `conv_free_enclosed.py` (parallel plates, vertical plates, critical Rayleigh numbers), `conv_jacket.py`.
* **Boiling** `boiling_nucleic.py` (nucleate + critical heat flux), `boiling_flow.py` (flow/film boiling),
  `boiling_plate.py` (plate boiling); **condensation** `condensation.py`; **two-phase non-boiling**
  `conv_two_phase.py`.
* **Other geometries** `conv_plate.py` (plate HX), `conv_tube_bank.py` (tube banks + shell-side dP +
  Bell-Delaware), `conv_packed_bed.py`, `conv_supercritical.py` (near-supercritical internal).
* **Heat exchangers** `hx.py` (eps-NTU, P-NTU/TEMA, LMTD F, TEMA sizing), **air coolers** `air_cooler.py`
  (finned-bundle air side, dP, noise, Ft), **conduction** `conduction.py`, **insulation** `insulation.py`
  (material tables), **radiation** `radiation.py`, `core.py` (LMTD, wall factors, fin efficiency),
  `units.py` (deprecated aliases).
* **Infrastructure, not translated**: `numba.py`, `numba_vectorized.py`, `vectorized.py`, `__init__.py`.

## 3. Sweep method

1. Listed every public module-level function of `ht/ht/*.py` with the Python AST (272 functions).
2. Read the docstring of each one: formula (LaTeX `.. math::`), validity range, original reference and the
   doctest example value (`>>>`), and extracted the reference list with a regular expression to fill the `notes`
   cell of the inventory row.
3. Classified each function as *correlation to translate* / *selector (dispatcher, not translated)* /
   *table lookup (needs data files)* / *private solver helper*, then grouped the correlations into families of the
   same physical process (one future `.eescode` file each, target 5–20 functions).
4. Cross-checked the families against the existing library (`library.csv`, `functions.csv`) and the other
   inventories (`sources/labothappy`, `sources/thermocycle` THC-004/005/011, `sources/tespy`): overlaps are
   written in the `notes` cell of the row.
5. Did **not** run the Python code (no virtualenv needed for a triage card); verification values for the future
   cards are the **doctests in the docstrings** and the `tests/test_<module>.py` regression values (both listed in
   `companion_files` of each row). `n_lines` is the number of physical lines of the module(s) of the family
   (sum when several modules).

## 4. Counts per module

| Module | Lines | Public functions | To translate | Selectors | Excluded |
|---|---:|---:|---:|---:|---:|
| `ht/air_cooler.py` | 1059 | 9 | 9 | 0 | 0 |
| `ht/boiling_flow.py` | 945 | 9 | 8 | 0 | 1 |
| `ht/boiling_nucleic.py` | 1413 | 16 | 12 | 4 | 0 |
| `ht/boiling_plate.py` | 577 | 5 | 5 | 0 | 0 |
| `ht/condensation.py` | 442 | 6 | 6 | 0 | 0 |
| `ht/conduction.py` | 690 | 14 | 14 | 0 | 0 |
| `ht/conv_external.py` | 952 | 16 | 12 | 4 | 0 |
| `ht/conv_free_enclosed.py` | 649 | 9 | 9 | 0 | 0 |
| `ht/conv_free_immersed.py` | 1676 | 27 | 19 | 8 | 0 |
| `ht/conv_internal.py` | 1907 | 35 | 33 | 2 | 0 |
| `ht/conv_jacket.py` | 357 | 2 | 2 | 0 | 0 |
| `ht/conv_packed_bed.py` | 243 | 4 | 4 | 0 | 0 |
| `ht/conv_plate.py` | 360 | 4 | 4 | 0 | 0 |
| `ht/conv_supercritical.py` | 1430 | 18 | 18 | 0 | 0 |
| `ht/conv_tube_bank.py` | 1553 | 14 | 14 | 0 | 0 |
| `ht/conv_two_phase.py` | 960 | 11 | 9 | 2 | 0 |
| `ht/core.py` | 590 | 8 | 4 | 1 | 3 |
| `ht/hx.py` | 5447 | 49 | 37 | 2 | 10 |
| `ht/insulation.py` | 786 | 7 | 0 | 0 | 7 |
| `ht/radiation.py` | 271 | 4 | 3 | 0 | 1 |
| `ht/units.py` | 84 | 3 | 0 | 0 | 3 |
| `ht/__init__.py`, `numba*.py`, `vectorized.py` | 365 | 1 | 0 | 0 | 2 |
| **Total** | **22 756** | **272** | **222** | **23** | **27** |

## 5. Families (one future `.eescode` file each)

`priority` = order of the proposed cards (wave1 first). Functions are listed in the `description` cell of the
inventory row; the numbers here are the count of translated `FUNCTION`s.

| ID | Priority | Folder | File name | Functions | Content |
|---|---|---|---|---:|---|
| HT-001 | wave1 | `heat_transfer/convection` | `internal_turbulent_nusselt` | 23 | turbulent and turbulent-entry internal Nu (Dittus-Boelter … Bhatti-Shah, Gnielinski) |
| HT-002 | wave1 | `heat_transfer/convection` | `nucleate_boiling_and_chf` | 12 | pool nucleate boiling heat flux (9) + critical heat flux (Zuber, Serth-HEDH, HEDH-Montinsky) |
| HT-003 | wave1 | `heat_transfer/convection` | `condensation_film` | 6 | film condensation: Nusselt plate, Boyko-Kruzhilin, Akers-Deans-Crosser, kinetic correction, Cavallini, Shah |
| HT-004 | wave1 | `components/heat_exchangers` | `hx_effectiveness_ntu` | 8 | Cmin/Cmax/Cr, NTU↔UA, eps(NTU, Cr) and NTU(eps, Cr) for counterflow, parallel, crossflow, boiler/condenser |
| HT-005 | high | `heat_transfer/convection` | `internal_laminar_and_curved_nu` | 10 | laminar (T_wall and q_wall), thermal entry region, rectangular duct, spiral/helical curved ducts |
| HT-006 | high | `heat_transfer/convection` | `free_conv_cylinders` | 13 | 10 vertical-cylinder + 3 horizontal-cylinder free-convection correlations |
| HT-007 | high | `heat_transfer/convection` | `free_conv_plates_and_sphere` | 5 | Churchill-Chu vertical plate, McAdams/VDI/Rohsenow horizontal plate, Churchill sphere |
| HT-008 | high | `heat_transfer/convection` | `external_crossflow_cylinder` | 8 | single-cylinder crossflow (Zukauskas … Whitaker, Perkins-Leppert) |
| HT-009 | high | `heat_transfer/convection` | `tube_bank_nusselt` | 7 | tube-bank Nu and row/angle correction factors (Grimison, Zukauskas, ESDU 73031, HEDH) |
| HT-010 | high | `components/heat_exchangers` | `plate_hx_heat_transfer` | 9 | plate HX single-phase Nu (Kumar, Martin, Muley-Manglik, Khan-Khan) + 5 plate two-phase boiling correlations |
| HT-011 | high | `heat_transfer/convection` | `two_phase_nonboiling_in_tube` | 9 | in-tube two-phase non-boiling HTC (Groothuis-Hendal, Martin-Sims, Hughmark, Aggour …) |
| HT-012 | high | `heat_transfer/convection` | `flow_boiling_in_tubes` | 8 | flow and film boiling in tubes (Lazarek-Black, Li-Wu, Thome, Chen, Liu-Winterton …) |
| HT-013 | high | `heat_transfer/convection` | `air_cooler_air_side` | 8 | finned-bundle air-side HTC and dP (Briggs-Young, ESDU low/high fin, Ganguli-VDI) + 2 air-cooler noise correlations |
| HT-014 | medium | `heat_transfer/convection` | `free_conv_enclosed_and_jackets` | 12 | enclosed plates, critical Rayleigh numbers, helical coils in tanks, vessel jackets |
| HT-015 | medium | `heat_transfer/convection` | `external_forced_conv_plates` | 4 | laminar/turbulent forced convection over a flat plate |
| HT-016 | medium | `components/heat_exchangers` | `hx_temperature_effectiveness_pntu` | 15 | P-NTU temperature effectiveness: TEMA E/G/H/J, plate, air cooler + the inverse NTU(P) relations |
| HT-017 | medium | `heat_transfer/pressure_drop` | `tube_bank_dp_bell_delaware` | 7 | shell-side dP (Kern, Zukauskas) + Bell-Delaware Jc, Jl, Jb, Js, Jr |
| HT-018 | medium | `heat_transfer/convection` | `supercritical_internal_nu` | 18 | near-supercritical internal convection (McAdams, Jackson, Swenson, Kitoh, Petukhov …) |
| HT-019 | medium | `components/heat_exchangers` | `lmtd_and_f_correction` | 3 | LMTD, Fakheri F correction, air-cooler Ft |
| HT-020 | medium | `heat_transfer/conduction` | `conduction_resistances_and_shapes` | 14 | cylindrical/plane-wall resistance, 6 shape factors, R-value conversions |
| HT-021 | medium | `heat_transfer/radiation` | `radiation_heat_flux` | 3 | blackbody spectral radiance, radiant heat flux with back-radiation, grey transmittance |
| HT-022 | low | `heat_transfer/convection` | `packed_bed_nusselt` | 4 | packed-bed forced convection |
| HT-023 | low | `heat_transfer/convection` | `fin_efficiency_and_wall_factors` | 3 | circular-fin efficiency, wall correction factors for Nu and for frictional dP |
| HT-024 | low | `components/heat_exchangers` | `shell_and_tube_sizing` | 13 | tube counts, bundle diameters, TEMA clearances, baffle thickness, unsupported length |

Five families are below the 5–20 target (HT-015, HT-019, HT-021, HT-022, HT-023: 4, 3, 3, 4, 3 functions): they
were kept separate to preserve the physics grouping; the card text says that the executor may merge them into a
neighbouring file.

## 6. Exclusions and why

* **Selectors / dispatchers (23, not translated)** — they only choose a method name and call one of the
  correlations of their family, which an EES caller does directly: `Nu_conv_internal(_methods)`,
  `Nu_external_cylinder(_methods)`, `Nu_external_horizontal_plate(_methods)`, `Nu_free_vertical_plate(_methods)`,
  `Nu_free_horizontal_plate(_methods)`, `Nu_vertical_cylinder(_methods)`, `Nu_horizontal_cylinder(_methods)`,
  `h_nucleic(_methods)`, `h_two_phase(_methods)`, `qmax_boiling(_methods)`, `effectiveness_NTU_method`,
  `P_NTU_method`, `wall_factor`. Each is named in the `notes` of its family row.
* **Input-consistency checks (3, not translated)** — return a Boolean, they are not correlations:
  `countercurrent_hx_temperature_check`, `is_heating_temperature`, `is_heating_property` (`core.py`).
* **Table lookups needing data files (11, not translated)** — `insulation.py` in full (`ASHRAE_k`, `k_material`,
  `rho_material`, `Cp_material`, `nearest_material`, `refractory_VDI_k`, `refractory_VDI_Cp`: ASHRAE handbook and
  VDI refractory tables), `radiation.solar_spectrum` (1.4 MB `ht/data/solar_iss_2018_spectrum.dat`),
  `hx.get_tube_TEMA` (BWG wall-gauge table), `hx.Ntubes_Phadkeb` and `hx.DBundle_for_Ntubes_Phadkeb`
  (four binary `.npy` coefficient tables in `ht/data/`). A future card *could* ship the tables as CoolSolve
  lookup tables (EES convention `<name>-<table>.csv`), but the value is low for this library.
* **Iteration / solver helpers (8, replaced by simultaneous equations)** — `_NTU_from_P_solver`,
  `_NTU_from_P_objective`, `_NTU_from_P_erf`, `_NTU_max_for_P_solver` (secant/bisection of the inverse P-NTU
  method; the NTU becomes an unknown), `to_solve_q_Thome` (inner solve for the film-boiling heat flux; q becomes
  an unknown), `to_solve_Ntubes_Phadkeb`, `_tubecount_objf_Perry`, `_load_coeffs_Phadkeb`.
* **Duplicates / aliases (3)** — `units.py` re-exports `R_to_k`, `R_value_to_k`, `k_to_R_value` from
  `conduction.py` as deprecated aliases: translate once (in HT-020).
* **Infrastructure (2)** — `transform_complete_ht` (numba) and `__init__.py`.
* **Pressure drop: mostly in `fluids`, not here.** `ht` contains **no friction factor and no pipe/two-phase
  pressure-drop correlation**: pipe dP, acceleration and gravity terms, the two-phase multipliers and the
  dimensionless-number helpers (`Prandtl`, `Reynolds`, `Boiling`, `Bond`, `Weber`,
  `Lockhart_Martinelli_Xtt`, `friction_factor`) are in `fluids` (`fluids.friction`, `fluids.two_phase_voidage`,
  `fluids.core`). `ht` only ships the **shell-side/tube-bank** dP (Kern, Zukauskas — HT-017) and the **air-side
  finned-bundle** dP (ESDU high/low fin — HT-013). Those are already covered by LTP-028/TSP-028 (`valves_nozzles_piping`)
  and CSL-0018 (Colebrook), so no new card is proposed for pipe dP.

## 7. Translation rules for the future cards (T-FUNC, workflow §4)

1. One `FUNCTION` per correlation, named after the `ht` function (e.g. `Nu_Gnielinski`, `Shah`), SI arguments
   (K, Pa, kg/s, W, m), formula and validity range in the comment block.
2. **Dual citation in every function**: the original paper/book (from the ht docstring, §4 of the row `notes`) and
   `ht`, module + function, version 1.2.0, commit `85e0ee6`, MIT — plus the credit block of §1 in the README and in
   `model.json` `origin`.
3. The file holds all its functions **and** a short main program calling each of them with realistic inputs (one
   call per function) so the file solves and gets a `.sol` baseline.
4. **Verification**: reproduce the ht doctest values and, for a few input sets per function, the values of the
   Python function (throw-away virtualenv with the local clone under `work/`); tabulate CoolSolve vs ht in the
   README (model status `verified`). The doctests of the family are listed in `companion_files`.
5. Selectors are not translated; non-smooth regime switches use an EES `IF`; property arguments (`Re`, `Pr`,
   `x`, `g`, …) are plain arguments, not CoolProp calls inside the functions, unless a card deliberately needs
   them (the calling model then passes them).
6. **Three constructs to check in CoolSolve before translating** (no gap is registered yet, see §9):
   the modified Bessel functions (`iv`, `i0`, `i1`, `k0`, `k1`) needed by the crossflow branches of
   `effectiveness_from_NTU` / `NTU_from_effectiveness` (HT-004) and by the P-NTU crossflow term (HT-016);
   the error function used by `Nu_Nusselt_Rayleigh_Holling_Herwig_err` (HT-014); and `LOOKUP`/`INTERPOLATE`
   inside a `FUNCTION` body for the digitised curves of HT-009/HT-017 (`CS-GAP-LOOKUP-PROC` is registered).
7. **Table curves** (`features` contains `table-lookup`): either ship the digitised points as a CoolSolve lookup
   table in the model folder or use the plain polynomial form that `ht` offers as an alternative (e.g. the
   Chebyshev fit of the Bell-Delaware factors) — log the choice in the README.

## 8. Overlaps with the library and the other inventories

* **Library (`library.csv`, 78 models; the 19 `FUNCTION`/`PROCEDURE` rows of `functions.csv` come from 11 models
  and are property routines such as `cpbar` and `BRINEPROP`)**: the only models of kind `function` are
  `cpbar_combustion_products` (CSL-0005) and `brineprop_secondary_refrigerants` (CSL-0079) — **no heat-transfer
  or pressure-drop correlation function exists**, so all 24 families are new. Correlation *models* that would use
  them: CSL-0008/CSL-0077 (air-cooled condenser → HT-009/HT-013), CSL-0002/CSL-0026/CSL-0027 (eps-NTU → HT-004),
  CSL-0027/CSL-0031 (condenser/evaporator → HT-003/HT-011), CSL-0038/TSP-042 (sCO2 → HT-018), CSL-0018 (pipe dP,
  `fluids`, untouched).
* **LaboThapPy**: LTP-034 (in-tube HTC incl. Thome condensation/flow boiling), LTP-035 (plate HTC), LTP-038 (external
  tube banks, HTC + dP, film condensation and boiling on tubes), LTP-037 (shell-side HTC, Kern/Bell-Delaware),
  LTP-030 (shell-side dP), LTP-039/LTP-032 (finned-tube air-side HTC and dP), LTP-033 (void fractions), LTP-042
  (eps-NTU + F-LMTD), LTP-014 (eps-NTU with geometry), LTP-069/LTP-070 (shell-and-tube sizing), LTP-028 (pipe dP,
  `fluids`-like, untouched). The `ht` families are **more complete** in each case: keep both,
  the `ht` version is the reference for the correlations and the LaboThapPy block for the component integration.
* **ThermoCycle**: **THC-004** (flow and nucleate boiling HTC, Shah 1979) overlaps HT-002 and HT-012 (ht is more
  complete and adds the CHF); **THC-005** (in-cylinder HTC) is a different physical case (combustion), not in
  `ht`; **THC-011** (single-phase and plate correlations, Martin 2012) overlaps HT-010.
* **TESPy**: TSP-030 (eps-NTU relations, cross-validated against `ht` by the TESPy test suite), TSP-012 (NTU HX),
  TSP-029 (smoothed LMTD), TSP-009 (condenser) overlap HT-004, HT-019, HT-003; TSP-028 (Darcy friction) is
  `fluids`-like and untouched.

## 9. Decisions and open questions taken by this card

* **Decisions taken** (documented here because this card has no model README): (1) one family = one future file,
  grouped by physical process, keeping small families separate (4 families below 5 functions, merge optional);
  (2) selectors, Boolean checks, table lookups and iteration helpers are excluded, with the reason in the row
  `notes`; (3) pipe/friction/two-phase dP is **out of scope** (it belongs to `fluids`); (4) `level_guess = 2`
  for every row (a function library with a demonstration main program: explicit equations plus procedures); (5)
  `category_guess` uses the taxonomy mapping of `docs/taxonomy.md` §1 (`heat_transfer/*` for correlations,
  `components/heat_exchangers` for exchanger relations and sizing).
* **Open questions for the first `T-FUNC` card** (no evidence gathered here, so nothing is registered in the
  CoolSolve gap register): can CoolSolve evaluate the modified Bessel functions (`i0`, `i1`, `iv`, `k0`, `k1`) and
  the error function? If not, the crossflow branch of the eps-NTU relations (HT-004/HT-016) needs either a
  truncated series (as `ht` offers) or becomes a documented gap. `CS-GAP-LOOKUP-PROC` already covers a lookup
  table read inside a `FUNCTION`.
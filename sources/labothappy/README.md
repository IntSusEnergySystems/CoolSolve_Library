# LaboThapPy - source sweep for the CoolSolve_Library

Quick sweep (not an audit) of the ULiege Thermodynamics Laboratory Python library, done to build a backlog of models that can be translated into the EES-compatible CoolSolve language. The machine-readable backlog is [`inventory.csv`](inventory.csv) (74 rows, `LTP-001` ... `LTP-074`).

| | |
|---|---|
| Repository | https://github.com/PyLaboThap/LaboThapPy (local snapshot `~/git/LaboThapPy`, commit `f03f7f47`, 2026-09-25; 744 commits since 2024-08) |
| Documentation | https://labothappy.readthedocs.io (Sphinx; `docs/source`) |
| Version | 0.1.0 (`pyproject.toml`, `setup.py`) |
| Language / stack | Python, CoolProp `AbstractState`, NumPy/SciPy (`fsolve`, `brentq`, `root`), pyswarms (PSO) |
| Size | 245 `.py` files, ~66 k lines: `component` 77 files/18.8 k (incl. 30 example scripts), `correlations` 48/14.2 k, `sizing` 49/18.7 k, `machine` 27/8.3 k, `toolbox` 38/4.8 k, `connector` 5/1.2 k |
| Tests / CI | none (example scripts only, one `test_connectors.py`); 3 docs notebooks, 4 PDF model descriptions |

## 1. License and attribution

> **Maintainer decision (2026-10-04):** the license is not an issue — both declared licenses
> (Apache-2.0 and MIT) are permissive and allow the translation into the CoolSolve language;
> translated models are published under the library license. What matters is **proper credit**
> to the authors of the original model (block below), in the README and `model.json` of each model.

* **Code: Apache License 2.0** - `LICENSE.txt` (full text) and `NOTICE.txt`: "Copyright (C) 2025 Universite catholique de Louvain (UCLouvain), Universite de Liege (ULiege), Universite de Mons (UMONS)"; contributors in `AUTHORS.txt`. NOTICE also states that the *documentation* is **CC BY-SA 4.0** (share-alike: do not paste documentation text/figures/PDFs into model READMEs - write original descriptions and cite).
* **Declared licenses differ** (`pyproject.toml`, `setup.py`, `PKG-INFO`: MIT; `LICENSE.txt`/`NOTICE.txt`: Apache-2.0); both are permissive, so this does not affect the translations (maintainer decision above). No SPDX headers in the source files.
* **Authors** (AUTHORS.txt): Basile Chaudoir, Elise Neven, Alanis Zeoli, Titouan Janod, Samuel Gendebien, Marie Peeters, Andres Hernandez (ULiege), Matteo Hauglustaine (UCLouvain/UMONS); guidance from Prof. V. Lemort, F. Contino, W. De Paepe. The README names Elise Neven and Basile Chaudoir as initial developers; git history: Elise Neven (337 commits), Basile Chaudoir (~280).
* **How to cite:** no `CITATION.cff`, DOI or paper in the repo. Cite the repository + docs, plus the scientific source of each model (listed in the inventory `notes`/`description`).
* **Third-party provenance to clear before copying** (file headers mention them; licence of the originals unknown): `correlations/heat_pipe/HP_h_coeffs.py` and `pipe_htc.py:pool_boiling` ("Van Long Le - Heat Pipe Code"), `find_2P_boundaries.py` (R. Dickes), `f_lmtd2.py` (J. Vega), `STHE_cost_estimation.py` (Caputo et al.), manufacturer data embedded in code (Soponova MicroCSP collector map, SWEP plate-HX geometries, pump/circulator curves).

**Credit block to reuse in the README of a translated model** (name the original authors, the library, the file and commit, the changes, and the scientific source):

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
<component/correlation name> from LaboThapPy, file <path>, commit f03f7f47.
LaboThapPy - https://github.com/PyLaboThap/LaboThapPy
Copyright (C) 2025 Universite catholique de Louvain (UCLouvain), Universite de Liege (ULiege),
Universite de Mons (UMONS). Original authors: E. Neven, B. Chaudoir et al. (see AUTHORS.txt).
Changes: translated from Python to CoolSolve; iterative Python solvers replaced by simultaneous
equations; <other changes>. Scientific basis: <original reference, e.g. Lemort 2008 thesis>.
```

## 2. What the repository contains

* `component/` - steady-state component classes (one class per model, `get_required_inputs/parameters`, `solve()`): compressors (const-eta, Lemort semi-empirical, radial mean-line), expanders (const-eta, Lemort semi-empirical, ejector, axial mean-line Aungier), pumps (const-eta, curve+similarity), valve, heat exchangers (const-eff, const-eff discretised, const-pinch, eps-NTU, finite-volume fin-tube, charge-sensitive moving boundary for plate/shell&tube/tube-fin/PCHE, thermosyphon), pipes/elbows, tanks (mixer, splitter, LV separator, drum/oil separators), storage (latent PCM, isothermal tank), parabolic-trough collector, plus `examples/` and `templates/`.
* `correlations/` - function libraries: in-tube/plate/shell&tube/tube-bank/fin/PCHE HTC, single- and two-phase pressure drop, 13 void-fraction models, HX relations (eps-NTU, LMTD F), turbomachinery loss models, PT heat-loss correlation, R1233zd(E) conductivity, pseudo-critical properties, cost correlations.
* `machine/` - sequential-modular circuit solvers (`base_circuit`, `CircuitFPI`: successive substitution/Wegstein/fsolve/..., `IterativeCircuit`), cycle examples (heat pumps, ORC, transcritical CO2 cycles), PSO optimisation scripts.
* `sizing/` - 0D (Cordier), mean-line 1D/3D turbomachinery design, PSO-based S&T/PCHE sizing, legacy plate-HX scripts, storage vessel design.
* `toolbox/`, `connector/` - geometry databases, plots, CPI/FX data, `MassConnector`/`WorkConnector`/`HeatConnector`/`HAConnector`.

**Skipped as infrastructure (not in the CSV):** connectors, `BaseComponent`, circuit solvers, templates, plotting, `zero_brent`, `step_smoother`, economic data tables, blade-geometry (Bezier) code, `humid_air_connector` (no humid-air component exists yet; docs page is empty).

## 3. Inventory statistics (`inventory.csv`)

74 rows: 35 steady models/cycles, 28 `function` families, 10 `optimization`, 1 `dynamic`. Levels: L1 16, L2 26, L3 17, L4 15. Translation difficulty (first token of `notes`): easy 29, easy-medium 4, medium 20, hard 15, infeasible 6. Priorities: `wave1` 9, `high` 8, `medium` 17, `low` 26, `skip` 14. Category with most rows: heat_exchangers (23). `n_lines` = physical lines of the main file (`wc -l`); `n_equations` is only filled for trivial blocks.

Reference results are **scarce**: no unit tests; (i) docs notebook for the const-eta compressor (reproduced here with CoolProp 7.2: R1233zd(E) 3.193 bar/331.03 K -> 6.062 bar, eta 0.8 gives T_ex = 354.293 K, dh = 15 357.5 J/kg - compare dh, the absolute enthalpy depends on the CoolProp reference state), (ii) TESPy's test-suite cross-validates its NTU exchanger against LaboThapPy's `HexeNTU` (water/water counterflow, UA = 132.069586 W/K: Q = 3961.9 W, T_h,out = 295.54 K, T_c,out = 296.98 K), (iii) calibrated parameter sets in the examples (Lemort-type machines, PT collector). For anything else, generate references by running the original Python examples or compare with the existing CoolSolve/EES versions.

## 4. Recommended translation candidates (top 15)

| # | ID | Candidate | Why | Difficulty | Reference data |
|---|---|---|---|---|---|
| 1 | LTP-013 | Constant-pinch evaporator/condenser (`hex_cstpinch`) | core ORC/heat-pump design block (3 zones, pinch, superheat/subcooling); not in CoolSolve examples | medium (P_sat as unknown, pinch-location logic) | pinch spec is an exact self-check |
| 2 | LTP-011 | Constant-effectiveness HX with enthalpy-based Q_max (`hex_csteff`) | IHX/recuperator building block, trivial | easy | self-checks |
| 3 | LTP-014 + LTP-042 | eps-NTU HX with plate geometry/Gnielinski + eps-NTU/F-LMTD relations | general HX FUNCTION set | easy | TESPy cross-validation case (Q = 3961.9 W) |
| 4 | LTP-020 + LTP-050 | Parabolic-trough collector, discretised (DUPLICATE) + Dickes-Lemort-Quoilin heat-loss correlation | solar gap; author-side expertise for cross-check | easy | efficiency map + 10 coefficients in repo; original model by S. Quoilin |
| 5 | LTP-028 | Pipe pressure drop: 6 friction factors + Friedel/MSH/Choi two-phase, acceleration, gravity | reusable FUNCTIONs; two-phase dP missing in CoolSolve | easy | literature values |
| 6 | LTP-033 | 13 void-fraction correlations | reusable FUNCTIONs for charge/ORC models | easy | literature/ACHP |
| 7 | LTP-055 | Heat pump (const-eta compressor, pinch HX, valve, + IHX) | integration test of items 1-2, Zorlu data | easy-medium | compare with CoolSolve zorlu_heat_pump / refrigeration examples |
| 8 | LTP-056 | Recuperated + preheated ORC (cyclopentane) | pinch-based ORC design; *beware: preheater source bug in the example main* | easy-medium | none stored |
| 9 | LTP-009 | Pump: manufacturer curves + affinity laws (P_N/P_M/M_N modes) | lookup tables; modes become a choice of knowns | medium | PDF derivation, real curve data |
| 10 | LTP-002 | Semi-empirical compressor (Lemort) | canonical; already an implicit system; m_dot mode and R1233zd(E) parameter set | medium | partial; overlaps `scroll_compressor.eescode` |
| 11 | LTP-005 | Semi-empirical expander (Lemort), 3 modes | idem | medium | partial; overlaps `expander_module.eescode` |
| 12 | LTP-012 | Discretised constant-effectiveness HX with minimum pinch (sCO2 recuperators) | pinch-limited real-fluid profiles | medium (while-loop -> pinch constraint) | none stored |
| 13 | LTP-034 | In-tube HTC family (Gnielinski ... Thome, Steiner-Taborek, Gungor-Winterton, sCO2) | FUNCTION library | medium | none |
| 14 | LTP-035 | Plate-HX HTC family (Martin, Han, Amalfi, Shah ...) | FUNCTION library, ORC/HP evaporators and condensers | easy-medium | none |
| 15 | LTP-048 | R1233zd(E) thermal conductivity (Perkins & Huber) | CoolProp has no conductivity model for the fluid (verified, v7.2.0) | easy | published coefficients |

Not recommended now: mean-line turbomachinery, PSO sizing/optimisation scripts, ejector (broken import), thermosyphon, 3000-line moving-boundary class (translate a fixed-topology plate evaporator later), oil/drum separators.

## 5. Translation guidelines specific to LaboThapPy

1. **Python solvers become equations.** Most components solve a *small implicit system* with `scipy.optimize.fsolve` inside nested multi-start loops (semi-empirical compressor/expander) or a scalar `brentq` (const-pinch, moving boundary, pump `P_M`). In CoolSolve write all internal residuals as ordinary equations, make the root-finding variable (T_wall, m_dot, h_ex2, P_ex2, P_sat, Q, N_rot ...) an unknown, delete the retry loops and move the retry guesses (e.g. T_w = 0.7-0.95*T, filling factor 0.7-1.3) into an `.initials` file with bounds.
2. **Circuits:** `CircuitFPI`/`IterativeCircuit` (guesses, "iteration variables", `Link` objectives, Wegstein) only exist because the model is sequential-modular. In CoolSolve connect state points directly (`p_ex_exp = p_su_cond`, `h_su_valve = h_ex_cond`); the iteration variables are simply unknown pressures closed by the pinch/subcooling equations.
3. **Modes** (`mode='N_rot'|'m_dot'`, `'P_N'|'P_M'|'M_N'`) only select which variables are known: provide one file with the three alternatives commented, not three models.
4. **Branching and clamps:** `max/min/abs` in the models (leakage velocity <= 300 m/s, `max(0,.)` zone heat, `min` over pinch candidates) are non-smooth; keep them only where physically needed, otherwise fix the regime or use smooth approximations (check solver behaviour with the `.initials`).
5. **Discretisation:** loops with `n_disc` (PT collector, `hex_csteff_disc`, fin-tube cells) -> `DUPLICATE i=1,N` with array variables; N is fixed at parse time.
6. **Interpolation:** `interp1d`, `RectBivariateSpline` (pump curves, PT efficiency map, Cordier line, void-fraction/HTC tables) -> CoolSolve lookup tables (1D/2D) or fitted polynomials; remember linear *extrapolation* in `interp1d(fill_value='extrapolate')`.
7. **Units/conventions:** SI everywhere (Pa, K, J/kg, kg/s); exceptions: `N_rot` in rpm, pump curves in m3/h and head in m, angles in rad in Python (CoolSolve trigonometric functions take degrees), `T_amb`/`T_su` in K, fouling factor in m2K/W. Fluid names are CoolProp names (`R1233zd(E)`, `Cyclopentane`, `CO2`); note `R1233ZDE` alias in some examples.
8. **Property gaps:** R1233zd(E) conductivity must come from `correlations/properties/thermal_conductivity.py`; `rho(s,h)`-type inversions (`DmassSmass_INPUTS`) used by the semi-empirical compressor need an equivalent property call or an extra unknown.
9. **Check before trusting a file:** broken imports (`ejector_csteff.py`, legacy `sizing/.../PHX_*_ORC.py` need a missing `BaseClases` package), copy-pasted docstrings (radial compressor, storage components, `tank_isothermal`), case-variant duplicate files (`FPI_*`/`fpi_*`, `Examples`/`examples`), the Zorlu ORC example feeding cold-source values to the preheater, `hex_eNTU.rst` writing 1/AU as a product, `e_NTU.py` counterflow singular at Cr = 1.

## 6. Overlaps and gaps

* **Already in CoolSolve examples (marginal value = cross-validation):** semi-empirical scroll compressor (`scroll_compressor`), expander (`expander_module`), Zorlu heat pump with PCM storage (`zorlu_heat_pump`), ORC/refrigeration/Rankine cycles, eps-NTU exchangers (`exchangers1-3`), three-zone condenser (`condenser_3zones`), Colebrook pressure drop (`pressuredrop`), CO2 ORC (`orc_co2`).
* **Gaps this library fills versus a classic EES teaching collection:** pinch-point design components for phase-changing HX; two-phase pressure-drop and void-fraction correlation families; plate/shell&tube/PCHE/fin-tube HTC sets and Bell-Delaware; sCO2 HTC correlations; pump curves with similarity laws; parabolic-trough semi-empirical collector; moving-boundary HX with refrigerant charge; transcritical/recompression CO2 cycle architectures; turbomachinery meanline loss models and Cordier sizing; heat-pipe/thermosyphon HX; cost correlations.
* **Not translatable without an optimiser:** everything under `machine/optimization` and `sizing/*PSO*`; use parametric studies of the underlying models instead.

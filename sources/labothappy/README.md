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

## 2026-10-24 triage

Card C-352 (T-PLAN, novelty triage of the 13 remaining `todo` rows with priority
wave1/high/medium against library.json, 282 models): 4 kept `todo` (translation
cards C-360...C-366 in roadmap.md §6), 7 `merged`, 2 `duplicate` (both of
inventory rows kept `todo`), 0 `discarded`.

| ID | Decision | Target / nearest model | Reason |
|---|---|---|---|
| LTP-015 | merged | CSL-0115 | discretised finite-volume evaporator already translated; fin-tube air-side HTC/DP correlations already in CSL-0099 and CSL-0109 |
| LTP-016 | merged | CSL-0138 | moving-boundary HX (Bell 2015) already translated; the charge-sensitive geometry version (3000-line class) is not recommended now, variant note only |
| LTP-018 | merged | CSL-0130 | single/two-phase pipe friction families already translated; refrigerant charge is trivial post-processing on the CSL-0131 void fraction |
| LTP-019 | duplicate | LTP-029 | same Idelchik elbow coefficients; the function-family row LTP-029 is kept for the T-FUNC card C-364 |
| LTP-021 | merged | CSL-0041 | latent/isothermal phase-change storage with HX already translated (ice-tank discharge; PCM storage in a HP: CSL-0039); the constant-pinch coupling would be a variant |
| LTP-029 | todo | none (new function family) | Idelchik local-loss coefficients for bends (single/two-phase) absent from the library (card C-364) |
| LTP-031 | merged | CSL-0111 | chevron plate HX pressure-drop correlations already in CSL-0111 (incl. Han-Lee-Kim two-phase) and CSL-0124; Han et al. chevron DP is the same family |
| LTP-049 | todo | none (new function family) | pseudo-critical temperature / pseudo-boiling bounds absent from the library (sCO2 utility, e.g. for CSL-0144) (card C-365) |
| LTP-053 | todo | none (new function family) | Cordier specific-speed line and 0D efficiency estimation absent from the library (card C-366) |
| LTP-057 | todo | nearest: CSL-0134 / CSL-0153 (design-point ORCs) | off-design ORC with semi-empirical scroll expander + moving-boundary plate HX absent from the library (card C-360) |
| LTP-058 | merged | CSL-0144 | sCO2 recompression Brayton already translated (Penkuhn & Tsatsaronis reference); the basic/recuperated architectures are simpler subsets |
| LTP-059 | merged | CSL-0145 | transcritical CO2 cycle physics already translated (booster: receiver, flash-gas by-pass, gas cooler); expander/IHX architectures would be variants there |
| LTP-065 | duplicate | LTP-053 | same Cordier/specific-speed physics in a sizing script; the correlations row LTP-053 is kept |

## 2026-10-31 triage (C-373)

Card C-373 (T-PLAN, novelty triage of the 26 remaining `todo` rows with priority
low/medium; LTP-057 excluded - card C-360 in progress - against library.json,
291 models): 6 kept `todo` (cards C-441, C-442, C-446, C-447, C-448, C-449),
5 `merged`, 8 `duplicate` (4 of them of inventory rows kept `todo`),
7 `discarded`.

| ID | Decision | Target / nearest model | Reason |
|---|---|---|---|
| LTP-003 | duplicate | LTP-052 | same radial loss models; the component adds the mean-line station assembly and has no reference data |
| LTP-007 | duplicate | LTP-051 | the Aungier loss correlations are the physics; the component adds map interpolation and PSO infrastructure |
| LTP-022 | discarded | nearest: CSL-0009 | unfinished sketch (undefined attributes; min(0,.) in discharge; copy-pasted docstring) |
| LTP-023 | discarded | CSL-0247 / CSL-0193 | textbook mixing balance present in every cycle model and as exercises |
| LTP-024 | discarded | cycle splitter blocks (CSL-0144) | fixed-fraction split with unchanged state; no physics beyond a mass balance |
| LTP-025 | discarded | CSL-0145 / CSL-0313 | saturated split already inside the booster (receiver/flash gas) and the flooded-evaporator drum |
| LTP-026 | discarded | none | droplet-separation equipment sizing, not thermodynamics; empty docstrings; plotting-heavy |
| LTP-030 | merged | CSL-0103 | Kern + Bell-Delaware shell-side DP already translated; only the Donohue variant would be added as a function |
| LTP-032 | duplicate | CSL-0099 | air-side DP of finned bundles already translated (ESDU high/low-fin); Handbook variant of the same family |
| LTP-038 | merged | CSL-0095 | same Zukauskas/HEDH plain-tube-bank Nu set; condensation/boiling in CSL-0089/CSL-0088; only the Euler-number bank DP is new |
| LTP-039 | duplicate | CSL-0099 (+CSL-0109) | finned-bundle air-side HTC and fin efficiency already translated; Handbook variant of the same family |
| LTP-043 | merged | CSL-0138 | same moving-boundary zone-boundary physics; the linear-dP helpers would be added as functions; Kim dry-out nearest CSL-0098 |
| LTP-044 | merged | CSL-0153 | ORC equipment-cost block already totalises Hall-type CAPEX; Caputo cost and CPI updating would extend it |
| LTP-045 | duplicate | CSL-0095 | tube-bank/boiling/condensation/radiation HTCs already in CSL-0095/0088/0089/0107; Van Long Le provenance to clear |
| LTP-047 | discarded | nearest: CSL-0110 | ASME allowable-stress pressure rating is mechanical-design data, not thermodynamics |
| LTP-060 | merged | CSL-0133 | same propane pinch HP; pipe pressure drops (CSL-0130/CSL-0316) and charge (CSL-0131) would be a variant there |
| LTP-066 | duplicate | LTP-051 | same Aungier analysis core; PSO design loops infeasible without an optimiser |
| LTP-067 | duplicate | LTP-052 | radial-turbine loss models are the analysis core; PSO design loops infeasible |
| LTP-068 | duplicate | LTP-052 | radial/axial compressor loss models are the analysis core; PSO design loops infeasible |
| LTP-072 | discarded | superseded by CSL-0138 | legacy scripts not runnable (missing BaseClases package); superseded by the moving-boundary model |

Kept `todo`: LTP-006 (two-phase CO2 ejector, card C-446), LTP-017 (thermosyphon
HX with operating limits, card C-447), LTP-037 (shell-side HTC correction
factors, card C-441), LTP-040 (PCHE HTC, card C-442), LTP-051 (Aungier axial
turbine loss models, card C-448), LTP-052 (radial machine loss models, card
C-449).

## 2026-11-02 upstream sweep (C-46x)

Card C-461 (T-TRIAGE, batch B-19): the three unmerged branches since the pinned
commit f03f7f47 - `origin/Elise` (19 commits, ~4100 lines added), `origin/Basile_Chaudoir`
(62 commits, ~17000/-10700) and `origin/Titouan_Janod` (large reorganising diff) -
inspected with throw-away diffs against f03f7f47 (no checkout in ~/git/LaboThapPy).
8 new inventory rows LTP-075..LTP-082 (2 `todo`, 4 `merged`, 3 `duplicate` in
total for the batch: counts below), labothappy now 82 candidates.

Survey (pure API/packaging/docs/plotting changes: `pressure_drop_distributor.py`,
`plate_DP_old.py` extraction, `toolboxes/solvers/__inti__.py` typo fix, branch
file renames design/sizing_1D -> design_1D/sizing, report.log churn, deleted
toolboxes (step_smoother, pump_perf_data, zero_brent)): NOT candidates.

No new row (reviewed): pytest-infra `machine/circuit_rec.py` + the
solver_comparison example set (Titouan: rec vs it solvers around already
translated components Zorlu HP/ORC; CSL-0039/CSL-0312 stay representative);
`CO2_HP_COP_Optimization`, `CO2_RC_HX_presize_Optimization`,
`CO2_RC_efficency_Optimization`, `CO2_RC_Cost_Optimization`, `PCHE_sizing.py`,
`shell_and_tube_sizing.py` (Basile, all pyswarms/PSO layouts
-> same infeasibility class as LTP-063/LTP-069/LTP-071); `CO2_RC.py` cycle
example (architecture duplicate of LTP-058 -> CSL-0144); `hexs_Zorlu.py`,
`hex_LHTES.py` (Titouan example scripts around `hex_MB_charge_sensitive`
-> CSL-0138 and `hex_eNTU` -> CSL-0128); `Aitor.py` (renamed `Aitor_F&T.py`,
LTP-054); `hydraulic_diameter_shell.py` helper (equations subset of
CSL-0103/CSL-0321); `properties/void_fraction.py` (move of the LTP-033 module,
merged; note upstream also DELETES `component/expander/ejector_csteff.py`,
the source of CSL-0325, which stays pinned at f03f7f47).

### New inventory rows

| ID | Decision | Target | Reason |
|---|---|---|---|
| LTP-075 | merged | CSL-0138 | hex_MB_charge_sensitive_bis: clean restructure, no new physics |
| LTP-076 | merged | CSL-0138 | hex_MB_plate_elise + correlations-distributor adapter API; plate HX already LTP-016 -> CSL-0138; the Martin/Lockhart-Martinelli DP rewrite of `plate_DP.py` is under re-check (impact CSL-0111) |
| LTP-077 | discarded | nearest CSL-0130/0316/0131 | splitter with optional dp/charge: trivial mass balance + calls to already translated sources |
| LTP-078 | todo | (T-FUNC card) | NEW physics: curved-duct HTC correlations (helical coil/Ito, SPHE spiral-plate, Shah-London rectangular duct) + SPHE MB example; absent from the library |
| LTP-079 | duplicate | LTP-028 | straight_pipe_DP.py: rewritten subset of pipe_DP.py (CSL-0130) |
| LTP-080 | duplicate | LTP-051 | Titouan axial-turbine mean-line loss-model design; Aungier core already LTP-051 -> CSL-0327 |
| LTP-081 | duplicate | LTP-051 | Basile axial-turbine mean-line loss-model sizing (PSO) |
| LTP-082 | duplicate | LTP-052 | Titouan radial compressor eta-row designs + 1D radial pump design; loss models already LTP-052 -> CSL-0328 |

### Impact on existing labothappy-derived models

| Model | Upstream (branch, commit/files) | Effect | Re-check? |
|---|---|---|---|
| CSL-0125 pump_curve_similarity | origin/Elise 8514bf89 (pump_curve_similarity.py rewrite + example) | mode M_N physical change: eta and NPSH_r now evaluated at the equivalent flow V_dot/N_rated (eta attributed unchanged at similarity, NPSH_r scaled N^2), out-of-range flag on the equivalent flow | yes |
| CSL-0131 void fraction | origin/Elise (void_fraction.py 86 lines: NEEDS_FLOW refactor, geometry-derived G, model-name validation) | compute_void_fraction refactor: G now derivable from m_dot/(A*n) or circular section for the 6 flow-dependent models; results should be identical when G is explicit | yes |
| CSL-0111 plate HX correlations | origin/Elise plate_DP.py rewrite (Martin/VDI dp, Lockhart-Martinelli-Chisholm) | translated equations (HAN dp and HTC set at f03f7f47) differ from rewritten upstream; same family, different equations (the HAN DP dropped to plate_DP_old.py) | yes |
| CSL-0130 pipe correlations | origin/Elise 0aab141c (pipe_DP.py modified, 23 lines: adapter consistency; new straight_pipe_DP subset is LTP-079) | correlations unchanged in intent; the component's correlation-calling scheme reworked (m_dot -> G) around pipe_DP | yes |
| CSL-0138, CSL-0312, CSL-0325 (MB family) | origin/Elise ff52f643 (two_phase.py: viscosity/surface-tension fallback to a full-EOS state; hex_MB_charge_sensitive.py comments only) | source crash conditioned on R1233zd(E) transport in CoolProp 8.0.0 partially fixed by the added CSP fallbacks; these helper fixes are used by CSL-0138/CSL-0130/CSL-0131; no physics change in the pinned components; the crash in the CSL-0312 source example (R1233zd(E) transport in CoolProp 8.0.0) is partially addressed upstream; the CSL-0325 source file ejector_csteff.py is DELETED upstream (Titouan reorg) | no (pinned sources unchanged for library) |
| CSL-0130/CSL-0131-0313 (two-phase density/charge) | origin/Elise two_phase.py viscosity compute fixed | two-phase density/charge results can change marginally; the two-phase viscosity used by CSL-0130/CSL-0131 is capped by the same fallback | yes |

Secondary (TESPy side of the card text; the TESPy repository is pinned at
19425523 and dev is 166 commits ahead / v0.12.0):

| Model | Upstream | Effect | Re-check? |
|---|---|---|---|
| CSL-0323 fuel cell | src/tespy/components/reactors/fuel_cell.py unchanged 19425523..origin/dev except API/deprecation cleanups | `_calc_Q` keeps `Q = -m_in1*(h_out1 - h_in1)` with Q<=0 (heat rejected): the sign convention suspected in CSL-0323 is CONFIRMED unchanged upstream, not fixed | no |
| all TESPy-oracle models (e.g. CSL-0314 steam_turbine) | dev commit e3038fff (PR #1102, fix #709 "vapour content sign"): pure-fluid quality 0/1 below T_crit even outside two-phase, NaN supercritical, consistent for all wrappers | affects only reference values computed with TESPy dev >= this commit (previously -1 returned above T_crit at subcritical p) | no for pinned translations (re-check only if a model re-verifies against TESPy dev) |

steam_turbine / pump / turbocompressor / characteristic-limits TESPy sweeps
were NOT re-inspected in this LaboThapPy card (template text of the TESPy
sweep card; deferred to that card).

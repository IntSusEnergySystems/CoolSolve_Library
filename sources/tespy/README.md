# TESPy - source sweep for the CoolSolve_Library

Quick sweep (not an audit) of **TESPy (Thermal Engineering Systems in Python)** to build a backlog of models that can be translated into the EES-compatible CoolSolve language. The machine-readable backlog is [`inventory.csv`](inventory.csv) (52 rows, `TSP-001` ... `TSP-052`).

| | |
|---|---|
| Repository | https://github.com/oemof/tespy (local snapshot `/home/sylvain/svn/tespy`, commit `19425523`, 2026-10-01; 5 715 commits, 47 distinct author names) |
| Documentation | https://tespy.readthedocs.io |
| Version | 0.11.3.dev0 (Python >= 3.11; roadmap: v0.12, 1.0) |
| Stack | CoolProp (also IAPWS, PyroMat, ThermoPack, REFPROP back ends), NumPy/SciPy, pandas, fluprodia, pymoo (optional) |
| Size | `src/tespy` 100 files/43.3 k lines (`components` 64 files/22.7 k, `networks`+`solver`+`connections` ~11 k, `tools` 8.9 k, `models` 0.7 k); `tests` 64 files/17.2 k lines; `tutorial` 12 scripts; `docs` incl. 12 notebooks and a 5-item model library |

## 1. License and attribution

* **License: MIT** - `LICENSE`: "Copyright (c) Francesco Witte"; 76 source files carry `SPDX-License-Identifier: MIT` and the sentence "copyrighted by the contributors recorded in the version control history". Tests, tutorials and docs live in the same repository and licence.
* **Maintainer/lead:** Francesco Witte (5 198 of 5 715 commits). `CITATION.cff` lists 34 contributors (Chaofan Chen, Markus Brandt, Malte Fritz, Julius Meier, Jonas Freissmann, Jorrit Wronski, Hannes Schneider, Sergio Tomasinelli, Jens Bucker, ...). Part of the oemof ecosystem.
* **How to cite** (from `README.rst`/`CITATION.cff`): software DOI `10.5281/zenodo.2555866`; JOSS paper (below); for the exergy features the Energies paper.

```bibtex
@article{Witte2020,
  doi = {10.21105/joss.02178}, year = {2020}, publisher = {The Open Journal},
  volume = {5}, number = {49}, pages = {2178},
  author = {Francesco Witte and Ilja Tuschy},
  title = {{TESPy}: {T}hermal {E}ngineering {S}ystems in {P}ython},
  journal = {Journal of Open Source Software} }
@article{Witte2022,
  doi = {10.3390/en15114087}, year = {2022}, volume = {15}, number = {11}, article-number = {4087},
  author = {Witte, Francesco and Hofmann, Mathias and Meier, Julius and Tuschy, Ilja and Tsatsaronis, George},
  title = {Generic and Open-Source Exergy Analysis - Extending the Simulation Framework TESPy},
  journal = {Energies} }
```

* **Third-party material inside the repo** (cite the original, check redistribution): Traupel turbine characteristic (`data/char_lines.json`, Traupel 2001), Bell (2015) oracle results (`tests/test_components/bell2015_five_cases.json`), Ebsilon result tables (`tests/test_models/cgam-ebsilon-results.csv`), Penkuhn & Tsatsaronis (2018) sCO2 state table (in `docs/model_library/sco2.ipynb`), D'Ettorre & Heerup (2026) CO2 booster case study (`co2_cycle.ipynb`), BITZER screw-compressor catalogue data (`heat_pump_partload.ipynb`, polynomial-compressor tests), Viessmann Vitocal 300-G datasheet values (GCHP tutorial). Several validation models live in separate repositories with their own licences (`fwitte/SEGS_exergy`, `fwitte/sCO2_exergy`, `fwitte/refrigeration_cycle_exergy`, CGAM chemical-exergy repo, `oemof/exerpy`).

**Text to reuse in the README of a translated model** (MIT requires the copyright and permission notice in copies or substantial portions):

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
<component/model name> from TESPy, file <path>, commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve, <specification set, simplifications>.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python",
J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific basis: <reference of the model, e.g. Penkuhn & Tsatsaronis 2018>.
```

> **Maintainer decision (2026-10-04):** the permissive MIT license of TESPy allows the translation; translated models are published under the library license, with the credit block above in their README and `model.json` (no license file needs to be copied).

## 2. What the repository contains

* **Components** (`src/tespy/components`, ~28 physically distinct models, every class has equations in its docstring and a doctest with reference numbers that runs in CI): turbomachinery (Compressor, TurboCompressor with characteristic maps, Turbine with Stodola cone law, SteamTurbine with wet-expansion correction, Pump with head/flow curves), displacement machinery (EN12900 PolynomialCompressor, with cooling), heat exchangers (HeatExchanger/Condenser/Desuperheater/ParallelFlow with LMTD-UA, NTUHeatExchanger, SectionedHeatExchanger, MovingBoundaryHeatExchanger, SimpleHeatExchanger, Pipe, SolarCollector, ParabolicTrough), valve, drum/droplet separator, merge/splitter/separator/node, CombustionChamber (+diabatic), CombustionEngine (CHP), WaterElectrolyzer, FuelCell, motor/generator/power and heat buses, humid-air connection (experimental).
* **Model library & tutorials** (`docs/model_library`, `tutorial/`, `docs/how_to_guides`): sCO2 recompression Brayton cycle, combined-cycle plant with district heat, CO2 transcritical booster refrigeration, heat pump with screw-compressor map and part load, ground-coupled heat pump with exergy analysis, ORC and cascade heat pump (ModelTemplate), basic Rankine/heat pump/gas turbine/district-heating tutorials, stepwise NH3 heat pump, regenerative steam plant with optimisation, zeotropic heat pump, humid-air coil.
* **Test models** (`tests/test_models`): CGAM (vs Ebsilon), SEGS solar plant (vs Ebsilon), two-stage NH3 heat pump (vs Ebsilon COP table), plus component tests with numeric references (`tests/test_components`: Bell 2015 oracle, EN12900 fits, eps-NTU relations cross-validated against the `ht` library and against **CoolSolve examples and LaboThapPy**).
* **Skipped as infrastructure:** `Network` (Newton solver, presolve, block decomposition), `Connection`/`Ref`, fluid-property wrappers and mixture rules, `CharLine/CharMap` machinery, `ModelTemplate` (parameter lookup, sensitivity analysis, pymoo optimisation), subsystems, unit handling, plotting (fluprodia), logger, schema; exergy analysis proper is in the external `exerpy` package.

## 3. Inventory statistics (`inventory.csv`)

52 rows: 46 steady models/cycles/components, 6 `function` rows (smoothed LMTD, eps-NTU relations, Darcy friction factor, default characteristic lines, Cecchinato UA scaling, physical exergy). Levels: L1 13, L2 20, L3 14, L4 5. Difficulty (first token of `notes`): easy 24, easy-medium 1, medium 20, hard 7. Priorities: `wave1` 8, `high` 8, `medium` 23, `low` 13. No `dynamic` or `optimization` rows: TESPy is steady-state; where the tutorial includes pymoo optimisation (steam plant, CO2 booster, sCO2, CCPP) the base model is listed as `steady` and the note says the optimiser part is out of scope. `n_lines` = physical lines of the main file (lines of the named functions for `function` rows living in larger files; code lines for notebooks).

**Reference results are TESPy's strength:** doctests in every component docstring (verified: the turbine doctest, 10 kg/s steam 550 C/110 bar -> 0.5 bar, eta_s 0.9, gives P = -10 452 574 W and x = 0.914 with CoolProp 7.2); CGAM Ebsilon table (`cgam-ebsilon-results.csv`, deviation < 0.5 %); SEGS vs Ebsilon (31.769 MW net, T(c79) = 296.254 C); sCO2 published T/p table (Penkuhn & Tsatsaronis 2018); Bell (2015) moving-boundary cases (8 cases, JSON); two-stage NH3 heat-pump COP matrix (2.216-2.866, tolerance 7 %); polynomial-compressor catalogue tables. The basic tutorials have **no stored numbers** (tests only execute them) - independent CoolProp checks computed during this sweep: Rankine tutorial (first solve) P_turb = 13.21 MW, P_pump = 0.224 MW, Q_sg = 33.69 MW, eta = 38.6 %, x_out = 0.866; R134a heat pump tutorial p_evap = 5.72 bar, p_cond = 26.87 bar, COP = 3.378, m = 8.06 kg/s, P_comp = 296 kW.

## 4. Recommended translation candidates (top 15)

| # | ID | Candidate | Why | Difficulty | Reference data |
|---|---|---|---|---|---|
| 1 | TSP-042 | sCO2 recompression Brayton cycle, 100 MW (`sco2.ipynb`) | validated against published data; recuperator pinch/sections; not in CoolSolve examples (`orc_co2` is a CO2 ORC) | medium | published T, p, exergy table for 12 states |
| 2 | TSP-050 | CGAM gas turbine + HRSG + drum (`test_CGAM_model.py`) | classic benchmark, ties combustion + HRSG + exergy | medium | Ebsilon CSV (m, T, p, h, s, composition), compressor 29.66 MW, turbine 59.66 MW |
| 3 | TSP-034 | Rankine cycle with condenser/cooling water, generator/motor, part-load cone law | canonical, easy; adds cooling-water coupling and off-design to `rankine1/2` | easy | independent CoolProp numbers above |
| 4 | TSP-035 | R134a heat pump tutorial | canonical, easy, parametric COP | easy | independent CoolProp numbers above |
| 5 | TSP-003 | Turbine: eta_s, Stodola cone law, characteristic line (off-design) | the off-design recipe reused by every cycle | easy | doctest P = -10 452 574 W, x = 0.914; off-design p_in = 88.6 bar |
| 6 | TSP-008 + TSP-009 | HeatExchanger / Condenser: UA with smoothed LMTD, ttd/pinch specs, UA characteristics | generic HX equations of all cycle models | easy | doctests + tests |
| 7 | TSP-022 | Combustion chamber (fuel/air stoichiometry, lambda, thermal input) | prerequisite of CGAM, gas-turbine tutorial | medium (species balance, ideal-gas mixture) | doctests, `test_combustion.py` |
| 8 | TSP-030 | eps-NTU relations for 7 flow arrangements (FUNCTION) | reusable, cross-validated (also against CoolSolve exchangers1-3) | easy | `test_ntu_heat_exchanger.py` |
| 9 | TSP-014 | Moving-boundary HX (Bell 2015) | reference oracle for any MB translation (fixed zone topology) | hard | 8 oracle cases (Q, outlet T) |
| 10 | TSP-040 | Regenerative steam plant with two extractions (optimisation tutorial base model) | extends `rankine2`; optimiser replaced by a 2-D sweep | medium | none stored |
| 11 | TSP-037 | District-heating loop (pipes with dP and heat loss, INCOMP water) | gap in CoolSolve examples | easy | none stored |
| 12 | TSP-044 | CO2 transcritical booster refrigeration (supermarket) | transcritical CO2 refrigeration gap | medium | Case Study 1 inputs from the chapter, no outputs |
| 13 | TSP-051 | SEGS parabolic-trough steam plant (Therminol VP-1) | large validated plant: ~80 connections, reheater, 5 feedwater heaters | hard | Ebsilon: 31.769 MW, T(c79) = 296.254 C |
| 14 | TSP-006 | EN12900 polynomial compressor (+ `heat_pump_partload` follow-up) | catalogue-based compressor model; overlaps `orc_co2` map approach | medium | catalogue tables in tests |
| 15 | TSP-036 | Open gas-turbine tutorial (CH4/CO2 fuel) | simple Brayton with combustion; use CGAM as validation | medium | none stored |

Next tier (`medium`): SteamTurbine wet-expansion (Baumann), Pump maps, Sectioned HX, Pipe with surface/buried heat loss, SolarCollector/ParabolicTrough, CombustionEngine (CHP), CCPP with district heat, two-stage NH3 heat pump with flooded evaporator, ORC + cascade heat pump, GCHP with exergy.

## 5. How TESPy equations map to CoolSolve/EES equations

TESPy is *equation-oriented* like CoolSolve: every connection carries `m, p, h` (+ fluid mass fractions), every component adds residual equations `f(x) = 0`, the network solves them with Newton after presolve and block decomposition. Translation is therefore mostly 1:1.

| TESPy | CoolSolve/EES |
|---|---|
| connection variables `m,p,h` | arrays or named variables per state point; `T,s,x,v` from property calls (`Temperature(fluid$,P=p,h=h)` etc.) |
| mandatory mass/fluid equality, `Valve` h_in = h_out, `CycleCloser` | `m_out = m_in`; `h_out = h_in`; cycle closer disappears (connect state points directly) |
| `Turbine eta_s`: `-(h_out-h_in) + (h_out_s-h_in)*eta_s = 0` | `h_out - h_in = eta_s*(h_out_s - h_in)`, `h_out_s = h(fluid, s = s_in, P = p_out)`; compressor/pump: `(h_out-h_in)*eta_s = h_out_s - h_in` |
| power connection `E = -m(h_out-h_in)` (turbine negative) | define work as positive output/input explicitly; motor/generator `eta`, bus balances as sums |
| `HeatExchanger UA`: `Q + UA*LMTD = 0`, smoothed LMTD (Quoilin 2011); `ttd_u`, `ttd_l`, `ttd_min`, `td_pinch`, `eff_*`; `pr`, `dp`, `zeta` | `Q = m1*(h1_in-h1_out) = m2*(h2_out-h2_in)`; `Q = UA*LMTD` (use the smooth form near dT_u = dT_l or negative differences); `ttd_u = T1_in - T2_out`; `p_out = pr*p_in` |
| `Condenser` | saturated-liquid (or subcooled) outlet, `ttd_u` vs dew-line temperature; for exact UA split into desuperheating/condensing/subcooling zones |
| specification flexibility (`T`, `x`, `T_dew`, `td_bubble`, `Ref(c,factor,delta)`) | choose the set of equations/inputs so that unknowns = equations; `Ref` is just `p_b = f*p_a + d`; the tutorials list the specification switching (robust first, final later) - keep the *final* set |
| `design` / `offdesign` lists, `design_path` | the design solution supplies constants (`m_ref`, `p_in_ref`, `v_ref`, `UA_design`, `eta_s_design`); in CoolSolve keep a design file and an off-design file, or both sets of variables in one model |
| Stodola `cone`: `m = m_ref*(p/p_ref)*sqrt(p_ref*v_ref/(p*v))*sqrt((1-(p_out/p)^2)/(1-pr_ref^2))` | explicit equation with design constants |
| `CharLine`/`CharMap` (`data/char_lines.json`, `char_maps.json`) | CoolSolve lookup tables (CSV), linear interpolation; efficiency = `eta_design*f(m/m_ref)` |
| `UA_char`, `UA_cecchinato` (Cecchinato 2010) | `UA = UA_ref*f_UA` with `f_UA = (1+x)/((m_c/m_c,ref)^-Re_c + x*(m_h/m_h,ref)^-Re_h)`, `x = (alpha_c/alpha_h)*(A_c/A_h)` |
| `Sectioned` (N sections) / `MovingBoundary` | `DUPLICATE` over fixed N enthalpy sections (equal duty) with `UA_i`, `T_h,i`, `T_c,i`; phase-boundary logic needs a fixed regime or IF-based zone detection |
| `CombustionChamber` (`COMBUSTION_FLUIDS`, `lamb`, `ti`) | species balances for the chosen fuel (e.g. CH4), `lambda = O2_available/O2_stoich`, energy balance with LHV/formation enthalpies, ideal-gas mixture enthalpy; reference-state differences vs TESPy/Ebsilon: compare enthalpy/entropy *differences* (the CGAM test shifts references) |
| `Pipe` Darcy: `dp = 8 m abs(m) v_avg L lambda(Re,ks,D)/(pi^2 D^5)`, Hazen-Williams, heat loss UA/`Tamb` | explicit equation + friction factor FUNCTION (Colebrook implicit is fine) |
| `ModelTemplate`, pymoo, sensitivity analysis | replace by CoolSolve parametric tables; no optimiser yet |

Practical notes: (i) TESPy units are converted at the `Network` level (bar, degC, kJ/kg, t/h, MW...) - normalise to the unit convention of the CoolSolve examples; (ii) models close with a *cycle closer*: in CoolSolve one state point is simply defined once (no extra equation); (iii) hard models (SEGS, CCPP, GCHP, heat-pump part load) need good starting values - run TESPy once and export `nw.results` as the `.initials` file; (iv) TESPy's block solver is why large models converge there - CoolSolve has structural block decomposition and tearing as well, but expect to provide initials for CO2 near the critical point and for two-phase zones; (v) mixtures other than ideal gases (zeotropic blends, humid air) depend on CoolProp HEOS/HAPropsSI and are lower priority.

## 6. Overlaps and gaps

* **Overlap with CoolSolve examples:** `rankine1/2` (steam cycles), `refrigeration1-3`/`heat_pump_MSTh_SB_R10` (vapour-compression), `orc_*` (ORC), `turbocompressor*` (compressor maps), `exchangers1-3` (eps-NTU; TESPy's NTU tests were built from these three cases), `cooling_coil`/`humidair*`/`evaporator` (psychrometrics), `boiler_cpbar*`/`internal_combustion_engine*` (combustion), `pressuredrop` (Colebrook).
* **Gaps filled (vs a classic EES teaching collection):** validated benchmark models (CGAM, SEGS, sCO2 recompression, two-stage NH3 heat pump) with stored reference data; off-design formalism (Stodola cone law, characteristic lines, UA scaling, design-to-off-design workflow); wet-steam Baumann correction; EN12900 polynomial compressors; CHP gas engine with load-dependent characteristics; generic fuel/air combustion with lambda; electrolyzer and fuel cell; district-heating pipes with heat loss and Hazen-Williams; solar collector with IAM (Quaschning/Janotte); combined cycle with district heat extraction; CO2 booster refrigeration; exergy post-processing (reference-state physical exergy).
* **Not translatable / out of scope:** pymoo optimisation, ModelTemplate plumbing, Thermopack/REFPROP-specific zeotropic mixture studies (low priority), plotting.
* **Authorship link:** the smoothed LMTD (`smoothed_lmtd`, from S. Quoilin's PhD thesis 2011), the discretised Sectioned HX (after the NextGenerationHeatPumps repository) and Bell et al. 2015 (co-authored by S. Quoilin and V. Lemort) are cited directly in TESPy - cross-checks against the original EES versions are possible.

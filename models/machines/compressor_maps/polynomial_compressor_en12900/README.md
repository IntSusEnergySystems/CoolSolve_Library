# Positive-displacement compressor with EN12900 efficiency-map polynomials

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0136`

Translation of the TESPy class `PolynomialCompressor`: a semi-hermetic positive
displacement compressor whose isentropic and volumetric efficiencies are
third-order (10-coefficient) EN 12900 polynomials of the evaporation and the
condensation temperature, read from a compressor catalogue. A dissipation ratio
splits the electrical power between the compression work and the heat leaving
the machine, and the mass flow follows from the swept volume, the frequency and
the volumetric efficiency. Four operating points of the source example are
computed: three with a fixed frequency and one with an imposed volumetric flow,
where the frequency becomes the unknown.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R134a (any refrigerant accepted by the property functions) |
| **Size** | 152 equations, all explicit (largest block: 1); 4 operating points, 1 `FUNCTION`, 1 `DUPLICATE` |
| **Source** | TESPy `src/tespy/components/displacementmachinery/polynomial_compressor.py` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`), tests `tests/test_components/test_polynomial_compressor.py`, map of `docs/model_library/heat_pump_partload.ipynb` |
| **Authors** | Francesco Witte (TESPy lead developer) and the TESPy contributors |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; translation verified against TESPy (see *Verification*) |

## Problem statement

An R134a semi-hermetic compressor of the catalogue used in the TESPy example
(power and cooling tables of `tests/test_components/test_polynomial_compressor.py`,
displacement 214 m³/h at 20 Hz, 20 K suction superheat, no liquid subcooling) is
operated at four points. Points 1 to 3 have a fixed frequency, a given
evaporation and condensation temperature and a given suction superheating;
point 4 has an imposed volumetric flow of 400 m³/h at 10/40 °C with 10 K
suction superheating, so that the frequency is a result. Determine the
isentropic and volumetric efficiency, the refrigerant mass flow, the electrical
power, the heat leaving the machine and the discharge temperature, and compare
the computed power with the catalogue value.

## Model

Compressor (`su` = suction state, `ex` = discharge state, `s` = isentropic
discharge state; indices 1 to 3 are the `DUPLICATE` loop of operating points,
`_4` the point with the imposed volumetric flow):

- map evaluation (TESPy `_calc_EN12900_SI`, temperatures in °C):
  `T_ev = t_sat(p_su)`, `T_cd_ref = t_sat(p_ex)` — the dew-point and the
  bubble-point temperatures of the suction and the discharge pressure — and
  `eta_s = en12900(c_eta_s, T_ev, T_cd_ref)`, `eta_v = en12900(c_eta_v, ...)`;
- isentropic relation with dissipation (TESPy `eta_s_poly_group_func` and
  `_calc_h2`): the outlet enthalpy is first corrected for the heat that leaves
  the machine, `h_2 = (h_ex - f_diss·h_su)/(1 - f_diss)` (virtual adiabatic
  discharge enthalpy), then
  `eta_s·(h_2 - h_su) = h_ex,s - h_su` with `h_ex,s = h(p_ex, s_su)`;
- displacement (TESPy `eta_vol_poly_frequency_group_func`):
  `m_dot = eta_v·V_swept·f/v_su`, `V_swept = V_dot_ref/f_ref`;
- power and dissipation (TESPy `_calc_P`, `_calc_Q_diss`):
  `P_el = m_dot·(h_ex - h_su)/(1 - f_diss)`, `Q_diss = -f_diss·P_el`, so that
  `P_el + Q_diss = m_dot·(h_ex - h_su)`;
- point 4: `m_dot = V_dot_4/v_su` and the frequency is
  `f_4 = m_dot·v_su/(eta_v·V_swept)`;
- the catalogue power and cooling polynomials (`c_pow`, `c_cool`, same
  EN 12900 form) give the catalogue values of the same operating points, used
  as the check of the map.

`FUNCTION en12900(c_0, …, c_9, T_ev, T_cd)` evaluates the third-order
polynomial `c_0 + c_1·T_ev + c_2·T_cd + c_3·T_ev² + c_4·T_ev·T_cd + c_5·T_cd² +
c_6·T_ev³ + c_7·T_ev²·T_cd + c_8·T_ev·T_cd² + c_9·T_cd³` of Cecchinato et al.
(2010); the term order is that of the source (`calc_EN12900`).

The **least-squares fit of the catalogue data** to the two efficiency
polynomials is data preparation, not an equation of the model: TESPy does it
outside the component (`generate_eta_polys_from_data`), and a polynomial
regression cannot be written as a set of steady simultaneous equations in EES
without a Gaussian elimination of the normal equations. The procedure is the
one of the source (`_calc_etas_from_polynome` + `fit_EN12900_points`):

1. fit the catalogue power and the catalogue cooling capacity with
   `en12900` (least squares on the 18 data points);
2. at every data point compute the saturation pressures, the suction state
   (`T_sh` superheat above `T_evap`) and the condenser-outlet state (`T_sc`
   subcooling below `T_cond`), the isentropic discharge enthalpy,
   `m_dot = Q_0/(h_su - h_cd,out)`,
   `eta_s = m_dot·(h_su,s - h_su)/P_cat` and
   `eta_v = m_dot/(rho_su·V_swept·f_poly)`;
3. fit `eta_s(T_evap, T_cond)` and `eta_v(T_evap, T_cond)` with `en12900`.

The four coefficient sets of the model are the result of steps 1–3 for the
catalogue of the TESPy test (see *Conversion log*).

| Inputs | Value (points 1 / 2 / 3 / 4) | Outputs (point 1) | Value |
|---|---|---|---|
| `T_evap` | -10 / 10 / 0 / 10 °C | `eta_s` isentropic efficiency | 0.4995 |
| `T_cd` | 50 / 40 / 50 / 40 °C | `eta_v` volumetric efficiency | 0.8137 |
| `DELTAT_sh` | 10 / 10 / 20 / 10 K | `m_dot` refrigerant flow | 0.4630 kg/s |
| `f` | 20 / 20 / 50 / 40.45 Hz | `V_dot` volumetric flow | 0.04837 m³/s |
| `diss` | 0.05 / 0.05 / 0 / 0.05 | `P_el` electrical power | 38.38 kW |
| `V_dot_ref`, `f_ref` | 214 m³/h, 20 Hz | `Q_diss` heat leaving the machine | -1.919 kW |
| `DELTAT_sh_ref`, `DELTAT_sc_ref`, `f_poly` | 20 K, 0 K, 50 Hz | `T_ex` discharge temperature | 100.46 °C |

## How to run

Open `polynomial_compressor_en12900.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./polynomial_compressor_en12900.eescode
```

No `.initials` or `coolsolve.conf` is needed: the 152 equations are explicit and
solve directly. To study another operating point, edit the `T_evap`, `T_cd`,
`DELTAT_sh`, `f` and `diss` values of the loop (a sweep over them is a CoolSolve
parametric study); to use another machine, replace the four coefficient sets and
`V_dot_ref`/`f_ref`/`DELTAT_sh_ref`/`DELTAT_sc_ref`/`f_poly` with the ones of its
catalogue.

## Results

| Point | T_evap / T_cd [°C] | T_su [°C] | p_su / p_ex [bar] | eta_s [-] | eta_v [-] | m_dot [kg/s] | V_dot [m³/s] | f [Hz] | P_el [kW] | Q_diss [kW] | T_ex [°C] | P_cat [kW] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | -10 / 50 | 0 | 2.006 / 13.179 | 0.4995 | 0.8137 | 0.4630 | 0.04837 | 20 (imposed) | 38.38 | -1.919 | 100.46 | 96.50 |
| 2 | 10 / 40 | 20 | 4.146 / 10.166 | 0.6652 | 0.9243 | 1.0548 | 0.05494 | 20 (imposed) | 31.17 | -1.558 | 60.48 | 78.00 |
| 3 | 0 / 50 | 20 | 2.928 / 13.179 | 0.5866 | 0.8578 | 1.6726 | 0.12748 | 50 (imposed) | 99.01 | 0 | 96.42 | 98.91 |
| 4 | 10 / 40 | 20 | 4.146 / 10.166 | 0.6652 | 0.9243 | 2.1331 | 0.11111 | 40.45 (result) | 63.03 | -3.151 | 60.48 | — |

Point 1 runs at 20 Hz, i.e. at the displacement frequency of the catalogue
reference (214 m³/h): its volumetric flow is 174.1 m³/h = 0.8137 × 214 m³/h.
At the catalogue point (50 °C, 0 °C) the model power is 99.01 kW against the
99.2 kW of the catalogue table (0.10 %), the residual of the polynomial fit
through the power and cooling data. Point 4 is run at 40.45 Hz to reach the
imposed 400 m³/h.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): eta_s / eta_v map of the
     compressor (T_evap-T_cond plane), figures/polynomial_compressor_en12900_eta.png -->

## Verification

TESPy has no stored solutions for this component, so its own examples and tests
were run in a throw-away virtual environment (Python 3.12.3,
TESPy 0.11.3.dev0 installed from the local snapshot at commit
`19425523`, CoolProp 8.0.0). Scripts (throw-away `work/` folder, deleted when
the card was closed, as the workflow requires): `run_reference.py` (the runs
below, values in `reference_results.json`, printed output in
`reference_run.txt`), `make_reference_csv.py` (the CSV read by
`compare_solution.py`), `bitzer_check.py` (item 4) and
`crosscheck_csl0123.py` (item 6).

1. **Component test** `tests/test_components/test_polynomial_compressor.py`:
   19 tests passed (`pytest -q`, 4.8 s), including `test_eta_poly`, which
   requires the model power at the catalogue point to stay within 1 % of
   99.2 kW and the volumetric flow to equal `V_swept·f·eta_v`.
2. **Class docstring (doctest)** of `polynomial_compressor.py`: 2 doctests
   passed (`pytest --doctest-modules`).
3. **Translation vs TESPy**, with
   `python3 ../CoolSolve/tools/compare_solution.py polynomial_compressor_en12900.sol reference/tespy_variables.csv`
   (63 common variables: `eta_s`, `eta_v`, `m_dot`, `P_el`, `Q_diss`, `T_ex`,
   `T_su`, `h_su`, `h_ex`, `s_su`, `v_su`, `p_su`, `p_ex`, `V_dot`, `T_ev`,
   `T_cd_ref` of the four operating points):

   | Run | Result |
   |---|---|
   | `--rtol 1e-06` | *63 common variables, 0 differ (rtol=1e-06); only in EES: 0; only in CoolSolve: 89* |
   | `--rtol 1e-09` | *63 common variables, 3 differ (rtol=1e-09)*, maximum relative difference **8.7e-09** (`T_su[3]`, an input temperature) |

   The three largest results, e.g. point 1: `eta_s` 0.499516 / 0.499516,
   `eta_v` 0.813665 / 0.813665, `P_el` 38 384.932 W / 38 384.932 W,
   `Q_diss` -1 919.247 W / -1 919.247 W (TESPy / CoolSolve); point 3:
   `P_el` 99 008.569 W / 99 008.569 W against the catalogue value 99 200 W.
   Not compared: the variables with no TESPy counterpart in the printout
   (`h_2`, `h_2_4`, `P_cat`, `Q_0_cat`, `P_dev`, the coefficient arrays) and
   the state-point arrays of the diagram block.
4. **Bitzer SP-111-1 map** of `docs/model_library/heat_pump_partload.ipynb`
   (the second verification source named in the card): the notebook prints
   `eta_s(2 °C, 57 °C)` and `eta_vol(2 °C, 57 °C)` for the three frequency maps
   of the catalogue. Scratch copies of this model file with the notebook's
   coefficients for 30, 50 and 90 Hz and the evaluation point (2 °C, 57 °C)
   give

   | Map | eta_s CoolSolve / notebook | eta_v CoolSolve / notebook |
   |---|---|---|
   | 30 Hz | 0.5053 / 0.505 | 0.9025 / 0.903 |
   | 50 Hz | 0.5701 / 0.570 | 0.9150 / 0.915 |
   | 90 Hz | 0.5764 / 0.576 | 0.9203 / 0.920 |

   i.e. the `FUNCTION en12900` of this model reproduces the notebook values
   rounded to three digits at all three frequencies.
5. **Catalogue tables** (the fixture power and cooling data of the test, 18
   points): the fitted power polynomial reproduces the data with a maximum
   relative deviation of 6.4e-04 and the fitted cooling polynomial 2.3e-04
   (`test_fit_en12900` requires 1e-03); through the two efficiency maps the
   computed power is 0.10 % below the catalogue value at the point of the
   table (point 3), which is the residual of the two-stage fit.
6. **Cross-check with `CSL-0123`** (`copeland_catalogue_correlation`, ARI/
   Copeland 3rd-order catalogue polynomial): both correlations are third-order
   polynomials with the same ten monomials in the same order (the only
   difference is the variable: °F in the ARI polynomial, °C in the EN 12900
   one), and both take the operating point from the saturation temperatures of
   the suction and the discharge pressure. At a shared point (R134a,
   `p_su` = 3 bar, `p_ex` = 10.17 bar, 5 K suction superheat, 50 Hz, the
   swept volume 211.22 cm³ read from the CSL-0123 table ZH38K4E-TFD) this
   model gives eta_is = 0.651, eta_v = 0.904, m_dot = 0.1374 kg/s, P = 5.51 kW.
   The Copeland columns of that table cannot be compared numerically: they
   imply eta_v = 0.003 and eta_is = 0.0007, which is not physical — the
   vintage of the shipped table is already documented in CSL-0123 (its stored
   EES run used 82.61 cm³ against 211.22 cm³ in the shipped table, and a power
   about three times the stored one). The cross-check therefore confirms the
   form and the operating point, not the machine data.
   At CSL-0123's own demonstration point (3 bar / 20 bar, i.e. 0.67 / 67.5 °C)
   the map of this model is extrapolated outside its data range (30–50 °C
   condensation): eta_v = 1.017 > 1. The polynomial must not be used outside
   the catalogue range (see *Limitations*).

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the TESPy component `PolynomialCompressor`, file
`src/tespy/components/displacementmachinery/polynomial_compressor.py`,
commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff /
version control history).
Original model released under the MIT License.
Changes: translated from Python to simultaneous EES equations; the iterative
network solver, the connection objects and the design/off-design switching
replaced by explicit equations; units normalised to SI-°C-Pa-J (the source
displays bar/°C/kJ/kg/kW); the four demonstration cases of the docstring, of
the component test and of the part-load notebook map; the polynomial fit kept
as data preparation (its coefficients are written in the model).
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in
Python", J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.

Scientific basis of the correlation (cited by the source):
L. Cecchinato, M. Chiarello and M. Corradi, "A simplified method to evaluate
the seasonal energy performance of water chillers", Int. J. Thermal Sciences
49(9), 1776-1786 (2010), doi:10.1016/j.ijthermalsci.2010.04.010 — the EN 12900
implementation followed by the source; EN 12900 is the European standard for
the rating conditions and polynomial representation of refrigeration
compressor performance data.
Catalogue data used in the model: the R134a power and cooling tables of
`tests/test_components/test_polynomial_compressor.py` (they come from the
Bitzer performance tables, as the notebook of the Bitzer SP-111-1 map
states).

Source file (Python, comments in English), local snapshot of S. Quoilin:
`~/git/tespy/src/tespy/components/displacementmachinery/polynomial_compressor.py`
(companions: `tests/test_components/test_polynomial_compressor.py`,
`docs/model_library/heat_pump_partload.ipynb`)
(inventory candidate `TSP-006`).

## Conversion log

- **2026-10-13 — translation** (workflow `T-TRANSLATE`): the TESPy network
  (Source, PolynomialCompressor, Sink, two connections) of the docstring
  rewritten as simultaneous equations. Equation-by-equation mapping:
  `eta_s_poly_group_func` → `eta_s·(h_2 - h_su) = h_ex,s - h_su` with
  `h_ex,s = enthalpy(fluid$, p=p_ex, s=s_su)`; `_calc_h2` → `h_2`;
  `eta_vol_poly_frequency_group_func` → `m_dot = eta_v·V_swept·f/v_su`;
  `energy_balance_group_func` / `_calc_P` → `P_el`; `_calc_Q_diss` →
  `Q_diss = -f_diss·P_el` (algebraically identical to `m·(h_ex - h_2)`);
  `_calc_eta_s`, `_calc_eta_vol` → the results `eta_s`, `eta_v`;
  `calc_EN12900` → `FUNCTION en12900`. Variable names of the source kept
  (`eta_s`, `eta_vol` → `eta_v`, `h2` → `h_2`, `P`, `Q_diss`, `frequency` → `f`,
  `dissipation_ratio` → `diss`, `reference_state` → the reference-state
  constants `DELTAT_sh_ref`, `DELTAT_sc_ref`, `f_poly`, `V_dot_ref`, `f_ref`,
  `V_swept`).
- **Unit conversion** (CoolSolve `docs/ees_import.md` §6, by hand): TESPy
  stores SI and displays bar/°C/kJ/kg/kW; the display units only. The source
  converts temperatures to °C inside `_calc_EN12900_SI`; the model evaluates
  the polynomials directly in °C (CoolSolve temperatures are °C), so no
  conversion appears in the equations. `displacement` 214 m³/h at 20 Hz is
  written as `V_dot_ref = 214/3600` m³/s and `f_ref = 20` Hz
  (`swept_volume_from_displacement`). The catalogue power in kW is written in
  W.
- **`T_dew_p` / `T_bubble_p` → `t_sat`**: the source reads the evaporation
  temperature as the dew-point temperature of the suction pressure and the
  condensation temperature as the bubble-point temperature of the discharge
  pressure. For a pure fluid both are the saturation temperature at that
  pressure, which is what `t_sat(p=…)` returns in CoolSolve; the map is
  therefore evaluated at the saturation temperatures of the two pressures.
  (The pressure drops between evaporator and compressor, and between
  compressor and condenser, are free in the model: give `p_su` and `p_ex`
  instead of `T_evap` and `T_cd` and the map still applies, as in the source.)
- **Operating-point specification**: the source sets `c1` with `T` and
  `td_dew` (dew-point depression) and `c2` with `p` or `T_dew`. The model
  takes the evaporation temperature, the condensation temperature and the
  suction superheating as inputs and writes `p_su = p_sat(T_evap)`,
  `p_ex = p_sat(T_cd)`, `T_su = T_evap + DELTAT_sh`; the dew-point depression
  of the source is the superheating `DELTAT_sh` of the model, and the
  saturation pressures of the source are recovered (`T_ev` = -10, 10, 0 °C and
  `T_cd_ref` = 50, 40, 50 °C in the .sol).
- **Not translated** (documented content of the source, not different
  physics): the `eta_s` / `eta_vol` *fixed-value* variants (the
  `eta_s_group`, `eta_vol_group`, `energy_balance_group` groups), the
  `rpm`-instead-of-`frequency` deprecated keys, the specification
  save/restore mechanism, the fitting helpers (`fit_EN12900*`,
  `generate_eta_polys_*`, `swept_volume_from_displacement` — the last one is
  written out as `V_swept = V_dot_ref/f_ref`), the pump/turbine components of
  the notebook and its frequency-interpolating subclass (a separate
  `eta_s_poly(frequency)` layer: with three frequency maps the user supplies
  three coefficient sets).
- **Level**: the taxonomy score of this model is 3 (152 equations → 1,
  largest block 1 → 0, one `FUNCTION` → 1, semi-empirical calibration →
  1, no curated guesses → 0), i.e. level 2; it is rated **level 3** because it
  is an off-design semi-empirical catalogue map used in engineering practice
  (taxonomy §3 allows ±1 with a justification).
- **Diagram support**: block of 8 post-processing equations (state arrays
  `P[i]`, `h[i]`, `T[i]`, `s[i]` of the suction and the discharge state of
  point 1) added at the end of the model for the CoolSolve diagrams; the
  results of the model are unchanged.

## Limitations and CoolSolve gaps

- **No CoolSolve gap encountered**: the model uses only property calls
  (`p_sat`, `t_sat`, `enthalpy`, `entropy`, `volume`, `temperature`), one
  `FUNCTION`, one `DUPLICATE` loop and arithmetic; it solves without guesses.
- **Validity range**: the polynomials must only be evaluated inside the range
  of the catalogue they were fitted on (here -10 to 10 °C evaporation and 30 to
  50 °C condensation, the Bitzer map of the notebook adds 60 °C at 50 and
  90 Hz). Outside it they extrapolate unphysically (eta_v > 1 at 67.5 °C, see
  *Verification*). The source warns about the fit quality (2 % deviation) but
  not about extrapolation; both callers should check the range.
- The map is **frequency dependent** in reality (the notebook fits one map per
  frequency). This model takes one coefficient set at a time, as the source
  component does; a frequency sweep of the model is a parametric study over
  `f`, and the frequency-dependent variant is a subclass in the source.
- The dissipation ratio is a constant input (0.05 in the docstring examples);
  the source has no part-load or motor-loss model, and the notebook removes an
  assumed 2.5 % motor loss from the catalogue power *before* the fit.
- The least-squares fit of a catalogue is data preparation and cannot be
  reproduced inside an EES steady-state model (see *Model*).

## Related models

- `CSL-0123` *copeland_catalogue_correlation*: the other catalogue polynomial
  of the library — the ARI/Copeland third-order power/mass-flow polynomial of a
  scroll compressor catalogue, with the five catalogue tables. Same ten
  monomials, Fahrenheit instead of Celsius, power and mass flow instead of the
  two efficiencies; see the cross-check above.
- `CSL-0007` *scroll_compressor_semi_empirical*: a semi-empirical scroll
  compressor model at a different level of detail (clearance volume and
  leakage instead of a catalogue map).
- `CSL-0001` *refrigeration_cycle_simple_compressor*: the same compressor
  concept (volumetric efficiency, constant losses) closing an R22 cycle, at
  level 1 and without a catalogue map.
- `CSL-0135` *turbine_stodola_offdesign*: the other off-design component of the
  same TESPy snapshot (`Turbine`, cone law); together they are the off-design
  pair of the translation batch.
- Off-design follow-up not in the library yet: the frequency-interpolating
  subclass and the heat-pump part-load notebook that uses the Bitzer SP-111-1
  map.
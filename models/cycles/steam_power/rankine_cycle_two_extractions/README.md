# Rankine cycle with two extractions and closed feedwater heaters (TESPy)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0143`

## Description

Regenerative steam power plant of the TESPy optimisation tutorial: 200 kg/s of
live steam (100 bar, 650 °C) expand through HP, MP and LP turbines
(isentropic efficiency 0.9). Two extractions (20 bar and 3 bar) preheat the
feedwater in two **closed** feedwater heaters (upper terminal temperature
difference `ttd_u` = 5 K), each followed by a **drain pump** returning the
condensate to the feedwater line; the first extraction is cooled in a
**desuperheater** before the second heater and leaves it as saturated vapour.
The condenser is cooled by water from 20 °C to 28 °C (3 bar, 1 % pressure
drop) with a 5 K upper terminal temperature difference, which sets the
condensation pressure (≈ 0.0504 bar). The steam generator has a pressure
ratio of 0.92; the pumps have an isentropic efficiency of 0.8.

The model returns the extraction, drain and cooling-water flows, the component
powers and the plant thermal efficiency.

The original tutorial maximises the efficiency over the two extraction
pressures with a pymoo differential-evolution optimiser. CoolSolve has no
optimiser (`CS-GAP-OPTIM`); per the card decision the model is shipped at the
design point `p_2` = 20 bar, `p_4` = 3 bar as a steady model, and the
optimisation is replaced by a **2-D sweep** (below).

## Results (design point, CoolSolve vs re-run TESPy source)

| Quantity | CoolSolve | TESPy (re-run) | rel. diff. |
|---|---|---|---|
| Extraction 1 flow `m_21` | 30.0984 kg/s | 30.0984 kg/s | 1e-11 |
| Extraction 2 flow `m_31` | 25.2298 kg/s | 25.2298 kg/s | 2e-10 |
| Condensate flow `m_5` | 144.672 kg/s | 144.672 kg/s | 4e-11 |
| Cooling-water flow `m_cw` | 9210.4 kg/s | 9228.6 kg/s | **2.0e-3** (1) |
| Turbine powers `W_hpt`/`W_mpt`/`W_lpt` | 100.460 / 71.080 / 80.982 MW | same | ≤ 1.3e-9 |
| Pump powers `W_pu1`/`W_pu2`/`W_pu3` | 2.031 / 0.392 / 0.364 MW | same | ≤ 2e-10 |
| Heat rates `Q_sg`/`Q_con` | 557.802 / 308.068 MW | same | ≤ 2.1e-10 |
| Net power `P_grid` | 249.734 MW | 249.734 MW | 2.5e-10 |
| Thermal efficiency `eta_th` | 0.4477110 | 0.4477110 | 2.5e-10 |

(1) The cooling water is `INCOMP::Water` in TESPy and `Water` (IAPWS-IF97) in
CoolSolve; the liquid enthalpy difference between the two models differs by
0.2 % over the 8 K rise, so the required cooling-water flow differs by the
same amount. All other variables agree to ≤ 2e-9 relative (both sides use
CoolProp HEOS water; TESPy snapshot commit 19425523, CoolProp 8.0.0 in the
verification environment).

## Source and attribution

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
the SamplePlant model from TESPy, file tutorial/advanced/optimization_example.py, commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve, design point at the given extraction
pressures (20 / 3 bar), pymoo optimisation replaced by a documented 2-D sweep.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python",
J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
```

Authors: Francesco Witte (TESPy lead developer) and the TESPy contributors.
Local snapshot: `~/git/tespy` (commit `19425523`, version 0.11.3.dev0).

## Translation notes (Python solver plumbing → simultaneous equations)

- TESPy connection variables `(m, p, h)` become named variables `m_<n>`, `p_<n>`,
  `h_<n>` with `<n>` = the connection label of the tutorial (states 1–13, 21–24,
  31–33, 41–42); `T` and `s` come from CoolProp property calls.
- The `CycleCloser` disappears: the SG pressure ratio and the loop closure give
  `p_13 = p_1/pr_sg`; the mass closure `m_13 = m_1` is implied by the mass
  balances of the splitters and merges and is not written.
- Splitters are isenthalpic with no pressure drop (`h_21 = h_2`, `p_21 = p_2`,
  …), as in the original. Merges are adiabatic mixtures: mass sum, equal
  pressure, `m_a*h_a + m_b*h_b = m_c*h_c`.
- Turbines: `h_in - h_out = eta_s_t*(h_in - h_out_s)` with
  `h_out_s = enthalpy(Water, s = s_in, P = p_out)`; pumps:
  `eta_s_p*(h_out - h_in) = h_out_s - h_in`.
- The TESPy `Condenser` model is used for the condenser **and** both feedwater
  heaters: hot outlet saturated liquid (`h = enthalpy(Water, P = p, x = 0)`),
  `ttd_u` referred to the **dew temperature at the hot inlet pressure**
  (`T_9 = T_sat(p_31) - ttd_u`, `T_11 = T_sat(p_22) - ttd_u`,
  `p_6 = pressure(Water, T = T_cw_out + ttd_u, x = 0)`), and pressure ratios
  `pr1`, `pr2`.
- The TESPy `Desuperheater` cools the hot gas **to the saturated vapour state**:
  its `saturated_gas` equation `h_22 = enthalpy(Water, P = p_22, x = 1)` is
  part of the model (it closes the mass-flow system: without it the two
  extraction flows have one degree of freedom left).
- The `INCOMP::Water` cooling water is replaced by the real-fluid `Water`
  (CoolSolve has no incompressible library); see the note in *Results*.
- The power bus is the sum `P_grid = W_hpt + W_mpt + W_lpt - W_pu1 - W_pu2 - W_pu3`.

## Verification

The TESPy source model (`SamplePlant`, the base plant of
`tutorial/advanced/optimization_example.py`, unmodified) was re-run in a
throw-away virtual environment (`work/tsp040/`, pip install of the local
snapshot, Python 3.12, tespy 0.11.3.dev0, CoolProp 8.0.0) at the design
extraction pressures; the design solve of the tutorial (`ttd_u` = 5 K on the
condenser, condenser pressure released) is the reference
(`nw.print_results()` + full-precision `nw.results` dump). Comparison script
over 38 common variables (mass flows, pressures, enthalpies, temperatures,
component powers, heat rates, efficiency): maximum relative deviation
**2.0e-3** on `m_cw` (property-model difference (1) above), **≤ 1.3e-9** on
all steam-cycle variables. Mass and energy balances of the CoolSolve solution
close to ≤ 7e-7 absolute (residuals of 1e8-sized terms). The model also
converges from default guesses (267 iterations); the committed `.initials`
come from the TESPy reference and speed it up (71 iterations).

## Sweep instead of the pymoo optimisation

The tutorial maximises `eta_th` over `p_2`, `p_4` ∈ [1, 40] bar with
`p_2 ≥ p_4` (differential evolution, pymoo). In CoolSolve: *Parametric* tab →
two-dimensional parametric study with `p_2` and `p_4` as parameters
(e.g. 1–40 bar in 1–5 bar steps, `p_2 ≥ p_4`), and plot `eta_th` over the two
parameters. As a sweep end-point check, both models were also solved at
`p_2` = 10 bar, `p_4` = 2 bar: `eta_th` = 0.4445680 on both sides (relative
difference 3e-11), lower than the design point 0.4477110 at 20/3 bar — the
sweep landscape is reproducible by the GUI parametric study; the committed
baseline is the design point.

## Level justification

154 equations (score 1), largest algebraic block 16 (1), arrays for the state
points (1), more than three coupled components (1), no off-design/semi-empirical
physics (0), converges from default guesses (0): score 4 → **level 3**.

## Related models

- `CSL-0029` `rankine_cycle_regenerative_extraction`: same steam plant family
  with a single extraction to an open feedwater heater (level 2).
- `CSL-0013` `heat_pump_basic_tespy`: first TESPy translation (pilot).

## Figure

![Placeholder: T-s diagram of the cycle (maintainer)](figures/rankine_cycle_two_extractions_ts.png)
State points for the diagram overlay are provided as arrays `P[i]`, `h[i]`,
`T[i]`, `s[i]`, `i` = 1…13 (main cycle path; the extraction/drain states 21–24
and 31–33 are available as named variables).

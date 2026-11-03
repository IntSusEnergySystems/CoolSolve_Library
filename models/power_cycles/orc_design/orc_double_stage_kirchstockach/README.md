# Double-stage (HT + LT series) ORC power plant Kirchstockach, design point

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0252`

Design-point model of the 5.5 MWe Kirchstockach geothermal power plant: two
R245fa Organic Rankine cycles (high-temperature and low-temperature) in series
on the geothermal brine, each with a preheating train, a constant-entropy-
efficiency turbine and an air-cooled condenser sized by an imposed pinch. The
translation of the TESPy notebook into simultaneous equations reproduces the
notebook's design point to less than 0.0001 %.

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R245fa (both cycles), Water (brine), Air (condenser cooling air) |
| **Size** | 167 equations, largest algebraic block 23 |
| **Source** | KCORC summer school, TESPy workshop notebook `tespy/ORC_offdesign/complete_ORC.ipynb` (github.com/fwitte/KCORC_summer_school) |
| **Authors** | Francesco Witte, Amalia Steinhauer (TESPy notebook) |
| **License** | No LICENSE file in the original repository (README: shared for educational use); credited and linked, licence to be confirmed by the maintainer |
| **CoolSolve** | 0.4.0 — verified against a re-run of the notebook (see *Verification*) |

## Problem statement

The geothermal brine (122.4 kg/s, 135.1 °C, 10 bar) gives heat first to the HT
cycle (evaporator + high-temperature preheater), then to the LT cycle
(evaporator); downstream of the LT evaporator (70.4 °C) the brine is split
between the LT preheater (54.5 kg/s) and the low-temperature preheater of the
HT cycle (67.9 kg/s), and the branches mix before reinjection (~51.8 °C). Both
cycles expand saturated vapour (HT 13.85 bar, LT 5.97 bar) into air-cooled
condensers (air 8.67 → 15 °C) with an imposed pinch (10.5 K / 11.5 K) and
subcooled outlets. Turbine and pump isentropic efficiencies: 0.883/0.52 (HT),
0.827/0.50 (LT) — pump efficiencies "calculated from design data" in the
paper; generators and motors have efficiency 1. The model computes the state
points 01–10a of both cycles, the brine path, the mass flows, the gross (5468.6
kW) and net (5197.2 kW) power and the second-law efficiencies.

## Model

Each refrigerant loop is a set of simultaneous equations: imposed pressure
drops per preheating section (3 × 1.39/3 bar HT, 0.78 bar LT), `td_bubble`-type
subcooling conditions (2 K at the condenser outlet of the HT cycle, 2.5 K at
the preheater outlet, 3 K / 2 K in the LT cycle), saturated-vapour turbine
supplies, and energy balances between brine and refrigerant duties. The
condensers are written as three sections (desuperheating, condensing,
subcooling) with the air heated step by step; the pinch condition
`T_sat = T_air(dew-point boundary) + td_pinch` closes the condensation
pressure. The brine branch split and the adiabatic mixing close the
geothermal path.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| brine m / T / p | 122.4 kg/s / 135.1 °C / 10 bar | m_HT / m_LT | 110.47 / 70.09 kg/s |
| T_C (LT evaporator inlet) | 92.95 °C | condensation pressures | 1.485 / 1.553 bar |
| T_D1 (LT evaporator outlet) | 70.4 °C | gross power | 5468.6 kW |
| m_D2 / T_G (LHT branch) | 67.9 kg/s / 51.66 °C | net power (grid) | 5197.2 kW |
| air in / out | 8.67 / 15 °C | HT / LT feed pump power | 217.2 / 54.2 kW |
| pinches HT / LT condenser | 10.5 / 11.5 K | η_II gross / net (Table 3 exergy) | 53.78 / 51.11 % |

The exergy reference of Heberle et al. (Table 3: 5309.64 kW gross at
η_II,gross = 52.22 %) implies a brine exergy flow of 10 167.8 kW; the model
also computes its own reference-state exergy flow (11 446.1 kW, giving
47.78 % / 45.41 %) — the two differ because the paper's ambient/exergy
reference is not fully specified in the notebook; the notebook therefore
validates against the Table-3-implied value.

## How to run

```bash
coolsolve ./orc_double_stage_kirchstockach.eescode
```

The `.initials` file carries reference-based guesses (the largest algebraic
block is 23 variables; from CoolSolve's default guess of 1.0 the condenser
blocks do not converge). The state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`
(i = 1…6 HT cycle, 7…11 LT cycle) follow the connection labels of the
notebook (01…05a, 07…10a) for the CoolSolve diagram overlay. The notebook's
Figure-6 parametric sweep (LHT mass flow 30–90 kg/s, regime switch between a
fixed T_G and a 3 K preheater pinch) is a parametric study of this model and
is not part of the file.

## Results (design point)

| Quantity | Heberle 2015 Table 3 | TESPy notebook re-run | CoolSolve |
|---|---:|---:|---:|
| T_01 / T_02 [°C] | 22.81 / 24.01 | 22.977 / 24.160 | 22.977 / 24.160 |
| p_02 [bar] | 15.24 | 15.24 | 15.24 |
| T_03 / T_04 / T_05 [°C] | 60.23 / 103.16 / 104.23 | 59.721 / 103.137 / 104.120 | 59.721 / 103.137 / 104.120 |
| T_05a [°C] | 47.70 | 44.032 | 44.032 |
| m_HT [kg/s] | 109.61 | 110.471 | 110.471 |
| T_07 / T_08 / T_09 / T_10 [°C] | 23.03 / 23.51 / 67.37 / 69.37 | 23.164 / 23.635 / 67.235 / 69.235 | 23.164 / 23.635 / 67.235 / 69.235 |
| p_10 [bar] | 5.97 | 5.97 | 5.97 |
| T_10a [°C] | 40.02 | 38.073 | 38.073 |
| m_LT [kg/s] | 69.72 | 70.086 | 70.086 |
| T_B / T_F / T_H [°C] | 106.96 / 52.13 / 51.87 | 106.834 / 52.040 / 51.829 | 106.834 / 52.040 / 51.829 |
| gross power [kW] | 5309.64 | 5468.63 | 5468.63 |
| HT / LT feed pump [kW] | 226.21 / 59.76 | 217.20 / 54.22 | 217.20 / 54.22 |
| η_II gross / net [%] (Table 3 exergy) | 52.22 / 49.41 | 53.78 / 51.11 | 53.78 / 51.11 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s or P-h overlay of the
     two cycles (arrays i = 1…11), figures/orc_double_stage_kirchstockach_ts.png -->

## Verification

The source notebook was re-run headless in a throw-away venv (TESPy 0.11.3,
CoolProp, commit `85a2362b` of the repository) and its design-point results
were compared with the CoolSolve solution: all 27 quantities of the notebook's
own validation table (state-point temperatures, pressures, both mass flows,
brine temperatures, gross/net power, pump powers, second-law efficiencies)
agree within **0.000002 %** (worst relative deviation 1.9·10⁻⁸ on `T_07`:
same CoolProp property backend, the differences are solver round-off). The
air mass flows (3666.2 / 2260.8 kg/s, worst 1.1·10⁻⁶ relative), the brine
exergy flow and the net power agree as well. The remaining differences to Heberle et
al. Table 3 (gross power 5468.6 vs 5309.6 kW, +3.0 %) are those of the
notebook itself (CoolProp vs the paper's property backend, pinch location at
the dew-point boundary instead of a constant condensation temperature); the
notebook documents them and fixes them as the reference for this
translation.

## Source and attribution

TESPy workshop notebook `tespy/ORC_offdesign/complete_ORC.ipynb` of the KCORC
summer school by **Francesco Witte** and **Amalia Steinhauer**:
https://github.com/fwitte/KCORC_summer_school (commit `85a2362b`). The
underlying plant data and reference results are from F. Heberle, Th. Jahrfeld,
D. Brüggemann, *Modelling and simulation of a double-stage Organic Rankine
Cycle power plant at Kirchstockach*, Proceedings World Geothermal Congress
2015 (paper 26002, PDF shipped as `tespy/ORC_design/Heberle.pdf` in the
repository). The repository has **no LICENSE file**; its README presents the
material as shared for educational use — the translation credits the authors
and links the repository; the licence situation is to be confirmed by the
maintainer.

## Conversion log

- **2026-10-22 — translation** (`T-TRANSLATE`, card C-279 / LDS-005): the
  TESPy `Network`/`SectionedHeatExchanger` physics was rewritten as
  simultaneous equations; the solver glue, plotting and the Figure-6 sweep
  loops of the notebook disappear. The `CycleCloser`, `Splitter`, `Merge` and
  the power bus (generator/motor efficiency 1) become direct equations. Fluid
  names: CoolProp `'R245fa'` and `'water'` keep their names, CoolProp `'air'`
  becomes the EES ideal-gas `Air` (differences in the liquid-like reference
  state have no effect: only enthalpy differences of the air enter the
  balances; air mass flows agree with the notebook to < 0.01 %). The
  `td_pinch` design condition (minimum approach over the exchanger sections =
  10.5 / 11.5 K) is written at its binding section boundary, the dew point
  (`T_sat = T_air_x1 + td_pinch`); the other section-boundary approaches are
  kept as output checks (HT: 16.23 / 14.31 / 29.03 K; LT: 17.37 / 14.49 /
  23.07 K — all above the pinch, confirming the binding location; TESPy's own
  section output of the re-run shows exactly 10.500 K / 11.500 K at the dew
  point). Writing the pinch with a `MIN(...)` over the four candidate
  approaches also describes the same physics and converges in simpler models
  (pattern `CSL-0133`), but in this model CoolSolve's tearing assigned the
  weakly pressure-sensitive liquid enthalpy inversion to the condensation
  pressure and the block stalled near the solution; the dew-point form is the
  same equation at the solution and is used here instead.
- **Unit system**: the notebook works in TESPy default units (bar, °C,
  kJ/kg, kg/s, kW); all values were converted by hand to Pa, J, W (e.g.
  `p_05 = 13.85E5 [Pa] "13.85 bar"`).
- **Level** (taxonomy.md §3): equations 167 (1), largest block 23 (2),
  arrays present (1), ≥ 3 coupled components (1), curated guesses needed (1)
  = 6 → level 3.

## Limitations

- Design point only: the notebook's off-design study (turbine
  characteristics, Figure-6 sweep) is not translated; the sweep can be
  reproduced as a CoolSolve parametric study on `m_D2` with the two regime
  closures described in the notebook.
- The exergy reference of the paper (ambient state, chemical exergy of the
  brine) is not fully specified in the notebook; both efficiencies (own and
  Table-3-implied reference) are computed.
- `Air` is the ideal-gas substance of EES, while the notebook uses CoolProp's
  pseudo-pure `air`; at 1 bar the enthalpy differences agree to < 0.1 %, which
  is confirmed by the identical air mass flows.

## Related models

- `CSL-0133` *heat_pump_propane_pinch*: pinch-sized condenser/evaporator with
  the `MIN`-based pinch condition; single-stage cycle.
- `CSL-0014` *hx_constant_pinch*: the pinch HX component pattern (three
  zones, `MIN` over the candidate approaches).
- `CSL-0019` *orc_simple_r245fa*, `CSL-0040` *orc_biomass_chp*,
  `CSL-0134` *orc_preheated_recuperated_cyclopentane*: single-loop ORCs of
  the library; this is the only two-stage series ORC on one heat source.

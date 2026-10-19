# Heating coil RefSim model, epsilon-NTU

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0164`

Reference simulation of a hot-water air heating coil from the ULiège model
bank. The coil is a counter-flow exchanger: the heating duty follows the
epsilon-NTU relation, and the overall conductance is the series of the
air-side, metal and water-side resistances. The air-side resistance scales
with the air flow to the power −0.6 (laminar) and the water-side resistance
with the water flow to the power −0.8 (turbulent). Heating does not change
the humidity ratio. It is the heating-coil counterpart of the cooling-coil
RefSim model `CSL-0074`.

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Air handling |
| **Fluids** | AirH2O, Water |
| **Size** | 43 equations (largest block: 24) |
| **Source** | ULiège model bank, heating coil reference simulation model (2008-03-17) |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | native file runs (11 iterations with the shipped `.initials`); verified (see *Verification*) |

## Problem statement

Given the supply state and the volume flow rate of the air and of the hot
water, and the three nominal thermal resistances, compute the heating duty,
the exhaust temperatures and the air and water pressure drops. The nominal
resistances and the nominal pressure drops are scaled to the actual flow
rates, so the same coil can be evaluated off its nominal point.

## Model

- Air and water capacity rates `C_dot = M_dot·c_p`, with the mass flow rates
  from the volume flow rates and the densities. Humid-air properties
  (`humrat`, `cp`, `density`, `relhum`) are evaluated at the mean air
  temperature; water properties at the mean water temperature.
- Counter-flow effectiveness, as in the original:

  `epsilon = (1 − exp(−NTU·(1 − ω))) / (1 − ω·exp(−NTU·(1 − ω)))`

  with `NTU = AU/C_min` and `ω = C_min/C_max`.
- Overall resistance `R_tot = R_a + R_m + R_w = 1/AU`, with

  `R_a = R_a_n·(M_dot_a_n/M_dot_a)^0.6`, `R_m = R_m_n`,
  `R_w = R_w_n·(M_dot_w_n/M_dot_w)^0.8`.
- Pressure drops: water `Δp_w = Δp_w_n·(M_dot_w/M_dot_w_n)^2` (turbulent),
  air `Δp_a = Δp_a_n·(M_dot_a/M_dot_a_n)` (laminar).
- The exhaust humidity ratio equals the supply humidity ratio.

| Inputs (default run, stored solution) | Value | Parameters | Value |
|---|---|---|---|
| `V_dot_a_m3h` air volume flow | 5000 m³/h | `V_dot_a_m3h_n` nominal air flow | 5000 m³/h |
| `t_a_su_heatingcoil` air supply temperature | −10 °C | `R_a_heatingcoil_n` nominal air-side resistance | 3·10⁻⁴ K/W |
| `RH_su_heatingcoil` air supply relative humidity | 0.9 | `R_m_heatingcoil_n` metal resistance | 3·10⁻⁵ K/W |
| `P_atm` atmospheric pressure | 100 000 Pa | `R_w_heatingcoil_n` nominal water-side resistance | 3·10⁻⁴ K/W |
| `V_dot_w_heatingcoil_m3h` water volume flow | 3.7 m³/h | `DELTAp_a_heatingcoil_n` nominal air pressure drop | 100 Pa |
| `t_w_su_heatingcoil` water supply temperature | 80 °C | `DELTAp_w_heatingcoil_n` nominal water pressure drop | 30 000 Pa |
| | | `V_dot_w_heatingcoil_m3h_n` nominal water flow | 4 m³/h |

In the original these thirteen variables are quoted strings in the equations
window (the Diagram window holds the values), so the extraction is not
square. Each is given its **stored** value as an equation. The stored run is
the file's default operating point and is kept as the regression case. The
equation-window string for the nominal water flow says 3.7 m³/h; the stored
run used 4 m³/h, and 4 m³/h is kept.

## How to run

```bash
coolsolve ./heating_coil_refsim.eescode
```

The model needs `heating_coil_refsim.initials` (the EES stored values). Without
it the 24-variable block stops with *SingularJacobian* (residual 4183). With the
shipped guesses it converges in 11 iterations.

## Results

Default operating point of the stored run. The EES column is the
stored solution.

| Quantity | CoolSolve | EES |
|---|---:|---:|
| Heating duty `Q_dot_heatingcoil` | 83 381.3 W | 83 381.8 W |
| Air exhaust temperature `t_a_ex_heatingcoil` | 39.26 °C | 39.25 °C |
| Water exhaust temperature `t_w_ex_heatingcoil` | 60.20 °C | 60.18 °C |
| Exhaust relative humidity `RH_ex_heatingcoil` | 0.03294 | 0.03299 |
| Effectiveness `epsilon_heatingcoil` | 0.5473 | 0.5472 |
| Overall conductance `AU_heatingcoil` | 1540.1 W/K | 1540.1 W/K |
| Air mass flow `M_dot_a_heatingcoil` | 1.6781 kg/s | 1.6775 kg/s |
| Water mass flow `M_dot_w_heatingcoil` | 1.0049 kg/s | 1.0049 kg/s |
| Air pressure drop `DELTAp_a_heatingcoil` | 100 Pa | 100 Pa |
| Water pressure drop `DELTAp_w_heatingcoil` | 25 669 Pa | 25 669 Pa |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against the 48 variables decoded from the EES file:

> 43 common variables, 3 differ (rtol=0.001); only in EES: 5; only in CoolSolve: 0

The three differences, quoted as printed:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `w_su_heatingcoil` | 0.0014583 | 0.00146432 | 4.11e-03 |
| `w_ex_heatingcoil` | 0.0014583 | 0.00146432 | 4.11e-03 |
| `RH_ex_heatingcoil` | 0.0329894 | 0.0329374 | 1.58e-03 |

Maximum relative difference **4.11e-03**, on the humidity ratio. The exhaust
humidity is set equal to the supply humidity, so the two humidity ratios are
one property difference: `humrat(AirH2O)` of CoolProp against the EES
psychrometric formulation, of the same size as in `CSL-0070` (4.4e-03) and
`CSL-0016` (5.1e-03). `RH_ex` is `relhum` at the exhaust and follows from it.
At rtol = 1e-4, 19 variables differ; the largest after the humidity ratio are
`omega_heatingcoil` 9.93e-04 and `c_p_w_heatingcoil` 7.84e-04 (water specific
heat, EES against CoolProp). The duty, the conductance and both pressure
drops stay within 1e-4. The humid-air density, `Density(AirH2O, …)` = `1/Volume`
per kg of dry air as in EES, is 1.20826 kg/m³ against the stored 1.20782 kg/m³
(3.62e-04).

Five decoded names are not variables of the model: `a`, `b`, `c`,
`M_dot_w_hotwater` and `W_dot_pump`. They appear in the variable records and
in the output list of the equations window, but no equation defines them
(leftovers of the Diagram window; the binary also keeps names of a
preheating-coil pump that this file does not compute).

## Source and attribution

Stéphane Bertagnolio, University of Liège, Faculty of Applied Sciences,
Thermodynamics Laboratory, 17 March 2008. The file header gives the contact
`stephane.bertagnolio@ulg.ac.be` and the laboratory website of 2008. The
equations window carries the laboratory disclaimer: freely distributed, may
not be sold, cite the origin. EES licence stamp: Jean Lebrun, Laboratoire de
Thermodynamique, Université de Liège (`{$ID$ #1206}`), EES X7.888.

Source:
`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Heating_Coil/HeatingCoil_REFSIM_MODEL_SB080317.zip!/HEATINGCOIL_REFSIM_EES_MODEL_SB080317.EES`
(inventory `TM-0474`, duplicate group `DG-0114`).

The parameter-identification companion of the same folder (`TM-0473`) is a
different model and stays in the backlog.

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py` on the zip member): unit
  system already `SI MASS DEG PA C J`, so no unit conversion; the
  `$UnitSystem` line was removed; no lookup or parametric table; licence tag
  removed. `AIRH2O` written as `AirH2O` (EES fluid names are
  case-insensitive). The header was replaced by the standard one. Comments
  paraphrase the original; the original heading "Chilled water side" is kept
  as a note on the water-side block.
- **Diagram-window inputs restored as equations.** Thirteen inputs and
  parameters are quoted strings in the equations window. Each is assigned its
  stored value, which makes the model square (43 equations, 43 variables).
  Nominal water flow: the string says 3.7 m³/h, the stored value is 4 m³/h;
  the stored value is kept.
- **Level**: 43 equations (0), largest block 24 (1), no procedure or array
  (0), one component (0), flow-scaled resistances, off-design (1), curated
  guesses required (1) → score 3 → level 2.

## Limitations and CoolSolve gaps

The coil is a single counter-flow zone with constant humidity. The three
resistances and the two pressure-drop exponents are hypotheses of the
original (laminar air side, turbulent water side), not identified from
measurements. The nominal water flow of the stored run (4 m³/h) is not the
3.7 m³/h written in the equations window.

## Related models

- `CSL-0074` *cooling_coil_refsim*: the cooling and dehumidifying coil of the
  same model bank (dry and wet regimes, BrineProp). This model is the
  heating-coil RefSim of the same collection.

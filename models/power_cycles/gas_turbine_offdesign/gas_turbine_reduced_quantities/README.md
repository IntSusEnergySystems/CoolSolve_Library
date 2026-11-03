# Gas turbine regime linked by reduced flow and reduced speed

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0200`

Steady exercise of a single-shaft gas turbine burning methane in air. The nominal reduced mass flow and reduced speed are given. One other regime, at 50 000 rpm and the same inlet state, is tied to that nominal point by a compressor law (reduced flow proportional to reduced speed) and by a single expander characteristic.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air, CH4 (equation window). The copied `cpbar` and `gamma` routines also call CO2, CO, H2O, N2 and O2 |
| **Size** | 58 equations after analysis (largest block: 19). 50 equation lines in the main program |
| **Source** | ULiège MSTh repetition R9, exercise 1 |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@f5b79cd — verified against the EES stored solution |

## Problem statement

A single-shaft gas turbine runs on air with methane (CH4, written `m_f = 1`, `n_f = 4`) as fuel. The isentropic efficiencies of the compressor and of the expander are 0.87. The inlet state is 15 °C and 10^5 Pa. The turbine inlet temperature is 950 °C. The lower heating value is 5×10^7 J/kg. The combustor energy balance is written per kilogram of air, with the air, the fuel and the products counted from 25 °C, and with `q_4 = 0`. The expander discharges at the inlet pressure (`P_4 = P_1`, `P_3 = P_2`).

The nominal regime is given by its reduced quantities, not by a second solved point:

| | |
|---|---|
| `MR_c_n` | 69.13 kg·K^0.5/s |
| `MR_e_n` | 18.1 kg·K^0.5/s |
| `NR_n` | 9.821 1/(s·K^0.5) |

`NR_n` is the reduced speed at 10 000 rpm and 15 °C. The diagram text of the file says that the nominal speed was 10 000 rpm. The equation window leaves `rpm = 10000`, `r_p_c = 8` and `W_dot_sh = 1E6` commented.

This solved regime is at **50 000 rpm**. It is linked to the nominal point by

\[
MR_c = MR_{c,n}\,\frac{NR}{NR_n}, \qquad MR_e = MR_{e,n}
\]

with

\[
NR = \frac{N}{\sqrt{T_1+273}}, \quad
MR_c = \frac{\dot m_a\sqrt{T_1+273}}{P_1/10^5}, \quad
MR_e = \frac{\dot m_p\sqrt{T_3+273}}{P_3/10^5}.
\]

The `+273` is the conversion written in the equation window. Find the pressure ratio, the shaft power, the efficiency and the reduced flow and speed of this regime.

## Model

Compressor: isentropic efficiency on the air enthalpies (`ENTHALPY` / `ENTROPY` / `TEMPERATURE` of `Air`).

Combustor, per kilogram of air, temperatures in °C:

\[
q_1+q_2+q_3+q_4+q_5 = 0
\]

\[
q_1 = c_{p,a}(T_{ref}-T_2),\quad
q_2 = f\,c_{p,f}(T_{ref}-T_1),\quad
q_3 = -f\,\mathrm{LHV},\quad
q_4 = 0,\quad
q_5 = (1+f)\,c_{p,p}(T_3-T_{ref}).
\]

`c_{p,a}` and `c_{p,f}` are `CP(Air)` and `CP(CH4)` at the mid-interval temperature. `c_{p,p}` and the expander `c_{p,p,e}` are the mean specific heats of the products from `cpbar` (CSL-0005, copied). The ratio of specific heats `gamma_e` is the `gamma` function of the same library. The isentropic expansion is

\[
\frac{T_{4s}+273}{T_3+273} = \left(\frac{P_4}{P_3}\right)^{(\gamma_e-1)/\gamma_e}, \qquad
\epsilon_{s,e} = \frac{T_3-T_4}{T_3-T_{4s}}.
\]

Shaft power: `W_dot_sh = M_dot_a * w_sh` with `w_sh = (1+f)*w_e - w_cp`. Efficiency: `eta = W_dot_sh / (M_dot_f * LHV_f)`.

| Inputs | Outputs |
|---|---|
| `T_1`, `P_1`, `T_3_max`, `epsilon_s_c`, `epsilon_s_e`, `LHV_f`, `rpm` | `W_dot_sh`, `eta`, `r_p_c` |
| `MR_c_n`, `MR_e_n`, `NR_n`, `m_f`, `n_f` | `MR_c`, `MR_e`, `NR`, `M_dot_a`, `f` |

## How to run

From this folder, with the shipped `.initials` beside the file:

```bash
coolsolve ./gas_turbine_reduced_quantities.eescode
```

The `.initials` file is the EES stored solution. It selects the physical expansion (`T_4` about 307 °C, `T_4_s` about 211 °C, both below `T_3`). With those guesses the solve takes **11 iterations**. Without `.initials` the block `gamma_e`, `T_4`, `T_4_s` stops in a line search (iteration 12 of that block) and the model does not converge.

## Results

| Quantity | EES stored | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `W_dot_sh` [W] | 2.728374×10^6 | 2.652475×10^6 | 2.78×10^−2 |
| `eta` [-] | 0.301440 | 0.295655 | 1.92×10^−2 |
| `MR_c` [kg·K^0.5/s] | 345.64745 | 345.64745 | 1.3×10^−10 |
| `MR_e` [kg·K^0.5/s] | 18.1 | 18.1 | 0 |
| `NR` [1/(s·K^0.5)] | 49.104638 | 49.104638 | 4.9×10^−11 |
| `r_p_c` [-] | 39.702208 | 39.699131 | 7.7×10^−5 |
| `h_1` [J/kg] | 288501.31 | 414374.57 | +125873 J/kg |

`T_4` is below `T_3`, the shaft power is positive, and the efficiency is about 0.30. `MR_c / NR` equals `MR_c_n / NR_n`, and `MR_e` equals `MR_e_n`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): ideal-gas air and
     combustion products have no diagram yet (CS-FEAT-DIAGRAM-IDEAL), so the figure
     is a parametric sweep plot, for example efficiency against shaft speed. -->

## Verification

Reference: stored solution in `MSTH-SB-R9-EX1.EES` (EES X7.458, 50 numeric values). Units are already Pa and J, so `compare_solution.py` was run without `--ees-units`. The summary line is:

```
50 common variables, 19 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8
```

`verification.max_rel_diff` is **0.32037**, the relative difference on `s_1` (3849.95 versus 5664.81 J/kg-K). That is the largest gap over all 50 common variables.

**Enthalpy and entropy reference of Air**, reported apart from the power. At the same inlet state (15 °C, 10^5 Pa), `h_1` is **+125873 J/kg** (+125.9 kJ/kg) above the EES value. `s_1` is **−1814.86 J/kg-K** relative to EES. Those two offsets are the ideal-gas reference states. They are not a rescaling of the model.

`h_2` and `h_2_s` are not the same constant. Their gaps above the `h_1` offset are +3203 J/kg and +2787 J/kg, which are the gaps on `w_cp` and `w_cp_s` (`h_2 = h_1 + w_cp`).

**Every other common variable above rtol 0.001:**

| Variable | rel. diff | Why |
|---|---:|---|
| `s_1` | 0.320 | Air entropy reference, same `T_1` and `P_1` |
| `h_1` | 0.304 | Air enthalpy reference, +125873 J/kg |
| `h_2_s` | 0.135 | that reference, plus the isentropic-work gap |
| `h_2` | 0.125 | that reference, plus the compressor-work gap |
| `W_dot_sh`, `w_sh` | 0.0278 | net work: `w_e` agrees to 6.2×10^−4, `w_cp` is 0.52% high, and the difference is a large part of the net |
| `eta` | 0.0192 | power 2.78% low and fuel flow 0.88% low |
| `q_2` | 0.0181 | follows `cp_f` and `f` |
| `cp_f` | 0.00941 | `CP(CH4)` at 20 °C: 2220.6 versus 2241.7 J/kg-K (CoolProp versus the EES ideal-gas methane) |
| `f`, `q_3`, `M_dot_f` | 0.00880 | combustor balance shifts with `q_1` and `cp_f`; `M_dot_a` itself agrees |
| `w_cp`, `w_cp_s` | 0.00519 | compressor enthalpies after the reference offset cancels; `T_2` is 2.42 K higher |
| `q_1` | 0.00515 | follows `T_2` (`cp_a` stays within 9.5×10^−4) |
| `T_2` | 0.00402 | ideal-gas air along the compression, 601.71 °C versus 599.29 °C |
| `T_4_s` | 0.00286 | isentropic expansion, with `gamma_e` within 4.6×10^−4 |
| `T_4` | 0.00171 | expander exit, 306.65 °C versus 307.18 °C |
| `cp_p_e` | 0.00144 | mean specific heat of the products between `T_3` and `T_4` |

`MR_c`, `MR_e`, `NR`, `rpm`, `N` and `M_dot_a` agree within 2×10^−10. `r_p_c` agrees within 7.7×10^−5. The CoolSolve hint that `Air` might be read as moist air was left as `Air`, the fluid named in the equation window. The hint that a temperature argument is in °C matches the equation window, and the reduced quantities agree, so no temperature was rewritten.

The eight names present only in CoolSolve are `Q_4_c`, `x_c`, `e_min_c`, `e_c`, `Q_4_e`, `x_e`, `e_min_e`, `e_e`: the outputs of `cpbar` that the original function-position call did not return.

## Source and attribution

The equation window and the file name are `MSTh - SB - R9 - Exercice 1` / `MSTH-SB-R9-EX1.EES`. They name no person. The filename marks an SB solution. The inventory attributes the course to J. Lebrun, V. Lemort and S. Bertagnolio. The EES licence tag is the Laboratoire de Thermodynamique, Université de Liège, and is not an author. `authors` is therefore `TBD (ULiège MSTh)`.

Source file (EES X7.458, French comments):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 09/MSTH-SB-R9-EX1.EES`
(inventory `TM-0144`).

`cpbar` and `gamma` are copied from CSL-0005 (P. Ngendakumana, ULiège, 2003).

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `MSTH-SB-R9-EX1.EES` (EES X7.458, plain text, 51 variable records, 50 stored numbers, no lookup or parametric table, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, deleted. Values are already in Pa and J; nothing was rescaled. The `+273` factors are the ones in the equation window (not 273.15). No `$Export`, `concat$`, `EESFILEDIR$` or `$TABSTOPS` lines. Comments translated to English. No diagram state arrays: the equation window has none, and the fluids are ideal gases.
- **2026-10-15 — square system**: the equation window has 49 equations and 50 stored variables (`gamma` is an empty record, the name of the library function). CoolSolve on that transcription, before `rpm` is restored: 57 equations, 58 unknowns, `System square: No`. `r_p_c` and `W_dot_sh` sit in the EES calculation order; `rpm` does not (stored value 50 000, guess 10 000, the commented nominal). Restoring `rpm = 50000` from the stored solution makes the system square (58/58). The commented nominal inputs `r_p_c = 8` and `W_dot_sh = 1E6` were not substituted for the solved values.
- **2026-10-15 — `cpbar`**: the original writes `cp_p = cpbar(...)` and `cp_p_e = cpbar(...)` in function position. The library routine is a five-output procedure, so both calls are `CALL` in this file (valid EES, same returned specific heat). `gamma_e = gamma(...)` stays a function call. `PROCEDURE cpbar` and `FUNCTION gamma` are copied from CSL-0005 until `$INCLUDE` exists (`CS-FEAT-IMPORT`). `CS-GAP-INCLUDE` is not a missing feature of this file: the routines are in the file. Not a `_coolsolve` variant.
- **Level**: equations 58 → 1 (50–300); largest block 19 → 1 (6–30); `PROCEDURE` and `FUNCTION` present → 1; compressor, combustor and expander coupled → 1; the solved point is a second regime linked by reduced flow and speed → 1; the expander block needs the shipped initials → 1. Score 6 → level 3 on the grid, moved down by one to **level 2**: MSTh repetition exercise, one steady point, constant efficiencies; the block of 19 is the cycle match, not a discretisation.

## Limitations and CoolSolve gaps

Constant isentropic efficiencies. One shaft and one shaft power; no heat-recovery boiler. Simplified air inside `cpbar` (79 % N2 / 21 % O2). The kelvin conversion in the reduced quantities and in the isentropic expansion is `+273`, as written. Absolute `Air` enthalpy and entropy use the CoolProp reference. No CoolSolve gap blocks the file. `missing_features` is empty.

## Related models

`related` is empty. The gas-turbine models already in this category (open cycle, reheat, two-shaft with a compressor map, turbojet, combined cycle, sCO2) are other calculations. CSL-0005 is the function library copied into this file, not the same turbine exercise.

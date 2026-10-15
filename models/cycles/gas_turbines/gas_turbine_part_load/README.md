# Single-shaft gas turbine at part load

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0218`

Steady exercise of a single-shaft gas turbine burning methane in air. The nominal reduced mass flow and reduced speed are given. One part-load point, at an inlet temperature of 30 °C and 10 000 rpm, is tied to that nominal point by a compressor law (reduced flow proportional to reduced speed) and by a single expander characteristic.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air, CH4 (equation window). The copied `cpbar` and `gamma` routines also call CO2, CO, H2O, N2 and O2 |
| **Size** | 58 equations after analysis (largest block: 19) |
| **Source** | ULiège MSTh repetition R9, exercise 1 continued |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution |

## Problem statement

A single-shaft gas turbine runs on air with methane (CH4, written `m = 1`, `n = 4`) as fuel. The isentropic efficiencies of the compressor and of the expander are 0.87. The inlet pressure is 10^5 Pa. The turbine inlet temperature is 950 °C. The lower heating value is 50×10^6 J/kg. Combustor pressure loss, mechanical losses and auxiliary consumption are neglected. The shaft speed is fixed at 10 000 rpm (`N_rot = 10000/60`).

The combustor energy balance is written in power, with the air enthalpy, the fuel and the products counted from 25 °C. The expander discharges at the inlet pressure (`P_4 = P_1`, `P_3 = P_2`).

The nominal regime is given by its reduced quantities, which the file header comment places at 15 °C. They are data, not a second solved point:

| | |
|---|---|
| `M_dot_R_c_n` | 0.0006582 kg·K^0.5/(s·Pa) |
| `M_dot_R_e_n` | 0.0001742 kg·K^0.5/(s·Pa) |
| `N_R_n` | 9.821 1/(s·K^0.5) |

`N_R_n` equals `(10000/60)/sqrt(15+273)`. This solved point is at an inlet temperature of **30 °C**. The equation window leaves `T_1 = 30`, `r_p_c = 8` and `W_dot_sh = 1E6` in comments (`r_p_c` and `W_dot_sh` change with `T_1`). The two regimes are linked by

\[
M_{R,c} = M_{R,c,n}\,\frac{N_R}{N_{R,n}}, \qquad M_{R,e} = M_{R,e,n}
\]

with

\[
N_R = \frac{N_{rot}}{\sqrt{T_1+273}}, \quad
M_{R,c} = \dot m_a\frac{\sqrt{T_1+273}}{P_1}, \quad
M_{R,e} = \dot m_p\frac{\sqrt{T_3+273}}{P_3}.
\]

The `+273` and the pressure in Pa are the ones written in the equation window. The comment mentions a parametric table on `T_1`. The file stores none. Find the pressure ratio, the shaft power, `eta` and the fuel flow of this point. In the window, `eta = W_dot_sh/W_dot_c`.

## Model

Compressor: isentropic efficiency on the air enthalpies (`enthalpy` / `entropy` of `Air`). `h_2 = enthalpy(Air, T=T_2)`, so the exit temperature is the unknown of that call.

Combustor, temperatures in °C:

\[
\dot Q_1+\dot Q_2+\dot Q_3+\dot Q_4 = 0
\]

\[
\dot Q_1 = \dot m_a(h_{a,2}-h_{a,ref}),\quad
\dot Q_2 = \dot m_f\,c_{p,f}(T_{f,su}-25),\quad
\dot Q_3 = -\dot m_f\,\mathrm{LHV},\quad
\dot Q_4 = \dot m_p\,c_{p,p}(T_3-25).
\]

`h_{a,ref}` is `enthalpy(Air, T=25)`. `c_{p,f}` is `cp(CH4)` at `T_m = (T_{f,su}+T_1)/2`, and `T_{f,su} = T_1`. `c_{p,p}` and the expander `c_{p,p,e}` are the mean specific heats of the products from `cpbar`. The ratio of specific heats `gamma_e` is the `gamma` function of the same routines. The isentropic expansion is

\[
\frac{t_{4s}+273}{T_3+273} = \left(\frac{P_4}{P_3}\right)^{(\gamma_e-1)/\gamma_e}, \qquad
\epsilon_{s,e} = \frac{T_3-T_4}{T_3-t_{4s}}.
\]

Shaft power: `W_dot_sh = w_dot_e - W_dot_c`, with `w_dot_e = M_dot_p*w_e` and `W_dot_c = M_dot_a*w_c`. `eta = W_dot_sh/W_dot_c`, as written. `w_dot_sh_n = 1E6` is assigned and is not used by another equation.

| Inputs | Outputs |
|---|---|
| `T_1`, `P_1`, `T_3`, `epsilon_s_c`, `epsilon_s_e`, `LHV_gn`, `N_rot` | `W_dot_sh`, `eta`, `r_p_c`, `M_dot_f` |
| `M_dot_R_c_n`, `M_dot_R_e_n`, `N_R_n`, `m`, `n` | `M_dot_R_c`, `M_dot_R_e`, `N_R`, `M_dot_a`, `f` |

## How to run

From this folder, with the shipped `.initials` beside the file:

```bash
coolsolve ./gas_turbine_part_load.eescode
```

The `.initials` file is the EES stored solution. It selects the stored root (`r_p_c` about 7.61, `T_2` about 299 °C, `T_4` about 542 °C, both temperatures on the compression and the expansion). With those guesses the solve takes **11 iterations**. Without `.initials` the same equations converge in **36 iterations** to another root: `r_p_c` about 1.60, `T_2` about 80 °C, `T_4` about 839 °C, shaft power about 339 kW and `eta` about 1.82. Use the shipped `.initials`.

## Results

| Quantity | EES stored | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `W_dot_sh` [W] | 897918.66 | 896469.16 | 1.61×10^−3 |
| `eta` [-] | 0.887551 | 0.885124 | 2.73×10^−3 |
| `M_dot_f` [kg/s] | 0.10256767 | 0.10255107 | 1.62×10^−4 |
| `r_p_c` [-] | 7.606619 | 7.606585 | 4.4×10^−6 |
| `M_dot_a` [kg/s] | 3.6864495 | 3.6864495 | 0 |
| `h_1` [J/kg] | 303601.13 | 429468.04 | +125867 J/kg |
| `s_1` [J/kg·K] | 5715.89 | 3901.01 | 0.31751 |

`T_2` is above `T_1` (298.98 °C versus 299.14 °C in EES) and `T_4` is below `T_3` (541.81 °C versus 542.02 °C). The shaft power is positive. `M_dot_R_c / N_R` equals `M_dot_R_c_n / N_R_n`, and `M_dot_R_e` equals `M_dot_R_e_n`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/. Ideal-gas Air has no diagram in CoolSolve, and the file stores no parametric table,
     so this placeholder stays. -->

## Verification

Reference: stored solution in `MSTh R9 Ex 1 - 2.EES` (EES X7.458, 50 numeric values). Units are already Pa, °C and J, so `compare_solution.py` was run without `--ees-units`. The summary line is:

```
50 common variables, 14 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8
```

`verification.max_rel_diff` is **0.31751**, the relative difference on `s_1` (3901.01 versus 5715.89 J/kg·K). That is the largest gap over all 50 common variables. All 58 equations are satisfied (max relative residual 5.0×10^−8).

**Shaft power, efficiency and fuel flow**, apart from the absolute enthalpies. `W_dot_sh` is 896469 W versus 897919 W (1.61×10^−3 low). `eta`, which the window defines as `W_dot_sh/W_dot_c`, is 0.88512 versus 0.88755 (2.73×10^−3 low). `M_dot_f` is 0.102551 kg/s versus 0.102568 kg/s (1.62×10^−4 low), inside the comparison tolerance. `w_dot_e` agrees to 1.6×10^−4. The shaft-power gap is the compressor work that remains after the enthalpy offset cancels: `w_c` is 0.112% high (+308 J/kg), and that increase is subtracted in `W_dot_sh = w_dot_e - W_dot_c`.

**Air enthalpy and entropy.** At the same inlet state (30 °C, 10^5 Pa), `h_1` is **+125867 J/kg** above the EES value. `h_a_ref` (air at 25 °C) is **+125868 J/kg**. The offset is not constant: `h_2` is +126175 J/kg and `h_2_s` is +126135 J/kg. The extras, +308 J/kg and +268 J/kg, are the gaps on `w_c` and `w_c_s`. `s_1` is **−1814.9 J/kg·K** relative to EES.

**Methane specific heat.** `c_p_f = cp(CH4, T=T_m)` at `T_m = 30` °C is 2243.2 J/kg·K in CoolSolve versus 2259.1 J/kg·K in EES (relative difference 7.05×10^−3). `Q_dot_2` follows it (7.21×10^−3). The fuel flow still agrees, as above.

`M_dot_a`, `N_R`, `M_dot_R_c` and `M_dot_R_e` agree. `r_p_c` agrees within 4.4×10^−6. The CoolSolve hint that `Air` might be read as moist air was left as `Air`. The hint that 30 might be Fahrenheit was left as °C: the stored solution and `T_2` are in °C. The eight names present only in CoolSolve are `Q_4_c`, `x_c`, `e_min_c`, `e_c`, `Q_4_e`, `x_e`, `e_min_e`, `e_e`: the outputs of `cpbar` that the original function-position call did not return.

## Source and attribution

The equation-window header is `MSTh R9 - Exercice 1- suite`. It names no person. The inventory attributes the course to J. Lebrun, V. Lemort and S. Bertagnolio. The EES licence tag is the Laboratoire de Thermodynamique, Université de Liège, and is not an author. `authors` is therefore `TBD (ULiège MSTh)`.

Source file (EES X7.458, French comments):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 09/MSTh R9 Ex 1 - 2.EES`
(inventory `TM-0142`).

`PROCEDURE cpbar` and `FUNCTION gamma` are copied from `models/cycles/gas_turbines/gas_turbine_reduced_quantities/` (the routines of CSL-0005, P. Ngendakumana, ULiège, 2003, including the 0/0 guard). This equation window does not define them.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `MSTh R9 Ex 1 - 2.EES` (EES X7.458, plain text, 50 variables, 0 tables, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already SI (Pa, °C, J), deleted. No `$TABSTOPS` and no `$Export`. Nothing was rescaled. `compare_solution.py` was run without `--ees-units`. The `+273` factors are the ones in the equation window. Comments translated to English. No diagram state arrays: the fluids are ideal gases, and CoolSolve has no ideal-gas diagram. The extract's function list names `p_2`; that is the comment `P_2 = 800000`, not a call. The comment that `T_1` could be varied in a parametric table is not a stored table.
- **2026-10-15 — square system**: the extraction with only `$UnitSystem` removed has 49 equations and 50 variables, `System square: No`. `T_1` is used by `enthalpy(Air, T=T_1)` and is not assigned. The stored solution holds 30 °C, so the only equation added is `T_1 = 30`. The comments `r_p_c = 8` and `W_dot_sh = 1E6` were not restored. The real equations are `r_p_c = P_2/P_1` and `W_dot_sh = w_dot_e - W_dot_c`. Provisional comments `c_p_p = 1200`, `c_p_p_e = 1200` and `gamma_e = 1.4` were not restored.
- **2026-10-15 — `cpbar` and `gamma`**: the window calls `cpbar(m,n,f,...)` and `gamma(m,n,f,T_3,T_4)` and defines neither. `PROCEDURE cpbar` and `FUNCTION gamma` are copied into this file. `gamma` is copied because the window calls it. The original writes `c_p_p = cpbar(...)` and `c_p_p_e = cpbar(...)` in function position. The routine is a five-output procedure, so both calls are `CALL` (valid EES, same returned specific heat). Not a variant. `CS-GAP-INCLUDE` is not a missing feature: the routines are in the file. `LHV_gn = 50E6` stays a constant; `LowerHeatingValue` is not called. No `MODULE`, `(T, h)` property pair, REFPROP or NASA call, `$COMMON` or string array, so no D10–D14 rewrite. `Air` stays `Air` and `CH4` stays `CH4`.
- **Level**: equations 58 → 1 (50–300); largest block 19 → 1 (6–30); a procedure and a function are present → 1; compressor, combustor and expander are coupled → 1; the point is part-load, linked by reduced quantities → 1; the stored root needs the shipped initials → 1. Score 6 → level 3 on the grid, moved down by one to **level 2**: this is an MSTh repetition exercise, one steady point, with constant efficiencies, and the block of 19 is the cycle match.

## Limitations and CoolSolve gaps

Constant isentropic efficiencies. One shaft. Simplified air inside `cpbar` (79 % N2 / 21 % O2). The kelvin conversion in the reduced quantities and in the isentropic expansion is `+273`, as written. `eta` is shaft power divided by compressor power, as written. Absolute `Air` enthalpy and entropy use the CoolProp reference, and the enthalpy offset is not a constant. No CoolSolve gap blocks the file. `missing_features` is empty.

## Related models

`related` is empty. No other library model is linked from this file.

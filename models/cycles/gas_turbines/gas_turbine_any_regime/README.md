# Single-shaft gas turbine at any regime

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0220`

Steady exercise of a single-shaft gas turbine burning methane in air. One operating point is closed by a three-row compressor map (reduced flow and isentropic efficiency versus pressure ratio) and by a constant expander reduced flow and isentropic efficiency.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air, CH4 (equation window). The copied `cpbar` and `gamma` routines also call CO2, CO, H2O, N2 and O2 |
| **Size** | 50 equations after analysis (largest block: 21) |
| **Source** | ULiège MSTh repetition R9, exercise 2 |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution |

## Problem statement

A single-shaft gas turbine runs on air with methane (CH4, written `m_f = 1`, `n_f = 4`) as fuel. The inlet is 15 °C and 1.01×10^5 Pa. The turbine inlet temperature is 850 °C. The lower heating value is 50×10^6 J/kg, written as a constant. The combustor pressure loss is 5 % (`P_3 = 0.95*P_2`). The expander discharges at the inlet pressure (`P_4 = P_1`).

The header of the file is "MSTh - SB - R9 - Exercice 2". Under "Régime nominal" the compressor map is interpolated against the pressure ratio. Under "Tout régime" the expander reduced flow and isentropic efficiency are constant:

| | |
|---|---|
| `M_R_e` | 14.2 (kg/s)·K^0.5/bar |
| `epsilon_s_e` | 0.85 |

The reduced mass flow is the one written in the window, with `+273` and with the pressure divided by 100000 (so the unit is per bar):

\[
M_{R,c} = \dot m_a\frac{\sqrt{T_1+273}}{P_1/100000}, \qquad
M_{R,e} = \dot m_p\frac{\sqrt{T_3+273}}{P_3/100000}, \qquad
r_{p,c} = \frac{P_2}{P_1}.
\]

The line `N_R = N/sqrt(T_1+273)` is a comment. It is not an equation. Find the pressure ratio, the shaft power, `eta` and the air and fuel flows of this point. In the window, `eta = W_dot_sh/Q_dot_c` and `Q_dot_c = M_dot_f*LHV_f`.

## Model

The map is parametric Table 1 of the EES file (three rows, no embedded lookup table). It is shipped as `gas_turbine_any_regime-lookup_1.csv`:

| `r_p_c` | `M_R_c` | `epsilon_s_c` |
|---:|---:|---:|
| 5 | 32.9 | 0.86 |
| 4.7 | 33.8 | 0.79 |
| 4.5 | 34.3 | 0.77 |

The window writes the short form `INTERPOLATE('M_R_c','r_p_c',r_p_c=r_p_c)` and the same for `epsilon_s_c` (the first string is the column, on the default lookup). Those calls are written here with the table name CoolSolve reads, in the native keyword form:

```
M_R_c = INTERPOLATE('lookup_1','M_R_c','r_p_c',r_p_c=r_p_c)
epsilon_s_c = INTERPOLATE('lookup_1','epsilon_s_c','r_p_c',r_p_c=r_p_c)
```

The stored point `r_p_c = 4.9246` lies between 4.7 and 5. Linear interpolation of the table reproduces the stored `M_R_c` and `epsilon_s_c`.

Compressor: isentropic relation on temperatures with `gamma(m_f,n_f,0,T_1,T_2)` (`f = 0` is pure air), then `epsilon_s_c*(T_2-T_1) = (T_2_s-T_1)`. The specific work uses `CP(Air)` at `T_m_c = (T_2+T_1)/2`. The window does not call `enthalpy` or `entropy` of Air.

Adiabatic combustor, per kg of air as the balance comment says (`en J/kg-air`):

\[
q_1+q_2+q_3+q_4+q_5 = 0
\]

\[
q_1 = c_{p,a,1}(T_{ref}-T_2),\quad
q_2 = c_{p,g}(T_{ref}-T_1),\quad
q_3 = -f\,\mathrm{LHV}_f,\quad
q_4 = 0,\quad
q_5 = (1+f)\,c_{p,p,23}(T_3-T_{ref}).
\]

`q_2` is written without a factor `f`. `c_{p,g}` is `CP(CH4)` at `(T_ref+T_1)/2`. `c_{p,p,23}` and the expander `c_{p,p,34}` are the mean specific heats from `cpbar`. The ratio of specific heats `gamma_e` is the `gamma` function of the same routines. The isentropic expansion is

\[
\frac{T_{4s}+273}{T_3+273} = \left(\frac{P_4}{P_3}\right)^{(\gamma_e-1)/\gamma_e}, \qquad
\epsilon_{s,e}(T_3-T_{4s}) = (T_3-T_4).
\]

Shaft power: `W_dot_sh = M_dot_a*w` with `w = (1+f)*w_e - w_c`.

| Inputs | Outputs |
|---|---|
| `T_1`, `P_1`, `T_3`, `LHV_f`, `M_R_e`, `epsilon_s_e` | `W_dot_sh`, `eta`, `r_p_c`, `M_dot_a`, `M_dot_f` |
| `m_f`, `n_f`, map `lookup_1` | `M_R_c`, `epsilon_s_c`, `T_2`, `T_4` |

## How to run

From this folder, with the shipped `.initials` and `gas_turbine_any_regime-lookup_1.csv` beside the file:

```bash
coolsolve ./gas_turbine_any_regime.eescode
```

The `.initials` file is the EES stored solution. It selects that root (`r_p_c` about 4.92, between the map rows 4.7 and 5). With those guesses the solve takes **8 iterations**. Without `.initials` the same equations do not converge: block 11 (21 variables) stops with `LineSearchFailed` at iteration 0. Use the shipped `.initials`.

## Results

| Quantity | EES stored | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `W_dot_sh` [W] | 328445.32 | 328143.52 | 9.19×10^−4 |
| `eta` [-] | 0.213658 | 0.213722 | 3.01×10^−4 |
| `M_dot_a` [kg/s] | 1.9714959 | 1.9715074 | 5.8×10^−6 |
| `M_dot_f` [kg/s] | 0.03074500 | 0.03070749 | 1.22×10^−3 |
| `r_p_c` [-] | 4.924622 | 4.924558 | 1.3×10^−5 |
| `M_R_c` [(kg/s)·K^0.5/bar] | 33.12613 | 33.12633 | 5.8×10^−6 |
| `epsilon_s_c` [-] | 0.842412 | 0.842397 | 1.8×10^−5 |
| `cp_g` [J/kg·K] | 2241.70 | 2220.60 | 9.41×10^−3 |
| `q_2` [J/kg] | 22416.96 | 22205.98 | 9.41×10^−3 |

`T_2` is above `T_1` (209.39 °C versus 209.77 °C in EES) and `T_4` is below `T_3` (549.21 °C versus 549.47 °C). The shaft power is positive. `r_p_c` stays between the map rows 4.7 and 5.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/. Ideal-gas Air has no diagram in CoolSolve, and the parametric table is the
     compressor map rather than a solved sweep, so this placeholder stays. -->

## Verification

Reference: stored solution in `MSTH-SB-R9-EX2.EES` (EES X7.458, 42 numeric values out of 45 names). Units are already Pa, °C and J, so `compare_solution.py` was run without `--ees-units`. The summary line is:

```
42 common variables, 12 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8
```

`verification.max_rel_diff` is **0.009411681**, the relative difference on `q_2`. `cp_g` has the same ratio, because `q_2 = cp_g*(T_ref-T_1)` and both temperatures are data. That is the largest gap over all 42 common variables. All 50 equations are satisfied (max absolute residual 1.05×10^−9).

**Shaft power, efficiency and flows**, apart from absolute enthalpies and entropies. The equation window does not evaluate `enthalpy(Air)` or `entropy(Air)`, and the stored solution has neither. `W_dot_sh` is 328144 W versus 328445 W (9.19×10^−4 low). `eta` is 0.21372 versus 0.21366 (3.01×10^−4 high). `M_dot_a` agrees to 5.8×10^−6. `M_dot_f` is 0.030707 kg/s versus 0.030745 kg/s (1.22×10^−3 low), just outside the comparison tolerance, in line with `cp(CH4)`.

The twelve names outside the tolerance are `cp_g`, `q_2`, `cp_a_1`, `cp_a_c`, `T_2`, `T_2_s`, `T_m_c`, `q_3`, `f`, `M_dot_f`, `Q_dot_c` and `cp_p_34`. `cp(Air)` is about 0.23 % high (`cp_a_1` 1013.03 versus 1010.64 J/kg·K, `cp_a_c` 1012.48 versus 1010.17 J/kg·K). `cp(CH4)` is 2220.60 versus 2241.70 J/kg·K (9.41×10^−3 low). The mean specific heat of the products over the expansion, `cp_p_34`, is 1.08×10^−3 low. The Air reference-state offset quoted for other models (enthalpy about +126 kJ/kg, not constant; entropy about −1814 to −1815 J/kg·K) is not a variable of this solution.

Only on the EES side of the variable list, and with no stored number, so they are not in the comparison: `gamma` (the function), `N` and `N_R` (the reduced-speed line is a comment). Only on the CoolSolve side: `Q_4_23`, `x_23`, `e_min_23`, `e_23`, `Q_4_34`, `x_34`, `e_min_34`, `e_34`, the unused outputs of the two `cpbar` calls.

## Source and attribution

Author of the original model: Stéphane Bertagnolio, from the header initials SB (`MSTh - SB - R9 - Exercice 2`). The `{$ID$}` tag is the EES licence of the Laboratoire de Thermodynamique, Université de Liège, not the author. Institution and course: ULiège, Machines et systèmes thermiques (MSTh), repetition R9, exercise 2.

Source file (EES X7.458, comments in French):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 09/MSTH-SB-R9-EX2.EES`
(inventory candidate `TM-0145`, representative, no duplicate group).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): unit system already `SI MASS DEG PA C J`. `$UnitSystem` was deleted. No `$TABSTOPS` and no `$Export` were present. No unit conversion, and `compare_solution.py` was run without `--ees-units`. The EES licence tag was removed. Comments translated to English. `T_1 = 15` and `P_1 = 1.01E5` stay equations. `LHV_f = 50E6` stays a constant. The line `N_R = N/sqrt(T_1+273)` stays a comment. Provisional values (`gamma_c = 1.4`, `gamma_e = 1.4`, `cp_p_23 = 1200`, `cp_p_34 = 1200`) stay comments. No original equation was replaced by a stored number, and no diagram array was added. The system is square (50 equations, 50 variables) without an extra input.
- **2026-10-15 — lookup**: the extract finds no lookup table and one parametric table, Table 1, 3×3. The rows were checked against the file (`r_p_c`, `M_R_c`, `epsilon_s_c` = 5 / 32.9 / 0.86, 4.7 / 33.8 / 0.79, 4.5 / 34.3 / 0.77) and against the stored point, which matches linear interpolation. They are shipped unchanged as `gas_turbine_any_regime-lookup_1.csv`. The window's short `INTERPOLATE` form is written with that table name, in the native keyword spelling `INTERPOLATE('lookup_1','M_R_c','r_p_c',r_p_c=r_p_c)` (and the same for `epsilon_s_c`). That form solves in CoolSolve 0.3.0@332d95a. No `_coolsolve` variant.
- **2026-10-15 — cpbar and gamma**: the window calls them and does not define them. `PROCEDURE cpbar` and `FUNCTION gamma` were copied from `gas_turbine_part_load.eescode`. `cpbar` is a five-output procedure, so the two calls written in function position are transcribed as `CALL`. That form is valid EES, and it is not a variant. `gamma` stays a function call. `CS-GAP-INCLUDE` is not listed. `related` stays empty.
- **Level**: equations 50 after analysis → 1 (50–300); largest block 21 → 1 (6–30); a procedure and a function are present → 1; compressor, combustor and expander are coupled → 1; the compressor map and the constant expander reduced flow are an any-regime characteristic → 1; without the shipped initials the block of 21 stops at iteration 0 → 1. Score 6 → level 3 on the grid, moved down by one to **level 2**: this is an MSTh repetition exercise, one steady point, and the block of 21 is the cycle match.

## Limitations and CoolSolve gaps

Physical simplifications of the exercise: air and combustion products are ideal gases with a specific heat evaluated at one temperature (compressor) or as a mean (`cpbar`), the combustor balance is written as in the window (`q_2` has no factor `f`, `q_4 = 0`), the mechanical losses are not in the window, and the expander is a single reduced flow and a single isentropic efficiency.

The native keyword form of `INTERPOLATE` solves. `missing_features` is empty. A hint to use `AirH2O` instead of `Air`, and a "Did you mean CO2?" hint on `molarmass(CO2)`, were ignored. The fluids of the window stay Air and CH4.

## Related models

No other library model was linked at import time (`related` was empty). TM-0147 and TM-0148 are similar exercises and are not in a duplicate group with TM-0145; those inventory rows were left unchanged. Later link: `CSL-0293` (*two_shaft_gas_turbine_expander_map*), the two-shaft exercise 3 of the same R9 series, from whose file this model's library routines were copied.

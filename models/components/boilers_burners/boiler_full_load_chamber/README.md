# Full-load boiler with a combustion chamber and fictitious exchangers

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0219`

Exercise of a fuel-oil boiler. An adiabatic combustion chamber brings the reactants to 25 °C through fictitious exchangers. A gas-water exchanger and a fictitious water-ambient exchanger follow. The same window also computes a stand-by blend and a third regime at one tenth of the useful heat. The mean specific heat of the products in the chamber is `cpbar`; on the gas side of the exchanger it stays the assigned constant 1300 J/kg·K.

| | |
|---|---|
| **Category** | Components › Boilers and burners |
| **Fluids** | Air, Water (equation window). The copied `cpbar` procedure also calls CO2, CO, H2O, N2 and O2 |
| **Size** | 80 equations after analysis (largest block: 18) |
| **Source** | ULiège MSTh repetition R7, exercise 4 |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution |

## Problem statement

The equation-window header is "MSTh - SB - R7 - Exercice 4". The nominal-regime comment says that two extra parameters come from the previous exercise, with `M_dot_w` and `AU_gw` proportional to the fuel flow:

\[
AU_{gw} = 75.28\times\frac{3}{5.813},\qquad
\dot M_w = 0.5961\times\frac{3}{5.813}.
\]

Fuel oil: hydrogen mass fraction 0.131, carbon the complement, equivalent fuel CmHn with `m = 1`, lower heating value `LHV_f = 43E6` J/kg, `cp_f = 1800` J/kg·K. The fuel volume flow is `V_dot_f = 3E-3/3600` and the mass flow is `M_dot_f = 0.8*1000*V_dot_f`. The fuel-air ratio is `f = 0.06`. Air and fuel are supplied at 20 °C. The ambient temperature is 20 °C. The supply pressure is 101325 Pa. Water enters at 70 °C.

At full load the chamber is adiabatic. `Q_dot_4 = 0` (complete combustion, as written). The gas-water exchanger uses `cp_p_2 = 1300`. The water-ambient exchanger is marked fictitious. Boiler efficiency is useful heat divided by fuel power. Stand-by sets the water outlet equal to the inlet and a fuel flow written `0.03E-3*0.8*1000/3600`. The third regime sets the useful heat to one tenth of the full-load value and blends the on and off water outlets with a time fraction `theta`.

## Model

Chamber energy balance, powers in W, temperatures in °C. The reactants are brought to 25 °C:

\[
\dot Q_1+\dot Q_2+\dot Q_3+\dot Q_4+\dot Q_5 = 0
\]

\[
\dot Q_1 = \dot M_a\,c_{p,a}(25-T_{su}),\quad
\dot Q_2 = \dot M_f\,c_{p,f}(25-T_{su}),\quad
\dot Q_3 = -\dot M_f\,\mathrm{LHV}_f,
\]

\[
\dot Q_4 = 0,\quad
\dot Q_5 = \dot M_p\,c_{p,p}(T_g-25),\quad
\dot M_p = \dot M_f+\dot M_a.
\]

`c_{p,a} = CP(Air)` at `T_m = (T_su+25)/2`. `c_{p,p}` is `cpbar(m,n,f,T_g,25)`. The original writes that call in function position. The routine is a five-output procedure, so the file uses `CALL`. The commented provisional `cp_p = 1300` is not an equation.

Gas-water exchanger, counterflow effectiveness. `cp_p_2 = 1300` is the equation. The commented `cp_p_2 = cpbar(...)` is not. Water specific heat is `CP(Water)` at the mean water temperature and `P_su`. The commented `cp_w_gw = 4187` is not an equation. `AU_gw` is known from the scaling above, so this exchanger does not determine it.

Fictitious water-ambient exchanger: effectiveness `1-exp(-NTU)`, with `NTU = AU_wenv/C_dot`. The same `AU_wenv` is used with the burner off. Stand-by closes it: `T_w_ex_set = T_w_su` and

\[
T_{w,ex,set} = \theta_{stb}\,T_{w,ex,on}+(1-\theta_{stb})\,T_{w,ex,off},
\]

with `T_w_ex_on = T_w_ex_2`. `AU_wenv` is that unknown (stored value 5.208 W/K, guess 5.123 W/K). It is not replaced by the stored number.

Third regime, after the full-load heat rate is known:

\[
\dot Q_{u,m} = 0.1\,\dot Q_{utile}
= \dot M_w\,c_{p,w,m,3}(T_{w,ex,3}-T_{w,su}),
\]

with `cp_w_m_3 = 4187` as assigned. `theta` blends the on and off outlets. `eta_m = Q_dot_u_m/Q_dot_c_m` and `Q_dot_c_m = theta*M_dot_f*LHV_f`.

The window has no `enthalpy()` call. `cpbar` uses ideal-gas enthalpies internally. No reference-state offset is applied.

| Inputs | Outputs |
|---|---|
| `T_su`, `T_env`, `P_su`, `T_w_su`, `f`, `LHV_f`, `y_h`, `V_dot_f`, `cp_f` | `Q_dot_utile`, `eta`, `T_g`, `T_w_ex_1`, `T_w_ex_2` |
| `cp_p_2 = 1300`, `cp_w_m_3 = 4187`, the two scale factors | `T_w_ex_off`, `T_w_ex_3`, `eta_m`, `AU_wenv`, `theta` |

## How to run

From this folder, with the shipped `.initials` beside the file:

```bash
coolsolve ./boiler_full_load_chamber.eescode
```

The `.initials` file is the EES stored solution. With those guesses the solve takes **19 iterations**. Without `.initials`, Newton stops at 100 iterations on the chamber block (`T_g`, `cp_p` and the `cpbar` outputs) and does not return a root (last residual 0.45). Use the shipped `.initials`.

## Results

| Quantity | EES stored | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Q_dot_utile` [W] | 25772.82 | 25753.02 | 7.68×10^−4 |
| `Q_dot_gw` [W] | 26137.99 | 26117.82 | 7.72×10^−4 |
| `Q_dot_wenv` [W] | 365.167 | 364.794 | 1.02×10^−3 |
| `Q_dot_conso` [W] | 28666.67 | 28666.67 | 0 |
| `eta` [-] | 0.899052 | 0.898361 | 7.68×10^−4 |
| `T_g` [°C] | 1926.78 | 1925.34 | 7.45×10^−4 |
| `T_w_ex_1` [°C] | 90.2573 | 90.2290 | 3.13×10^−4 |
| `T_w_ex_2` [°C] | 89.9750 | 89.9470 | 3.11×10^−4 |
| `T_w_ex_off` [°C] | 69.7982 | 69.7985 | 4.0×10^−6 |
| `T_w_ex_3` [°C] | 72.0009 | 71.9993 | 2.1×10^−5 |
| `cp_a` [J/kg·K] | 1006.66 | 1006.22 | 4.31×10^−4 |
| `cp_p` [J/kg·K] | 1277.07 | 1278.04 | 7.55×10^−4 |
| `cp_w_gw` [J/kg·K] | 4194.21 | 4196.84 | 6.26×10^−4 |

`T_g` is about 1925 °C, above the 20 °C supply. Water enters at 70 °C and leaves the gas-water exchanger near 90 °C, then drops by a fraction of a degree in the envelope. With the burner off the outlet is just under 70 °C. `Q_dot_conso` matches the stored fuel power. `Q_dot_u_set` is 0 because the stand-by outlet equals the inlet.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/. This is a boiler energy balance. No P[i]/h[i]/T[i]/s[i] arrays were added,
     and the file stores no parametric table, so this placeholder stays. -->

## Verification

Reference: stored solution in `MSTh-SB-R7-Ex4.EES` (EES X7.458, 76 numeric values). Units are already Pa, °C and J, so `compare_solution.py` was run without `--ees-units`. The summary line is:

```
76 common variables, 4 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 4
```

`verification.max_rel_diff` is **0.001402**, the relative difference on `NTU_wenv_off` (0.00403784 versus 0.00404351). That is the largest gap over all 76 common variables. All 80 equations are satisfied (max relative residual 8.8×10^−14).

Four common variables sit above the comparison tolerance: `NTU_wenv_off` (1.40×10^−3), `epsilon_wenv_off` (1.40×10^−3), `eta_m` (1.34×10^−3) and `Q_dot_wenv` (1.02×10^−3). They follow `cp(Water)` and the `AU_wenv` closure. `cp_w_wenv_off` is 4190.01 versus 4186.73 J/kg·K. `AU_wenv` is 5.2048 versus 5.2080 W/K. The NTU is `AU_wenv` divided by a capacity rate near 1290 W/K, so a small absolute gap is a relative gap of 0.0014 on a number near 0.004.

**Heat rates and water temperatures**, apart from specific heats. Useful heat is 25753.0 W versus 25772.8 W (7.68×10^−4 low). Gas-water heat is 26117.8 W versus 26138.0 W. Fuel power agrees (28666.67 W). Water leaves the gas-water exchanger at 90.229 °C versus 90.257 °C, the boiler at 89.947 °C versus 89.975 °C, and the burner-off state at 69.7985 °C versus 69.7982 °C. The third-regime outlet is 71.999 °C versus 72.001 °C.

**Specific heats.** The window does not call `enthalpy()`, so there is no enthalpy offset to remove. `cp(Air)` at 22.5 °C is 1006.22 versus 1006.66 J/kg·K, and `Q_dot_1` follows it (55.901 versus 55.925 W). `cp_p` from `cpbar` is 1278.04 versus 1277.07 J/kg·K; `T_g` is 1925.34 °C versus 1926.78 °C. `cp(Water)` differs by at most 3.3 J/kg·K (`cp_w_set`, 4190.07 versus 4186.79).

The four names present only in CoolSolve are `Q_4_cb`, `x_cb`, `e_min_cb` and `e_cb`: outputs of `cpbar` that the original function-position call did not return. `Q_4_cb = 0` and `x_cb = 1`, the complete-combustion defaults. `Air` was left as `Air`. The hint "Did you mean CO2?" on `molarmass(CO2)` was left as written.

## Source and attribution

The equation-window header is `MSTh - SB - R7 - Exercice 4`. SB is Stéphane Bertagnolio. The EES licence tag is the Laboratoire de Thermodynamique, Université de Liège, and is not an author.

Source file (EES X7.458, French comments):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 07/SB/MSTh-SB-R7-Ex4.EES`
(inventory `TM-0114`).

`PROCEDURE cpbar` is copied from `models/cycles/gas_turbines/gas_turbine_part_load/` (the routine of CSL-0005, including the 0/0 guard). `FUNCTION gamma` is not copied: this procedure does not call it. The equation window does not define `cpbar`.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `MSTh-SB-R7-Ex4.EES` (EES X7.458, plain text, 77 variable records, 0 tables, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already SI (Pa, °C, J), deleted. No `$TABSTOPS` and no `$Export`. Nothing was rescaled. `compare_solution.py` was run without `--ees-units`. Comments translated to English. No diagram-state arrays: this is a boiler energy balance, not a refrigerant cycle. The original writes `t_w_ex_3`, `t_w_ex_on` and `t_w_ex_off`; EES names are case-insensitive, so the file uses `T_w_ex_3`, `T_w_ex_on` and `T_w_ex_off`. One stored record `P` has an empty value and the default guess 1; it is the keyword `P=` inside `CP(...,P=P_su)`, not an equation variable, and it was not added.
- **2026-10-15 — square system**: the extraction with only `$UnitSystem` removed has 76 equations and 76 variables, `System square: Yes`. No diagram-window input was added. No stored unknown replaced an equation. `AU_wenv` is an output of the stand-by closure (the burner-on and burner-off exchangers share it). The comments `cp_p=1300`, `cp_p_2=cpbar(m,n,f,T_g_su,T_g_ex)`, `cp_w_gw=4187`, `cp_w_wenv=4187`, `cp_w_m_set=4187` and `cp_w_wenv_off=4187` stay comments. The assignment `cp_p_2 = 1300` stays the equation. `LHV_f = 43E6` stays a constant; `LowerHeatingValue` is not called.
- **2026-10-15 — `cpbar`**: the window calls `cp_p = cpbar(m,n,f,T_g,25)` and does not define `cpbar`. `PROCEDURE cpbar` is copied into this file. `FUNCTION gamma` is not copied. The original writes the call in function position. The routine is a five-output procedure, so the call is `CALL cpbar(m,n,f,T_g,25:cp_p,Q_4_cb,x_cb,e_min_cb,e_cb)` (valid EES, same returned specific heat). Not a variant. `CS-GAP-INCLUDE` is not listed. `Air` and `Water` stay as written.
- **Level**: equations 80 → 1 (50–300); largest block 18 → 1 (6–30); a procedure is present → 1; the chamber, the gas-water exchanger and the envelope are sequential blocks (sizes 6, 10 and 18), so the coupled-components criterion is 0; the third regime is an explicit blend at a prescribed fraction of full-load heat, not a part-load map or a dynamic model → 0; without the stored guesses the chamber block does not converge → 1. Score 4 → level 3.

## Limitations and CoolSolve gaps

`cp_p_2` is the constant 1300 J/kg·K, as assigned, not a second `cpbar` call. `Q_dot_4 = 0` assumes complete combustion. `cpbar` uses simplified air (79 % N2 / 21 % O2). `AU_wenv` is calculated from the stand-by blend, not chosen as a free input. Absolute enthalpies are not variables of this window. No CoolSolve gap blocks the file. `missing_features` is empty.

## Related models

`related` is empty. No other library model is linked from this file.

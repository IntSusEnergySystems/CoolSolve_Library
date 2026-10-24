# Fuel-oil boiler with on/off envelope losses and a set-point blend (theta)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0263`

Exercise of a fuel-oil boiler (MSTh repetition R7, exercise 3, suite). Fuel oil with carbon mass fraction 0.869 burns at a fuel-air ratio computed from the air flow; the adiabatic flame temperature follows from a combustor energy balance with the mean specific heat of the products (`cpbar`). A gas-water exchanger (eps-NTU, gas-side specific heat assigned the constant 1300 J/kg·K) and a water-envelope exchanger with an ON branch and an OFF branch follow. Exercise 3 adds a set-point outlet temperature that blends the ON and OFF water outlets with a fraction `theta`, the independent variable of the original parametric table; here `theta = 1`, its default-run value.

| | |
|---|---|
| **Category** | Components › Boilers and burners |
| **Fluids** | Air, Water (equation window). The copied `cpbar` procedure also calls CO2, CO, H2O, N2 and O2 |
| **Size** | 54 equations after analysis (largest block: 6) |
| **Source** | ULiège MSTh repetition R7, exercise 3 (`MSTh R7 Ex 3 - 2.EES`) |
| **Authors** | TBD (ULiège MSTh repetition R7; course team J. Lebrun, V. Lemort, S. Bertagnolio) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution |

## Problem statement

The equation-window header is `MSTh R7 - 071105 - Exercice 3 - suite` (5 November 2007). The file continues the data of exercise 2 (`nouvelles données (ex2)`) and states for exercise 3 a set-point water outlet temperature `T_w_ex_set = 80`, marked `(table paramétrique)`: the value is obtained by sweeping `theta` in an EES parametric table rather than by one equation.

Fuel oil: carbon mass fraction 0.869, hydrogen the complement, equivalent fuel CmHn with `m = 1` and `n = y_h*12/y_c`, lower heating value 4.3E7 J/kg, fuel specific heat 1800 J/kg·K. Air and fuel enter at 25 °C, the environment is at 25 °C, water returns at 70 °C. Flows and conductances are the exercise-2 data: air 0.02084 kg/s, fuel 0.001292 kg/s, water 0.5972 kg/s, `AU_gw` 73.73 W/K, `AU_wenv` 9.59 W/K. The fuel-air ratio `f` is solved from `M_dot_a = M_dot_f/f` (0.061996, the commented `{f=0.062}` is not an equation).

## Model

Per kg of fuel, the equivalent hydrocarbon `CmHn` is closed by `m = 1`, `n = y_h*12/y_c`. The adiabatic combustor balance (the original's comment "chaudière adiabatique"), powers in W, temperatures in °C:

\[
\dot M_f \mathrm{LHV} + \dot M_a c_{p,a}(T_{a,su}-T_{ref}) + \dot M_f c_f (T_{f,su}-T_{ref}) = \dot M_p c_{p,p}(T_{p,ad}-T_{ref})
\]

with `T_ref = 25 °C`, `cp_a = cp(Air)` at `T_a_su`, `c_{p,p} = cpbar(m,n,f,T_p_ad,T_ref)` and `M_dot_p = M_dot_a + M_dot_f`.

Gas-water exchanger, counterflow effectiveness (as in the original):

\[
\varepsilon_1=\frac{1-e^{-NTU_1(1-\omega_1)}}{1-\omega_1 e^{-NTU_1(1-\omega_1)}},\quad
NTU_1 = \frac{AU_{gw}}{\dot C_{min}},\quad \omega_1 = \frac{\dot C_{min}}{\dot C_{max}}
\]

\[
\dot Q_1 = \varepsilon_1 \dot C_{min}(T_{gas,su}-T_{w,su}) = \dot C_w (T_{w,ex,1}-T_{w,su}) = \dot C_p (T_{gas,su}-T_{gas,ex})
\]

with `cp_p_hex = 1300` J/kg·K as assigned, `cp_w = 4186` J/kg·K, `AU_1 = AU_gw`, `T_gas_su = T_p_ad`.

Envelope (semi-isothermal, metal at `T_env`, `AU_2 = AU_wenv`, `epsilon_2 = 1-exp(-NTU_2)`), two branches:

\[
\dot Q_{2,on} = \varepsilon_2 \dot C_w (T_{w,ex,1}-T_{env}) = \dot C_w (T_{w,ex,1}-T_{w,ex,on})
\]

\[
\dot Q_{2,off} = \varepsilon_2 \dot C_w (T_{w,su}-T_{env}) = \dot C_w (T_{w,su}-T_{w,ex,off})
\]

Balance and efficiency: `Q_dot_u = Q_dot_1 - Q_dot_2_on`, `Q_dot_c = M_dot_f*LHV`, `eta = Q_dot_u/Q_dot_c`. Set-point block:

\[
T_{w,ex,set} = \theta T_{w,ex,on} + (1-\theta) T_{w,ex,off},\quad
\dot Q_{u,set} = \dot C_w (T_{w,ex,set}-T_{w,su}),\quad
\dot Q_{c,set} = \theta \,\mathrm{LHV}\, \dot M_f,\quad \eta_{set} = \dot Q_{u,set}/\dot Q_{c,set}.
\]

| Inputs | Outputs |
|---|---|
| `M_dot_a`, `M_dot_f`, `M_dot_w`, `AU_gw`, `AU_wenv`, `T_w_su`, `T_env`, `theta = 1` | `T_p_ad`, `T_gas_ex`, `T_w_ex_1`, `T_w_ex_on`, `T_w_ex_off`, `Q_dot_u`, `eta`, `eta_set` |

The flame-temperature block is implicit: the unknown `T_p_ad` sits inside the `cpbar` call.

## How to run

From this folder, with the shipped `.initials` (the EES stored solution):

```bash
coolsolve ./fuel_oil_boiler_onoff_setpoint.eescode
```

The solve takes **12 iterations** with the shipped guesses. Without `.initials` Newton stops at 100 iterations in the `cpbar` block (`T_p_ad`, `cp_p` and the routine outputs, last residual 0.457) and does not return a root: keep the `.initials`. No `coolsolve.conf`, no variant, no lookup tables.

## Results

Default operating point (`theta = 1`), EES stored solution versus CoolSolve:

| Quantity | EES stored | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_p_ad` [°C] | 1979.55 | 1978.08 | 7.42×10⁻⁴ |
| `T_gas_ex` [°C] | 220.034 | 219.918 | 5.25×10⁻⁴ |
| `T_w_ex_1` [°C] | 90.2507 | 90.2351 | 1.73×10⁻⁴ |
| `T_w_ex_on` [°C] | 90.0008 | 89.9853 | 1.72×10⁻⁴ |
| `T_w_ex_off` [°C] | 69.8277 | 69.8277 | 3.94×10⁻¹¹ |
| `Q_dot_1` [W] | 50624.2 | 50585.2 | 7.70×10⁻⁴ |
| `Q_dot_2_on` [W] | 624.555 | 624.406 | 2.39×10⁻⁴ |
| `Q_dot_2_off` [W] | 430.723 | 430.723 | 9.33×10⁻¹¹ |
| `Q_dot_u` [W] | 49999.7 | 49960.8 | 7.76×10⁻⁴ |
| `Q_dot_c` [W] | 55556 | 55556 | 0 |
| `eta` [-] | 0.899987 | 0.899288 | 7.76×10⁻⁴ |
| `cp_a` [J/kg·K] | 1006.68 | 1006.31 | 3.68×10⁻⁴ |
| `cp_p` [J/kg·K] | 1284.29 | 1285.26 | 7.52×10⁻⁴ |
| `f` [-] | 0.0619962 | 0.0619962 | 0 |

The boiler hands about 50.0 kW of useful heat to the water (70 → 90.2 °C) from 55.6 kW of fuel power, i.e. `eta ≈ 0.90`, at a flame temperature near 1980 °C and a chimney gas temperature near 220 °C. `T_w_ex_set = T_w_ex_on` because `theta = 1`, and `eta_set = eta` accordingly.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![Boiler efficiency vs theta](figures/fuel_oil_boiler_onoff_setpoint_theta.png)
     + one-line caption. This is a boiler energy balance; no P[i]/h[i]/T[i]/s[i] arrays were added. -->

## Verification

Reference: the solution stored in `MSTh R7 Ex 3 - 2.EES` (EES X7.458, 51 variable records of which 50 carry a value). The unit system is already `$UnitSystem SI MASS DEG PA C J`, so `compare_solution.py` was run without `--ees-units`. The summary line is:

```
50 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 4
```

`verification.max_rel_diff` is **0.000776**, on `eta` (0.899288 versus 0.899987). It is the largest relative difference over all 50 common variables; nothing reaches the printed `rtol=0.001`. The differences follow the property backend: `cp_a` is 1006.31 versus 1006.68 J/kg·K and `cp_p` from `cpbar` is 1285.26 versus 1284.29 J/kg·K, which propagates to `T_p_ad` (1978.08 versus 1979.55 °C), `Q_dot_1` and `eta`. The window has no `enthalpy()` call, so there is no reference-state offset. The 54 equations of the solve are all satisfied (max relative residual 5.4×10⁻¹³).

The four names present only in CoolSolve are `Q_4_ad`, `x_ad`, `e_min_ad` and `e_ad`: outputs of `cpbar` that the original function-position call did not return. Their values are the complete-combustion defaults (`Q_4_ad = 0`, `x_ad = 1`, `e_min_ad = 0`) and the excess air `e_ad = 0.1164` (11.6 % above stoichiometric; `f_st = f*(1+e) = 0.0692`, consistent with the CmHn stoichiometry).

The one stored record without a value is `T_w_ex`: it comes from the commented line `{T_w_ex=90}` of the previous exercise and appears in no equation, so CoolSolve does not keep it — this is the 51st record of the "50/51" stored solution.

## Source and attribution

Source file (EES X7.458, French comments, RTF equation window):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 07/MSTh R7 Ex 3 - 2.EES`
(inventory `TM-0108`, duplicate group `DG-0025`, representative of a 10-file family). EES licence tag: Laboratoire de Thermodynamique, Université de Liège — a licence holder, not an author. No initials appear in the file (the header carries only the date `071105`); the inventory credits the ULiège MSTh course team (J. Lebrun, V. Lemort, S. Bertagnolio), so `authors` is `TBD` with that hint.

`PROCEDURE cpbar` is copied from `models/fundamentals/combustion/cpbar_combustion_products/` (CSL-0005, P. Ngendakumana, ULiège 2003, with the 0/0 guard). `FUNCTION gamma` is not copied: the procedure does not call it. The equation window does not define `cpbar`; in EES it comes from the laboratory's user library.

## Conversion log

- **2026-10-22 — import**: `ees_extract.py` on `MSTh R7 Ex 3 - 2.EES` (EES X7.458, RTF equation window converted to text, 93 lines, 51 variable records, no tables decoded, no warnings). One trailing NUL byte removed; `$UnitSystem SI MASS DEG PA C J` deleted (already SI-°C-Pa-J, nothing rescaled, `compare_solution.py` without `--ees-units`). Comments translated to English (the original's "mole de C" in the CmHn comment is a typo for H, corrected). Unit annotations `[J/kg-K]`, `[J/kg]`, `[W/K]` kept as written. No diagram-state arrays: this is a boiler energy balance, not a refrigerant cycle.
- **2026-10-22 — square system**: the extraction with only `$UnitSystem` removed has **49 equations and 50 unknowns** (`System square: No` — `coolsolve -d`). `theta` appears in two equations but is defined by none: it is the independent variable of the EES parametric table of the file (table block with the columns `theta`, `T_w_ex_set`, `eta_set`; the statement comment `(table paramétrique)`), and the stored solution has `theta = 1`. Following workflow §3 (parametric-table inputs → default run), the equation `theta = 1` was added; the system is then 54/54 square with the copied `cpbar` outputs. No stored unknown was put into an equation: the stored values live in the shipped `.initials`.
- **2026-10-22 — parametric table**: `ees_extract.py` reported no tables (the heuristic does not decode tables of an RTF file) and the inventory `tables` cell is empty; the table was located by a hand scan of the binary block of the file (`theta`, `T_w_ex_set`, `eta_set` column names). The model never calls the table, so no table file is shipped; the sweep itself is reproduced by changing `theta`.
- **2026-10-22 — `cpbar`**: the window calls `cp_p = cpbar(m,n,f,T_p_ad,T_ref)` and does not define `cpbar`. `PROCEDURE cpbar` is copied from CSL-0005. The original writes the call in function position; the routine is a five-output procedure, so the call is `CALL cpbar(m,n,f,T_p_ad,T_ref:cp_p,Q_4_ad,x_ad,e_min_ad,e_ad)` (valid EES, same returned specific heat — the CSL-0034 pattern). Not a variant; `CS-GAP-INCLUDE` (`CS-FEAT-IMPORT`) is not listed in `missing_features`.
- **2026-10-22 — level**: equations 54 → 1 (50–300); largest block 6 → 1 (6–30); a procedure is present → 1; the combustor, the gas-water exchanger and the envelope are sequential blocks (49 blocks) → 0; the `theta` blend is an explicit set-point formula, not a part-load map or a dynamic model → 0; without the shipped guesses the `cpbar` block does not converge → 1. Score 4 → level 3 (the inventory guessed 2).

## Limitations and CoolSolve gaps

`cp_p_hex` stays the assigned constant 1300 J/kg·K, not a `cpbar` call over the exchanger, as in the original. `cpbar` uses simplified air (79 % N2 / 21 % O2). The envelope uses the ON branch for `Q_dot_u`; the OFF branch only feeds the blend. `T_env` and `T_ref` are fixed at 25 °C. Absolute enthalpies are not variables of this window. No CoolSolve gap blocks the file; `missing_features` is empty.

## Related models

`CSL-0005` (cpbar_combustion_products): source of the copied `PROCEDURE cpbar`. `CSL-0006` (boiler_mean_specific_heat): same boiler structure (adiabatic combustor, eps-NTU gas-water exchanger, envelope losses) with other data, a `cpbar` call on the gas side and a single envelope branch. `CSL-0219` (boiler_full_load_chamber): the next exercise of the same MSTh R7 series, with a combustion chamber on fictitious exchangers and a `theta` blend of its own.

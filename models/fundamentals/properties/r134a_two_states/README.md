# R134a properties at three states (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0238`

Teaching exercise on R134a property calls at three independent states. The
equation window returns the specific volume and the quality from temperature
and pressure, the pressure and the quality from temperature and specific
volume, and the temperature from pressure and quality. There is no cycle and
no enthalpy call.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | R134a |
| **Size** | 11 equations (largest block: 1) |
| **Source** | thermo_models, KU Leuven exercises, file `03-31.EES` (Cengel 3-31) |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7d66c3b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The equation window evaluates three R134a states:

1. temperature −8 °C and pressure 320 kPa: specific volume and quality;
2. temperature 30 °C and specific volume 0.015 m³/kg: pressure and quality;
3. pressure 180 kPa and quality 1: temperature.

The file is the KU Leuven solution of textbook exercise Cengel 3-31. The
window itself carries only the comment "properties of r134a".

## Model

Each state is one pair of property calls, as written. CoolSolve treats `t_1`
and `T_1` as one variable, and `t_2` and `T_2` as one variable, so both
spellings stay. The fluid token stays `r134a`.

| State | Given | Computed |
|---|---|---|
| 1 | `T_1` = −8 °C, `p_1` = 320e3 Pa | `v_1` = `volume(r134a, t=t_1, p=p_1)`, `x_1` = `quality(...)` |
| 2 | `T_2` = 30 °C, `v_2` = 0.015 m³/kg | `P_2` = `pressure(r134a, t=t_2, v=v_2)`, `x_2` = `quality(...)` |
| 3 | `p_3` = 180e3 Pa, `x_3` = 1 | `T_3` = `temperature(r134a, p=p_3, x=x_3)` |

Those six assignments are already equations. With the five property calls the
system is square: 11 equations and 11 variables. No stored name was turned
into an equation. The stored names `T` and `P` (both 1) are not in the window.

No diagram-state arrays are added. These calls are property evaluations, not
a cycle.

## How to run

```bash
coolsolve ./r134a_two_states.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. The `.initials` file holds the EES
stored values of the 11 window variables, including `x_1 = -100`. `T` and `P`
are not in that file.

## Results

| Variable | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `v_1` [m³/kg] | 7.569328309920e-04 | 0.0007569329561 | 1.65e-07 |
| `x_1` [-] | 0 | −100 | 1.00e+00 |
| `P_2` [Pa] | 770196.303077 | 770641.9152 | 5.78e-04 |
| `x_2` [-] | 0.548766107515 | 0.5491822976 | 7.58e-04 |
| `T_3` [°C] | −12.7124453496 | −12.72895832 | 1.30e-03 |

`p_1`, `T_1`, `T_2`, `v_2`, `p_3` and `x_3` match the stored values (printed
relative difference 0). The `.sol` file tags `v_1` and `v_2` as kg/m³. The
numbers are the specific volumes above, and they match the stored specific
volumes.

`pressure()` prints two hints. `t=30` is within a few degrees of 32, so the
hint says the value looks like Fahrenheit and shows T=−1.11. The solved
`T_2` is 30 °C, and `P_2` is the saturation pressure near 770 kPa. `v=0.015`
m³/kg draws the hint that the specific volume looks large and that a density
would be D=66.6667. `v_2` stays 0.015 m³/kg, and `x_2` is the two-phase
quality at that volume. No fluid-name hint was printed. The call stays
`r134a`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `03-31.EES` (EES X9.920, 13 stored names),
compared with `compare_solution.py` without `--ees-units`. The tool's summary
line is:

`11 common variables, 2 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 0`

The two names only in EES are `T` and `P`, both stored as 1. They are not in
the equation window.

Differences above rtol 0.001:

- `x_1` prints 1.00e+00. The unrounded relative difference is 1. EES stores
  −100. CoolSolve returns 0. That is `quality()` outside the dome. `x_1`
  feeds no other equation.
- `T_3` prints 1.30e-03 (unrounded 1.297e-03). CoolSolve gives −12.7124453496 °C
  and EES stores −12.72895832 °C. The absolute difference is 0.0165 °C, the
  saturation temperature of R134a at 180 kPa.

Inside rtol: `P_2` prints 5.78e-04 (770196.303077 Pa against 770641.9152 Pa),
`x_2` prints 7.58e-04 (0.548766107515 against 0.5491822976), and `v_1` prints
1.65e-07 (7.569328309920×10⁻⁴ m³/kg against 0.0007569329561 m³/kg).

The maximum relative difference over all 11 common variables is 1.00e+00, on
`x_1`.

The window has no enthalpy call, so the comparison has no R134a
reference-state offset. All 11 equations are satisfied (max residual 0).
0 iterations with `.initials` and 0 without.

## Source and attribution

The equation window names nobody. The EES licence tag is the J. Lebrun
laboratory licence (University of Liège), not the author. The inventory
authors column names S. Quoilin for this KU Leuven course file, so `authors`
is `["S. Quoilin"]`.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/03-31.EES`
(EES X9.920, inventory row TM-0332, no duplicate group). The only comment
in the window, "properties of r134a", is English.

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `03-31.EES` (EES X9.920, plain text, `$UnitSystem SI MASS DEG PA C J`, 13 stored names, 11 equation-window equations, no tables, no warnings). `$UnitSystem` was deleted. The file has no `$TABSTOPS` and no `$Export`. No number was scaled: `T_1 = -8`, `p_1 = 320e3`, `T_2 = 30`, `v_2 = 0.015`, `p_3 = 180e3` and `x_3 = 1` stay. With `$UnitSystem` removed, CoolSolve reports System square: Yes (11 equations, 11 variables, largest block 1). `t_1`/`T_1` and `t_2`/`T_2` were left as written. The fluid token stays `r134a`. `T` and `P` stay only in the EES stored solution. No diagram-state array was added. Comments are in English, with SI units.
- **Level**: equations 11 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; three independent property states, not a discretised model and not coupled components → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

`quality()` at state 1 returns 0. EES stores −100 for that call, the value
it uses outside the dome. `x_1` feeds no equation. `missing_features` is
empty; `CS-GAP-QUALITY-DOME` is not listed.

`T_3` differs from the stored saturation temperature by 0.0165 °C
(printed relative difference 1.30e-03). `P_2` and `x_2` stay inside
rtol 0.001. The Fahrenheit hint on `t=30` and the specific-volume hint on
`v=0.015` do not change the arguments.

## Related models

`related` is empty. No other R134a model is linked.

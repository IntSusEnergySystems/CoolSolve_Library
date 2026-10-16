# Rigid 50 L vessel: heat removed from water at constant volume (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0230`

A closed rigid vessel of 50 L holds water at 120 °C with a vapour quality of
0.6. The model computes the mass of water, the final quality, and the heat
removed while the vessel is cooled at constant volume. Teaching exercise of
the ULiège course *Thermodynamique appliquée* (MECA0002), repetition 2
(2022-2023).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water |
| **Size** | 12 equations (largest block: 1) |
| **Source** | thermo_models, file `R2_E1_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise 1. A closed rigid vessel with a capacity of 50 L contains water at
120 °C with a quality of 60%. The statement says the vessel is cooled to
−10 °C. Calculate the heat transferred during the process.

The equation window stores `T_f = 10 [K]+273.15 [K]`, which is 10 °C
(283.15 K). The model follows the equation window.

## Model

One closed rigid vessel, with an initial state and a final state, as written
in the equation window. The volume is constant, so the process does no work.
The first law, as in the original, is

\[
Q = m(u_f - u_i)
\]

The mass follows from the initial specific volume. The specific volume is the
same at the final state. The final quality and two internal energies are
property calls at the stored final temperature.

Property calls pass `T - 273.15` because CoolSolve reads the temperature
argument as °C. `T_i` and `T_f` stay in kelvin. `intenergy` returns J/kg, so
`u_i`, `u_f`, `u_f_bis` and `Q` are in J. The equations are the original
products and quotients.

The original writes `intenergy(water,t=t_i,x=x_i)`. CoolSolve treats `t_i` and
`T_i` as one variable, and the system is square, so both spellings stay.
`volume` and `quality` keep the argument name `v`. `v_i` is a specific volume.

| Input | Value |
|---|---|
| `Vol` | 0.05 m³ (50 L, `50e-3`) |
| `T_i` | 120 °C, stored as `120 [K]+273.15 [K]` (393.15 K) |
| `x_i` | 0.6 |
| `T_f` | 10 °C, stored as `10 [K]+273.15 [K]` (283.15 K) |

Those four assignments are already equations. The system is square without
any further assignment (12 equations, 12 variables). The window is one vessel
with an initial state and a final state, so no diagram-state array is added.

## How to run

```bash
coolsolve ./rigid_vessel_water_heat_removal.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. There is no `abs()`, so the
guesses do not select a root. The `.initials` file is the EES stored
solution with `u_i`, `u_f`, `u_f_bis` and `Q` multiplied by 1000. The
temperatures stay in kelvin. The stored name `x` is omitted.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `Q` [J] | −155558.556 | −155538.904 (stored −155.5389041 kJ) | 1.26e-04 |
| `m_eau` [kg] | 0.093431492 | 0.093419626 | 1.27e-04 |
| `x_f` [−] | 0.005024835 | 0.005024752 | 1.64e-05 |
| `u_i` [J/kg] | 1718759.229 | 1718760.307 (stored 1718.760307 kJ/kg) | 6.27e-07 |
| `u_f` [J/kg] | 53811.439 | 53811.403 (stored 53.81140325 kJ/kg) | 6.61e-07 |
| `u_f_bis` [J/kg] | 53811.439 | 53811.403 (stored 53.81140325 kJ/kg) | 6.61e-07 |
| `v_i` [m³/kg] | 0.5351515 | 0.5352194 | 1.27e-04 |
| `T_i` | 393.15 K | 393.15 K | 6.95e-01 against 120 °C |
| `T_f` | 283.15 K | 283.15 K | 9.65e-01 against 10 °C |

`u_f` and `u_f_bis` are equal. `x_f` is about 0.005, inside the saturation dome.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R2_E1_2022.EES` (EES X10.836, 13 variables),
compared with `compare_solution.py --ees-units`. The tool's summary line is:

`12 common variables, 2 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 0`

`--ees-units` scaled `u_i`, `u_f`, `u_f_bis` and `Q` (kJ ×1000) and rewrote
`T_i` and `T_f` from K to °C. The name `x` is only in the EES reference. It
is the stored value 0 m². It is absent from the equation window, so the model
does not define it.

Every difference above rtol 0.001:

- `T_f` prints 9.65e-01. The equation window stores 283.15 K and the model
  keeps 283.15 K. The tool subtracts 273.15 and compares 283.15 with 10.
  In kelvin the two values are the same 283.15 K.
- `T_i` prints 6.95e-01. The equation window stores 393.15 K and the model
  keeps 393.15 K. The tool subtracts 273.15 and compares 393.15 with 120.
  In kelvin the two values are the same 393.15 K.

`Q` prints 1.26e-04 and `m_eau` prints 1.27e-04, both inside rtol 0.001.
`x_f` prints 1.64e-05. `u_i` prints 6.27e-07. `u_f` and `u_f_bis` print
6.61e-07. `v_i` and `v_f` print 1.27e-04. `Vol` and `x_i` match.

The largest relative difference over all 12 common variables, as printed by
the tool, is 9.65e-01, on `T_f`.

CoolSolve warns that `v=0.535151 m³/kg` is unusually large and suggests `D`.
`v_i` is the specific volume from `volume(Water, ...)`. The argument name
stays `v`. The solved quality is 0.005024835, so the final state is inside
the dome and `u_f = intenergy(Water, T=T_f-273.15, x=x_f)` uses that quality.

All 12 equations are satisfied (max residual 0).

## Source and attribution

The equation window names no person. The EES licence tag is the student and
staff licence of the Laboratoire de Thermodynamique, University of Liège. The
file itself names nobody. The inventory attributes the course to S. Quoilin,
so the authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R2/R2_E1_2022.EES`.

Candidate TM-0397, the representative of duplicate group DG-0082. Teaching
exercise. Course: *Thermodynamique appliquée* (ULiège, MECA0002), repetition 2,
2022-2023. EES X10.836.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R2_E1_2022.EES` (EES X10.836, plain text, decimal commas already rewritten as dots, 13 stored names, no tables). With `$UnitSystem` removed, the extraction is square: 12 equations, 12 variables, largest block 1. The thirteenth stored name is `x` = 0 m², which does not appear in the equation window, so it was not added. No diagram-state array was added. `$UnitSystem` was deleted. The file contains no `$TABSTOPS` and no `$Export`. Comments translated to English. `water` is written `Water`.
- **Units**: `$UnitSystem SI MASS DEG KPA K KJ`. There is no pressure input. `Vol = 50e-3` m³ stays. Temperatures stay in kelvin: `T_i = 120 [K]+273.15 [K]` and `T_f = 10 [K]+273.15 [K]`, as the equation window stores them. The statement text says the vessel is cooled to −10 °C; the window stores +10 °C, and that stored value is kept. Property calls pass `T-273.15` because CoolSolve reads the temperature argument as °C. `intenergy` returns J, so `u_i`, `u_f`, `u_f_bis` and `Q` are in J without multiplying the equations by 1000. `.initials`: those four stored results ×1000; temperatures and the other stored values left as stored; `x` omitted.
- **Case**: the original writes `intenergy(water,t=t_i,x=x_i)`. CoolSolve treats `t_i` and `T_i` as one variable. The converted window is square (12 equations, 12 variables), so both spellings stay.
- **Level**: equations 12 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one closed vessel, not discretised → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The statement cools the vessel to −10 °C. The equation window, and this model,
use 10 °C (283.15 K).

`compare_solution.py --ees-units` rewrites a stored kelvin temperature whose
name starts with `T` into °C, so `T_f` and `T_i` print large relative
differences while 283.15 K and 393.15 K agree with the stored kelvin values.

The stored name `x` is only in the EES solution. `quality()` warns that `v`
looks like a density. The value is the specific volume, and the call keeps `v`.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` is empty.

# Second-law efficiency of an R113 heat pump (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0228`

Teaching exercise for an R113 heat pump. The real COP is compared with the
Carnot COP taken between the saturation temperatures of the condenser and
of the evaporator, and the ratio is the second-law efficiency. Evaporator
inlet quality 0.35, saturated vapour at the evaporator outlet, 5 K of
superheat at the condenser inlet, and `h4 = h1` as written in the equation
window.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R113 |
| **Size** | 31 equations (largest block: 1): 15 in the equation window, 16 for the diagram state points |
| **Source** | ULiège, thermodynamique appliquée, MECA0002 — `Q1_rendement_II_principe.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified (see verification field) |

## Problem statement

Calculate the second-law efficiency of the heat pump. The ideal cycle may be
taken at the phase-change temperatures of the condenser and of the evaporator.

At the evaporator outlet (compressor inlet) the fluid is saturated, while at
the evaporator inlet its quality is 0.35.

The evaporator and condenser pressures are 45 kPa and 320 kPa.

The fluid is superheated by 5 °C at the condenser inlet.

## Model

R113, one operating point. Temperatures are kept in kelvin, as in the
equation window. CoolSolve property functions take °C, so only the property
boundary is shifted.

- `p1 = p2 = 45e3` Pa and `p3 = p4 = 320e3` Pa, already in pascal in the window.
- `T1 = T_sat(R113, P=p1) + 273.15` and `T_cond = T_sat(R113, P=p3) + 273.15`.
  `T2 = T1`. `T3 = T_cond + 5` is unchanged: both temperatures are in kelvin
  and 5 °C is the same interval.
- Carnot COP, unchanged, with those absolute temperatures:
  \(\mathrm{COP_{carnot}} = T_{cond}/(T_{cond}-T_1)\).
- `h1 = enthalpy(R113, x=0.35, P=p1)` and `h2 = enthalpy(R113, P=p2, x=1)`.
  Neither call has a temperature argument.
- `h3 = enthalpy(R113, T=T3-273.15, P=p3)`.
- `h4 = h1`, as in the original.
- \(\mathrm{COP_{reel}} = (h_3-h_4)/(h_3-h_2)\) and
  \(n_{\mathrm{II,principe}} = \mathrm{COP_{reel}}/\mathrm{COP_{carnot}}\times 100\)
  in percent.

Diagram states, post-processing only. State 1 is `(P, x) = (p1, 0.35)`.
State 2 is saturated vapour `(P, x) = (p2, 1)`. State 3 is `(T, P)` with
`T3-273.15`. State 4 is `(H, P) = (h4, p4)`. `(T, H)` is not used.
`temperature()` returns °C, so `T[4]` adds 273.15 and stays in kelvin with
`T[1]`, `T[2]` and `T[3]`.

| Inputs | Value | Outputs | CoolSolve |
|---|---|---|---|
| `p1` evaporator pressure | 45 kPa | `COP_reel` | 3.33573 |
| `p3` condenser pressure | 320 kPa | `COP_carnot` | 5.79692 |
| evaporator inlet quality | 0.35 | `n_II_principe` | 57.5432 % |
| condenser-inlet superheat | 5 K | `T1` / `T_cond` | 298.246 / 360.420 K |

## How to run

Open `r113_heat_pump_second_law.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./r113_heat_pump_second_law.eescode
```

The model is fully explicit (largest block: 1). It converges in 0 iterations
with `.initials` and in 0 iterations without it. No `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `COP_reel` | 3.33573 | 3.32517 |
| `COP_carnot` | 5.79692 | 5.81875 |
| `n_II_principe` | 57.5432 % | 57.1458 % |
| `T1` | 298.246 K | 298.355 K |
| `T_cond` | 360.420 K | 360.270 K |
| `T3` | 365.420 K | 365.270 K |
| `h1` = `h4` | 275721 J/kg | 109626 J/kg |
| `h2` | 374075 J/kg | 207959 J/kg |
| `h3` | 416184 J/kg | 250250 J/kg |

`T3 - T_cond = 5` K. The four pressures are 45 kPa and 320 kPa.

Diagram states (CoolSolve only; temperatures in kelvin):

| State | | `P` [Pa] | `T` [K] | `h` [J/kg] | `s` [J/kg-K] |
|---|---|---:|---:|---:|---:|
| 1 | evaporator inlet, x = 0.35 | 45000 | 298.246 | 275721 | 1257.21 |
| 2 | saturated vapour | 45000 | 298.246 | 374075 | 1586.99 |
| 3 | condenser inlet | 320000 | 365.420 | 416184 | 1631.50 |
| 4 | condenser pressure, `h4 = h1` | 320000 | 354.095 | 275721 | 1241.69 |

The saturation temperatures are about 25 °C and 87 °C. `T[4]` is 354.095 K,
below `T_cond`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `Q1_rendement_II_principe.EES` (EES X6.883,
15 variables), compared with `compare_solution.py --ees-units`. The tool's
summary line is:

`15 common variables, 9 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 16`

The 16 names only in CoolSolve are the diagram arrays `P[i]`, `h[i]`, `T[i]`
and `s[i]`.

`--ees-units` rewrote `T1` and `T_cond` from K to °C. Their stored unit is K
and the name starts with T. `T2` and `T3` have a blank stored unit, so they
were left in kelvin.

Every difference above rtol 0.001:

- `T1` prints 9.15e-01 (unrounded 0.91549) and `T_cond` prints 7.58e-01.
  The model keeps kelvin: 298.245733 K and 360.420202 K. The tool subtracts
  273.15 and then compares those values with 25.2045 °C and 87.1199 °C.
  That printed difference is not a model error. In kelvin the relative
  differences are 3.65e-04 and 4.17e-04. `T2` prints 3.65e-04 and `T3`
  prints 4.11e-04, inside rtol 0.001. `T3 - T_cond` is 5 in both solutions.
- `h1` and `h4` print 6.02e-01, `h2` prints 4.44e-01 and `h3` prints
  3.99e-01. CoolSolve minus the stored value is 166094.71 J/kg for `h1` and
  `h4`, 166116.30 J/kg for `h2` and 165934.32 J/kg for `h3`. The saturation
  states share an offset of about 166.1 kJ/kg (22 J/kg apart). The
  superheated `h3` sits 160 J/kg below that offset, so the differences do
  not cancel. `h3 - h2` is 42108.55 J/kg against the stored 42290.53 J/kg.
  `h3 - h4` is 140462.88 J/kg against the stored 140623.26 J/kg.
- `COP_reel` prints 3.17e-03: 3.33573274 against the stored 3.32517152.
  `COP_carnot` prints 3.75e-03: 5.79691647 against 5.81874955, from the
  saturation temperatures above. `n_II_principe` prints 6.91e-03: 57.543226
  against 57.145809.

`p1`, `p2`, `p3` and `p4` print 0.00e+00.

The largest relative difference over all 15 common variables, as printed by
the tool, is 9.15e-01 on `T1`.

All 31 equations are satisfied (maximum residual 0). The four pressures match
the window, and the saturation temperatures are about 25 °C and 87 °C.

`ees_extract.py` warns that every stored value equals its guess, so the
reference might be an unsolved file. The stored `COP_reel`, `COP_carnot` and
`n_II_principe` are the values implied by the stored enthalpies and
temperatures, so the comparison uses that solution. R113 has no separate
check here of an enthalpy origin at saturated liquid and −40 °C. The absolute
enthalpies are reported above, apart from the three performance figures.

CoolSolve accepted `R113`. No fluid-name warning was printed.

## Source and attribution

The equation window names nobody. The EES licence tag is
`{$ID$ #434: For use only by Kwangil Kim of Samsung Electronics Co.}`, the
licence holder, not the author. The file belongs to the ULiège MECA0002
course, so the authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/Aout 2022/Q1_rendement_II_principe.EES`.

Candidate TM-0457. Teaching exercise. Course: *Thermodynamique appliquée*
(ULiège, MECA0002). EES X6.883. Language: French.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `Q1_rendement_II_principe.EES` (EES X6.883, plain text, decimal comma converted to a dot, 15 variables, no tables). With `$UnitSystem` removed, the window is square: 15 equations, 15 variables, largest block 1, `System square: Yes`. No stored unknown was added. `h4 = h1` stays. `$UnitSystem` was deleted. No `$TABSTOPS` and no `$Export`. Comments translated to English. The diagram block was added after that square solve.
- **Units**: `$UnitSystem SI MASS DEG PA K J`. Pressures stay `45e3` Pa and `320e3` Pa; they were not multiplied by 1000. Enthalpies stay in J; they were not multiplied by 1000. Temperatures stay in kelvin. `T_sat` returns °C, so `T1` and `T_cond` add 273.15. `T3 = T_cond+5` is unchanged. `h3` passes `T3-273.15`. `h1` and `h2` stay enthalpy calls on `P` and `x`. The Carnot equation is still `T_cond/(T_cond-T1)` in kelvin. `.initials` is the stored solution: temperatures left in kelvin, pressures left in Pa.
- **Fluid**: `R113` left as `R113`. CoolSolve accepted the calls.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for i = 1…4. State 1 is `(P, x)`, state 2 is saturated vapour `(P, x=1)`, state 3 is `(T, P)` in °C at the call, state 4 is `(H, P)`. `(T, H)` is not used. `T[4]` adds 273.15. The 15 stored variables are unchanged by this block. After it, CoolSolve reports 31 equations, 31 variables, largest block 1, `System square: Yes`.
- **Level**: equations 31 → 0; largest block 1 → 0; diagram arrays → 1; four states of one explicit cycle, not three coupled component models → 0; one operating point, no calibration or off-design → 0; explicit, 0 iterations with and without guesses, no `coolsolve.conf` → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The window fixes the condenser-inlet state by 5 K of superheat and sets
`h4 = h1`. It does not solve a compressor efficiency. Absolute R113
enthalpies and entropies follow the CoolProp reference. The offset against
the stored enthalpies is about 166.1 kJ/kg and does not fully cancel, which
is why `COP_reel` and `n_II_principe` sit slightly off the stored figures.
`compare_solution.py --ees-units` rewrites a stored kelvin temperature whose
unit is K and whose name starts with `T`, so `T1` and `T_cond` print a large
relative difference while the stored kelvin values agree within 4.2e-04.

No CoolSolve gap. `missing_features` is empty. The source has no `$Export`.

## Related models

None. `related` is empty.

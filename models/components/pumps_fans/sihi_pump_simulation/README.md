# SIHI pump simulation from dimensionless polynomials

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0240`

Example simulation of a SIHI pump. Cubics give the dimensionless head and
absorbed-power coefficients as functions of the flow coefficient, and the
affinity-law definitions return the pressure rise and the shaft power at
the stated diameter, speed and volume flow. Water enters only through the
suction density.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | Water |
| **Size** | 14 equations (largest block: 1) |
| **Source** | Laborelec toolkit, 2002, example `Pumps_SIHI_simulation_021016.EES` |
| **Authors** | Felipe Trebilcock |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7d66c3b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The pump is represented by

`phi = V_dot / (D³ · ω)`, `psi = Δp / (ρ · ω² · D²)`, `lambda = W_dot_shaft / (ρ · ω³ · D⁵)`,

with `epsilon_s = psi · phi / lambda`. The cubics of `phi` are the
polynomials written in the equation window. Diameter, speed and volume
flow are inputs. The original calls the diameter and the speed catalogue
data.

## Model

Suction density is evaluated at the suction state. Rotational speed stays
in rev/min; `ω = rpm · 2π / 60`.

| Input | Value |
|---|---:|
| Volume flow | 0.00508 m³/s (stored solution) |
| Impeller diameter | 0.50 m |
| Speed | 2900 rev/min |
| Suction temperature | 20 °C |
| Suction pressure | 101300 Pa (101.3 kPa in the original) |
| Gravity | 9.81 m/s² |

The cubics in the equation window are

`psi = 0.06593 + 193.982·phi − 2.68298×10⁶·phi² + 2.14012×10⁹·phi³`

`Lambda = 0.000005387 + 0.07254·phi − 91.0212·phi² + 42483·phi³`

`g = 9.81` is an equation of the original. No other equation uses it.

The original brace comment lists `V_dot_p = 0.00211`. That line is a
comment. The equation is the stored volume flow, 0.00508 m³/s.

With `$UnitSystem` and the trailing NUL removed, and before `V_dot_p` is
assigned, CoolSolve reports 13 equations and 14 unknowns (`System square:
No`). The variable list contains `V_dot_p` and a single `Lambda_p`. The
efficiency equation still spells `lambda_p`. EES is case-insensitive, and
CoolSolve already treats the two spellings as one variable, so both
spellings stay. Assigning `V_dot_p = 0.00508` makes the window square:
14 equations, 14 unknowns, largest block 1 (`System square: Yes`).

The extractor also wrote a 6-row parametric table (`Table 1`, 6×9). Its
columns are `V_dot_1`, `DELTAP_1`, `W_dot_shaft_1`, `V_dot_2`, `DELTAP_2`,
`W_dot_shaft_2`, `V_dot_p`, `DELTAP_p` and `W_dot_shaft_p`. The last row
of `V_dot_p`, `DELTAP_p` and `W_dot_shaft_p` equals the stored solution
0.00508, 1127087.439 and 11852.78207. The equation window does not call
`INTERPOLATE` or `LOOKUP`. The polynomials are already equations. The
table is not part of this model.

## How to run

```bash
coolsolve ./sihi_pump_simulation.eescode
```

CoolSolve reports 3 iterations with the shipped `.initials` and 23
iterations without them. Both runs satisfy the equations. The `.sol`
baseline is the run with initials. Without initials the shaft power moves
to 11852.48048 W, the stored power times the suction-density ratio, and
the power-coefficient residual is 0. With the stored shaft power as a
guess, that equation keeps absolute residual 3.452e-10 and CoolSolve
reports all 14 equations satisfied.

## Results

Solved point, with the shipped initials. The EES column is the stored
solution. `P_w_su_p` is shown after the kPa scaling of `--ees-units`.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| Pressure rise `DELTAP_p` | 1127058.760 Pa | 1127087.439 Pa |
| Shaft power `W_dot_shaft_p` | 11852.78207 W | 11852.78207 W |
| `epsilon_s_p` | 0.483059939498 | 0.4830599395 |
| Flow coefficient `phi_p` | 0.000133821866633 | 0.0001338218666 |
| Head coefficient `psi_p` | 0.0489702867479 | 0.04897028675 |
| Power coefficient `Lambda_p` | 1.35662153830e-05 | 1.356621538e-05 |
| Suction density `rho_su_p` | 998.207139 kg/m³ | 998.2325392 kg/m³ |
| Angular speed `omega_p` | 303.687289847 rad/s | 303.6872898 rad/s |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
the extraction of `Pumps_SIHI_simulation_021016.EES`. The tool first
prints:

`Converted EES reference values: P_w_su_p (kPa x1000)`

Summary line, quoted as printed:

> 14 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

No common variable differs by more than rtol 0.001. The maximum relative
difference over all 14 common variables is **2.544516e-05** on `rho_su_p`.
`DELTAP_p` is **2.544491e-05**. `W_dot_shaft_p` matches the stored value.
`epsilon_s_p` differs by 4.14e-12.

`rho_su_p` is CoolProp water at 20 °C and 101300 Pa: 998.207139 kg/m³
against the stored 998.2325392 kg/m³. `psi`, `phi` and `Lambda` come from
the cubics and from `V_dot`, `D` and `ω`, so they match the stored
solution. `DELTAP = psi · ρ · ω² · D²` carries the density ratio, and that
defining equation is satisfied. With the shipped initials, `W_dot_shaft_p`
stays at the stored 11852.78207 W. The power-coefficient equation then has
absolute residual 3.452e-10, and CoolSolve reports all 14 equations
satisfied (max |residual| 3.4520e-10). Dividing that residual by `Lambda_p`
returns the same density ratio. Without initials the shaft power is
11852.48048 W and the residual of that equation is 0.

A blank stored unit is left unchanged. `--ees-units` scales only
`P_w_su_p`. `DELTAP_p` and `W_dot_shaft_p` have blank unit strings; their
stored values stay 1127087.439 Pa and 11852.78207 W. No stored unit is
`kJ`.

The name present only in the CoolSolve solution is `pi`.

## Source and attribution

The equation window names no person. Inventory row TM-0305 names Felipe
Trebilcock. EES version stamp: X6.596. The file is an example, in English,
in the Laborelec toolkit of 2002.

Source:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/3_Pumps and Fans/3_1_Pumps/Examples/Pumps_SIHI_simulation_021016.EES`
(inventory `TM-0305`).

## Conversion log

- **2026-10-16 — import** (`tools/ees_extract.py`): plain-text equations,
  EES X6.596, unit system `$UnitSystem SI MASS DEG KPA C KJ` (deleted).
  One trailing NUL byte was removed. `$TABSTOPS` and `$Export` are absent
  from the equation window. `origin.type` is `teaching` because the file
  is an example.
- **Square system.** With `$UnitSystem` and the NUL removed, CoolSolve
  reports 13 equations and 14 unknowns (`System square: No`). `V_dot_p` is
  used in the flow-coefficient definition and has no equation. The
  efficiency line divides by `lambda_p` while the polynomial assigns
  `Lambda_p`; the variable list has one `Lambda_p`, so the spellings stay.
  `V_dot_p = 0.00508` is the stored solution. The brace value 0.00211 stays
  a comment. After that assignment the system is square (14 equations,
  largest block 1).
- **Unit conversion** (hand). Suction pressure `101.3` kPa becomes
  `101300` Pa. Temperature stays 20 °C. `DELTAP_p` stays 1127087.439: the
  stored unit string is blank, and `psi = DELTAP/(rho·ω²·D²)` already
  returns pascals. `W_dot_shaft_p` stays 11852.78207 W: its stored unit
  string is blank. A blank unit is not scaled. `--ees-units` scales only
  `P_w_su_p` (`kPa x1000`). Speed stays in rev/min (original annotation
  `[rev/m]`). `g = 9.81` stays.
- **Catalogue table.** The 6-row parametric table was checked against the
  stored solution on its last `V_dot_p`, `DELTAP_p` and `W_dot_shaft_p`
  values and was left out. It was not turned into equations.
- **Level**: 14 equations (0), largest block 1 (0), no procedure, array or
  `DUPLICATE` (0), one pump (0), explicit cubics and affinity-law
  definitions at one speed and one volume flow (0), converges from the
  default guesses in 23 iterations (0) → score 0 → level 1.

## Limitations and CoolSolve gaps

The running model is one operating point: 0.00508 m³/s at 2900 rev/min
and D = 0.50 m. The cubics are the equation-window fit. Density is the
suction density only. `g` is assigned and unused by the other equations.
The catalogue points live in the parametric table of the source file and
are absent here.

No CoolSolve gap.

## Related models

None.

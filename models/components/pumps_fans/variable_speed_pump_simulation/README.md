# Variable-speed pump from dimensionless polynomials

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0203`

Predicts the running point of a centrifugal pump on a quadratic system
curve. Catalogue cubics give the dimensionless head and absorbed-power
coefficients as functions of the flow coefficient, and the affinity laws
return the speed and the shaft power. Motor and variable-frequency-drive
efficiencies depend on the fraction of catalogue speed, so the electrical
power is the wire-to-water power of the installation. Water enters only
through the suction density.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | Water |
| **Size** | 27 equations (largest block: 3) |
| **Source** | Laborelec toolkit, 2002 |
| **Authors** | TBD (Laborelec toolkit). The file itself names nobody |
| **License** | MIT |
| **CoolSolve** | 0.3.0@ae7946e — verified against the EES stored solution (see *Verification*) |

## Problem statement

The pump is represented, at fixed impeller diameter, by

`phi = V_dot / (D³ · ω)`, `psi = Δp / (ρ · ω² · D²)`, `lambda = W_dot_shaft / (ρ · ω³ · D⁵)`,

with `Δp = ρ · g · H` and `epsilon_s = psi · phi / lambda`. The head and
power coefficients are cubics of `phi`, identified from catalogue data and
labelled in the file for a Grundfos LP 100-200/210. The system curve is
the example `H = K · V_dot²`. The required speed is the one that places
the pump on both the cubic and the system curve at the imposed volume
flow.

Electrical power at the inlet of the pump and drive is

`W_dot_elec = W_dot_shaft / (eta_vfd · eta_motor)`.

`eta_motor` falls below the nameplate value as the percent of catalogue
speed decreases, and `eta_vfd` is a cubic of that same percent. The
nameplate efficiency is `1 − a · P_kW^b` for a 2-pole motor, with `P`
in kW.

## Model

Suction density is evaluated at the suction state. Head stays in m.
Rotational speed stays in rev/min; `ω = rpm · 2π / 60`.

| Input | Value |
|---|---:|
| System-curve coefficient | 130000 s²/m⁵ |
| Volume flow | 50/3600 m³/s |
| Impeller diameter | 0.210 m |
| Catalogue speed | 2960 rev/min |
| Nominal motor power | 23000 W (23 kW in the original) |
| 2-pole coefficients | a = 0.184, b = −0.236 |
| Suction temperature | 20 °C |
| Suction pressure | 101300 Pa (101.3 kPa in the original) |
| Gravity | 9.81 m/s² |

The cubics in the equation window are

`psi = 0.14125 − 0.44025·phi + 91.887·phi² − 15013.09·phi³`

`lambda = 0.0004725 + 0.179·phi − 8.369·phi² + 214.7057·phi³`

The original brace comment lists unused 4-pole, 6-pole and 8-pole pairs
`(a, b)`. Only the 2-pole pair is an equation.

With `$UnitSystem` and the trailing NUL removed, CoolSolve reports 26
equations and 26 unknowns (`System square: Yes`). No diagram-window input
was added. The extra equation in the library file is the conversion of
nominal motor power into kW for the nameplate correlation.

The speed is an algebraic loop of three unknowns (`omega`, `psi`, `phi`).
Eliminating `omega` leaves a cubic in `phi`. At this operating point that
cubic has one positive root (`phi ≈ 0.007429`) and two negative roots.
The shipped `.initials` are the stored solution, which is the positive root.

## How to run

```bash
coolsolve ./variable_speed_pump_simulation.eescode
```

CoolSolve reports 9 iterations with the shipped `.initials` and 34
iterations without them. Both stay on the positive flow coefficient.
Without initials the Newton stop is looser: shaft power differs from the
shipped solution by about 9.7e-05 relative. The `.sol` baseline is the
run with initials.

## Results

Solved point. The EES column is the stored solution, with `P_w_su_p` and
`W_dot_motor_nom_p` scaled by `--ees-units`.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| Head `H_p` | 25.07716049 m | 25.07716049 m |
| Speed `rpm_p` | 1927.66912 rev/min | 1927.66914 rev/min |
| Shaft power `W_dot_shaft_p` | 4790.379 W | 4790.501 W |
| Electrical power `W_dot_elec_p` | 5830.822 W | 5830.971 W |
| Effectiveness `epsilon_s_p` | 0.711976503 | 0.711976503 |
| Motor efficiency `eta_motor_p` | 0.909677864 | 0.909677865 |
| Drive efficiency `eta_vfd_p` | 0.903134526 | 0.903134527 |
| Wire-to-water `eta_vfd·eta_motor` | 0.821561487 | 0.821561488 |
| Flow coefficient `phi_p` | 0.007429310509 | 0.007429310509 |
| Head coefficient `psi_p` | 0.1368946762 | 0.1368946762 |
| Suction density `rho_su_p` | 998.207139 kg/m³ | 998.2325392 kg/m³ |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
the extraction of `3_1_2_Variable_speed_pump_simulation.EES`. The tool first
prints:

`Converted EES reference values: P_w_su_p (kPa x1000), W_dot_motor_nom_p (kW x1000)`

Summary line, quoted as printed:

> 26 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2

No common variable differs by more than rtol 0.001. The largest relative
difference the tool prints, over all 26 common variables, is **2.55e-05**
on `W_dot_elec_p` (exact ratio 2.546e-05). `rho_su_p`, `DELTAP_p` and
`W_dot_shaft_p` are **2.54e-05**.

`rho_su_p` is CoolProp water at 20 °C and 101300 Pa: 998.207139 kg/m³
against the stored 998.2325392 kg/m³. Head does not use density
(`H = K · V_dot²`), and `psi = g · H / (ω² · D²)`, so head, both
coefficients and speed match the stored solution. Shaft power and
electrical power are proportional to density, and they carry that same
relative difference. It is a property difference, not an equation error.

`DELTAP_p`, `W_dot_shaft_p` and `W_dot_elec_p` have empty stored unit
strings. Their stored values are already in Pa and W (245572 Pa, 4790 W,
5831 W). `--ees-units` does not scale them. No stored unit is `kj` or
`KJ`, and the file has no enthalpy.

Names present only in the CoolSolve solution: `pi`, and
`W_dot_motor_nom_kW_p` (nominal power in kW, introduced so the nameplate
correlation keeps its original coefficients).

## Source and attribution

The equation window and the variable list name no person. The file itself
names nobody, so `authors` is `TBD (Laborelec toolkit)`. Inventory row
TM-0302 attributes the Laborelec toolkit to Felipe Trebilcock, with
reviewers J. Lebrun and E. Winandy. That attribution is not written in
this file. There is no licence-holder tag. EES version stamp: X6.585.
The file is in English.

Source:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/3_Pumps and Fans/3_1_Pumps/3_1_2_Variable_speed_pump_simulation.EES`
(inventory `TM-0302`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): plain-text equations,
  EES X6.585, unit system `$UnitSystem SI MASS DEG KPA C KJ` (deleted, not
  an equation). No lookup table and no parametric table. A trailing NUL
  was removed. `lambda_p` in the effectiveness equation is the same EES
  name as `Lambda_p` and is written `Lambda_p`. `k_p = 130000` is the same
  name as `K_p` and is written `K_p`.
- **Unit conversion** (hand). Suction pressure `101.3` kPa becomes
  `101300` Pa. Nominal motor power `23` kW becomes `23000` W. The
  nameplate correlation `eta = 1 − a · P^b` was fitted with `P` in kW
  (`a = 0.184`, `b = −0.236` at 23 kW returns the stored 0.912209), so
  it is fed by `W_dot_motor_nom_kW_p = W_dot_motor_nom_p/1000`. Temperature
  stays 20 °C. Head stays in m. Speed stays in rev/min (original
  annotation `[rev/m]`). `DELTAP = rho·g·H` is already in Pa in the stored
  solution (empty unit string; 245572 Pa). Shaft and electrical power are
  already in W (empty unit strings). No enthalpy in kJ appears.
  `--ees-units` scales only `P_w_su_p` and `W_dot_motor_nom_p`.
- **Square system.** With `$UnitSystem` and the NUL removed, and before the
  kW auxiliary, CoolSolve reports 26 equations, 26 unknowns, largest block
  3 (`System square: Yes`). Diagram-window inputs were not restored. No
  computed unknown was replaced by a stored value.
- **Comment.** The original comment on the `omega` equation says it
  changes the result from rad/s to rpm. The equation multiplies rev/min by
  `2·pi/60`, which is rad/s. The trailing comment follows the equation.
- **Level**: 27 equations (0), largest block 3 (0), no procedure, array or
  `DUPLICATE` (0), one pump (0), semi-empirical cubics at a speed other
  than the catalogue speed, with part-load motor and VFD curves (1),
  converges from the default guesses in 34 iterations (0) → score 1 →
  level 1.

## Limitations and CoolSolve gaps

The system curve is the quadratic example written in the file. The cubics
are the Grundfos LP 100-200/210 fit of this equation window, not a new
identification. Diameter does not change. The motor correlation is the
2-pole pair; the 4-, 6- and 8-pole pairs stay comments. Density is the
suction density only.

No CoolSolve gap. `$Export`, `concat$` and `EESFILEDIR$` do not occur.

## Related models

- `CSL-0183` *pump_polynomial_identification*: the catalogue identification
  of the same affinity-law coefficients (TM-0301, file `3_1_1` beside this
  `3_1_2`). This file is the simulation companion: it takes cubics
  identified from catalogue data and solves the speed on a system curve.
  Both use `D = 0.210` m, a catalogue speed of 2960 rev/min, and water at
  20 °C and 101.3 kPa. The cubics are not the same numbers. This file’s
  equations are labelled Grundfos LP 100-200/210
  (`psi` linear term −0.44025). `CSL-0183` states a more precise cubic
  labelled RZR 800 (`psi` linear term −0.43544). The back-link is left for
  the orchestrator.
- `CSL-0318` *cordier_specific_speed*: 0D pre-design from the duty (specific speed, Cordier diameter, efficiency chart), before a pump is selected from a catalogue.

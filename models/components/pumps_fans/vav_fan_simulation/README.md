# Variable-speed fan from dimensionless polynomials

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0205`

Predicts the running point of a fan at a speed below the catalogue speed.
Catalogue quadratics give the dimensionless pressure and absorbed-power
coefficients as functions of the flow coefficient, and the affinity laws
return the pressure rise and the shaft power. Motor and
variable-frequency-drive efficiencies depend on the fraction of catalogue
speed, so the electrical power is the power at the drive inlet. Air enters
only as the constant density 1.2 kg/m³.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | Air at a fixed density 1.2 kg/m³ (no property call) |
| **Size** | 21 equations (largest block: 1) |
| **Source** | Laborelec toolkit, 2002 |
| **Authors** | TBD (Laborelec toolkit). The file itself names nobody |
| **License** | MIT |
| **CoolSolve** | 0.3.0@6730bcf — verified against the EES stored solution (see *Verification*) |

## Problem statement

The fan is represented, at fixed impeller diameter, by

`phi = V_dot / (D³ · ω)`, `psi = Δp / (ρ · ω² · D²)`, `lambda = W_dot_shaft / (ρ · ω³ · D⁵)`,

with `epsilon_s = psi · phi / lambda`. The pressure and power coefficients
are quadratics of `phi`, taken from a dimensionless curve identified from
catalogue data. Volume flow, diameter and running speed are imposed, so
the coefficients, the pressure rise and the shaft power follow directly.

Electrical power at the inlet of the drive is

`W_dot_elec = W_dot_shaft / (eta_vfd · eta_motor)`.

The original comment calls the product of the two efficiencies the
wire-to-water efficiency, and it says “pump” where this file is the fan
sheet. `eta_motor` falls below the nameplate value as the percent of
nominal speed decreases, and `eta_vfd` is a cubic of that same percent.
The nameplate efficiency is `1 − a · P_kW^b` for a 6-pole motor, with `P`
in kW.

## Model

Air density is the constant 1.2 kg/m³. Rotational speed stays at the stored
number 900; `ω = rpm · 2π / 60` is the conversion already present in the
file. That stored `ω` is 94.24777961 rad/s, which is 900 revolutions per
minute. The numeric assignment is annotated `[rev/s]` and the stored unit
string is `rev/s`. The equation that defines the percent of nominal speed
is annotated `[rev/m]`.

| Input | Value |
|---|---:|
| Volume flow | 7 m³/s |
| Impeller diameter | 0.808 m |
| Running speed | 900 (stored number; annotation `[rev/s]`) |
| Catalogue speed | 1200 (annotation `[rev/m]` on the percent-of-speed equation) |
| Nominal motor power | 15000 W (15 kW in the original) |
| 6-pole coefficients | a = 0.167, b = −0.239 |
| Suction density | 1.2 kg/m³ |

The quadratics in the equation window are

`psi = 0.115 + 0.358·phi − 2.200·phi²`

`lambda = 0.00187 + 0.1959·phi − 0.399·phi²`

The original brace comment lists unused 2-pole, 4-pole and 8-pole pairs
`(a, b)`. Only the 6-pole pair (1200 rpm) is an equation. Catalogue speed
in this file is 1200.

With `$UnitSystem` and the trailing NUL removed, CoolSolve reports 20
equations and 20 unknowns (`System square: Yes`). No diagram-window input
was added. The extra equation in the library file is the conversion of
nominal motor power into kW for the nameplate correlation.

Every block has size 1 and is explicit, so the solution is unique. There
is no `abs()`. The shipped `.initials` are the stored solution, with
nominal motor power in W.

## How to run

```bash
coolsolve ./vav_fan_simulation.eescode
```

CoolSolve reports 4 iterations with the shipped `.initials` and 17
iterations without them. Both stay on the stored point. Without initials,
`DELTAP_f`, `W_dot_shaft_f` and `W_dot_elec_` differ from the shipped
solution by at most 4.84e-11 relative. The `.sol` baseline is the run with
initials.

## Results

Solved point. The EES column is the stored solution, with
`W_dot_motor_nom_f` scaled by `--ees-units`.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| Pressure rise `DELTAP_f` | 847.5564622 Pa | 847.5564622 Pa |
| Shaft power `W_dot_shaft_f` | 7453.254866 W | 7453.254866 W |
| Electrical power `W_dot_elec_` | 8903.807396 W | 8903.807397 W |
| Effectiveness `epsilon_s_f` | 0.7960140022 | 0.7960140022 |
| Motor efficiency `eta_motor_f` | 0.9115390654 | 0.9115390654 |
| Drive efficiency `eta_vfd_f` | 0.918321875 | 0.918321875 |
| Nameplate efficiency `eta_motor_nom_f` | 0.9125760026 | 0.9125760026 |
| Wire-to-water `eta_vfd·eta_motor` | 0.837086264 | 0.837086264 |
| Speed `rpm_f` | 900 | 900 |
| Angular speed `omega_f` | 94.24777961 rad/s | 94.24777961 rad/s |
| Percent of nominal speed `X` | 75 | 75 |
| Suction density `rho_a_su_f` | 1.2 kg/m³ | 1.2 kg/m³ |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
the extraction of `3_2_2_VAV_Fan_simulation.EES`. The tool first prints:

`Converted EES reference values: W_dot_motor_nom_f (kW x1000)`

Summary line, quoted as printed:

> 20 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2

No common variable differs by more than rtol 0.001. The largest relative
difference the tool prints, over all 20 common variables, is **4.03e-10**
on `psi_f` (exact ratio 4.031e-10). The CSV stores 0.1217930249; CoolSolve
has 0.121793024949. The same stored-digit rounding accounts for the smaller
printed differences: `Lambda_f` 1.71e-10, `phi_f` 1.10e-10, `W_dot_elec_`
9.20e-11, `eta_motor_nom_f` 3.98e-11, `eta_motor_f` 3.48e-11, `omega_f`
2.45e-11 and `epsilon_s_f` 1.11e-11. `DELTAP_f` and `W_dot_shaft_f` print 0.

`DELTAP_f` is stored with unit `Pa` (847.5564622 Pa). `W_dot_shaft_f` and
`W_dot_elec_` are stored with unit `W` (7453.254866 W and 8903.807397 W).
`--ees-units` does not scale them. No stored unit is `kj` or `KJ`, and the
file has no enthalpy. Blank unit strings (`rho_a_su_f`, the efficiencies,
`X`, `a`, `b`) are not scaled. `rho_a_su_f` is the constant 1.2 kg/m³ in
the equation and in the stored solution.

Names present only in the CoolSolve solution: `pi`, and
`W_dot_motor_nom_kW_f` (nominal power in kW, introduced so the nameplate
correlation keeps its original coefficients).

## Source and attribution

The equation window and the variable list name no person. The file itself
names nobody, so `authors` is `TBD (Laborelec toolkit)`. Inventory row
TM-0307 attributes the Laborelec toolkit to Felipe Trebilcock, with
reviewers J. Lebrun and E. Winandy. That attribution is not written in
this file. There is no licence-holder tag. EES version stamp: X6.585.
The file is in English. A paragraph of the equation window still says
“pump” and “wire-to-water”; it reads as text carried over from the pump
sheet of the same toolkit.

Source:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/3_Pumps and Fans/3_2_Fans/3_2_2_VAV_Fan_simulation.EES`
(inventory `TM-0307`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): plain-text equations,
  EES X6.585, unit system `$UnitSystem SI MASS DEG KPA C KJ` (deleted, not
  an equation). No lookup table and no parametric table. A trailing NUL
  was removed. No `$Export`, `concat$`, `EESFILEDIR$` or `$TABSTOPS`.
  The unused 2-pole, 4-pole and 8-pole pairs were an EES brace comment
  (decimal commas); they are one comment, and the commas are transcribed
  to decimal points. The display string that calls the machine a pump and
  the combined efficiency wire-to-water is paraphrased in the comments
  above the electrical-power equations.
- **Unit conversion** (hand). Nominal motor power `15` kW becomes `15000` W.
  The nameplate correlation `eta = 1 − a · P^b` was fitted with `P` in kW
  (`a = 0.167`, `b = −0.239` at 15 kW returns the stored 0.912576), so
  it is fed by `W_dot_motor_nom_kW_f = W_dot_motor_nom_f/1000`. Pressure
  rise stays 847.5564622 Pa (stored unit `Pa`). Shaft power stays
  7453.254866 W and electrical power stays about 8903.807 W (stored unit
  `W`). Speed stays 900; the `ω` equation already divides by 60. No
  temperature and no energy in kJ appear. `--ees-units` scales only
  `W_dot_motor_nom_f`.
- **Square system.** With `$UnitSystem` and the NUL removed, and before the
  kW auxiliary, CoolSolve reports 20 equations, 20 unknowns, largest block
  1 (`System square: Yes`). Diagram-window inputs were not restored. No
  computed unknown was replaced by a stored value.
- **Level**: 21 equations (0), largest block 1 (0), no procedure, array or
  `DUPLICATE` (0), one fan (0), quadratics at a speed other than the
  catalogue speed, with part-load motor and VFD curves (1), converges from
  the default guesses in 17 iterations (0) → score 1 → level 1.

## Limitations and CoolSolve gaps

The running model is one operating point: 7 m³/s at the stored speed 900,
75 % of the catalogue speed 1200. The quadratics are the equation-window
fit, not a new identification. Diameter does not change. The motor
correlation is the 6-pole pair; the 2-, 4- and 8-pole pairs stay comments.
Density is the constant 1.2 kg/m³.

No CoolSolve gap. `$Export`, `concat$` and `EESFILEDIR$` do not occur.

## Related models

- `CSL-0187` *fan_polynomial_identification*: the catalogue identification
  of the same affinity-law coefficients (TM-0306, file `3_2_1` beside this
  `3_2_2`). This file is the simulation companion. It uses the quadratics
  stated in `CSL-0187`, rounded: `0.115891009 + 0.358857555·phi − 2.20079945·phi²`
  and `0.0018700149 + 0.195918348·phi − 0.39979922·phi²` become
  `0.115 + 0.358·phi − 2.200·phi²` and `0.00187 + 0.1959·phi − 0.399·phi²`.
  The diameters and speeds differ: this file uses `D = 0.808` m and a
  catalogue speed of 1200, while `CSL-0187` evaluates one point at
  `D = 0.570` m and 1800. A label in this file reads “RZR 0800” and
  “1200 rpm”; `CSL-0187` states those quadratics in a comment labelled
  RZR 800. The back-link is left for the orchestrator.

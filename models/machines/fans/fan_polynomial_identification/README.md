# Fan dimensionless coefficients from one catalogue point

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0187`

One catalogue point of a fan, reduced to the dimensionless flow, pressure
and power coefficients of the affinity laws. The Laborelec file (December
2002) describes a polynomial identification of those coefficients; the
equation window evaluates a single point, and the quadratic fits are
written out as a result.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | Air at a fixed density 1.2 kg/m³ (no property call) |
| **Size** | 13 equations (largest block: 1) |
| **Source** | Laborelec toolkit, December 2002 |
| **Authors** | TBD (Laborelec toolkit). Inventory attribution: Felipe Trebilcock (ULiège, December 2002, for Laborelec); reviewers J. Lebrun and E. Winandy |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The affinity laws represent a fan, at varying speed and fixed impeller
diameter, by the dimensionless group

`phi = V_dot / (D³ · ω)`, `psi = Δp / (ρ · ω² · D²)`, `lambda = W_dot_shaft / (ρ · ω³ · D⁵)`,

with `epsilon_s = psi · phi / lambda`. When the manufacturer gives
electrical motor power, the shaft power is that power times a fixed motor
efficiency (here 0.93), on the assumption that the motor is at full load.

The original text says that many catalogue points, placed in a parametric
table, collapse onto one normalised curve that can be fitted by a quadratic
in `phi`. This file contains no parametric table. It holds one point and,
as a comment, the quadratics labelled “For RZR 800”. The plot window shows
the same quadratics, rounded, and other curves labelled RZR 0560 (1800 rpm),
RZR 0450 (2100 rpm), RZR 0355 (2800 rpm), RZR 0315 (3200 rpm), RZR 0250
(4500 rpm) and RZR 8000 (4500 rpm).

## Model

Air density is the constant 1.2 kg/m³. The pressure coefficient uses the
catalogue pressure rise directly. The rotational speed stays at the stored
number 1800; `ω = rpm · 2π / 60` is the conversion already present in the
file. That stored `ω` is 188.4955592 rad/s. The original annotation on the
speed line is `[rev/s]`, and the stored unit string is `rev/s`.

| Input | Value |
|---|---:|
| Impeller diameter | 0.570 m |
| Speed | 1800 (stored number; annotation `[rev/s]`) |
| Volume flow | 2.7 m³/s |
| Pressure rise | 1800 Pa |
| Motor power | 7200/0.93 W |
| Motor efficiency | 0.93 |
| Suction density | 1.2 kg/m³ |

Volume flow and pressure rise are not assigned in the equation window. The
comment says they belong in the parametric table. With those two values and
the motor power restored, CoolSolve reports 13 equations and 13 unknowns
(`System square: Yes`). Before that restoration the count is 10 equations
and 13 unknowns.

The stored motor-power record is the EES +infinity marker (guess 1). The
shaft-power equation is `W_dot_shaft = W_dot_motor · eta`. The stored shaft
power is 7200 W, so the motor power that satisfies the equation is
`7200/0.93` W. The shaft power itself stays a computed unknown.

The quadratics stated in the file (decimal commas transcribed) are

`psi = 0.115891009 + 0.358857555·phi − 2.20079945·phi²`

`lambda = 0.0018700149 + 0.195918348·phi − 0.39979922·phi²`

They are comments. The solver does not identify the coefficients. The
equation window contains no EES optimisation directive.

## How to run

```bash
coolsolve ./fan_polynomial_identification.eescode
```

Every equation is an explicit assignment. CoolSolve reports 0 iterations
with the shipped `.initials` and 0 iterations without them.

## Results

Solved point. The EES column is the stored solution.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `phi_cat_f` | 0.07734603834 | 0.07734603834 |
| `psi_cat_f` | 0.1299389346 | 0.1299389346 |
| `Lambda_cat_f` | 0.01488927677 | 0.01488927677 |
| `epsilon_s_cat_f` | 0.675 | 0.675 |
| `W_dot_shaft_cat_f` | 7200 W | 7200 W |
| `W_dot_cat_motor_f` | 7741.93548387 W | +infinity marker |
| `omega_cat_f` | 188.4955592 rad/s | 188.4955592 rad/s |
| `DELTAP_cat_f` | 1800 Pa | 1800 Pa |
| `rho_a_su_f` | 1.2 kg/m³ | 1.2 kg/m³ |

Coefficients stated in the EES file (a comment, same numbers in the plot
to fewer digits). There is no EES solved value to set beside them.

| Term | `psi` quadratic | `lambda` quadratic |
|---|---:|---:|
| constant | 0.115891009 | 0.0018700149 |
| `phi` | 0.358857555 | 0.195918348 |
| `phi²` | −2.20079945 | −0.39979922 |

At the solved `phi`, the pressure quadratic returns `psi = 0.13048114`
(relative difference 4.17e-03 from the solved pressure coefficient). The
power quadratic returns `lambda = 0.01463176` (relative difference 1.73e-02
from the solved power coefficient).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
the extraction of `3_2_1_Fan_polynomial_identif.EES`. The tool prints no
`Converted EES reference values` line.

Summary line, quoted as printed:

> 13 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

Nothing sits above rtol 0.001. With `--all`, the largest printed relative
difference over the finite common variables is **2.46e-10**, on
`Lambda_cat_f`. The CSV stores 0.01488927677; the EES extended value is
0.014889276766330756, and CoolSolve matches that extended value. The same
rounding accounts for the smaller printed differences on `omega_cat_f`
(8.17e-11), `psi_cat_f` (1.31e-11) and `phi_cat_f` (2.07e-12).

`rho_a_su_f` is the constant 1.2 kg/m³ in the equation window and in the
stored solution. `psi_cat_f`, `Lambda_cat_f` and `epsilon_s_cat_f` satisfy
their equations at that density. The pattern in which stored head and power
coefficients were evaluated at a density other than the stored density does
not appear in this file.

`W_dot_cat_motor_f` is stored as the EES +infinity marker.
`compare_solution.py` skips a non-finite reference value, so that name is
one of the 13 common variables and is absent from the difference table.
CoolSolve uses `7200/0.93` W. `W_dot_shaft_cat_f` is 7200 W on both sides,
with a printed relative difference of 0.

The name present only in the CoolSolve solution is `pi`.

## Source and attribution

The equation window, the variable list and the plot annotations name no
person. `authors` is therefore `TBD (Laborelec toolkit)`. The inventory
row TM-0306 attributes the file to Felipe Trebilcock (University of Liège,
Thermodynamics Laboratory, December 2002, for Laborelec), with reviewers
J. Lebrun and E. Winandy. That attribution is not in the file. The reviewers
are not listed as authors. EES version stamp: X6.585. The file is in English.
Two paragraphs still say “pump” and one says “shat power”; they read as
text carried over from the pump sheet of the same toolkit.

Source:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/3_Pumps and Fans/3_2_Fans/3_2_1_Fan_polynomial_identif.EES`
(inventory `TM-0306`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): plain-text equations,
  EES X6.585, unit system `$UnitSystem SI MASS DEG KPA C KJ` (deleted).
  No lookup table and no parametric table. A trailing NUL on the last
  comment was removed. `lambda_cat_f` in the effectiveness equation is the
  same EES name as `Lambda_cat_f` and is written `Lambda_cat_f`. The
  quadratic result was one quoted string broken across two lines; it is
  two comment lines, and the decimal commas are transcribed to decimal
  points.
- **Unit conversion** (hand). No numerical input changes unit. The only
  pressure is `DELTAP_cat_f = 1800`, stored with unit `Pa`, and it stays
  1800 Pa. `--ees-units` scales no variable: no unit string is kPa, bar,
  kJ or kW. No temperature and no energy in kJ appear. Shaft power stays
  7200 W (stored unit `W`). Speed stays 1800; the `ω` equation already
  divides by 60. The variable list also holds `N_cat_f` and `w_cat_f`
  (both 125.6637061436 rad/s). Neither name appears in the equation
  window, so neither is imported.
- **Inputs restored from the stored solution.** With `$UnitSystem` and the
  NUL removed, CoolSolve reports 10 equations and 13 unknowns (`System
  square: No`). The three names with no equation are `DELTAP_cat_f`,
  `V_dot_cat_f` and `W_dot_cat_motor_f`. Pressure rise and volume flow are
  assigned their stored values 1800 Pa and 2.7 m³/s. The stored motor
  power is the EES +infinity marker. `W_dot_cat_motor_f = 7200/0.93` is
  the stored shaft power divided by `eta_cat_motor_f = 0.93`, which is
  what the shaft-power equation requires in order to return the stored
  7200 W. No computed unknown is replaced.
- **Level**: 13 equations (0), largest block 1 (0), no procedure or array
  (0), one fan (0), explicit definitions of the dimensionless groups at
  one point (0), 0 iterations from the default guesses (0) → score 0 →
  level 1.

## Limitations and CoolSolve gaps

The running model is one catalogue point. The multi-point fit described in
the comments is the pair of quadratics transcribed above; this file does not
minimise an error and does not contain the catalogue series. Motor
efficiency is constant. Suction density is the constant 1.2 kg/m³.

No CoolSolve gap. The equation window has no `$Export`, `concat$` or
optimisation directive.

## Related models

- `CSL-0205` *vav_fan_simulation*: the Laborelec simulation that uses the
  RZR 800 quadratics of this identification below catalogue speed, with
  part-load motor and VFD efficiencies.
- `CSL-0183` *pump_polynomial_identification*: the pump counterpart in the
  same Laborelec toolkit (one catalogue point, the same motor efficiency,
  affinity-law coefficients, polynomial fit left as a comment). The pump
  file uses water density and a head in m; this file uses a fixed air
  density and a pressure rise in Pa. `CSL-0183` does not yet list
  `CSL-0187` (that back-link is left for the orchestrator; this import
  does not edit `CSL-0183`).

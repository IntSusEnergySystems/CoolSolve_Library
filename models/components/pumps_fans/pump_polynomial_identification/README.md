# Pump dimensionless coefficients from one catalogue point

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0183`

One catalogue point of a centrifugal pump, reduced to the dimensionless
flow, head and power coefficients of the affinity laws. The Laborelec
file (December 2002) describes a polynomial identification of those
coefficients; the equation window evaluates a single point, and the cubic
fits are written out as a result.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | Water |
| **Size** | 17 equations (largest block: 1) |
| **Source** | Laborelec toolkit, December 2002 |
| **Authors** | TBD (Laborelec toolkit). Inventory attribution: Felipe Trebilcock; reviewers J. Lebrun and E. Winandy |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The affinity laws represent a pump, at varying speed and fixed impeller
diameter, by the dimensionless group

`phi = V_dot / (D³ · ω)`, `psi = Δp / (ρ · ω² · D²)`, `lambda = W_dot_shaft / (ρ · ω³ · D⁵)`,

with `Δp = ρ · g · H` and `epsilon_s = psi · phi / lambda`. When the
manufacturer gives electrical motor power, the shaft power is that power
times a fixed motor efficiency (here 0.93), on the assumption that the
motor is at full load.

The original text says that many catalogue points, placed in a parametric
table, collapse onto one normalised curve that can be fitted by a cubic in
`phi`. This file contains no parametric table. It holds one point and, as
a comment, the cubics labelled “For RZR 800”. The plot window shows the
same cubics, rounded, with the label `LP 100-200/210` at 2960 rpm.

## Model

Water density is evaluated at the suction state. Head stays in m. The
rotational speed stays in rev/min; `ω = rpm · 2π / 60` is the conversion
already present in the file.

| Input | Value |
|---|---:|
| Impeller diameter | 0.210 m |
| Speed | 2960 rev/min |
| Volume flow | 0.04992 m³/s |
| Head | 35.61 m |
| Motor power | 28500 W |
| Motor efficiency | 0.93 |
| Suction temperature | 20 °C |
| Suction pressure | 101300 Pa (101.3 kPa in the original) |
| Gravity | 9.81 m/s² |

Volume flow, head and motor power are not assigned in the equation window.
The comment says they belong in the parametric table. Restoring the stored
values makes the system square (14 equations and 17 unknowns before that).

The cubics stated in the file (decimal commas transcribed) are

`psi = 0.141245568 − 0.43543986·phi + 91.1642763·phi² − 14983.2745·phi³`

`lambda = 0.000472721306 + 0.179348056·phi − 8.35199824·phi² + 214.071727·phi³`

They are comments. The solver does not identify the coefficients.

## How to run

```bash
coolsolve ./pump_polynomial_identification.eescode
```

Every equation is an explicit assignment. CoolSolve reports 0 iterations
with the shipped `.initials` and 0 iterations without them.

## Results

Solved point. The EES column is the stored solution.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `phi_cat_p` | 0.017389871 | 0.017389871 |
| `psi_cat_p` | 0.082444509 | 0.082444509 |
| `Lambda_cat_p` | 0.002182980 | 0.002180066 |
| `epsilon_s_cat_p` | 0.656763 | 0.657640 |
| `DELTAP_cat` | 348707.79 Pa | 349173.80 Pa |
| `rho_su_p` | 998.207 kg/m³ | 998.233 kg/m³ |
| `W_dot_shaft_cat_p` | 26505 W | 26505 W |
| `omega_cat_p` | 309.97048 rad/s | 309.97048 rad/s |

Coefficients stated in the EES file (a comment, same numbers in the plot
to fewer digits). There is no EES solved value to set beside them.

| Term | `psi` cubic | `lambda` cubic |
|---|---:|---:|
| constant | 0.141245568 | 0.000472721306 |
| `phi` | −0.43543986 | 0.179348056 |
| `phi²` | 91.1642763 | −8.35199824 |
| `phi³` | −14983.2745 | 214.071727 |

At the solved `phi`, the head cubic returns `psi = 0.08244761` (relative
difference 3.76e-05 from the solved head coefficient). The power cubic
returns `lambda = 0.00219162` (relative difference 3.96e-03 from the
solved power coefficient).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
the extraction of `3_1_1_Pump_polynomial_identif.EES`. The tool first prints
`Converted EES reference values: P_w_su_p (kPa x1000)`.

Summary line, quoted as printed:

> 17 common variables, 3 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

| Variable | EES (after `--ees-units`) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `DELTAP_cat` | 349174 | 348708 | 1.33e-03 |
| `Lambda_cat_p` | 0.00218007 | 0.00218298 | 1.33e-03 |
| `epsilon_s_cat_p` | 0.65764 | 0.656763 | 1.33e-03 |

Maximum relative difference over all 17 common variables: **1.33e-03**
(the exact ratio is 1.3346e-03 on each of the three).

`DELTAP_cat = rho·g·H` and `Lambda_cat_p = W_dot_shaft/(rho·ω³·D⁵)` at the
stored `rho_su_p` of 998.2325392 kg/m³ give 348716.67 Pa and 0.002182924.
The stored pressure rise 349173.7985 Pa and the stored power coefficient
0.002180066199 are those expressions at 999.541 kg/m³. The stored
effectiveness is `psi·phi/lambda` with that stored power coefficient.
`psi_cat_p` does not depend on density (`psi = g·H/(ω²·D²)`) and agrees.
CoolSolve satisfies the equations at the density it computes.

`rho_su_p` itself is under the tolerance: EES 998.2325392 kg/m³, CoolSolve
998.207139 kg/m³, relative difference **2.54e-05** (CoolProp water at
20 °C and 101300 Pa). That property difference is the whole of the gap
between CoolSolve and the equation-consistent EES density; it is not the
1.33e-03 gap.

The name present only in the CoolSolve solution is `pi`.

## Source and attribution

The equation window, the variable list and the plot annotations name no
person. `authors` is therefore `TBD (Laborelec toolkit)`. The inventory
row TM-0301 attributes the file to Felipe Trebilcock (University of Liège,
Thermodynamics Laboratory, December 2002, for Laborelec), with reviewers
J. Lebrun and E. Winandy. That attribution is not in the file. EES version
stamp: X6.585. The file is in English.

The inventory description of duplicate group DG-0071 names a SIHI/Grundfos
example. This file’s result comment is labelled “For RZR 800”, and the plot
annotation is labelled `LP 100-200/210` at 2960 rpm. Neither SIHI nor
Grundfos appears in the file.

Source:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/3_Pumps and Fans/3_1_Pumps/3_1_1_Pump_polynomial_identif.EES`
(inventory `TM-0301`, representative of DG-0071).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): plain-text equations,
  EES X6.585, unit system `$UnitSystem SI MASS DEG KPA C KJ` (deleted).
  No lookup table and no parametric table. A trailing NUL on the last
  comment was removed. `lambda_cat_p` in the effectiveness equation is the
  same EES name as `Lambda_cat_p` and is written `Lambda_cat_p`.
- **Unit conversion** (hand). The only value whose unit changes is the
  suction pressure: `P_w_su_p = 101.3` kPa becomes `101300` Pa. Temperature
  stays 20 °C. Head stays 35.61 m. Speed stays 2960 rev/min (original
  annotation `[rev/m]`; the `ω` equation already divides by 60). Motor
  power stays 28500 W: the stored unit string is `W`, and
  `28500 · 0.93 = 26505` matches the stored shaft power, so the kJ setting
  does not scale it. `DELTAP_cat = rho·g·H` is already in Pa (stored unit
  string `Pa`); no factor was added. No enthalpy, heat or energy in kJ
  appears. `--ees-units` scales only `P_w_su_p`.
- **Inputs restored from the stored solution.** With `$UnitSystem` and the
  NUL removed, CoolSolve reports 14 equations and 17 unknowns (`System
  square: No`). The three names with no equation are `V_dot_cat_p`,
  `H_cat_p` and `W_dot_cat_motor_p`. They are assigned their stored values
  0.04992 m³/s, 35.61 m and 28500 W. No computed unknown is replaced.
- **Level**: 17 equations (0), largest block 1 (0), no procedure or array
  (0), one pump (0), explicit definitions of the dimensionless groups at
  one point (0), 0 iterations from the default guesses (0) → score 0 →
  level 1.

## Limitations and CoolSolve gaps

The running model is one catalogue point. The multi-point fit described in
the comments is the pair of cubics transcribed above; this file does not
minimise an error and does not contain the catalogue series. Motor
efficiency is constant. The head uses `Δp = ρ·g·H` with the suction density.

No CoolSolve gap. `$Export` and `concat$` do not occur.

## Related models

- `CSL-0203` *variable_speed_pump_simulation*: the Laborelec simulation that
  uses the LP 100-200/210 cubics of this identification on a quadratic system
  curve, with part-load motor and VFD efficiencies.
- `CSL-0125` *pump_curve_similarity*: manufacturer curves and affinity laws
  for a pump, as a translation of the LaboThapPy component. It interpolates
  tabulated flow, head, efficiency and NPSH and scales them to another
  speed (fluid R744, three operating modes). The equations of this file
  are the dimensionless coefficients at one water point.
- `CSL-0187` *fan_polynomial_identification*: the fan counterpart in the
  same Laborelec toolkit, one catalogue point at a fixed air density.

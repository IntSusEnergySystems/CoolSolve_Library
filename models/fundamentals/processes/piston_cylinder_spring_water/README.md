# Water heated in a spring-loaded piston-cylinder (exercise 4.21)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0210`

A frictionless piston-cylinder holds 4 kg of saturated water at 35 °C. The
piston rests on stops until the pressure reaches 300 kPa, rises at that
pressure until the volume is 75 L, then compresses a linear spring while
heating continues to 7 MPa. The model computes the final state and the
boundary work on the piston. Teaching exercise 4.21 of the French edition
of Cengel.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water |
| **Size** | 39 equations (largest block: 1) |
| **Source** | thermo_models, file `R2_E2_borguet.EES` |
| **Authors** | TBD (ULiège THD) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@d1e1203 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A frictionless piston of area 0.06 m² rests on stops, and the enclosed volume
is then 30 L. The piston mass is such that 300 kPa is required to lift it at
ambient pressure. When the volume reaches 75 L the piston meets a spring that
needs 360 kN to compress by 1 m. The cylinder initially holds 4 kg of
saturated water (liquid and vapour) at 35 °C. The system is heated until the
internal pressure is 7 MPa. Determine the final state of the water and the
work of the process.

The source computes each stage as a positive integral of \(P\,\mathrm{d}V\)
and signs the total at the end, so the work of the fluid is negative.

## Model

Three stages, as written in the equation window:

1. Constant volume, from the initial saturated mixture up to the lift-off
   pressure. The boundary work is zero.
2. Constant pressure at the lift-off pressure, until the piston meets the
   spring.
3. Compression of the spring. The pressure rise above the lift-off pressure
   is \(k\,\Delta h / A\), and the boundary work is the integral of that
   linear \(P(V)\) law.

The initial pressure is the saturation pressure of Water at 35 °C. The other
states are fixed by pressure and specific volume. `h_3` and `h_4` are piston
heights in metres. The equation window stores the four states as `p[i]` and
`v[i]` for a Clapeyron diagram.

- \(p_1 = p_\mathrm{sat}(T_1)\)
- \(W_{12} = 0\)
- \(W_{23} = p_2\,(V_3 - V_2)\)
- \(\Delta p_{34} = p_4 - p_3 = k\,(h_4 - h_3)/A_p\)
- \(W_{34} = p_2\,(V_4 - V_3) + \dfrac{k}{2 A_p^2}(V_4 - V_3)^2\)
- \(W = -(W_{12} + W_{23} + W_{34})\)

| Input | Value |
|---|---|
| `A_p` | 0.06 m² |
| `k_ressort` | 360 kN/m (360×10³ N/m) |
| `m_eau` | 4 kg |
| `Vol_1` | 0.030 m³ (30 L) |
| `T_1` | 35 °C |
| `p_2` | 300 kPa (300×10³ Pa) |
| `Vol_3` | 0.075 m³ (75 L) |
| `p_4` | 7000 kPa (7×10⁶ Pa) |

Those eight assignments are already equations. The system is square without
any further assignment (39 equations, 39 variables). The stored solution also
contains `k` = 1, with a blank unit string. That name is absent from the
equation window, so it is not restored. The Clapeyron arrays `p[i]` and
`v[i]` are the arrays the equation window already contains.

Heat transfer is outside this equation window. The final state and the work
are the results the source computes.

## How to run

```bash
coolsolve ./piston_cylinder_spring_water.eescode
```

Every block is explicit (largest block 1). CoolSolve reports 2 iterations
with the shipped `.initials` and 3 iterations without them. There is no
`abs()` call: the spring law is linear in the piston height, and the stored
physical root is the only root. The `.initials` file is the EES stored
solution converted to Pa, N/m and J. The guess `x_4 = 100` is the EES
superheated sentinel; the solved quality is 0.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `W` | −258050 J | −258.05 kJ |
| `W_12` | 0 J | 0 kJ |
| `W_23` | 13500 J | 13.5 kJ |
| `W_34` | 244550 J | 244.55 kJ |
| `p_4` | 7×10⁶ Pa | 7000 kPa |
| `T_4` | 352.359 °C | 352.668 °C |
| `Vol_4` | 0.142 m³ | 0.142 m³ |
| `v_4` | 0.0355 m³/kg | 0.0355 m³/kg |
| `x_4` | 0 | 100 |
| `p_1` | 5629.02 Pa | 5.62669 kPa |
| `T_2`, `T_3` | 133.522 °C | 133.532 °C |
| `h_4` | 2.36667 m | 2.36667 m |

Heat is not a stored result and is not an equation. `T_4`, `p_1` and the
qualities are printed at the digits of `compare_solution.py`. The final
water is superheated vapour at 7 MPa and about 352.4 °C. The piston height
goes from 1.25 m at spring contact to 2.367 m.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R2_E2_borguet.EES` (EES X8.423, 40 stored variables). The tool converted
`p_1`, `p_2`, `p_3`, `p_4`, `DELTAp_34` and `p[1]`…`p[4]` (kPa ×1000) and
`W_12`, `W_23`, `W_34` and `W` (kJ ×1000):

> 39 common variables, 2 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 0

The two differences, quoted as the tool prints them:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `k_ressort` | 360 | 360000 | 9.99e-01 |
| `x_4` | 100 | 0 | 1.00e+00 |

Maximum relative difference over all common variables: **1.00e+00** (`x_4`).

`k_ressort` is stored as `kN/m`. `--ees-units` scales kPa and kJ; it does
not scale `kN`. The model value 360000 N/m is the original 360 kN/m. The
spring work that uses it, `W_34`, matches at 244550 J (relative difference 0).

`x_4` is the final quality. The unit string is blank, so `--ees-units` leaves
100 unscaled. EES returns 100 for superheated vapour. CoolSolve returns 0.
`x_4` is not used in any other equation, so the work and the final
temperature are unchanged. The name only in the EES reference is `k` (stored
value 1, blank units), which the equation window does not contain.

Water enthalpy is absent from the equation window, so there is no enthalpy
residual and no reference-state offset to report. `h_3` and `h_4` are piston
heights; `h_4` agrees to a relative difference of 1.41e-10.

The property residuals stay under rtol = 0.001. They are Water formulation
differences, a few pascals or a fraction of a degree, not a constant shift:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_4` | 352.668 | 352.359 | 8.74e-04 |
| `x_3` | 0.0292094 | 0.0292331 | 8.10e-04 |
| `x_2` | 0.0106198 | 0.0106284 | 8.05e-04 |
| `x_1` | 0.000257498 | 0.000257653 | 6.01e-04 |
| `p_1` | 5626.69 | 5629.02 | 4.14e-04 |
| `T_2` | 133.532 | 133.522 | 7.10e-05 |
| `T_3` | 133.532 | 133.522 | 7.10e-05 |

`W`, `W_12`, `W_23`, `W_34`, the volumes and the assigned pressures agree
exactly (relative difference 0). `p_1` differs by about 2.3 Pa.

`P_sat` prints a hint that `t=35` looks like Fahrenheit and shows 1.67 °C.
`T_1` remains 35 °C: `p_1` is the saturation pressure near 5.63 kPa, which is
the saturation pressure at 35 °C. The specific-volume hints on 0.0075,
0.01875 and 0.0355 m³/kg describe the wet-mixture and final volumes. Those
three values match the stored solution exactly.

## Source and attribution

The file itself names nobody. The filename is `R2_E2_borguet.EES`. The
inventory attributes the ULiège THD course to S. Bertagnolio and S. Borguet.
The `{$ID$}` licence tag is the Laboratoire de Thermodynamique, University of
Liège, and is not an author. Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R02/R2_E2_borguet.EES`
(EES X8.423, inventory row TM-0360). The statement is exercise 4.21 of the
French edition of Cengel. The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X8.423, unit
  system `SI MASS DEG KPA C KJ`, 40 stored variables, 0 tables). Decimal
  comma `0,5` written as `0.5`; semicolons in the property calls written as
  commas. `$UnitSystem` deleted. Pressures converted by hand from kPa to Pa:
  `p_2` 300 kPa → `300e3` Pa, `p_4` 7000 kPa → `7000e3` Pa. Spring stiffness
  `k_ressort` 360 kN/m → `360e3` N/m, so that \(k\,\Delta h/A\) stays in Pa
  and the \(P\,\mathrm{d}V\) integrals stay in J. `T_1` stays 35 °C.
  `A_p`, `m_eau`, `Vol_1` and `Vol_3` are unchanged. No `*1000` factor was
  removed from an equation: the source had none, and every term of the work
  and spring equations scales together. Property calls are unchanged
  (`P_sat(Water,…)`, `quality(water,…)`, `temperature(water,…)`). The system
  is square (39 equations, 39 variables), so no Diagram-window input was
  restored and the unused stored name `k` was left out. No extra
  diagram-state arrays were added. Comments translated to English
  (paraphrases of the original French statement and equation comments).
  Variable names unchanged, including `h_3` and `h_4` for piston height.
  Guesses in `.initials` are the stored solution in SI: pressures and
  `DELTAp_34` ×1000, works ×1000, `k_ressort` ×1000; lengths, volumes,
  temperatures and qualities unchanged, with `x_4` left at 100.
- **Level**: equations 39 → 0; largest block 1 → 0; arrays present (`p[i]`,
  `v[i]` in the original equation window) → 1; no multi-zone or discretised
  component → 0; no semi-empirical, off-design or dynamic physics → 0;
  explicit, 2 iterations with guesses and 3 without, no `coolsolve.conf` → 0.
  Score 1 → level 1.

## Limitations and CoolSolve gaps

The final pressure is an assigned input, as in the source. Heat transfer is
outside the equation window. EES `quality` returns 100 for this superheated
vapour; CoolSolve returns 0 (`CS-GAP-QUALITY-DOME`, not blocking: `x_4` is a
diagnostic output only). The `.sol` file labels `v_1` to `v_4` as kg/m³
(`CS-BUG-UNIT-VOLUME`); the values are specific volumes in m³/kg. No gap
blocks the file.

## Related models

None linked. `CSL-0176` is a different piston-cylinder exercise: water heated
at constant pressure (Cengel 3-55), with the mass and the final volume as the
results. The equations are not the same, so it is not linked.

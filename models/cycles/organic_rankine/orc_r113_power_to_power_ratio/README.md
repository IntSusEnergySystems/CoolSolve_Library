# R113 power-to-power ratio of an ORC and a heat pump (example)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0229`

Teaching example for an R113 installation. The ORC turbine electrical power
follows from a given enthalpy drop of 17.5 kJ/kg. The heat-pump compressor
electrical power follows from the saturated evaporator exit and a condenser
inlet superheated by 5 °C. The result is the absolute ratio of the turbine AC
output to the compressor AC input. ULiège course *Thermodynamique appliquée*
(MECA0002), August 2022.

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R113 |
| **Size** | 18 equations (largest block: 1) |
| **Source** | thermo_models, file `Q5_power_to_power_ratio.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

The ORC turbine has an isentropic efficiency of 89 %, and the fluid enthalpy
changes by 17.5 kJ/kg inside it. The refrigerant flow in the ORC is 1.2 kg/s.

To characterise the installation under the given conditions, an engineer
defines a power-to-power ratio, in absolute value: the electrical power
delivered by the turbine (AC) divided by the electrical power consumed
upstream by the compressor (also AC). The compressor is driven mechanically
by an electric motor, and that motor is fed from the grid through a converter.
The turbine drives an electric generator, which also needs a converter to
reinject power into the grid, and a mechanical link to the turbine shaft.
The mechanical efficiency of each link is the same, 97 %, and the converter
efficiency is 92 %. Calculate the power-to-power ratio.

The fluid flow in the heat pump is 200 g/s. The evaporator and condenser
pressures are 45 kPa and 320 kPa. The fluid is superheated by 5 °C at the
condenser inlet. At the evaporator outlet (compressor inlet) the fluid is
saturated.

The equation window uses the given enthalpy drop of 17.5 kJ/kg. The 89 %
isentropic efficiency stays in the statement.

## Model

The window computes the heat-pump compressor inlet and outlet, and a given
turbine enthalpy drop. It does not build a cycle of states.

The compressor inlet is saturated vapour at the evaporator pressure. The
condenser inlet is 5 °C above the saturation temperature at the condenser
pressure. Temperatures are stored in kelvin. `T_sat` returns °C, so the
saturation results are shifted once:

\[
T_2 = T_\mathrm{sat}(\mathrm{R113}, p_2) + 273.15
\]
\[
T_\mathrm{cond} = T_\mathrm{sat}(\mathrm{R113}, p_3) + 273.15
\]
\[
T_3 = T_\mathrm{cond} + 5
\]

The interval of 5 is unchanged: both temperatures are in kelvin, and 5 °C is
the same interval. The compressor-outlet enthalpy passes °C into the property
call. The saturated-vapour enthalpy does not:

\[
h_2 = h(\mathrm{R113}, p_2, x=1)
\]
\[
h_3 = h(\mathrm{R113}, T=T_3-273.15, p_3)
\]

Electrical compressor power, turbine fluid power and turbine electrical power:

\[
\dot W_{cp} = \frac{\left|\dot m_{pac}(h_3-h_2)\right|}{\eta_{meca}\,\eta_{conv}}
\]
\[
\dot W_{turb} = \dot m_{orc}\,\Delta h_{turb}
\]
\[
\dot W_{turb,elec} = \dot W_{turb}\,\eta_{meca}\,\eta_{conv}
\]
\[
\mathrm{Power\_to\_power\_ratio} = \dot W_{turb,elec} / \dot W_{cp}
\]

`abs()` is the absolute value written in the original. The efficiencies stay
0.97 and 0.92.

| Input | Value |
|---|---|
| `m_dot_orc` | 1.2 kg/s |
| `m_dot_pac` | 0.2 kg/s (200 g/s) |
| `delta_h_turb` | `17.5*1000` J/kg (17.5 kJ/kg) |
| `p1`, `p2` | 45e3 Pa (45 kPa written as 45e3) |
| `p3`, `p4` | 320e3 Pa (320 kPa written as 320e3) |
| `eta_meca` | 0.97 |
| `eta_conv` | 0.92 |

`p2 = p1` and `p4 = p3`. `p4` is not used by a later equation. Both assignments
stay. Those inputs are already equations. The system is square without any
further assignment (18 equations, 18 variables). No diagram-state array is
added.

## How to run

```bash
coolsolve ./orc_r113_power_to_power_ratio.eescode
```

Every block is explicit (largest block 1). CoolSolve reports 0 iterations
with the shipped `.initials` and 0 iterations without them. Without initials
the compressor power is the same positive value, 9437.147538742 W. The
`.initials` file is the EES stored solution, including the stored positive
compressor power `W_cp = 9477.931285` W. Temperatures stay in kelvin and
pressures stay in pascal.

## Results

Powers, compared with the stored solution on their own:

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `Power_to_power_ratio` [-] | 1.985811912240 | 1.97726692 | 4.30e-03 |
| `W_cp` [W] | 9437.147538742 | 9477.931285 | 4.30e-03 |
| `W_turb_fluide_elec` [W] | 18740.4 | 18740.4 | matches (inside rtol) |
| `W_turb_fluide` [W] | 21000 | 21000 | matches |

Absolute enthalpies, separate from the powers. The R113 reference offset is
about 166 kJ/kg and is not the same at the two states:

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `h2` [J/kg] | 374075.416351 | 207959.1186 | 4.44e-01 |
| `h3` [J/kg] | 416183.968669 | 250249.648 | 3.99e-01 |
| `h3 - h2` [J/kg] | 42108.552 | 42290.529 | remainder 181.977 J/kg |

CoolSolve − EES is +166116.3 J/kg on `h2` and +165934.3 J/kg on `h3`. The
182 J/kg change of that offset is the whole of the 4.30e-03 on `W_cp` and on
the power ratio. `W_turb_fluide_elec` does not use those enthalpies, and it
matches 18740.4 W.

Temperatures stay in kelvin. In kelvin, `T2` is 298.24573329 K against
298.3545351 K, `T_cond` is 360.420202088 K against 360.2698789 K, and `T3` is
365.420202088 K against 365.2698789 K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `Q5_power_to_power_ratio.EES` (EES X6.883,
18 variables), compared with `compare_solution.py --ees-units`. The tool's
summary line is:

`18 common variables, 6 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The tool also prints `Converted EES reference values: T_cond (K->C), T2 (K->C)`.
`T2` and `T_cond` are stored with units K and their names start with `T`, so
the reference is rewritten to °C and compared with the kelvin value kept in
the model. That printed difference is the conversion, and the kelvin values
agree within rtol 0.001. `T3` starts with `T` as well, but its stored units
field is empty, so the tool leaves 365.2698789 K unscaled. `T3` then prints
inside rtol.

Every difference above rtol 0.001:

- `T2` prints 9.15e-01 (unrounded 0.915491). The model keeps 298.24573329 K.
  The tool compares that with 25.2045 °C. In kelvin the difference is 0.109 K.
- `T_cond` prints 7.58e-01 (unrounded 0.758283). The model keeps
  360.420202088 K. The tool compares that with 87.1199 °C. In kelvin the
  difference is 0.150 K.
- `h2` prints 4.44e-01 and `h3` prints 3.99e-01. The absolute enthalpies
  carry the R113 reference offset given in *Results*.
- `Power_to_power_ratio` and `W_cp` print 4.30e-03 (unrounded 4.303e-03).
  The 181.977 J/kg remainder of the enthalpy offset is this difference.
  The ratio is 1.985811912240 against 1.97726692. `W_cp` is
  9437.147538742 W against 9477.931285 W.

The maximum relative difference over all 18 common variables, as printed by
the tool, is 9.15e-01, on `T2`.

`W_turb_fluide_elec` is 18740.4 W on both sides. `W_turb_fluide` is 21000 W
on both sides. Pressures, mass flows, `delta_h_turb` and both efficiencies
match.

All 18 equations are satisfied. The largest residual is 7.4e-9, on
`W_cp = abs(m_dot_pac*(h3-h2))/eta_meca/eta_conv`. The other residuals are 0.

CoolSolve reports 0 iterations with the shipped `.initials` and 0 iterations
without them. Without initials, `W_cp` is 9437.147538742 W, the same positive
value. The fluid call stays `R113`. This solve printed no fluid-name warning.

## Source and attribution

The equation window names no person. The EES licence tag is
`{$ID$ #434: For use only by Kwangil Kim of Samsung Electronics Co.}`, the
licence holder, not the author. The file belongs to the ULiège course
MECA0002. The authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/Aout 2022/Q5_power_to_power_ratio.EES`.

Candidate TM-0461. No duplicate group. Teaching example. Course:
*Thermodynamique appliquée* (ULiège, MECA0002), August 2022. EES X6.883.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `Q5_power_to_power_ratio.EES` (EES X6.883, plain text, decimal commas rewritten as dots, European argument separators, 18 variables, no tables). The converted window is square: 18 equations, 18 variables, largest block 1. No stored unknown was added. `$UnitSystem` was deleted. The equation window contains no `$TABSTOPS` and no `$Export`. Comments translated to English. No diagram-state arrays: the window computes the compressor inlet and outlet and a given turbine enthalpy drop.
- **Units**: `$UnitSystem SI MASS DEG PA K J`. Pressures stay `p1 = 45e3` Pa and `p3 = 320e3` Pa. `delta_h_turb` stays `17.5*1000` J/kg. The superheat stays `T3 = T_cond + 5`. Temperatures stay in kelvin. Property boundary only: `T2 = T_sat(R113, P=p2) + 273.15`, `T_cond = T_sat(R113, P=p3) + 273.15`, `h3 = enthalpy(R113, T=T3-273.15, P=p3)`, and `h2 = enthalpy(R113, P=p2, x=1)`. `.initials` are the stored solution, with temperatures in kelvin, pressures in pascal, and the stored positive `W_cp`.
- **Fluid**: `R113` stays `R113`. `abs()` stays in the compressor-power equation. The efficiencies stay 0.97 and 0.92.
- **Level**: equations 18 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; two machines coupled by the power ratio, and no third coupled component → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The absolute R113 enthalpies differ from the stored solution by about
166 kJ/kg. The enthalpy rise differs by 181.977 J/kg, so `W_cp` and
`Power_to_power_ratio` print 4.30e-03. The equations are satisfied, and
`W_turb_fluide_elec` matches the stored 18740.4 W.

`compare_solution.py --ees-units` rewrites a stored kelvin temperature whose
name starts with `T` and whose units are K. `T2` and `T_cond` therefore print
9.15e-01 and 7.58e-01 while the kelvin values agree within rtol 0.001.

`missing_features` is empty.

## Related models

`related` is empty. This example stands on its own.

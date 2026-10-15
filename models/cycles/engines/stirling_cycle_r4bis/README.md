# Ideal Stirling cycle with a regenerator (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0201`

Teaching exercise for a theoretical Stirling cycle on ideal-gas Air, with an
ideal regenerator. Compression and expansion are isothermal, the other two
processes are isochoric, and the compression ratio is volumetric. The model
returns the work and the heat of each process, the net work, and the thermal
efficiency with and without the regenerator, next to the Carnot efficiency
between the same temperature limits.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 37 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4bis/R05_E03_2022.EES` (EES X8.423) |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@f5b79cd — verified against the EES stored solution (printed max rel. diff 9.99e-01, on unscaled `cv`) |

## Problem statement

Exercise 5, as written in the equation window. A theoretical Stirling cycle has
an ideal regenerator. The minimum pressure and temperature are 100 kPa and
25 °C, the volumetric compression ratio is 10, and the maximum temperature is
1000 °C. For each of the four processes, find the work and the heat exchanged.
Find the overall efficiency and compare it with the Carnot efficiency between
the minimum and maximum temperatures. What is the efficiency of the same cycle
without the regenerator?

The equation window writes 25 °C as `T[1] = 298` K and 1000 °C as
`T[3] = 1273` K (offsets of 273, the same 273 later subtracted in the property
calls).

## Model

States, as in the equation window: 1 start of the isothermal compression,
2 end of the compression, 3 end of the isochoric heating, 4 end of the
isothermal expansion. The isochoric cooling 4–1 closes the cycle. The original
sign convention is kept: `w_12` is the work required by the compression
(`w_12 > 0`) and `w_34` is the work of the expansion (`w_34 < 0`). The net
work is `w_net = -(w_34 + w_12)`.

Ideal-gas Air, with the gas constant given in the file:

\[
v = RT/p, \qquad R = 287~\mathrm{J/(kg\cdot K)}
\]

`R = 0.287` kJ/kg-K and `p[1] = 100` kPa in the original. The volumetric ratio
is `r_v = 10`: `v[2] = v[1]/r_v`, `v[3] = v[2]`, `v[4] = v[1]`. The isotherms
are `T[2] = T[1]` and `T[4] = T[3]`.

Closed-form works, as written (`−∫p dv` in the original comments):

\[
w_{12} = RT[1]\ln(r_v), \qquad w_{34} = RT[3]\ln(v[3]/v[4])
\]

The isochoric works are `w_23 = 0` and `w_41 = 0`.

Heats from the first law, with `cv` held at the mean temperature of each
process:

\[
w_{ij} + q_{ij} = c_{v,ij}\,(T[j] - T[i])
\]

CoolSolve property calls take Celsius, and `T[]` stays in kelvin, so each call
is `cv(fluid$, T=(T[i]+T[j])/2 - 273)`, the expression in the equation window.
On an isotherm the temperature change is zero, so `q_12 = -w_12` and
`q_34 = -w_34`.

Efficiencies:

\[
q_\mathrm{couteux} = q_{23} + q_{34}, \qquad q_c = q_{34}
\]

\[
\eta_\mathrm{stirling} = w_\mathrm{net}/q_\mathrm{couteux}, \qquad
\eta_\mathrm{stirling,regen} = w_\mathrm{net}/q_c, \qquad
\eta_\mathrm{Carnot} = 1 - T[1]/T[3]
\]

Without the regenerator both `q_23` and `q_34` are supplied. With the ideal
regenerator the isochoric heat `q_23` is recovered from the isochoric cooling
`q_41`, and only `q_34` is supplied. The entropies `s[1]` to `s[4]` are
`entropy('Air', T=T-273, p=p)`. The equation window already indexes `p`, `T`,
`v` and `s`. No further state array is added.

With this closure `w_net = R(T[3]-T[1])\ln(r_v)` and `q_c = RT[3]\ln(r_v)`, so
`eta_stirling_regen` equals `eta_carnot`. The original comment states that
equality, and that the efficiency without the regenerator is about 55 percent
of the Carnot value (`0.3955/0.7659`).

| Quantity | Role | Value |
|---|---|---|
| `fluid$` | ideal-gas Air | `'Air'` |
| `R` | gas constant | 287 J/kg-K |
| `r_v` | volumetric compression ratio | 10 |
| `p[1]`, `T[1]` | minimum pressure and temperature | 1×10⁵ Pa, 298 K |
| `T[3]` | maximum temperature | 1273 K |
| `w_net` | net specific work | solved [J/kg] |
| `q_c`, `q_couteux` | heat supplied with and without the regenerator | solved [J/kg] |
| `eta_stirling_regen`, `eta_stirling`, `eta_carnot` | efficiencies | solved |

Every equation is explicit (37 blocks of size 1). The system is square
(37 equations, 37 variables).

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./stirling_cycle_r4bis.eescode
```

`stirling_cycle_r4bis.initials` is the EES stored solution converted to Pa and
J. The two isochoric works are 0, the value stored by EES (the extractor had
written the default guess 1). There is no `abs()` call and no second root.
With that file the solver reports 8 iterations. Without it the same explicit
system still returns the solution, in 55 iterations. No `coolsolve.conf` and
no variant.

## Results

Temperatures below are kelvin. Pressures and energies are the SI values
(`--ees-units` scales the stored kPa and kJ).

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `eta_stirling_regen` [-] | 0.7659073056 | 0.7659073056 |
| `eta_carnot` [-] | 0.7659073056 | 0.7659073056 |
| `eta_stirling` [-] | 0.3954769077 | 0.3955002074 |
| `w_net` [J/kg] | 644320.8736 | 644320.8736 |
| `q_c` = `q_34` [J/kg] | 841251.7663 | 841251.7663 |
| `q_couteux` [J/kg] | 1629225.022 | 1629129.041 |
| `w_12` [J/kg] | 196930.8927 | 196930.8927 |
| `w_34` [J/kg] | −841251.7663 | −841251.7663 |
| `q_12` [J/kg] | −196930.8927 | −196930.8927 |
| `q_23` [J/kg] | 787973.2558 | 787877.275 |
| `q_41` [J/kg] | −787973.2558 | −787877.275 |

`eta_stirling_regen` equals `eta_carnot`. The maximum temperature is `T[3]`
and the maximum pressure is `p[3]` (4.271812081×10⁶ Pa).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Ideal-gas Air: the maintainer's figure is a parametric sweep (for example
`eta_stirling` against `r_v`), saved as `figures/stirling_cycle_r4bis_sweep.png`.

## Verification

Reference: the solution stored in `R05_E03_2022.EES` (R4bis folder, 36 values,
EES X8.423). Unit system `SI MASS DEG KPA C KJ`.
`compare_solution.py stirling_cycle_r4bis.sol reference/ees_variables.csv --ees-units`
prints:

> 36 common variables, 12 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

Maximum relative difference over all common variables, as printed in the
tool's table: **9.99e-01** (`cv12`; `cv23`, `cv34` and `cv41` print the same
9.99e-01).

| Variable | EES (after `--ees-units`) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `cv12` | 0.717587 | 717.886 | 9.99e-01 |
| `cv23` | 0.808079 | 808.178 | 9.99e-01 |
| `cv34` | 0.897554 | 897.638 | 9.99e-01 |
| `cv41` | 0.808079 | 808.178 | 9.99e-01 |
| `T[1]`, `T[2]` | 24.85 | 298 | 9.17e-01 |
| `s[2]` | 5038.25 | 3217.26 | 3.61e-01 |
| `s[1]` | 5699.16 | 3884.28 | 3.18e-01 |
| `s[3]` | 6173.76 | 4359.65 | 2.94e-01 |
| `s[4]` | 6834.67 | 5021.17 | 2.65e-01 |
| `T[3]`, `T[4]` | 999.85 | 1273 | 2.15e-01 |

`cv12`, `cv23`, `cv34` and `cv41` have a blank unit string in the stored
solution, so `--ees-units` does not multiply them by 1000. The CoolSolve
values are already in J/kg-K. Dividing them by 1000 leaves relative
differences 4.16e-04, 1.22e-04, 9.34e-05 and 1.22e-04 (CoolProp `cv(Air)`
slightly above the EES values at the same Celsius arguments). `q_23` and
`q_41` follow `cv23` at 1.22e-04. `q_couteux` and `eta_stirling` follow that
heat at 5.89e-05. All of those are under rtol 0.001.

`T[1]` to `T[4]` are stored with unit `K`. `--ees-units` rewrites every such
name to °C (298 → 24.85, 1273 → 999.85). The model keeps the equation-window
values in kelvin, because `v = RT/p` and `eta_carnot = 1 - T[1]/T[3]` use
absolute temperature. The solved numbers are the stored kelvin numbers.

`s[1]` to `s[4]` are scaled kJ → J by the tool (unit `kJ/kg-K`). EES minus
CoolSolve is 1814.89, 1820.99, 1814.12 and 1813.50 J/kg-K. The isothermal
step `s[2] - s[1]` is −660.909 J/kg-K in the stored solution and −667.013
J/kg-K from `entropy('Air')`. Those entropies are post-processing. The work,
the heat and the efficiencies do not use them.

Work and the regenerator heat agree with the stored solution: `w_net` =
644320.8736 J/kg (rel 7.31e-11), `w_12` = 196930.8927 J/kg,
`w_34` = `q_12` magnitude = `q_c` = `q_34` = 841251.7663 J/kg.
`eta_stirling_regen` and `eta_carnot` are both 0.7659073056 (rel 2.95e-11).
That equality is the closed form `R(T[3]-T[1])\ln(r_v)` over
`RT[3]\ln(r_v)`.

Enthalpy is not in the equation window, so the usual ideal-gas Air enthalpy
offset of about +126 kJ/kg against EES does not appear.

The name only in the CoolSolve solution is `fluid$`. The `.sol` file contains
`fluid$ = 0` and `fluid$ = 'Air'` (`CS-BUG-SOL-STRING`). The EES variable list
has no numeric `fluid$`.

CoolSolve warns that moist air should use `AirH2O`, and that `t = 512.5` is
read as 512.5 °C. The fluid in the file is ideal-gas `Air`. The argument
512.5 °C is `(T[2]+T[3])/2 - 273`, the mean temperature of the isochoric
heating, and the solved `cv23` matches the stored specific heat once both are
in J/kg-K. The fluid and the temperature arguments are unchanged.

## Source and attribution

Source file
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4bis/R05_E03_2022.EES`
(EES X8.423). The file itself names nobody. The `{$ID$}` tag is the EES
licence of the Laboratoire de Thermodynamique, University of Liege, the
licence holder. The inventory attributes the course to S. Quoilin, so
`authors` is `["S. Quoilin"]`. The equation window titles the problem
"Exercice 5". Published under the library licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`, card C-227): EES X8.423, plain-text
  equation window, decimal commas already rewritten as dots, `{$ID$}` removed,
  no lookup or parametric table, 36 stored values. `$UnitSystem SI MASS DEG KPA C KJ`
  removed. `R = 0.287` kJ/kg-K is written `287` J/kg-K and `p[1] = 100` kPa is
  written `100e3` Pa. Temperatures stay in kelvin (`T[1] = 298`, `T[3] = 1273`).
  Property calls keep the original `-273` and the array indices `p[i]`, `T[i]`,
  `v[i]`, `s[i]`. The unmodified extract (directive removed) is square
  (37 equations, 37 variables, largest block 1), so no Diagram-window value
  was restored and no computed unknown was replaced by a stored number.
  `$Export`, `concat$` and `EESFILEDIR$` are absent. No integral.
- **2026-10-15 — initials**: the shipped guesses are the stored solution in SI.
  `w_23` and `w_41` are 0. The extractor had written 1, which is the EES
  default guess for a stored zero. Specific heats and entropies in the guess
  file are the stored numbers times 1000; the equations overwrite them.
- **Level**: equations 37 (< 50) → 0; largest block 1 (≤ 5) → 0; arrays → 1;
  one cycle, no multi-zone discretisation and no third component → 0; ideal
  gas with `cv` at a mean temperature, no calibration, off-design, part-load
  or dynamics → 0; converges without curated guesses (55 iterations, no
  `coolsolve.conf`) → 0. Score 1 → **level 1**.

## Limitations and CoolSolve gaps

- Ideal regenerator and a perfect-gas closure with `cv` constant on each
  process. The file has no real engine geometry, speed or indicated work.
- Absolute entropies follow the CoolProp reference state of ideal-gas Air.
  The cycle results do not use `s[i]`.
- CoolSolve warns that moist air should use `AirH2O`. The fluid stays `Air`.
- The mean-temperature call at 512.5 °C draws the generic Celsius hint. The
  argument is the one written in the equation window.
- No CoolSolve gap blocks this file. `missing_features` is empty. The numeric
  `fluid$ = 0` line in the `.sol` file is `CS-BUG-SOL-STRING`.

## Related models

- `CSL-0059` (*stirling_cycle_ideal_regenerator*): the same exercise type from
  the R5 folder (`R05_E03_2022.EES`, candidate TM-0431). That model also
  evaluates the cycle with real-gas air properties and with the EES definite
  integral of `p dv`. This R4bis file is the ideal-gas closed form only.
  The back-link is left for the orchestrator.

# R134a heat-pump condenser heat rejection (Cengel 6-54)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0171`

R134a enters the condenser of a heat pump and leaves as saturated liquid at
the same pressure. The condenser is an open system at steady state. The model
computes the heat rejection and the heat-pump COP. Textbook exercise
Cengel 6-54.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R134a |
| **Size** | 18 equations (largest block: 1) |
| **Source** | thermo_models, KU Leuven exercises, file `06-54.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@b3c0d78 — verified against the EES stored solution (see *Verification*) |

## Problem statement

R134a enters the condenser of a heat pump at 800 kPa and 35 °C at 0.018 kg/s
and leaves at 800 kPa as saturated liquid. The power input is 1.2 kW. The
source treats the condenser alone as an open system at steady state and
applies the first law, then forms the heat-pump COP. Textbook exercise
Cengel 6-54.

## Model

The inlet state is fixed by pressure and temperature. The outlet state is
fixed by the same pressure and a vapour quality of 0 (saturated liquid).
Enthalpies are real-fluid properties of R134a. The heat rejection is the
first-law balance written in the source, and the COP divides that heat by
the given power input.

- \(h_\mathrm{out} = h(p_\mathrm{out}, x_\mathrm{out})\)
- \(h_\mathrm{in} = h(p_\mathrm{in}, T_\mathrm{in})\)
- \(\dot Q_h = \dot m\,(h_\mathrm{in} - h_\mathrm{out})\)
- \(\mathrm{COP} = \dot Q_h / \dot W_\mathrm{in}\)

| Input | Value |
|---|---|
| `M_dot` | 0.018 kg/s (`0,018` in the source) |
| `p_in` | 800 kPa (800×10³ Pa) |
| `T_in` | 35 °C |
| `p_out` | 800 kPa (800×10³ Pa) |
| `x_out` | 0 (saturated liquid) |
| `W_dot_in` | 1200 W |

`M_dot`, `p_in`, `T_in`, `p_out`, `x_out` and `W_dot_in` are already
equations in the EES equation window. The system is square without any
further assignment (10 equations, 10 variables). The stored values of the
unknowns are guesses in `.initials`, not equations.

The eight equations `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 inlet, i = 2
outlet) are post-processing for the CoolSolve diagram. They do not change
the ten physical results.

## How to run

```bash
coolsolve ./r134a_condenser_heat_rejection.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. The `.initials` file is the EES
stored solution, including enthalpies on the EES reference state. The
extracted guess `x_out = 1` is not used: the stored value is 0, and the
equation window already sets `x_out = 0`.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `p_in`, `p_out` | 800000 Pa | 800000 Pa |
| `T_in` | 35 °C | 35 °C |
| `T[2]` | 31.327 °C | not stored |
| `Q_dot_h` | 3163.02 W | 3163.52 W |
| `COP` | 2.63585 | 2.63626 |
| `W_dot_in` | 1200 W | 1200 W |

`T[2]` is the post-processing saturation temperature at 800 kPa and
`x_out = 0`. EES did not store an outlet temperature. `Q_dot_h` and `COP`
are printed at the digits of `compare_solution.py`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against `reference/ees_variables.csv` from `06-54.EES`
(EES X9.920, 10 stored variables):

> 10 common variables, 2 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8

The two differences, quoted as the tool prints them:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h_in` | 271222 | 419369 | 3.53e-01 |
| `h_out` | 95471.4 | 243645 | 6.08e-01 |

Maximum relative difference over all common variables: **6.08e-01** (`h_out`).

Those two names are the absolute enthalpies. EES sets \(h = 0\) and \(s = 0\)
for saturated liquid R134a at −40 °C. The same state in this CoolSolve binary
is \(h = 148144.046\) J/kg and \(s = 795.610\) J/kg·K. EES did not store an
entropy, so there is no entropy offset to compare. The enthalpy offsets
against the stored values are not exactly that constant:

| Variable | EES | CoolSolve | CoolSolve − EES |
|---|---:|---:|---:|
| `h_in` | 271222.2885 | 419368.8978 | 148146.609 |
| `h_out` | 95471.37418 | 243645.4062 | 148174.032 |

The two offsets differ from each other by 27.423 J/kg, and from
148144.046 J/kg by 2.563 J/kg and 29.986 J/kg. That 27.423 J/kg is the whole
difference of the condenser enthalpy drop (175723.49 J/kg here, 175750.91 J/kg
in EES), a relative difference of 1.56e-04. It is a property-formulation
residual, and it is below rtol = 0.001. The printed relative differences
3.53e-01 and 6.08e-01 are the same reference shift divided by the two
absolute enthalpies. `h_out` prints the larger relative difference because
the EES saturated-liquid enthalpy is the smaller of the two absolutes.

The tool's other common variables stay under rtol = 0.001 (`--all`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Q_dot_h` | 3163.52 | 3163.02 | 1.56e-04 |
| `COP` | 2.63626 | 2.63585 | 1.56e-04 |
| `M_dot` | 0.018 | 0.018 | 0.00e+00 |
| `p_in`, `p_out` | 800000 | 800000 | 0.00e+00 |
| `T_in` | 35 | 35 | 0.00e+00 |
| `W_dot_in` | 1200 | 1200 | 0.00e+00 |
| `x_out` | 0 | 0 | 0.00e+00 |

`Q_dot_h` and `COP` carry the enthalpy-drop residual. The eight names only
in the CoolSolve solution are the diagram arrays `P[1]`, `h[1]`, `T[1]`,
`s[1]`, `P[2]`, `h[2]`, `T[2]`, `s[2]`.

## Source and attribution

S. Quoilin, KU Leuven course exercises. Textbook problem Cengel 6-54. The
EES licence tag in the file is the J. Lebrun laboratory licence (University
of Liège), not the author. Source file:
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/06-54.EES`
(EES X9.920, inventory row TM-0339). The comments in the source are English.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X9.920, unit
  system `SI MASS DEG PA C J`, 10 variables, no tables, no warnings). The
  equation window is plain text with a decimal comma (`0,018`) and semicolons
  in the property calls; those were written as `0.018` and commas. No unit
  was converted: pressures are already in Pa, the power already in W, and the
  temperature already in °C. The `$UnitSystem` directive was removed. No
  Diagram-window input had to be restored: the six inputs above are already
  equations, and the system is square. The fluid name `r134a` was written
  `R134a`. EES names are case-insensitive, so the energy balance and the
  inlet property call were written with `M_dot` and `T_in`, the names of the
  assignments. Comments were already English; each dimensional quantity was
  given its SI unit. Variable names are otherwise unchanged. The extracted
  `.initials` had `x_out = 1`, the EES guess; the shipped file uses the
  stored value 0.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1, 2. `T[1]` is `T_in`. `T[2]` is `temperature(R134a, p=p_out, x=x_out)`.
  `s[1]` is `entropy(R134a, p=p_in, T=T_in)` and `s[2]` is
  `entropy(R134a, p=p_out, x=x_out)`. A solve of the equation window alone
  and a solve of this file give the same ten original variables (relative
  difference 0).
- **Level**: equations 18 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; explicit, 0 iterations
  with or without guesses → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The first law is written `Q_dot_h = M_dot*(h_in - h_out)`, as in the
original, so a work term and changes of kinetic and potential energy are
absent. Both pressures are assigned, so the file imposes equal inlet and
outlet pressures. No CoolSolve
gap blocks the file. The solver prints the known hint `CS-BUG-HINT-FAHRENHEIT`
on the inlet temperature 35 °C (within 3 of 32). The value used is still
35 °C.

## Related models

None. No other library model is this condenser energy balance.

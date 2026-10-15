# R134a compressor minimum power (Cengel 7-41)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0169`

Saturated R134a vapour is compressed from 160 kPa to 900 kPa. The inlet
volume flow is 2 m³/min. The model computes the minimum compressor power,
which is the power of a reversible adiabatic (isentropic) compression.
Textbook exercise Cengel 7-41.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R134a |
| **Size** | 19 equations (largest block: 1) |
| **Source** | thermo_models, KU Leuven exercises, file `07-41.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@c11a18d — verified against the EES stored solution (see *Verification*) |

## Problem statement

Refrigerant 134a enters a compressor as saturated vapour at 160 kPa with a
volume flow of 2 m³/min and leaves at 900 kPa. The minimum power input is
required. In the source file that minimum is the reversible adiabatic
compression: reversible and adiabatic means isentropic, and the power follows
from the steady-flow energy balance.

## Model

The inlet state is fixed by pressure and quality. The discharge pressure is
imposed and the discharge entropy equals the inlet entropy. Density, enthalpy
and entropy are real-fluid properties of R134a.

- \(s_2 = s_1\)
- \(\dot m = \dot V\,\rho_1\)
- \(\dot W = \dot m\,(h_2 - h_1)\)

| Input | Value |
|---|---|
| `p_1` | 160 kPa (160×10³ Pa) |
| `x_1` | 1 (saturated vapour) |
| `V_dot` | 2 m³/min = 2/60 m³/s |
| `p_2` | 900 kPa (900×10³ Pa) |

`p_1`, `V_dot`, `p_2` and `x_1` are already equations in the EES equation
window. The system is square without any further assignment. The stored
values of the unknowns are guesses in `.initials`, not equations.

The eight equations `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 inlet, i = 2
discharge) are post-processing for the CoolSolve diagram. They do not change
the eleven physical results.

## How to run

```bash
coolsolve ./r134a_compressor_minimum_power.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. The `.initials` file is the EES
stored solution, including enthalpies and entropies on the EES reference
state.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `p_1` | 160000 Pa | 160000 Pa |
| `p_2` | 900000 Pa | 900000 Pa |
| `T[1]` | −15.588 °C | not stored |
| `T[2]` | 42.708 °C | not stored |
| `rho_1` | 8.09787 kg/m³ | 8.09858 kg/m³ |
| `M_dot` | 0.269929 kg/s | 0.269953 kg/s |
| `h_2 − h_1` | 35955.11 J/kg | 35951.79 J/kg |
| `W_dot` | 9705.329 W | 9705.277 W |

`T[1]` and `T[2]` are the post-processing temperatures. EES did not store a
temperature. The inlet is saturated vapour at 160 kPa; the discharge is the
isentropic state at 900 kPa.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against `reference/ees_variables.csv` from `07-41.EES`
(EES X9.920, 11 stored variables):

> 11 common variables, 4 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8

The four differences, quoted as the tool prints them:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h_1` | 241109 | 389269 | 3.81e-01 |
| `h_2` | 277061 | 425224 | 3.48e-01 |
| `s_1` | 941.896 | 1737.57 | 4.58e-01 |
| `s_2` | 941.896 | 1737.57 | 4.58e-01 |

Maximum relative difference over all common variables: **4.58e-01** (`s_1`
and `s_2`).

Those four names are the absolute enthalpies and entropies. EES sets
\(h = 0\) and \(s = 0\) for saturated liquid R134a at −40 °C. The same state
in this CoolSolve binary is \(h = 148144.046\) J/kg and
\(s = 795.610\) J/kg·K. The solution offsets against the stored values are
not exactly that constant:

| Variable | EES | CoolSolve | CoolSolve − EES |
|---|---:|---:|---:|
| `h_1` | 241109.1212 | 389268.5223 | 148159.401 |
| `h_2` | 277060.9142 | 425223.6315 | 148162.717 |
| `s_1`, `s_2` | 941.8957642 | 1737.566280 | 795.670516 |

`s_2 = s_1` in both solutions, so the entropy offset is one number. It sits
0.060 J/kg·K above the −40 °C saturated-liquid entropy. The two enthalpy
offsets differ from each other by 3.316 J/kg, and from 148144.046 J/kg by
15.4 J/kg and 18.7 J/kg. That 3.316 J/kg is the whole difference of the
isentropic enthalpy rise (35955.11 J/kg here, 35951.79 J/kg in EES), a
relative difference of 9.22e-05. It is a property-formulation residual, and
it is below rtol = 0.001. The printed relative differences 3.81e-01 and
3.48e-01 are the same reference shift divided by the two absolute enthalpies.

The tool's other common variables stay under rtol = 0.001 (`--all`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `W_dot` | 9705.28 | 9705.33 | 5.34e-06 |
| `rho_1` | 8.09858 | 8.09787 | 8.69e-05 |
| `M_dot` | 0.269953 | 0.269929 | 8.69e-05 |
| `p_1`, `p_2`, `x_1` | assigned | assigned | 0.00e+00 |
| `V_dot` | 0.0333333 | 0.0333333 | 9.99e-11 |

`M_dot` carries the saturated-vapour density difference. `W_dot` stays at
5.34e-06 because the mass-flow and enthalpy-rise residuals partly compensate.
The eight names only in the CoolSolve solution are the diagram arrays
`P[1]`, `h[1]`, `T[1]`, `s[1]`, `P[2]`, `h[2]`, `T[2]`, `s[2]`.

## Source and attribution

S. Quoilin, KU Leuven course exercises. Textbook problem Cengel 7-41. The
EES licence tag in the file is the J. Lebrun laboratory licence (University
of Liège), not the author. Source file:
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/07-41.EES`
(EES X9.920, inventory row TM-0344). The comments in the source are English.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X9.920, unit
  system `SI MASS DEG PA C J`, 11 variables, no tables, no warnings). The
  `$UnitSystem` directive was removed. No value was converted. No
  Diagram-window input had to be restored: `p_1`, `V_dot`, `p_2` and `x_1`
  are already equations, and the system is square (11 equations, 11
  variables). The fluid name `r134a` was written `R134a`. Comments were
  already English; the split sentence on reversible adiabatic compression
  was reflowed and each dimensional quantity was given its SI unit. Variable
  names are unchanged.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1, 2. `T[1]` is `temperature(R134a, p=p_1, x=x_1)` and `T[2]` is
  `temperature(R134a, p=p_2, h=h_2)`. A solve of the equation window alone
  and a solve of this file give the same eleven original variables (relative
  difference 0).
- **Level**: equations 19 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; explicit, 0 iterations
  with or without guesses → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The power is the reversible adiabatic minimum. The energy balance is written
`W_dot = M_dot*(h_2 - h_1)`, as in the original, so heat transfer and changes
of kinetic and potential energy are absent. No CoolSolve gap.

## Related models

None. No other library model is this exercise.

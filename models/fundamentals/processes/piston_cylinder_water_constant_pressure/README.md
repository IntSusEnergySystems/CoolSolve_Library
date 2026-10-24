# Piston-cylinder water heated at constant pressure (Cengel 3-55)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0176`

A piston-cylinder contains 0.1 m³ of liquid water and 0.9 m³ of water vapour
in equilibrium at 800 kPa. Heat is transferred at constant pressure until the
temperature reaches 350 °C. The model computes the initial temperature, the
total mass and the final volume. Textbook exercise Cengel 3-55.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water |
| **Size** | 21 equations (largest block: 1) |
| **Source** | thermo_models, KU Leuven exercises, file `03-55.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A piston-cylinder device contains 0.1 m³ of liquid water and 0.9 m³ of water
vapour in equilibrium at 800 kPa. Heat is transferred at constant pressure
until the temperature reaches 350 °C. The source file asks for the initial
temperature of the water, the total mass, and the final volume, and to show
the process on a P-v diagram with respect to the saturation lines.

Textbook problem Cengel 3-55 also asks for the boundary work. That equation
is absent from `03-55.EES`, and the stored solution has no work variable, so
this model does not evaluate it.

## Model

The initial state is a saturated mixture at the given pressure. The liquid
and vapour volumes are known, so the two masses follow from the saturation
densities. Heating is at constant pressure up to the given temperature. The
final density is a property of Water; the final volume follows from the total
mass.

- \(T_\mathrm{init} = T_\mathrm{sat}(p)\)
- \(m_f = \rho_f V_f\), \(m_g = \rho_g V_g\), \(m_\mathrm{tot} = m_f + m_g\)
- \(\rho_\mathrm{final} = \rho(T_\mathrm{final}, p) = m_\mathrm{tot}/V_\mathrm{final}\)

| Input | Value |
|---|---|
| `V_f` | 0.1 m³ |
| `V_g` | 0.9 m³ |
| `p` | 800 kPa (800×10³ Pa in the file) |
| `T_final` | 350 °C |

`V_f`, `V_g`, `p` and `T_final` are already equations in the EES equation
window. The system is square (12 equations, 12 variables) without any
Diagram-window value. The stored values of the unknowns are guesses in
`.initials`.

The second equation for `rho_final` is kept as written,
`rho_final = m_tot/V_final`, so `V_final` is solved by a one-variable Newton
step. The nine equations `x_1`, `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 initial
mixture, i = 2 final state) are post-processing for the CoolSolve diagram.
`x_1 = m_g/m_tot` is the vapour mass fraction of the initial mixture. They do
not change the twelve original variables.

## How to run

```bash
coolsolve ./piston_cylinder_water_constant_pressure.eescode
```

CoolSolve reports 3 iterations with the shipped `.initials` and 11 iterations
without them. Both runs succeed. The iterations are the Newton solve of
`V_final`. The `.initials` file is the EES stored solution.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `T_init` | 170.406 °C | 170.444 °C |
| `m_f` | 89.7035 kg | 89.7054 kg |
| `m_g` | 3.74469 kg | 3.74423 kg |
| `m_tot` | 93.4482 kg | 93.4496 kg |
| `V_final` | 33.1202 m³ | 33.1175 m³ |
| `rho_f` | 897.035 kg/m³ | 897.054 kg/m³ |
| `rho_g` | 4.16077 kg/m³ | 4.16026 kg/m³ |
| `rho_final` | 2.82149 kg/m³ | 2.82176 kg/m³ |

The diagram states, present only in the CoolSolve solution, are
`P[1] = P[2] = 800000` Pa, `T[1] = 170.406` °C, `T[2] = 350` °C,
`x_1 = 0.0400724`, `h[1] = 802910` J/kg, `s[1] = 2230.62` J/kg·K,
`h[2] = 3.16217×10⁶` J/kg, `s[2] = 7410.63` J/kg·K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against `reference/ees_variables.csv` from `03-55.EES`
(EES X9.486, 12 stored variables), without `--ees-units` (the file is already
pascal and joule):

> 12 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 9

No common variable exceeds rtol = 0.001. The maximum relative difference over
all common variables is **2.20e-04** (`T_init`). The tool prints:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_init` | 170.444 | 170.406 | 2.20e-04 |
| `rho_g` | 4.16026 | 4.16077 | 1.23e-04 |
| `m_g` | 3.74423 | 3.74469 | 1.23e-04 |
| `rho_final` | 2.82176 | 2.82149 | 9.70e-05 |
| `V_final` | 33.1175 | 33.1202 | 8.18e-05 |
| `rho_f` | 897.054 | 897.035 | 2.09e-05 |
| `m_f` | 89.7054 | 89.7035 | 2.09e-05 |
| `m_tot` | 93.4496 | 93.4482 | 1.52e-05 |
| `p`, `V_f`, `V_g`, `T_final` | assigned | assigned | 0.00e+00 |

`T_init` is the saturation temperature at 800 kPa. The density differences are
the same Water formulation residual; `m_f` and `m_g` repeat `rho_f` and
`rho_g` because the volumes are exact, and `V_final` repeats `rho_final`.

The stored solution contains no enthalpy and no entropy, so no Water
reference-state offset was measured. `h[1]`, `h[2]`, `s[1]` and `s[2]` are
diagram outputs only. The nine names only in the CoolSolve solution are
`x_1`, `P[1]`, `h[1]`, `T[1]`, `s[1]`, `P[2]`, `h[2]`, `T[2]` and `s[2]`.

A solve of the twelve equation-window equations alone and a solve of this
file give the same twelve variables (relative difference 0).

`density()` prints that `t=350` is interpreted as 350 °C. That is the assigned
`T_final`. The known Fahrenheit hint did not appear. `rho_final` agrees with
the stored value to 9.70e-05, which confirms the Celsius reading.

## Source and attribution

S. Quoilin, KU Leuven course exercises. Textbook problem Cengel 3-55. The
EES licence tag in the file is the J. Lebrun laboratory licence (University
of Liège), not the author. Source file:
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/03-55.EES`
(EES X9.486, inventory row TM-0333). The comments in the source are English.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X9.486, unit
  system `SI MASS DEG PA C J`, decimal commas already converted by the
  extractor, 12 variables, no tables, no warnings). The `$UnitSystem`
  directive was removed. No value was rescaled: `p = 800e3` is already
  800000 Pa. No Diagram-window input had to be restored: the system is square
  (12 equations, 12 variables). The fluid name was written `Water`. `T_sat`
  is called with `P=p` because EES treats `P` and `p` as one variable.
  Comments were rewritten in English and each dimensional quantity was given
  its SI unit. Variable names are unchanged.
- **2026-10-15 — diagram states**: added `x_1` and `P[i]`, `h[i]`, `T[i]`,
  `s[i]` for i = 1, 2. A solve without that block and a solve of this file
  give the same twelve original variables (relative difference 0).
- **Level**: equations 21 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges without
  curated guesses (11 iterations from the default guess, 3 with the stored
  solution) → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The source evaluates the initial saturation state, the two masses and the
final volume. It does not evaluate the boundary work or the heat transfer.
The initial liquid and vapour are each at saturation at the common pressure.
No CoolSolve gap.

## Related models

- `CSL-0283` *helium_bottle_lox_displacement*: same constant-pressure
  closed-system process, other fluid (ideal-gas helium instead of two-phase
  water) and other question (pressurant work and bottle sizing).

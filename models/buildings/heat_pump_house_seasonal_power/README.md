# Exercise: seasonal power of a heat pump for a house

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0239`

Teaching exercise 6.21. A heat pump heats a house in winter and, reversed,
cools it in summer. Heat flow through the building envelope is proportional
to the indoor-outdoor temperature difference, and the machine is an ideal
reversible Carnot cycle between the indoor air and the outdoor air. The
model computes the winter mechanical power, then the summer outdoor
temperature at which the same power holds the house at 25 °C.

| | |
|---|---|
| **Category** | Buildings |
| **Fluids** | none |
| **Size** | 11 equations (largest block: 3) |
| **Source** | thermo_models, ULiège thermodynamique appliquée, exercise 6.21, file `THD09_R04_Ex03.EES` |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7d66c3b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The file is labelled `THD09 - R04 - Ex03` and `[Exercice 6.21]`. The equation
window is the statement.

(a) Mechanical power required to run the heat pump. The indoor temperature
is 20 °C and the outdoor temperature is 0 °C. The original comment states
that the first and second laws give an ideal reversible Carnot cycle,
`COP_pac = Q_c/W = t_c/(t_c-t_f)`. Heat flows through the building envelope.

(b) Refrigerator mode. The cooling COP depends on the unknown outdoor
temperature `t_out_ete`. The power is held constant, equal to the winter
power. The indoor temperature is 25 °C. Heat flows through the building
envelope.

The loss coefficient is written `AU_pertes = 2400E3/3600`, with the original
comment “en W/K”.

## Model

Winter heat delivered to the house replaces the envelope loss. Summer, the
same mechanical power and the envelope balance close the outdoor temperature.
Both summer expressions for `Q_dot_ete` are kept.

- `AU_pertes = 2400E3/3600` W/K
- `Q_dot_hiver = AU_pertes (t_in_hiver − t_out_hiver)`
- `COP_pac_hiver = (t_in_hiver + 273.15) / (t_in_hiver − t_out_hiver)`
- `W_dot_pac_hiver = Q_dot_hiver / COP_pac_hiver`
- `COP_frigo = (t_in_ete + 273.15) / (t_out_ete − t_in_ete)`
- `Q_dot_ete = COP_frigo · W_dot_frigo`
- `W_dot_frigo = W_dot_pac_hiver`
- `Q_dot_ete = AU_pertes (t_out_ete − t_in_ete)`

`t_in_ete = 25`, `t_in_hiver = 20` and `t_out_hiver = 0` stay. The two
Carnot ratios stay in that form: Celsius temperatures shifted by 273.15.

| Input | Value |
|---|---|
| `t_in_hiver` | 20 °C |
| `t_out_hiver` | 0 °C |
| `t_in_ete` | 25 °C |
| `AU_pertes` | `2400E3/3600` W/K |

The summer outdoor temperature enters as a difference and as a divisor, so
the balance is quadratic in `(t_out_ete − t_in_ete)`. The two roots are
equally far above and below 25 °C. The stored solution is the root above
25 °C. The shipped `.initials` set `t_out_ete = 45.16984002` so the solve
keeps that root. The loss coefficient and the winter temperatures are
unchanged.

CoolSolve reports the system square: 11 equations and 11 variables. The
largest algebraic block is 3 (`Q_dot_ete`, `t_out_ete`, `COP_frigo`). The
winter equations and `W_dot_frigo = W_dot_pac_hiver` are explicit. There is
no fluid and no property call, so no diagram-state arrays were added.

Four stored names have no equation in the window: `COP`, `COP_pac`, `t_c`
and `t_f`. They stay only in the EES file.

## How to run

```bash
coolsolve ./heat_pump_house_seasonal_power.eescode
```

With the shipped `.initials`, CoolSolve reports 2 iterations and
`t_out_ete = 45.16984000548` °C. Without `.initials`, the same file
converges in 4 iterations to the other root, `t_out_ete = 4.830160123477` °C.
No `coolsolve.conf` is used.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `W_dot_pac_hiver` | 909.6594462448 W | 909.6594462 W |
| `COP_pac_hiver` | 14.6575 | 14.6575 |
| `t_out_ete` | 45.16984000548 °C | 45.16984002 °C |
| `Q_dot_hiver` | 13333.33333333 W | 13333.33333 W |
| `Q_dot_ete` | 13446.56000366 W | 13446.56001 W |
| `COP_frigo` | 14.78197149402 | 14.7819715 |
| `W_dot_frigo` | 909.6594462448 W | 909.6594462 W |
| `AU_pertes` | 666.6666666667 W/K | 666.6666667 W/K |

Closed form of the same equations, with `AU_pertes = 2400E3/3600` and
`dT = t_out_ete − 25`:

`COP_pac_hiver = 293.15/20 = 14.6575`,

`W_dot_pac_hiver = AU_pertes · 20 / COP_pac_hiver = 909.6594462448` W,

`dT² = W_dot_pac_hiver · 298.15 / AU_pertes`,

so `t_out_ete = 45.1698400055` °C or `4.8301599945` °C. The shipped solution
matches the root above 25 °C.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against `reference/ees_variables.csv` from
`THD09_R04_Ex03.EES` (EES X7.888, 15 stored variables), without
`--ees-units`. The tool's summary line:

> 11 common variables, 0 differ (rtol=0.001); only in EES: 4; only in CoolSolve: 0

The printed maximum relative difference over all common variables is
**4.71e-10** (`Q_dot_ete`). The unrounded ratio is 4.715×10⁻¹⁰.

| Variable | EES stored | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Q_dot_ete` | 13446.56001 W | 13446.56000366 W | 4.71e-10 |
| `COP_frigo` | 14.7819715 | 14.78197149402 | 4.05e-10 |
| `t_out_ete` | 45.16984002 °C | 45.16984000548 °C | 3.21e-10 |
| `Q_dot_hiver` | 13333.33333 W | 13333.33333333 W | 2.50e-10 |
| `AU_pertes` | 666.6666667 W/K | 666.6666666667 W/K | 4.99e-11 |
| `W_dot_pac_hiver`, `W_dot_frigo` | 909.6594462 W | 909.6594462448 W | 4.92e-11 |
| `COP_pac_hiver` | 14.6575 | 14.6575 | 0 |
| `t_in_ete`, `t_in_hiver`, `t_out_hiver` | assigned | assigned | 0 |

Every common variable is inside rtol 0.001. The differences are the stored
solution written with fewer digits. The closed form above reproduces the
CoolSolve digits.

Only in the EES reference: `COP` (4.0525), `COP_pac` (8.518571429),
`t_c` (25 °C) and `t_f` (−10 °C). None of them appears in an equation.
The system is square without them, so they were not restored.

A solve without `.initials` returns the other outdoor temperature,
`t_out_ete = 4.830160123477` °C, with `COP_frigo` and `Q_dot_ete` negative.
The closed form of that sign is 4.8301599945 °C.

## Source and attribution

Exercise 6.21, file header `THD09 - R04 - Ex03`. The folder name `SBe` is
the initials SB, and the inventory notes name the solution as S. Bertagnolio.
Author: Stéphane Bertagnolio. The `{$ID$}` tag is the laboratory licence of
Jean Lebrun (Laboratoire de Thermodynamique, Université de Liège), not an
author.

The collection copy is under the 2017-2018 course tree. The equation window
does not give a person or a date.

Source: `~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R04/SBe/THD09_R04_Ex03.EES`

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `THD09_R04_Ex03.EES` (EES X7.888). Unit system `$UnitSystem SI MASS DEG PA C J`, already pascal, Celsius and joule, so no number was scaled. The directive was deleted. The file contains no `$TABSTOPS` and no `$Export`. No lookup table and no parametric table. 11 equations in the window, 15 stored names. CoolSolve reports `System square: Yes`, so no stored unknown was added. Comments translated to English. `AU_pertes = 2400E3/3600`, `COP_pac_hiver = (t_in_hiver+273.15)/(t_in_hiver-t_out_hiver)` and `COP_frigo = (t_in_ete+273.15)/(t_out_ete-t_in_ete)` are unchanged. Both equations for `Q_dot_ete` are kept.
- **2026-10-16 — initials**: the shipped guesses are the stored values of the eleven equation-window names, including `t_out_ete = 45.16984002`. That selects the root above 25 °C. Without those guesses the solver returns 4.830160123477 °C.
- **Level**: equations 11 → 0 (< 50); largest block 3 → 0 (≤ 5); no procedure, function, array or `DUPLICATE` → 0; one building balance, so not three coupled components → 0; no calibration, off-design or dynamics → 0; the stored guesses are required to select the outdoor temperature above 25 °C → 1. Score 1 → level 1.

## Limitations and CoolSolve gaps

The envelope loss is linear in the indoor-outdoor temperature difference,
and the heat pump is reversible and Carnot. Summer uses the winter
mechanical power. The model has no refrigerant loop and no part-load map.
The summer balance has two roots; the root below 25 °C makes `Q_dot_ete`
and `COP_frigo` negative.

No CoolSolve gap blocks this file.

## Related models

None.

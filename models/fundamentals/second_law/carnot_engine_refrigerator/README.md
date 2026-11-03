# Carnot engine driving a Carnot refrigerator

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0186`

Teaching exercise: a Carnot heat engine, driven by a hot reservoir, drives
a Carnot refrigerator that holds a cold space. Both machines are reversible.
The model computes the engine efficiency, the refrigerator COP and the ratio
of the heat given up by the hot reservoir to the heat given up by the cold
space. It does not solve a working fluid.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | none |
| **Size** | 10 equations (largest block: 1) |
| **Source** | thermo_models, ULiège MECA0002, repetition R4 exercise 5 (2022-2023), file `R04_E5_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution and the closed form (see *Verification*) |

## Problem statement

Refrigeration is to be produced at −30 °C. A reservoir is available at
200 °C and the ambient temperature is 30 °C. Work can therefore be produced
between the reservoir at 200 °C and the ambient, and that work can drive the
refrigerator. Determine the ratio of the heat given up by the hot reservoir
to the heat given up by the cold chamber, assuming that every process is
reversible.

The pasted statement and the equation window agree. The window computes
that ratio as `Rapport_Q`.

## Model

Two ideal Carnot machines. The engine operates between the hot reservoir
and the ambient. The refrigerator operates between the ambient and the cold
space. The model writes the Carnot ratios and the heat ratio. It does not
introduce a refrigerant, a working fluid or a component.

- Cold space, hot reservoir and ambient: `T_ref = -30` °C, `T_hot = 200` °C, `T_amb = 30` °C.
- Engine sources: `T_F_eng = T_amb`, `T_C_eng = T_hot`.
- Engine efficiency `eta = 1.0 - (T_F_eng + 273.15)/(T_C_eng + 273.15)`. In the original both temperatures were already in kelvin, so the ratio was `T_F_eng/T_C_eng`.
- Refrigerator sources: `T_F_ref = T_ref`, `T_C_ref = T_amb`.
- Refrigerator COP `COP = 1.0/((T_C_ref + 273.15)/(T_F_ref + 273.15) - 1.0)`.
- Heat ratio `Rapport_Q = 1/(eta*COP)`. The original derives it from `Q_C_eng = W_eng/eta`, `Q_F_ref = W_ref*COP` and `W_eng = W_ref`. Those four names are comments, not equations.

| Input | Value |
|---|---|
| `T_ref` | −30 °C |
| `T_hot` | 200 °C |
| `T_amb` | 30 °C |

`T_ref`, `T_hot` and `T_amb` are equations. The system is square (10 equations,
10 variables). No Diagram-window value was substituted. The stored names
`W_eng`, `Q_C_eng`, `W_ref` and `Q_F_ref` have no equation; they are left out.

Every equation is an assignment. The largest algebraic block has 1 equation.

## How to run

```bash
coolsolve ./carnot_engine_refrigerator.eescode
```

CoolSolve reports 0 iterations without `.initials` and 0 iterations with
the shipped `.initials`. Both runs succeed. The equations are explicit, so
the initials do not select a root: there is no `abs()` and no second root.
No `coolsolve.conf` is used.

## Results

Efficiency, COP and the heat ratio (the stored EES solution was solved for
these names):

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `eta` | 0.359294092782 | 0.3592940928 |
| `COP` | 4.0525 | 4.0525 |
| `Rapport_Q` | 0.686794643829 | 0.6867946438 |
| `T_ref` | −30 °C | 243.15 K |
| `T_hot` | 200 °C | 473.15 K |
| `T_amb` | 30 °C | 303.15 K |
| `T_F_eng` | 30 °C | 303.15 K |
| `T_C_eng` | 200 °C | 473.15 K |
| `T_F_ref` | −30 °C | 243.15 K |
| `T_C_ref` | 30 °C | 303.15 K |

Heat rates and power. The equation window does not solve them. Each stored
value equals its guess. No unit is stored.

| Name | CoolSolve | EES stored |
|---|---:|---:|
| `W_eng` | not an equation | 1 (guess) |
| `Q_C_eng` | not an equation | 1 (guess) |
| `W_ref` | not an equation | 1 (guess) |
| `Q_F_ref` | not an equation | 1 (guess) |

Those four numbers are not a solution of the commented definitions. With a
common work of 1, those definitions would give `Q_C_eng = 1/eta = 2.78324`
and `Q_F_ref = COP = 4.0525`, and the ratio of those two heats is
`Rapport_Q`. The file leaves the scale unset and reports only the ratio.

Closed form of the same equations: `eta = 1 - 303.15/473.15 = 0.359294092782`,
`COP = 1/(303.15/243.15 - 1) = 4.0525`,
`Rapport_Q = 1/(eta*COP) = 0.686794643829`. The shipped solution matches
those digits.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R04_E5_2022.EES` (EES X10.836, 14 stored variables). The tool's summary line:

> 10 common variables, 0 differ (rtol=0.001); only in EES: 4; only in CoolSolve: 0

The printed maximum relative difference over all common variables is
**4.90e-11** (`eta`). Nothing is above rtol 0.001.

| Variable | EES (after `--ees-units`) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `eta` | 0.359294 | 0.359294 | 4.90e-11 |
| `Rapport_Q` | 0.686795 | 0.686795 | 4.25e-11 |
| `T_ref` | −30 °C | −30 °C | 9.47e-16 |
| `T_F_ref` | −30 °C | −30 °C | 9.47e-16 |
| `COP` | 4.0525 | 4.0525 | 0.00e+00 |
| `T_amb`, `T_C_ref`, `T_F_eng` | 30 °C | 30 °C | 0.00e+00 |
| `T_hot`, `T_C_eng` | 200 °C | 200 °C | 0.00e+00 |

`--ees-units` converted the seven temperatures from K to °C and nothing
else. No stored variable carries a kJ or kPa unit. The two result residuals
are the stored solution written with fewer digits: `eta` is stored as
0.3592940928 against 0.359294092782, and `Rapport_Q` as 0.6867946438
against 0.686794643829. `T_ref` and `T_F_ref` differ by 9.47e-16, which is
243.15 − 273.15 against the assigned −30 °C.

Only in the EES reference: `Q_C_eng`, `Q_F_ref`, `W_eng`, `W_ref`. Each
stored value is 1 and equals its guess. They appear in the explanatory
comments (`eta = W_eng/Q_C_eng`, `COP = Q_F_ref/W_ref`, `W_ref = W_eng`)
and not as equations. The system is square without them, so they were not
restored. They are unsolved guesses. CoolSolve satisfies the equation
window, so the status stays verified.

Only in CoolSolve: nothing. The kelvin shift sits inside the two Carnot
ratios, so no extra variable was added.

## Source and attribution

Repetition exercise 5, session R4, of the ULiège course *Thermodynamique
appliquée* (MECA0002), 2022-2023. The file itself names nobody. The
`{$ID$}` tag is the laboratory licence, not an author. Companion metadata
names repetition assistants; they are not authors of this file. Authors:
S. Quoilin, as the course instructor named in the inventory.

Source: `~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4/R04_E5_2022.EES`

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R04_E5_2022.EES` (EES X10.836). Unit system `$UnitSystem SI MASS DEG KPA C KJ`, deleted. The extractor rewrote the decimal commas (`273,15` → `273.15`, `1,0` → `1.0`). No lookup table, no parametric table, no `$Export`. 10 equations in the equation window, 14 stored variables. Solved with the `$UnitSystem` line removed: Equations 10, Variables 10, System square: Yes. No Diagram-window value was restored.
- **2026-10-15 — units**: thermodynamic temperatures are stored in °C. Each Carnot ratio adds 273.15, because the original temperatures were kelvin.
  - `T_ref`: `-30[K] + 273.15 [K]` → `-30` °C
  - `T_hot`: `200[K] + 273.15 [K]` → `200` °C
  - `T_amb`: `30[K] + 273.15 [K]` → `30` °C
  - `T_F_eng = T_amb`, `T_C_eng = T_hot`, `T_F_ref = T_ref`, `T_C_ref = T_amb`: same assignments, now in °C
  - `eta = 1.0 - T_F_eng/T_C_eng` → `eta = 1.0 - (T_F_eng + 273.15)/(T_C_eng + 273.15)`
  - `COP = 1.0/(T_C_ref/T_F_ref - 1.0)` → `COP = 1.0/((T_C_ref + 273.15)/(T_F_ref + 273.15) - 1.0)`
  - `Rapport_Q = 1/(eta*COP)` is unchanged
  - No pressure. No energy term in an equation, so nothing is scaled from kJ to J
- **Level**: equations 10 → 0 (< 50); largest block 1 → 0 (≤ 5); no procedure, function, array or `DUPLICATE` → 0; two Carnot ratios, not a multi-zone or discretised model and not three coupled components → 0; no calibration, off-design or dynamics → 0; explicit assignments, 0 iterations from the default guesses, no `coolsolve.conf` → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

Both machines are reversible and Carnot. The heat ratio does not depend on
the power level, and the file does not set that level. The model has no
refrigerant loop and no part-load map.

No CoolSolve gap blocks this file.

## Related models

CSL-0184 (Carnot heat pump for a house in winter and summer): the next
exercise of the same session, R4 exercise 6. Listed in `related` here. The
return link is left in that model's `model.json` for the review.

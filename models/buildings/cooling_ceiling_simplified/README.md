# Simplified cooling ceiling (sizing and TXV control)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0175`

Simplified model of a cooling ceiling from the ULiège model bank. The
nominal water capacity rate and the nominal conductance are sized from
the nominal cooling load and the nominal temperatures. At the stored
point the heat rate is the effectiveness times the capacity rate times
the supply-to-air temperature difference, multiplied by a valve factor
that is linear in the air-temperature offset, as written in the original.

| | |
|---|---|
| **Category** | Buildings |
| **Fluids** | none (the water capacity rate is the heat rate divided by the supply-to-exit temperature difference) |
| **Size** | 21 equations (largest block: 1) |
| **Source** | ULiège model bank, simplified cooling ceiling with sizing and TXV control (2008-03-17) |
| **Authors** | Jean Lebrun, Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@b3c0d78 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Size the ceiling from a nominal cooling heat rate, an oversizing factor
and the nominal water and air temperatures, then compute the heat rate
at one operating point. The original describes a thermostatic valve with
perfect authority: the offset from the air set-point sets a factor
clipped to 0 and 1. Supply-water-temperature control is not included.
The stored run is one cooling operating point of that model.

## Model

- Nominal ceiling heat rate `Q_dot_ceiling_n = F_ceiling_oversizing·Q_dot_cooling_n`.
- Nominal water capacity rate, as in the original:

  `C_dot_w_ceiling_n = Q_dot_ceiling_n/(t_w_su_ceiling_n − t_w_ex_ceiling_n)`

- Nominal effectiveness and NTU:

  `epsilon_ceiling_n = Q_dot_ceiling_n/(C_dot_w_ceiling_n·(t_w_su_ceiling_n − t_a_in_n))`

  `NTU_ceiling_n = −ln(1 − epsilon_ceiling_n)` and `AU_ceiling_n = NTU_ceiling_n·C_dot_w_ceiling_n`.

- At the simulated point, `C_dot_w_ceiling = C_dot_w_ceiling_n`.
- Conductance, as in the original:

  `AU_ceiling = AU_ceiling_n·(0.9·|(t_w_su_ceiling − t_a_in)/(t_w_su_ceiling_n − t_a_in_n)|^n_ceiling + 0.1)`

- `NTU_ceiling = AU_ceiling/C_dot_w_ceiling` and `epsilon_ceiling = 1 − exp(−NTU_ceiling)`.
- Valve factor, as in the original:

  `X_ceiling = min(1, max(0, C_ceiling·(t_a_in − t_a_in_set)))`

- Heat rate `Q_dot_ceiling = X_ceiling·epsilon_ceiling·C_dot_w_ceiling·(t_w_su_ceiling − t_a_in)`.

The original comment says the water flow rate varies linearly with the
temperature offset. In the equations the capacity rate stays at its
nominal value, and `X_ceiling` multiplies the heat rate. The heat rate
is negative when the water is colder than the air (stored cooling point).
The file does not compute a water exit temperature or an air exit state
at the simulated point.

| Inputs (default run, stored solution) | Value | Parameters | Value |
|---|---|---|---|
| `Q_dot_cooling_n` nominal cooling heat rate | −1000 W | `F_ceiling_oversizing` oversizing factor | 1 |
| `t_w_su_ceiling_n` nominal water supply temperature | 15 °C | `n_ceiling` exponent | 0.01 |
| `t_w_ex_ceiling_n` nominal water exit temperature | 18 °C | `C_ceiling` control gain | 0.5 1/K |
| `t_a_in_n` nominal air temperature | 24 °C | | |
| `t_a_in` air temperature | 25 °C | | |
| `t_a_in_set` set-point air temperature | 24 °C | | |
| `t_w_su_ceiling` water supply temperature | 16 °C | | |

These inputs and parameters are equations of the original. The stored
run is the regression case.

## How to run

```bash
coolsolve ./cooling_ceiling_simplified.eescode
```

Every block is explicit, so the solve takes 0 iterations from the default
guesses and 0 iterations with the shipped `.initials` (the EES stored
values).

## Results

The stored operating point. The EES column is the stored solution, printed
at the digits stored in the file. At this point the supply-to-air
temperature difference equals the nominal one, so the conductance
correction is 1 and the simulated effectiveness equals the nominal
effectiveness. `X_ceiling = 0.5` because the air is 1 °C above the set-point
and `C_ceiling = 0.5` 1/K.

| Quantity | CoolSolve | EES |
|---|---:|---:|
| `Q_dot_ceiling` | −500 W | −500 W |
| `X_ceiling` | 0.5 | 0.5 |
| `epsilon_ceiling` | 0.3333333333 | 0.3333333333 |
| `NTU_ceiling` | 0.4054651081 | 0.4054651081 |
| `AU_ceiling` | 135.155036 W/K | 135.155036 W/K |
| `C_dot_w_ceiling` | 333.3333333 W/K | 333.3333333 W/K |
| `Q_dot_ceiling_n` | −1000 W | −1000 W |
| `AU_ceiling_n` | 135.155036 W/K | 135.155036 W/K |
| `C_dot_w_ceiling_n` | 333.3333333 W/K | 333.3333333 W/K |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against the stored solution:

> 21 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

No variable differs above rtol = 0.001. The maximum relative difference
over the 21 common variables is **2.67e-10** (`AU_ceiling` and
`AU_ceiling_n`). At rtol = 0 the tool also lists `C_dot_w_ceiling` and
`C_dot_w_ceiling_n` at 9.99e-11. `epsilon_ceiling` and `epsilon_ceiling_n`
(9.99e-11) and `NTU_ceiling` and `NTU_ceiling_n` (2.02e-11) stay inside
the absolute tolerance 1e-9. Those residuals are the stored solution
written with fewer digits than the CoolSolve values (`C_dot_w_ceiling_n`
is 1000/3, stored as 333.3333333; `AU_ceiling_n` is `−ln(2/3)·1000/3`,
stored as 135.155036).

## Source and attribution

Jean Lebrun and Stéphane Bertagnolio, University of Liège, Thermodynamics
Laboratory, 17 March 2008. The file name ends in `JLSB080317` (initials
and date), and the equations window repeats that stamp in the title. EES
licence stamp: Jean Lebrun, Laboratoire de Thermodynamique, Université de
Liège (`{$ID$ #1206}`), EES X7.888. The equations window carries the title
"Simplified model of a cooling ceiling system (sizing and TXV control)".

Source:
`~/Nextcloud/thermo_models/Model data bank/Heating_Cooling_Terminal_Units/CoolingCeilings/CoolingCeilingWithControl_Simplified_EES_ModeJLSB080317.EES`
(inventory `TM-0261`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): equations stored as
  **RTF**; unit system already `SI MASS DEG PA C J`, so no value was
  converted; `$UnitSystem` removed; licence tag removed; no lookup or
  parametric table; no warning in the extract report. The trailing NUL
  byte of the extracted text was dropped. The unmodified extraction
  (NUL and `$UnitSystem` removed) is square: 21 equations, 21 variables.
  The inputs are already equations, so no Diagram-window value was
  substituted and no computed unknown was replaced by a stored number
  (those stay in `.initials`).
- **Unit labels.** Temperatures are annotated `[°C]` (the original wrote
  `[C]`). `C_ceiling` is annotated `[1/K]` (the original wrote `[C^-1]`).
  `AU_ceiling`, `AU_ceiling_n`, `C_dot_w_ceiling` and `C_dot_w_ceiling_n`
  are annotated `[W/K]`. The numbers are the same.
- Comments translated into short English trailing comments. The original
  text was already in English. Section titles of the original (sizing,
  simulation, parameters) are kept. No equation was rewritten.
- **Level**: 21 equations (0), largest block 1 (0), no procedure or array
  (0), one component (0), the conductance uses an empirical exponent on
  the temperature-difference ratio and `X_ceiling` is a part-load law, so
  the off-design criterion scores 1, solves from the default guesses (0)
  → score 1 → level 1.

## Limitations and CoolSolve gaps

The water capacity rate is `Q/ΔT`, not a mass flow times a specific heat.
The simulated point has no water exit temperature and no air exit state.
`X_ceiling` multiplies the heat rate; it does not change `C_dot_w_ceiling`.
One operating point is stored. The factor 0.9 in the conductance
correction, and the added 0.1, are as written in the original.

The original comment says the same equations can be used in heating mode
by setting `n_ceiling` to 0.01 and by replacing `(t_a_in − t_a_in_set)`
with `(t_a_in_set − t_a_in)`. The stored file already has `n_ceiling = 0.01`
and keeps the cooling sign of the offset. That heating adaptation is not
a second solved case. Supply-water-temperature control is not in the
model, as the original states.

No CoolSolve gap. The file uses only assignments, `abs`, `exp`, `ln`,
`min` and `max`.

## Related models

`CSL-0168` (Radiator reference model): hot-water radiator by the same
authors and the same date, with the same effectiveness `1 − exp(−NTU)`
and the same conductance correction. This file is a different component:
it sizes the nominal capacity rate and conductance of a cooling ceiling
and multiplies the heat rate by the valve factor `X_ceiling`.

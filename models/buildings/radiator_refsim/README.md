# Radiator reference model

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0168`

Reference simulation of a hot-water radiator from the ULiège model bank.
The heat output is the effectiveness times the water capacity rate times
the supply-to-air temperature difference. The effectiveness is
`1 − exp(−NTU)`, and the conductance is the nominal value scaled with
that temperature difference, both as written in the original file.

| | |
|---|---|
| **Category** | Buildings |
| **Fluids** | none (water specific heat is the constant 4187 J/(kg·K)) |
| **Size** | 14 equations (largest block: 1) |
| **Source** | ULiège model bank, radiator reference simulation model (2008-03-17) |
| **Authors** | Jean Lebrun, Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@c11a18d — verified against the EES stored solution (see *Verification*) |

## Problem statement

Given the water mass flow rate, the inlet air temperature, the water
supply temperature, and the nominal conductance and its exponent, compute
the heat output and the water exit temperature. The stored run is one
operating point of that characteristic.

## Model

- Water capacity rate `C_dot_w_rad = M_dot_w_rad·c_w`, with `c_w` fixed at
  4187 J/(kg·K).
- Conductance, as in the original:

  `AU_rad = AU_rad_n·(0.9·|(t_w_su_rad − t_a_in)/(t_w_su_rad_n − t_a_in_n)|^n_rad + 0.1)`

- `NTU_rad = AU_rad/C_dot_w_rad` and `epsilon_rad = 1 − exp(−NTU_rad)`.
- Heat output `Q_dot_rad = epsilon_rad·C_dot_w_rad·(t_w_su_rad − t_a_in)`.
- Water exit temperature `t_w_ex_rad = t_w_su_rad − Q_dot_rad/C_dot_w_rad`.

The air temperature is an input. The file does not compute an air exit
state.

| Inputs (default run, stored solution) | Value | Parameters | Value |
|---|---|---|---|
| `M_dot_w_rad` water mass flow rate | 0.04 kg/s | `n_rad` exponent | 0.3 |
| `t_a_in` inlet air temperature | 20 °C | `AU_rad_n` nominal conductance | 30 W/K |
| `t_w_su_rad` water supply temperature | 70 °C | `t_a_in_n` nominal inlet air temperature | 20 °C |
| | | `t_w_su_rad_n` nominal water supply temperature | 80 °C |
| | | `c_w` water specific heat | 4187 J/(kg·K) |

In the original the seven inputs and parameters above, except `c_w`, are
quoted strings in the equations window (the Diagram window holds the
values). Each string already states the stored value, and that value is
kept as an equation. `c_w = 4187` is an equation of the original. The
stored run is the regression case.

## How to run

```bash
coolsolve ./radiator_refsim.eescode
```

Every block is explicit, so the solve takes 0 iterations from the default
guesses and 0 iterations with the shipped `.initials` (the EES stored
values).

## Results

The stored operating point. The EES column is the stored solution, printed
at the digits stored in the file.

| Quantity | CoolSolve | EES |
|---|---:|---:|
| `Q_dot_rad` | 1312.999293 W | 1312.999293 W |
| `t_w_ex_rad` | 62.16026216 °C | 62.16026216 °C |
| `epsilon_rad` | 0.1567947567 | 0.1567947567 |
| `NTU_rad` | 0.1705448829 | 0.1705448829 |
| `AU_rad` | 28.56285699 W/K | 28.56285699 W/K |
| `C_dot_w_rad` | 167.48 W/K | 167.48 W/K |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against the stored solution:

> 14 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

No variable differs above rtol = 0.001. The maximum relative difference
over the 14 common variables is **2.25e-10** (`Q_dot_rad`). At rtol = 0
the tool also lists `AU_rad` at 1.06e-10 and `t_w_ex_rad` at 7.11e-11;
`epsilon_rad` (7.46e-11) and `NTU_rad` (3.93e-11) stay inside the absolute
tolerance 1e-9. Those residuals are the stored solution written with fewer
digits than the CoolSolve values (for example `Q_dot_rad` is stored as
1312.999293 and computed as 1312.999292704).

## Source and attribution

Jean Lebrun and Stéphane Bertagnolio, University of Liège, Thermodynamics
Laboratory, 17 March 2008. The file name is `JLSB080317` (initials and
date). EES licence stamp: Jean Lebrun, Laboratoire de Thermodynamique,
Université de Liège (`{$ID$ #1206}`), EES X7.966. The equations window
carries the title "Radiator reference model" and no further reference.

Source:
`~/Nextcloud/thermo_models/Model data bank/Heating_Cooling_Terminal_Units/Radiators/Radiator_RefSim_EES_Model_JLSB080317.EES`
(inventory `TM-0262`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): equations stored as
  **RTF**; unit system already `SI MASS DEG PA C J`, so no value was
  converted; `$UnitSystem` removed; licence tag removed; no lookup or
  parametric table; no warning in the extract report. The trailing NUL
  byte of the extracted text was dropped.
- **Diagram-window inputs restored as equations.** `M_dot_w_rad`,
  `t_a_in`, `t_w_su_rad`, `n_rad`, `AU_rad_n`, `t_a_in_n` and
  `t_w_su_rad_n` are quoted strings. Each is assigned the value written in
  that string, which is also the stored value. The simulation equations
  are unchanged, so the unknowns are not replaced by stored numbers (those
  stay in `.initials`).
- **Unit labels.** Temperatures are annotated `[°C]` (the original wrote
  `[C]`). `AU_rad_n` and `AU_rad` are annotated `[W/K]` (the original wrote
  `[W/C]` on `AU_rad_n`); `c_w` is annotated `[J/(kg K)]` (the original
  wrote `[J/(kg*C)]`). The numbers are the same.
- Comments translated into short English trailing comments. Section titles
  of the original ("Inputs", "Parameters", "Simulation") are kept. No
  equation was rewritten.
- **Level**: 14 equations (0), largest block 1 (0), no procedure or array
  (0), one component (0), the conductance uses an empirical exponent on
  the temperature-difference ratio, so the off-design criterion scores 1,
  solves from the default guesses (0) → score 1 → level 1.

## Limitations and CoolSolve gaps

The specific heat of water is a constant. The air is an imposed
temperature: there is no air mass flow and no air exit state. One
operating point is stored; the same equations accept other flows and
temperatures. The factor 0.9 in the conductance correction, and the added
0.1, are as written in the original.

No CoolSolve gap. The file uses only assignments, `abs` and `exp`.

## Related models

`CSL-0175` (Simplified cooling ceiling): cooling ceiling by the same authors and the same date, with the same effectiveness `1 − exp(−NTU)`. This file is the hot-water radiator.

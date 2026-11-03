# 1 GW power plant cooled by river water (exercise 6.22)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0236`

Teaching exercise for a 1 GW power plant that rejects heat to river water. The condensation pressure fixes the saturation temperature, taken as the low temperature of an equivalent Carnot cycle. The model returns the Carnot efficiency, the condenser heat rate and the river temperature rise.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water |
| **Size** | 13 equations (largest block: 1) |
| **Source** | thermo_models, file `THD09_R04_Ex04.EES` |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7d66c3b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The equation window is titled "THD09 - R04 - Ex04" and labelled "[Exercice 6.22]". It does not add a prose statement. The given data and the resolution comments are the exercise.

A power of `W_dot = 1000E6` W is rejected from an equivalent Carnot cycle whose high temperature is `t_c = 550` °C. The condensation pressure is `P_cond = 10000` Pa. River water carries the condenser heat away. The window asks for the Carnot efficiency, the condenser heat rate and the river temperature change after perfect mixing.

## Model

The condensation pressure gives the condensation temperature at saturation, and that temperature is the low temperature of the equivalent Carnot cycle, as in the original:

\[
t_\mathrm{cond} = T(\mathrm{Water},\, P = P_\mathrm{cond},\, x = 1), \quad t_f = t_\mathrm{cond}
\]

`temperature` returns °C. `t_f = t_cond` stays. The fluid stays `Water`.

The Carnot efficiency, with both temperatures in °C, is kept as written:

\[
\eta = \frac{t_c - t_f}{t_c + 273.15}
\]

The same efficiency is also `W_dot/Q_dot_utile`. The condenser heat rate is `Q_dot_utile - W_dot`, as in the original.

River water, assuming perfect mixing after the heat is rejected, as in the original:

\[
\dot Q_\mathrm{cond} = \dot m_w \, c_{p,w} \, \Delta t_w
\]

`q_v_w = 8*60*10/60` is kept (m³/s, as in the original). `rho_w = 1000` kg/m³ and `c_p_w = 4187` J/(kg·K) stay. `W_dot = 1000E6` and `P_cond = 10000` stay. No number is scaled.

| Input | Value |
|---|---|
| `t_c` | 550 °C |
| `P_cond` | 10000 Pa |
| `W_dot` | 1000E6 W |
| `q_v_w` | `8*60*10/60` m³/s |
| `rho_w` | 1000 kg/m³ |
| `c_p_w` | 4187 J/(kg·K) |

Those assignments are already equations. With `$UnitSystem` removed, the window is square: 13 equations, 13 variables. No stored unknown was added. This is not a cycle of states, so no diagram-state array was added.

## How to run

```bash
coolsolve ./power_plant_river_carnot.eescode
```

CoolSolve reports 4 iterations with the shipped `.initials` and 38 without them. The system is square, the largest block has size 1, and 11 of the 13 blocks are direct evaluation. There is no `coolsolve.conf`. The `.initials` file is the EES stored solution.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `eta` [−] | 0.6125173675226 | 0.6125375648 | 3.30e-05 |
| `Q_dot_cond` [W] | 632606766.6578 | 632552936.4 | 8.51e-05 |
| `DELTAt_w` [°C] | 1.888603912879 | 1.888443206 | 8.51e-05 |
| `t_cond` [°C] | 45.8063289238 | 45.78970357 | 3.63e-04 |
| `t_f` [°C] | 45.8063289238 | 45.78970357 | 3.63e-04 |

`t_f` equals `t_cond`. `Q_dot_utile` prints 3.30e-05 (1632606766.658 W against the stored 1632552936 W). `t_c`, `P_cond`, `W_dot`, `q_v_w`, `q_m_w`, `rho_w` and `c_p_w` match.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `THD09_R04_Ex04.EES` (EES X7.888, 13 variables), compared with `compare_solution.py` without `--ees-units`. The tool's summary line is:

`13 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The unit system of the file is already pascal, Celsius and joule, so no value was scaled and `--ees-units` was not used.

Every common variable is inside rtol 0.001. The largest relative difference printed by the tool is 3.63e-04, on `t_cond`. `t_f` prints the same 3.63e-04. Unrounded, both are 3.629488367788e-04, and that is the maximum over all 13 common variables. `temperature(Water, P=10000 Pa, x=1)` returns 45.8063289238 °C; the stored saturation temperature is 45.78970357 °C. The equation is satisfied. `eta` prints 3.30e-05, `Q_dot_cond` prints 8.51e-05 and `DELTAt_w` prints 8.51e-05.

All 13 equations are satisfied (max residual 6.6595e-10). CoolSolve reports 4 iterations with the `.initials` file and 38 without it.

## Source and attribution

The file sits in the `SBe` folder and is named `THD09_R04_Ex04.EES`. The inventory notes say the solution is by S. Bertagnolio (THD09). SB is Stéphane Bertagnolio. The EES licence tag is Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege; that tag is the licence holder, not the author.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R04/SBe/THD09_R04_Ex04.EES`.

Candidate TM-0373. No duplicate group. Teaching exercise. Course: *Thermodynamique appliquée* (ULiège), THD09, R04, exercise 6.22 (2009). EES X7.888. The file date in the collection is 2009-03-02.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `THD09_R04_Ex04.EES` (EES X7.888, plain text, 13 stored variables, no tables, no warnings). With `$UnitSystem` removed, the extraction is square: 13 equations, 13 variables, largest block 1. No stored unknown was added. No diagram-state array was added. Comments translated to English. `WATER` is written `Water`. `TEMPERATURE` is written `temperature`.
- **Units**: `$UnitSystem SI MASS DEG PA C J`. Already pascal, Celsius and joule. No number was scaled. `$UnitSystem` was deleted. The file contains no `$TABSTOPS` and no `$Export`. `.initials` is the EES stored solution, unchanged.
- **Equations kept**: `eta = (t_c-t_f)/(t_c+273.15)` with both temperatures in °C; `t_f = t_cond`; `q_v_w = 8*60*10/60`; `rho_w = 1000`; `c_p_w = 4187`; `W_dot = 1000E6`; `P_cond = 10000`.
- **Level**: equations 13 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one plant energy balance, not three coupled components → 0; no calibration, off-design or dynamics → 0; converges with the stored guesses (4 iterations) and without them (38 iterations), no `coolsolve.conf` → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The model is an equivalent Carnot cycle plus one river energy balance. It is not a cycle of states.

`temperature(Water, P=P_cond, x=1)` differs from the stored saturation temperature by a relative 3.63e-04. The equations are satisfied, and every common variable is inside rtol 0.001.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` is empty.

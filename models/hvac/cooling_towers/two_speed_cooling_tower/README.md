# Two-speed cooling tower

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0030`

Operating regimes of an evaporative cooling tower equipped with a two-speed
fan (nominal speed and half speed). Each regime is rated with the
effectiveness–NTU method written between the water and a fictitious ideal dry
fluid whose temperatures are the wet-bulb temperatures of the moist air.
Given the set-point temperature of the water at the tower outlet, the model
returns the outlet temperatures, the heat rejected in each regime and the
weighted-mean fan powers, and shows which regime mixtures can physically meet
the set-point.

| | |
|---|---|
| **Category** | HVAC › Cooling towers |
| **Fluids** | Moist air (`AirH2O`); water with constant c = 4187 J/(kg·K) |
| **Size** | 54 equations (largest block: 11) |
| **Source** | ULiège MSTh course, exercise MSTH 051024 Ex 2 — CoolSolve example `cooling_tower` + original EES file |
| **Authors** | ULiège MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the solution stored in the original EES file |

## Problem statement

Exercise 2 of the MSTh session of 2005-10-24 (built on exercise 1 of the same
session, the tower with AU = 90 kW/K, 50 kg/s of water and 60 kg/s of air,
35 °C inlet water). Translated from the original header:

> Determine the operating regimes, the outlet temperatures, the heat rates
> dissipated and the mean electrical powers consumed by the tower of the
> previous question, when the set-point temperature of the water at the tower
> outlet is varied from 26 to 36 °C. The tower is equipped with a two-speed
> fan: nominal speed and half speed. Power consumed by the fan at nominal
> speed: 15 kW. Assume that the air flow rate and the heat-transfer
> coefficient of the tower are both practically proportional to the fan
> rotational speed. Neglect the possible variation of the fan efficiency.

## Model

- **Rating of each regime** (course equations, page 95): the tower is rated
  like a dry counterflow exchanger working between the water and a fictitious
  ideal dry fluid whose temperatures are the wet-bulb temperatures of the
  moist air: fictitious capacity rates $\dot C_f = \dot m_a c_{p,f}$ with
  $c_{p,f} = (h_{a,ex}-h_{a,su})/(t_{wb,ex}-t_{wb,su})$, UA referred to that
  fictitious fluid by $AU_f = AU\,c_{p,f}/c_p$ ($c_p$ = inlet moist-air
  specific heat), then $\varepsilon$-NTU, and the heat rejected closed by the
  air-side and water-side balances. The outlet air is saturated (`R=1`).
  The reduced regime duplicates the equations with the index `_r` and half
  the air flow and UA (fan laws given in the exercise).
- **Fan power**: 15 kW at nominal speed, identified through the air-side
  power $\dot V_a\,\Delta p/\eta$ with $\eta = 0.6$ (hypothetical value that
  fixes the tower frontal area `A`; it cancels out of the results).
- **Regime at the set-point**: two weighting laws mix the regime outlet
  temperatures to the set-point `t_w_ex_set` — `theta` between the nominal
  and reduced regimes, `theta_1` between the reduced and off regimes — each
  giving a weighted-mean fan power. The physical regime at a given set-point
  is the one whose weighting fraction lies in [0, 1]; at other set-points the
  fraction falls out of [0, 1] and the model reports it (part of the
  exercise).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `AU` / `AU_r` UA, nominal / half speed | 90 / 45 kW/K | `Q_dot` / `Q_dot_r` heat rejected | 1.977 / 1.211 MW |
| `M_dot_w` water flow | 50 kg/s | `t_w_ex` / `t_w_ex_r` water outlet | 25.55 / 29.22 °C |
| `M_dot_a` / `M_dot_a_r` air flow | 60 / 30 kg/s | `t_wb_su` inlet wet-bulb | 20.96 °C |
| `t_w_su` / `t_a_su` / `RH_su` / `P` | 35 °C / 25 °C / 0.7 / 1 atm | `theta` / `theta_1` weighting fractions | −1.579 / 0 |
| `t_w_ex_set` set-point (default run) | 35 °C | `W_dot` / `W_dot_r` fan power | 15 / 1.875 kW |
|  |  | `W_dot_mean` / `W_dot_mean_1` | −18.8 / 0 kW |

At the default set-point 35 °C (= water inlet temperature) no cooling is
needed: `theta_1` = 0 gives `W_dot_mean_1` = 0 (fan off), while `theta` falls
out of [0, 1] — that mixing law has no physical solution at this set-point,
and `W_dot_mean` = −18.8 kW is not a physical result. Sweeping `t_w_ex_set`
from 26 to 36 °C (parametric study in the GUI) shows the regime change: near
26 °C the nominal/reduced mixture (`theta` ≈ 0.88) is the physical one.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. theta, theta_1 and the mean fan powers vs t_w_ex_set
     (26–36 °C), showing the physical regime in [0, 1] -->

## How to run

Open `two_speed_cooling_tower.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./two_speed_cooling_tower.eescode
```

The shipped `two_speed_cooling_tower.initials` (guess values = the EES stored
solution) is required: without it the coupled wet heat-transfer loop does not
converge (already noted in the CoolSolve example). The default run uses
`t_w_ex_set` = 35 °C; sweep it in the GUI (*Parametric* tab) to redo the
26–36 °C study of the exercise.

## Verification

Reference: the solution stored in the original EES file `MSTH051024EXERCICE2.EES`
(EES 7.458, `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh -
Repetitions/TP 06/`, candidate TM-0094), which was last solved by EES with
`t_w_ex_set` = 35 °C — used as the default run. Comparison with
`tools/compare_solution.py`:

> `54 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

Largest relative deviation 7.1·10⁻⁴ (`omega_f_r`, `c_p_f_r`,
`C_dot_min_f_r`), from the humid-air property backend (EES 7.458 vs CoolProp
`AirH2O` specific heats and wet-bulb temperatures), well within the property
tolerance of CoolSolve `docs/ees_import.md` §11. The 55th stored variable,
`R`, is the empty humidity-ratio keyword holder (no stored value).

## Source and attribution

Original exercise (in French) from the ULiège *Machines et systèmes
thermiques* course (J. Lebrun, V. Lemort, S. Bertagnolio), session of
2005-10-24, exercise 2; the `{$ID$}` stamp is the J. Lebrun laboratory EES
licence, not the authorship. The model was rewritten in English as the
CoolSolve example `examples/cooling_tower.eescode` by S. Quoilin; this library
model follows the EES original, which supersedes that example — it remains in
the CoolSolve repository as a test case.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/cooling_tower.eescode`
  (inventory candidate `CSX-011`);
- original EES file with its stored solution:
  `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh -
  Repetitions/TP 06/MSTH051024EXERCICE2.EES` (EES 7.458, candidate TM-0094;
  duplicate copy TM-0088).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `MSTH051024EXERCICE2.EES`): unit system already SI-°C-Pa-J (no conversion
  needed); EES licence tag removed; no lookup or parametric tables; complete
  stored solution (54 valued variables). The raw extraction has 53 equations
  for 54 unknowns: `t_w_ex_set` is defined only by the GUI parametric study
  of the exercise (its commented test line `"t_w_ex_set=25"` is inactive in
  the original; that line was not kept). Following CoolSolve
  `docs/ees_import.md` §8, the value of the stored solution (35 °C) was added
  as the default run — the file stays valid EES and reproduces the reference.
- **Difference with the CoolSolve example**: the example activates
  `t_w_ex_set=25` (fixed set-point run, theta ≈ 1.15, theta_1 ≈ −0.73, both
  out of [0, 1]); the library model follows the EES original and sweeps the
  set-point as the exercise intends. The example's `//c_p_f=4000` provisional
  comments are kept as a note in the file.
- **2026-10-05 — curation**: standard header added, comments translated from
  French to English, section titles and SI units added. No change to any
  equation or value; variable names kept.
- **Level**: score 4 (54 equations, block of 11, part-load regime logic,
  curated guesses needed) → level 2 as assigned by the task card, moved down
  one notch: single-component course exercise with one solution loop.

## Limitations and CoolSolve gaps

- Constant water specific heat (4187 J/(kg·K)) and a fictitious-fluid ε-NTU
  rating on wet-bulb temperatures (course-level accuracy, page 95 equations).
- The two weighting laws are both solved: outside the set-point range where a
  mixture is physical, the corresponding fraction and mean power lose their
  physical meaning (read the regime from the fraction in [0, 1]).
- CoolSolve has no parametric tables (registered gap `CS-GAP-PARAMETRIC`):
  the 26–36 °C sweep of the exercise is done with a GUI parametric study on
  `t_w_ex_set`. The native file itself runs and is not blocked.

## Related models

- `CSL-0016` *moist_air_cooling_coil_contact_factor* and `CSL-0017`
  *chilled_water_cooling_coil*: other humid-air (AirH2O) component models.
- CoolSolve example `cooling_tower2` (single-speed fan tower, candidate
  CSX-012, recorded as a duplicate at the C-46 review): its equations are the
  nominal-speed regime block of this model (same inputs: AU = 90 kW/K, 50 kg/s
  of water at 35 °C, 60 kg/s of air at 25 °C and 70 % RH), without the fan
  power; it is not imported separately.

- `CSL-0076` *cooling_tower_direct_contact_refsim*: another cooling tower of
  the library, from the ULiège model bank: a direct-contact tower whose heat
  transfer coefficient, air-side pressure drop and fan characteristic are
  referred to the nominal conditions (both flow rates and the fan speed act on
  them).
- `CSL-0064` *psychrometric_mixer_condensation*: adiabatic mixing of room
  and outdoor air with condensation in the mixer (same humid-air property
  offsets).
- `CSL-0065` *cooling_tower_condenser_water*: level-1 exercise on the same
  equipment (total mass/energy balance on humid air, air flow and make-up
  water for one operating point), without the ε-NTU rating nor the fan.

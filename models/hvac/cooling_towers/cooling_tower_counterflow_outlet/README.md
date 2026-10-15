# Counterflow cooling tower, outlet water temperature

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0179`

Outlet water temperature of a counterflow cooling tower. The tower is rated
as a dry counterflow exchanger between the water and a fictitious fluid whose
temperatures are the wet-bulb temperatures of the moist air (course equations,
page 95). The air leaving the tower is saturated. The exercise gives the dry
overall heat-transfer coefficient, the water and air flow rates and the inlet
water temperature.

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Cooling towers and evaporative equipment |
| **Fluids** | Moist air (`AirH2O`); water with constant c = 4187 J/(kg·K) |
| **Size** | 24 equations (largest block: 11) |
| **Source** | ULiège MSTh, session of 2005-10-24, exercise 1 |
| **Authors** | TBD (ULiège MSTh). The file names no person. The course is attributed to J. Lebrun, V. Lemort and S. Bertagnolio. |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise 1 of the MSTh session of 2005-10-24. Translated from the original header:

> Determine the water temperature at the outlet of a cooling tower under the
> following conditions: counterflow; overall heat-transfer coefficient in the
> dry regime 90 kW/K; water and air flow rates 50 and 60 kg/s; water
> temperature at the tower inlet 35 °C; atmospheric pressure 101325 Pa;
> ambient-air temperature and degree of saturation 25 °C, 70 %. Practical
> hint: take the air as saturated at the tower outlet.

The file stores the 70 % as `RH_su` and passes it as the relative-humidity
argument of the humid-air functions. The rating equations are those of
page 95 of the course notes, as the original says.

## Model

The tower is rated like a dry counterflow exchanger working between the water
and a fictitious fluid on the wet-bulb temperatures:

- inlet moist air: specific heat `c_p`, wet-bulb temperature `t_wb_su` and
  enthalpy `h_a_su` from `AirH2O` at 25 °C, 101325 Pa and relative humidity 0.70;
- fictitious specific heat \(c_{p,f} = (h_{a,ex} - h_{a,su})/(t_{wb,ex} - t_{wb,su})\),
  capacity rate \(\dot C_f = \dot m_a c_{p,f}\), and
  \(AU_f = AU\, c_{p,f}/c_p\);
- counterflow effectiveness–NTU on the water capacity rate
  \(\dot C_w = \dot m_w c_w\) and \(\dot C_f\);
- heat rate closed by the air-side balance \(\dot Q = \dot m_a (h_{a,ex} - h_{a,su})\)
  and the water-side balance \(\dot Q = \dot C_w (t_{w,su} - t_{w,ex})\);
- outlet air saturated (`R = 1`), so `t_wb_ex` is the dry-bulb temperature of
  that saturated state.

The original leaves a commented provisional value `c_p_f = 4000`. It is not
an equation; the fictitious specific heat is computed.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `AU` dry overall heat-transfer coefficient | 90 kW/K | `t_w_ex` outlet water temperature | 25.555 °C |
| `M_dot_w` water flow | 50 kg/s | `Q_dot` heat rate | 1.977 MW |
| `M_dot_a` air flow | 60 kg/s | `t_wb_su` inlet wet-bulb | 20.963 °C |
| `t_w_su` inlet water | 35 °C | `t_wb_ex` outlet wet-bulb (saturated air) | 28.765 °C |
| `t_a_su` / `RH_su` / `P` | 25 °C / 0.70 / 101325 Pa | `epsilon_f` effectiveness | 0.673 |

## How to run

Open `cooling_tower_counterflow_outlet.eescode` in the CoolSolve GUI and
press *Solve*, or from the model folder:

```bash
coolsolve ./cooling_tower_counterflow_outlet.eescode
```

The shipped `cooling_tower_counterflow_outlet.initials` holds the EES stored
solution as guesses. With those guesses the solve takes 5 iterations. Without
the file, the block of 11 (the wet rating loop) stops on a singular Jacobian.

## Results

| Quantity | CoolSolve | EES stored solution |
|---|---:|---:|
| Outlet water temperature `t_w_ex` | 25.555 °C | 25.555 °C |
| Heat rate `Q_dot` | 1.9773 MW | 1.9773 MW |
| Inlet wet-bulb `t_wb_su` | 20.963 °C | 20.961 °C |
| Outlet wet-bulb `t_wb_ex` | 28.765 °C | 28.768 °C |

The water leaves between the inlet wet-bulb (20.96 °C) and the inlet water
(35 °C). The heat rate is about 1.98 MW.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. outlet water temperature and heat rate versus the inlet
     air temperature (CoolSolve has no psychrometric chart yet) -->

## Verification

Reference: the solution stored in `MSTH051024exercice1.EES` (EES 7.458,
candidate TM-0093). `compare_solution.py` prints:

> `24 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The largest relative difference in that table is 6.52e-04, on `c_p_f`,
`omega_f`, `C_dot_f` and `C_dot_max_f` (exact maximum 6.515e-4 on `c_p_f`).
Nothing exceeds rtol = 0.001. The file has no humidity-ratio variable. The
humid-air quantities that move, all under the tolerance, are the inlet
specific heat `c_p` (6.40e-4), the wet-bulb temperatures `t_wb_su` (1.18e-4)
and `t_wb_ex` (9.31e-5), and the enthalpies `h_a_su` (3.54e-5) and `h_a_ex`
(1.96e-5): EES 7.458 against CoolProp `AirH2O`. They pull `c_p_f` with them.
`t_w_ex` differs by 8.8e-5 K (relative 3.46e-6) and `Q_dot` by 19 W
(relative 9.36e-6).

## Source and attribution

The equation window is headed "MSTH 051024 Exercice 1" and names no person.
The `{$ID$}` stamp is the J. Lebrun laboratory EES licence (Univ. Liège), not
the authorship, so `authors` is `TBD (ULiège MSTh)`. The inventory attributes
the course to J. Lebrun, V. Lemort and S. Bertagnolio.

Source (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 06/MSTH051024exercice1.EES`
(EES X7.458, candidate TM-0093, representative of duplicate group DG-0020).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): EES X7.458, unit system
  already `SI MASS DEG PA C J`, so no value was rescaled and the
  `$UnitSystem` directive was deleted. No lookup table and no parametric
  table. The equation window already contains the seven inputs; the system
  is square (24 equations, 24 variables), so no Diagram-window value was
  turned into an equation. The commented provisional `c_p_f = 4000` stays a
  comment. Property calls use `t_a_su`; the original wrote `T_a_su`, the
  same variable in EES. The licence tag was removed. No `$Export`,
  `concat$` or `EESFILEDIR$` line.
- **2026-10-15 — curation**: English comments and the standard header. No
  equation and no numerical input was changed.
- **Level**: equations 0 (24 < 50), largest block 1 (11, in 6–30), structure
  0 (no procedure, array or `DUPLICATE`), multi-zone 0, physics 0 (one
  operating point, `AU` given), numerics 1 (the block of 11 does not
  converge without the stored-solution guesses) → score 2 → level 2.

## Limitations and CoolSolve gaps

- The outlet air is taken as saturated, and the water specific heat is the
  constant 4187 J/(kg·K). `AU` is an input, not computed from the fill.
- Humid-air properties differ slightly between EES 7.458 and CoolProp; see
  *Verification*. No humidity ratio is computed.
- No CoolSolve gap blocks the file. `missing_features` is empty.

## Related models

- `CSL-0030` *two_speed_cooling_tower*: exercise 2 of the same session. Its
  nominal-speed rating is this model (same `AU`, flows and inlet state); it
  adds the half-speed regime, the fan power and the set-point weighting.
- `CSL-0076` *cooling_tower_direct_contact_refsim*: the same counterflow
  fictitious-fluid rating, as a reference simulation whose dry `AU`, air-side
  pressure drop and fan head depend on the flow rates and the fan speed.
  Different inputs and extra equations.
- `CSL-0198` *cooling_tower_wetbulb_exchanger*: MSTh R6 exercise 1, the
  same wet-bulb exchanger rating from a different file (28 equations).

# Dynamic greenhouse climate model with weather lookup

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0334`

Six-day dynamic simulation (10–15 Dec, Brussels TMY) of the climate of a
single-glass Venlo tomato greenhouse: the air, canopy, cover, floor and five
ground layers are heat-capacity nodes, the air moisture is a state (vapour
pressure), the pipe rail is a lumped heating system under proportional
control, and the roof vents open proportionally above the temperature
set-point. Outdoor weather and climate set-points are read hourly from the
companion lookup table. Flat EES translation of the [Greenhouses Modelica
library](https://github.com/QueraltAltes/Greenhouses-Library) climate model
described by Altes-Buch *et al.* — the dynamic form of
[`CSL-0333`](../greenhouse_steady_state/).

| | |
|---|---|
| **Category** | Buildings › Greenhouses |
| **Fluids** | humid air (correlations, no property calls) |
| **Size** | 186 equations (largest block: 64), 10 states |
| **Source** | [Greenhouses Modelica library](https://github.com/QueraltAltes/Greenhouses-Library) (example `Greenhouse_2`), BSD-3 |
| **Authors** | Queralt Altes-Buch (library); paper with S. Quoilin, V. Lemort |
| **License** | MIT (translation), credits to the original authors |
| **CoolSolve** | 0.4.0 — verified against an independent RK4 integration |

## Niche

Same climate correlations as [`CSL-0333`](../greenhouse_steady_state/), with
the ten heat and moisture capacitances integrated over six days of Brussels
TMY weather, a proportional pipe-power controller and proportional vents.
[`CSL-0042`](../../building_rc_network_3r2c/) is the dwelling counterpart
(weather lookup + `INTEGRAL`, no moisture or crop). [`CSL-0335`](../greenhouse_heating_pipe_dynamic/)
replaces the lumped pipe by a five-cell rail on an open-loop schedule.

## Problem statement

*How do the indoor climate of a heated Venlo tomato greenhouse and its
heating power evolve over six December days (mild overcast weather, a windy
cold front, then a clear cold spell) when the pipe-rail power is controlled
proportionally on the air-temperature set-point and the roof vents open
above set-point + 2 K?*

The boundary conditions — outdoor air temperature and humidity, global
irradiation, wind speed, sky temperature, temperature and CO₂ set-points —
are read from the companion table
`greenhouse_climate_dynamic-weather.csv` (145 hourly rows, extracted from
the TMY data file of the Greenhouses library, Brussels, starting 10 Dec).
Replace the table to simulate another period or site.

## Model

Single air zone (no thermal screen), fixed tomato canopy (LAI = 1.06, no
crop growth), CO₂ concentration prescribed by the set-point table (no CO₂
balance). All flux correlations — free and hindered convection, the
ventilation rate of Boulard & Baille, long-wave radiation with the view
factors of de Zwart, the PAR/NIR solar model, Stanghellini transpiration
and cover condensation — are those of [`CSL-0333`](../greenhouse_steady_state/),
whose README documents each equation with its reference in Altes-Buch *et
al.* Here the node balances carry their capacitances (paper, eqs. 2–8, 10):

$$\rho_{air} c_{p,air} h_{air} \frac{dT_{air}}{dt} = \dot q^{swr}_{air}
+ \dot q^{cnv}_{pip,air} + \dot q^{cnv}_{can,air} - \dot q^{cnv}_{air,flr}
- \dot q^{cnv}_{air,cov} - \dot h^{sens}_{air,out}$$

$$c_{leaf}\,LAI \frac{dT_{can}}{dt} = \dot q^{swr}_{can}
+ \dot q^{rad}_{pip,can} - \dot q^{cnv}_{can,air} - \dot q^{lat}_{can,air}
- \dot q^{rad}_{can,cov} - \dot q^{rad}_{can,flr}$$

$$\rho_{cov} c_{cov} \frac{e_{cov}}{\cos\varphi} \frac{dT_{cov}}{dt}
= \dot q^{swr}_{cov} + \dot q^{cnv}_{air,cov} + \dot q^{lat}_{air,cov}
+ \dot q^{rad}_{can,cov} + \dot q^{rad}_{flr,cov} + \dot q^{rad}_{pip,cov}
- \dot q^{cnv}_{cov,out} - \dot q^{rad}_{cov,sky}$$

$$C_{flr} \frac{dT_{flr}}{dt} = \dot q^{swr}_{flr} + \dot q^{rad}_{pip,flr}
+ \dot q^{rad}_{can,flr} + \dot q^{cnv}_{air,flr} - U_{flr,so1}(T_{flr}-T_{so1})$$

$$\rho_{so}\,c_{so}\,e_{so,i}\frac{dT_{so,i}}{dt} = \dot q^{cnd}_{so,i-1\,so,i}
- \dot q^{cnd}_{so,i\,so,i+1}, \qquad i = 1..5 \quad\text{(paper, eq. 8)}$$

$$\frac{M_{H_2O}\,h_{air}}{R\,T}\frac{dP^v_{air}}{dt} = \dot m^v_{can,air}
- \dot m^v_{air,cov} - \dot m^v_{air,out} \qquad\text{(paper, eq. 10, } T = 291\ \mathrm{K)}$$

with the soil layer thicknesses doubling downward (0.02–0.32 m) and the
deepest layer conducting to a 3 °C deep-ground boundary.

**Heating (lumped pipe rail)**: a proportional controller sets the pipe heat
release, and the (capacitance-free) pipe balance gives the pipe temperature
at which the rail releases it:

$$Q_{pip} = \min\left(\max\left(K_h (T_{air,SP} - T_{air}),\, 0\right),\, Q_{pip}^{max}\right)$$

with $K_h$ = 100 W/m²K and $Q_{pip}^{max}$ = 250 W/m² (P-band 2.5 K). The
PI controller of the source example (on the water mass flow rate) is
replaced by this P controller on the power — flat, transparent, and the
steady offset it leaves is visible in the results.

**Ventilation**: the roof vents open proportionally above the set-point
$u_{ven} = \min(\max(K_{ven}(T_{air} - T_{air,SP} - 2), 0), 1)$ with
$K_{ven}$ = 0.2 1/K (full opening at set-point + 7 K), plus the leakage of
`CSL-0333`; the ventilation rate follows paper eq. 14 (Boulard & Baille).

**Initial state**: `T_air` = `T_can` = 19 °C, `T_cov` = 8 °C, `T_flr` = 16 °C,
soil 14/12/10/8/5 °C, `VP_air` = 80 % RH at 19 °C.

### Inputs and outputs

| | |
|---|---|
| **Inputs** | lookup table `weather` (tau, T_out, RH_out, I_glob, u_wind, T_sky, T_air_sp, CO2_air_sp; hourly), construction parameters, controller constants, initial state |
| **Outputs** | 145-row hourly trajectory (`$IntegralTable`): T_air, T_can, T_cov, T_flr, T_so1..5, VP_air, RH_air, Q_pip, u_ven, f_air_out, weather inputs |

## How to run

```bash
coolsolve ./greenhouse_climate_dynamic.eescode
```

The ten states are integrated with RK4 at the step written in `INTEGRAL`
(120 s, 4320 steps). The trajectory is written hourly, and 120 s divides
the hour, so each row is a step. Without that step the default RK4 step is
above the stability limit of the air and cover (about 50–175 s) and the run
diverges. `integralMethod = BDF` with `integralRelTol = 1e-4` and
`integralAbsTol = 1e-6` does not need the step: the hourly temperatures stay
within 0.03 K of RK4 at 15 s. The shipped file keeps 120 s, which is what
the table below compares. Times are in *Solving time*. The reference itself is

```bash
python3 greenhouse_climate_dynamic_ref.py
```

(numpy and scipy, classical RK4 at 30 s). It prints the max difference
against the CoolSolve hourly table when that file is present.

## Results

| Quantity (over 6 days) | min | max |
|---|---|---|
| Air temperature `T_air` [°C] | 18.73 | 19.58 |
| Canopy temperature `T_can` [°C] | 17.28 | 19.39 |
| Cover temperature `T_cov` [°C] | 8.0 | 14.5 |
| Floor temperature `T_flr` [°C] | 14.1 | 20.0 |
| Air vapour pressure `VP_air` [Pa] | 1167 | 1811 |
| Relative humidity `RH_air` [%] | 53.5 | 80.6 |
| Heating power `Q_pip` [W/m²] | 42 (sunny hours) | 200 (initial hour only) |

The P controller holds the air between set-point − 1.3 K (first night) and
set-point − 0.4 K. The 250 W/m² cap is not reached: `Q_pip` is 200 W/m² only
at the initial instant (`T_air` starts 2 K below the 21 °C set-point) and
stays below 127 W/m² after that. The vents never open (December). The soil
layers still carry their initial transient (T_so5 rises from 5 to 6.5 °C),
i.e. six days is not a periodic state — as in the source example, which
starts on the same date.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![...](figures/greenhouse_climate_dynamic_trajectories.png)  + one-line caption -->

## Verification

The trajectory was checked against an **independent RK4 integration** of the
same equations (`greenhouse_climate_dynamic_ref.py` in this folder, classical
RK4, h = 30 s, written from the Greenhouses library sources, hourly linear
interpolation of the same weather table). Over the 145 hourly rows:

| | CoolSolve (h = 120 s) | RK4 reference (h = 30 s) | max difference |
|---|---|---|---|
| `T_air` [°C] | 18.926 (end) | 18.926 (end) | 0.0014 |
| `T_can` [°C] | 17.754 (end) | 17.754 (end) | 0.0031 |
| `T_cov`, `T_flr`, soil layers [°C] | — | — | ≤ 0.00015 |
| `VP_air` [Pa] | 1235.5 (end) | 1235.6 (end) | 0.019 |

Max relative difference over these ten states: **1.7·10⁻⁴** (on `T_can`).
The heating power, which is `100·(T_sp − T_air)` clipped to 0–250 W/m²,
follows within 0.15 W/m². The day/night moisture cycle (condensation at
night, transpiration-driven rise during the day, about 1200–1800 Pa) is the
physical plausibility check.

## Solving time

Release build, one thread, six days (518 400 s). The file is RK4 at 120 s.
BDF is `integralMethod = BDF` in `coolsolve.conf`, with
`integralAbsTol = integralRelTol / 100`. Evaluations include the Jacobians
and the rejected steps.

| | evaluations | wall time | hourly temperatures vs RK4 at 15 s |
|---|---:|---:|---:|
| this file, RK4 at 120 s | 17 280 | 0.57 s | 0.003 K |
| BDF, `integralRelTol` 1e-4 | 2 921 | 0.12 s | 0.021 K |
| BDF at the default 1e-6 | 10 700 | | 0.0005 K |
| `greenhouse_climate_dynamic_ref.py`, RK4 at 30 s | | about 6 s | the reference |

One evaluation of the right-hand side takes 33 µs: only the blocks that
depend on the time or a state are solved, by slots, and an explicit block
carries no Jacobian. The pipe balance is the one block that stays implicit.
The 8.0 min (477 s) of 2026-11-10 was the algebraic solver copying the state
at every block of every stage, on a machine about three times slower than
these figures (the Python script took 20 s there, 6 s here).

The fixed step stays in the file because it is the verified trajectory.
RK4 without it diverges. BDF's step follows the tolerance.

## Source and attribution

- **Original model**: Greenhouses Modelica library —
  <https://github.com/QueraltAltes/Greenhouses-Library> (example
  `Greenhouse_2.mo`), BSD-3 license, commit `89ae0e8`.
- **Data**: weather and set-point table extracted from
  `Greenhouses/Resources/Data/10Dec-22Nov.txt` and `SP_10Dec-22Nov.txt`
  (TMY Brussels) of the same library.
- **Authors**: Queralt Altes-Buch (library and climate model), on the
  greenhouse models of Bot (1983), de Zwart (1996), Stanghellini (1987).
- **Scientific reference**: Q. Altes-Buch, S. Quoilin, V. Lemort,
  *A modeling framework for the integration of electrical and thermal energy
  systems in greenhouses* (manuscript, University of Liège);
  documentation: <https://greenhouses-library.readthedocs.io>.

## Conversion log

- **2026-11-09 — import (T-TRANSLATE)**: flat translation of the Greenhouses
  library climate model with capacitances; flux correlations identical to
  `CSL-0333` (see its conversion log). The screen, top air zone, lighting,
  CO₂ balance, crop-yield model, PID controllers and state-graph controls of
  the source example are out of scope (documented simplification).
- Controllers: PI on water mass flow (source) → P on pipe power (this
  model); PI on vents (source) → P on vents opening. The air heat capacity
  uses ρ·cp = 1.2·1005 (harmonized, see CSL-0333).
- `c_cov` renamed `cp_cov` (case collision with the capacitance `C_cov`).
- The convection power laws carry a smooth floor `((ΔT)²+10⁻⁸)^0.165`
  on the cover and `^0.16` on the pipe (regularization of the
  `max(1e-9,·)` guard; negligible above 0.01 K).
- Integration step fixed at 120 s (5th INTEGRAL argument): the automatic
  step is too large for the air/cover time constants (RK4 instability,
  solver diverges at t ≈ 1000 s).
- **2026-11-10 — correction**: the floor balance did not subtract
  `q_rad_flr_cov` (the cover receives that long-wave flow; the floor must
  lose it). Re-solved and re-checked against RK4. The check is
  `greenhouse_climate_dynamic_ref.py`.
- **2026-11-10 — solving time**: the 8 min figure was the march before a
  stage stopped copying the state. Current times, and BDF, are in *Solving
  time*.
- **Level**: equations 186 (1) + largest block 64 (2) + no function or
  array (0) + multi-zone (1) + dynamics (1) + default guesses (0) = 5
  → level 3.

## Limitations and CoolSolve gaps

- No thermal screen (no top air zone), no lighting, no CO₂ balance, no crop
  growth; the heating pipe is lumped (see [`CSL-0335`](../greenhouse_heating_pipe_dynamic/)
  for the discretized pipe rail).
- P controllers leave a steady offset to the set-point (by design).
- The fixed 120 s step is the RK4 stability limit of the air and cover
  (about 50–175 s; high ventilation in summer goes below 100 s). BDF with a
  tolerance replaces that step (*Solving time*). The shipped file keeps 120 s.
- No CoolSolve gaps (`missing_features` empty).

## Related models

- [`CSL-0333`](../greenhouse_steady_state/): the steady state of this model
  (same correlations, capacitances dropped).
- [`CSL-0335`](../greenhouse_heating_pipe_dynamic/): same climate core,
  heating by a discretized pipe rail driven from the table.
- [`CSL-0042`](../../building_rc_network_3r2c/): the same simulation pattern
  (weather lookup + INTEGRAL) on a dwelling.

# Greenhouse heating pipe rail: discretized dynamic model

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0335`

Six-day simulation (10–15 Dec, Brussels TMY) of the pipe-rail heating
circuit of a Venlo tomato greenhouse: the pipe loop is divided into five
cells in series, each with the water temperature as a state (finite-volume
energy balance, paper eq. 28), exchanging hindered convection with the air
and long-wave radiation with the canopy, floor and cover. The climate core
is the one of [`CSL-0334`](../greenhouse_climate_dynamic/); the heating
circuit boundary conditions — supply temperature and mass flow rate
(weather-compensated schedule) — join the weather in the lookup table.

| | |
|---|---|
| **Category** | Buildings › Greenhouses |
| **Fluids** | humid air, water (constant property, as in the source) |
| **Size** | 222 equations (largest block: 90), 15 states |
| **Source** | [Greenhouses Modelica library](https://github.com/QueraltAltes/Greenhouses-Library) (example `Greenhouse_2`, `HeatingPipe.mo`), BSD-3 |
| **Authors** | Queralt Altes-Buch (library); paper with S. Quoilin, V. Lemort |
| **License** | MIT (translation), credits to the original authors |
| **CoolSolve** | 0.4.0 — verified against an independent RK4 integration |

## Niche

Same climate core as [`CSL-0334`](../greenhouse_climate_dynamic/), with the
pipe rail split into five finite-volume water cells (the heating-circuit
model the source paper adds on top of an isothermal pipe). The supply
temperature and the mass flow are an open-loop weather-compensated schedule,
so the air temperature is no longer held by a feedback controller.

## Problem statement

*How do the water temperature along the pipe rail and the greenhouse
climate respond when the heating circuit is driven open-loop — supply
temperature and flow rate following a weather-compensated schedule — instead
of by a feedback controller?* The model demonstrates the discretized
heating-pipe model of the Greenhouses library (the element the paper
improves over earlier greenhouse models, which assumed isothermal pipes)
and its two-way coupling with the climate: the pipe cells radiate to the
canopy, floor and cover at their local temperature, and the climate feeds
back through those same surfaces.

## Model

Climate core, flux correlations and control of the roof vents:
[`CSL-0334`](../greenhouse_climate_dynamic/) (equations and references in
its README; here the pipe terms of every node balance are the sums over the
five cells, e.g. $\dot q^{cnv}_{pip,air} = \sum_i \dot q^{cnv}_{pip\,i,air}$).
The pipe rail replaces the lumped heating system:

**Pipe cells** (paper, eq. 28; `HeatingPipe.mo` with the `Flow1DimInc`
finite-volume fluid model, upwind discretization, constant-property water
and constant heat-transfer coefficient of the `Ideal` model replaced by the
hindered-convection correlation):

$$C_w \frac{dT_{w,i}}{dt} = \dot m_{pip}\,c_{p,w}\,(T_{w,i-1} - T_{w,i})
- \dot q_{pip,i}, \qquad i = 1..5, \quad T_{w,0} = T_{su,pip}$$

$$C_w = \frac{\rho_w c_{p,w}\,\pi\,d_{int}^2/4\,l_{pip}}{5} = 3.24\cdot10^3\ \mathrm{J/m^2K}$$

with $l_{pip}$ = 2.232 m/m², $d_{int}$ = 0.047 m (0.051 m outer, 2 mm wall).
Each cell releases one fifth of the lumped pipe exchange of
[`CSL-0333`](../greenhouse_steady_state/): hindered convection to the air
($1.99\,|\Delta T|^{0.32}$, Bot 1983) and long-wave radiation to the canopy,
the floor and the cover, with the same emissivities and view factors.

**Heating-circuit boundary conditions** (table `heating`, hourly): a
weather-compensated supply temperature $T_{su,pip} = \mathrm{clip}(78 -
1.1\,T_{out},\,58,\,75)$ °C and a mass flow rate $\dot m_{pip} = 1.8\cdot10^{-3}
\cdot\mathrm{clip}(0.08\,(T_{air,SP}-T_{out}) - I_{glob}/300,\,0.05,\,1)$
kg/m²s — high on cold nights, reduced by solar gains. The schedule is an
open-loop surrogate for the three-way-valve control of the source paper:
the model shows both its success (air within a 3 K band) and its limit
(the air runs up to 2.2 K above the set-point, nights included, while a
feedback controller would throttle).

**Initial state**: climate as `CSL-0334`, pipe cells at 40 °C.

### Inputs and outputs

| | |
|---|---|
| **Inputs** | lookup table `heating` (tau, T_out, RH_out, I_glob, u_wind, T_sky, T_air_sp, CO2_air_sp, T_su_pip, M_dot_pip; hourly), construction parameters, initial state |
| **Outputs** | 145-row hourly trajectory (`$IntegralTable`): T_air, T_can, T_cov, T_flr, T_so1..5, VP_air, T_w1..5, RH_air, Q_pip, u_ven, f_air_out, weather and heating inputs |

## How to run

```bash
coolsolve ./greenhouse_heating_pipe_dynamic.eescode
```

Fifteen states, RK4 at a fixed step of 60 s (8640 steps, about 25 min). At 120 s the
moisture state drifts by about 1.2 % and `T_air` by 0.5 K against a 30 s
reference, so the shorter step is kept. The trajectory is written hourly. The
reference itself is

```bash
python3 greenhouse_heating_pipe_dynamic_ref.py
```

(numpy, classical RK4 at 30 s, about 7 s). It prints the max difference
against the CoolSolve hourly table when that file is present.

## Results

| Quantity (over 6 days) | min | max |
|---|---|---|
| Air temperature `T_air` [°C] | 19.0 | 22.2 |
| Cover temperature `T_cov` [°C] | 8.0 | 15.1 |
| Air vapour pressure `VP_air` [Pa] | 1234 | 1986 |
| Pipe cell 1 (supply end) `T_w1` [°C] | 40 (initial) | 67.7 |
| Pipe cell 5 (return end) `T_w5` [°C] | 38.7 | 53.2 |
| Pipe heat release `Q_pip` [W/m²] | 69 (initial) | 149 |

After the first hour the rail releases 87–149 W/m². At the peak (hour 2,
outdoor air 5 °C, no sun) the water falls from 67.5 °C to 52.6 °C along the
five cells. The open-loop schedule lets `T_air` rise to 2.2 K above the
20 °C set-point; the vents open on those hours (`u_ven` ≤ 0.038). The cells
do not fall back to the air temperature: the supply end stays above 55 °C.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![...](figures/greenhouse_heating_pipe_dynamic_pipe_profile.png)  + one-line caption -->

## Verification

The trajectory was checked against an **independent RK4 integration** of
the same equations (`greenhouse_heating_pipe_dynamic_ref.py` in this folder,
classical RK4, h = 30 s, written from the Greenhouses library sources, same
table). Over the 145 hourly rows:

| | CoolSolve (h = 60 s) | RK4 reference (h = 30 s) | max difference |
|---|---|---|---|
| pipe cells `T_w1..5` [°C] | 67.47…53.07 (end) | 67.47…53.07 (end) | 0.0015 |
| `T_air` [°C] | 22.047 (end) | 22.036 (end) | 0.018 |
| `T_can`, `T_cov`, `T_flr`, soils [°C] | — | — | ≤ 0.0048 |
| `VP_air` [Pa] | 1349.8 (end) | 1349.6 (end) | 1.05 |

Max relative difference over these fifteen states: **8.3·10⁻⁴** (on
`T_air`). The deviation is the integration step, not the equations. The
water enthalpy drop equals the heat release only when the cells store no
heat; on the hourly rows the storage term reaches tens of W/m².

## Solving time

Measured 2026-11-10, CoolSolve 0.4.0, six days (518400 s):

| | step | steps | wall time |
|---|---|---|---|
| `greenhouse_heating_pipe_dynamic_ref.py` | 30 s | 17280 | 6.8 s |
| `coolsolve` | 60 s | 8640 | 25.1 min (1503 s) |

CoolSolve is slower although it takes half as many steps, and although this
model is explicit once the fifteen states are pinned: there is no algebraic
unknown left. Each RK4 stage still calls the full algebraic solver (four
solves per step, about 43 ms each, about 34600 solves). The Python script
evaluates the cell and climate fluxes directly.

Four changes would close most of that gap, in this order:

1. A march residual that substitutes the explicit equations and runs Newton
   only on the blocks that stay implicit. On this model that set is empty,
   so a stage should be one residual evaluation. The integrator needs the
   integrands, not a full solve report.
2. A cached map of the pinned variables and a reused automatic-differentiation
   tape. Today both are rebuilt at every stage, and the cost grows with the
   number of blocks times the number of variables. That walk, not an implicit
   unknown, is why this model is slower than CSL-0334.
3. A Jacobian kept along the trajectory, refreshed from one residual per
   smooth stage. The default rebuilds it at every Newton iteration, and
   nothing is kept from one stage to the next.
4. A BDF or DASSL step, which can take longer steps than the fixed RK4 the
   air and cover time constants currently force. That cuts the number of
   stages; it does not make one stage cheaper. Index reduction does not
   apply: the pipe cells are explicit ODEs.

The algebraic sibling CSL-0333 does not show this gap: there the 1.3 s
CoolSolve run against a 1 ms scipy root is process startup and the report.

## Source and attribution

- **Original model**: Greenhouses Modelica library —
  <https://github.com/QueraltAltes/Greenhouses-Library>
  (`Components/Greenhouse/HeatingPipe.mo` and example `Greenhouse_2.mo`),
  BSD-3 license, commit `89ae0e8`.
- **Data**: weather columns extracted from `Resources/Data/10Dec-22Nov.txt`
  and `SP_10Dec-22Nov.txt` (TMY Brussels) of the same library; the heating
  schedule columns are the weather-compensated rule documented above.
- **Authors**: Queralt Altes-Buch (library and climate model), on the
  greenhouse models of Bot (1983), de Zwart (1996), Stanghellini (1987).
- **Scientific reference**: Q. Altes-Buch, S. Quoilin, V. Lemort,
  *A modeling framework for the integration of electrical and thermal energy
  systems in greenhouses* (manuscript, University of Liège);
  documentation: <https://greenhouses-library.readthedocs.io>.

## Conversion log

- **2026-11-09 — import (T-TRANSLATE)**: climate core copied from
  `CSL-0334` (same conversion log); the lumped heating system replaced by
  the five-cell finite-volume pipe rail (eq. 28 of the paper, upwind
  advection, constant-property water as in the Modelica example).
- The `Ideal` heat-transfer model of `Flow1DimInc` is replaced by the
  hindered-convection correlation of `PipeFreeConvection_N` (the physically
  consistent choice for a pipe rail near the floor, and the one used by the
  paper's Table 1); radiation per cell follows `Radiation_N` (each cell one
  fifth of the area, full view factor).
- Water cell capacitance renamed `C_water` (case collision with the wind
  coefficient `C_w` of the climate core).
- Heating-circuit boundary conditions (T_su_pip, M_dot_pip) added to the
  lookup table — the open-loop surrogate of the three-way valve of the
  source paper (documented above).
- Integration step fixed at 60 s (moisture-state accuracy: at 120 s,
  `VP_air` drifts by about 1.2 % and `T_air` by 0.5 K against a 30 s step).
- **2026-11-10 — correction**: same missing floor term as `CSL-0333`
  (`- q_rad_flr_cov`). Re-solved (about 25 min, 8640 steps) and re-checked
  against RK4. The check is `greenhouse_heating_pipe_dynamic_ref.py`; the
  Solving time section records why that 30 s Python run takes 7 s and the
  60 s CoolSolve run takes 25 min.
- **Level**: equations 222 (1) + largest block 90 (2) + arrays, 15 states
  (1) + multi-zone/discretized (1) + dynamics (1) + default guesses (0)
  = 6 → level 3.

## Limitations and CoolSolve gaps

- Constant-property water and no pipe metal capacitance (as in the source);
  five cells only (the source discretization, `N` = 5).
- Open-loop heating schedule: no feedback from the climate on the supply
  temperature or flow rate (the point of the demonstration, see Results).
- Same climate limitations as `CSL-0334` (no screen, lighting, CO₂ balance,
  crop growth).
- No CoolSolve gaps (`missing_features` empty).

## Related models

- [`CSL-0334`](../greenhouse_climate_dynamic/): the same climate core with
  the lumped pipe and a feedback controller — the natural comparison.
- [`CSL-0333`](../greenhouse_steady_state/): the steady state of the common
  climate core.

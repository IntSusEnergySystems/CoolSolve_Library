# Steady-state energy and moisture balance of a Venlo greenhouse

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0333`

Steady-state climate model of a single-glass Venlo tomato greenhouse at its
night design point: given the outdoor conditions set directly in the file, it
computes the pipe-rail heating power needed to hold the air at its night
set-point, the temperatures of the canopy, cover, floor and heating pipes, the
air humidity, and every heat and vapour flux. It is the flat EES translation
of the correlations of the [Greenhouses Modelica library](https://github.com/QueraltAltes/Greenhouses-Library)
and of the climate model described by Altes-Buch *et al.* — the same physics
as the dynamic model [`CSL-0334`](../greenhouse_climate_dynamic/) with all
capacitances set to zero.

| | |
|---|---|
| **Category** | Buildings › Greenhouses |
| **Fluids** | humid air (correlations, no property calls) |
| **Size** | 147 equations (largest block: 36) |
| **Source** | [Greenhouses Modelica library](https://github.com/QueraltAltes/Greenhouses-Library) (example `Greenhouse_2`), BSD-3 |
| **Authors** | Queralt Altes-Buch (library); paper with S. Quoilin, V. Lemort |
| **License** | MIT (translation), credits to the original authors |
| **CoolSolve** | 0.4.0 — verified against an independent re-solve of the same equations |

## Niche

First greenhouse model in the library: a night design-point heat load with the
cover, canopy, floor, soil and pipe-rail correlations of the Greenhouses
library (moisture, transpiration, condensation, long-wave exchange). The
nearest existing model, [`CSL-0042`](../../building_rc_network_3r2c/), is a
dwelling 3R2C network and has none of that. [`CSL-0334`](../greenhouse_climate_dynamic/)
is the same physics with capacitances; [`CSL-0335`](../greenhouse_heating_pipe_dynamic/)
replaces the lumped pipe by a five-cell rail.

## Problem statement

*What heating power must the pipe-rail circuit of a 1.4 ha Venlo tomato
greenhouse deliver on a cold clear winter night (−10 °C, wind 3 m/s, sky
−25 °C) to keep the indoor air at its 18 °C night set-point, and what are the
resulting component temperatures and humidity?*

The boundary conditions are set directly in the `.eescode` file (section
*Boundary conditions*): change `T_out`, `u_wind`, `T_sky`, `I_glob`, `RH_out`
and the set-point `T_air` and re-solve. On this same cold night, `I_glob` = 100 W/m²
brings `Q_pip` down to 142 W/m² and `I_glob` = 200 W/m² to 77 W/m²; the sky
and the outdoor air still dominate, so the heating power does not fall to zero.

## Model

The greenhouse has no thermal screen (single air zone), the roof vents are
closed (leakage only) and the canopy is a fixed tomato crop (LAI = 1.06, the
initial value of the source example; no crop growth). All quantities are per
m² of floor. The model is the steady state of the dynamic climate model of
Altes-Buch *et al.*: every node balance below also exists with its
capacitance in [`CSL-0334`](../greenhouse_climate_dynamic/).

**Node balances** (paper, eqs. 2–6; steady state, capacitances dropped). The
five unknowns $T_{can}$, $T_{cov}$, $T_{flr}$, $T_{pip}$ and $VP_{air}$
follow from the canopy, cover, floor, pipe and moisture balances; the air
balance then gives the pipe heat release $Q_{pip}$:

$$0 = \dot q^{swr}_{air} + \dot q^{cnv}_{pip,air} + \dot q^{cnv}_{can,air}
- \dot q^{cnv}_{air,flr} - \dot q^{cnv}_{air,cov} - \dot h^{sens}_{air,out}$$

$$0 = \dot q^{swr}_{can} + \dot q^{rad}_{pip,can} - \dot q^{cnv}_{can,air}
- \dot q^{lat}_{can,air} - \dot q^{rad}_{can,cov} - \dot q^{rad}_{can,flr}$$

$$0 = \dot q^{swr}_{cov} + \dot q^{cnv}_{air,cov} + \dot q^{lat}_{air,cov}
+ \dot q^{rad}_{can,cov} + \dot q^{rad}_{flr,cov} + \dot q^{rad}_{pip,cov}
- \dot q^{cnv}_{cov,out} - \dot q^{rad}_{cov,sky}$$

$$0 = \dot q^{swr}_{flr} + \dot q^{rad}_{pip,flr} + \dot q^{rad}_{can,flr}
+ \dot q^{cnv}_{air,flr} - \dot q^{cnd}_{flr,soil}$$

$$\dot m^{v}_{can,air} - \dot m^{v}_{air,cov} - \dot m^{v}_{air,out} = 0
\qquad\text{(paper, eq. 10)}$$

The pipe rail has no capacitance: $Q_{pip} = \dot q^{cnv}_{pip,air} +
\dot q^{rad}_{pip,can} + \dot q^{rad}_{pip,flr} + \dot q^{rad}_{pip,cov}$
determines $T_{pip}$.

**Convection** (paper, Table 1; free convection from the Nu–Ra relation of
Balemans 1989, hindered pipe convection and wind-driven cover convection
fitted by Bot 1983):

$$U_{air,cov} = 1.7\,|T_{air}-T_{cov}|^{0.33}\cos\varphi^{-0.66}, \qquad
U_{can,air} = 2\,LAI\,U_{leaf,air}$$

$$U_{pip,air} = 1.99\,\pi\,d_{pip}\,l_{pip}\,|T_{pip}-T_{air}|^{0.32}, \qquad
\alpha_{cov,out} = \frac{2.8+1.2\,v_w}{\cos\varphi}\ (v_w < 4\ \mathrm{m/s})$$

The air–floor exchange uses $1.7\,|\Delta T|^{0.33}$ (floor warmer) or
$1.3\,|\Delta T|^{0.25}$ (air warmer); both this switch and the wind-speed
switch are written with the smooth switches of the current library
(logistic functions, slope 11), as in the source — no solver events, and the
deviation from the sharp switch is below 0.1 % outside a 0.5 K (0.5 m/s)
band. This file keeps the source guard `max(1e-9, |ΔT|)`. The dynamic models
replace it by a smooth floor (see [`CSL-0334`](../greenhouse_climate_dynamic/)).

**Ventilation** (paper, eqs. 15–16; Boulard & Baille 1993): with the vents
closed only the leakage remains,

$$\dot v_{leak} = \max(0.25, v_w)\,K_{leak}, \qquad K_{leak} = 1.5\cdot10^{-4}$$

$$\dot h^{sens}_{air,out} = \rho_{air} c_{p,air}\, \dot v_{leak} (T_{air}-T_{out}),
\qquad \dot m^{v}_{ij} = \frac{M_{H_2O}\,\dot v_{ij}}{R}\left(\frac{P^v_i}{T_i}-\frac{P^v_j}{T_j}\right)$$

**Long-wave radiation** (paper, eq. 17) between every pair of surfaces with
the view factors of de Zwart (1996): $FF_{can} = 1-e^{-0.94\,LAI}$,
$FF_{pip} = c\,\pi d_{pip} l_{pip}$ with $c = 0.49$ for the hindered pipe
rail, screening factors $(1-FF)$ of the surfaces in between:

$$\dot q^{rad}_{ij} = \varepsilon_i\,\varepsilon_j\,FF_i\,FF_j \prod_k (1-FF_k)\,\sigma\,(T_i^4 - T_j^4)$$

**Latent heat** (paper, eq. 18): $\dot q^{lat}_{ij} = \Delta h_{fg}\,
\dot m^v_{ij}$ with $\Delta h_{fg} = 2.45\cdot10^6$ J/kg (at 21 °C).

**Transpiration** (paper, eq. 24; Stanghellini 1987, simplified switch form
of the current library): the stomatal resistance multiplies five factors
(radiation, CO₂, vapour pressure deficit, temperature, day/night switch
$S_{rs} = [1+\exp(-(R_{can}-5))]^{-1}$), the boundary-layer resistance is
constant $r_b$ = 275 s/m:

$$\dot m^{v}_{can,air} = \frac{2\,\rho_{air}\,c_{p,air}\,LAI}{\Delta h_{fg}\,\gamma\,(r_b+r_s)}
\,(P^v_{can} - P^v_{air}), \qquad r_s = r_{min}\,r_I\,r_{CO_2}\,r_{VP}\,r_T$$

**Condensation** (paper, eq. 22; de Zwart 1996): proportional to the
convective exchange coefficient, only when the air is supersaturated at the
cover:

$$\dot m^{v}_{air,cov} = \max\left(0,\ \xi\,U_{air,cov}\,(P^v_{air} - P^v_{sat}(T_{cov}))\right), \qquad \xi = 6.4\cdot10^{-9}$$

**Short-wave radiation** (paper, eqs. 19–27): the global radiation is split
50 % PAR / 50 % NIR (UV neglected); 2 % is absorbed by the glass cover, the
PAR transmitted to the canopy and floor decays exponentially with the LAI
(extinction $K_{PAR}$ = 0.7) with one floor reflection, and the NIR
absorption of canopy and floor is lumped by a three-layer (cover–canopy–
floor) reflection model. The saturation vapour pressure uses the library fit
$P_{sat} = -274.36 + 877.52\,e^{0.0545\,T[°C]}$ Pa.

**Ground**: conduction through the floor (concrete, 0.02 m) and five soil
layers of doubling thickness (0.02–0.32 m, paper, eq. 8) to a deep-ground
boundary at 3 °C; at steady state the chain collapses into the series
resistance $R_{so,tot} = \sum_i 1/U_{so,i} = 0.735$ m²K/W.

### Inputs and outputs

| | |
|---|---|
| **Inputs** (in the file) | `T_out` = −10 °C, `RH_out` = 80 %, `u_wind` = 3 m/s, `I_glob` = 0, `T_sky` = −25 °C, `T_air` = 18 °C, `CO2_air` = 400 ppm, `u_ven` = 0; construction parameters of the 1.4 ha Venlo greenhouse of the source example |
| **Outputs** | `Q_pip`, `T_pip`, `T_can`, `T_cov`, `T_flr`, `VP_air`, `RH_air`, `K_glob`, all convective, radiative, latent and moisture fluxes |

## How to run

```bash
coolsolve ./greenhouse_steady_state.eescode
```

Solves from the default guesses in about ten Newton iterations (no
`.initials`, no `coolsolve.conf` needed). The independent check is

```bash
python3 greenhouse_steady_state_ref.py
```

(numpy and scipy). It re-solves the design point and, when the `.sol` is
present, prints the max relative difference.

## Results

| Quantity | Value | Unit |
|---|---|---|
| Pipe heating power `Q_pip` | 197.7 | W/m² |
| Pipe temperature `T_pip` | 67.3 | °C |
| Canopy temperature `T_can` | 16.3 | °C |
| Cover temperature `T_cov` | 0.70 | °C |
| Floor temperature `T_flr` | 14.6 | °C |
| Air vapour pressure `VP_air` | 682 | Pa |
| Relative humidity `RH_air` | 33.0 | % |
| Overall transfer coefficient `K_glob` = `Q_pip`/(T_air−T_out) | 7.06 | W/m²K |
| — losses: convection cover→out | 75.5 | W/m² |
| — losses: radiation cover→sky | 87.2 | W/m² |
| — losses: ventilation (leakage) | 15.2 | W/m² |
| — losses: conduction to the ground | 15.8 | W/m² |
| Transpiration `MV_can_air` | 2.93·10⁻⁶ | kg/m²s |
| Condensation at the cover `MV_air_cov` | 1.34·10⁻⁶ | kg/m²s |

The canopy sits 1.7 K below the air temperature (transpiration cooling), the
glass cover 10.7 K above the outdoor air; the losses split about evenly
between convection and radiation to the sky. `K_glob` = 7.1 W/m²K and
`Q_pip` = 198 W/m² are typical values for a single-glass greenhouse, which
is the order-of-magnitude check of the solution.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![...](figures/greenhouse_steady_state_....png)  + one-line caption -->

## Verification

No Dymola/OpenModelica result exists for this boundary condition (the source
example simulates a full year with controllers), so the model was verified
against an **independent re-solve of the same equations**:
`greenhouse_steady_state_ref.py` in this folder (scipy `root`, written from
the Greenhouses library sources: `Air`, `Cover`,
`Canopy`, `Floor`, `Solar_model`, `MV_CanopyTranspiration`,
`Convection_Condensation`, `Ventilation`/`NaturalVentilationRate_2`,
`PipeFreeConvection_N`, `Radiation_T4`/`_N`), parameter by parameter.
27 shared quantities agree (temperatures, humidity, heating power and the
convective, radiative, latent and moisture fluxes):

| | CoolSolve | scipy `root` |
|---|---|---|
| `T_pip` [°C] | 67.316278 | 67.316278 |
| `Q_pip` [W/m²] | 197.66322 | 197.66322 |
| `T_can`, `T_cov`, `T_flr`, `VP_air` | same digits | same digits |

Max relative difference over the 27 quantities: **1.1·10⁻¹¹** (on `MV_air_cov`). A control-volume
check that is not an equation of the model — heating plus solar, minus cover
convection, sky radiation, sensible ventilation, conduction to the ground and
the latent heat carried out by the ventilation — closes to 2·10⁻¹⁰ W/m².

## Solving time

Measured 2026-11-10, CoolSolve 0.4.0. The design point alone:

| | wall time |
|---|---|
| `greenhouse_steady_state_ref.py` (scipy `root`, 14 evaluations) | 0.001 s |
| `coolsolve` (7 Newton iterations, startup and the LaTeX report included) | 1.3 s |

On this algebraic model the gap is the process startup and the report, not
the Newton loop. The same solver, called once per Runge–Kutta stage, is what
makes the dynamic variants slow: CSL-0334 takes 8.0 min in CoolSolve against
20 s in Python, and CSL-0335 takes 25.1 min against 6.8 s.

CoolSolve integrates by pinning the time and the states, then calling the
full algebraic solver at every stage (four solves per RK4 step). The Python
scripts evaluate the derivatives directly; the climate script solves only
the pipe temperature, with one scalar `brentq`. Four changes would close
most of that gap, in this order:

1. A march residual that substitutes the explicit equations and runs Newton
   only on the blocks that stay implicit. The integrator needs the
   integrands, not a full solve report.
2. A cached map of the pinned variables and a reused automatic-differentiation
   tape. Today both are rebuilt at every stage, and the cost grows with the
   number of blocks times the number of variables. The pipe model has no
   implicit unknown once the states are pinned, and it is still the slower of
   the two.
3. A Jacobian kept along the trajectory, refreshed from one residual per
   smooth stage. The default rebuilds it at every Newton iteration, and
   nothing is kept from one stage to the next.
4. A BDF or DASSL step, which can take longer steps than the fixed RK4 the
   air and cover time constants currently force. That cuts the number of
   stages; it does not make one stage cheaper. Index reduction does not
   apply: once the pipe temperature is known these are explicit ODEs.
   Tearing that pipe balance down to one unknown, as the Python script does,
   is a small extra on CSL-0334.

## Source and attribution

- **Original model**: Greenhouses Modelica library —
  <https://github.com/QueraltAltes/Greenhouses-Library> (example
  `Greenhouse_2.mo`, components under `Greenhouses/Components/Greenhouse/`),
  BSD-3 license, commit `89ae0e8`.
- **Authors**: Queralt Altes-Buch (Energy Systems Research Unit, ULiège;
  library and climate model), with the climate model building on the
  greenhouse models of G.P.A. Bot (1983), L.F. de Zwart (1996) and
  C. Stanghellini (1987).
- **Scientific reference**: Q. Altes-Buch, S. Quoilin, V. Lemort,
  *A modeling framework for the integration of electrical and thermal energy
  systems in greenhouses* (manuscript, University of Liège); library
  documentation: <https://greenhouses-library.readthedocs.io>. Equations of
  this README are numbered as in that manuscript.

The flat translation (one equation per line, SI-°C-Pa-J) is published under
the library license (MIT) with full credit to the original authors.

## Conversion log

- **2026-11-09 — import (T-TRANSLATE)**: flat translation of the Greenhouses
  library climate model: every `Flows.*` element is written as one or two EES
  equations per m² of floor; the object graph (connectors, per-component
  areas) is dropped. Parameters from the example `Greenhouse_2` (1.4 ha
  Venlo: 625 pipe loops of 50 m, d = 0.051 m, φ = 25°, single glass,
  LAI₀ = 1.06).
- Per-m² formulation: all `A` factors cancel (`Q_flow/A`, `P/A`), pipe
  geometry kept as `l_pip` = 2.232 m/m².
- Air moisture state (eq. 10) becomes algebraic (steady state); `T_air` is
  an input (set-point), the heating power `Q_pip` is an output.
- Soil: the two-concrete + five-soil layer chain of the source is
  simplified to one concrete floor layer (0.02 m) + five soil layers of
  doubling thickness (0.02–0.32 m), same λ and ρc as the source; at steady
  state only the series resistance matters.
- cp of air harmonized to 1005 J/kgK everywhere (the source uses 1000 in
  the air capacitance and 1005 in the ventilation term; no effect at steady
  state).
- `c_cov` (specific heat) renamed `cp_cov`: EES is case-insensitive and the
  capacitance `C_cov` of the dynamic variant would collide.
- No CoolSolve gaps: the file is valid EES and solves as written.
- **2026-11-10 — correction**: the floor balance did not subtract
  `q_rad_flr_cov`, so the long-wave exchange with the cover (connected on
  both heat ports in `Radiation_T4`) was a source. `Q_pip` was 183 W/m² and
  is 198 W/m² after the fix. Re-solved and re-checked the same day. The
  check is `greenhouse_steady_state_ref.py`; the Solving time section
  records why the dynamic variants are much slower in CoolSolve.
- **Level**: equations 147 (1) + largest block 36 (2) + multi-zone, five
  coupled components (1) + no dynamics/calibration (0) + solves from default
  guesses (0) = 4 → level 3.

## Limitations and CoolSolve gaps

- No thermal screen (single air zone), no supplementary lighting, no CO₂
  balance (concentration prescribed), no crop growth (fixed LAI) — the
  boundaries of the translated sub-model; the full library has them.
- The correlations are the steady-state ones of the source (no thermal
  inertia), and the moisture balance assumes the fixed capacity temperature
  T = 291 K of the source (eq. 10).
- No CoolSolve gaps (`missing_features` empty).

## Related models

- [`CSL-0334`](../greenhouse_climate_dynamic/) (dynamic climate model): the
  same physics with all capacitances — this model is its steady state.
- [`CSL-0335`](../greenhouse_heating_pipe_dynamic/) (discretized heating
  pipe): the same climate core with a finite-volume pipe rail.
- [`CSL-0042`](../../building_rc_network_3r2c/) (3R2C building network): the
  building-counterpart of the lumped climate approach.

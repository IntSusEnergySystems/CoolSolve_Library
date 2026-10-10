# Cooling coil with control, simplified model

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0073`

Simplified model of a cooling and dehumidifying coil of an air handling unit,
from the ULiège model bank (Laborelec toolkit lineage): the refrigerant side
is not modelled at all and the coil is represented by a **contact
temperature**, the fraction of the approach between the supply air and the
minimum contact temperature being fixed by a contact-factor effectiveness
`epsilon_c_coolingcoil`. The contact temperature is driven by a proportional
control law on the deviation of the exhaust air temperature from its set
point, bounded between 0 and 1, so the model computes the exhaust air state
(temperature and humidity ratio) and the total, sensible and latent cooling
powers of the coil for any operating point, without any refrigerant-side
data.

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (humid air) |
| **Size** | 34 equations, 30 blocks (largest block: 5): 10 for the inputs and parameters of the control panel, 24 for the model |
| **Source** | ULiège model bank — *Cooling coil with control: simplified model*, 18 March 2008 (EES file inside `COOLINGCOILWithControl_SIMPLIFIED_MODEL_VL080318.zip`) |
| **Authors** | Vincent Lemort, Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | **verified** against the EES stored solution (max. 2.7e-02 on the latent power, 14 of 34 variables above 1e-3, EES vs CoolProp humid air). The native file uses the EES 5-argument `IF` |

## Problem statement

Air at 28 °C and 11.83 g of water per kg of dry air flows at 1.757 kg/s
through the cooling coil of an air handling unit at 101 325 Pa; the water
entering the coil is at 6 °C. The coil has a contact-factor effectiveness
`epsilon_c = 0.9714`, an air-side effectiveness of 0.8148 in the dry regime
and 0.539 in the wet regime, and the exhaust air temperature is controlled
to a set point of 14.61 °C by a proportional control of gain 10 acting on
the contact temperature. Determine the contact temperature, the exhaust air
state, the total, sensible and latent cooling powers of the coil and its
sensible heat ratio.

## Model

- Minimum contact temperature (two regimes, as in the original):
  - dry: `t_c_mindry = t_a_su − (epsilon_a_dry/epsilon_c)·(t_a_su − t_w)`,
  - wet: `t_c_minwet = t_wb_su − (epsilon_a_wet/epsilon_c)·(t_wb_su − t_w)`;
  the supply wet-bulb temperature `t_wb_su` and dew-point temperature `t_dp_su`
  come from the humid-air property calls `wetbulb(airH2O,P=…,W=…,T=…)` and
  `dewpoint(airH2O,P=…,W=…,T=…)`; the regime is selected by a 5-argument EES
  `IF`: `IF(t_dp_su, t_c_minwet, t_c_mindry, t_c_mindry, t_c_minwet)` returns the
  dry value when the supply dew point is below the minimum wet contact temperature
  and the wet value when it is above.
- Contact temperature: `t_c = t_a_su − X_control·(t_a_su − t_c_min)` with the
  bounded control variable `X_control = max(min(C_control·(t_a_ex − t_a_ex_set),1),0)`.
- Outlet air temperature: `t_a_ex = t_a_su − epsilon_c·(t_a_su − t_c)`
  (contact-factor closure).
- Outlet air humidity ratio: `W_ex = min(W_su, W_su − epsilon_c·(W_su − W_c))`
  with `W_c = humrat(airH2O,P=…,T=t_c,R=1)`, the humidity ratio of air
  saturated at the contact temperature; `W_ex` is never above the supply
  value.
- Enthalpies `h_a_su`, `h_a_ex` from `enthalpy(airH2O,P=…,W=…,T=…)`;
  total cooling power `Q_dot = M_dot_a·(h_a_su − h_a_ex)`, sensible power
  `Q_dot_sens = M_dot_a·c_p_a_coil·(t_a_su − t_a_ex)` with
  `c_p_a_coil = specheat(airH2O,T=t_a_su,P=…,w=W_su)`, latent power
  `Q_dot_lat = Q_dot − Q_dot_sens` and sensible heat ratio
  `SHR = Q_dot_sens/(Q_dot + 1e-5)`.
- `h_a_ex_coolingcoil_sensible = c_p_a·t_a_ex + W_su·(c_p_g·t_a_ex + h_fg0)`
  is an output of the original (the dry-air-plus-vapour enthalpy written with
  the constant `c_p_a = 1020 J/(kg-K)`); no equation of the model uses it.

| Inputs (default run) | Value | Parameters | Value |
|---|---|---|---|
| `t_a_su_coolingcoil` supply air temperature | 28 °C | `epsilon_c_coolingcoil` contact factor | 0.9714 |
| `W_su_coolingcoil` supply humidity ratio | 0.01183 kg/kg | `epsilon_a_coolingcoil_dry` | 0.8148 |
| `M_dot_a_coolingcoil` air flow | 1.757 kg/s | `epsilon_a_coolingcoil_wet` | 0.539 |
| `t_w_su_coolingcoil` water inlet temperature | 6 °C | `C_coolingcoil_control` control gain | 10 |
| `t_a_ex_coolingcoil_set` exhaust air set point | 14.61 °C | `c_p_a` / `c_p_g` / `h_fg0` | 1020 / 1840 J/(kg·K), 2.501 MJ/kg |
| `P_atm` atmospheric pressure | 101 325 Pa | | |

In the original these values are entered in the control panel (Diagram
window): the equations window only lists them as comment lines, and the two
air-side effectiveness values were inside a `{}` comment. The library model
gives them their stored (default-run) values as equations — the stored run is
the regression case.

## How to run

The native file keeps the native EES syntax (the 5-argument `IF`). Open
`cooling_coil_with_control_simplified.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./cooling_coil_with_control_simplified.eescode
```

No `.initials` file is needed (the system converges from the default guesses
in 2 iterations). To study another operating point, change the supply state,
the set point or the parameters of the control panel; a sweep of
`t_a_su_coolingcoil` or of `t_a_ex_coolingcoil_set` gives the coil capacity
and the sensible heat ratio of the coil (see the figure placeholder below).

## Results (default run)

| Quantity | CoolSolve | EES (stored) | rel. diff |
|---|---:|---:|---:|
| `t_c_coolingcoil` contact temperature [°C] | 14.3060 | 14.3061 | 8e-06 |
| `t_c_coolingcoil_min` minimum contact temperature [°C] | 12.3711 | 12.3916 | 1.7e-03 |
| `t_wb_su_coolingcoil` supply wet-bulb [°C] | 20.3128 | 20.3589 | 2.3e-03 |
| `t_dp_su_coolingcoil` supply dew point [°C] | 16.5491 | 16.6133 | 3.9e-03 |
| `X_coolingcoil_control` control variable [-] | 0.87620 | 0.87734 | 1.3e-03 |
| `t_a_ex_coolingcoil` exhaust air temperature [°C] | 14.6976 | 14.6977 | 7e-06 |
| `W_ex_coolingcoil` exhaust humidity ratio [kg/kg] | 0.0102634 | 0.0102219 | 4.0e-03 |
| `Q_dot_coolingcoil` total cooling power [W] | 30 991.7 | 31 185.9 | 6.2e-03 |
| `Q_dot_sensible_coolingcoil` sensible power [W] | 24 043.6 | 24 044.4 | 3e-05 |
| `Q_dot_latent_coolingcoil` latent power [W] | 6948.1 | 7141.4 | 2.7e-02 |
| `SHR_coolingcoil` sensible heat ratio [-] | 0.77581 | 0.77100 | 6.2e-03 |

The control law holds the exhaust air temperature 0.09 K above its set point
(`X = 10·(14.6976 − 14.61) = 0.876`, inside the [0, 1] bounds). The contact
temperature is 14.31 °C, i.e. 13.7 K below the supply air, and the coil
delivers 31.0 kW of cooling (17.6 kJ per kg of dry air), of which 24.0 kW is
sensible and 6.9 kW latent (SHR 0.776).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. Q_dot_coolingcoil and SHR_coolingcoil vs t_a_ex_coolingcoil_set or vs t_a_su_coolingcoil
     (no psychrometric chart in CoolSolve, CS-FEAT-PSYCHRO: decision D7, sweep plot),
     figures/cooling_coil_with_control_simplified_sweep.png -->

## Verification

The **native file** (with the 5-argument `IF`, solved by CoolSolve in 2
iterations) is the verified file, checked on the regression point and on a
dry-regime point (supply humidity
ratio 0.004: dew point 0.74 °C below the minimum wet contact temperature 9.45 °C,
dry value selected). Compared with
`compare_solution.py` against the 34 variables stored in the source EES
file: **34 common variables, 14 differ above rtol = 0.001, maximum relative
difference 2.71e-02** (`Q_dot_latent_coolingcoil`, 6948.13 W against
7141.41 W).

The deviations have a single cause: the EES and the CoolProp humid-air
formulations (different treatment of the water vapour enhancement factor)
give slightly different dew-point, wet-bulb, humidity-ratio and enthalpy
values (the same 0.2–0.5 % spread as the other humid-air models of the
library, e.g. `CSL-0070` 4.4e-03 and `CSL-0016` 5.1e-03).

- Property calls: `t_dp_su` 3.9e-03, `t_wb_su` 2.3e-03, `W_c` 4.2e-03,
  `W_ex` 4.0e-03, `h_a_ex` 2.0e-03 (the supply enthalpy `h_a_su` and
  `c_p_a_coil` agree within 4.8e-04 and 4e-05).
- Purely algebraic results: `t_a_ex` 7e-06, `t_c` 8e-06, `Q_dot_sensible`
  3e-05, `t_c_mindry` and `h_a_ex_coolingcoil_sensible` exact (below 1e-06) —
  the contact factor and the control law are reproduced exactly.
- Amplified differences: `X_control` 1.3e-03 (it multiplies the small
  difference of `t_a_ex` and the set point), `Q_dot_coolingcoil` 6.2e-03 and
  `SHR` 6.2e-03 (they integrate the enthalpy difference), and the largest
  deviation 2.71e-02 on `Q_dot_latent_coolingcoil`, which is the **difference
  of two large numbers** (30 991.7 − 24 043.6 W): a 0.6 % error on the total
  power becomes 2.7 % on the 7 kW latent residual.

No variable is excluded from the comparison (all 34 variables of the file are
compared).

The stored EES solution was cross-checked against the equations before use:
`t_c_mindry = 28 − (0.8148/0.9714)·22 = 9.5466 °C`,
`t_c_minwet = 20.3589 − (0.539/0.9714)·(20.3589 − 6) = 12.3916 °C` and
`X = 10·(14.69773 − 14.61) = 0.87734` re-derive the stored values, so the
panel is self-consistent (one operating point, not a stale mix).

## Source and attribution

ULiège model bank (Laborelec toolkit lineage), *cooling coil with control:
simplified model*, dated 16 January 2008 (file name suffix `VL080318`), by
**Vincent Lemort** and **Jean Lebrun** (University of Liège, Faculty of
Applied Sciences, Thermodynamics Laboratory; the EES licence tag
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}`
confirms the laboratory). Published in
Lemort, V., C. Cuevas, J. Lebrun, I.V. Teodorese, *Development of simple
cooling coil models for simulation of HVAC systems*, ASHRAE Transactions
114(1), 2008 (reference [1] of the file). The zip carries the laboratory
disclaimer (freely distributed, may not be sold or distributed for
commercial purposes, cite the origin).

Source file (EES 7.888), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Cooling_Coil/COOLINGCOILWithControl_SIMPLIFIED_MODEL_VL080318.zip!/CoolingCoilWithControl_Simplified_EES_Model_VL080318.EES`
(inventory candidate `TM-0472`). The zip also contains a compiled `.EXE`
version of the model, not imported. Sibling files of the same component are
in the collection and are **kept as separate models of different level of
detail** (workflow §2): the reference-simulation model (RefSim, dry and wet
regimes, one zone, inventory `TM-0471`, card C-79) and the
parameter-identification model (ParamID, `TM-0470`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): unit system already
  `SI MASS DEG PA C J`, so no unit conversion; no lookup or parametric table;
  licence tag removed; the header was replaced by the standard one, the
  comments of the original were kept and their typos corrected
  (`regim` → *regime*, `Temp` → *temperature*), and every equation and
  value is unchanged. `AIRH2O`/`airH2O` and the mixed-case variable names of
  the original were made consistent (EES and CoolSolve names are
  case-insensitive).
- **Control-panel variables restored as equations.** In the equations window
  of the original the six inputs, `C_coolingcoil_control` and
  `epsilon_c_coolingcoil` appear as *quoted comment lines* (they are entered
  in the Diagram window: `"! in diagram"`), and the two air-side
  effectiveness values are inside a `{}` comment. The extraction is therefore
  not square (34 unknowns, 24 equations). Each of the ten variables is given
  its **stored** value as an equation — the stored solution is the file's
  default operating point and is kept as the regression case (workflow §3,
  step 4 / [ees_import.md §8](../CoolSolve/docs/ees_import.md)). With them
  the model is square (34 equations, 34 unknowns) and solves.
- **Units in comments.** Temperatures, powers, humidity ratios and
  heat capacities carry their SI unit; the air-side effectiveness values are
  dimensionless `[-]`.
- **No figure-ready state arrays.** This is a humid-air (`AirH2O`) component
  model, for which CoolSolve has no psychrometric diagram
  (`CS-FEAT-PSYCHRO`, decision D7): its figure is a parametric sweep plot,
  as for `CSL-0070`.
- **Level.** Score (taxonomy.md §3): equations 34 (< 50 → 0), largest block 5
  (≤ 5 → 0), no functions/arrays (0), single component (0), identified
  effectiveness parameters and a control law (semi-empirical: 1), no curated
  guesses needed (0) → 1 → **level 1** (card value confirmed).

## Limitations

- Physical limitations: the refrigerant side is not modelled (the coil
  capacity is whatever the control law asks for); the outlet humidity ratio
  is that of the contact factor at the contact temperature, with no
  condensate-flow or bypass effect; the dry/wet regime switch uses the supply
  dew point only (frost formation is not modelled); the two air-side
  effectiveness values are correlated parameters of the original, not
  identified by this model.

## Related models

- `CSL-0017` *chilled_water_cooling_coil*: chilled-water cooling coil of the
  same air-handling family, dry and wet regimes, resolved in several zones
  (the reference-simulation level of detail of this component).
- `CSL-0016` *moist_air_cooling_coil_contact_factor*: the same
  contact-factor closure for a moist-air cooling coil, from the
  psychrometrics side.
- `CSL-0070` *adiabatic_humidifier_simplified*: the simplified model of
  another air-handling component of the same ULiège model bank and author
  group.
- `CSL-0074` *cooling_coil_refsim*: the reference-simulation model of the same
  coil of the same model bank, the other level of detail (dry and wet regimes
  computed simultaneously, secondary refrigerant side).
- `CSL-0163` *cooling_coil_paramid*: the parameter-identification sibling of
  the same model bank and authors (card C-155); one measured wet-regime point
  identifies the resistances that this simplified model drops.

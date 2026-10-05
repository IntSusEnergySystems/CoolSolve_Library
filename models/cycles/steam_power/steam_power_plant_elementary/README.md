# Elementary steam power plant (component balances)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0053`

A steam power plant analysed component by component — pump, economiser,
steam generator, turbine, condenser — with the imperfections of a real
machine: pressure drops between all components, a thermal loss between
generator outlet and turbine inlet, significant kinetic energies at the
turbine exhaust and in the main steam line. Given the seven state points, the
model computes the turbine power, the heat rates of the condenser,
economiser and steam generator, the required cooling-water flow rate and the
overall cycle efficiency.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water |
| **Size** | 88 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), exercise session R3, exercise 6 (EES file `R3_E6_2022.EES`) |
| **Authors** | TBD (see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

The data correspond to an elementary steam power plant (the 2017 version of
the exercise refers to textbook exercise 5.51, figure 5.30). The states 1–7
are given, with pressure drops between components and a thermal loss between
states 4 and 5. Determine:

- a) the power output of the turbine;
- b) the heat transfer rate in the condenser, the economiser and the steam
  generator;
- c) the cooling-water flow rate in the condenser, if the cooling-water
  temperature rises there from 15 to 25 °C.

| Inputs | Value | Inputs | Value |
|---|---|---|---|
| `p_1` pump outlet | 6200 kPa | `x_6` turbine-exhaust quality | 0.92 |
| `p_2` / `T_2` economiser inlet | 6100 kPa / 45 °C | `c_6` exhaust velocity | 200 m/s |
| `p_3` / `T_3` economiser outlet | 5900 kPa / 175 °C | `p_7` / `T_7` condenser outlet | 9 kPa / 40 °C |
| `p_4` / `T_4` generator outlet | 5700 kPa / 500 °C | `q_m_vap` steam flow | 25 kg/s |
| `p_5` / `T_5` turbine inlet | 5500 kPa / 490 °C | `W_dot_pump` pump power | 300 kW |
| `p_6` turbine outlet | 10 kPa | `d_45` / `d_7123` pipe diameters | 0.2 / 0.075 m |
| | | `DeltaT_rfd` water temperature rise | 10 K |

## Model

Each component is an open system at steady state with one inlet and one
outlet: `q_m_out = q_m_in = q_m` and the first law reads
$\dot Q + \dot W = \dot m\,(\Delta h + \Delta EC)$, the kinetic-energy term
being kept where the velocities are significant (turbine: exhaust velocity
200 m/s against 48.6 m/s at the inlet; condenser: the same exhaust velocity).
The turbine and the condenser are adiabatic / have no work transfer
respectively, potential energy is neglected everywhere (as in the original).
Velocities follow from the mass flow rate and the pipe cross-sections
(`d_45` for the 4–5 and 4 lines, `d_7123` for the 7, 1, 2, 3 lines). The
pump outlet enthalpy comes from its power, `h_1 = h_7 + W_dot_pump/q_m_vap`;
the overall balance leaves a residual `Pertes` of −175 kW, the image of the
pressure drops (1-2, 2-3, 3-4, 4-5, 6-7) and of the thermal loss (4-5); the
efficiency nets the pump power in the numerator.

The original sign convention is kept: powers and heat rates received by the
working fluid are positive, hence a negative turbine power (the machine
produces work) and a negative condenser duty.

## How to run

Open `steam_power_plant_elementary.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./steam_power_plant_elementary.eescode
```

The system is fully explicit (88 blocks of size 1): no guess values needed.

## Results

| Point | T [°C] | p [kPa] | h [kJ/kg] | | Quantity | Value |
|---|---:|---:|---:|---|---|---:|
| 1 — pump outlet | 41.6 | 6200 | 179.5 | | `W_dot_turb` turbine power | −24.85 MW |
| 2 — economiser inlet | 45 | 6100 | 193.8 | | `Q_dot_cond` condenser duty | −56.12 MW |
| 3 — economiser outlet | 175 | 5900 | 743.7 | | `Q_dot_econ` economiser duty | 13.75 MW |
| 4 — generator outlet | 500 | 5700 | 3426.6 | | `Q_dot_gen` generator duty | 67.10 MW |
| 5 — turbine inlet | 490 | 5500 | 3405.3 | | `q_m_rfd` cooling water | 1341 kg/s |
| 6 — turbine outlet (x = 0.92) | 45.8 | 10 | 2392.5 | | `eta_rankine` efficiency | 30.37 % |
| 7 — condenser outlet | 40 | 9 | 167.5 | | `Pertes` balance residual | −175.1 kW |

The energy inputs (0.3 + 13.75 + 67.10 = 81.15 MW) exceed the turbine output
(24.85 MW) plus the condenser duty (56.12 MW) by 0.175 MW: the residual
`Pertes`. Cooling water 1341 kg/s for a 10 K rise checks
`Q_dot_rfd = q_m_rfd · 4184 · 10`. The velocities at stations 2, 3 and 7 come
out below 10 m/s (5.7–6.3 m/s), so their kinetic terms could be neglected
without a large error, as the original notes.

The state arrays `p[i]`, `h[i]`, `T[i]`, `s[i]`, `v[i]` (i = 1…7) plot the
cycle in the CoolSolve *Diagram* tab (*Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle,
     figures/steam_power_plant_elementary_ts.png -->

## Verification

**Faithful import vs EES.** The converted model was compared with the
solution stored in the source EES file
(`compare_solution.py --ees-units`): all 74 common variables agree, 0 differ
at rtol = 0.001, largest relative deviation 7.87e-06 (on `rho_6`; enthalpies
within 6e-07). This confirms both the property agreement (EES 10.836 vs
CoolProp, water) and the unit conversion. Two variables stored in the EES
file, `P` and `q_m`, appear only as leftovers of an earlier edit: they hold
no equation and their stored value equals the default guess; they are not
part of the model. The 15 CoolSolve-only variables are the added `T[i]` /
`s[i]` diagram arrays.

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée*
(MECA0002), exercise session R3, 2022-2023 version. The EES file names no
author (the `{$ID$}` tag is the laboratory licence); the inventory metadata
points to S. Quoilin with the repetition assistants N. Paulus and B. Dechesne
(companion Python/Word files) — the maintainer will confirm the author
attribution (`TBD`).

Source file (EES 10.836, comments in French, kPa/kJ/kW with decimal comma),
collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R3/R3_E6_2022.EES`
(inventory candidate `TM-0416`, duplicate group `DG-0084`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  decimal comma converted automatically by the tool; the EES licence tag was
  removed. Unit system converted **by hand** from `SI MASS DEG KPA C KJ` to
  `SI MASS DEG PA C J` (ees_import.md §6): `p_1`…`p_7` and `p[1]`…`p[7]`
  ×1000 (e.g. 6200 kPa → 6200e3 Pa), `W_dot_pump` 300 kW → 300e3 W,
  `C_eau` 4.184 kJ/kg-K → 4184 J/kg-K, and the four kinetic-energy terms
  `c^2/2*0.001 [kJ/J]` rewritten `c^2/2` (J/kg) — the 0.001 kJ/J factor
  disappears with the conversion. All other equations are homogeneous and
  stay unchanged; all temperatures are already in °C and no relation uses an
  absolute temperature. Comments translated to English and joined onto single
  lines (the original wraps comments over several lines, gap
  `CS-GAP-MULTILINE-COMMENT` — comment-only edit). The unit annotation inside
  the `specheat` named argument (`T=20[°C]` → `T=20`) was rewritten by the
  conversion (gap `CS-GAP-UNIT-NAMEDARG`, non blocking). Two stale variables
  of the EES binary (`P`, `q_m`: no equations, stored value = default guess)
  were not carried over. No `.initials` needed (fully explicit model).
  Verified against the EES stored solution (see above).
- **2026-10-05 — diagram support**: block of 14 post-processing equations
  (state arrays `T[i]`, `s[i]`; the original already stored `p[i]`, `h[i]`,
  `v[i]`) added at the end of the model for the CoolSolve diagrams; the
  results of the model are unchanged.
- **2026-10-05 — merge of the duplicate group.** The 2017 version
  `THD10_R03_E1.EES` (TM-0365, textbook exercise 5.51 wording) has identical
  equations and input values; only the comment wording and an algebraically
  equivalent writing of the kinetic terms (`c^2/2000` vs `c^2/2*0.001`)
  differ → `duplicate` of this model.
- **Level score** (taxonomy.md §3): equations 88 → 1; largest block 1 → 0;
  arrays present → 1; ≥ 3 coupled components → 1; no semi-empirical physics
  → 0; no curated guesses → 0. Score 3 → level 2.

## Limitations and CoolSolve gaps

- None blocking. The liquid-water specific heat of the cooling circuit is a
  constant 4184 J/kg-K, compared in the model with the saturation value
  computed at 20 °C (`C_eau_EES`, as in the original).

## Related models

- `CSL-0004` *rankine_cycle_60mw*: steam plant of the same course with
  isentropic/boiler/alternator efficiencies instead of tabulated state
  points (idealised, no pressure drops).

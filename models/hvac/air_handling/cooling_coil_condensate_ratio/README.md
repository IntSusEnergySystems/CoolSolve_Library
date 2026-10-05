# Condensate ratio and dry-air flow at a cooling coil, and a counter-flow recuperator

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0062`

A revision exercise (January 2022 exam of the ULiège course *Thermodynamique
appliquée*) with two questions on one heat-pump cycle:

1. **Cooling coil EV1**: humid ambient air (28 °C, 80 % RH, 1 bar) is cooled
   to 13 °C, saturated; the condensate leaves the coil at the air temperature
   and the refrigeration power is 7 kW. Compute the ratio of the
   condensed-water flow to the dry-air flow entering the coil, and the
   dry-air mass flow rate — by two first-law methods (with and without the
   enthalpy contribution of the condensate).
2. **Recuperator REC** (R113): counter-flow heat exchanger of effectiveness
   60 % between state 5 (35 °C) and state 9 (62.8 °C), 0.1 kg/s on both
   sides, with 5 kPa of pressure drop on each side and no latent exchange.
   Compute the outlet temperature at 10.

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (humid air), Water/Steam, R113, Air_ha (dry air of the humid-air package) |
| **Size** | 54 equations, 54 variables, largest algebraic block 4 |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), R12 revision session 2022-2023, exercises from the January 2022 exam (EES file `R12 - Révisions.EES`) |
| **Authors** | TBD (ULiège course MECA0002 — see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement (paraphrase of the French original)

**Question 1.** The cooling coil EV1 condenses part of the water of a humid
air stream. Given the supply state (28 °C, relative humidity 80 %), the
exhaust state (13 °C, saturated), an ambient pressure of 1 bar, a condensate
leaving at the air temperature and a refrigeration power of 7 kW, find the
ratio of the condensed-water flow rate to the dry-air flow rate, and the
dry-air flow rate itself. The original solves it twice: *method 1* applies
the first law to the humid air with the EES humid-air enthalpies (per kg of
dry air), which neglects the enthalpy contribution of the condensate; *method
2* writes the first law with separate dry-air, water-vapour and condensate
terms (the water vapour being evaluated at its partial pressure). The course
relations for the enthalpies of dry air (cp·T) and of water vapour (2500.9 +
1.82·T, T in °C) are computed as cross-checks of the property calls (`*_bis`
variables).

**Question 2.** The recuperator is a counter-flow exchanger of effectiveness
60 %: 60 % of the power that would be exchanged by an ideal exchanger is
actually transferred, the maximum being set by the side that first reaches
the inlet temperature of the other fluid. With 5 kPa of pressure drop on
each side, no latent exchange, the inlet states 5 (35 °C) and 9 (62.8 °C)
and a mass flow of 0.1 kg/s, compute the outlet temperature at 10.

## Model

Question 1 couples the humidity ratios at both states (from the EES
humid-air package), the water balance
$\dot m_{w,su} = \dot m_{w,ex} + \dot m_{cond}$ and the two energy balances;
the partial pressures follow from $P_{eau} = R\,p_{sat}(T)$ and
$P = P_{air} + P_{eau}$. Question 2 computes the maximum exchange on each
side through enthalpies ($\Delta h_{max}$ to the inlet temperature of the
other fluid, evaluated at the outlet pressure, which covers the pressure
drops), takes the minimum, applies the effectiveness and recovers `T6` and
`T10` from the R113 enthalpies.

| Inputs | Value | Outputs (CoolSolve) | Value |
|---|---|---|---|
| `T_a_su` / `T_a_ex` | 28 / 13 °C | `ratio` condensate/dry-air | 1.00 % (EES 0.996 %) |
| `R_su` / `R_ex` | 0.8 / 1 | `m_dot_a` dry-air flow (method 1) | 0.1713 kg/s (EES 0.1719) |
| `P` | 1 bar | `m_dot_a_bis2` dry-air flow (method 2) | 0.1736 kg/s (EES 0.1740) |
| `Q_dot` | −7 kW | `m_dot_cond` condensate | 1.735 g/s (EES 1.733) |
| `eta_HEX` / `dp` | 0.6 / 5 kPa | `Q_max` / `Q_f` | 1893 / 1136 W (EES same) |
| `T5`, `p5` | 35 °C, 3750 bar | `T6` | 47.57 °C (EES 47.58) |
| `T9`, `p9`, `m_dot` | 62.8 °C, 0.7 bar, 0.1 kg/s | `T10` (question 2) | 46.18 °C (EES 46.18) |

The two methods give dry-air flows differing by ≈ 1.3 % (1.2 % in EES): the
condensate enthalpy term is small but not zero, as the original notes ("on
remarque que m_dot_cond est si petit que l'on peut effectivement le négliger
dans les bilans enthalpiques").

## How to run

```bash
coolsolve ./cooling_coil_condensate_ratio.eescode
```

## Results

Question 1: the condensate ratio is ≈ 1 % of the dry-air flow (ω falls from
0.0195 to 0.0095 kg/kg) and the dry-air flow is ≈ 0.17 kg/s. Question 2: the
R113 leaves the recuperator at `T10` = 46.18 °C (state 9 is cooled by 16.6 °C,
state 5 heated by 12.6 °C — side 9-10 is the limiting one).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): humid-air model, so a
     parametric sweep plot, e.g. ratio and m_dot_a vs the coil exhaust temperature
     T_a_ex (7 -> 13 °C), figures/cooling_coil_condensate_ratio_sweep.png -->

## Verification

Solved in CoolSolve 0.3.0 and compared with the solution stored in the
original EES file (54/54 variables, hand-converted kPa/kJ → Pa/J,
`compare_solution.py --ees-units`):

- `54 common variables, 12 differ (rtol=0.001)`. All 12 are question-1
  humid-air quantities; all 21 recuperator variables (R113 enthalpies,
  `Q_max`, `Q_f`, `T6` = 47.575 °C, `T10` = 46.178 °C) agree within the
  printed tolerance, `T10` to 2e-7.
- The largest deviation, `3.06e-01` on `h_a_sec_ex`, is the **reference-state
  offset** of the dry-air enthalpy `Air_ha` (CoolProp reference ≈ EES +126 kJ/kg);
  the *difference* `h_a_sec_ex − h_a_sec_su` = −15 095 J/kg is identical in
  both tools, so the derived results are unaffected — as the original's own
  comment anticipates.
- The remaining deviations are the EES-vs-CoolProp humid-air properties, as
  in `CSL-0016`: humidity ratios +4.6e-03 (`omega_su`) and +5.2e-03
  (`omega_ex`), humid-air enthalpies +3.2e-03, hence `ratio` 3.9e-03,
  `m_dot_a` 3.3e-03, `m_dot_a_bis2` 2.5e-03, `m_dot_cond` 1.5e-03 — the
  question's answers agree within 0.4 %.

`.sol` baseline committed; `tools/test_models.py CSL-0062` passes.

## Source and attribution

Solution file of the R12 revision session (December 2022) of the ULiège
course *Thermodynamique appliquée* (MECA0002); the exercises are those of the
January 2022 exam. The EES file carries no author name (student/staff licence
of the Laboratoire de Thermodynamique); the inventory metadata suggests
S. Quoilin with the repetition assistants — to be confirmed by the
maintainer.

Source file (EES 10.836, comments in French; statement in the accompanying
Word file `R12 - Révisions.docx`), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R12/R12 - Révisions.EES`
(inventory candidate `TM-0396`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES 10.836, unit system `SI MASS DEG KPA C KJ`, decimal comma converted by
  the tool; licence/display tags removed. The multi-line `"…"` comment blocks
  of the original (water balance, humidity-ratio formulas) are comments, not
  equations — kept as comments.
- **2026-10-05 — hand unit conversion** (kPa/kJ → Pa/J,
  docs/ees_import.md §6): `P = 1e2 [kPa]` → `1E5` Pa; `Q_dot = -7 [kW]` →
  `-7000` W; `P=100 [kPa]` in the two `AirH2O` enthalpy calls → `1E5`;
  `cp_air = 1.005 [kJ/kg-C]` → `1005` J/kg-K; course vapour relation
  `2500.9 [kJ/kg] + 1.82 [kJ/(C-kg)]*T` → `2500.9E3 + 1.82E3*T`; `dp =
  0.05e2` → `5000` Pa; `p6 = 3.75e5 [kPa]` → `3.75E8` Pa; `p9 = 0.7e2 [kPa]`
  → `0.7E5` Pa; `.initials` converted accordingly. Unit annotations
  (`[kPa]`, `[%]`, `[kJ/kg]`…) replaced by comments.
- **2026-10-05 — `p6 = 375 MPa` kept as in the original.** The original
  types `p6 = 3.75e5` in a kPa unit system, i.e. 375 MPa — far above the
  critical pressure of R113 (3.39 MPa) and certainly a unit slip (3.75 bar
  was probably intended). It is kept unchanged: the EES stored solution was
  computed with it and CoolSolve/CoolProp reproduces every recuperator value
  within 2.3e-4 relative (compressed-liquid extrapolation of both backends).
  Consequences for the physics: at such a pressure the liquid enthalpy
  barely depends on p, so `T6` ≈ the temperature at which the liquid
  enthalpy equals `h6`, and the exercise conclusion is unaffected.
- **2026-10-05 — comments** translated to English (paraphrase of the French
  comments; the pedagogical discussion of the recuperator effectiveness is
  summarised, "as in the original"); standard header added; no change to the
  equations.
- **2026-10-05 — level**: score 1 per taxonomy.md §3 (54 equations, largest
  block 4, no procedures/arrays) → level 1, moved +1 to **level 2** per the
  card: two coupled questions on one cycle using three fluid descriptions
  (humid air, water/steam at partial pressures, R113) and two first-law
  formulations.

## Limitations and CoolSolve gaps

- No blocking gap. The two unit-annotation lines of the original
  (`enthalpy(...,P=100 [kPa],...)`, `2500.9 [kJ/kg] + 1.82 [kJ/(C-kg)]*T`;
  gaps `CS-GAP-UNIT-NAMEDARG` and `CS-GAP-UNIT-SUBEXPR`, not blocking) were
  rewritten by the hand unit conversion, as the register recommends.
- The `.sol` run prints two known noisy hints (`steam` → Water alias; the
  "looks like Fahrenheit" hint on T = 35 °C, `CS-BUG-HINT-FAHRENHEIT`);
  both are harmless.
- Absolute enthalpies of `Air_ha` carry a reference-state offset against EES
  (see *Verification*); the model only uses their difference.

## Related models

- `CSL-0016` *moist_air_cooling_coil_contact_factor*: cooling and
  dehumidifying coil per kg of dry air, with the same EES-vs-CoolProp
  humid-air offsets (+0.5 % on the humidity ratios).
- `CSL-0017` *chilled_water_cooling_coil*: chilled-water cooling coil with
  dry and wet regimes, condensate flow computed.
- `CSL-0028` *air_handling_unit_moist_air*: air handling unit on `AirH2O`
  with cooling coil, post-heating and condensate.
- `CSL-0055` *moist_air_room_psychrometrics*: psychrometric quantities of a
  room atmosphere computed both with the course relations and with the EES
  property functions (same `*_bis` cross-check pattern as here).

- `CSL-0064` *psychrometric_mixer_condensation*: adiabatic mixing of
  room and outdoor air with condensation in the mixer; the condensate
  enthalpy term of the same kind appears here in the energy balance.
- `CSL-0066` *adiabatic_saturation_wet_bulb*: humid-air property calls
  cross-checked with the course relations (same pattern as here).

# Adiabatic saturation and wet-bulb temperature of moist air

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0066`

Moist air characterised by a psychrometer: the dry-bulb and wet-bulb
temperatures are the measured quantities, and the model recovers the
humidity ratio, the relative humidity and the specific enthalpy of the air
per kg of dry air. The humidity ratio comes from the adiabatic-saturation
formula — the mass and energy balances of the wet-bulb thermometer, derived
in the course from a water balance, a dry-air balance and an energy balance —
and every result is computed a second time with the EES property functions
(`HumRat`, `RelHum`, `enthalpy`), so the exercise doubles as a comparison of
the course relations with a property package.

| | |
|---|---|
| **Category** | Heating, ventilation and air conditioning › Psychrometrics |
| **Fluids** | AirH2O, Water, Air_ha |
| **Size** | 27 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), exercise session R9, exercise 5 (EES file `R09_E05_2022.EES`) |
| **Authors** | TBD (see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

The dry-bulb and wet-bulb temperatures of air at 1 atm are measured at 25 °C
and 15 °C respectively with a psychrometer. Determine the specific humidity
(humidity ratio), the relative humidity and the enthalpy of the air.

## Model

A wet-bulb thermometer is a wet wick in a steady air stream: the air that
leaves it is saturated at the wet-bulb temperature `T_wb`, and the heat it
gives up to the evaporating water cools the air from `T_db` to `T_wb`. The
course formula follows from the balances on that air stream (water balance,
dry-air balance, energy balance), with the vapour enthalpy approximated by
that of the saturated vapour at the same temperature:

$$\omega_{db} \;=\; \frac{c_{p,air}\,(T_{wb}-T_{db}) + \omega_{wb}\,h_{fg,wb}}{h_{g,db} - h_{f,wb}}$$

The humidity ratio at the wet-bulb state is the saturated one,
`P_v_wb = p_sat(Water,T_wb)`,
$$\omega_{wb} = 0.622\,\frac{P_{v,wb}}{P_{amb}-P_{v,wb}}$$
and the specific enthalpy of the air is, by definition and with the course
constants (`c_p` = 1.005 kJ/kg·K, `h_g` = 2500.9 + 1.82·T kJ/kg, dry-air
enthalpy referred to 0 °C),
$$h_{db} = c_{p,air}\,T_{db} + \omega_{db}\,h_{g,db}$$

The relative humidity follows from the humidity ratio,
$$\phi_{db} = \frac{\omega_{db}\,P_{amb}}{(0.622+\omega_{db})\,p_{sat}(T_{db})}$$

Five further variables of the original are checks of this chain, and they
are kept: the dry-air enthalpy drop computed with the property function
instead of the constant `c_p` (`DELTAh_air2`), the vapour enthalpies without
the saturated-vapour approximation (`h_g_db_bis`, `h_g_wb_bis`), the vapour
enthalpy evaluated at its own partial pressure instead of at the saturation
pressure (`h_g_db_bis2`), the specific enthalpy with every term referred to
its own 0 °C reference (`h_db_bis2`) and the three EES property functions
(`omega_db_bis`, `RH_db_bis`, `h_db_bis`).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_db` dry-bulb temperature | 25 °C | `omega_db` specific humidity | 6.5255 g/kg dry air |
| `T_wb` wet-bulb temperature | 15 °C | `omega_db_bis` (EES `HumRat`) | 6.5601 g/kg dry air |
| `P_amb` ambient pressure | 101 325 Pa | `RH_db` relative humidity | 33.19 % |
| | | `RH_db_bis` (EES `RelHum`) | 33.22 % |
| | | `h_db` specific enthalpy | 41.742 kJ/kg dry air |
| | | `h_db_bis` (EES `enthalpy`) | 41.855 kJ/kg dry air |

## How to run

Open `adiabatic_saturation_wet_bulb.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./adiabatic_saturation_wet_bulb.eescode
```

The system is fully explicit (27 blocks of size 1, *System square: Yes*): it
converges with no guess values and no `.initials` file is shipped.

## Results

| Quantity | Course relations | EES property functions |
|---|---:|---:|
| `P_v_wb` saturation pressure at 15 °C | 1.70579 kPa | — |
| `P_sat_db` saturation pressure at 25 °C | 3.16993 kPa | — |
| `omega_wb` humidity ratio at the wet-bulb state | 0.0106506 | — |
| `omega_db` / `omega_db_bis` specific humidity | 0.00652554 | 0.00656012 kg/kg dry air |
| `RH_db` / `RH_db_bis` relative humidity | 0.331864 | 0.332230 |
| `h_db` / `h_db_bis` enthalpy of the moist air | 41.7416 | 41.8547 kJ/kg dry air |
| `h_db_bis2` enthalpy, every term at its 0 °C reference | 41.7665 | — |
| `DELTAh_air1` / `DELTAh_air2` dry-air enthalpy drop | −10.050 | −10.0615 kJ/kg |
| `h_f_wb` / `h_fg_wb` water and latent heat at 15 °C | 63.0768 / 2465.12 | — |
| `h_g_db` / `h_g_db_bis` vapour enthalpy at 25 °C | 2546.40 | 2546.51 kJ/kg |
| `P_v_db` vapour partial pressure in the air | 1.05314 kPa | — |

Sanity checks. The two routes to the humidity ratio differ by 0.53 %
(`omega_db` 0.00652554 against the `HumRat` function 0.00656012), the two
routes to the enthalpy by 0.27 % (41.7416 against 41.8547 kJ/kg) and the two
routes to the relative humidity by 0.11 % (0.331864 against 0.332230); see
*Verification* for the origin of these differences. The constant-`c_p`
approximation is worth 0.11 % on the dry-air enthalpy drop
(−10.050 against −10.0615 kJ/kg), and the saturated-vapour approximation
0.004 % on the vapour enthalpy (2546.40 against 2546.51 kJ/kg), i.e. both
approximations of the course are accurate here. `h_db` is reproduced by its
definition to 6·10⁻⁴ relative by the reference-shifted route `h_db_bis2`
(41.7665 kJ/kg). The air is dry: at 25 °C a wet-bulb temperature of 15 °C
corresponds to about a third of the saturation humidity.

The EES saturation pressure of water at 15 °C stored in the file,
1.705677 kPa, agrees with CoolProp to 6.8·10⁻⁵.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): CoolSolve has no
     psychrometric chart yet (CS-FEAT-PSYCHRO), so the figure of this humid-air model is
     a parametric sweep (roadmap decision D7), e.g. the specific humidity `omega_db` and
     the relative humidity `RH_db` as a function of the dry-bulb temperature `T_db` for a
     fixed wet-bulb depression of 10 K (CoolSolve GUI, Parametric tab, 1D plot), saved as
     figures/adiabatic_saturation_wet_bulb_t_db.png -->

## Verification

**Faithful import vs EES.** The hand-converted model was compared with the
solution stored in the source EES file (`compare_solution.py --ees-units`):
**26 common variables, 2 differ (rtol=0.001), largest relative deviation
5.24e-03** (on `omega_db_bis`).

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `omega_db_bis` | 0.00652574 | 0.00656012 | 5.24e-03 |
| `h_db_bis` | 41725.9 | 41854.7 | 3.08e-03 |

Everything else agrees at least as well as `P_v_db` (8.47e-04),
`RH_db_bis` (8.14e-04), `omega_db` (1.12e-04), `P_v_wb` (6.80e-05),
`DELTAh_air2`/`h_a_db_bis` (4.91e-06), `h_g_db_bis` (9.97e-07) and `h_f_wb`
(3.39e-09).

The two deviations are both outputs of the EES property functions on humid
air, i.e. differences between the moist-air formulation of EES and that of
CoolProp, not errors of the conversion:

- `omega_db_bis` (5.24e-03, +0.53 %): the EES function `HumRat` with the
  wet-bulb temperature as input. CoolProp's moist air includes the
  water-enhancement factor, so `omega_db_bis` is 0.53 % above the course
  formula `omega_db`, which itself agrees with the stored EES answer to
  1.12e-04. `CSL-0055` measured the same effect at +0.42 % on another state.
- `h_db_bis` (3.08e-03, +0.31 %): the absolute enthalpy of moist air depends
  on the reference state and slightly on the formulation; the course
  definition `h_db` = 41.7416 kJ/kg agrees with both (EES 41.7398, CoolProp
  41.8547 kJ/kg), and `CSL-0055` measured the same +0.3 % offset.

**Second check — the property calls themselves.** The three humid-air calls
were recomputed with the CoolProp Python library (v8.0.0, same backend,
inputs `(T, B, P)`), and reproduce the model to the last digit:
`HAPropsSI('W','T',298.15,'B',288.15,'P',101325)` = 0.006560122464113 =
`omega_db_bis`, `HAPropsSI('H',…)` = 41854.698 J/kg = `h_db_bis`,
`HAPropsSI('R',…)` = 0.332229743 = `RH_db_bis`.

**Third check — an independent psychrometric formula.** The ASHRAE
relation between the humidity ratio and the wet-bulb temperature,
ω = [(2501 − 2.326·T_wb)·ω_ws − 1.006·(T_db − T_wb)] /
[2501 + 1.86·T_db − 4.186·T_wb] with ω_ws = 0.62198·p_sat(T_wb)/(P_amb −
p_sat(T_wb)), gives 0.00652176 kg/kg against the 0.00652554 of the model, an
agreement of 5.8·10⁻⁴ with a formula the model does not use.

**Variables left out of the comparison.** The EES file stores 44 variables
that are not part of this model: the arrays `h[1…7]`, `p[1…7]`, `T[1…7]`,
`s[1…7]`, `v[1…7]`, `x[1]`, `x[3…7]` and the scalars `P` and `cp`. They
carry no equation in the Equations window and are leftovers of an earlier
exercise saved in the same file (the sibling exercises of the same folder,
`R09_E01_2022.EES` …, carry the very same arrays — the file was also listed
for `CSL-0055`). They were not carried over. The stored value of the unused
`h_g_wb_bis2` (1, a default) and the contradiction between the stored
`x[3]` = 0 and the value written in `.initials` (`x[3]` = 1) are further
signs that the variable records of the binary are stale for those names; the
25 variables that do belong to the model are consistent with its equations
and were used as the reference. Only `fluid$` is present in the CoolSolve
`.sol` alone (it appears twice, as a number and as a string:
`CS-BUG-SOL-STRING`).

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée*
(MECA0002), exercise session R9, 2022-2023 edition (repetition 10 of the
course). The EES file names no author (the `{$ID$}` tag is the laboratory
licence of the *Laboratoire de Thermodynamique*, University of Liège); the
inventory metadata attributes the session to S. Quoilin with the repetition
assistants N. Paulus and B. Dechesne (companion Python and Word files) — the
maintainer will confirm the author attribution (`TBD`).

Source file (EES 10.836, comments in French, kPa/kJ with decimal comma),
collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/R09_E05_2022.EES`
(inventory candidate `TM-0455`, no duplicate group: the copy of the same file
inside `R9.zip` of the same folder is byte-identical and carries no
inventory row of its own).

The statement of the exercise (in French) is also given in
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/ex5 - demo.docx`
together with the derivation of the adiabatic-saturation formula. The course
ships Python/CoolProp solutions of exercises 1 to 3 of this session
(`ThAp20_R09E01.py`, `ThAp20_R09E02.py`, `ThAp20_R09E03.py`, used for
`CSL-0055` and `CSL-0063`), but none for exercise 5; the two checks of
*Verification* above were therefore computed for this model rather than
taken from the collection.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  decimal comma converted automatically by the tool, EES licence and display
  tags removed, `$UnitSystem` directive deleted (CoolSolve has a single unit
  system). Unit system converted **by hand** from `SI MASS DEG KPA C KJ` to
  `SI MASS DEG PA C J` (ees_import.md §6): `P_amb = 101.325 [kPa]` →
  `101325 [Pa]` (original value kept in the comment),
  `cp_air = 1.005 [kJ/kg-C]` → `1005 [J/kg-K]`, and the two vapour
  enthalpies `2500.9 [kJ/kg]+1.82*(25) [kJ/kg]` →
  `2500900 + 1820*T_db` and `2500900 + 1820*T_wb` [J/kg]. All other
  equations are homogeneous and stay unchanged; the temperatures are already
  in °C and no equation uses an absolute temperature. Two unit annotations had
  to be removed for the file to parse, both already in the register and both
  non blocking: the annotation on the named argument `T=0[C]` of the four
  `enthalpy` calls of the reference-shift equations
  (`CS-GAP-UNIT-NAMEDARG`, rewritten as `T=0`; the unit is °C in both unit
  systems). Comments translated to English and paraphrased (no comment
  invents physical meaning), section titles kept as displayed comments. No
  `.initials` needed (fully explicit model). Verified against the EES stored
  solution (see above).
- **2026-10-05 — two input values turned back into symbols.** The original
  writes the numeric dry-bulb and wet-bulb temperatures inside the course
  expression for the vapour enthalpy (`2500.9[kJ/kg]+1.82*(25)[kJ/kg]` and
  `... 1.82*(15)[kJ/kg]`) instead of the variables `T_db` and `T_wb`, which
  it defines just above. The symbols are restored, so that the relation
  reads as a function of the measured temperatures; the values are unchanged
  for the inputs of the statement (25 °C and 15 °C), and the results are
  those of the original.
- The 44 stale variables of the EES binary (arrays and scalars of an earlier
  exercise, see *Verification*) were not carried over, and no `.initials` is
  shipped.
- **Level score** (taxonomy.md §3): equations 27 → 0; largest block 1 → 0;
  no arrays/functions/procedures → 0; a single physical system, not
  multi-zone → 0; no semi-empirical, off-design or dynamic physics → 0; no
  curated guesses, `coolsolve.conf` or *Try Harder* → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

- None blocking: the model runs in CoolSolve (`missing_features` is empty)
  and every equation is satisfied (27/27, max residual 0). One
  unit-annotation gap of the register (`CS-GAP-UNIT-NAMEDARG`) is met by the
  original but rewritten away by the mandatory hand unit conversion, so it
  does not block the native file.
- CoolSolve prints one hint when solving: `enthalpy(): p=1053.14 is
  interpreted as 1053.14 Pa`. It is the call `h_g_db_bis2` on the vapour
  partial pressure, correctly converted from the 1.053 kPa of the original.
- The course constants (1.005 kJ/kg·K, 2500.9 kJ/kg, 1.82 kJ/kg·K, 0.622)
  are constants of the course, not properties of the EES fluids; comparing
  them with the property functions is the point of the exercise.
- `enthalpy(Water,T=0,x=0)` (the reference state of the water, which the
  course takes equal to 0 at 0 °C) returns −41.6 J/kg in CoolProp: the
  property package uses another water reference. The term is kept as in the
  original and contributes −0.27 J/kg, i.e. 6·10⁻⁶ relative, to `h_db_bis2`.

## Related models

- `CSL-0055` *moist_air_room_psychrometrics*: same session (R9), exercise 1:
  the same humidity-ratio, enthalpy and reference-shift relations of the
  course, cross-checked with the EES property functions.
- `CSL-0063` *moist_air_adiabatic_mixing*, `CSL-0064` *psychrometric_mixer_condensation*:
  same session, exercises 2 and 3: mixing of moist air, with the same
  humid-air property offsets on the humidity ratios.
- `CSL-0028` *air_handling_unit_moist_air*: air handling unit on `AirH2O`
  (property calls on the same fluid).
- `CSL-0062` *cooling_coil_condensate_ratio*: humid-air property calls
  cross-checked with the course relations (same pattern as here).
- `CSL-0070` *adiabatic_humidifier_simplified*: humidifier on `AirH2O`
  described by an effectiveness-NTU closure about the wet-bulb state
  (the humidification line of this exercise).
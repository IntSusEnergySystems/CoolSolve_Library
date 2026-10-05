# Moist air in a room: humidity ratio, enthalpy and dew point

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0055`

Moist air filling a closed room: the model computes the partial pressures of
dry air and of water vapour, the humidity ratio, the specific enthalpy per kg
of dry air, the masses of dry air and of water vapour in the room, and the
dew-point temperature below which condensation appears on the windows. Every
quantity is obtained twice — once with the relations of the course
(approximate humidity-ratio formula, constant heat capacities) and once with
the EES property functions — so the exercise doubles as a comparison of the
two approaches.

| | |
|---|---|
| **Category** | Heating, ventilation and air conditioning › Psychrometrics |
| **Fluids** | AirH2O, Water, Air |
| **Size** | 28 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), exercise session R9, exercise 1 (EES file `R09_E01_2022.EES`) |
| **Authors** | TBD (see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution and the course's Python/CoolProp solution (see *Verification*) |

## Problem statement

A room of 5 m × 5 m × 3 m contains air at 25 °C with a degree of saturation
(relative humidity) of 75 %. The ambient pressure is 100 kPa. Determine:

- a) the partial pressure of the air;
- b) the humidity ratio (absolute humidity) and the specific enthalpy of the
  air;
- c) the masses of air and of water vapour contained in the room;
- d) below which temperature does condensation appear on the windows?

## Model

The room is treated as a rigid volume of moist air in equilibrium at the
dry-bulb temperature `T`, the whole content being at the ambient pressure `p`.

The relative humidity is the ratio of the partial pressure of the vapour to
the saturation pressure of water at the air temperature, so the vapour partial
pressure follows directly,

$$p_v = \phi\, p_{sat}(T), \qquad p_{air} = p - p_v$$

and the humidity ratio follows from the approximate relation of the course
(the model also evaluates the EES function `HumRat`, which returns a very
similar value),

$$w \simeq 0.622\, \frac{p_v}{p - p_v}$$

The specific enthalpy per kg of dry air is computed with the EES function
`enthalpy` on the moist-air fluid `AirH2O` and, independently, from its
definition with constant heat capacities,

$$h_{aa} = c_{p,air}\,T + w\,h_v, \qquad h_v = 2500.9 + 1.82\,T \;\;[\text{kJ/kg}]$$

The dry-air mass is obtained from the specific volume of the dry air
(`VOLUME`) and, independently, from the ideal-gas relation written with the
partial pressures (`p_air·Vol = m_air2·R_air·(T+273.15)`); the vapour mass
follows from the humidity ratio or from the same ideal-gas relation.

The dew point is the temperature at which the air becomes saturated at the
given humidity ratio, returned by the EES function `dewpoint`; below it, the
windows of the room are colder than the air and condense.

The original states `p = 100 kPa` as an input and writes the sum of the
partial pressures as the equation `p = p_air + p_v`. Both statements are kept
verbatim: CoolSolve keeps `p` at its input value and uses the equation to fix
`p_air` (the model is square, checked with `coolsolve -d`: 28 equations,
28 variables, *System square: Yes*, all blocks of size 1), and reproduces the
stored EES value `p_air` = 97.62263 kPa.

## How to run

Open `moist_air_room_psychrometrics.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./moist_air_room_psychrometrics.eescode
```

The system is fully explicit (28 blocks of size 1): no guess values are
needed, and no `.initials` file is shipped.

## Results

| Quantity | Course relations | EES property functions |
|---|---:|---:|
| `p_sat` saturation pressure at 25 °C | 3.16993 kPa | — |
| `p_v` vapour partial pressure | 2.37745 kPa | — |
| `p_air` dry-air partial pressure | 97.62255 kPa | — |
| `w_corr` / `w_ees` humidity ratio | 0.0151479 | 0.0152115 kg/kg dry air |
| `h_air` / `h_air2` / `h_air3` dry-air enthalpy (0 °C reference) | 25.125 | 25.1472 / 25.1489 kJ/kg |
| `h_aa` / `h_a` enthalpy of the moist air | 63.6975 | 63.8812 kJ/kg dry air |
| `h_v` / `h_v2` vapour enthalpy | 2546.4 | 2546.909 kJ/kg |
| `v` / `v3` specific volume of the dry air | 0.876675 | 0.876402 m³/kg |
| `m_air` / `m_air3` mass of dry air (`VOLUME` route) | 85.5772 | 85.5772 kg |
| `m_air2` mass of dry air (ideal-gas route) | 85.5498 | — |
| `m_v` / `m_v2` mass of water vapour | 1.3018 | 1.2948 kg |
| `T_r` dew-point temperature | 20.1966 °C | — |

Sanity checks: `p_v + p_air` = 2.37745 + 97.62255 = 100 kPa; the course
enthalpy `h_aa` and the `enthalpy` function agree to 0.29 %; the two mass
routes (85.5772 kg from `VOLUME`, 85.5498 kg from the ideal-gas relation)
differ by 0.03 %, which is the 3.2·10⁻⁴ difference between the gas constant
implied by CoolProp's `Air` (286.96 J/kg·K) and the constant 287.05 J/kg·K of
the course. The room can be cooled by 25 − 20.2 = 4.8 K before the windows
fog over.

`HumRat` returns a humidity ratio 0.42 % above the course formula
(0.0152115 vs 0.0151479): CoolProp's moist air carries the water-enhancement
factor, so the vapour partial pressure it implies is 9.75 Pa higher, which
lowers the dew point computed from `w_corr` by 9.75/143 = 0.068 K. Computed
from `phi` instead of `w_corr`, the dew point is 20.26 °C (see *Verification*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): CoolSolve has no
     psychrometric chart yet (CS-FEAT-PSYCHRO), so the figure of this humid-air model is
     a parametric sweep (roadmap decision D7), e.g. dew point `T_r` or humidity ratio
     `w_corr` as a function of the relative humidity `phi` (CoolSolve GUI, Parametric tab),
     saved as figures/moist_air_room_psychrometrics_phi.png -->

## Verification

**Faithful import vs EES.** The hand-converted model was compared with the
solution stored in the source EES file (`compare_solution.py --ees-units`):
**27 common variables, 7 differ at rtol = 0.001, largest relative deviation
4.76e-03** (on `m_v`). The seven variables and their relative deviations:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `m_v` | 1.29557 | 1.30176 | 4.76e-03 |
| `w_ees` | 0.0151439 | 0.0152115 | 4.45e-03 |
| `T_r` | 20.2648 | 20.1966 | 3.37e-03 |
| `h_a` | 63680 | 63881.2 | 3.15e-03 |
| `h_air3` | 25103.7 | 25148.9 | 1.80e-03 |
| `R_air` | 0.28705 | 287.05 | 9.99e-01 |
| `R_v` | 0.461889 | 461.889 | 9.99e-01 |

Explanations, one per deviation:

- `w_ees`, `m_v` (+4.5 %·10⁻¹, +0.48 %): the EES function `HumRat`, i.e. the
  humid-air formulation. CoolProp's moist air includes the water-enhancement
  factor, which puts `w_ees` 0.42 % above the course formula `w_corr`
  (0.0152115 vs 0.0151479); `w_corr` itself agrees with EES to 3.4e-05, so the
  property backend, not the conversion, is responsible. `m_v = w_ees·m_air`
  inherits the difference. The same order of magnitude was measured on
  `CSL-0016` *moist_air_cooling_coil_contact_factor* (+0.46 %).
- `T_r` (3.4e-03, −0.068 K): the dew point is computed from `w_corr`, and
  `w_corr` is 0.42 % above the vapour pressure EES uses for its own stored
  answer; 9.75 Pa of vapour pressure at 20 °C is 9.75/143 = 0.068 K. Computed
  from the relative humidity, the same CoolProp backend gives
  `dewpoint(AirH2O,T=25,P=1e5,r=0.75)` = 20.2628 °C, i.e. the EES value 20.2648 °C.
- `h_a` (3.2e-03): EES and CoolProp use different reference states and slightly
  different moist-air formulations for the absolute enthalpy; the course
  definition `h_aa` = 63.6975 kJ/kg agrees with both (EES 63.67998, CoolProp
  63.88121), and `CSL-0016` measured the same +0.3 % moist-air enthalpy offset.
- `h_air3` (1.8e-03) and `m_air` (3.1e-04, below the tolerance): `enthalpy(air,…)`
  and `VOLUME(air,…)` on the ideal-gas substance `Air`, EES JANAF data vs
  CoolProp: the specific volume implies a gas constant of 286.96 J/kg·K in
  CoolProp against 287.05 in EES (0.876402 vs 0.876675 m³/kg). Note that the
  comment of the original calls `v` the specific volume with air "as a real
  gas", but EES's `Air` is an ideal gas and the value it stored is the
  ideal-gas one (287.05·298.15/97622.63 = 0.876675 m³/kg).
- `R_air`, `R_v`: **not a real difference.** EES stored these two constants in
  the unit spelling `kj/(kg-C)`, which `compare_solution.py --ees-units` does
  not recognise (it matches `kJ`, capital J), so the tool compares
  0.28705 kJ/(kg·K) with 287.05 J/(kg·K) and reports 9.99e-01. The two values
  are identical by construction (0.28705 kJ/(kg·K) = 287.05 J/(kg·K)), and the
  hand conversion of the equations (below) is exactly this one. New tool bug
  registered as `CS-BUG-COMPARE-UNIT-CASE`.

**Second reference — the course's Python/CoolProp solution.** The same
exercise was solved with CoolProp in the course (2021 edition,
`ThAp21_R08E01.py`, credited to N. Paulus). Running it reproduces the values
quoted in its own printed output and agrees with the converted model:

| Quantity | Python/CoolProp | This model |
|---|---:|---:|
| `p_air` | 97 622.55 Pa | 97 622.553 Pa |
| `h_a` (`HAPropsSI('H',T,P,R)`) | 63 881.211 J/kg | 63 881.211 J/kg |
| `w_corr` | 0.0151479 | 0.0151479 |
| `m_air` (`75/Vda`) | 85.577 kg | 85.5772 kg (`m_air3`, the `air_ha` route) |
| dew point from `phi` (side check, not a variable of the model) | 20.26 °C | 20.2628 °C (`dewpoint(AirH2O,T=25,P=1e5,r=0.75)`) |

**Variables left out of the comparison.** The EES file stores 31 variables
that are not part of this model: the arrays `h[1…6]`, `p[1…6]`, `T[1…6]`,
`s[1…6]`, `v[1…6]`, `t[5]` and the scalars `h`, `a`, `R`. They carry no
equation (they hold no value in the Equations window) and they are leftovers
of an earlier exercise saved in the same EES file — the sibling exercises of
the same folder (`R09_E02_2022.EES` …) carry the very same arrays. They were
not carried over. The decoded parametric table of the extraction report
(`table1`, 4931×2, columns `V` and `l`) is such a leftover as well: it is
empty apart from a few `-9999` sentinels, no equation of the model calls it,
and the model does not ship it. Only `fluid$` is CoolSolve-only in the `.sol`
(it appears twice, as a number and as a string: `CS-BUG-SOL-STRING`).

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
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/R09_E01_2022.EES`
(inventory candidate `TM-0451`, duplicate group `DG-0111`).

Reference used for the second verification:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/Python/ThAp21_R08E01.py`
(Python/CoolProp solution of the same exercise, 2021 edition, author
N. Paulus).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  decimal comma converted automatically by the tool, EES licence and display
  tags removed, `$UnitSystem` directive deleted. Unit system converted **by
  hand** from `SI MASS DEG KPA C KJ` to `SI MASS DEG PA C J`
  (ees_import.md §6): `p = 100 [kPa]` → `100e3 [Pa]` (original value kept in
  the comment), `cp_air` 1.005 → `1005 [J/kg-K]`, `h_v` written
  `2500.9 [kJ/kg]+1.82 [kJ/(C-kg)]*T` → `2500900 + 1820*T` [J/kg],
  `R_v = 8.314/18` → `8314/18` and `R_air = 0.28705` → `287.05` [J/kg·K]. All
  other equations are homogeneous and stay unchanged; the temperatures are
  already in °C and the only absolute temperature, `(T+273.15[C])` of the two
  ideal-gas equations, keeps its 273.15 offset. Two unit annotations had to be
  removed for the file to parse (both non blocking, already in the register):
  the annotation on a sub-expression `1.82 [kJ/(C-kg)]*T` and on the named
  argument `T=0[C]` (`CS-GAP-UNIT-SUBEXPR`, `CS-GAP-UNIT-NAMEDARG`; the
  conversion rewrites both lines, so no `_coolsolve` variant is needed). The
  `$UnitSystem` line was the only thing that made the file unparsable as
  extracted; comments translated to English and paraphrased (no comment
  invents physical meaning), section titles kept as displayed comments. The
  31 stale variables of the EES binary (arrays and scalars of an earlier
  exercise, see *Verification*) were not carried over, and the unused
  4931×2 parametric-table leftover of the extraction report is not shipped. No
  `.initials` needed (fully explicit model). Verified against the EES stored
  solution and the course's Python solution (see above).
- **2026-10-05 — duplicate group `DG-0111` triaged.** `TM-0533` (2017-2018,
  inside `THD10_R10.zip`) and `TM-0551` (inside `R9.zip`) are the same exercise
  with the same statement and the same inputs, but not the same equations, so
  both are `merged` rather than `duplicate`: the 2017 file (EES 8.423, 46
  variables) has no reference-shift equations (`h_air2`, `h_air3`), no course
  formula for `h_v` (it uses `enthalpy(water,…)` only), and computes
  `v = volume(AirH2O,T=T,p=p,r=phi)` and
  `T_r = dewpoint(AirH2O,T=T,p=p,r=phi)`; the copy inside `R9.zip` (54
  variables) is an earlier revision of the 2022 file, with
  `enthalpy(air_ha,p=p,T=T)` (total pressure instead of `p_air`) and the
  `AirH2O`/`r=phi` form of `volume` and `dewpoint`. Nothing of the two older
  files adds to this model, so they are described here only and not shipped as
  variant files.
- **Level score** (taxonomy.md §3): equations 28 → 0; largest block 1 → 0;
  no arrays/functions/procedures → 0; a single physical system, not
  multi-zone → 0; no semi-empirical, off-design or dynamic physics → 0; no
  curated guesses, `coolsolve.conf` or *Try Harder* → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

- None blocking: the model runs in CoolSolve, `missing_features` is empty.
  Two unit-annotation gaps of the register (`CS-GAP-UNIT-SUBEXPR`,
  `CS-GAP-UNIT-NAMEDARG`) are met by the original but are rewritten away by
  the mandatory hand unit conversion, so they do not block the native file.
- The specific heat capacity of dry air, the latent heat of vapour at 0 °C and
  the two specific gas constants are constants of the course (1.005 kJ/kg·K,
  2500.9 kJ/kg, 1.82 kJ/kg·K, 0.28705 and 0.4619 kJ/kg·K), not properties of
  the EES fluids; this is the point of the exercise (compare the course
  relations with the property functions).
- `v` is the ideal-gas specific volume of dry air although the comment of the
  original speaks of air "as a real gas" (EES's `Air` is an ideal-gas
  substance); the equation and the value are kept as they are.

## Related models

- `CSL-0016` *moist_air_cooling_coil_contact_factor*: moist air cooled over a
  coil, per kg of dry air, with the same EES-vs-CoolProp humid-air offsets
  (+0.46 % on the humidity ratios).
- `CSL-0028` *air_handling_unit_moist_air*: air handling unit on `AirH2O`,
  companion exercise of the same kind (blocked native file, runnable
  `_coolsolve` variant).
- `CSL-0062` *cooling_coil_condensate_ratio*: cooling coil of a heat-pump
  cycle, humid-air property calls cross-checked with the course relations
  (same pattern as here).
- `CSL-0063` *moist_air_adiabatic_mixing*: adiabatic mixing of room and
  outdoor air (same course, session R9).

- `CSL-0064` *psychrometric_mixer_condensation*: same session, exercise 3
  (room air mixed with outdoor air, condensation in the mixer); same
  humid-air property offsets (+0.4 % on the humidity ratios).
- `CSL-0066` *adiabatic_saturation_wet_bulb*: same session, exercise 5:
  specific humidity, relative humidity and enthalpy from the dry-bulb and
  wet-bulb temperatures (adiabatic-saturation formula of the course).

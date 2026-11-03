# Vehicle exhaust emissions from fuel flow and gas fractions

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0278`

Teaching exercise: pollutant emissions of a vehicle from the fuel mass flow,
the excess-air factor and the CO, NO2 and HC mole fractions of the wet exhaust
gas. The mole fractions are converted to mass fractions (given exhaust-gas
molar mass) and reported as emission indices in g/kg fuel, g/km and g/kWh of
brake work — the units of the European emission regulations. The native file
is blocked because CoolProp has no NO2 fluid; the runnable variant
`vehicle_exhaust_emissions_coolsolve.eescode` builds the NO2 molar mass from
atomic weights instead and reproduces the EES stored solution.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | CO, NO2 (molar masses only), C3H8 (HC surrogate) |
| **Size** | 30 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP7/EX_1_PNG_2019.EES` |
| **Authors** | P. Ngendakumana |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — native blocked by CS-GAP-FLUIDS-NASA-SPECIES; variant verified |

## Problem statement

A vehicle drives at 60 km/h with a brake power of 80 kW. It burns diesel fuel
at 4.303 g/s with an excess-air factor λ = 2 (stoichiometric air-fuel ratio
14.6). The wet exhaust gas carries 2200 ppm mole fraction of CO, 1000 ppm of
NO2 and 300 ppm of unburned hydrocarbons (taken as C3H8); its mean molar mass
is 28.6 kg/kmol. Compute the air and exhaust-gas mass flows, and the CO, NO2
and HC emissions in g/kg of fuel, g/km and g/kWh.

## Model

All equations are explicit (each block holds one equation):

- Air flow from the excess-air factor: `AFR = Lambda*AFR_st`,
  `M_dot_a = AFR*M_dot_f`, exhaust-gas flow `M_dot_g = M_dot_a + M_dot_f`.
- Mole-to-mass fraction conversion with the mean exhaust molar mass:
  `y_i = x_i*MM_i/MM_g`.
- Pollutant mass flows `M_dot_i = y_i*M_dot_g`, then the three emission
  indices per pollutant: per fuel mass `1e3*M_dot_i/M_dot_f` [g/kg],
  per distance `1e3*M_dot_i/V` [g/km] and per brake work
  `1e3*M_dot_i/(W_dot_sh*1e-3/3600)` [g/kWh].

## How to run

```bash
coolsolve ./vehicle_exhaust_emissions_coolsolve.eescode
```

The native file `vehicle_exhaust_emissions.eescode` is kept in valid EES and
fails on `MM_NO2 = molarmass(NO2)` (no NO2 fluid, see gaps below). The variant
changes only that one equation. No `.initials` needed: the system is a chain
of explicit equations (default guesses suffice, 4 iterations).

## Results (variant, default operating point)

| Variable | Value | Unit |
|---|---:|---|
| AFR | 29.2 | kg air/kg fuel |
| M_dot_a | 0.12565 | kg/s |
| M_dot_g | 0.12995 | kg/s |
| y_CO_f / y_NO2_f / y_HC_f | 65.07 / 48.58 / 13.97 | g/kg fuel |
| y_CO_km / y_NO2_km / y_HC_km | 16.80 / 12.54 / 3.61 | g/km |
| y_CO_W / y_NO2_W / y_HC_W | 12.60 / 9.41 / 2.70 | g/kWh |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g. ![CO2 emissions per km](figures/vehicle_exhaust_emissions_pollutants.png) + one-line caption -->

## Verification

Variant compared with the EES stored solution of `EX_1_PNG_2019.EES`
(`compare_solution.py`, reference `ees_variables_full.csv`):

> 30 common variables, 0 differ (rtol=0.001); only in EES: 24; only in
> CoolSolve: 0

Largest relative difference **3.13e-05** on `MM_HC` (CoolProp C3H8 molar mass
44.09562 kg/kmol, EES 44.097). The 24 EES-only variables are the variables of
the commented-out CO2 block of the source (see conversion log), left as
default guesses in the EES records except `f_st` = 0.06702 and
`AFR_st_bis` = 14.92, which agree with a hand check of the diesel formula
C12H26.

The 9 emission-index records (`y_*_f`, `y_*_km`, `y_*_W`) are missing from the
`ees_extract.py` output: their records carry format byte 1 instead of 3 and
are silently dropped — registered bug `CS-BUG-EXTRACT-FMT-BYTE`. They were
recovered by hand-decoding the binary (values 65.0694, 48.5798, 13.9692 g/kg,
16.7996, 12.5423, 3.6066 g/km, 12.5997, 9.4067, 2.7049 g/kWh) and re-derive
exactly from the kept stored values (`y_CO_km = 1e3*M_dot_CO/V` etc.). The
native file itself was also run to confirm the failure mode: `Unknown fluid:
'NO2'`.

## Source and attribution

- Source: `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP7/EX_1_PNG_2019.EES`
  (EES 10.589, ULiège collection), file name tag `PNG_2019`, EES licence stamp
  of P. Ngendakumana (ULiège Thermotechnics); statement in French in the
  comments ("MCI - TP - Séance 7 : Exercice 1").
- Authors: P. Ngendakumana (course MCI, TP séance 7, 2019).
- License: MIT (ULiège laboratory collection).

## Conversion log

- **2026-10-22 — import**: extracted with `tools/ees_extract.py` (EES 10.589,
  unit system SI-MASS-DEG-PA-C-J: no unit conversion needed; NUL byte and
  `$UnitSystem`/`$TABSTOPS` lines removed; licence/display tags removed).
  Comments translated from French. 9 stored-value records missing from the
  extraction (format byte 1, `CS-BUG-EXTRACT-FMT-BYTE`), recovered by hand as
  described under Verification.
- **2026-10-22 — dead code removed**: the source carries a commented-out
  `{...}` block ("Emissions de CO2 en g/km : à ajouter pour 2016-2017",
  combustion of C12H26 with CO/HC/NO2 speciation, marked by the author as
  unrealistic: "Pas de NO dans les gaz d'échappement, mais NO2? Ce n'est pas
  réaliste"). It is not part of the exercise and is dropped from both files
  (no impact: the block was never solved; its variables carry default guesses
  in the EES records).
- **2026-10-22 — comment correction**: the original comment of `Lambda` says
  "richesse" (richness), but λ = 2 with AFR = 29.2 > AFR_st = 14.6 is *lean*
  combustion (excess air); the comment was corrected, the equation unchanged.
- **2026-10-22 — variant** `vehicle_exhaust_emissions_coolsolve.eescode`: the
  single equation `MM_NO2 = molarmass(NO2)` (unknown fluid, valid EES) is
  replaced by `MM_NO2 = molarmass(N)+2*molarmass(O)` = 46.0055 kg/kmol — the
  same standard atomic weights EES uses for NO2 (stored 46.006, rel. diff
  1.1e-05). Valid EES syntax; no other change.
- **Level**: equations 30 (<50) = 0; largest block 1 (≤5) = 0; no
  functions/arrays = 0; single system = 0; no calibration/dynamics = 0;
  default guesses = 0 → score 0 → level 1.

## Niche

Nearest library models: `CSL-0188` *fuel_co2_per_km* (same MCI TP7 session,
CO2 per km from a fuel volume consumption by stoichiometric combustion) and
`CSL-0058`/`CSL-0266` *diesel/gasoline_engine_excess_air_exhaust_analysis*
(exhaust composition analysis to find λ and the fuel composition — the
inverse problem). This model adds the emission-index accounting of a
regulated pollutant set (CO, NO2, HC) in the three regulatory units
(g/kg fuel, g/km, g/kWh) from λ and measured wet-gas fractions; no library
model converts measured pollutant fractions into emission indices.

## Limitations and CoolSolve gaps

- The native file needs the species **NO2**, which neither CoolProp nor
  CoolSolve has: `MM_NO2 = molarmass(NO2)` fails with *Unknown fluid: 'NO2'*.
  Registered gap **CS-GAP-FLUIDS-NASA-SPECIES** (one of the six missing
  NASA species; this model needs only its molar mass) — the only entry of
  `missing_features`. The variant substitutes atomic weights.
- Emissions per kWh use the brake power only (no accounting of the drive
  cycle), as in the original exercise.

## Related models

- CSL-0188 (*fuel_co2_per_km*): same MCI TP7 session, CO2 emissions per km
  from the fuel volume consumption (exercise 3 of the same statement).
- CSL-0058 (*diesel_engine_excess_air_exhaust_analysis*), CSL-0266
  (*gasoline_engine_excess_air_exhaust_analysis*): exhaust-gas composition
  used the other way round, to identify λ and the fuel.
- CSL-0279 (*engine_bsfc_bore_stroke_afr*): exercise 2 of the same TP7
  statement; engine geometry and volumetric efficiency give the fuel flow and
  the specific fuel consumptions instead of the emissions.

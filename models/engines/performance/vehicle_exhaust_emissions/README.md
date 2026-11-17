# Vehicle exhaust emissions from fuel flow and gas fractions

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0278`

Pollutant emissions of a vehicle from the fuel mass flow, the excess-air
factor and the CO, NO2 and HC mole fractions of the wet exhaust gas. The mole
fractions become mass fractions (given exhaust molar mass) and emission
indices in g/kg of fuel, g/km and g/kWh of brake work.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | CO, NO2, C3H8 (molar masses only; HC is taken as propane) |
| **Size** | 30 equations (largest block: 1) |
| **Source** | ULiège MCI, TP7 exercise 1 (`EX_1_PNG_2019.EES`) |
| **Authors** | P. Ngendakumana |
| **License** | MIT |
| **CoolSolve** | 0.5.0@793f378 — verified |

## Problem statement

A vehicle at 60 km/h and 80 kW burns diesel at 4.303 g/s with λ = 2
(stoichiometric air-fuel ratio 14.6). The wet exhaust holds 2200 ppm CO,
1000 ppm NO2 and 300 ppm HC (as C3H8); its molar mass is 28.6 kg/kmol.
Compute the air and exhaust mass flows and the three emission indices.

## Model

Explicit chain. `AFR = Lambda*AFR_st`, then the air and exhaust mass flows.
`y_i = x_i*MM_i/MM_g` with `MM_CO = molarmass(CO)`, `MM_NO2 = molarmass(NO2)`
and `MM_HC = molarmass(C3H8)`. Each pollutant mass flow is reported per kg of
fuel, per km and per kWh of brake work.

## How to run

```bash
coolsolve vehicle_exhaust_emissions.eescode
```

No guesses: 30 explicit equations, 4 iterations.

## Results

| Variable | Value | Unit |
|---|---:|---|
| AFR | 29.2 | kg air/kg fuel |
| M_dot_g | 0.1300 | kg/s |
| y_CO_f / y_NO2_f / y_HC_f | 65.07 / 48.58 / 13.97 | g/kg fuel |
| y_CO_km / y_NO2_km / y_HC_km | 16.80 / 12.54 / 3.61 | g/km |
| y_CO_W / y_NO2_W / y_HC_W | 12.60 / 9.41 / 2.70 | g/kWh |

## Verification

`compare_solution.py` against the stored solution of `EX_1_PNG_2019.EES`:

> 30 common variables, 0 differ (rtol=0.001); only in EES: 24; only in CoolSolve: 0

Largest relative difference **3.13e-05** on `MM_HC` (CoolProp C3H8 44.09562
kg/kmol, EES 44.097). `MM_NO2` is 46.0055 against the stored 46.006. The 24
EES-only names belong to a commented-out CO2 block of the source (C12H26);
they are not equations of this exercise. Nine emission-index records were
absent from the extractor output (format byte 1) and were recovered by hand
from the file; they match `1e3*M_dot_i/V` and the other index definitions.

## Source and attribution

`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP7/EX_1_PNG_2019.EES`
(EES 10.589, P. Ngendakumana, ULiège MCI TP séance 7, 2019). MIT.

## Conversion log

- **2026-10-22 — import**: already `SI MASS DEG PA C J`; licence tags and the
  commented-out CO2 block removed (never solved). The original comment calls
  λ = 2 "richesse"; with AFR = 29.2 the mixture is lean, and the comment says
  so. Equations unchanged.
- **Level**: 30 equations, largest block 1, no routine or array → score 0 →
  level 1.

## Limitations

The indices use the brake power of this point only, as in the exercise. There
is no drive cycle.

## Related models

- `CSL-0188` *fuel_co2_per_km*: same session, CO2 per km from a fuel volume.
- `CSL-0058`, `CSL-0266`: exhaust analysis used to find λ, the inverse problem.
- `CSL-0279` *engine_bsfc_bore_stroke_afr*: exercise 2 of the same statement.

# Engine bsfc from bore, stroke and air-fuel ratio (MCI TP7 Ex2)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0279`

Teaching exercise (ULiège MCI, TP séance 7, exercise 2): a 12-cylinder
four-stroke engine is described by its bore and stroke, its speed, the
air-fuel mass ratio and the volumetric, mechanical and combustion
efficiencies. The volumetric efficiency gives the air mass flow, the AFR the
fuel mass flow, hence the brake and indicated specific fuel consumptions
(bsfc, isfc in g/kWh) and the unburnt-hydrocarbon flow per unit of shaft
work.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air |
| **Size** | 24 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP7/EX_2_PNG_2019.EES` (EES X10.589) |
| **Authors** | P. Ngendakumana, R. Dickes |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (max rel. diff 3.13e-04) |

## Problem statement

The equation window is titled `MCI - TP - Séance 7 : Exercice 2` (2019).
Data, as written in the file:

- `n_c = 12` cylinders
- `i = 1/2`, the intermittency factor of a four-stroke engine
- `W_dot_sh = 2440` kW, the shaft power
- `RPM = 550` rev/min
- `AFR = 14.5`, the air-fuel mass ratio
- `D = 24e-2` m, the bore; `L = 32e-2` m, the piston stroke
- `epsilon_v = 0.97`, the volumetric efficiency
- `eta_m = 0.88`, the mechanical efficiency
- `epsilon_c = 0.98`, the combustion efficiency
- `p_su = 98` kPa, `T_su = 25` °C, the intake state

## Model

Total displacement from the bore and the stroke:

\[
V_s = n_c\,\pi\,D^2/4\,L = 0.1737\ \mathrm{m^3}
\]

Air mass flow from the definition of the volumetric efficiency (as in the
original, solved for `M_dot_a`), with the intake density on `Air`:

\[
\epsilon_v = \dot M_a/(\rho_{su}\,V_s\,N\,i), \qquad
\rho_{su} = \mathrm{density}(\mathrm{Air},T_{su},p_{su})
\]

Fuel mass flow from the air-fuel ratio, `f = 1/AFR`, `M_dot_f = f*M_dot_a`.

Brake and indicated specific fuel consumptions (g/kWh; the factor is
`3600*10^6` because `W_dot_sh` and `W_dot_i` are in W — the original, in kW,
wrote `3600*1000`), the mechanical-efficiency chain, and the check of isfc:

\[
\mathrm{bsfc} = \dot M_f\,3600\,10^6/\dot W_{sh} = \mathrm{isfc}/\eta_m, \qquad
\dot W_{sh} = \eta_m\,\dot W_i, \qquad
\mathrm{isfc\_bis} = \dot M_f\,3600\,10^6/\dot W_i
\]

Unburnt hydrocarbons, referred to the shaft work:

\[
\dot M_{f,unb} = (1-\epsilon_c)\,\dot M_f \quad \mathrm{[g/s]}, \qquad
\dot M_{f,unb,W} = \dot M_{f,unb}\,3600\,10^3/\dot W_{sh} \quad \mathrm{[g/kWh]}
\]

Every block has size 1; the system is square (24 equations, 24 variables).

## How to run

```bash
coolsolve ./engine_bsfc_bore_stroke_afr.eescode
```

The `.initials` file holds the stored EES values (converted); without it the
model also solves from the default guesses.

## Results

| Quantity | Value | Unit |
|---|---:|---|
| `V_s` total displacement | 0.1737 | m³ |
| `N` engine speed | 9.167 | rev/s |
| `rho_su` intake air density | 1.1454 | kg/m³ |
| `M_dot_a` air mass flow | 0.8846 | kg/s |
| `M_dot_f` fuel mass flow | 0.06101 | kg/s |
| `bsfc` brake specific fuel consumption | 90.01 | g/kWh |
| `isfc` = `isfc_bis` indicated specific fuel consumption | 79.21 | g/kWh |
| `W_dot_i` indicated power | 2.773×10⁶ | W |
| `M_dot_f_unb` unburnt fuel flow | 1.220 | g/s |
| `M_dot_f_unb_W` unburnt fuel per shaft work | 1.800 | g/kWh |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `EX_2_PNG_2019.EES` (EES X10.589, 20
records). The file stores 20 of its 24 variables: `M_dot_f`, `bsfc`, `isfc`
and `isfc_bis` have no stored record (they were typed after the last solve,
or cleared); they are checked above by the identity `isfc = isfc_bis` and
`bsfc = isfc/eta_m` instead.

`compare_solution.py engine_bsfc_bore_stroke_afr.sol reference/ees_variables.csv --ees-units`:
**20 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
CoolSolve: 5.** Maximum relative difference **3.13e-04**, on `rho_su` and the
flows derived from it (`M_dot_a`, `M_dot_f_unb`, `M_dot_f_unb_W`): the
original calls `DENSITY(Air,…)` on the EES real `Air` fluid, CoolSolve uses
the CoolProp `Air` ideal gas; 0.03 % is within the property tolerance. The
other CoolSolve-only names are `M_dot_f`, `bsfc`, `isfc`, `isfc_bis` (above)
and the constant `pi`.

## Niche

Nearest models: `CSL-0221` `supercharged_engine_air_flow` (shares the
volumetric-efficiency air-flow equation, but on a supercharger/intercooler
system, no displacement from geometry and no consumptions), `CSL-0244`
`engine_dynamometer_test` (the eta_m shaft/indicated chain from a dynamometer
reading, no fuel and no geometry) and `CSL-0278` `vehicle_exhaust_emissions`
(same TP7 session, exercise 1: emissions per km and per kWh from a given fuel
flow, no geometry or volumetric efficiency). This model is the only one that
links bore/stroke → displacement → air flow → fuel flow → bsfc/isfc and
unburnt HC, as one teaching chain.

## Source and attribution

Source: `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP7/EX_2_PNG_2019.EES`
(ULiège collection, MCI TP séance 7, exercise 2, 2019; stored as RTF; EES
licence stamp P. Ngendakumana). Authors P. Ngendakumana, R. Dickes
(inventory). MIT licence, as the rest of the collection.

## Conversion log

- **2026-10-23 — import** (ees_extract.py, RTF equations decoded, `{$ID$…}`,
  `{$PX$96}`, `{$ST$OFF}` tags removed): unit system `SI MASS DEG KPA C KJ`
  converted by hand to SI-°C-Pa-J (ees_import.md §6): `W_dot_sh = 2440e3` W
  (2440 kW), `p_su = 98e3` Pa (98 kPa); the g/kWh factors become
  `3600*1e6/W` for bsfc/isfc_bis (original `3600*1000` with W in kW) and
  `3600*1e3/W` for `M_dot_f_unb_W` (original `3600`); `DENSITY(Air,…)`
  written `density(Air,…)`. Comments translated to English; `$UnitSystem` and
  `$TABSTOPS` directives removed. No other equation changed.
- **2026-10-23 — verification**: solved unmodified after conversion
  (system square 24×24, largest block 1, no curated guesses needed); 20/20
  stored variables agree, max rel diff 3.13e-04 (see Verification).
- **Level**: equations 24 → 0; largest block 1 → 0; no special structure → 0;
  not multi-zone → 0; no calibration/off-design → 0; default guesses → 0.
  Score 0 → level 1.

## Limitations and CoolSolve gaps

None: the native file runs as extracted (after the unit conversion). The
model is a fixed-design teaching exercise, not an engine map.

## Related models

- CSL-0221 (`supercharged_engine_air_flow`): same volumetric-efficiency
  definition of the air flow, in a supercharged engine with intercooler.
- CSL-0244 (`engine_dynamometer_test`): the shaft/indicated/friction chain of
  the mechanical efficiency, from a dynamometer test.
- CSL-0278 (`vehicle_exhaust_emissions`): same TP7 session, exercise 1;
  emissions per km and per kWh of brake work from the fuel flow.

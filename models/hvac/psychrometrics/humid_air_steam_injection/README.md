# Humid air with steam injection (Cengel 14-75)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0194`

Teaching exercise. Humid air at 10 °C and 70 % relative humidity is heated
at constant humidity ratio and then humidified by saturated steam at 100 °C.
The air leaves at 20 °C and 60 % relative humidity. The model returns the
humidity ratio and the enthalpy per kg of dry air, the state between the
heater and the steam injection, the steam mass flow and the heater power.

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Psychrometrics |
| **Fluids** | AirH2O, Water |
| **Size** | 21 equations (largest block: 1) |
| **Source** | thermo_models, `thermo_kuleuven/exercices/14-75.EES` (Cengel exercise 14-75) |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@91d2b56 — verified against the EES stored solution |

## Problem statement

Humid air at 10 °C and 70 % relative humidity, flowing at the rate written
`35/60` and at 1.013×10⁵ Pa, receives a steam injection. Saturated steam at
100 °C is the injected fluid. The outlet is at 20 °C and 60 % relative
humidity. The exercise finds the humidity ratio, the enthalpy and the outlet
state per kg of dry air, together with the steam mass flow and the heater
power for that volume flow.

The original keeps two book values, a heater power of 391 kJ/min and a steam
flow of 0.147 kg/min, labelled as the comparison at 0.95 bar. The solved
pressure stays 1.013 bar.

## Model

State 1 is the inlet. The heater raises the enthalpy from `h_1` to `h_2` at
constant humidity ratio (`omega_2 = omega_1`). Saturated steam at 100 °C is
then injected, and the outlet (state 3) is fixed by temperature and relative
humidity. Per kg of dry air the balances written in the file are

$$\dot m_w = \dot m_a\,(\omega_3 - \omega_1)$$

$$\dot m_a h_3 = \dot m_a h_2 + \dot m_w h_{w,2}$$

$$\dot Q_\mathrm{heater} = \dot m_a\,(h_2 - h_1)$$

Humid-air properties use `AirH2O` (enthalpy, density, humidity ratio,
temperature, relative humidity). The steam enthalpy is `enthalpy(Water, x=1, T=100)`.
The original writes both fluid names in lower case; they are the same fluids.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_1` inlet temperature | 10 °C | `omega_1` inlet humidity ratio | 0.00534543 kg/kg |
| `RH_1` inlet relative humidity | 0.70 | `h_1` inlet enthalpy | 23.520 kJ/kg dry air |
| `V_dot_1` inlet volume flow | 35/60 m³/s | `omega_3` outlet humidity ratio | 0.00877520 kg/kg |
| `p` pressure | 1.013×10⁵ Pa | `h_3` outlet enthalpy | 42.381 kJ/kg dry air |
| `T_3` outlet temperature | 20 °C | `T_2` temperature at point 2 | 19.531 °C |
| `RH_3` outlet relative humidity | 0.60 | `M_dot_w` / `M_dot_a` steam per kg dry air | 0.00342978 kg/kg |
| | | `Q_dot_heater` heater power | 6984 W |

## How to run

Open `humid_air_steam_injection.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./humid_air_steam_injection.eescode
```

The system is square and fully explicit (21 blocks of size 1). It converges
in 4 iterations from the stored EES values in
`humid_air_steam_injection.initials`, and in 4 iterations with that file
removed. There is one solution; the initials are the stored EES values and
are not required to select a root.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `omega_1` inlet humidity ratio | 0.00534543 | 0.00532308 kg/kg dry air |
| `h_1` inlet enthalpy | 23520.3 | 23449.2 J/kg dry air |
| `rho_1` inlet density | 1.23637 | 1.24392 kg/m³ |
| `omega_3` outlet humidity ratio | 0.00877520 | 0.00873716 kg/kg dry air |
| `h_3` outlet enthalpy | 42380.8 | 42255.4 J/kg dry air |
| `T_2` temperature at point 2 | 19.5312 | 19.5368 °C |
| `RH_2` relative humidity at point 2 | 0.378341 | 0.378256 |
| `h_2` enthalpy at point 2 | 33204.2 | 33120.2 J/kg dry air |
| `M_dot_a` dry-air mass flow | 0.721216 | 0.725619 kg/s |
| `M_dot_w` steam mass flow | 0.00247361 | 0.00247732 kg/s |
| Steam per kg of dry air | 0.00342978 | 0.00341408 kg/kg |
| `Q_dot_heater` heater power | 6984.18 | 7017.49 W |
| `h_w_2` steam enthalpy | 2.675570×10⁶ | 2.675726×10⁶ J/kg |

The outlet temperature `T_3` is an input, 20 °C, and it matches the stored
solution. The temperature the model solves is `T_2`.

The book comparison constants stored in the file are
`Q_dot_heater_book` = 6516.67 W (391 kJ/min) and `M_dot_w_book` = 0.00245 kg/s
(0.147 kg/min). The original labels them as the values at 0.95 bar. They are
not the solution at the 1.013 bar of this run.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): CoolSolve has no
     psychrometric chart yet (CS-FEAT-PSYCHRO), so the figure of this humid-air model is
     a parametric sweep (roadmap decision D7), e.g. outlet humidity ratio `omega_3` and
     heater power `Q_dot_heater` against the outlet temperature `T_3`
     (CoolSolve GUI, Parametric tab, 1D plot), saved as
     figures/humid_air_steam_injection_t3.png -->

## Verification

Reference: the solution stored in `14-75.EES` (EES X9.920, 21 variables),
compared with `compare_solution.py` with no unit rescaling (the file is
already `SI MASS DEG PA C J`).

Summary line, quoted exactly:

`21 common variables, 10 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The maximum relative difference over all 21 common variables is 6.07e-03, on
`rho_1` and on `M_dot_a` (the tool prints 6.07e-03; the exact value is
6.068×10⁻³). The same solution, and the same ten differences, is obtained
with and without `.initials`.

The ten differences above rtol 0.001 come from the CoolProp humid-air
formulation against the EES one. Five of them are property calls; the other
five copy those calls through the balances.

Property calls:

| Variable | Relative difference | Call |
|---|---:|---|
| `rho_1` | 6.07e-03 | `density(AirH2O)` at 10 °C, 70 % RH |
| `omega_3` | 4.34e-03 | `humrat` at 20 °C, 60 % RH |
| `omega_1` | 4.18e-03 | `humrat` at 10 °C, 70 % RH |
| `h_1` | 3.02e-03 | `enthalpy` at state 1 |
| `h_3` | 2.96e-03 | `enthalpy` at state 3 |

`density(AirH2O)` in this binary equals `1/volume(AirH2O)` at the same state
(both 1.23637 kg/m³). It does not return 1×10⁴. `CS-BUG-HUMIDAIR-PROPS` is
fixed in commit 17e9bcc, which is contained in the binary commit 91d2b56, so
the native file is not blocked and no variant is shipped.

Quantities that repeat a property difference:

- `omega_2` is set equal to `omega_1`, so it carries the same 4.18e-03.
- `M_dot_a = V_dot_1*rho_1`. `V_dot_1` agrees, so `M_dot_a` carries the same
  6.07e-03 as `rho_1`.
- `M_dot_w = M_dot_a*(omega_3-omega_1)` differs by 1.50e-03. The CoolProp
  humidity rise is 0.00342978 kg/kg against 0.00341408 kg/kg in EES, and that
  increase partly offsets the lower dry-air flow.
- `h_2` is fixed by `h_3 - (omega_3-omega_1)*h_w_2` and differs by 2.53e-03.
  `h_w_2` itself, saturated steam at 100 °C, differs by only 5.82e-05.
- `Q_dot_heater = M_dot_a*(h_2-h_1)` differs by 4.75e-03, the lower dry-air
  flow combined with a slightly larger enthalpy rise.

`T_2` (2.87e-04) and `RH_2` (2.26e-04) stay inside rtol 0.001. The inputs,
`h_w_2` and the two book constants agree more closely still.

## Source and attribution

The equation window names no person. The inventory attributes the KU Leuven
course to S. Quoilin, so `authors` is `["S. Quoilin"]`. The EES licence tag
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}` is
the licence holder, not an author. Cengel is the textbook of exercise 14-75,
not an author of the file.

Source file: `~/Nextcloud/thermo_models/thermo_kuleuven/exercices/14-75.EES`
(candidate TM-0353). The file is not copied into the library.

## Conversion log

- **2026-10-15 — import**: extracted with `tools/ees_extract.py` (EES X9.920,
  plain text, 21 variables, no tables, no warnings). Unit system
  `SI MASS DEG PA C J`; `$UnitSystem` deleted; no value was rescaled.
  The equation window is already square (21 equations, 21 variables), so no
  Diagram-window input was restored. Comments translated to trailing English
  notes with SI units; the equations are unchanged. Fluid tokens stay
  `airh2o` and `water`.
- **Level**: 21 equations → 0; largest block 1 → 0; no function, procedure,
  array or `DUPLICATE` → 0; not multi-zone or discretised → 0; no
  semi-empirical, off-design, part-load or dynamic physics → 0; converges in
  4 iterations with or without initials, no `coolsolve.conf` → 0. Score 0 →
  level 1.

## Limitations and CoolSolve gaps

The book comparison is at 0.95 bar and the model is solved at 1.013 bar, as
the original states. Humid-air properties differ from the EES stored values
by a few tenths of a percent (CoolProp against EES); see *Verification*.

`density(AirH2O)` feeds `M_dot_a`. In this binary it returns the dry-air
density `1/volume(AirH2O)`, so `CS-BUG-HUMIDAIR-PROPS` does not block the
model. No CoolSolve gap is listed in `missing_features`.

## Related models

None. No other library model was identified as this same exercise.

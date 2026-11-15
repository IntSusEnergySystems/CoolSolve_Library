# Isenthalpic throttle with kinetic energy (R134a)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0345`

Outlet state of a refrigerant throttle: the stagnation enthalpy is conserved and
the mass flow rate is the same in the inlet and in the outlet section of equal
area. The model returns the outlet temperature, enthalpy, entropy, specific
volume and velocity of an R134a stream expanded from 1000 kPa to 100 kPa, and
the mass flow rate of the throttle.

| | |
|---|---|
| **Category** | Other components › Pipes, valves and flow meters |
| **Fluids** | R134a (main file), R1234yf (variant) |
| **Size** | 16 equations (largest block: 4) |
| **Source** | `~/Nextcloud/thermo_models/EES_library/Throttle.EES` (EES X9.067); MIT text mirror: <https://fchartsoftware.com/ees/examples/throttle.ees> |
| **Authors** | S.A. Klein (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@cc582a6 — verified (see *Verification*) |

## Problem statement

A refrigerant throttle (expansion valve) drops the pressure of a refrigerant
without any work and, to a first approximation, without any heat transfer. The
outlet state is then fixed by the energy balance of the device. The original
EES example asks for the outlet state of an R134a throttle: the inlet state and
the inlet velocity are given, the outlet pressure is imposed, and the outlet
temperature, velocity, specific volume and mass flow rate are computed. The
kinetic energy of the flow is kept, so the balance is written on the
*stagnation* enthalpy `h + Vel^2/2` and not on the enthalpy alone.

## Niche

The library had no isenthalpic throttle (thermodynamic expansion valve): the
models of `components/piping_valves` are flow meters and pressure-drop
elements (orifice plate, ball-valve authority, pipe and duct pressure drops,
nozzle discharge coefficients), and the closest component, `CSL-0310`
(isentropic nozzle of air), uses another closure (isentropic expansion with a
critical pressure, no mass-flow continuity). This model adds the isenthalpic
closure with the kinetic energy on a real refrigerant.

## Model

Governing equations (as in the original EES file):

- mass balance: `m_dot[2] = m_dot[1]`;
- continuity in the two sections of equal area `A`:
  `m_dot = A*Vel/v`, with `v` the specific volume of the fluid;
- steady-state energy balance on the stagnation enthalpy:
  `h[1] + Vel[1]^2/2 = h[2] + Vel[2]^2/2`;
- property calls `v = volume(fluid, T, P)` and `h = enthalpy(fluid, T, P)`.

The outlet state is therefore given by the outlet pressure, the inlet state and
the inlet velocity; the outlet velocity follows from the continuity equation.

| Variable | Meaning | Unit |
|---|---|---|
| `R$` | refrigerant | – |
| `T[1]`, `P[1]`, `Vel[1]` | inlet temperature, pressure, velocity | °C, Pa, m/s |
| `P[2]` | outlet pressure | Pa |
| `A` | cross-sectional area (inlet = outlet) | m² |
| `m_dot[1]`, `m_dot[2]` | mass flow rate | kg/s |
| `v[1]`, `v[2]` | specific volumes | m³/kg |
| `h[1]`, `h[2]` | specific enthalpies | J/kg |
| `s[1]`, `s[2]` | specific entropies (added, see the conversion log) | J/kg·K |
| `Vel[2]` | outlet velocity | m/s |

## How to run

```bash
coolsolve r134a_isenthalpic_throttle.eescode
```

No guess file is needed: the system is square (16 equations, 16 variables) and
solves in 6 iterations from the default guesses. The variant
`r134a_isenthalpic_throttle_r1234yf.eescode` (same equations, R1234yf instead
of R134a, i.e. the setting of the stored EES solution) is tested as
`CSL-0345:variant`.

## Results

Default operating point of the main file (R134a): `T[1]` = 50 °C,
`P[1]` = 1000 kPa, `Vel[1]` = 15 m/s, `P[2]` = 100 kPa, `A` = 0.005 m².

| Quantity | Value |
|---|---|
| `m_dot[1]` = `m_dot[2]` | 3.441 kg/s |
| `T[2]` | 17.60 °C |
| `h[1]` | 430 885 J/kg |
| `h[2]` | 418 289 J/kg |
| `s[1]` | 1748.2 J/kg·K |
| `s[2]` | 1880.5 J/kg·K |
| `v[1]` | 0.021796 m³/kg |
| `v[2]` | 0.231653 m³/kg |
| `Vel[2]` | 159.4 m/s |

The stagnation enthalpy is conserved: `h[1] + Vel[1]²/2` = 430 997 J/kg and
`h[2] + Vel[2]²/2` = 430 997 J/kg. The outlet is superheated vapour
(`T[2]` = 17.6 °C at 100 kPa, saturation temperature ≈ −26 °C).

The variant (R1234yf) gives `m_dot` = 3.937 kg/s, `T[2]` = 19.74 °C,
`h[2]` = 385 792 J/kg and `Vel[2]` = 164.3 m/s; see *Verification*.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-h or h-s diagram
     of the two throttle states, saved in figures/, e.g.
     ![T-h diagram of the throttle states](figures/r134a_isenthalpic_throttle_th.png) -->

## Verification

The stored solution of the source EES file is the state of its *Diagram window*
(radio button "HFO-1234yf", `P[1]` = 1000 kPa, `P[2]` = 100 kPa, `T[1]` = 50 °C,
`Vel[1]` = 15 m/s, `A` = 0.005 m²); the variant
`r134a_isenthalpic_throttle_r1234yf.eescode` reproduces that configuration and
is compared with the stored solution by `compare_solution.py`:

```
12 common variables, 8 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 4
```

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h[1]` | 400 917 | 399 170 | 4.4e-3 |
| `h[2]` | 387 379 | 385 792 | 4.1e-3 |
| `m_dot[1]`, `m_dot[2]` | 3.94231 | 3.93718 | 1.3e-3 |
| `T[2]` | 21.1958 °C | 19.7436 °C | 6.9e-2 |
| `v[1]` | 0.0190244 | 0.0190492 | 1.3e-3 |
| `v[2]` | 0.209557 | 0.208596 | 4.6e-3 |
| `Vel[2]` | 165.228 | 164.256 | 5.9e-3 |
| `A`, `P[1]`, `T[1]`, `Vel[1]` | — | — | 0 |

The maximum relative difference over the common variables is **6.9e-2** (`T[2]`).
It is not a modelling difference: the EES property tables of R1234yf and the
CoolProp HEOS equation of state differ by about 0.4 % on the enthalpy
(`h[1]`: 400 917 against 399 170 J/kg), and at the low outlet pressure
(100 kPa) a 0.4 % enthalpy difference is amplified into a 1.45 K difference of
the outlet temperature (`dh ≈ cp·dT` with `cp` ≈ 1000 J/kg·K). The main file
(R134a) uses the same equations, which are therefore verified by the variant;
its own results were checked with the energy and mass balances (values above).

## Source and attribution

`Throttle.EES` (EES X9.067), "Determine the outlet state of a throttle", from
the ULiège collection of EES examples: `~/Nextcloud/thermo_models/EES_library/Throttle.EES`.
The file is the EES-for-Engineers Chapter 15 example (EES V9.067, 2012-12-02,
author `klein` = S.A. Klein, F-Chart Software) and its MIT text mirror is
published by F-Chart at <https://fchartsoftware.com/ees/examples/throttle.ees>.
Licence: MIT (the licence tag of the file is `{$ID$ #0001: For use only by
S.A. Klein, F-Chart Software klein}`).

## Conversion log

- **2026-11-14 — import (`ees_extract.py`)**: the source file uses the EES unit
  system `SI MASS DEG KPA C J`; the model was converted by hand to the CoolSolve
  unit system (SI, °C, Pa, J): `P[1]` = 1000 kPa → `1000E3` [Pa] and `P[2]` =
  100 kPa → `100E3` [Pa]. No other quantity changes (velocities in m/s, area
  in m², enthalpies and entropies already in J/kg and J/kg·K).
- **2026-11-14 — Diagram window**: the inputs of the original file were inside
  an `$IFNOT DiagramWindow` block, i.e. they were the defaults used when the
  program runs without its Diagram window. The stored solution of the file
  corresponds to a run *with* the Diagram window: `P[1]` = 1000 kPa (instead
  of the 700 kPa of the `$IFNOT` block), `P[2]` = 100 kPa (instead of 300 kPa,
  value deduced from the stored specific volume and enthalpy of the outlet
  state) and the fluid R1234yf (the radio button "HFO-1234yf" of the Diagram
  window; the strings `HFC-134a//R$='R134a'` and `HFO-1234yf//R$='R1234yf'` are
  in the binary file). The Diagram-window values are copied into the equation
  file as plain assignments, the `$IFNOT`/`$ENDIF` directives are dropped, and
  the main file uses the default fluid of the original (`R134a`); the stored
  configuration is shipped as the variant
  `r134a_isenthalpic_throttle_r1234yf.eescode`. The `$ShowWindow`,
  `GetWindowInfo`, `$HideWindow` and `$TabStops` lines (window layout and plot
  formatting, no equation) are dropped.
- **2026-11-14 — unused variable**: the original file stores a scalar `m_dot`
  (value 1) that appears in no equation; it is not carried over. The arrays
  `m_dot[1]` and `m_dot[2]` of the original are kept.
- **2026-11-14 — state points**: `s[1]` and `s[2]` (specific entropies) are
  added at the end of the file, as the state points of the two throttle states
  for the thermodynamic diagram (workflow §3, step 5). They feed no other
  equation, so the results are unchanged.
- **2026-11-14 — variant**: `r134a_isenthalpic_throttle_r1234yf.eescode` is the
  same file with `R$ = 'R1234yf'`; it is the configuration of the stored EES
  solution and the reference of the verification above.
- **Level**: taxonomy §3 score 0 (16 equations < 50 → 0; largest block 4 ≤ 5
  → 0; no function, procedure or array → 0; no multi-zone model → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges with the default
  guesses → 0) → level 1.

## Limitations and CoolSolve gaps

The model describes an ideal adiabatic throttle of a constant cross-sectional
area: no heat transfer, no friction and no valve loss coefficient are
modelled, and the fluid is always a single phase at both ends (the state
2 (R134a, 17.6 °C, 100 kPa) of the default run is superheated vapour). The
stagnation enthalpy is conserved exactly; the enthalpy alone is not, because
the kinetic energy term is kept (`Vel[2]` = 159 m/s in the default run).

No CoolSolve gap blocks this model: `missing_features` is empty. The
Diagram-window objects of the source file (sliders, radio button, P-h plot)
are not imported; the policy for them is decided in card C-518 of the
roadmap, not here.

## Related models

None: the library holds no other throttle model. `CSL-0310` (isentropic
nozzle of air) is a different closure and is therefore not a related model.

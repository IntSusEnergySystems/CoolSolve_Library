# R134a heat pump with effectiveness heat exchangers

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0344`

An R134a heat-pump cycle in which the evaporator and the condenser are described by
effectiveness–capacitance rate products (Alpha, Beta in W/K) instead of fixed evaporation and
condensation temperatures: the cycle points adjust to the outdoor air temperature `T_amb` and to
the building air temperature `T_H` through heat-transfer relations, so the COP varies with the
weather. The compressor has a given isentropic efficiency (0.60) and a fixed suction volumetric
flow (4.3E-3 m³/s). The model returns the heat rates, the mass flow and the COP; the original EES
example sweeps `T_amb` from -15 to 15 °C in a parametric table and plots the COP (this official
EES example also illustrates array variables and the `$SUMROW` directive).

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Heat pump cycles |
| **Fluids** | R134a |
| **Size** | 32 equations (largest block: 15) |
| **Source** | EES example `capvst.ees` (`~/Nextcloud/thermo_models/EES_library/capvst.ees`; [fchartsoftware.com/ees/examples/capvst.ees](https://fchartsoftware.com/ees/examples/capvst.ees)) |
| **Authors** | S. A. Klein (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@cc582a6 — verified (see verification field) |

## Problem statement

As in the original example: a heat pump serves a building kept at `T_H = 20 °C` while the outdoor
temperature `T_amb` changes. The evaporator and condenser are heat exchangers characterised by
their effectiveness–capacitance rate products (`Alpha = 0.75 kW/K`, `Beta = 1.75 kW/K` in the
original, i.e. 750 W/K and 1750 W/K), so that:

- evaporator: `Q_evap = Alpha*(T_amb - T[1])` and the R134a energy balance;
- condenser: `Q_H = Beta*(T[3] - T_H)` and the R134a energy balance;

with `T[1]` the evaporating temperature (saturated vapour, `x[1] = 1`) and `T[3]` the condensing
temperature (saturated vapour at state 2, saturated liquid at state 3). The compressor is
isentropic (`ComEff = 0.60` accounts for the irreversibilities) and is sized by a fixed suction
volumetric flow `VolFlow = 4.3E-3 m³/s` (`VolFlow = m_dot*volume(R134a,T=T[1],x=x[1])`). The
expansion valve is isenthalpic. `COP = abs(Q_H/W_c)` uses the original sign convention (the
compressor power is negative).

## Model

Steady-state algebraic system, 32 equations, 32 unknowns (square), largest block 15 (the coupled
exchanger/compressor loop that floats `T[1]` and `T[3]`). Inputs: `T_amb` (here 15 °C, the run of
the stored EES solution; the original parametric table sweeps -15 to 15 °C in steps of 5 K).
Given: `T_H = 20 °C`, `Alpha`, `Beta`, `VolFlow`, `ComEff`. Outputs: `COP`, `Q_H`, `Q_evap`,
`m_dot`, `W_c`, and the state points `P[i]`, `h[i]`, `T[i]`, `s[i]`.

## How to run

```
coolsolve ./r134a_heat_pump_effectiveness.eescode
```

The default run is `T_amb = 15 °C` (the file's stored EES solution). To reproduce the sweep of the
original parametric table, change `T_amb` (e.g. 0 °C or -15 °C, see Verification) or use the GUI
parametric study. Guesses in `.initials` come from the stored EES solution, converted to SI
(pressures, enthalpies, entropies, powers ×1000).

## Results

Default run (`T_amb = 15 °C`), compared with the stored EES solution:

| Variable | EES (converted) | CoolSolve |
|---|---:|---:|
| COP | 6.574 | 6.574 |
| Q_H [W] | 12 298 | 12 298 |
| Q_evap [W] | 10 427 | 10 427 |
| m_dot [kg/s] | 0.06443 | 0.06443 |
| T[1] (evaporation) [°C] | 1.097 | 1.096 |
| T[3] (condensation) [°C] | 27.03 | 27.03 |
| P[2]/P[1] (pressure ratio) | 2.32 | 2.32 |

COP rises from 3.80 at `T_amb = -15 °C` to 6.57 at `T_amb = +15 °C`, as in the original parametric
table. The compression does raise the pressure (P[1] = 305 kPa → P[2] = 707 kPa at `T_amb = 15 °C`)
and `T[3] > T_H`, `T[1] < T_amb`, as the effectiveness relations require.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/r134a_heat_pump_effectiveness_ph.png)  + one-line caption -->

## Verification

Compared with the solution stored in the EES file (last run, `T_amb = 15 °C`,
`reference` extraction of `~/Nextcloud/thermo_models/EES_library/capvst.ees`) and with run 1 of
its parametric table (`T_amb = -15 °C`). The absolute enthalpies and entropies of EES carry the
ASHRAE reference state while CoolSolve (CoolProp) uses the IIR one; after subtracting the
documented offsets (CoolProp − EES = +148.1 kJ/kg on h, +0.796 kJ/kg-K on s, `ees_import.md` §11)
`compare_solution.py` reports, for the stored solution:

```
27 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 5
| T[1] | 1.09708 | 1.09568 | 1.28e-03 | **DIFF** |
```

Without the shift the comparison shows 6.24e-01 on the absolute `h`/`s` — the reference-state
offset, not a model difference. The remaining 1.28e-03 on `T[1]` (0.13 %) is a property difference
between EES and CoolProp near saturation, amplified by the small `T_amb - T[1]` difference; it is
within the 0.5 % tolerance expected for different fluid formulations. For the parametric row
(`T_amb = -15 °C`, checked by hand, the table stores no units: `Q_H` converted kW → W):
COP 5.41e-05, `m_dot` 2.61e-04, `Q_H` 3.68e-04 relative difference.

## Source and attribution

Official EES example `capvst.ees`, © S. A. Klein / F-Chart Software, distributed under the MIT
licence (the copy in the ULiège collection `~/Nextcloud/thermo_models/EES_library/capvst.ees`,
EES 9.227, was used for the stored solution and the parametric table; the public text version at
fchartsoftware.com differs only by a `$IfNot ParametricTable` default `T_amb = 0 °C`, absent from
the binary copy). No personal data.

## Conversion log

- **2026-11-14 — import**: `ees_extract.py` (EES 9.227, decimal comma → dots, `;` → `,` in
  argument lists); unit system `SI MASS DEG KPA C KJ` converted by hand to SI-°C-Pa-J
  (`ees_import.md` §6): `Alpha = 750 [W/K]` (0.75 kW/C), `Beta = 1750 [W/K]` (1.75 kW/C); all
  other equations are homogeneous (kW & kJ/kg → W & J/kg) and unchanged; `.initials` converted
  (pressures, enthalpies, entropies, powers ×1000); comments translated; licence tag
  `{$ID$…}` removed by the extractor.
- **2026-11-14 — inputs restored**: in the binary copy `T_amb` is defined only by the parametric
  table (7 runs, -15 to 15 °C); the default run is set in the equations as `T_amb = 15` (the run
  of the stored solution), following `ees_import.md` §8. The public text version guards
  `T_amb = 0` behind `$IfNot ParametricTable`; that block is not present in the binary copy.
- **2026-11-14 — curation**: trailing `:` after `W_c_ID=-(h_ID[2]-h[1])*m_dot` (dead punctuation
  of the original) removed; `$TabStops` and `$SUMROW ON` kept (accepted by CoolSolve, display-only
  directives); a post-processing block `T[2]`, `T[4]`, `s[2]`, `s[3]`, `s[4]` added for the
  thermodynamic diagrams (no effect on the results); `P[1]`…`P[4]`, `h[1]`…`h[4]`, `s[1]`,
  `T[1]`, `T[3]` are already arrays of the original.
- **2026-11-14 — niche**: the library had no cycle whose evaporator AND condenser are
  effectiveness–capacitance exchangers on a floating condensation/evaporation temperature with a
  volumetric-flow-sized compressor and COP as a function of outdoor temperature (equations diffed
  against the 6 models of `heat_pump_cycles` and the 6 models of `refrigeration_cycles`).
- **Level**: equations 32 (<50 → 0); largest block 15 (6–30 → 1); arrays present (→ 1); 4 coupled
  components (→ 1); exchangers floating with the outdoor temperature, part-load-like behaviour
  (→ 1); no curated guesses needed (→ 0): score 4 → level 3, moved down to 2 (−1): short
  pedagogical EES example, one equation per component, converges directly from the stored guesses.

## Limitations and CoolSolve gaps

None: the model runs as extracted (after the unit conversion). The absolute `h`/`s` depend on the
property reference state (ASHRAE vs IIR, see Verification).

## Related models

- CSL-0001 (refrigeration cycle with a simple compressor model): same cycle at a different level
  of detail — fixed evaporation/condensation temperatures, compressor with clearance volume and
  loss model.
- CSL-0015 (basic vapour-compression refrigeration cycle, R134a): same cycle at a different level
  of detail — fixed temperatures, isentropic efficiency only.

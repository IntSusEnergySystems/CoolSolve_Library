# Refrigeration cycle with a simple compressor model

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0001`

A vapour-compression refrigeration cycle driven by a reciprocating compressor
whose performance is described by two classic laws: a volumetric efficiency
due to the clearance volume, and an electrical power made of constant losses
plus losses proportional to the isentropic power. The model compares three
refrigerants (R22, R134a, propane) for the same compressor and temperature
levels.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R22 (default), R134a, Propane |
| **Size** | 48 equations, all explicit (largest block: 1): 32 for the model, 16 for the diagram state points |
| **Source** | ULiège — course *Machines et systèmes thermiques*, exercise session 1, exercise 3 (EES file `MSTh-SB-R1-Ex3.EES`) |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) — exercise of the course *Machines et systèmes thermiques* |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against EES (see *Verification*) |

## Problem statement

A reciprocating compressor has a swept volume flow rate of 0.040 m³/s, a
clearance factor of 6 %, constant electromechanical losses of 3400 W and a
loss factor α = 0.30 (losses proportional to the isentropic power). It runs a
refrigeration cycle with an evaporation temperature of 0 °C, a condensation
temperature of 40 °C, 8 K of superheating at the evaporator outlet and 5 K of
subcooling at the condenser outlet. Determine the refrigerant flow rate, the
cooling capacity, the power consumption and the COP with R22, R134a and
propane.

## Model

Compressor (supply state *su* = evaporator outlet, exhaust state *ex*):

- volumetric efficiency: $\varepsilon_v = \dot V_{su}/\dot V_s = 1 - C\,(r_v - 1)$
  with $r_v = v_{su}/v_{ex,s}$ the volume ratio of the isentropic compression;
- refrigerant flow rate: $\dot V_{su} = \dot m_r\, v_{su}$;
- power: $\dot W = \dot W_{loss,0} + (1+\alpha)\,\dot m_r\,(h_{ex,s} - h_{su})$.

Cycle: saturation pressures at $T_{ev}$ and $T_{cd}$, isenthalpic expansion,
pressure drops neglected, $\dot Q_{ev} = \dot m_r (h_1 - h_4)$,
$COP = \dot Q_{ev}/\dot W$. The subcooled-liquid enthalpy is evaluated on the
saturation curve at $T_3 = T_{cd} - \Delta T_{sc}$.

| Inputs | Value | Outputs (R22) | Value |
|---|---|---|---|
| `V_dot_s` swept volume flow | 0.04 m³/s | `M_dot_r` refrigerant flow | 0.729 kg/s |
| `C` clearance factor | 0.06 | `epsilon_v` volumetric efficiency | 0.895 |
| `W_dot_loss_0` constant losses | 3400 W | `Q_dot_ev` cooling capacity | 122.3 kW |
| `alpha` loss factor | 0.3 | `W_dot` power consumption | 31.1 kW |
| `T_ev` / `T_cd` | 0 / 40 °C | `COP` | 3.93 |
| `DELTAT_oh` / `DELTAT_sc` | 8 / 5 K | | |

## How to run

Open `refrigeration_cycle_simple_compressor.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./refrigeration_cycle_simple_compressor.eescode
```

Change `fluid$` to `'R134a'` or `'Propane'` to reproduce the fluid comparison.

## Results

| Fluid | P_ev [bar] | P_cd [bar] | ṁ [kg/s] | ε_v [-] | Q̇_ev [kW] | Ẇ [kW] | COP [-] |
|---|---:|---:|---:|---:|---:|---:|---:|
| R22 | 4.98 | 15.34 | 0.729 | 0.895 | 122.3 | 31.10 | 3.93 |
| R134a | 2.93 | 10.17 | 0.477 | 0.860 | 74.7 | 20.15 | 3.71 |
| Propane | 4.74 | 13.69 | 0.354 | 0.892 | 104.9 | 27.28 | 3.85 |

With the same compressor, R22 gives the largest capacity (highest vapour
density at the compressor supply) and the best COP; R134a, with a lower
evaporation pressure, loses 39 % of capacity.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 evaporator outlet, 2 isentropic
compressor exhaust, 3 condenser outlet, 4 evaporator inlet) give the cycle on
the P-h or T-s diagram (CoolSolve *Diagram* tab, *Overlay array path*, *Close
cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the R22 cycle,
     figures/refrigeration_cycle_simple_compressor_ph.png -->

## Verification

1. **Faithful import vs EES.** The original equations were solved unchanged
   (with `fluid$` set for each run) and compared with the parametric table
   stored in the original EES file:

   | Fluid | COP EES / CoolSolve | Q̇_ev [W] EES / CoolSolve | Ẇ [W] EES / CoolSolve | max. deviation |
   |---|---|---|---|---:|
   | R22 | 5.218 / 5.264 | 163 575 / 165 952 | 31 347 / 31 525 | 1.4 % |
   | R134a | 4.981 / 4.980 | 105 664 / 105 709 | 21 212 / 21 225 | 0.06 % |
   | Propane | 5.102 / 5.107 | 139 709 / 140 117 | 27 382 / 27 438 | 0.3 % |

   R134a and propane agree within the property tolerance. The R22 deviation
   is most likely due to differences between the R22 formulations of EES 7.4
   and CoolProp; it was not investigated further.
2. **Corrected model** (see *Conversion log*) vs the independent CoolSolve
   example `compressor_refrigeration_simple.eescode`: COP 3.9336 / 3.9343 (R22)
   and 3.7089 / 3.7092 (R134a), i.e. < 0.02 %.

## Source and attribution

Exercise solution by **Stéphane Bertagnolio** (ULiège Thermodynamics
Laboratory) for the course *Machines et systèmes thermiques* (exercise
session 1, exercise 3). The author was identified from the folder name `SB`;
the file itself names no author.

Source file (EES 7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 01/SB/MSTh-SB-R1-Ex3.EES`
(inventory candidate `TM-0018`).

## Conversion log

- **2026-10-04 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-C-Pa-J; the EES licence tag was removed; the file had
  been last run from its parametric table (stored values = −9999), whose
  string column `fluid$` was the only definition of the refrigerant →
  `fluid$ = 'R22'` added as the default run. Comments translated to English and
  standard header added. Faithful import verified (see above).
- **2026-10-04 — correction of the original model.** The original evaluated
  the superheated compressor supply state with `x=1` at `T_su`, i.e. as
  saturated vapour at 8 °C (a pressure 29 % higher than `P_ev` for R22). This
  overestimates the supply density, hence the flow rate (+38 %) and the COP
  (5.26 instead of 3.93 for R22, implausible for a 0/40 °C cycle with losses).
  `v_su`, `h_su`, `s_su` and `h_1` are now evaluated at `(T, P_ev)`, as in the
  CoolSolve example of the same exercise.
- The CoolSolve example `compressor_refrigeration_simple.eescode` (same
  exercise, R22 and R134a computed side by side) is superseded by this model in
  the library; it remains in the CoolSolve repository as a test case.
- **2026-10-04 — diagram support**: block of 16 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) added at the end of the model for
  the CoolSolve diagrams; the results of the model are unchanged.

## Limitations and CoolSolve gaps

- The fluid comparison of the original EES file is a parametric table with a
  string column; CoolSolve parametric studies cannot sweep a string variable,
  so each fluid is run by editing `fluid$` (gap `CS-GAP-PARAMETRIC`, not
  blocking).
- The subcooled liquid is approximated by saturated liquid at `T_3`
  (negligible pressure effect).

## Related models

- `CSL-0007` *scroll_compressor_semi_empirical*: same component at the
  semi-empirical level of detail.
- `CSL-0013` *heat_pump_basic_tespy*, `CSL-0015` *refrigeration_cycle_basic_r134a*:
  basic R134a vapour-compression cycles (constant isentropic efficiency).
- `CSL-0022` *refrigeration_compressor_identification*: same SB solution
  series (repetition 1, exercise 2) on R22, identification of a
  clearance-volume/loss-factor compressor model from two points.
- See also the CoolSolve example `compressor_refrigeration_simple.eescode`.
- `CSL-0054` *heat_pump_r410a_air_evaporator*: same category; heat pump on
  the zeotropic R410A with an air-side evaporator balance (the useful effect is
  here at the condenser).
- `CSL-0061` *refrigerator_freezer_r134a*: same fluid family (R134a) and
  same course; a fridge-freezer cycle with two evaporators and two expansion
  valves, sized from a required refrigeration capacity.
- `CSL-0077` *aircooled_chiller_refsim*: the same compressor concept
  (volumetric efficiency, constant losses, refrigerant heat transfers
  represented by a fictitious wall) in a full air-cooled water chiller of the
  ULiège model bank.
- `CSL-0156` *refrigeration_screw_compressor_r22*: the same R22 cycle closed by the
  ULiège reference screw compressor (internal leakage nozzle/diffuser, sliding-valve
  part load) — the detailed component counterpart of this simple compressor model.
- `CSL-0167` *reciprocating_polynomial_r22*: the same R22 cycle closed by the ULiège
  reference reciprocating compressor (six-step semi-empirical model with clearance
  re-expansion and motor slip) — the detailed component counterpart of this simple
  compressor model.

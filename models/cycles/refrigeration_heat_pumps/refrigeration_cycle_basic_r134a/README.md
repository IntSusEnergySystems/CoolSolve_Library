# Basic vapour-compression refrigeration cycle (R134a)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0015`

A R134a refrigeration machine operating between a condensation temperature
of 20 °C and an evaporation temperature of −10 °C, with 6 K of subcooling at
the condenser outlet and 2 K of superheat at the evaporator outlet. The
compressor is described by an isentropic efficiency of 0.75 and its drive
motor by an efficiency of 0.80. For a prescribed cooling capacity of 50 kW,
the model determines the refrigerant mass flow rate, the compressor power
consumption and the COP.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R134a |
| **Size** | 47 equations, all explicit (largest block: 1): 39 for the model, 8 for the diagram state points |
| **Source** | ULiège exercise (répétition 8, exercise 1) — CoolSolve example `refrigeration1` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs; import verified against the solution stored in the original EES file |

## Problem statement

A R134a refrigeration machine operates between 20 °C at the condenser and
−10 °C at the evaporator. The fluid is subcooled by 6 K at the condenser
outlet and superheated by 2 K at the evaporator outlet. The isentropic
efficiency of the compressor is 0.75 and the efficiency of the electric
drive motor is 0.80. Knowing that the machine must produce 50 kW of cooling
effect, determine the refrigerant mass flow rate, the power absorbed by the
compressor and the COP of the machine.

## Model

Four state points (1: compressor inlet, 2: compressor outlet = condenser
inlet, 3: condenser outlet, 4: evaporator inlet):

- saturation pressures at $T_{ev}$ and $T_{cond}$ (phase-change plateau, any
  quality in [0, 1] gives the same pressure);
- compressor: isentropic efficiency
  $\varepsilon_{s,cp} = w_s/w$ with $w_s = h_{2,s} - h_1$ and
  $w = h_2 - h_1$, giving $h_2$; outlet temperature from $(P_2, h_2)$;
- condenser outlet: subcooled state $(P_3, T_3)$ with
  $T_3 = T_{cond} - \Delta T_{sc}$;
- evaporator inlet: isenthalpic expansion $h_4 = h_3$, quality $x_4$ from
  $(P_4, h_4)$; pressure drops neglected ($P_1 = P_4 = P_{ev}$,
  $P_2 = P_3 = P_{cd}$);
- mass flow rate from the prescribed capacity
  $\dot Q_{41} = \dot m_r (h_1 - h_4)$;
- electrical power $\dot W_{cp} = \dot m_r (h_2 - h_1)/\eta_m$;
  $COP = \dot Q_{41}/\dot W_{cp}$.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_cond` / `T_ev` | 20 / −10 °C | `M_dot_r` refrigerant flow | 0.2853 kg/s |
| `DELTA_T_sc` / `DELTA_T_oh` | 6 / 2 K | `W_dot_cp` electrical power | 10.38 kW |
| `epsilon_s_cp` isentropic eff. | 0.75 | `COP` | 4.817 |
| `eta_m` motor efficiency | 0.80 | `P_ev` / `P_cd` | 2.006 / 5.717 bar |
| `Q_dot_41` cooling capacity | 50 kW | `T_2` / `x_4` | 34.0 °C / 0.157 |

## How to run

Open `refrigeration_cycle_basic_r134a.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./refrigeration_cycle_basic_r134a.eescode
```

The model is fully explicit (largest block: 1) and converges from the
default guesses in 25 iterations; no `.initials` file is needed.

## Results

| Quantity | Value |
|---|---:|
| `P_ev` evaporation pressure | 200.6 kPa |
| `P_cd` condensation pressure | 571.7 kPa |
| `M_dot_r` refrigerant mass flow | 0.2853 kg/s |
| `w_41` specific cooling effect | 175.3 kJ/kg |
| `w_12` specific compression work | 29.11 kJ/kg |
| `W_dot_12` shaft power | 8.303 kW |
| `W_dot_cp` electrical power | 10.38 kW |
| `T_2` compressor outlet | 34.0 °C |
| `x_4` evaporator-inlet quality | 0.157 |
| `COP` | 4.817 |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 evaporator outlet, 2
compressor exhaust, 3 condenser outlet, 4 evaporator inlet) give the cycle on
the P-h or T-s diagram (CoolSolve *Diagram* tab, *Overlay array path*, *Close
cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle,
     figures/refrigeration_cycle_basic_r134a_ph.png -->

## Verification

Faithful import vs the solution stored in the original EES file
(`EES_ok/refrigeration1.EES`, EES 9.920). All 47 equations satisfied
(max. relative residual 2.5e-16). Of the 39 EES variables:

- 29 agree within 0.07 % (largest deviations: saturation pressures 0.06–0.07 %,
  EES vs CoolProp R134a saturation curves);
- the 9 absolute enthalpies and the inlet entropy differ by constant
  reference-state offsets between EES and CoolProp R134a (148.15 kJ/kg on all
  enthalpies, 795.69 J/(kg·K) on `s_1`); all their differences and every
  derived result agree:

| Quantity | EES | CoolSolve | rel. diff. |
|---|---:|---:|---:|
| `M_dot_r` [kg/s] | 0.285292 | 0.285282 | −3.3e-05 |
| `w_41` [J/kg] | 175259 | 175265 | 3.3e-05 |
| `w_12` [J/kg] | 29102.4 | 29105.9 | 1.2e-04 |
| `W_dot_cp` [W] | 10378.3 | 10379.3 | 8.9e-05 |
| `COP` [-] | 4.81773 | 4.81730 | −8.9e-05 |
| `T_2` [°C] | 33.998 | 33.9978 | −5.2e-06 |
| `x_4` [-] | 0.157358 | 0.157355 | −2.2e-05 |

(EES also stores a stray scalar `h = 1` with no counterpart in the
equations — an extraction artifact of an array name, ignored.)

## Source and attribution

Exercise of the ULiège thermodynamics course (répétition 8, exercise 1). The
author was identified from the file header `VL050415` (V. Lemort, 2005-04-15);
the `{$ID$ … Jean Lebrun …}` tag is the EES licence of the laboratory, not the
author. The CoolSolve example `refrigeration1.eescode` (S. Quoilin) is the
English version of the same exercise.

Source files: CoolSolve `examples/refrigeration1.eescode` (inventory
candidate `CSX-038`) and its EES original `misc/EES_ok.zip`:
`EES_ok/refrigeration1.EES` (EES 9.920, comments in French, full stored
solution of 40 variables, no tables).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `refrigeration1.EES`): unit system already SI-°C-Pa-J (no conversion
  needed); EES licence tag (Jean Lebrun, the lab licence, not the author)
  and `{$PX$}` display tag removed; no tables, no external functions (only
  `pressure`, `enthalpy`, `entropy`, `temperature`, `quality`, all CoolSolve
  built-ins); full stored solution available. Faithful run of the raw
  extraction: all derived results identical to EES (see above).
- **2026-10-05 — curation**: standard header added, comments translated from
  French to English (the CoolSolve example's English comments say the same),
  section titles added, property calls upper-cased. No change to any equation
  or value: the library model and the CoolSolve example solve to the same
  values (COP 4.8173 both).
- **2026-10-05 — diagram support**: block of 8 post-processing equations
  (state arrays `T[i]`, `s[i]`; `P[i]`/`h[i]` were already in the original)
  added at the end of the model for the CoolSolve diagrams; the results of
  the model are unchanged (the example differs only by these arrays and the
  comments).
- The `thermodynamique appliquée` exercise `R08_E01_2022` (TM-0448 and its
  two copies TM-0531/TM-0549) is the same statement with 100 kW of cooling
  instead of 50 kW (kPa/kJ units, decimal comma): recorded as duplicates of
  this model (results scale linearly with the capacity).

## Limitations and CoolSolve gaps

- Subcooled and superheated states are evaluated directly at $(P, T)$; the
  saturation pressures use $x = 1$ on the phase-change plateau (any quality
  in [0, 1] gives the same pressure), as in the original.
- No CoolSolve gap: the model uses only built-in property functions.

## Related models

- `CSL-0001` (Refrigeration cycle with a simple compressor model): same
  category; a refrigeration cycle driven by a clearance-volume/loss-factor
  compressor model with a three-fluid comparison (R22, R134a, propane).
- `CSL-0013` (Heat pump basic TESPy): same category; TESPy tutorial heat
  pump translated to CoolSolve.
- `CSL-0019` (Simple ORC with imposed component performance): same
  category family (vapour cycle, imposed component performance).
- CoolSolve example `refrigeration1.eescode` (same exercise, kept in
  CoolSolve as a test case).

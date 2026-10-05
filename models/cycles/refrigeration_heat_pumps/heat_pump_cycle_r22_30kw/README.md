# R22 heat pump cycle delivering 30 kW

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0025`

A R22 heat pump delivering 30 kW of heating, operating between an
evaporation temperature of 8 °C and a condensation temperature of 60 °C,
with 10 K of subcooling at the condenser outlet and no superheat. The
compressor is described by an isentropic efficiency of 0.80. The heat
source is groundwater at 10 °C feeding the evaporator, whose
effectiveness is 1. For the prescribed heating capacity, the model
determines the COP, the refrigerant mass flow rate and the groundwater
flow rate extracted.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R22, Water (groundwater, constant properties) |
| **Size** | 55 equations, all explicit (largest block: 1): 39 for the model, 16 for the diagram state points |
| **Source** | ULiège exercise (répétition 8, exercise 3) — CoolSolve example `refrigeration2` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | main 2026-10-05 — runs; import verified against the solution stored in the original EES file |

## Problem statement

A heat pump must deliver 30 kW of heating. It works between an
evaporation temperature of 8 °C and a condensation temperature of 60 °C,
with 10 K of subcooling at the condenser outlet and no superheat at the
evaporator outlet; the refrigerant is R22. The secondary fluid of the
evaporator is groundwater at 10 °C, and the evaporator effectiveness is
taken as 1. Knowing that the isentropic efficiency of the compressor is
0.80, determine the COP of the machine, the refrigerant mass flow rate
and the groundwater flow rate extracted.

## Model

Four state points (1: compressor inlet, 2: compressor outlet = condenser
inlet, 3: condenser outlet, 4: evaporator inlet):

- saturation pressures at $T_{ev}$ and $T_{cond}$ (phase-change plateau, any
  quality in [0, 1] gives the same pressure);
- compressor inlet: saturated vapour at $P_{ev}$ ($x_1 = 1$, no superheat);
- compressor: isentropic efficiency
  $\varepsilon_{s,cp} = w_s/w$ with $w_s = h_{2,s} - h_1$ and
  $w = h_2 - h_1$, giving $h_2$; outlet temperature from $(P_2, h_2)$;
- condenser outlet: subcooled state $(P_3, T_3)$ with
  $T_3 = T_{cond} - \Delta T_{sc}$;
- evaporator inlet: isenthalpic expansion $h_4 = h_3$, quality $x_4$ from
  $(P_4, h_4)$; pressure drops neglected ($P_1 = P_4 = P_{ev}$,
  $P_2 = P_3 = P_{cd}$);
- mass flow rate from the prescribed heating capacity
  $\dot Q_{23} = \dot m_r (h_3 - h_2) = -30$ kW;
- compressor power $\dot W_{cp} = \dot m_r (h_2 - h_1)$ — the drive motor
  efficiency is commented out in the original, so this is the shaft power;
  $COP = -\dot Q_{23}/\dot W_{cp}$;
- groundwater side: $\dot Q_{41} = \dot m_r (h_1 - h_4)$ exchanged with
  $\dot m_w c_{p,w} (T_{w,su} - T_{w,ex})$, and
  $\varepsilon_{ev} = (T_{w,su} - T_{w,ex})/(T_{w,su} - T_{ev}) = 1$ gives
  $T_{w,ex} = T_{ev}$; the volume flow $\dot V_w$ is reported in m³/h.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_cond` / `T_ev` | 60 / 8 °C | `M_dot_r` refrigerant flow | 0.1608 kg/s |
| `DELTA_T_sc` / `DELTA_T_oh` | 10 / 0 K | `W_dot_cp` shaft power | 6.705 kW |
| `epsilon_s_cp` isentropic eff. | 0.80 | `COP` | 4.474 |
| `Q_dot_23` heating capacity | −30 kW | `P_ev` / `P_cd` | 6.409 / 24.27 bar |
| `T_w_su` groundwater supply | 10 °C | `T_2` / `x_4` | 89.8 °C / 0.270 |
| `epsilon_ev` evaporator eff. | 1 | `M_dot_w` / `V_dot_w` groundwater | 2.783 kg/s / 10.02 m³/h |

## How to run

Open `heat_pump_cycle_r22_30kw.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./heat_pump_cycle_r22_30kw.eescode
```

The model is fully explicit (largest block: 1) and converges from the
default guesses in 29 iterations; no `.initials` file is needed.

## Results

| Quantity | Value |
|---|---:|
| `P_ev` evaporation pressure | 640.9 kPa |
| `P_cd` condensation pressure | 2427.5 kPa |
| `M_dot_r` refrigerant mass flow | 0.1608 kg/s |
| `w_23` specific heat rejected | −186.6 kJ/kg |
| `w_12` specific compression work | 41.70 kJ/kg |
| `W_dot_12 = W_dot_cp` shaft power | 6.705 kW |
| `Q_dot_41` heat absorbed at the evaporator | 23.30 kW |
| `T_2` compressor outlet | 89.8 °C |
| `x_4` evaporator-inlet quality | 0.270 |
| `COP` | 4.474 |
| `M_dot_w` groundwater mass flow | 2.783 kg/s |
| `V_dot_w` groundwater volume flow | 10.02 m³/h |
| `T_w_ex` groundwater return (= `T_ev`) | 8.0 °C |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 compressor inlet, 2
compressor outlet = condenser inlet, 3 condenser outlet, 4 evaporator
inlet) give the cycle on the P-h or T-s diagram (CoolSolve *Diagram* tab,
*Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle,
     figures/heat_pump_cycle_r22_30kw_ph.png -->

## Verification

Faithful import vs the solution stored in the original EES file
(`EES_ok/refrigeration2.EES`, EES 7.210). All 39 model equations satisfied
(max. relative residual 9.6e-12). Of the 47 reference variables:

- all live model variables agree within 0.27 % (EES 7.210 vs CoolProp R22
  properties), largest deviations on the evaporator-inlet quality (0.27 %),
  the refrigerant flow rate and the specific heating effect (0.13 % each):

| Quantity | EES | CoolSolve | rel. diff. |
|---|---:|---:|---:|
| `M_dot_r` [kg/s] | 0.160977 | 0.160771 | 1.28e-03 |
| `w_23` [J/kg] | −186361 | −186601 | 1.28e-03 |
| `x_4` [-] | 0.270451 | 0.269723 | 2.69e-03 |
| `W_dot_cp` [W] | 6708.20 | 6704.69 | −5.24e-04 |
| `COP` [-] | 4.47214 | 4.47448 | 5.24e-04 |
| `T_2` [°C] | 89.7014 | 89.7887 | 9.73e-04 |
| `Q_dot_41` [W] | 23291.8 | 23295.3 | 1.51e-04 |
| `M_dot_w` [kg/s] | 2.78211 | 2.78253 | 1.51e-04 |
| `V_dot_w` [m³/h] | 10.0156 | 10.0171 | 1.51e-04 |

(`compare_solution.py`: 47 common variables, 10 differ with rtol=0.001;
only in EES: 2; only in CoolSolve: 8.)

- the stored `P[1..3]` and `h[1..4]` are stale leftovers: the P-h diagram
  block was commented out when EES last solved the file (only `P[4]`,
  coincidentally equal to `P_ev`, still matches) — ignored;
- (EES also stores a stray scalar `h = 1` with no counterpart in the
  equations — an extraction artifact of an array name, ignored — and the
  commented-out `eta_m`, which defines no variable.)

## Source and attribution

Exercise of the ULiège thermodynamics course (répétition 8, exercise 3).
The author was identified from the file header `VL050415` (V. Lemort,
2005-04-15); the `{$ID$ … Laboratoire de Thermodynamique, U. de Liege}`
tag is the EES licence of the laboratory, not the author. The CoolSolve
example `refrigeration2.eescode` (S. Quoilin) is the English version of
the same exercise: same 39 equations, only the comments differ.

Source files: CoolSolve `examples/refrigeration2.eescode` (inventory
candidate `CSX-039`) and its EES original `misc/EES_ok.zip`:
`EES_ok/refrigeration2.EES` (EES 7.210, comments in French, full stored
solution of 49 variables, no tables). No counterpart of this exercise was
found in the `thermo_models` collection (searched by title, fluid, values
and storage date): no `thermo_models` row is decided on by this card.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `refrigeration2.EES`): unit system already SI-°C-Pa-J (no conversion
  needed); EES licence tag (the lab licence, not the author) removed; no
  tables, no external functions (only `pressure`, `enthalpy`, `entropy`,
  `temperature`, `quality`, all CoolSolve built-ins); full stored solution
  available. Faithful run of the raw extraction: all derived results agree
  with EES within 0.27 % (see above).
- **2026-10-05 — curation**: standard header added, comments translated from
  French to English (the CoolSolve example's English comments say the same),
  section titles added, property calls upper-cased. The P-h diagram block
  (`P[i]`/`h[i]`), commented out in both the original and the example, was
  activated, and a block of 8 post-processing equations (state arrays
  `T[i]`, `s[i]`) was added at the end of the model for the CoolSolve
  diagrams; the results of the model are unchanged. The commented-out motor
  efficiency (`{eta_m = 0.8}`, `W_dot_cp = W_dot_12{/eta_m}`) is kept as in
  the original: `W_dot_cp` is the shaft power. The library model and the
  CoolSolve example solve to the same values (COP 4.4745 both).
- Level 1 (card L1): 55 equations, all explicit (largest block 1); arrays
  only for the diagram state points.

## Limitations and CoolSolve gaps

- The drive motor efficiency (`eta_m = 0.8`) is commented out in the
  original, so `W_dot_cp` is the shaft power, not the electrical power;
  kept faithful to the original.
- Subcooled and superheated states are evaluated directly at $(P, T)$; the
  saturation pressures use $x = 1$ on the phase-change plateau (any quality
  in [0, 1] gives the same pressure), as in the original.
- CoolSolve prints the hint *"PRESSURE(): fluid 'R22'. Did you mean
  'R22'?"* although the fluid name is already correct (same hint-table
  behaviour as registered bug `CS-BUG-FLUID-HINT-CO2`); the results are
  unaffected.
- No CoolSolve gap blocks this model: it uses only built-in property
  functions.

## Related models

- `CSL-0015` (Basic vapour-compression refrigeration cycle, R134a): same
  exercise series (répétition 8, exercise 1), same structure with the
  cooling capacity prescribed at the evaporator instead.
- `CSL-0001` (Refrigeration cycle with a simple compressor model): same
  category; a refrigeration cycle driven by a clearance-volume/loss-factor
  compressor model with a three-fluid comparison (R22, R134a, propane).
- `CSL-0013` (Heat pump basic TESPy): same category; TESPy tutorial heat
  pump translated to CoolSolve.
- CoolSolve example `refrigeration2.eescode` (same exercise, kept in
  CoolSolve as a test case).

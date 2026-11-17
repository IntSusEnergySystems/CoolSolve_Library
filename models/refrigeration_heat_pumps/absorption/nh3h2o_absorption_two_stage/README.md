# Two-stage ammonia-water absorption system with condensate precooling

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0352`

A two-stage (double-effect) NH3H2O absorption refrigeration cycle, solved as one
simultaneous system of 213 equations over the 29 state points of the diagram.
Desorber 1 (low temperature) is *not* heated externally: its driving heat is the
heat rejected internally by Absorber 2 and Rectifier 2. Desorber 2 receives the
external driving heat. The vapour generated in both desorbers is purified in
three rectifiers (R1, R2, R3) — Rectifier 2 rejects its heat to Desorber 1 — and
a condensate precooler (the refrigerant heat exchanger RHX) subcools the
condensed liquid with the cold evaporator outlet. Given the heat rejection
temperatures (absorber and condenser at 40 °C), the evaporator temperature
(−10 °C) and the design goals (rectified vapour x[9] = 0.99, concentration steps
DELTAx_1 = DELTAx_2 = 0.04), the model computes all state points, the component
heat rates and the COP of the system.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O |
| **Size** | 213 equations (largest block: 119) |
| **Source** | F-Chart EES example `ex10_1.ees` (EES-Community/ees-examples, Case_Study) |
| **Authors** | S. A. Klein (F-Chart Software); Example 10.1 of Herold, Radermacher & Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015 |
| **License** | MIT |
| **CoolSolve** | 0.4.0@00a4daa — blocked by CS-BUG-PROP-QLIMIT (native file); runnable variant compared with the stored solution (see Verification) |

## Problem statement

Example 10.1 of the book: *Performance of a two-stage absorption system with
condensate precooling. Two rectifiers are used in the second stage. Rectifier 2
heat is rejected to the low-temperature generator.* Inputs (as in the original):
m_dot[1] = 1 kg/s, eta_pump = 1, solution heat exchanger effectiveness
epsilon_shx = 0.8, condensate precooler effectiveness epsilon_cpc = 0.8,
T[1] = T[10] = 40 °C (absorber / condenser heat rejection), T[13] = −10 °C
(evaporator), saturated liquid at states 1, 4, 8, 10, 16, 19, 23, 28 and
saturated vapour at 7, 9, 22, 24, 27, evaporator outlet quality Q[13] = 0.88
(to limit the temperature glide), rectifier design goal x[9] = 0.99 and
concentration steps x[1] − x[4] = x[16] − x[19] = 0.04.

## Model

Each of the 29 states carries arrays m_dot[i], P[i], T[i], h[i], x[i], Q[i].
Components (mass, ammonia and energy balances, as in the original): Absorber 1
(with internal heat exchange between streams 15/29), Desorber 1, Rectifier R1,
Pump 1, expansion valves, Solution Heat Exchanger 1, mixing of streams 9/27
before the condenser, Condenser, Evaporator, refrigerant heat exchanger (RHX =
condensate precooler), Absorber 2, Desorber 2, Rectifiers R2 and R3, Pump 2,
Solution Heat Exchanger 2. Design goals written as equations in the original:
T[29] = T[6], T[16] = T[4], T[24] = T[16], T[22] = T[23], T[28] = T[24] and
T[7] = T[8] (equilibrium between the rectifier inlet vapour and outlet liquid),
Q_dot_des_1 = Q_dot_abs_2 + Q_dot_rect_2 (internal heat exchange). The solution
heat exchangers and the RHX use the `PROCEDURE shx` of the original: an
effectiveness model that takes the maximum possible heat transfer on both sides
and uses `Min()` — the smaller of the two heat rates, *not* an optimiser (it
parses in CoolSolve as it is).

Pressures are set by the saturation of the solution: P_low from the absorber 1
conditions (T[1], x[1], Q[1] = 0), P_high from the condenser conditions
(T[10], x[10], Q[10] = 0).

The state-point arrays P[i], T[i], h[i] (and m_dot[i], x[i], Q[i]) of the
original are kept; a post-processing block adds s[i] = ENTROPY(NH3H2O, P, x, h)
for the thermodynamic diagrams (no effect on the results).

## How to run

The **native file** `nh3h2o_absorption_two_stage.eescode` is the faithful
transcription of the example; it is **blocked** by CS-BUG-PROP-QLIMIT (state 25,
below). The **runnable variant** `nh3h2o_absorption_two_stage_coolsolve.eescode`
changes only the two property calls of state 25 (every change logged in the
conversion log; both forms are valid EES). Both files take their guesses from
`.initials` (values stored by EES, pressures and enthalpies converted to
Pa/J — 83 entries ×1000):

```bash
coolsolve ./nh3h2o_absorption_two_stage_coolsolve.eescode   # solves (49 iterations)
```

Tested as `CSL-0352:coolsolve` by `tools/test_models.py`; the blocked native
file is skipped.

## Results (runnable variant vs EES stored solution)

| Quantity | EES | CoolSolve (variant) | rel. diff as printed |
|---|---:|---:|---:|
| COP (with pump power) | 0.496153 | 0.479037 | 3.45e-02 |
| COP_c (without pump power) | 0.502086 | 0.484672 | 3.47e-02 |
| Q_dot_evap | 90.109 kW | 87.950 kW | 2.40e-02 |
| Q_dot_des_2 (driving heat) | 179.5 kW (implied from COP_c) | 181.46 kW | 1.11e-02 |
| P_low | 269.93 kPa | 267.21 kPa | 1.01e-02 |
| P_high | 1539.88 kPa | 1538.01 kPa | 1.22e-03 |
| m_dot[16] (loop 2 circulation) | 0.4787 kg/s | 0.4708 kg/s | 1.66e-02 |
| x[1] (strong solution, loop 1) | 0.38652 | 0.37495 | 2.99e-02 |
| x[19] (weak solution, loop 2) | 0.020811 | 0.0096591 | 5.36e-01 |
| T[9] (rectified vapour) | 76.64 °C | 76.09 °C | 7.14e-03 |
| T_glide (evaporator) | 1.57 K | 1.80 K | 1.28e-01 |
| checkQ (whole-cycle balance) | −2.3 mW | 1.6e-6 W | — |

The whole-cycle energy balance
(Q_dot_des_2 + Q_dot_evap + W_dot_p1 + W_dot_p2 = Q_dot_rect_1 + Q_dot_rect_3 +
Q_dot_cond + Q_dot_abs_1) closes to 1.6e-6 W on 271.5 kW (EES: −2.3 mW); the
Desorber 1 mass and ammonia balances (err_abs_mass1, err_absammonia_1) are
4.4e-16 and 6.8e-15.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/nh3h2o_absorption_two_stage_ph.png)  + one-line caption -->

## Verification

The runnable **variant** was solved in CoolSolve and compared with the EES
stored solution (`compare_solution.py … --ees-units`, 241 common variables;
the native file cannot run, see below). COP, pressures, mass flows and most
temperatures agree within a few percent; the deviations are explained by the
NH3H2O **property backend**, evidenced by identical property calls at identical
inputs (EES stored values fed to CoolProp):

| Property call (identical inputs) | EES | CoolSolve (CoolProp) |
|---|---:|---:|
| T at P = 1539.88 kPa, x = 0.99, Q = 1 (dew point) | 76.636 °C | 76.120 °C |
| P at T = 40 °C, x = 0.38652, Q = 0 (bubble point) | 269.93 kPa | 286.91 kPa |
| x at T = 112.205 °C, P = 1539.88 kPa, Q = 0 | 0.34652 | 0.33894 |

EES uses its own NH3H2O formulation, CoolSolve the CoolProp (IAPWS) ammonia-water
model; the bubble-point pressure differs by up to 6 % at identical inputs, which
shifts every state of the cycle. The **compositions of the dilute second loop
are most sensitive**: x[19] is 2.08 % in EES and 0.97 % in CoolSolve (rel. diff
5.36e-01 as printed) — the loop adjusts its composition level until the internal
heat exchange closes, so the backend difference is amplified there. The COP
(3.45e-02) and all first-loop quantities stay within a few percent.

Excluded from the comparison, as printed by `compare_solution.py`:
- `h*`, `swp*` — absolute NH3H2O enthalpies carry a different reference state in
  EES and CoolProp (offsets of +118 to +336 kJ/kg depending on composition and
  phase); enthalpy *differences* and derived results are compared instead;
- `s[i]` — computed in CoolSolve only for the diagrams; the EES records are
  stale (the file computes no entropy; 27 such stale `v[i]` records exist too);
- `checkQ` — balance residual, closes in both tools (−2.3 mW / 1.6e-6 W on
  271.5 kW);
- `Q_dot_des_2` — no stored EES value; implied at 179.5 kW from COP_c and
  Q_dot_evap, CoolSolve gives 181.5 kW.

Per the import card, the status is **not** `verified`: the compositions of the
dilute loop do not agree with the EES reference (they do satisfy all balances of
the model in the CoolProp backend). The native file status is `blocked`.

## Source and attribution

Source: F-Chart Software EES example `ex10_1.ees`
(https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/ex10_1.ees,
MIT, (c) F-Chart Software / S. A. Klein), Example 10.1 of Herold, Radermacher
and Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015.
The binary `.EES` inside the `.eez` companion (EES X11.926, licence of
S. A. Klein, F-Chart Software) provided the stored solution used as reference.
Candidate row EEX-077 of `sources/ees_examples/inventory.csv`.

## Conversion log

- **2026-11-15 — import**: `ees_extract.py` on the binary `Ex10_1.EES`
  (extracted from `ex10_1.eez`, a zip): 268 variables with stored solution, no
  lookup or parametric table, RTF equations converted, licence tag removed.
- **2026-11-15 — unit conversion**: original `$UnitSystem SI C kPa kJ mass`
  converted by hand to SI-°C-Pa-J. The directive and `$TabStops` are removed;
  **no numeric value changed**: every equation is scale-homogeneous (mass,
  ammonia and energy balances, effectiveness relations), only the property
  functions change scale (kPa→Pa, kJ→J). The stored EES values were converted
  the same way in `.initials` (pressures, enthalpies, heat rates, entropies,
  83 entries ×1000) and by `--ees-units` in the comparison.
- **2026-11-15 — comments**: comment typos fixed (*solutuion* → solution,
  *efectiveness* → effectiveness, *bewteen* → between); comments otherwise
  paraphrase the original. Standard header added (24 lines).
- **2026-11-15 — post-processing**: `DUPLICATE i=1,29 s[i]=ENTROPY(NH3H2O,P=P[i],X=x[i],H=h[i])`
  block added at the end of both files for the thermodynamic diagrams
  (P[i], T[i], h[i] already exist as state points in the original); no effect
  on the results.
- **2026-11-15 — variant `nh3h2o_absorption_two_stage_coolsolve`**: the two
  property calls of **state 25** rewritten with the (P, x, H) input pair of the
  same state, decision D11 style:
  `h[25]=Enthalpy(NH3H2O,P=P[25],x=x[25],Q=Q[25])` →
  `Q[25]=Quality(NH3H2O,P=P[25],x=x[25],h=h[25])` and
  `T[25]=Temperature(NH3H2O,P=P[25],x=x[25],Q=Q[25])` →
  `T[25]=Temperature(NH3H2O,P=P[25],x=x[25],h=h[25])`. Both replacement forms
  occur elsewhere in the original file (states 6, 12, 2, 26…), so the variant
  is valid EES and models the same physics. All other equations unchanged.
  This is the only change; it works around CS-BUG-PROP-QLIMIT.
- **PROCEDURE shx**: kept exactly as in the original, including `Min()` — the
  smaller of the two heat rates (it parses and evaluates in CoolSolve 0.4.0,
  tested with `c = Min(3, 7)` = 3).
- **Level**: equations 213 → 1; largest block 119 → 2; PROCEDURE + arrays → 1;
  ≥ 3 coupled components (two solution loops, three rectifiers, five heat
  exchangers, two pumps, two valves) → 1; no off-design/dynamics → 0; needs
  converted `.initials` (large implicit block) → 1. Score 6 → **level 3**
  (matches the level_guess 3 of the inventory row).

## Limitations and CoolSolve gaps

- `CS-BUG-PROP-QLIMIT` — a property call whose Q input is an unknown sitting at
  the quality limit (state 25 mixes two *identical* saturated-vapour streams,
  so its quality is exactly 1 by construction) raises EvaluationError and stops
  the solve. Blocks the native file; the variant rewrites the two calls of
  state 25 (above). Registered in CoolSolve `docs/model_library_support.md`
  with a reproducer.
- The stored EES solution contains 56 stale records (`s[1]`…`s[29]`, `v[2]`…
  `v[29]`) of variables the file does not compute — an earlier version of the
  exercise called entropy and volume; they are ignored (and the extraction tool
  warns in general about stale values).

## Related models

- `CSL-0249` nh3h2o_absorption_chiller: single-effect NH3H2O absorption chiller
  with rectifier and solution/RHX heat exchangers — the single-stage counterpart
  of this two-stage cycle (written for the library). *Niche of this model*: the
  two-stage (double-effect) topology — Desorber 1 heated internally by Absorber 2
  and Rectifier 2, three rectifiers, condensate precooler — and the coupled
  solution of the two concentration loops.

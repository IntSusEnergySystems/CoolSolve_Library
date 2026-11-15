# Single-stage ammonia-water absorption cycle with absorber recirculation and condensate precooler

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0354`

A single-stage (single-effect) NH3H2O absorption refrigeration cycle solved as
one simultaneous system of 134 equations over the 16 state points of the
diagram, with three refinements over the basic single-stage cycle (Herold,
Radermacher and Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd
ed., 2015, Example 9.6):

- a **condensate precooler** (effectiveness `epsilon_sc`): the condensed
  refrigerant (10) is subcooled by the cold evaporator outlet (13/14);
- **solution recirculation in the absorber**: the pumped rich solution (2) is
  recirculated as stream 15, heated to the saturation temperature of the poor
  solution entering at 6, and sprayed back into the absorber;
- **preheating of the rich solution in the rectifier**: the rectifier coolant
  (the rich solution, stream 2 → 16) picks up the heat rejected by the
  rectification before entering the solution heat exchanger.

Given the heat rejection temperatures (absorber and condenser at 40 °C), the
evaporator temperature (−10 °C) and the design goals (rectified vapour
x[9] = 0.99, concentration difference DELTAx = 0.1), the model computes all
state points, the component heat rates and the COP.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O |
| **Size** | 134 equations (largest block: 13) |
| **Source** | F-Chart EES example `ex9_6.ees` (EES-Community/ees-examples, Case_Study) |
| **Authors** | S. A. Klein (F-Chart Software); Example 9.6 of Herold, Radermacher & Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015 |
| **License** | MIT |
| **CoolSolve** | 0.4.0@00a4daa — native file solves and was compared with the stored solution (see Verification) |

## Problem statement

Example 9.6 of the book: *Performance of a single-stage absorption system with
condensate precooling, solution recirculation in the absorber and preheating of
rich solution in the rectifier.* Inputs (as in the original): m_dot[1] = 1 kg/s,
eta_pump = 1, solution heat exchanger effectiveness epsilon_shx = 0.8,
condensate precooler effectiveness epsilon_sc = 0.8, T[1] = T[10] = 40 °C
(absorber / condenser heat rejection), T[13] = −10 °C (evaporator), saturated
liquid at states 1, 4, 8, 10, saturated vapour at 7, 9, evaporator outlet
quality Q[13] = 0.975 (to limit the temperature glide), rectifier design goal
x[9] = 0.99 and concentration difference x[1] − x[4] = DELTAx = 0.1.

## Model

The 16 states carry arrays m_dot[i], P[i], T[i], h[i], x[i], Q[i]. Components
(mass, ammonia and energy balances, as in the original): pump, solution heat
exchanger, desorber, rectifier (its coolant is the rich solution, 2 → 16),
two expansion valves, condenser, evaporator, condensate precooler, absorber
with recirculation (T[15] = T[6], the recirculated solution heated to the
saturation temperature of the poor solution at 6; the pump work is rejected
into the absorber). The solution heat exchanger and the condensate precooler
use the `PROCEDURE shx` of the original: an effectiveness model written with
capacity rates C_dot = m_dot·cp and `Min()` — the smaller of the two capacity
rates, *not* an optimiser (it parses and evaluates in CoolSolve as it is).

Pressures are set by the saturation of the solution: P_high from the condenser
conditions (T[10], x[10], Q[10] = 0), P_low from the evaporator exit
(T[13], x[13], Q[13] = 0.975); pressure changes only across the valves.

The state-point arrays P[i], T[i], h[i] (and m_dot[i], x[i], Q[i]) of the
original are kept; a post-processing block adds s[i] = Entropy(NH3H2O, P, x, h)
for the thermodynamic diagrams (no effect on the results).

## How to run

The native file is the faithful transcription of the example and solves in
CoolSolve as it is. It takes its guesses from `.initials` (values stored by
EES, pressures and enthalpies converted to Pa/J — 150 entries):

```bash
coolsolve ./nh3h2o_absorption_recirculation.eescode   # solves (56 iterations)
```

## Results (native file vs EES stored solution)

| Quantity | EES | CoolSolve | rel. diff as printed |
|---|---:|---:|---:|
| COP_1 (with pump power) | 0.467224 | 0.464763 | 5.27e-03 |
| COP_2 (without pump power) | 0.469585 | 0.467122 | 5.24e-03 |
| Q_dot_evap | 146.77 kW | 145.22 kW | 1.06e-02 |
| Q_dot_des (driving heat) | 312.55 kW | 310.87 kW | 5.37e-03 |
| Q_dot_abs | 308.80 kW | 307.01 kW | 5.79e-03 |
| Q_dot_cond | 152.10 kW | 150.65 kW | 9.50e-03 |
| Q_dot_shx | 213.76 kW | 214.46 kW | 3.27e-03 |
| Q_dot_precooler | 17.03 kW | 16.99 kW | 2.27e-03 |
| P_high | 1539.88 kPa | 1538.01 kPa | 1.22e-03 |
| P_low | 131.875 kPa | 134.746 kPa | 2.13e-02 |
| f (circulation ratio) | 8.0994 | 8.1596 | 7.38e-03 |
| x[1] (strong solution) | 0.280060 | 0.274042 | 2.15e-02 |
| x[4] (poor solution) | 0.180060 | 0.174042 | 3.34e-02 |
| x[7] (vapour at generator exit) | 0.872551 | 0.870187 | 2.71e-03 |
| T[4] (generator exit) | 152.61 °C | 151.27 °C | 8.79e-03 |
| T[9] (rectified vapour) | 76.64 °C | 76.09 °C | 7.14e-03 |
| DELTAt_glide (evaporator) | 17.72 K | 17.25 K | 2.64e-02 |
| checkQ (whole-cycle balance) | 1.2e-4 W | 2.3e-7 W | — |

The whole-cycle energy balance (Q_dot_des + Q_dot_evap + W_dot_pump =
Q_dot_cond + Q_dot_abs) closes to 2.3e-7 W on 460 kW (EES: 1.2e-4 W); the
absorber residual balances err_absmass and err_absammonia are ~1e-15.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/nh3h2o_absorption_recirculation_ph.png)  + one-line caption -->

## Verification

The native file was solved in CoolSolve and compared with the EES stored
solution of the binary `Ex9_6.EES` inside the `.eez` companion
(`compare_solution.py … --ees-units`, 132 common variables). COP, heat rates,
pressures, mass flows and temperatures agree within 0.1–2.6 %; the mass
fractions differ by up to 3.34e-02, explained by the NH3H2O **property
backend**, evidenced by identical property calls at identical inputs (EES
stored values fed to CoolProp):

| Property call (identical inputs) | EES | CoolSolve (CoolProp) | rel. diff |
|---|---:|---:|---:|
| P at T = −10 °C, x = 0.99, Q = 0.975 | 131.875 kPa | 134.746 kPa | 2.1e-02 |
| x at T = 40 °C, P = 131.875 kPa, Q = 0 (bubble) | 0.280060 | 0.271109 | 3.2e-02 |
| T at P = 1539.880 kPa, x = 0.99, Q = 1 (dew) | 76.636 °C | 76.120 °C | 6.8e-03 |

EES uses its own NH3H2O formulation, CoolSolve the CoolProp (IAPWS) ammonia-water
model; at identical inputs the bubble-point pressure and the bubble composition
differ by 2–3 %. The cycle then adjusts the composition level (x[1] from the
saturation at T[1] = 40 °C, x[4] = x[1] − 0.1) and every downstream state, so
the 2.15e-02 on x[1] and 3.34e-02 on x[4] follow from the backend alone —
already visible on the single property call at identical inputs (3.2e-02
above). All other cycle quantities stay within 2.6 %.

Excluded from the comparison, as printed by `compare_solution.py`:
- `h[i]`, `swp`, `s[i]` — absolute NH3H2O enthalpies and entropies carry a
  different reference state in EES and CoolProp (offsets of the order of
  1e5 J/kg on h, 1e3 J/kg-K on s); enthalpy *differences* and derived results
  are compared instead. The EES `s[1..14]`, `v[2..14]`, `Q[2]`, `Q[5]`,
  `Q[11]`, `Q[14]` records are moreover stale: the file computes none of them
  (they remain from an earlier version of the exercise); `v[1]` is computed
  and agrees to 2.83e-03;
- `checkQ` — balance residual, closes in both tools (1.2e-4 W / 2.3e-7 W on
  460 kW);
- `cp_1011`, `cp_1314`, `cp_163` — the reference CSV stores their units as
  `J/g-K`, which `--ees-units` does not convert (tool bug
  `CS-BUG-COMPARE-JGK`, reported): the printed 9.99e-01 is an artifact;
  converted by hand, the true diffs are 3.84e-03 (cp_1011), 5.14e-03
  (cp_1314) and 2.09e-02 (cp_163).

Verification summary: verified with the printed tolerance 3.34e-02 as the
maximum over the compared set (x[4], x[5], x[6]) — the card threshold "a mass
fraction within a few percent" is met at 3.3 %, and the deviation is fully
accounted for by the documented backend difference at identical inputs (same
quantity: 3.2e-02).

## Source and attribution

Source: F-Chart Software EES example `ex9_6.ees`
(https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/ex9_6.ees,
MIT, (c) F-Chart Software / S. A. Klein), Example 9.6 of Herold, Radermacher
and Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015.
The binary `.EES` inside the `.eez` companion (EES X11.926, licence of
S. A. Klein, F-Chart Software) provided the stored solution used as reference.
Candidate row EEX-112 of `sources/ees_examples/inventory.csv`.

## Conversion log

- **2026-11-15 — import**: the `.eez` companion (a zip) was extracted to the
  inner `Ex9_6.EES` binary first, then `ees_extract.py`: 163 variables with
  stored solution, no lookup or parametric table, EES X11.926, licence tag
  removed. Unit system `$UnitSystem SI MASS DEG KPA C KJ`.
- **2026-11-15 — unit conversion**: original SI-C-kPa-kJ converted by hand to
  SI-°C-Pa-J. The directives (`$UnitSystem`, `$TabStops`) are removed; **no
  numeric value changed**: every input is a temperature in °C, a mass fraction,
  a mass flow in kg/s or an effectiveness; every equation is scale-homogeneous
  (mass, ammonia and energy balances, capacity-rate relations), only the
  property functions change scale (kPa→Pa, kJ→J: e.g. `swp = v[1]*(P[2]-P[1])`
  reads kPa·m³/kg = J/kg in Pa). The stored EES values were converted the same
  way in `.initials` (pressures, enthalpies, heat rates, cp and C_dot entries
  ×1000; 150 entries) and by `--ees-units` in the comparison.
- **2026-11-15 — comments**: comment typos fixed (*capcitance* → capacitance,
  *eficency*/*efectiveness* → efficiency/effectiveness, *equlibrium* →
  equilibrium, *ansd* → and); two comment/line mismatches of the original
  corrected (the `T[9]` line said "Enthalpy obtained as well" and the `Q[12]`
  line "Temperature obtained as well", swapped; the state-7 comment said
  "saturated liquid" while `Q[7] = 1` and the stored `v[7]` = 0.108 m³/kg make
  it the saturated **vapour** at the generator exit — comment-only corrections,
  no effect on the results). Comments otherwise paraphrase the original.
  Standard header added (25 lines).
- **2026-11-15 — post-processing**: `DUPLICATE i=1,16
  s[i]=Entropy(NH3H2O,P=P[i],X=x[i],H=h[i])` block added at the end for the
  thermodynamic diagrams (P[i], T[i], h[i] already exist as state points in
  the original); no effect on the results.
- **PROCEDURE shx**: kept exactly as in the original (equations unchanged),
  including `Min()` — the smaller of the two capacity rates C_dot_c and
  C_dot_h, not an optimiser; capacity-rate comments now carry their unit
  [W/K].
- **Level**: equations 134 → 1; largest block 13 → 1; PROCEDURE + arrays → 1;
  ≥ 3 coupled components (desorber, rectifier, absorber with recirculation,
  SHX, precooler, condenser, evaporator, pump, two valves) → 1; no
  off-design/dynamics → 0; needs converted `.initials` (implicit loops) → 1.
  Score 5 → **level 3** (matches the level_guess 3 of the inventory row).

## Niche

The library has the basic single-effect chiller `CSL-0249` (written for the
library, no recirculation), the ideal-cycle `CSL-0347`, the two-stage
`CSL-0352` (Example 10.1) and the LiBr-H2O cycle `libr_water_absorption_chiller`.
This model adds the Example 9.6 topology of the same textbook: absorber
solution recirculation heated to the poor-solution saturation temperature,
rich-solution preheating by the rectifier coolant, and the condensate
precooler with capacity-rate effectiveness models — a different state-point
layout (16 states), the circulation ratio f as an output, and the verified
comparison against the stored solution of the F-Chart example file.

## Related models

- `CSL-0249` nh3h2o_absorption_chiller: single-effect NH3H2O absorption
  chiller with rectifier and solution/RHX heat exchangers, without absorber
  recirculation (written for the library).
- `CSL-0352` nh3h2o_absorption_two_stage: the two-stage (double-effect)
  Example 10.1 of the same book, same component family with two solution
  loops and three rectifiers.

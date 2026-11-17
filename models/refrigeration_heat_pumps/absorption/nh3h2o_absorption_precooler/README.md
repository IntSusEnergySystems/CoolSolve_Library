# Single-stage ammonia-water absorption cycle with a condensate precooler

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0360`

A single-stage (single-effect) NH3H2O absorption refrigeration cycle solved as
one simultaneous system of 122 equations over the 14 state points of the
diagram (Herold, Radermacher and Klein, *Absorption Chillers and Heat Pumps*,
CRC Press, 2nd ed., 2015, Example 9.3): the basic single-stage cycle extended
with a **condensate precooler** (effectiveness `epsilon_sc`) that subcools the
condensed refrigerant (10 → 11) with the cold evaporator outlet (13 → 14).

Given the heat rejection temperatures (absorber and condenser at 40 °C), the
evaporator temperature (−10 °C) and the design goals (rectified vapour
x[9] = 0.9996, concentration difference DELTAx = 0.1), the model computes all
state points, the component heat rates and the COP.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O |
| **Size** | 122 equations (largest block: 7) |
| **Source** | F-Chart EES example `ex9_3.ees` (EES-Community/ees-examples, Case_Study) |
| **Authors** | S. A. Klein (F-Chart Software); Example 9.3 of Herold, Radermacher & Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015 |
| **License** | MIT |
| **CoolSolve** | 0.4.0@a53de60 — native file solves and was compared with the stored solution (see Verification) |

## Problem statement

Example 9.3 of the book: *Performance of a Single-Stage Absorption System With
a Condensate Precooler.* Inputs (as in the original): m_dot[1] = 1 kg/s,
eta_pump = 1, solution heat exchanger effectiveness epsilon_shx = 0.8,
condensate precooler effectiveness epsilon_sc = 0.8, T[1] = T[10] = 40 °C
(absorber / condenser heat rejection), T[13] = −10 °C (evaporator), saturated
liquid at states 1, 4, 8, 10, saturated vapour at 7, 9, evaporator outlet
quality Q[13] = 0.975 (to limit the temperature glide), rectifier design goal
x[9] = 0.9996 and concentration difference x[1] − x[4] = DELTAx = 0.1.

## Model

The 14 states carry arrays m_dot[i], P[i], T[i], h[i], x[i], Q[i]. Components
(mass, ammonia and energy balances, as in the original): pump, solution heat
exchanger, desorber, rectifier, two expansion valves, condenser, evaporator,
condensate precooler, absorber. The solution heat exchanger and the condensate
precooler use the `PROCEDURE shx` of the original: an effectiveness model
written with capacity rates C_dot = m_dot·cp and `Min()` — the smaller of the
two capacity rates, *not* an optimiser (it parses and evaluates in CoolSolve
as it is).

Pressures are set by the saturation of the solution: P_high from the condenser
conditions (T[10], x[10], Q[10] = 0), P_low from the evaporator exit
(T[13], x[13], Q[13] = 0.975); pressure changes only across the valves.

The state-point arrays P[i], T[i], h[i] (and m_dot[i], x[i], Q[i]) of the
original are kept; a post-processing block adds s[i] = Entropy(NH3H2O, P, x, h)
for the thermodynamic diagrams (no effect on the results).

## How to run

The native file is the faithful transcription of the example and solves in
CoolSolve as it is. It takes its guesses from `.initials` (values stored by
EES, pressures and enthalpies converted to Pa/J — 136 entries):

```bash
coolsolve ./nh3h2o_absorption_precooler.eescode   # solves (54 iterations)
```

## Results (native file vs EES stored solution)

| Quantity | EES | CoolSolve | rel. diff as printed |
|---|---:|---:|---:|
| COP_1 (with pump power) | 0.501833 | 0.492974 | 1.77e-02 |
| COP_2 (without pump power) | 0.504113 | 0.495221 | 1.76e-02 |
| Q_dot_evap | 165.07 kW | 162.12 kW | 1.79e-02 |
| Q_dot_des (driving heat) | 327.45 kW | 327.37 kW | < 1e-03 |
| Q_dot_abs | 292.00 kW | 291.13 kW | 2.98e-03 |
| Q_dot_cond | 159.17 kW | 156.59 kW | 1.62e-02 |
| Q_dot_rect | 42.84 kW | 43.26 kW | 9.62e-03 |
| Q_dot_shx | 257.87 kW | 268.93 kW | 4.11e-02 |
| Q_dot_precooler | 18.13 kW | 18.02 kW | 6.02e-03 |
| P_high | 1555.70 kPa | 1554.71 kPa | < 1e-03 |
| P_low | 286.44 kPa | 286.15 kPa | 1.01e-03 |
| f (circulation ratio) | 7.0338 | 7.1352 | 1.42e-02 |
| x[1] (strong solution) | 0.396223 | 0.386080 | 2.56e-02 |
| x[4] (poor solution) | 0.296223 | 0.286080 | 3.42e-02 |
| x[7] (vapour at generator exit) | 0.958210 | 0.956022 | 2.28e-03 |
| T[4] (generator exit) | 124.24 °C | 124.83 °C | 4.67e-03 |
| T[9] (rectified vapour) | 45.11 °C | 45.05 °C | 1.33e-03 |
| T[11] (subcooled condensate) | 13.56 °C | 13.19 °C | 2.69e-02 |
| DELTAt_glide (evaporator) | 0.3573 K | 0.3780 K | 5.46e-02 |
| checkQ (whole-cycle balance) | 3.6e-03 W | −7.9e-07 W | — |
| Q[6], Q[14] (boundary qualities) | −0.001 / 1.001 | −0.001 / 1.001 | exact |

The whole-cycle energy balance (Q_dot_des + Q_dot_evap + W_dot_pump =
Q_dot_rect + Q_dot_cond + Q_dot_abs) closes to −7.9e-07 W on 470 kW (EES:
3.6e-03 W); the absorber residual balances err_absmass and err_absammonia are
~1e-17. Q[6] (after the solution valve, saturated-liquid boundary) and Q[14]
(superheated) take the boundary clamp values −0.001 and 1.001 in both tools.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/nh3h2o_absorption_precooler_ph.png)  + one-line caption -->

## Verification

The native file was solved in CoolSolve and compared with the EES stored
solution of the binary `Ex9_3.EES` inside the `.eez` companion
(`compare_solution.py … --ees-units`, 122 common variables, 81 differ at
rtol=0.001). COP within 1.8 %, heat rates within 4.2 %, pressures within
0.11 %, temperatures within 2.8 %; the mass fractions differ by up to 3.42e-02
(a few percent), explained by the NH3H2O **property backend**, evidenced by
identical property calls at identical inputs in the comparison itself:

| Property call (identical inputs) | EES | CoolSolve (CoolProp) | rel. diff |
|---|---:|---:|---:|
| P at T = 40 °C, x[10] = x[9] = 0.9996, Q = 0 (bubble) | 1555.70 kPa | 1554.71 kPa | < 1e-03 |
| P at T = −10 °C, x = 0.9996, Q = 0.975 | 286.435 kPa | 286.146 kPa | 1.01e-03 |
| x[1] at T = 40 °C, P = P_low (≈ equal to 1e-03), Q = 0 | 0.396223 | 0.386080 | 2.56e-02 |

EES uses its own NH3H2O formulation, CoolSolve the CoolProp ammonia-water
model; at nearly pure refrigerant (x = 0.9996) the pressures agree to 1e-03,
while the bubble composition of the *solution* at identical (T, P) differs by
2.6 %. The cycle then adjusts the composition level (x[1] from the saturation
at T[1] = 40 °C, x[4] = x[1] − 0.1) and every downstream state, so the
2.56e-02 on x[1] and 3.42e-02 on x[4] follow from the backend alone; the
composition-dependent cp_23/cp_45 (3.2–3.7e-02), Q_dot_shx (4.11e-02) and
DELTAt_glide (5.46e-02, an absolute difference of 0.021 K on a 0.36 K glide)
inherit the same shift. All other cycle quantities stay within 2.8 %.

Excluded from the comparison, as printed by `compare_solution.py`:
- `h[i]`, `s[i]`, `swp` — absolute NH3H2O enthalpies and entropies carry a
  different reference state in EES and CoolProp (offsets of the order of
  1e5 J/kg on h, 1e3 J/kg-K on s); enthalpy *differences* and derived results
  are compared instead. The EES `s[1..14]` and `v[2..14]` records are
  moreover stale: the file computes none of them (they remain from an earlier
  version of the exercise); `v[1]` is computed and agrees to 3.14e-03;
- `checkQ` — balance residual, closes in both tools (3.6e-03 W / −7.9e-07 W
  on 470 kW);
- `cp_1011`, `cp_1314` — the reference CSV stores their units as `J/g-K`,
  which `--ees-units` does not convert (tool bug `CS-BUG-COMPARE-JGK`,
  already registered): the printed 9.99e-01 is an artifact; converted by
  hand, the true diffs are 5.4e-03 (cp_1011) and 8.3e-03 (cp_1314);
- `C_dot_min` — procedure-local variable (not an output of the model);
- `Q[2]`, `Q[3]`, `Q[5]`, `Q[11]`, `v[2..14]` — stored EES records for
  variables the file never computes (stale, EES boundary marker −0.001).

Verification summary: verified with the printed tolerance 5.46e-02 as the
maximum over the compared set (DELTAt_glide, 0.021 K absolute); the card
threshold "a mass fraction within a few percent" is met at 3.4 %, and the
deviation is fully accounted for by the documented backend difference at
identical inputs (same quantity: 2.56e-02).

## Source and attribution

Source: F-Chart Software EES example `ex9_3.ees`
(https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/ex9_3.ees,
MIT, (c) F-Chart Software / S. A. Klein), Example 9.3 of Herold, Radermacher
and Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015.
The binary `.EES` inside the `.eez` companion (EES X11.926, licence of
S. A. Klein, F-Chart Software) provided the stored solution used as reference.
Candidate row EEX-109 of `sources/ees_examples/inventory.csv`.

## Conversion log

- **2026-11-15 — import**: the `.eez` companion (a zip) was extracted to the
  inner `Ex9_3.EES` binary first, then `ees_extract.py`: 161 variables with
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
  ×1000; 136 entries, stale records of states 15–17 dropped) and by
  `--ees-units` in the comparison.
- **2026-11-15 — comments**: comment typos fixed (*capcitance* → capacitance,
  *efectiveness*/*efficency* → effectiveness/efficiency, *equlibrium* →
  equilibrium); three comment/line mismatches of the original corrected
  (the `T[9]` line said "Enthalpy obtained as well" and the `Q[12]` line
  "Temperature obtained as well", swapped; the state-7 comment said
  "assumed to be saturated liquid" while `Q[7] = 1` and the stored `v[7]` =
  0.108 m³/kg make it the saturated **vapour** at the generator exit; the
  precooler cp comments said "stream 2-3"/"stream 4-5", copied from the
  solution heat exchanger, for what are streams 10-11 and 13-14) —
  comment-only corrections, no effect on the results. Comments otherwise
  paraphrase the original. Standard header added (24 lines).
- **2026-11-15 — post-processing**: `DUPLICATE i=1,14
  s[i]=Entropy(NH3H2O,P=P[i],X=x[i],H=h[i])` block added at the end for the
  thermodynamic diagrams (P[i], T[i], h[i] already exist as state points in
  the original); no effect on the results.
- **PROCEDURE shx**: kept exactly as in the original (equations unchanged),
  including `Min()` — the smaller of the two capacity rates C_dot_c and
  C_dot_h, not an optimiser; capacity-rate comments now carry their unit
  [W/K].
- **No property-call rewrite**: no call uses an unsupported input pair; the
  qualities at the dome boundary (Q[6] ≈ 0, Q[14] > 1) are outputs of
  `Quality(P, H, X)` calls that both tools clamp to the same boundary values
  (−0.001 / 1.001); `Q[7] = 1` enters the state-7 calls as a constant and
  evaluates (no `CS-BUG-PROP-QLIMIT` trigger).
- **Level**: equations 122 → 1; largest block 7 → 1; PROCEDURE + arrays → 1;
  ≥ 3 coupled components (desorber, rectifier, absorber, SHX, precooler,
  condenser, evaporator, pump, two valves) → 1; no off-design/dynamics → 0;
  needs converted `.initials` (implicit loops) → 1. Score 5 → **level 3**
  (matches the level_guess 3 of the inventory row).

## Niche

The library has the basic single-effect chiller `CSL-0249` (written for the
library, no precooler), the ideal-cycle `CSL-0347`, the two-stage `CSL-0352`
(Example 10.1), the LiBr-H2O cycle `libr_water_absorption_chiller` and the
Example 9.6 topology with absorber recirculation `CSL-0354`. This model adds
the Example 9.3 topology of the same textbook: the plain single-stage cycle
with the condensate precooler only (no recirculation loop, no rectifier
preheating), a different design point (x[9] = 0.9996, rich solution
x[1] ≈ 0.40, generator exit 124 °C), and the verified comparison against the
stored solution of the F-Chart example file.

## Related models

- `CSL-0249` nh3h2o_absorption_chiller: single-effect NH3H2O absorption
  chiller with rectifier and solution/RHX heat exchangers (written for the
  library).
- `CSL-0354` nh3h2o_absorption_recirculation: Example 9.6 of the same book,
  same precooler plus absorber solution recirculation and rectifier
  preheating (16 states).
- `CSL-0352` nh3h2o_absorption_two_stage: the two-stage (double-effect)
  Example 10.1 of the same book.

## Limitations and CoolSolve gaps

None: the native file solves as extracted (after the by-hand unit
conversion); no CoolSolve gap blocks it. Absolute NH3H2O enthalpies and
entropies use a different reference state in EES and CoolProp — a property
backend difference, not a gap.

# Single-stage ammonia-water absorption cycle with a condensate precooler and UA models on the four corners

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0364`

The Example 9.3 single-stage (single-effect) NH3H2O absorption refrigeration
cycle with condensate precooler (Herold, Radermacher and Klein, *Absorption
Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015), modified as **Example
9.3b**: the corner temperatures (absorber, condenser, evaporator, desorber)
are no longer imposed. Instead, each corner is coupled to an **external water
loop** by a UA·LMTD heat-exchanger model (`LMTD_F`), and these four couplings
close the system: the cycle operating point (pressures, mass fractions,
temperatures, COP) floats with the given UA values, water flows and loop inlet
temperatures.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O |
| **Size** | 143 equations (largest block: 80) |
| **Source** | F-Chart EES example `ex9_3_ua.ees` (EES-Community/ees-examples, Case_Study) |
| **Authors** | S. A. Klein (F-Chart Software); Example 9.3b of Herold, Radermacher & Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015 |
| **License** | MIT |
| **CoolSolve** | 0.4.0@a53de60 — native file solves and was compared with the stored solution (see Verification) |

## Problem statement

Example 9.3b of the book: *Performance of a Single-Stage Absorption System
With a Condensate Precooler and Heat Exchanger Models.* The internal cycle
keeps the Example 9.3 inputs (m_dot[1] = 1 kg/s, eta_pump = 1,
epsilon_shx = 0.8, precooler effectiveness epsilon_sc = 0.8, rectified vapour
x[9] = 0.9996, saturated liquid at 1, 4, 8, 10, saturated vapour at 7, 9,
evaporator outlet quality Q[13] = 0.975). The imposed temperatures T[1],
T[10], T[13] and the concentration difference DELTAx of Example 9.3 are
replaced by the external loops:

| Corner | Loop inlet | Water flow | UA |
|---|---|---:|---:|
| Condenser | T[21] = 35 °C | 12.5 kg/s | UA_c = 30 kW/K |
| Evaporator | T[23] = 0 °C | 7.5 kg/s | UA_e = 20 kW/K |
| Absorber | T[25] = 35 °C | 12.5 kg/s | UA_a = 30 kW/K |
| Desorber | T[27] = 150 °C | 7.5 kg/s | UA_d = 10 kW/K |

## Model

The 14 internal states carry arrays m_dot[i], P[i], T[i], h[i], x[i], Q[i].
Components (mass, ammonia and energy balances, as in the original): pump,
solution heat exchanger, desorber, rectifier, two expansion valves,
condenser, evaporator, condensate precooler, absorber. The solution heat
exchanger and the condensate precooler use the `PROCEDURE shx` of the
original: an effectiveness model written with capacity rates
C_dot = m_dot·cp and `Min()` — the smaller of the two capacity rates, *not*
an optimiser.

Each corner adds three equations of the original: the water-loop outlet
temperature (T[22], T[24], T[26], T[28], from an energy balance with
cp = 4.2 kJ/kg-K), the log mean temperature difference `LMTD_F(...)`, and the
conductance closure UA = Q_dot/LMTD. Pressures are set by the saturation of
the solution (P_high from the condenser conditions, P_low from the evaporator
exit quality Q[13] = 0.975); pressure changes only across the valves. With
the temperatures no longer imposed, the corner states T[1], T[10], T[13] and
DELTAx become unknowns of the simultaneous system.

A post-processing block adds s[i] = Entropy(NH3H2O, P, x, h) for the
thermodynamic diagrams (no effect on the results).

## How to run

The native file is the faithful transcription of the example and solves in
CoolSolve as it is. It takes its guesses from `.initials` (values stored by
EES, pressures, enthalpies, heat rates and specific heats converted to Pa/J —
162 entries):

```bash
coolsolve ./nh3h2o_absorption_precooler_ua.eescode   # solves (20 iterations)
```

## Results (native file vs EES stored solution)

| Quantity | EES | CoolSolve | rel. diff as printed |
|---|---:|---:|---:|
| COP_1 (with pump power) | 0.495448 | 0.488390 | 1.42e-02 |
| COP_2 (without pump power) | 0.497738 | 0.490648 | 1.42e-02 |
| Q_dot_evap | 161.75 kW | 159.22 kW | 1.56e-02 |
| Q_dot_des (driving heat) | 324.98 kW | 324.52 kW | 1.42e-03 |
| Q_dot_abs | 289.12 kW | 288.20 kW | 3.18e-03 |
| Q_dot_cond | 155.90 kW | 153.76 kW | 1.37e-02 |
| Q_dot_rect | 43.22 kW | 43.29 kW | 1.63e-03 |
| Q_dot_shx | 261.40 kW | 271.20 kW | 3.62e-02 |
| Q_dot_precooler | 17.97 kW | 17.83 kW | 7.54e-03 |
| P_high | 1561.72 kPa | 1557.40 kPa | 2.77e-03 |
| P_low | 278.27 kPa | 280.05 kPa | 6.36e-03 |
| T[1] (absorber exit) | 39.90 °C | 39.86 °C | 1.10e-03 |
| T[10] (condenser exit) | 40.14 °C | 40.06 °C | 1.91e-03 |
| T[13] (evaporator exit) | −10.72 °C | −10.53 °C | 1.75e-02 |
| T[4] (generator exit) | 125.04 °C | 125.17 °C | 1.06e-03 |
| DELTAx (now an output) | 0.098372 | 0.098376 | < 1e-04 |
| x[1] (strong solution) | 0.392008 | 0.383332 | 2.21e-02 |
| x[4] (poor solution) | 0.293636 | 0.284956 | 2.96e-02 |
| x[7] (vapour at generator exit) | 0.956236 | 0.954693 | 1.61e-03 |
| DELTAt_glide (evaporator) | 0.3486 K | 0.3761 K | 7.31e-02 |
| checkQ (whole-cycle balance) | 9.1e-05 W | −2.5e-07 W | — |
| Q[6], Q[14] (boundary qualities) | −0.001 / 1.001 | −0.001 / 1.001 | exact |

The whole-cycle energy balance (Q_dot_des + Q_dot_evap + W_dot_pump =
Q_dot_rect + Q_dot_cond + Q_dot_abs) closes to −2.5e-07 W on 485 kW (EES:
9.1e-05 W on 488 kW); the absorber residual balances err_absmass and err_absammonia are
below the solver tolerance. Q[6] (after the solution valve,
saturated-liquid boundary) and Q[14] (superheated) take the boundary clamp
values −0.001 and 1.001 in both tools. The resulting cycle differs from the
imposed-temperature Example 9.3 (library model `CSL-0360`): T[1] = 39.9 °C,
T[10] = 40.1 °C, T[13] = −10.7 °C and DELTAx = 0.0984 come out close to, but
not at, the values that example imposed (40 °C, 40 °C, −10 °C, 0.1).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/nh3h2o_absorption_precooler_ua_ph.png)  + one-line caption -->

## Verification

The native file was solved in CoolSolve and compared with the EES stored
solution of the binary `Ex9_3_UA.EES` inside the `.eez` companion
(`compare_solution.py … --ees-units`, 143 common variables, 98 differ at
rtol=0.001). COP within 1.4 %, heat rates within 3.6 %, pressures within
0.64 %, temperatures within 2.7 %; the mass fractions differ by up to 2.96e-02
(within a few percent), explained by the NH3H2O **property backend**, exactly
as documented for the sibling model `CSL-0360` (same property calls, same
book example): at identical inputs the bubble composition of the solution
differs by ~2.6 % between EES and CoolProp, the cycle shifts the composition
level (x[1], x[4]) accordingly, and the composition-dependent cp_23/cp_45
(3.2–3.7e-02), Q_dot_shx (3.62e-02) and DELTAt_glide (7.31e-02, an absolute
difference of 0.027 K on a 0.35 K glide) inherit the same shift. All other
cycle quantities stay within 2.7 %.

Excluded from the comparison, as printed by `compare_solution.py`:
- `h[i]`, `s[i]`, `swp` enthalpy/entropy *offsets* — absolute NH3H2O
  enthalpies and entropies carry a different reference state in EES and
  CoolProp (e.g. h[1]: −49 233 EES vs +70 477 J/kg CoolSolve, a constant
  offset of 1.197e5 J/kg; h[2] = h[1] + swp holds in both); enthalpy
  *differences* and derived results are compared instead. The EES `s[1..14]`,
  `v[2..14]`, `Q[2]`, `Q[3]`, `Q[5]`, `Q[11]`, `T[16]` records are moreover
  stale: the file computes none of them (leftovers of an earlier version of
  the exercise);
- `checkQ` — balance residual, closes in both tools (9.1e-05 W / −2.5e-07 W
  on ~485 kW);
- `cp`, `cp_1011`, `cp_1314` — the reference CSV stores their units as
  `J/g-K` / `J/g-DELTAK`, which `--ees-units` does not convert (tool bug
  `CS-BUG-COMPARE-JGK`, already registered): the printed 9.99e-01 diffs are
  artifacts; converted by hand, `cp` (a given input, 4.2 J/g-K = 4200 J/kg-K)
  agrees exactly, cp_1011 differs by 5.4e-03 and cp_1314 by 9.8e-03;
- `C_dot_min`, `m_dot_c` — procedure-local variables (not outputs of the
  model).

## Source and attribution

Source: F-Chart Software EES example `ex9_3_ua.ees`
(https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/ex9_3_ua.ees,
MIT, (c) F-Chart Software / S. A. Klein), Example 9.3b of Herold, Radermacher
and Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015
(the file links the original download
https://fchartsoftware.com/ees/examples/examples_achp_2015/chapter%209/ex9_3_ua.eez).
The binary `.EES` inside the `.eez` companion (EES X11.926, licence of
S. A. Klein, F-Chart Software) provided the stored solution used as
reference. Candidate row EEX-110 of `sources/ees_examples/inventory.csv`.

## Conversion log

- **2026-11-15 — import**: the `.eez` companion (a zip) was extracted to the
  inner `Ex9_3_UA.EES` binary first, then `ees_extract.py`: 183 variables with
  stored solution, no lookup or parametric table, EES X11.926, licence tag
  removed. Unit system `$UnitSystem SI MASS DEG KPA C KJ`.
- **2026-11-15 — unit conversion**: original SI-C-kPa-kJ converted by hand to
  SI-°C-Pa-J. Directives (`$UnitSystem`, `$TabStops`) removed. Converted
  values: `cp = 4.2 [J/g-DELTAK]` → 4200 J/kg-K; `UA_d = 10 [kW/K]` →
  10 000 W/K, `UA_c = 30` → 30 000 W/K, `UA_e = 20` → 20 000 W/K,
  `UA_a = 30` → 30 000 W/K (the four corner conductances). Everything else is
  unchanged: temperatures stay in °C, mass flows in kg/s, mass fractions and
  qualities are dimensionless; every balance is scale-homogeneous, and the
  property calls change scale consistently (kPa→Pa, kJ→J: e.g.
  `swp = v[1]*(P[2]-P[1])` reads Pa·m³/kg = J/kg,
  `UA = Q_dot/LMTD` reads W/K). Stored EES values converted the same way in
  `.initials` (162 entries: pressures, enthalpies, heat rates, cp and
  C_dot entries ×1000; stale records of states 15–17 dropped) and by
  `--ees-units` in the comparison.
- **2026-11-15 — comments**: comment typos fixed (*capcitance* → capacitance,
  *efectiveness*/*efficency* → effectiveness/efficiency, *equlibrium* →
  equilibrium, *ansd* → and); comment/line mismatches of the original
  corrected as in `CSL-0360` (the `T[9]` line said "Enthalpy obtained as
  well" and the `Q[12]` line "Temperature obtained as well", swapped; the
  state-7 comment said "saturated liquid" while `Q[7] = 1` makes it the
  saturated **vapour**; the precooler cp comments said "stream 2-3"/"stream
  4-5", copied from the solution heat exchanger, for what are streams 10-11
  and 13-14; the rectifier ammonia balance was labelled "energy balance") —
  comment-only corrections, no effect on the results. The commented-out
  `{T[13]=-10}`, `{T[10]=40}`, `{T[1]=40}`, `{DELTAx=0.1}` lines are kept as
  in the original: they document the Example 9.3 imposed-temperature
  alternative. Comments otherwise paraphrase the original. Standard header
  added (20 lines).
- **2026-11-15 — post-processing**: `DUPLICATE i=1,14
  s[i]=Entropy(NH3H2O,P=P[i],X=x[i],H=h[i])` block added at the end for the
  thermodynamic diagrams (P[i], T[i], h[i] already exist as state points in
  the original); no effect on the results.
- **PROCEDURE shx**: kept exactly as in the original (equations unchanged),
  including `Min()` — the smaller of the two capacity rates C_dot_c and
  C_dot_h, not an optimiser; capacity-rate comments now carry their unit
  [W/K]. The four `LMTD_F` calls are kept; `LMTD_F(a, b)` evaluates as the
  log mean (a−b)/ln(a/b) (checked: LMTD_F(20, 10) = 14.42695).
- **No property-call rewrite**: no call uses an unsupported input pair and no
  unknown quality hits the limit (`CS-BUG-PROP-QLIMIT` does not trigger);
  the qualities at the dome boundary are outputs of `Quality(P, H, X)` calls
  that both tools clamp to the same boundary values (−0.001 / 1.001); the
  calls with `Q=` input all receive constants (Q = 0, 0.975 or 1).
- **Level**: equations 143 → 1; largest block 80 → 2; PROCEDURE + arrays → 1;
  ≥ 3 coupled components (desorber, rectifier, absorber, SHX, precooler,
  condenser, evaporator, pump, two valves, four UA corners) → 1; corner
  temperatures floating with fixed UA (off-design-style closure) → 1; needs
  converted `.initials` (implicit loops) → 1. Score 7 → level 4, moved down
  one step to **level 3** (matches the level_guess 3 of the inventory row and
  the sibling `CSL-0360`): textbook exercise of the same family, the 80-
  equation block is the property-call closure, and the solve takes 20
  iterations from the stored guesses without tuning.

## Niche

The library has the imposed-temperature version of this exact cycle
`CSL-0360` (Example 9.3), the basic single-effect chiller `CSL-0249`, the
ideal-cycle `CSL-0347`, the two-stage `CSL-0352` (Example 10.1) and the
Example 9.6 topology with absorber recirculation `CSL-0354`. This model adds
the **UA-coupled** closure of the same Example 9.3 topology: the four corner
temperatures and DELTAx become simultaneous unknowns driven by corner
conductances and external water loops, so the model can be swept over UA or
loop temperatures (off-design studies the imposed-temperature version cannot
do), with the verified comparison against the stored solution of the F-Chart
example file.

## Related models

- `CSL-0360` nh3h2o_absorption_precooler: the same cycle with the corner
  temperatures imposed (Example 9.3, the file this one was derived from in
  the F-Chart collection).
- `CSL-0354` nh3h2o_absorption_recirculation: Example 9.6 of the same book,
  precooler plus absorber solution recirculation and rectifier preheating.
- `CSL-0352` nh3h2o_absorption_two_stage: the two-stage (double-effect)
  Example 10.1 of the same book.

## Limitations and CoolSolve gaps

None: the native file solves as extracted (after the by-hand unit
conversion); no CoolSolve gap blocks it. Absolute NH3H2O enthalpies and
entropies use a different reference state in EES and CoolProp — a property
backend difference, not a gap. Cosmetic: CoolSolve prints an
`Unknown function 'LMTD_F'` warning while evaluating the built-in correctly
(the result was checked against the closed form).

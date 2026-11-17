# Single-stage ammonia-water absorption cycle with rectifier (Herold Example 9.2)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0363`

Single-stage NH3/H2O absorption refrigeration cycle, Example 9.2 of Herold,
Radermacher and Klein, *Absorption Chillers and Heat Pumps* (CRC Press, 2015):
a rectifier purifies the vapour leaving the generator, and an effectiveness
solution heat exchanger preheats the rich solution. Given the heat rejection
temperatures (40 °C), the evaporator temperature (−10 °C), the rectifier
outlet mass fraction (x[9] = 0.9996) and the concentration difference
(DELTAx = 0.1), the model computes the 13 state points, the component heat
rates and the COP.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O |
| **Size** | 105 equations (largest block: 7) |
| **Source** | `ex9_2.ees`, F-Chart Software EES example (EES-Community/ees-examples, Case_Study) |
| **Authors** | S. A. Klein (F-Chart Software); exercise from Herold, Radermacher and Klein 2015 |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — verified (see the verification field) |

## Problem statement

Example 9-2 of the book: *Performance of a Single-Stage Absorption System*.
A single-stage ammonia-water absorption refrigerator operates with
absorber/condenser exit temperatures of 40 °C and an evaporator exit
temperature of −10 °C. The rectifier delivers an almost pure ammonia vapour
(x[9] = 0.9996), the concentration difference across the generator is
DELTAx = 0.1 and the solution circulation through the pump is 1 kg/s. The
solution heat exchanger has an effectiveness of 0.8 and the pump an
efficiency of 1.0. Compute all state points, the heat rates and the COP.

## Model

The cycle states are numbered as in the book's diagram window: rich solution
1→2 (pump) →3 (solution heat exchanger) → desorber; poor solution 4→5
(solution heat exchanger) →6 (expansion valve) → absorber; vapour 7
(generator exit) → rectifier → 9 (nearly pure NH3 vapour) → condenser → 10 →
expansion valve → 12 →13 (evaporator, exit quality 0.975); rectifier runoff
8 returns to the desorber. Pressures change only across the valves; the high
and low pressures follow from saturation at the condenser exit (T = 40 °C,
x[10], Q = 0) and the evaporator exit (T = −10 °C, x[13] = 0.9996,
Q = 0.975). The rectifier closure follows the example: T[8] = T[7] and
x[8] = x[3]. Mass, ammonia and energy balances on every component; the
solution heat exchanger is an effectiveness model (`PROCEDURE shx`;
`Min()` is the smaller of the two capacity rates, not an optimiser). Each
NH3H2O state point is fixed by three properties (T, P, x, Q, h…).

Inputs: m_dot[1] = 1 kg/s, eta_pump = 1.0, epsilon_shx = 0.8, T[1] = T[10] =
40 °C, T[13] = −10 °C, x[9] = 0.9996, DELTAx = 0.1, qualities Q[1], Q[4],
Q[7], Q[8], Q[9], Q[10], Q[13]. Outputs: all state points (h[i], T[i],
x[i], Q[6], Q[12]), heat rates Q_dot_des/rect/abs/cond/evap/shx, W_dot_pump,
f, P_high, P_low, COP_1, COP_2, DELTAt_glide.

## How to run

```
coolsolve nh3h2o_absorption_rectifier.eescode
```

Converges from default guesses (104 iterations); `.initials` holds the EES
stored solution values (pressures and enthalpies converted to Pa/J) and
speeds the solve up (46 iterations).

## Results

| Quantity | EES (stored) | CoolSolve |
|---|---:|---:|
| COP_2 = Q̇_evap/Q̇_des | 0.44874 | 0.440167 |
| COP_1 (with pump power) | 0.44671 | 0.438171 |
| Q̇_evap | 146 941 W | 144 096 W |
| Q̇_des | 327 451 W | 327 366 W |
| Q̇_abs | 273 867 W | 273 105 W |
| Q̇_cond | 159 170 W | 156 589 W |
| Q̇_rect | 51 435 W | 43 259 W |
| Q̇_shx | 257 866 W | 268 928 W |
| Ẇ_pump | 1 487.9 W | 1 491.8 W |
| f (circulation ratio) | 7.0338 | 7.1352 |
| x[1] / x[4] | 0.39622 / 0.29622 | 0.38608 / 0.28608 |
| T[4] (generator exit) | 124.24 °C | 124.83 °C |
| T[7] = T[8] (rectifier) | 101.92 °C | 102.35 °C |
| P_high / P_low | 1 555 700 / 286 435 Pa | 1 554 714 / 286 146 Pa |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/ + one-line caption -->

## Verification

The CoolSolve solution was compared with the EES stored solution of the
binary `Ex9_2.EES` inside `ex9_2.eez` (`compare_solution.py --ees-units`,
105 common variables; the EES reference is in kPa/kJ, converted by the
tool). COP within 1.91e-02, temperatures within 4.67e-03, mass fractions
within 3.42e-02, heat rates within 1.62e-02 except Q̇_rect: **1.59e-01**
(printed maximum, kept). Deviations come from the NH3H2O property backend,
quantified with direct property calls at identical inputs (EES stored input
values, CoolSolve values):

| Property call (identical inputs) | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| MassFraction(T=40, P=286435, Q=0) | 0.39622 | 0.38625 | 2.52e-02 |
| Pressure(T=−10, x=0.9996, Q=0.975) | 286 435 Pa | 286 146 Pa | 1.01e-03 |
| Pressure(T=40, x=0.9996, Q=0) | 1 555 700 Pa | 1 554 714 Pa | 6.35e-04 |
| MassFraction(T=101.922, P=1555700, Q=1) | 0.95821 | 0.95698 | 1.29e-03 |
| Temperature(P=1555700, x=0.29622, Q=0) | 124.24 °C | 122.48 °C | 1.42e-02 |
| Δh_evap = h(−10 °C, Q=0.975) − h(40 °C, Q=0), x=0.9996 | 1 033 547 J/kg | 1 028 152 J/kg | 5.22e-03 |

EES uses the Ibrahim & Klein (1993) ammonia-water formulation, CoolSolve the
IAPWS G4-01 guideline (Tillner-Roth & Friend 1998); the composition of the
saturated liquid at 40 °C differs by 2.5 % between the two, and the cycle
adjusts its composition level accordingly (x[1], then f and the flow rates).
The rectifier duty Q̇_rect is a small difference of large enthalpy streams
(ṁ₇h₇ − ṁ₉h₉ − ṁ₈h₈ ≈ 0.15·1.85e6 − 0.14·1.65e6 − 0.011·0.36e6), so the
backend shift amplifies to 15.9 %; the whole-cycle energy balance closes to
0 W in CoolSolve (checkQ). Excluded from the comparison: h[i] and s[i]
(absolute NH3H2O enthalpy/entropy, different reference state in EES and
CoolProp, deviations up to 1.7 as printed) and checkQ (balance residual; its
EES stored record is flagged suspect by the extraction — substituted into
the equation it gives −8.59 kW, a stale mix of records — no weight given).

## Source and attribution

Example 9-2 of K. E. Herold, R. Radermacher and S. A. Klein, *Absorption
Chillers and Heat Pumps*, CRC Press, 2nd edition, 2015. EES file `ex9_2.ees`
by S. A. Klein / F-Chart Software, distributed in the
EES-Community/ees-examples repository (`Case_Study/ex9_2.eez`, MIT;
https://github.com/EES-Community/ees-examples). Credit: (c) F-Chart Software
/ S. A. Klein, MIT via EES-Community/ees-examples.

## Conversion log

- **2026-11-15 — import**: `ees_extract.py` on the binary `Ex9_2.EES`
  extracted from the `ex9_2.eez` zip (EES X11.926; 159 variable records, no
  tables; the stored-solution records of states 11, 14, 15 and of `s[...]`,
  `v[...]` are stale leftovers of sibling examples, no weight). Unit system
  `SI C kPa kJ mass` converted by hand to SI-°C-Pa-J: the equations are
  homogeneous (pressures and enthalpies come only from property calls;
  inputs are °C, kg/s and dimensionless), so no numeric value changed — only
  the `$UnitSystem` and `$TabStops` directives were removed and the unit
  annotations updated. Comments kept in English, typos fixed
  ("capcitance", "efectiveness", "ansd"); three comment labels corrected
  without touching equations: the rectifier fraction balance was labelled
  "energy balance" (it is the ammonia balance), the condenser balance
  "energy balance on evaporator" (copy-paste from the next block), and
  state 7 "saturated liquid" (Q[7] = 1: saturated vapour). `PROCEDURE shx`
  kept as in the original; `Min()` is the smaller of two numbers.
- **2026-11-15 — diagram-ready**: post-processing block added (no effect on
  the results): `s[i] = Entropy(NH3H2O,P=P[i],X=x[i],H=h[i])` for the 13
  states (the example numbers states 1–10 and 12–13; a `DUPLICATE i=1,13`
  would create undefined `x[11]`/`h[11]`, so states 12–13 are written out).
- **Level**: equations 105 → 1 (50–300); largest block 7 → 1 (6–30);
  procedures/arrays → 1; ≥ 3 coupled components → 1; no semi-empirical or
  off-design physics → 0; converges from default guesses → 0; score 4 →
  level 3.

## Limitations and CoolSolve gaps

None: the native file solves in CoolSolve. The physics is limited by the
NH3H2O formulation (IAPWS G4-01 vs EES Ibrahim & Klein 1993, see
Verification) and by the imposed rectifier closure (T[8] = T[7],
x[8] = x[3], as in the original example). No `missing_features`.

## Related models

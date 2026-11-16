# Single-stage ammonia-water absorption cycle with rectifier heat recovery

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0361`

A single-stage (single-effect) NH3H2O absorption refrigeration cycle solved as
one simultaneous system of 127 equations (Herold, Radermacher and Klein,
*Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015, Example 9.5):
the cycle of Example 9.3 (`CSL-0360`, condensate precooler) with one change —
**all the rectifier heat is recovered into the rich solution** instead of being
rejected: the solution stream 2 is heated to 16 by the rectifier duty and
enters the solution heat exchanger at 16.

Given the heat rejection temperatures (absorber and condenser at 40 °C), the
evaporator temperature (−10 °C) and the design goals (rectified vapour
x[9] = 0.99, concentration difference DELTAx = 0.1), the model computes all
state points, the component heat rates and the COP.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O |
| **Size** | 127 equations (largest block: 7) |
| **Source** | F-Chart EES example `ex9_5.ees` (EES-Community/ees-examples, Case_Study) |
| **Authors** | S. A. Klein (F-Chart Software); Example 9.5 of Herold, Radermacher & Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015 |
| **License** | MIT |
| **CoolSolve** | 0.4.0@a53de60 — native file solves and was compared with the stored solution (see Verification) |

## Problem statement

Example 9.5 of the book: *Performance of a Single-Stage Absorption System With
a Condensate Precooler and Rectifier Heat Exchange* (the original file title
has the typos "Witho … andd"). Inputs (as in the original): m_dot[1] = 1 kg/s,
eta_pump = 1, solution heat exchanger effectiveness epsilon_shx = 0.8,
condensate precooler effectiveness epsilon_sc = 0.8, T[1] = T[10] = 40 °C
(absorber / condenser heat rejection), T[13] = −10 °C (evaporator), saturated
liquid at states 1, 4, 8, 10, saturated vapour at 7, 9, evaporator outlet
quality Q[13] = 0.975, rectifier design goal x[9] = 0.99 and concentration
difference x[1] − x[4] = DELTAx = 0.1.

## Model

The states carry arrays m_dot[i], P[i], T[i], h[i], x[i], Q[i] (states 1–14
plus 16; there is no state 15 in the original). Components (mass, ammonia and
energy balances, as in the original): pump, solution heat exchanger, desorber,
rectifier, two expansion valves, condenser, evaporator, condensate precooler,
absorber. Compared to Example 9.3 (`CSL-0360`), the rectifier energy balance
has no rejected duty: `m_dot[7]*h[7] = m_dot[9]*h[9] + m_dot[8]*h[8] +
m_dot[2]*(h[16] - h[2])` — the coolant stream 2 → 16 (same fluid, m_dot[16] =
m_dot[3] = m_dot[2]) takes the rectifier heat and re-enters the solution heat
exchanger at T[16]; `Q_dot_des` is the only external driving heat.

The solution heat exchanger and the condensate precooler use the `PROCEDURE
shx` of the original: an effectiveness model written with capacity rates
C_dot = m_dot·cp and `Min()` — the smaller of the two capacity rates, *not* an
optimiser (it parses and evaluates in CoolSolve as it is).

Pressures are set by the saturation of the solution: P_high from the condenser
conditions (T[10], x[10], Q[10] = 0), P_low from the evaporator exit
(T[13], x[13], Q[13] = 0.975); pressure changes only across the valves. The
rectified refrigerant keeps 1 % water (x[9] = 0.99), so the evaporator
temperature glide is large (17.7 K in EES, 17.3 K in CoolSolve) and T3s (the
saturation temperature of the solution at state 3) is an extra output of the
original.

The state-point arrays of the original are kept; a post-processing block adds
s[1..14], s[16] = Entropy(NH3H2O, P, x, h) for the thermodynamic diagrams (no
effect on the results).

## How to run

The native file is the faithful transcription of the example and solves in
CoolSolve as it is. It takes its guesses from `.initials` (values stored by
EES, pressures and enthalpies converted to Pa/J, stale records of states 15/17
dropped — 148 entries):

```bash
coolsolve ./nh3h2o_absorption_rectifier_heat.eescode   # solves (59 iterations)
```

## Results (native file vs EES stored solution)

| Quantity | EES | CoolSolve | rel. diff as printed |
|---|---:|---:|---:|
| COP_1 (with pump power) | 0.415236 | 0.410117 | 1.23e-02 |
| COP_2 (without pump power) | 0.4171 | 0.411954 | 1.23e-02 |
| Q_dot_evap | 146.77 kW | 145.21 kW | 1.06e-02 |
| Q_dot_des (driving heat) | 351.88 kW | 352.50 kW | 1.78e-03 |
| Q_dot_abs | 348.13 kW | 348.64 kW | 1.48e-03 |
| Q_dot_cond | 152.10 kW | 150.65 kW | 9.50e-03 |
| Q_dot_shx | 302.37 kW | 307.67 kW | 1.72e-02 |
| Q_dot_precooler | 17.03 kW | 16.99 kW | 2.27e-03 |
| W_dot_pump | 1579.34 W | 1578.49 W | 5.4e-04 |
| P_high | 1539.88 kPa | 1538.01 kPa | 1.22e-03 |
| P_low | 131.88 kPa | 134.75 kPa | 2.13e-02 |
| P_ratio | 11.6768 | 11.4141 | 2.25e-02 |
| f (circulation ratio) | 8.0994 | 8.1596 | 7.38e-03 |
| x[1] (strong solution) | 0.28006 | 0.274042 | 2.15e-02 |
| x[4] (poor solution) | 0.18006 | 0.174042 | 3.34e-02 |
| x[7] (vapour at generator exit) | 0.872551 | 0.870187 | 2.71e-03 |
| T[4] (generator exit) | 152.61 °C | 151.27 °C | 8.79e-03 |
| T[9] (rectified vapour) | 76.64 °C | 76.09 °C | 7.14e-03 |
| T[16] (SHX inlet after rectifier recovery) | 54.97 °C | 54.66 °C | 5.57e-03 |
| T[11] (subcooled condensate) | 11.29 °C | 11.03 °C | 2.29e-02 |
| DELTAt_glide (evaporator) | 17.72 K | 17.25 K | 2.64e-02 |
| Q[6] (quality after solution valve) | 0.024094 | 0.022863 | 5.11e-02 |
| checkQ (whole-cycle balance) | −3.4e-07 J | −6.3e-06 W | — |

The whole-cycle energy balance (Q_dot_des + Q_dot_evap + W_dot_pump =
Q_dot_cond + Q_dot_abs; the recovered rectifier heat is internal) closes to
−6.3e-06 W on 499.3 kW in CoolSolve (EES: −3.4e-07 J); the absorber residual
balances err_absmass and err_absammonia are ~1e-15.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/nh3h2o_absorption_rectifier_heat_ph.png)  + one-line caption -->

## Verification

The native file was solved in CoolSolve and compared with the EES stored
solution of the binary `Ex9_5.EES` inside the `.eez` companion
(`compare_solution.py … --ees-units`, 126 common variables, 96 differ at
rtol=0.001). COP within 1.3 %, heat rates within 1.8 %, pressures within
2.2 %, temperatures within 2.4 %; the mass fractions differ by up to 3.34e-02
(a few percent), explained by the NH3H2O **property backend**, evidenced by
identical property calls at identical inputs in the comparison itself:

| Property call (identical inputs) | EES | CoolSolve (CoolProp) | rel. diff |
|---|---:|---:|---:|
| P_high at T = 40 °C, x[10] = x[9] = 0.99, Q = 0 (bubble) | 1539.88 kPa | 1538.01 kPa | 1.22e-03 |
| P_low at T = −10 °C, x = 0.99, Q = 0.975 | 131.875 kPa | 134.746 kPa | 2.13e-02 |

EES uses its own NH3H2O formulation, CoolSolve the CoolProp ammonia-water
model; at the refrigerant-rich composition x = 0.99 the two-phase (dew-point
region) saturation pressure at identical inputs already differs by 2.13e-02.
The cycle then adjusts the composition level (x[1] from the saturation at
T[1] = 40 °C and P_low, x[4] = x[1] − 0.1) and every downstream state, so
x[1] (2.15e-02), x[4] (3.34e-02 — the fixed DELTAx = 0.1 amplifies the
relative difference on the smaller value), the composition-dependent cp_45 and
cp_163, Q_dot_shx (1.72e-02), Q[6] (5.11e-02, a quality read from the shifted
dome at h[6] = h[5] and x[6] = x[4]) and DELTAt_glide (2.64e-02) inherit the
same shift. All other cycle quantities stay within 1.5 %.

Excluded from the comparison, as printed by `compare_solution.py`:
- `h[i]`, `s[i]`, `swp` — absolute NH3H2O enthalpies and entropies carry a
  different reference state in EES and CoolProp (offsets of the order of
  1e5 J/kg on h, 1e3 J/kg-K on s); enthalpy *differences* and derived results
  are compared instead. The EES `v[2..14]`, `Q[2]`, `Q[3]`, `Q[5]`, `Q[11]`,
  `Q[14]` records are moreover stale: the file computes none of them
  (earlier version of the exercise); `v[1]` is computed and agrees to 2.83e-03;
- `cp_1011`, `cp_1314`, `cp_163` — the reference CSV stores their units as
  `J/g-K`, which `--ees-units` does not convert (tool bug
  `CS-BUG-COMPARE-JGK`, already registered): the printed 9.99e-01 is an
  artifact; converted by hand, the true diffs are 3.8e-03 (cp_1011),
  5.1e-03 (cp_1314) and 3.4e-02 (cp_163, composition-dependent as cp_45,
  printed 2.66e-02 since stored in kJ/kg-K);
- `checkQ` — balance residual, closes in both tools (−3.4e-07 J / −6.3e-06 W
  on 499 kW);
- `C_dot_min` — procedure-local variable (not an output of the model).

Verification summary: verified with the printed tolerance 5.11e-02 as the
maximum over the compared set (Q[6], a two-phase quality inheriting the
documented composition shift); the largest mass-fraction difference is
3.34e-02 (a few percent, as in `CSL-0360` at 3.42e-02), fully accounted for by
the backend difference at identical inputs (same quantity, two-phase region:
2.13e-02).

## Source and attribution

Source: F-Chart Software EES example `ex9_5.ees`
(https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/ex9_5.ees,
MIT, (c) F-Chart Software / S. A. Klein), Example 9.5 of Herold, Radermacher
and Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 2nd ed., 2015.
The binary `.EES` inside the `.eez` companion (EES X11.926, licence of
S. A. Klein, F-Chart Software) provided the stored solution used as reference.
Candidate row EEX-111 of `sources/ees_examples/inventory.csv`.

## Conversion log

- **2026-11-15 — import**: the `.eez` companion (a zip) was extracted to the
  inner `Ex9_5.EES` binary first, then `ees_extract.py`: 162 variables with
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
  ×1000; 148 entries, stale records of states 15–17 dropped) and by
  `--ees-units` in the comparison.
- **2026-11-15 — comments**: comment typos fixed (*capcitance* → capacitance,
  *efectiveness*/*efficency* → effectiveness/efficiency, *equlibrium* →
  equilibrium, *ansd* → and, "esc" → epsilon_sc); comment/line mismatches of
  the original corrected as in `CSL-0360` (the `T[9]` line said "Enthalpy
  obtained as well" and the `Q[12]` line "Temperature obtained as well",
  swapped; the state-7 comment said "assumed to be saturated liquid" while
  Q[7] = 1 makes it the saturated **vapour** at the generator exit; the cp
  comments "stream 2-3"/"stream 4-5", copied from the original solution heat
  exchanger, renamed to streams 16-3, 4-5, 10-11 and 13-14) — comment-only
  corrections, no effect on the results. Comments otherwise paraphrase the
  original. Standard header added (23 lines).
- **2026-11-15 — post-processing**: `DUPLICATE i=1,14 s[i]=Entropy(NH3H2O,P=…)`
  plus `s[16]` (states 1–14 and 16 exist in the original; there is no state 15)
  added at the end for the thermodynamic diagrams (P[i], T[i], h[i] already
  exist as state points in the original); no effect on the results.
- **PROCEDURE shx**: kept exactly as in the original (equations unchanged),
  including `Min()` — the smaller of the two capacity rates C_dot_c and
  C_dot_h, not an optimiser; capacity-rate comments now carry their unit
  [W/K].
- **No property-call rewrite**: no call uses an unsupported input pair and no
  call with an unknown quality failed (no `CS-BUG-PROP-QLIMIT` trigger);
  `T[16]` is read with the supported (P, H, X) triple.
- **Level**: equations 127 → 1; largest block 7 → 1; PROCEDURE + arrays → 1;
  ≥ 3 coupled components (desorber, rectifier, absorber, SHX, precooler,
  condenser, evaporator, pump, two valves) → 1; no off-design/dynamics → 0;
  needs converted `.initials` (implicit loops) → 1. Score 5 → **level 3**
  (matches the level_guess 3 of the inventory row).

## Niche

The library has the basic single-effect chiller `CSL-0249` (written for the
library), the ideal-cycle `CSL-0347`, the two-stage `CSL-0352` (Example 10.1),
the absorber-recirculation `CSL-0354` (Example 9.6, which preheats the rich
solution *by the rectifier at the absorber side*), the Example 9.3 precooler
cycle `CSL-0360` and the LiBr-H2O `libr_water_absorption_chiller`. This model
adds the Example 9.5 topology of the same textbook: the rectifier heat is
recovered into the rich solution **upstream of the solution heat exchanger**
(stream 2 → 16, no rejected rectifier duty), a configuration between `CSL-0360`
and `CSL-0354`, with the less pure refrigerant of the Herold examples
(x[9] = 0.99, 1 % water, evaporator glide 17.7 K) and the verified comparison
against the stored solution of the F-Chart example file.

## Related models

- `CSL-0360` nh3h2o_absorption_precooler: the same cycle without rectifier
  recovery (rectifier heat rejected), Example 9.3 of the same book — the
  closest model.
- `CSL-0354` nh3h2o_absorption_recirculation: Example 9.6 of the same book,
  precooler plus absorber solution recirculation and rectifier preheating
  (16 states).
- `CSL-0249` nh3h2o_absorption_chiller: single-effect NH3H2O absorption
  chiller with rectifier and solution heat exchangers (written for the
  library).

## Limitations and CoolSolve gaps

None: the native file solves as extracted (after the by-hand unit
conversion); no CoolSolve gap blocks it. Absolute NH3H2O enthalpies and
entropies use a different reference state in EES and CoolProp — a property
backend difference, not a gap.

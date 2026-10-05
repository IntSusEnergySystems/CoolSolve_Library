# Steam Rankine cycle with regenerative extraction

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0029`

A 60 MW steam power plant with a regenerative extraction from the turbine at
25 bar: the extracted steam preheats the feedwater in an open (mixing)
feedwater heater, whose outlet is saturated water. From the given net
electrical output, the model computes the steam flow rate, the extraction
flow rate, the boiler power, the cooling-water flow rate and the plant
thermal efficiency. The seven state points are stored in arrays, ready for
the T-s or P-h diagram.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water |
| **Size** | 73 equations, largest block 4 (69 explicit): 45 for the model, 28 for the diagram state points |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 7, exercise 3 (EES file `rankine2.EES`) |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory) — exercise of the course *Machines et systèmes thermiques* |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

Same 60 MW steam plant as `rankine_cycle_60mw` (CSL-0004): live steam at
70 bar and 500 °C, condenser at 0.1 bar, boiler pressure drop of 4 bar,
boiler efficiency of 90 %, turbine-stage isentropic efficiency of 0.83,
alternator efficiency of 95 %, pump isentropic efficiency of 0.85,
pump-motor efficiency of 0.94, cooling-water temperature rise limited to
10 K. A steam extraction is taken from the turbine at 25 bar and sent to an
open feedwater heater (mixing preheater with negligible losses); at the
heater outlet the water is saturated. What are the new flow rates and the
new thermal efficiency of the cycle?

## Model

Standard Rankine cycle with one regenerative extraction, steady flow,
kinetic and potential energy neglected:

- **HP turbine stage** (full flow): $h_{3a} = h_3 - \eta_{is,t}(h_3 - h_{3a,s})$
  with $s_{3a,s} = s_3$ at the extraction pressure $P_{3a}$;
- **LP turbine stage** (flow without extraction):
  $h_4 = h_{3a} - \eta_{is,t}(h_{3a} - h_{4s})$ with $s_{4s} = s_{3a}$;
- **open feedwater heater**: $( \dot m - \dot m_s)\,h_2 + \dot m_s\,h_{3a} =
  \dot m\,h_{2a}$, with $h_{2a}$ saturated water at $P_{2a} = P_{3a}$;
- **pumps**: $h_2 = h_1 + (h_{2s} - h_1)/\eta_{is,p}$ (pump 1: condenser to
  heater pressure) and likewise for pump 2 (heater to boiler pressure
  plus $\Delta p$);
- **boiler**: $\eta_{b}\,\dot Q_{b} = \dot m\,(h_3 - h_{2b})$;
- **plant**: $\dot W_{el} = \eta_{a}\,\dot W_t$,
  $\eta = \dot W_{el}/(\dot Q_{b} + \dot W_{p})$.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `W_dot_el` net electrical power | 60 MW | `M_dot_steam` steam flow | 73.79 kg/s |
| `P_3` live-steam pressure | 70 bar | `M_dot_steam_s` extraction flow | 19.13 kg/s |
| `T_3` live-steam temperature | 500 °C | `Q_dot_boiler` boiler heat release | 200.25 MW |
| `P_3a` extraction pressure | 25 bar | `Q_dot_cd` condenser heat rejection | 117.74 MW |
| `p_cd` condenser pressure | 0.1 bar | `M_dot_w_cd` cooling-water flow | 2812.7 kg/s |
| `DELTA_p` boiler pressure drop | 4 bar | `eta` thermal efficiency | 29.85 % |
| `epsilon_s_t` / `eta_a` | 0.83 / 0.95 | `x_4` turbine-outlet quality | 0.901 |
| `epsilon_s_p` / `eta_m` | 0.85 / 0.94 | `W_dot_t` / `W_dot_p` | 63.16 / 0.77 MW |
| `DELTAT_w_cd` water temperature rise | 10 K | | |

## How to run

Open `rankine_cycle_regenerative_extraction.eescode` in the CoolSolve GUI
and press *Solve*, or from a terminal:

```bash
coolsolve ./rankine_cycle_regenerative_extraction.eescode
```

No guess values needed (converges from defaults in 154 iterations). Set
`P_3a = 14E5` to reproduce the previous exercise (extraction at 14 bar).

## Results

| Point | T [°C] | p [bar] | h [kJ/kg] | s [kJ/kg-K] |
|---|---:|---:|---:|---:|
| 1 — condenser outlet / pump 1 inlet | 45.8 | 0.10 | 191.8 | 0.649 |
| 2 — pump 1 outlet / heater inlet | 46.0 | 25.0 | 194.8 | 0.651 |
| 3 — heater outlet / pump 2 inlet | 224.0 | 25.0 | 961.9 | 2.554 |
| 4 — pump 2 outlet / boiler inlet | 225.2 | 74.0 | 968.8 | 2.556 |
| 5 — boiler outlet / turbine inlet | 500 | 70.0 | 3411.4 | 6.800 |
| 6 — extraction / LP-turbine inlet | 361.7 | 25.0 | 3153.6 | 6.885 |
| 7 — turbine outlet / condenser inlet | 45.8 | 0.10 | 2346.1 | 7.403 |

Main results: steam flow 73.79 kg/s (of which 19.13 kg/s extracted),
boiler heat release 200.25 MW, thermal efficiency 29.85 %, cooling water
2812.7 kg/s.

The native state arrays `T[i]`, `P[i]`, `h[i]`, `s[i]` (i = 1…7) plot the
cycle directly in the CoolSolve *Diagram* tab (*Overlay array path*,
*Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle,
     figures/rankine_cycle_regenerative_extraction_ts.png -->

## Verification

**Faithful import vs EES.** The model was compared with the solution stored
in the source EES file (`compare_solution.py`, default tolerance): all 44
common variables agree within the default tolerance `rtol=0.001`
(`44 common variables, 0 differ (rtol=0.001); only in EES: 0`); at
`rtol=1e-9` the largest deviation is 5.5·10⁻⁴ (on `M_dot_steam_s`),
typical of the EES 7.2 vs CoolProp (IAPWS-IF97) water-property
formulations. Derived results: η 0.29853 / 0.29847, `M_dot_steam` 73.80 /
73.79 kg/s, `M_dot_steam_s` 19.14 / 19.13 kg/s, `Q_dot_boiler` 200.22 /
200.25 MW. The 29 variables present only in CoolSolve are the 28
post-processing state-array elements plus `P_2b` (7.4 MPa, as in the
equations; EES stored no value for it).

## Source and attribution

Exercise solution by **Vincent Lemort** (ULiège Thermodynamics Laboratory)
for the course *Machines et systèmes thermiques* (repetition 7,
exercise 3, 2005): the header comment reads `VL050211 / Répétition 7,
exercice 3 / Que deviendrait le rendement du cycle si le soutirage de
l'exercice précédent était effectué à 25 bar ?` (`VL` = Vincent Lemort;
the `{$ID$}` tag is the laboratory licence).

Source file (EES 7.210, comments in French, SI-C-Pa-J), CoolSolve
`misc/EES_ok.zip`: `EES_ok/rankine2.EES` (inventory candidate `CSX-037`
is the CoolSolve example derived from it).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-C-Pa-J, no conversion needed; the EES licence tag
  was removed. Comments translated to English and standard header added.
  Property-call argument keywords normalised to uppercase (`p=` → `P=`,
  `t=` → `T=`, `s=`/`h=`/`x=` unchanged); fluid name kept as `water`.
  The `"!!"…"!!"` EES comment markers inside identifiers (e.g.
  `P_2"!!"b"!!"` = `P_2b`) are kept as in the original — CoolSolve parses
  them. Faithful import verified (see above).
- **2026-10-05 — extraction pressure.** In the EES file the default-run line
  is commented out (`{P_3a=14E5}`, "car dans table paramétrique": the
  14 bar value of the previous exercise, driven by a parametric table that
  is no longer in the file) and the stored solution is the 25 bar run asked
  in the exercise (`P_3a` = 2.5 MPa, `eta` = 0.2985). The library model sets
  `P_3a = 25E5` as the default run, as in the stored solution. The
  CoolSolve example `rankine2.eescode` (CSX-037) instead has `P_3a = 14E5`
  uncommented while its header announces 25 bar: it solves the 14 bar case
  (`eta` = 0.3033) and stays in the CoolSolve repository as a test case.
- **2026-10-05 — diagram support**: block of 28 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`, i = 1…7) added at the end of
  the model for the CoolSolve diagrams; the results of the model are
  unchanged (44/44 EES variables still agree).
- **2026-10-05 — triage of the thermo_models group.** `DG-0107` (TM-0444,
  TM-0445, TM-0520, TM-0521, TM-0548) is the same regenerative-extraction
  system as the previous exercise (14 bar extraction, kPa/kJ, French,
  component-by-component with state arrays, 0.2 bar condenser): all five
  rows are marked `duplicate` of this model (same system, other input
  values — reproducible with `P_3a = 14E5`).

## Limitations and CoolSolve gaps

- The cycle is idealised: no reheat, no turbine or condenser pressure
  losses beyond the boiler drop, no heater heat losses; the heater outlet
  is taken as saturated water at the extraction pressure.
- No CoolSolve gap blocks or affects this model.

## Related models

- `CSL-0004` *rankine_cycle_60mw*: the simple Rankine cycle this exercise
  builds on (same plant without extraction, 0.2 bar condenser, 0.85 turbine
  efficiency) — different level of detail (no regeneration), linked both ways.
- See also the CoolSolve example `rankine2.eescode` (CSX-037): same EES
  origin, solved at 14 bar (header announces 25 bar).

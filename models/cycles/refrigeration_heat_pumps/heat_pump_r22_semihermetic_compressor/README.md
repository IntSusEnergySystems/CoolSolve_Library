# R22 heat pump with a semi-hermetic compressor model

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0033`

A R22 heat pump whose compressor is a semi-hermetic (enclosed) reciprocating
machine: the electromechanical losses of the machine do not leave it but reheat
the incoming fresh charge, so the refrigerant is compressed from the reheated
state. The compressor is further described by a clearance-factor volumetric
efficiency and a swept volume flow rate, and the evaporator and the condenser
are semi-isothermal (isothermal on the refrigerant side) heat exchangers rated
by the effectiveness–NTU method against water flow rates. The model closes on
the saturation pressures of the evaporator and condenser temperatures and
returns the COP, the heating capacity, the compressor power and the
refrigerant flow rate of the machine. It is the exercise of *répétition 10,
exercise 1* of the ULiège *Machines et systèmes thermiques* course.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R22 (CoolProp properties); Water (secondary circuits, properties at the mean water temperature) |
| **Size** | 75 equations, largest block: 39 (evaporator, condenser and compressor) |
| **Source** | ULiège *Machines et systèmes thermiques*, répétition 10, exercise 1 — CoolSolve example `heat_pump_MSTh_SB_R10` + original EES file |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory, EES solution); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the solution stored in the original EES file (needs the shipped `.initials`) |

## Problem statement

A water-cooled heat pump working with R22 has a semi-hermetic compressor with
the following known parameters: constant electromechanical losses
`W_dot_loss_0 = 1294` W, proportional loss factor `alpha = 0.228`,
clearance factor `C = 0.125`, swept volume flow rate `V_dot_s = 0.0233` m³/s;
the evaporator and the condenser have overall conductances
`AU_ev = 7000` W/K and `AU_cd = 15000` W/K. The water flow rates are
2.4 kg/s (evaporator, leaving at 10 °C) and 2.2 kg/s (condenser, entering at
40 °C); there are 5 K of superheat at the evaporator outlet and 3 K of
subcooling at the condenser outlet. Because the compressor is semi-hermetic,
the losses reheat the fresh charge before compression. Compute the heating
capacity, the compressor power and the COP of the machine.

The original also asks which closure of the refrigerant side of the condenser
is the better one: the energy balance `Q_dot_cd = M_dot_r*(h_2 − h_3)`, or the
flow rate deduced from the compressor characteristics
(`M_dot_r = epsilon_vol_1*V_dot_s/v_su_1`). The author keeps the second one
(see *Model* below); both give slightly different results.

## Model

Four state points (1: evaporator outlet, 2: compressor outlet, 3: condenser
outlet, 4: evaporator inlet), the pressures of the two exchangers being the
saturation pressures of the evaporator and condenser temperatures:

- `P_ev = PRESSURE(R22, T=T_ev, x=0.5)`, `P_cd = PRESSURE(R22, T=T_cd, x=0.5)`
  (any quality in [0, 1] gives the same pressure);
- evaporator outlet: saturated vapour, 5 K above `T_ev`;
  condenser outlet: subcooled liquid, 3 K below `T_cd`;
- expansion: isenthalpic, `h_4 = h_3`;
- evaporator duty on the refrigerant side `Q_dot_ev = M_dot_r*(h_1 − h_4)`;
- **compressor**: semi-hermetic reheat of the fresh charge,
  `Q_dot_loss = Q_dot_rech = M_dot_r*(h_su_1 − h_su)`, the losses following
  `W_dot_loss = W_dot_loss_0 + alpha*W_dot_in`, so
  `W_dot_cp = W_dot_loss + W_dot_in = W_dot_loss_0 + (1 + alpha)*W_dot_in`;
  internal isentropic compression from the reheated state to `P_cd`
  (`h_ex_cp_s_1 = ENTHALPY(R22, s=s_su_1, P=P_cd)`);
- **volumetric efficiency**: `epsilon_v = 1 − C*(r_v − 1)` with
  `r_v = v_su/v_ex`, closed by the definition `V_dot_su = epsilon_v*V_dot_s`.
  This relation (instead of the condenser balance) is what fixes `M_dot_r`;
- machine energy balance `Q_dot_ev + W_dot_cp = Q_dot_cd`;
- **evaporator and condenser**: semi-isothermal ε-NTU rating,
  `Q = epsilon*C_dot_min*(T_water,in − T_refrigerant)` with
  `C_dot_min = M_dot_w*cp_w` (the refrigerant side is isothermal, hence an
  infinite capacity rate there), `NTU = AU/C_dot_min` and
  `epsilon = 1 − exp(−NTU)`; the same duty is written on the water side,
  `Q = M_dot_w*cp_w*(T_water,in − T_water,out)`, which gives `T_w_ev_su` and
  `T_w_cd_ex`.

The global isentropic efficiency of the compressor,
`epsilon_s = M_dot_r*(h_ex_s − h_su)/W_dot_cp`, is reported as an extra result;
it is not in the original but in the questions file of the same exercise
(`thermo_models` TM-0160), from which it is taken.

Two alternatives written by the author are kept as comments, as in the
original: the reheat with a constant vapour cp
(`Q_dot_rech = M_dot_r*cp_r*(T_su_1 − T_su)`) and the whole compressor model
*without* the semi-hermetic design (adiabatic machine, no reheat of the fresh
charge).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `W_dot_loss_0` / `alpha` | 1294 W / 0.228 | `COP` | 3.311 |
| `C` / `V_dot_s` | 0.125 / 0.0233 m³/s | `Q_dot_u` (= `Q_dot_ev`) heating capacity | 57.05 kW |
| `AU_ev` / `AU_cd` | 7000 / 15000 W/K | `Q_dot_cd` heat rejected | 74.29 kW |
| `M_dot_w_ev` / `M_dot_w_cd` | 2.4 / 2.2 kg/s | `Q_dot_c` (= `W_dot_cp`) power | 17.23 kW |
| `T_w_ev_ex` / `T_w_cd_su` | 10 / 40 °C | `M_dot_r` refrigerant flow | 0.3824 kg/s |
| `DELTAT_oh` / `DELTAT_sc` | 5 / 3 K | `T_ev` / `T_cd` | 4.36 / 50.04 °C |
| `P_atm` secondary circuits | 101 325 Pa | `P_ev` / `P_cd` | 572.5 / 1944.6 kPa |
| | | `W_dot_loss` (reheat) / `epsilon_v` | 4.253 kW / 0.747 |
| | | `epsilon_s` / `T_su_1` (after reheat) | 0.687 / 24.34 °C |

## How to run

Open `heat_pump_r22_semihermetic_compressor.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./heat_pump_r22_semihermetic_compressor.eescode
```

**The shipped `.initials` file (the guesses stored in the original EES file)
is needed**: without it the 39-equation block (evaporator + condenser +
compressor, the largest in the model) fails to converge — *MaxIterations* —
which is also noted in the header of the CoolSolve example. No
`coolsolve.conf` is required; with the `.initials` the model converges in
4 iterations.

## Results

| Quantity | Value |
|---|---|
| `COP` | 3.311 |
| `Q_dot_ev` = `Q_dot_u` (useful output) | 57.05 kW |
| `Q_dot_cd` (condenser duty) | 74.29 kW |
| `W_dot_cp` = `Q_dot_c` (compressor power) | 17.23 kW |
| `M_dot_r` | 0.3824 kg/s |
| `T_ev` / `T_cd` | 4.36 °C / 50.04 °C |
| `T_w_ev_su` / `T_w_cd_ex` | 15.67 °C / 48.08 °C |
| `W_dot_loss` = `Q_dot_rech` | 4.253 kW (24.7 % of the electrical power) |
| `epsilon_v_1` / `epsilon_s` | 0.747 / 0.687 |

The losses of the semi-hermetic machine (4.25 kW) heat the fresh charge from
9.36 °C to 24.34 °C before it is compressed; the refrigerant leaves the
compressor at 89.6 °C. The temperature lifts of the two water circuits are
5.7 K (evaporator, 10 → 15.7 °C) and 8.1 K (condenser, 40 → 48.1 °C).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7):
     ![P-h diagram of the cycle](figures/heat_pump_r22_semihermetic_compressor_ph.png)
     P-h diagram of the cycle (state points `h[i]`/`P[i]` at the end of the model) -->

## Verification

Reference: the solution stored in the EES original of the exercise,
`MSTH-SB-R10-EX1.EES` (EES 7.458, `thermo_models` TM-0154, 55 stored
variables), compared with `tools/compare_solution.py` (rtol = 0.001), which
prints:

> 55 common variables, 19 differ (rtol=0.001); only in EES: 0; only in
> CoolSolve: 20

(the 20 variables "only in CoolSolve" are the 16 diagram state points of
`P[i]`, `h[i]`, `T[i]`, `s[i]` and the four added variables of the global
isentropic efficiency, which the original does not have). Largest deviation
over all common variables: **6.6e-03** (`T_ev`).

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `COP` | 3.2955 | 3.31066 | 4.6e-03 |
| `Q_dot_ev` | 56 790.8 W | 57 053.2 W | 4.6e-03 |
| `Q_dot_cd` | 74 023.6 W | 74 286.3 W | 3.5e-03 |
| `W_dot_cp` | 17 232.8 W | 17 233.2 W | 2.0e-05 |
| `M_dot_r` | 0.383217 kg/s | 0.382423 kg/s | 2.1e-03 |
| `T_ev` | 4.38841 °C | 4.35929 °C | 6.6e-03 |
| `T_cd` | 50.0056 °C | 50.0438 °C | 7.6e-04 |
| `P_ev` | 573 191 Pa | 572 491 Pa | 1.2e-03 |
| `P_cd` | 1 943 584 Pa | 1 944 640 Pa | 5.4e-04 |
| `h_1` | 408 553 J/kg | 408 344 J/kg | 5.1e-04 |
| `h_3` | 260 358 J/kg | 259 156 J/kg | 4.6e-03 |
| `h_ex_cp_s_1` | 455 353 J/kg | 455 455 J/kg | 2.2e-04 |
| `W_dot_loss` | 4253.32 W | 4253.39 W | 1.5e-05 |
| `epsilon_v_1` | 0.747287 | 0.746890 | 5.3e-04 |
| `T_su_cp_1` (after the reheat) | 24.3085 °C | 24.3436 °C | 1.4e-03 |

All 19 deviations have the same origin and stay below 0.7 %, the tolerance
expected when the EES and CoolProp fluid models differ
(CoolSolve `docs/ees_import.md` §11, "older EES fluid models … up to a few %"):

1. the R22 properties of EES 7.458 against those of CoolProp — the
   evaporation pressure is 0.12 % lower, the subcooled-liquid enthalpy
   (`h_3`, which enters `Q_dot_ev`) 0.46 % lower;
2. the water specific heat at the mean evaporator water temperature (12.8 °C):
   4184.93 J/(kg·K) in EES 7.458 against 4191.03 J/(kg·K) in CoolProp
   (0.15 %), which shifts `NTU_ev`, `T_w_ev_su` and `Q_dot_ev`.

The compressor power and the losses, which are the results of interest,
agree to 2·10⁻⁵; `COP` and the capacities differ by 0.35–0.46 %, entirely from
the two effects above.

## Source and attribution

Exercise of the ULiège course *Machines et systèmes thermiques* (J. Lebrun,
V. Lemort), repetition session (répétition) 10, exercise 1, solved by
**Stéphane Bertagnolio** (file header `MSTh - SB - R10 - Exercice 1`, EES
7.458). The header of the file also announces a second part of the exercise
("dupliquer les équations avec l'indice 'r', modifier les données, introduire
les équations de régulation"), which is *not* part of this file: it is a
question, and only the solution of exercise 1 is transcribed. The
EES `{$ID$}` tag (`Laboratoire de Thermodynamique, U. de Liege`) is the
laboratory licence, not an author.

The English transcription of this solution is the CoolSolve example
`examples/heat_pump_MSTh_SB_R10.eescode` (S. Quoilin); it stays in the
CoolSolve repository as a test case. This library model is its curated
version, built from the EES original.

Source files (not copied into the library):

- EES original with its stored solution:
  `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 10/MSTH-SB-R10-EX1.EES`
  (inventory candidate `TM-0154`, EES 7.458, 63 variables, no table, no
  external function);
- CoolSolve example: `~/git/CoolSolve/examples/heat_pump_MSTh_SB_R10.eescode`
  (inventory candidate `CSX-020`), with its `.initials`;
- same exercise, other versions (see *Related models*):
  `~/Nextcloud/thermo_models/…/TP 10/R10 - SB - EX 1 - questions.EES`
  (`TM-0159`) and `R10 - SB - Ex 1.EES` (`TM-0160`), and
  `MSTh R10 Ex 1.EES` (`TM-0152`).

The example is an equation-for-equation transcription of the EES original (a
diff of the equations stripped of comments and blanks shows no difference: the
same 55 equations, the same values, the same commented alternatives), so the
library model follows the EES original. It differs from the example by: the
standard header, English section titles, the unit of every quantity given in a
trailing comment, the `h_su`/`epsilon_s` block and the 16 diagram state-point
equations added at the end (post-processing only — the results are those of
the raw extraction), and the `//cp_w_ev=4187` / `//cp_w_cd=4187` provisional
values of the example dropped (they are comments; the water specific heat is
computed with `CP(Water, …)` in both files).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on
  `MSTH-SB-R10-EX1.EES`): unit system already SI-°C-Pa-J, no conversion
  needed; the `$UnitSystem` directive and the EES licence tag removed; no
  lookup or parametric table; only built-in functions (`pressure`, `enthalpy`,
  `entropy`, `volume`, `cp`, `temperature`, `exp`); the stored solution
  (55 variables) is complete. Faithful run of the raw extraction (55
  equations, 17 blocks, largest block 39): *SUCCESS*, largest deviation from
  the EES stored solution 6.6e-03 (see *Verification*), the same as after
  curation.
- **2026-10-05 — curation**: standard header added; comments translated from
  French to English (paraphrasing the original's own comments); section
  titles added; dimensional quantities given their SI unit in trailing
  comments; the intermediate water capacity rates `C_dot_w_ev` / `C_dot_w_cd`
  of the original inlined as `M_dot_w*cp_w` (no numerical change, the same
  relation as `C_dot_min_ev` / `C_dot_min_cd`); the `"valeur provisoire"` display strings of the original
  (`Q_dot_cd = 70000`, `Q_dot_ev = 50000`) kept as comments. Variable names
  unchanged (`W_dot_cp`, `h_su_cp`, `epsilon_v_1`, `Q_dot_u`, …). The
  commented alternatives of the original (constant-cp reheat, compressor
  without the semi-hermetic design) are kept, each with a note that they come
  from the original.
- **2026-10-05 — diagram state points**: block of 16 post-processing
  equations added at the end (`P[i]`, `h[i]`, `T[i]`, `s[i]` for the four
  state points, pattern of `CSL-0001`), for the CoolSolve diagram overlay; no
  effect on the results. The original only had `h[1…4]` and `P[1…4]`
  ("représentation graphique").
- **2026-10-05 — result added**: the global isentropic efficiency
  `epsilon_s` (with `h_su = h_1`, `h_ex_s`, `s_su`) taken from the questions
  file of the same exercise (TM-0160); no effect on the other results.
- **2026-10-05 — guesses**: `.initials` shipped with the guesses stored in the
  EES file (the entries of the commented alternatives — `epsilon_v`, `r_v`,
  `v_su`, `v_ex`, `V_dot_su`, `cp_r` — were dropped, they are not variables of
  the model). Without them the 39-equation block does not converge.
- **Level**: score of `docs/taxonomy.md` §3 = 1 (75 equations) + 2 (largest
  block 39) + 1 (arrays) + 1 (evaporator, condenser and compressor coupled)
  + 0 (no calibration, off-design or dynamics) + 1 (needs curated guesses)
  = 6 → level 3; moved down by one to **level 2**: the model is a
  single-operating-point exercise whose implicit block comes from the cycle
  closure, not from a design or off-design study (the card also asks for
  level 2).

## Limitations and CoolSolve gaps

- The two exchangers are semi-isothermal (an infinite capacity rate on the
  refrigerant side) and rated with a constant overall conductance AU: no
  superheat/condensation/subcooling zones, no pressure drop, no dependence of
  the conductance on the flow rates.
- The refrigerating capacity is not imposed; the flow rate is fixed by the
  compressor characteristics (`epsilon_v_1 = V_dot_su_1/V_dot_s`) and the
  machine energy balance, as in the original — this is the closure the author
  kept (see *Problem statement*).
- `h_1` is the saturated-vapour enthalpy at `T_ev + DELTAT_oh` (`x = 1`) while
  the compressor inlet `h_su_cp` is the superheated enthalpy at the same
  temperature and at `P_ev`; the two differ by about 2 kJ/kg in EES. Kept as in
  the original (the questions file of the exercise discusses it).
- The `.sol` file labels the specific volumes `kg/m^3` instead of
  `m^3/kg`: registered bug `CS-BUG-UNIT-VOLUME`, no impact on the results.
- CoolSolve prints the hint *"PRESSURE(): fluid 'R22'. Did you mean 'R22'?"*
  although the fluid name is already correct: same hint-table behaviour as the
  registered bug `CS-BUG-FLUID-HINT-CO2`, no impact.
- No CoolSolve gap blocks this model (`missing_features` is empty): it uses
  only built-in property functions and arrays.

## Related models

- `CSL-0001` *refrigeration_cycle_simple_compressor*: same compressor laws
  (clearance-volume volumetric efficiency, constant + proportional losses) on a
  refrigeration cycle, with the machine adiabatic (no reheat) and a
  three-fluid comparison.
- `CSL-0022` *refrigeration_compressor_identification*: the same compressor
  model whose four parameters are identified from two measured regimes instead
  of being given.
- `CSL-0025` *heat_pump_cycle_r22_30kw*: the same machine (R22, water source and
  sink) with an imposed isentropic compressor efficiency and a prescribed
  heating capacity.
- Same exercise, other files (not imported, see the inventory notes):
  `thermo_models` TM-0159 / TM-0160 (questions file: constant water specific
  heat, the discussion of the two condenser closures, the global isentropic
  efficiency) and TM-0152 (statement version with a different compressor
  closure); the other exercises of the same repetition are TM-0153, TM-0155,
  TM-0156 (R10 Ex3) and TM-0157 (R10 Ex4, R22/R407C comparison).
- CoolSolve example `heat_pump_MSTh_SB_R10.eescode` (same model, kept in the
  CoolSolve repository as a test case).
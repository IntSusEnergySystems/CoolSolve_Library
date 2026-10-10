# Biomass-boiler ORC (R123) with scroll expanders and a split condenser

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0040`

Organic Rankine cycle on R123, heated by a **biomass boiler** and coupled,
through the feed-water loop, to a condenser split into a **water-cooled** and an
**air-cooled** part. The five cycle components are described by dedicated
sub-models, originally written as EES `MODULE`/`SUBPROGRAM` blocks and called
from the main program: the scroll **expander** (5 machines in parallel), the
**evaporator** (liquid / two-phase / vapour zones, water source) and the biomass
**burner** (adiabatic combustion chamber, water flue-gas heat exchanger,
water-to-ambient heat exchanger). The library version flattens those three
blocks into the main program (library decision D10; CoolSolve does not implement
`MODULE`/`SUBPROGRAM`, `CS-GAP-MODULE`) and keeps the EES `PROCEDURE`s
`pump`, `cond` and the `FUNCTION`s `write`, `cp_g`.

The model does **not** run in CoolSolve: a registered gap blocks the native
file (see *Blocked features*). The file stays valid EES; the flattening of the
sub-models has known deviations (see *Known deviations of the flattening*).

| | |
|---|---|
| **Category** | Cycles › Organic Rankine cycles |
| **Fluids** | R123 (cycle), Water (feed water, evaporator source), Air / humid air (condenser part 2, boiler air), CO2 / H2O / O2 / N2 (combustion products, ideal gases) |
| **Size** | 363 equations, 392 unknowns once the nine switches are resolved for the stored run (372 and 401 with the nine string constants), see *Blocked features* |
| **Source** | S. Quoilin (ULiège Thermodynamics Laboratory), EES file `orc_complex.EES` (EES 9.920), transcribed as CoolSolve example `examples/orc_complex.eescode` |
| **Authors** | S. Quoilin (ULiège Thermodynamics Laboratory) — probable, to be confirmed by the maintainer |
| **License** | MIT |
| **CoolSolve** | **blocked**: the file parses (the `C%`, `H%`, `O%` names are accepted; the `$if` directives are evaluated) and stops on the nine Diagram-window strings that have no value (`CS-GAP-IF-NO-CONSTANT`) |

## Model

### 0. Biomass burner (`SUBPROGRAM biomass_burner`)

Adiabatic combustion chamber: the air and the fuel are brought to `T_ref = 25 °C`,
the lower heating value `LHV_f` is released (`Q_dot_3 = −M_dot_f·LHV_f`) and the
sensible heat of the products gives the adiabatic flame temperature `T_adiab`
(`cp_g`, the ideal-gas mixture model below). A water–flue-gas heat exchanger
(`epsilon_gw`-NTU, part-load law `AU_gw_n·(M_dot_g/M_dot_g_n)^0.65`) boils the
feed water, and a water-to-ambient heat exchanger rejects the remaining heat.
`Q_dot_u_boil` (useful heat) and `eta_boil = −Q_dot_u_boil/Q_dot_3` are the
results. The fuel is described by its mass fractions `C%`, `H%`, `O%` (percent
signs) and the excess-air coefficient `e`.

### 0b/1. Water overheater and economiser

Both are optional blocks of the original (`water_overheater$`, `economiser$`);
in the stored run they are **off** (`$else` branch), so `Q_dot_wo = 0` and
`Q_dot_econ = 0`.

### 1. Evaporator (`MODULE evaporator`)

Three zones on the water source `fluidev$` at `p_sf_su_ev`, seen from the
refrigerant side as superheated liquid → saturated liquid → two-phase → vapour
(`DELTAT_oh_ex_ev` superheat at the exit). Each zone has its own
effectiveness–NTU closure (counter-flow relation `epsilon·(1−ω·e^(−NTU(1−ω))) =
1−e^(−NTU(1−ω))` for the single-phase zones, `epsilon = 1−e^(−NTU)` for the
two-phase zone) and its `AU` value; the pinch point `pinch_ev` is the minimum
approach temperature over the three zones. The zone states are written to the
arrays `T_r[1..4]`, `h_r[1..4]`, `P[1..4]`, `H_dot_r[1..4]`.

### 1bis. Overheater

Optional block, **off** in the stored run (`overheater$='no'`).

### 2. Expander (`MODULE expander`), 5 machines in parallel

Scroll (positive-displacement) expander, semi-empirical: supply throttling
through `d_su` and wall heat transfer down to `su1`, wall heat transfer `su1 →
su2`, swept volume from `V_s_exp` (built-in volume ratio `r_v_in`), isentropic
expansion to the adapted pressure `P_r_in_exp` then isochoric expansion to the
exhaust pressure, leakage flow through `A_leak` at the choking pressure
`P_r_thr`, mixing of the leakage with the main flow at the exhaust, wall heat
transfer at the exhaust, mechanical losses and ambient heat balance, global
isentropic effectiveness `epsilon_s_exp`. Five machines in parallel:
`M_dot_r_exp_tot = n_exp·M_dot_r_exp`, `W_dot_sh_exp_tot = n_exp·W_dot_sh_exp`.

### 3. Condenser (`PROCEDURE cond`), two heat exchangers in series

The three refrigeration-side zones (vapour → two-phase → liquid) are computed
from the imposed sub-cooling `DELTAT_sc_ex_cd` at `p_cd`; heat exchanger 1
condenses part of the vapour (`Q_dot_cd1`) into the feed-water loop (water at
`T_sf_ex_cd` → `T_sf_su_cd`), heat exchanger 2 rejects the rest into the air
(`T_a_ex_cd2` − `T_a_su_cd2`). `pinch_cd` is the approach temperature of
heat exchanger 1. Zone states go to `T_r[5..8]`, `h_r[5..8]`, `P[5..8]`.

### 4. Pump (`PROCEDURE pump`)

Isentropic efficiency `epsilon_s_pp`, swept-volume flow and shaft power
`W_dot_pp`.

### 5. Regenerator

Optional block, **off** in the stored run (`regenerator$='no'`), `Q_dot_reg = 0`.

### 7. Cycle performances

First-law efficiency `eta_I = W_dot_el_net/(Q_dot_ev+Q_dot_econ+Q_dot_oh)`,
global efficiency `eta_global = (W_dot_el_net + Q_dot_cd + Q_dot_wo)/Q_dot_tot_boil`,
Carnot efficiency of the evaporator source, pressure ratio `r_p` and the
calculation residual `res_ref`. `write()` stores `eta_I`, `W_dot_el_net` and
`eta_global` in row `i` of the lookup table `results`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): a T-ṁ diagram of the
     whole plant (boiler + cycle) or a P-h diagram of the cycle, once a runnable
     variant exists; figures/orc_biomass_chp_th.png -->

## Results (EES reference solution, `EES_ok/orc_complex.tex`)

The reference below is the **EES solution report** shipped with the original file
(`misc/EES_ok.zip`, `EES_ok/orc_complex.tex`, EES 9.920). It is listed here as
the target a runnable variant must reproduce; the library model itself does not
solve, so no CoolSolve column is given.

| Quantity | EES solution report |
|---|---:|
| `eta_I` first-law efficiency [-] | 0.108 |
| `eta_global` (power + condenser heat over the boiler heat) [-] | 0.88 |
| `W_dot_el_net` net electric power [W] | 72 320 |
| `W_dot_sh_exp_tot` shaft power of the 5 expanders [W] | 76 880 |
| `W_dot_pp` pump power [W] | 4 560 |
| `epsilon_s_exp` expander isentropic effectiveness [-] | 0.828 |
| `Q_dot_ev` evaporator duty [W] | 672 320 |
| `Q_dot_cd` condenser duty [W] | 600 000 |
| `Q_dot_u_boil` useful boiler heat [W] | 672 301 |
| `Q_dot_tot_boil` total boiler heat [W] | 763 970 |
| `M_dot_r_exp_tot` refrigerant flow [kg/s] | 3.259 |
| `M_dot_f` fuel flow [kg/s] | 0.04494 |
| `n_exp` expanders in parallel [-] | 17.5 |
| `t_r_ex_exp` expander exhaust temperature [°C] | 92.27 |
| `t_r_ex_cd` / `t_r_ex_pp` condenser exit / pump exit [°C] | 57.4 / 58.44 |
| `p_ev` / `p_cd` evaporator / condenser pressure [Pa] | 1.461·10⁶ / 3.065·10⁵ |
| `Q_dot_econ`, `Q_dot_oh`, `Q_dot_wo`, `Q_dot_reg` (blocks off) [W] | 0 |

The string switches of the stored run, read from the solution report:
`fluid$='R123'`, `fluidev$='water'`, `expanderType$='Open'`,
`pressuredrop$='no'`, `heatTransfer$='no'`, `unadaptedVolumeRatio$='no'`,
`mechanicalLosses$='no'`, `water_overheater$='no'`, `economiser$='no'`,
`overheater$='no'`, `regenerator$='no'`.

## Verification

**Not verified — the model is blocked.** See *Blocked features*. The EES
reference solution listed above is the one a runnable variant would be compared
with.

Two properties of the reference material must be known before importing:

- The **solution report** `EES_ok/orc_complex.tex` lists the main-program
  variables only (module-internal variables have no entry).
- The **variable records** decoded from the binary `.EES` by `ees_extract.py`
  into `reference/ees_variables.csv` are **stale** for the flattened sub-models
  (registered tool bug `CS-BUG-EXTRACT-STALE`): e.g. they give
  `P_r_su1_exp = 1.016·10⁶` while `P_r_su_exp = 1.461·10⁶` and
  `r_p_su_exp = 0.99997`, three mutually inconsistent values. The values of the
  main-program variables agree with the solution report (`h_r_su_exp = 468 246.7`
  vs `468 247`, `M_dot_r_exp = 0.18665` vs `0.1866`). They are therefore not
  used as the reference, and **no `.initials` file is shipped**: a converged
  baseline could not be produced (blocked model) and stale guesses would be
  worse than none.

## Blocked features

`model.json` `missing_features` lists the registered gap that blocks the native
file:

| Gap | What it blocks here | Evidence |
|---|---|---|
| `CS-GAP-IF-NO-CONSTANT` | The main program selects blocks with `$if <string>$='…' / $else / $endif` (nine switches, listed under *Runnable variant*). CoolSolve evaluates the directives; the seven `*_exp$` tests of the flattened expander resolve (their strings are set in the file), but the nine strings of the main program (`water_overheater$`, `economiser$`, `overheater$`, `expanderType$` (twice), `pressuredrop$`, `heatTransfer$`, `unadaptedVolumeRatio$`, `mechanicalLosses$`, `regenerator$`) are values given in the **EES Diagram window**, absent from the `.eescode`: *\"$IF: the string variable 'economiser$' has no value when the directive is compiled: it must be set to a string constant … before the $IF (a value given in the EES Diagram window is not available in CoolSolve)\"* (10 errors, lines 592, 635, 708, 777, 803, 809, 817, 823, 833, 971). CoolSolve never chooses a branch silently. | Registered gap `CS-GAP-IF-NO-CONSTANT` (found with this model and `CSL-0166`). With the nine switches resolved for the stored run in a scratch copy, 363 equations and 392 variables remain. |

Not blocking, but noted:

- `CS-GAP-LKT` — the function `write()` stores three results per run in row `i`
  of the lookup table `results` (`lookup('results',i,1) = …` inside a
  `FUNCTION`). The table is not in the file; CoolSolve parses and solves this
  form without it, so the gap does not block the file. The write is an output
  sink with no feedback on the solution.
- `CS-GAP-MODULE` — `MODULE`/`SUBPROGRAM` are **not** in `missing_features`: the
  three blocks are flattened (decision D10), so the native file does not use
  them.
- `CS-GAP-PROC-COMMENT` — the comment strings `"<=inputs outputs=>"` inside the
  argument lists of `procedure pump` and of its `call`s were **removed**
  (comments only); this is not a blocking gap.
- `CS-GAP-BOUNDS` — EES used lower/upper bounds on several variables; CoolSolve
  `.initials` carries guesses only. A runnable variant would have to rely on
  better guesses.
- `CS-BUG-FLUID-HINT-CO2` — `molarmass(CO2)` raises the harmless warning
  *\"Did you mean 'CO2'?'\"*; `CS-BUG-UNIT-VOLUME`-type hints on the arrays are
  likewise cosmetic.
- `cp_g` calls `enthalpy(CO2, T=…)`, `enthalpy(H2O, T=…)`, `enthalpy(O2, T=…)`
  and `enthalpy(N2, T=…)` without a pressure: in EES these are **ideal-gas**
  substances (the file is in SI-C-Pa-J, so this is the native EES convention and
  was kept). CoolProp resolves them to CoolProp's CO2/water references; since
  `cp_g` only uses enthalpy **differences** over 25 → `T_p1`, the reference
  offset cancels, but a runnable variant must be checked against the reference
  `Q_dot_u_boil` / `T_adiab`.
- `cp_a=cp(air,…)` (condenser, part 2) and `cp_a=CP(air_ha,…)` (boiler) use two
  different EES air names; CoolSolve warns that `'air'` means moist air and
  suggests `AirH2O`. A runnable variant should use `Air`.

## Known deviations of the flattening

Decision D10 replaces every formal argument of a block by its actual argument.
For six formals that the block also assigns itself (a result, or an input
redefined inside) the import **renamed** the formal as an internal variable
instead, and did not write the link `formal = actual` that EES generates (the
`.residuals` file of the original lists these links, e.g.
`evaporator\1.pinch_ev=pinch_ev`). The equations of the blocks are those of the
original (the normalised comparison with the extraction shows only the
renamings of the conversion log); the links are missing:

| Block | Formal → flattened name | Missing link |
|---|---|---|
| `expander` | `A_leak_mm2` → `A_leak_exp_mm2` | `A_leak_exp_mm2 = A_leak_mm2` (the leakage area `A_leak_exp` is otherwise not tied to the input `A_leak_mm2_1`) |
| `evaporator` | `pinch_ev` → `Pinch_ev_ev` | `Pinch_ev_ev = pinch_ev` (the EES diagram input `pinch_ev = 10` has to be written on `Pinch_ev_ev`) |
| `biomass_burner` | `Q_dot_3` (actual `-Q_dot_tot_boil`) → `Q_dot_3_boil` | `Q_dot_3_boil = -Q_dot_tot_boil` (`Q_dot_tot_boil`, used by `eta_global`, is otherwise defined by no equation) |
| `biomass_burner` | `T_w_ex_boil` → `T_w_ex_boil_boil` | `T_w_ex_boil_boil = T_w_ex_boil` (the burner water outlet is not tied to `T_w_ex_boil = T_sf_su_ev` of the main program) |
| `biomass_burner` | `m`, `n`, `p` → `m_boil`, `n_boil`, `p_boil` | `m_boil = m`, `n_boil = n`, `p_boil = p` (the main-program `m`, `n`, `p` are used only by the optional blocks, off in the stored run) |
| `biomass_burner` | `Q_dot_gw` → `Q_dot_gw_boil` | `Q_dot_gw_boil = Q_dot_gw` (the main-program `Q_dot_gw` is used nowhere else) |

Evidence: in a scratch copy with the switches of the stored run resolved and the
diagram inputs of EES added (next section) the file has 391 variables and 388
equations; adding the first, third and fourth links makes it **square (391 ×
391)** (the second link is absorbed by writing the pinch input on
`Pinch_ev_ev`). The library file is **not repaired**: the repair is to replace
the six renamed formals by their actual arguments in a runnable variant.

## Runnable variant: not shipped, feasible

A runnable `_coolsolve` variant was not built within the card. The review
checked, in a scratch copy (nothing shipped), that it is structurally feasible:

1. resolve the nine `$if` switches for the stored run — set each string as a constant in
   the main program **before** its first `$if` (`CS-GAP-IF-NO-CONSTANT`: CoolSolve
   evaluates the directives but needs a constant value; the EES Diagram value is not in
   the file): `pressuredrop$='no'`,
   `unadaptedVolumeRatio$='no'`, `heatTransfer$='no'`, `mechanicalLosses$='no'`,
   `economiser$='no'`, `overheater$='no'`, `regenerator$='no'`,
   `water_overheater$='no'`, `expanderType$='Open'` (the strings of the flattened
   expander, renamed `*_exp$`, keep their module-local values `'yes'` /
   `'hermetic'`: they are local to the module in EES);
2. no renaming is needed: the `C%`, `H%`, `O%` names parse;
3. add the **diagram inputs** of EES. The model has no equation for them because
   EES holds them in its Diagram window (the `"! in diagram"` comments);
   `EES_ok/orc_complex.residuals` flags them `D`: 52 equations in all (11 strings,
   41 numbers). For the stored run the resolved file uses `fluid$='R123'`,
   `fluidev$='water'` and 24 numbers: `T_sf_su_ev=150`, `T_amb_exp=20`,
   `DELTAT_sc_ex_cd=5`, `DELTAT_oh_ex_ev=10`, `epsilon_s_pp=0.6`,
   `DELTAT_sf_ev=10`, `pinch_ev=10` (on `Pinch_ev_ev`), `pinch_cd=5`,
   `r_v_in_1=4.1`, `AU_amb_exp_1=6.4`, `AU_su_exp_n_1=21.2`,
   `AU_ex_exp_n_1=34.2`, `d_su_1=0.00591`, `M_dot_r_exp_n_1=0.12`,
   `A_leak_mm2_1=4.858`, `N_rot_exp_1=3000`, `V_s_cp_cm3_1=148`, `eta_gen=0.8`,
   `T_w_ex_wo=60` (`t_w_ex_wo` of EES), `T_sf_su_cd1=40`, `Q_dot_cd2=0`,
   `Q_dot_cd=600000`, `T_a_su_cd2=20`, `T_a_ex_cd2=35`. The other diagram values
   (the `_2` hermetic set, `T_m`, `epsilon_reg`, `epsilon_wo`, `epsilon_oh`,
   `epsilon_econ`) belong to branches that are off. `n_exp = 17.5`,
   `Q_dot_tot_boil`, `M_dot_f_kgh`, `Q_dot_cd1`, `T_sf_ex_cd1`, `gamma_r` and the
   leakage area `A_leak` are **results** of the stored run, not inputs (the list
   of free constants given by the import was wrong on these);
4. add the missing links (or repair the flattening: *Known deviations*);
5. drop `written = write(...)` and the function `write` (output sink; `i = 4`
   only feeds it);
6. map `air` / `air_ha` to `Air`.

Result of the scratch test: **391 equations, 391 variables, square, largest block
116**. It does **not converge** from the decoded stored values (stale for the
module variables, `CS-BUG-EXTRACT-STALE`): Newton stops by line-search failure and
TrustRegion at 500 iterations in the 116-variable block (initial residual
7·10⁶). Curated initial values built from the main-program values of the
solution report (and a simplified-model bootstrap, `docs/debugging_models.md`)
are the remaining work.

## How to run

```bash
coolsolve ./orc_biomass_chp.eescode      # -> Parse failed (CS-GAP-IF-NO-CONSTANT)
```

## Source and attribution

Cycle and boiler model written by **S. Quoilin** (ULiège Thermodynamics
Laboratory). The EES licence stamp of the file is
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege sylvain}`,
i.e. the lab licence with the author initials `sylvain`; the author is recorded
as *probable* and is left for the maintainer to confirm. Source files
(MIT, collection of S. Quoilin):

- CoolSolve example (equation-identical transcription of the original, plus a
  banner saying CoolSolve cannot parse it): `~/git/CoolSolve/examples/orc_complex.eescode`
  (inventory `CSX-029`), with `~/git/CoolSolve/examples/orc_complex.initials`,
- original EES file with the stored solution, the residuals window and the
  solution report: `~/git/CoolSolve/misc/EES_ok.zip`, `EES_ok/orc_complex.EES`
  (EES 9.920), `EES_ok/orc_complex.residuals`, `EES_ok/orc_complex.tex`, and the
  two plot windows `orc_complex_P1.jpg` (boiler) / `_P2.jpg` (condenser).

**Differences between the CoolSolve example and the EES original.** The two
files carry the *same equations*: `diff` of the extraction against
`examples/orc_complex.eescode` (both de-`\r`-ed) leaves only (i) a five-line
banner added by CoolSolve at the top of the example
(*"PARSE ERROR: This file contains invalid procedure syntax …"*) and (ii) the
comment line `"PUMP   MODEL"`, which the example omits. The library model
therefore follows the EES original; the example stays in CoolSolve as a parser
test case.

**The same exercise in the ULiège collection.** `sources/thermo_models/inventory.csv`
was searched (title, description, variables and values): it contains **no row**
for this model — no biomass-boiler ORC and no `R123` biomass cogeneration file.
The nearest candidates are different systems and were left `todo` for their own
cards: `TM-0268` *cycle ORC with refprop.EES* (REFPROP mixtures, needs an
external `EES_REFPROP` library and three undefined procedures), `TM-0314`
*ORC simple model with void fraction.EES* (R134a, charge by void fraction) and
`TM-0323` *simple ORC with fluidprop* (benzene–toluene through FluidProp). The
expander module of this cycle is the same code as `CSL-0037`
`TM-0272`/`TM-0273` (already `merged`/`duplicate`), with the leakage flow and
the electrical output added.

## Conversion log

- **2026-10-05 — import (roadmap card C-42, batch B-04).** `ees_extract.py` on
  `EES_ok/orc_complex.EES` (EES 9.920, 1020 equation-window lines, 433 variable
  records, unit system already `SI MASS DEG PA C J`, licence and display tags
  removed, no embedded lookup or parametric table). Comments translated to
  English, standard header added, `$UnitSystem` directive removed. **No equation
  was changed** apart from the variable renamings of the flattening (below; their
  consequence, six missing formal-actual links, is described in *Known
  deviations of the flattening*).
- **MODULE / SUBPROGRAM flattening (decision D10).** Three blocks, one `CALL`
  each; all their internal variables already carried a per-component suffix,
  which serves as the per-call tag, and were kept unchanged unless they collided
  with a main-program variable. The mapping (file header and this log):

  | block (tag) | formal → actual argument of the `CALL` | internal variables renamed | notes |
  |---|---|---|---|
  | `MODULE expander` (`_exp`) | `r_v_in`→`r_v_in_input`, `AU_su_exp_n`→`AU_su_exp_n_input`, `AU_ex_exp_n`→`AU_ex_exp_n_input`, `d_su`→`d_su_input`, `alpha`→`alpha_input`, `W_dot_loss_0`→`W_dot_loss_0_input`, `T_m`→`T_m_input`, `eta_gen`→`eta_gen_input`; all other formals have the name of the actual argument | `pressuredrop$`→`pressuredrop_exp$`, `heatTransfer$`→`heatTransfer_exp$`, `unadaptedVolumeRatio$`→`unadaptedVolumeRatio_exp$`, `mechanicalLosses$`→`mechanicalLosses_exp$`, `expandertype$`/`expanderType$`→`expandertype_exp$`/`expanderType_exp$` (they collide with the main-program switches of the same name), `A_leak_mm2`→`A_leak_exp_mm2` and `A_leak`→`A_leak_exp` (the module overwrites its formal `A_leak_mm2` with its own `A_leak·1000²`) | the main-program `A_leak_mm2`, `AU_*_exp_n`, `d_su`, `alpha`, `W_dot_loss_0`, `N_rot_exp`, `V_s_cp_cm3`, `r_v_in` assignments (section 2.1) keep their names; `T_m`, `eta_gen`, `A_leak`, `V_s_exp` are shared |
  | `MODULE evaporator` (`_ev`) | none (every formal has the name of its actual argument) | `Pinch_ev`→`Pinch_ev_ev`, `DELTAT_sf_ev`→`DELTAT_sf_ev_ev` (both collide with a main-program variable: the module overwrites the formal `pinch_ev`, and the main program re-computes `DELTAT_sf_ev` with the identical equation) | arrays `T_r[1..4]`, `h_r[1..4]`, `P[1..4]`, `H_dot_r[1..4]`, `T_sf_ev[1..4]`, `H_dot_sf_ev[1..4]` do not collide with the main-program arrays (`T_r[5..8]`, `T_r[10]`, `h_r[5..8]`, `h_r[10..11]`, `P[5..8]`, `P[10..11]`, `P_r[10..11]`) |
  | `SUBPROGRAM biomass_burner` (`_boil`) | `Q_dot_gw`→`Q_dot_gw_boil` and `Q_dot_3`→`Q_dot_3_boil` (actual argument `-Q_dot_tot_boil`); all other formals have the name of their actual argument | `m`→`m_boil`, `n`→`n_boil`, `p`→`p_boil`, `T_w_ex_boil`→`T_w_ex_boil_boil` (these four are formals that the sub-program overwrites, so they act as internal variables) | the internal `cp_a` (boiler) does not collide with the local `cp_a` of `procedure cond`; `MM_O2`, `MM_N2`, `MM_CO2`, `MM_H2O`, `MM_prod` are local to `cp_g` |

  The `module` / `subprogram` / `call` / `end` lines were removed and the
  `$bookmark` GUI tags kept (they are EES display tags, harmless).
- **`CS-GAP-PROC-COMMENT`**: the comment string `"<=inputs outputs=>"` was removed
  from the argument list of `procedure pump` (which would otherwise be a parse
  error) and from the matching `call pump(...)` of the main program, for
  consistency (comments only, an allowed edit; the `procedure cond` signature has
  none).
- **C-46 review — `procedure cond` header restored.** The import had dropped
  `:pinch_cd` from the header (18 arguments and no colon, against 19 and a colon
  in the `call`): CoolSolve answered *\"Procedure cond expected 18 inputs, got
  10\"* in the scratch test. Restored as in the original (the equations of the
  procedure were not touched).
- **Unit system**: the original is already `SI MASS DEG PA C J`; no conversion
  was needed. Note that `C%`, `H%`, `O%` are **mass fractions in percent**
  (they are divided by the atomic masses in `m_boil=C%/MM_C`), not percentages
  of the mixture.
- **Dead code**: nothing was removed; the commented-out alternatives of the
  original (`{M_dot_r_exp=A_thr_su*sqrt(...)}`, `{gamma_r=1.1}`, `{p_ev=9E5}`,
  `{c_p_r_econ=1000}`, …) are kept, as they document the alternative closures
  the author was choosing between.
- **Level justification** (taxonomy §3): equations 443 (300–1500 → 2), largest
  algebraic block > 30 → 2 (the flattened `expander` sub-model alone has 63
  equations and is closed through `M_dot_r_exp_tot`, `t_r_ex_exp` and
  `P_r_su_exp` by the evaporator, the split condenser and the pump; the whole
  cycle and the burner then form one loop), functions/procedures present → 1,
  ≥ 3 coupled components (burner, evaporator, 5 expanders, 2 condensers, pump) →
  1, semi-empirical calibration (expander leakage/choking, burner stoichiometry,
  part-load `AU` laws) → 1, needs curated guesses → 1: **total 8 → level 4**. The
  block size of the native file could not be measured (`coolsolve -d` stops at the
  not-square system); in the review's scratch copy with the stored-run switches
  and inputs it is 116.
- **Trajectory / sweep claims**: the model has no sweep or trajectory; the only
  numerical claim in this README is the EES solution report table, copied from
  `EES_ok/orc_complex.tex`.

## Related models

- `CSL-0037` *scroll_expander_semi_empirical*: the same scroll-expander module
  (`expander`), imported standalone and flattened by the same decision D10.
- `CSL-0036` *orc_extraction_r134a*: ORC with two-stage scroll expanders.
- `CSL-0019` *orc_simple_r245fa*: screening ORC model.
- `CSL-0038` *orc_co2_polynomial_maps*: transcritical CO2 ORC with polynomial
  compressor/turbine maps.
- See also the CoolSolve example `examples/orc_complex.eescode` (kept in
  CoolSolve as a parser test case).
# Brine-to-water heat pump reference model (RefSim)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** (adapted from the original) &nbsp;|&nbsp; `CSL-0078`

Reference simulation model of a brine-to-water (ground-source) heat pump of the
ULiège model bank: a rotary (scroll) compressor described step by step between
the evaporator exhaust and the condenser supply, a brine evaporator (propylene
glycol solution, properties from the BrineProp library) and a water condenser.
Both heat exchangers are described by three thermal resistances in series
referred to their nominal flow rates, and all the heat transfers of the machine
are referred to a fictitious envelope of uniform temperature whose balance
closes the model.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R407C (refrigerant, default), Water (constant `cp_w` = 4187 J/kg·K), PG 25 % brine (BrineProp library) |
| **Size** | 161 equations in the main program (the model with its 12 inputs and 19 parameters restored from the stored run, the `(s, v)` rewrite and the 16 state points of the diagrams); `BRINEPROP` comes from `CSL-0079`; 86 blocks, largest block 76 |
| **Source** | ULiège model bank (Laborelec toolkit lineage), heat production by vapour compression, reference simulation model, 8 January 2008 (`BrinetoWaterHeatPump_RefSim_EES_Model_VL080108.EES`, EES 7.888) |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — **verified** after two documented adaptations (see *Conversion log*, 2026-11-01): `P_ev`, `P_cd`, `M_dot_r` are unknowns again (as in the original) and the internal compressor power counts the leakage flow (energy balance closed); needs the shipped `.initials` |

## Problem statement

A ground-source heat pump heats 0.389 kg/s of water entering the condenser at
25.5 °C (400 kPa) with a brine flow rate of 1.11 kg/s entering the evaporator at
0 °C, in a 25 % propylene glycol solution. The refrigerant is R407C, evaporating
at about 438 kPa and condensing at about 1.77 MPa (results of the model), with 5 K of superheating at the
evaporator exhaust and 5 K of subcooling at the condenser exhaust. The scroll
compressor runs at 3000 tr/min with a reference swept volume of 9.478·10⁻⁵ m³
and runs at full load (`X_cp` = 1). Determine the heating power, the
compressor electrical power, the heating COP, the compressor exhaust
temperature, the water temperature at the condenser exhaust and the brine
temperature at the evaporator exhaust, and the volumetric and isentropic
effectivenesses of the machine.

## Model

**Compressor** (supply state *su* = evaporator exhaust, discharge state *ex* =
condenser supply). The refrigerant path is decomposed into five steps, as in the
original:

- (i) *supply heating-up* (su → su1): a heat exchanger of effectiveness
  `epsilon_su_cp = 1 − exp(−NTU)` between the refrigerant capacity flow rate
  `C_dot_su_cp = M_dot_r·c_p_su_cp` and the fictitious envelope `t_w_cp`, with
  the conductance `AU_su_cp = AU_su_cp_n·(M_dot_r/M_dot_r_cp_n)^0.8`;
- (ii) *isentropic compression* (su1 → in): the state at the adapted pressure,
  `v_in_cp = v_su2_cp/r_v_in_cp` and `p_in_cp` the pressure reached by the gas
  after this first compression (`in` = adapted pressure);
- (iii) *isochoric compression* (in → ex1): the compression chamber opens to the
  discharge plenum at constant volume, `w_in2_cp = v_in_cp·(p_ex1_cp − p_in_cp)`,
  **positive** here (the adapted pressure 1.51 MPa is below the discharge
  pressure 1.73 MPa);
- (iv) *exhaust cooling-down* (ex1 → ex): the same heat-exchanger form as (i)
  with `AU_ex_cp = AU_ex_cp_n·(M_dot_r/M_dot_r_cp_n)^0.8`;
- (v) *internal leakage* (ex1 → su1): the gas leaking back through the scroll
  throat, an isentropic flow from the exhaust state to the throat pressure
  `P_thr_cp = max(P_thr_crit, P_su1_cp)` with
  `P_thr_crit = P_ex1_cp·(2/(gamma_leak_cp+1))^(gamma_leak_cp/(gamma_leak_cp−1))`,
  a leakage volume flow rate `V_dot_leak_cp = A_leak_cp·C_thr_cp` and a mixing
  with the fresh suction gas, `M_dot_s_cp·h_su2_cp = M_dot_r·h_su1_cp +
  M_dot_leak_cp·h_ex1_cp`.

The mass flow rate of the machine follows the swept volume,
`V_dot_s_cp = V_s_cp_ref·(N_rot/60)·X_cp`, the electrical power is the
compression power plus `W_dot_loss0_cp + alpha_cp·W_dot_in_cp`, and the
fictitious envelope balance closes the machine:
`t_w_cp = t_amb + (W_dot_loss_cp − Q_dot_su_cp − Q_dot_ex_cp)/AU_amb_cp`. The
global isentropic effectiveness is `epsilon_s_cp = (h_exs − h_su)/w_cp` and the
volumetric one `epsilon_v_cp = v_su_cp/v_su1_cp`.

**Heat exchangers**: three thermal resistances in series, each referred to its
nominal flow rate (`R_x = R_x_n·(M_dot_x_n/M_dot_x)^0.8`), an effectiveness
`epsilon = 1 − exp(−NTU)` and the mean evaporating / condensing temperature
`T = (T_sat(T,P,x=1) + T_sat(T,P,x=0))/2` of the refrigerant. The brine side of
the evaporator computes `Q_dot_ev = epsilon_ev·C_dot_glw_ev·(t_glw_su_ev −
t_ev)` and the refrigerant side `Q_dot_ev = M_dot_r_ev·(h_ex_ev − h_su_ev)` with
the isenthalpic expansion `h_su_ev = h_ex_cd`; the condenser likewise computes
the condensing power from the refrigerant side and from the water temperature
rise. The model **writes each of these heat rates and two compressor
relations twice** (four pairs): they are not duplicates but the closures of
the unknowns `P_ev`, `P_cd`, `M_dot_r` and `gamma_leak_cp` (effectiveness
form against refrigerant balance for the two exchangers, swept-volume flow
against the mixing relation, and the isentropic relation across the leakage
orifice).

| Inputs | Value | Parameters | Value |
|---|---|---|---|
| `t_amb` ambient temperature | 25 °C | `A_leak_cp` leakage area | 5·10⁻⁷ m² |
| `t_w_su_cd` / `p_w_su_cd` water supply | 25.5 °C / 400 kPa | `r_v_in_cp` volume ratio | 3.2 [-] |
| `t_glw_su_ev` brine supply | 0 °C | `W_dot_loss0_cp` constant losses | 150 W |
| `DELTAt_oh_ev` / `DELTAt_sc_cd` | 5 / 5 K | `alpha_cp` loss factor | 0.25 [-] |
| `M_dot_w_cd` water flow | 0.3889 kg/s | `M_dot_r_cp_n` nominal flow | 0.12 kg/s |
| `M_dot_glw_ev` brine flow | 1.11 kg/s | `AU_su_cp_n` / `AU_ex_cp_n` | 25 / 30 W/K |
| `X_cp` compressor load | 1 [-] | `AU_amb_cp` envelope-ambient | 10 W/K |
| `conc_glw` glycol concentration | 25 % | `V_s_cp_ref` reference swept volume | 9.478·10⁻⁵ m³ |
| `n_cp` number of compressors | 1 | `N_rot` rotation speed | 3000 tr/min |
| `fluid$` refrigerant | `R407C` | `R_m_ev` / `R_m_cd` metal resistance | 10⁻⁵ K/W |
| | | `R_glw_ev_n` / `R_r_ev_n` | 6·10⁻⁵ K/W |
| | | `R_w_cd_n` / `R_r_cd_n` | 3·10⁻⁴ K/W |

`P_ev`, `P_cd` and `M_dot_r` are **results** (they were wrongly listed as inputs by the first import).

## How to run

```bash
coolsolve ./brine_to_water_heat_pump_refsim.eescode
```

It converges from the shipped `.initials` (CoolProp-consistent values of the
solution) in one Newton pass per block (12 iterations over 86 blocks). **Hard
start otherwise:** the 76-variable block (compressor, both exchangers, the
leakage orifice) fails from the default guesses (*SingularJacobian* at
iteration 0, also with Try Harder) and, from the EES stored values (enthalpies
in the EES reference of R407C), the normal solve stops at *MaxIterations*
while the GUI **Try Harder** button converges it (96 iterations). Keep the
`.initials` when changing an input, or use Try Harder.

## Results

Default operating point (brine 1.11 kg/s from 0 °C, water 0.389 kg/s from
25.5 °C, ambient 25 °C):

| Variable | Value | | Variable | Value |
|---|---:|---|---|---:|
| `Q_dot_cd` heating power | 16.02 kW | | `M_dot_r` refrigerant flow | 0.07722 kg/s |
| `W_dot_cp` compressor power | 3.984 kW | | `t_ev` / `P_ev` | −3.66 °C / 438.1 kPa |
| `COP_heating` | 4.021 | | `t_cd` / `P_cd` | 42.90 °C / 1.769 MPa |
| `Q_dot_ev` evaporating power | 12.39 kW | | `t_ex_cp` compressor exhaust | 73.95 °C |
| `t_w_ex_cd` water exhaust | 35.34 °C | | `t_w_cp` fictitious envelope | 60.40 °C |
| `t_glw_ex_ev` brine exhaust | −2.81 °C | | `epsilon_s_cp` / `epsilon_v_cp` | 0.6786 / 0.9391 |
| `AU_cd` / `AU_ev` conductance | 1357 / 6417 W/K | | `epsilon_cd` / `epsilon_ev` | 0.5654 / 0.7665 |
| `Q_dot_su_cp` suction heating | 0.886 kW | | `r_p_cp` pressure ratio | 4.037 |
| `Q_dot_ex_cp` discharge cooling | −0.323 kW | | `P_thr_cp` throat pressure | 1.057 MPa |
| `Q_dot_amb_cp` loss to the ambient | 0.354 kW | | `M_dot_leak_cp` leakage flow | 0.00325 kg/s |
| `W_dot_in_cp` internal power | 3.067 kW | | `gamma_leak_cp` leakage exponent | 1.0386 |

The heat pump delivers 16.0 kW to the water (+9.84 K on 0.3889 kg/s) and takes
12.4 kW from the brine (−2.81 K on 1.11 kg/s, `cp_glw` = 3973.6 J/(kg·K)).
**Energy balances** (checked on the `.sol`): the compressor balance
`W_dot_cp = M_dot_r·(h_ex_cp − h_su_cp) + Q_dot_amb_cp` closes to round-off
(3983.79 = 0.077219·46 997.2 + 353.96 W), hence the cycle balance
`Q_dot_ev + W_dot_cp = Q_dot_cd + Q_dot_amb_cp`; the envelope balance
`W_dot_loss_cp = Q_dot_su_cp + Q_dot_ex_cp + Q_dot_amb_cp` (916.8 = 885.9 −
323.1 + 354.0 W) and the water and brine balances close as well. **Second law**:
`epsilon_s_cp` = 0.68 < 1, the suction gas is heated by the 60.4 °C envelope
(3.7 → 15.9 °C) and the 77.5 °C discharge gas is cooled by it, the brine
(0 → −2.8 °C) stays above the mean evaporating temperature (−3.7 °C) and the
water (25.5 → 35.3 °C) below the mean condensing temperature (42.9 °C).

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 evaporator exhaust, 2
compressor exhaust, 3 condenser exhaust, 4 evaporator supply) give the cycle on
the P-h or T-s diagram (CoolSolve *Diagram* tab, *Overlay array path*, *Close
cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle,
     figures/brine_to_water_heat_pump_refsim_ph.png -->

## Verification

Reference: the **stored solution of EES 7.888** in the source file (142 of its
146 variable records hold a value). `compare_solution.py
brine_to_water_heat_pump_refsim.sol reference/ees_variables.csv` (2026-11-01):

```
142 common variables, 95 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 19
```

| Variable | EES 7.888 | CoolSolve | rel. diff | Before the power fix |
|---|---:|---:|---:|---:|
| `COP_heating` [-] | 4.11234 | 4.02053 | 2.2e-02 | 4.18154 |
| `W_dot_cp` [W] | 3 760.12 | 3 983.79 | 5.6e-02 | 3 827.38 |
| `Q_dot_cd` [W] | 15 462.9 | 16 016.9 | 3.5e-02 | 16 004.3 |
| `Q_dot_ev` [W] | 11 933.2 | 12 387.1 | 3.7e-02 | 12 399.1 |
| `M_dot_r` [kg/s] | 0.0756131 | 0.0772188 | 2.1e-02 | 0.0772801 |
| `P_ev` / `P_cd` [Pa] | 436 183 / 1.73033e6 | 438 119 / 1.76867e6 | 4.4e-03 / 2.2e-02 | |
| `t_ex_cp` [°C] | 74.045 | 73.949 | 1.3e-03 | 73.623 |
| `epsilon_s_cp` [-] | 0.708898 | 0.678605 | 4.3e-02 | 0.706717 |
| `epsilon_v_cp` [-] | 0.941799 | 0.939053 | 2.9e-03 | 0.939848 |
| `c_p_su_cp` [J/(kg·K)] | 833.72 | 932.24 | 1.06e-01 | 932.23 |
| `cp_glw` [J/(kg·K)] | 3 973.62 | 3 973.62 | < 1e-9 | |

The differences have two causes, both identified:

1. **The energy-balance correction** (adaptation 2 of the Conversion log): the
   internal power now includes the recompressed leakage, +124 W of internal
   power and +155 W of electrical power (with `alpha_cp` = 0.25); this lowers
   `epsilon_s_cp` and `COP_heating` by about 4 % with respect to EES. The
   column *Before the power fix* is the same model with the original
   `M_dot_r·w_in_cp`: it is within 0.3–3.8 % of EES.
2. **The R407C properties of EES 7.888**, which are not those of the current
   reference equation of state: at the suction state (438 kPa, 3.6 °C) EES
   stores `c_p` = 833.7 J/(kg·K), while CoolProp gives 930.8 with its pseudo-pure
   R407C (Lemmon 2003) and 929.3 with its independent R32/R125/R134a mixture model
   (fluid string `R32[0.3811]&R125[0.1796]&R134a[0.4393]`, the mixture formulation
   REFPROP uses by default for R407C); the dew temperature at 436.2 kPa is
   −1.248 °C in EES and −1.554 °C in both CoolProp formulations. These feed
   `C_dot_su_cp`, the saturation temperatures of the exchangers and through
   them the operating pressures. The same EES-side R407C deviation is found in
   `CSL-0319` (EES 7.458). The absolute enthalpies and entropies of R407C are
   offset by about +143.4 kJ/kg and +763 J/(kg·K) (reference states).

The brine properties are not affected (`cp_glw`, `rho_glw_su_ev` agree to
1·10⁻⁹, same BrineProp tables as `CSL-0079`). `gamma_leak_cp` is solved by
the leakage relations (1.0386 against 1.0447 in EES). The 19 CoolSolve-only
variables are the diagram state points (`P[i]`, `h[i]`, `T[i]`, `s[i]`), the
added auxiliary `t_in_cp` of the `(s, v)` rewrite, and `fluid$`.

## Source and attribution

Reference simulation model by **Vincent Lemort** (ULiège Thermodynamics
Laboratory, Faculty of Applied Sciences), part of the ULiège model bank
(Laborelec toolkit lineage), dated 8 January 2008 in the file header
(`"Authors: Vincent Lemort"`); the `{$ID$…}` tag names the EES licence of
J. Lebrun's laboratory, not the author. The model cites Winandy, Saavedra &
Lebrun (2002), *Applied Thermal Engineering* 22, 107-120, as its reference for
the scroll compressor. The file carries the laboratory disclaimer reproduced in
its header (freely distributed, may not be sold, cite the origin); the library
is published under the MIT licence like the rest of the collection.

Source file (EES 7.888, English), collection of S. Quoilin, **inside a zip
archive that the collection does not extract**:
`~/Nextcloud/thermo_models/Model data bank/Heat_and_Cool_Production_Systems/Heat_Production_by_Vapor_Compression/BrinetoWaterHeatPump_RefSim_Model_VL080108.zip!/BrinetoWaterHeatPump_RefSim_EES_Model_VL080108.EES`
(inventory candidate `TM-0495`).

The same archive holds the **EXE version** of the model
(`BrinetoWaterHeatPump_RefSim_EXE_Model_VL080108.EXE`) and the `UserLib/BrineProp`
folder (`Brineprop.lib`, `Brineprop2.LIB`, `Brine1.lkt`, `Brine2.lkt`,
`BrineProp.chm`, `BRINEPROP.hlp`) the model calls implicitly; in CoolSolve the
library procedure and its tables (decoded from `Brine1.lkt`/`Brine2.lkt`) come
from the function model `CSL-0079`, through the line
`$INCLUDE brineprop_secondary_refrigerants`.
The candidate has **no `duplicate_group`** in the inventory: no ParamID
(parameter-identification) or simplified version of this heat pump exists in the
model bank, so nothing was merged into or split from this model.

## Conversion log

- **2026-10-05 — extraction** (`CoolSolve/tools/ees_extract.py`): EES 7.888,
  equations stored as **RTF**, unit system already `SI MASS DEG PA C J` (no
  conversion needed, no `$UnitSystem` directive in the library file), **no**
  lookup and no parametric table, licence tag removed. The report lists the
  functions `brineprop`, `density`, `enthalpy`, `entropy`, `exp`, `max`,
  `pressure`, `specheat`, `temperature`, `volume`; all but `brineprop` are
  built into CoolSolve. 146 variable records decoded, 143 of them holding a
  value, so the file **was run in EES** and its stored solution is the reference
  of the verification. The trailing NUL byte of the RTF conversion was removed
  (`CS-BUG-EXTRACT-NUL`, registered with `CSL-0036`): without it CoolSolve
  refuses the file.
- **2026-10-05 — inputs and parameters restored as assignments.** The equations
  window lists 9 inputs and 19 parameters of the control panel in its display
  strings, all commented out; five further names appear in the equations without
  being defined at all (the three inputs `P_ev`, `P_cd` and `M_dot_r` and the
  two parameters `M_dot_r_cp_n` and `V_s_cp_ref`). They are written as input assignments with the
  values of the **stored EES run**, which is the regression point of this card.
  The commented values of the original (what the diagram showed when the file
  was saved) differ from that run for 13 of them — `r_v_in_cp` 3.5 vs 3.2,
  `W_dot_loss0_cp` 175 vs 150 W, `alpha_cp` 0.45 vs 0.25, `AU_su_cp_nom` 4 vs
  `AU_su_cp_n` = 25 W/K, `AU_ex_cp_nom` 5 vs `AU_ex_cp_n` = 30 W/K,
  `DELTAt_sc_cd` 10 vs 5 K, `p_w_su_cd` 2·10⁵ vs
  4·10⁵ Pa, `t_w_su_cd` 30 vs 25.5 °C, `t_glw_su_ev` 5 vs 0 °C, `R_w_cd_n` and
  `R_r_cd_n` 6.36·10⁻⁴ vs 3·10⁻⁴ K/W, `M_dot_r_ev_n`/`M_dot_r_cd_n` 0.023 vs
  0.12 kg/s — the stored values are the ones used, as in `CSL-0072`.
  The equations use `AU_su_cp_n`, `AU_ex_cp_n` and `M_dot_r_cp_n` where the
  panel of the original lists `AU_su_cp_nom`, `AU_ex_cp_nom` and
  `M_dot_r_nom`: the three `*_nom` names exist in the binary as leftovers of an
  older version of the model (their records hold no value and they feed no
  equation) and are **not imported**; the names used by the equations are kept.
  `gamma_leak_cp` is left **commented out** in the native file, as in the
  original (`{gamma_leak_cp=1.03}`): the leakage relations of the original
  determine it (EES stores 1.0447).
- **2026-10-05 — the (s, v) property pair rewritten (decision D11 style).**
  `h_in_cp = enthalpy(fluid$,s=s_in_cp,v=v_in_cp)` and `p_in_cp =
  pressure(fluid$,s=s_in_cp,v=v_in_cp)` are valid EES but CoolProp returns
  NaN/Inf for the **(s, v)** pair, so both calls are rewritten with the
  equivalent `(P, s)` / `(T, v)` pair: an auxiliary temperature
  `t_in_cp = temperature(fluid$,P=p_in_cp,s=s_in_cp)` is added,
  `h_in_cp = enthalpy(fluid$,P=p_in_cp,s=s_in_cp)` and
  `p_in_cp = pressure(fluid$,T=t_in_cp,v=v_in_cp)`. Same states, valid EES,
  logged here and in the header; the gap is registered as `CS-GAP-PROP-SV`.
- **2026-10-05 — curation**: standard header, comments in English paraphrasing
  the comments of the original (its typos — *INPUtS*, *PARAMEtERS*,
  *elctrical*, *refrigerant* — are not reproduced), one equation per line with
  its SI unit in the comment. The three resistances in series stay written
  `1 / AU = R_a + R_m + R_r` as in the original, and the leakage relation keeps
  its `{_bis}` suffix (CoolSolve parses it). No equation was added, removed or
  re-arranged, no variable was renamed.
- **2026-10-05 — diagram support**: 16 post-processing equations (`P[i]`,
  `h[i]`, `T[i]`, `s[i]`, i = 1…4) added at the end of the model, as the
  workflow asks for cycles on a real fluid; they add no physics and change no
  result of the model.
- **2026-10-10 — unit labels**: string array `U$[…]` of `BRINEPROP` replaced by the lookup
  table `brine_to_water_heat_pump_refsim-Units.csv` and `LOOKUP$`
  (`UO$=LOOKUP$('Units',Pro,1)`), decision D14 (CoolSolve does not support string arrays).
- **2026-10-05 — runnable variant** `brine_to_water_heat_pump_refsim_coolsolve.eescode`
  (same pattern as `CSL-0072`/`CSL-0079`): the `BRINEPROP` procedure is split
  into the selector `BRINEPROP_SELECT` (range checks and fluid number, the
  `ELSE IF` ladders rewritten as sequential single-line `IF` statements with
  mutually exclusive conditions) and two property blocks **flattened** into the
  main program (`_rho` for the density, `_cp` for the specific heat, the
  procedure-internal variables renamed per call); the `REPEAT` loop of the
  procedure is expanded into its 18 explicit coefficient equations; the
  expression output `:cp_glw/1000` of the second call becomes
  `cp_glw = Funkt_cp` (the procedure output is `Funkt/1000`, so the two factors
  of 1000 cancel, same value). The **four duplicated relations of the original**
  (`h_ex1_cp` energy balance in the leakage orifice, `M_dot_s_cp` from the swept
  volume, and the effectiveness forms of `Q_dot_ev` and `Q_dot_cd`) are turned
  into post-processing **checks** with the same right-hand sides and the names
  `h_ex1_cp_chk`, `M_dot_s_cp_chk`, `Q_dot_ev_chk`, `Q_dot_cd_chk` (plus
  `Q_dot_ev_chk_brine`, `Q_dot_cd_chk_water`), because CoolSolve cannot solve an
  over-determined system; four equations of the original that have no simple
  left-hand side are written in the equivalent explicit form (`h_su2_cp`,
  `t_w_cp`, `AU_ev`, `AU_cd`, `C_thr_cp`) and `gamma_leak_cp` is fixed at the
  default value 1.03 of the commented line of the original (the isentropic
  relation across the orifice becomes the check `P_thr_chk`), which is why the
  variant is 1.4e-02 away from EES on that variable. The variant has its own
  companion tables (`brine_to_water_heat_pump_refsim_coolsolve-Brine1/Brine2.csv`,
  same decoded values) and its own `.initials` (EES stored solution plus guesses
  for the flattened variables).
- **2026-11-01 — adaptation (failing → verified)**, review of the failing
  models: (1) the three assignments `P_ev`, `P_cd`, `M_dot_r` added by the
  first import are removed (they are unknowns of the original, closed by the
  four "duplicated" relations, see *Model*); the system is square
  (161/161). (2) First-law check of the solution: the compressor balance
  `W_dot_cp = M_dot_r·(h_ex_cp − h_su_cp) + Q_dot_amb_cp` was open by 124 W
  (in EES as well: 121 W, the "1.4 % cycle imbalance" noted earlier), exactly
  `M_dot_leak_cp·w_in_cp`: the original computes the internal power with
  `M_dot_r` while the chamber compresses `M_dot_s_cp = M_dot_r + M_dot_leak_cp`.
  Corrected to `W_dot_in_cp = M_dot_s_cp·w_in_cp`, the form of the other scroll
  models of the library (`CSL-0007`, `CSL-0116`, `CSL-0260`); the balance now
  closes to round-off. (3) With a CoolProp-consistent starting point the
  76-variable block converges (it had been reported as non-converging from the
  EES-reference enthalpies); the `.initials` is that solution. (4) The
  `_coolsolve` variant (evaluated at the EES operating point with the four
  closures turned into checks) is superseded and removed with its two
  companion tables; its `.sol` baseline is replaced by the main file's.
  Status `verified` (EES stored solution, energy balances, R407C cross-check
  with two CoolProp formulations).
- **Level**: score 6 with [taxonomy.md §3](../docs/taxonomy.md) (166 equations
  → 1, largest block 30 → 2, a procedure but no discretisation array → 0,
  three coupled components → 1, semi-empirical calibration referred to nominal
  conditions → 1, curated guesses needed → 1) = level 3 by the table; lowered by
  one to **level 2** because the model is a single-zone description of one
  operating point of three components with explicit balances and no off-design,
  multi-zone or array treatment — the same profile as the other component models
  of the bank (`CSL-0074`, `CSL-0076`, `CSL-0077`), also rated level 2.

- **2026-11-05 — `$INCLUDE` instead of the copy**: the file carried a copy
  of `BRINEPROP` (another edition of `Brineprop.lib` than the one of
  `CSL-0079`: the same code and tables, other wording of the range-check
  messages, two surplus `ENDIF`s that CoolSolve reported, `P008`) and copies of
  its three tables. The copy and the three table files are removed; the file
  gets the line `$INCLUDE brineprop_secondary_refrigerants` after its header,
  and the header names `CSL-0079` instead of the companion tables. `BRINEPROP`
  is now the wrapper of the SI function `BrineProperty` of `CSL-0079` (same
  values; `'specheat'` in lower case is read as before). The model reproduces
  its baseline (1.4e-8, `DELTAt_su_cp`); the baseline is regenerated because
  the auxiliary variable of the `:cp_glw/1000` output is named after its line
  (`__out1_BRINEPROP_L412` → `__out1_BRINEPROP_L262`).

## Limitations and CoolSolve gaps

- **Adapted from the original** (2026-11-01, see *Conversion log*): the
  internal compressor power counts the recompressed leakage
  (`M_dot_s_cp·w_in_cp` instead of `M_dot_r·w_in_cp`), which closes the
  compressor energy balance (open by 124 W in the original, in EES as well);
  the results therefore differ from the stored EES run by up to 5.6 % on the
  compressor power. `P_ev`, `P_cd` and `M_dot_r` are unknowns, as in the
  original (an earlier version of this import assigned them).
- **Hard model for the solver**: the 76-variable block needs the shipped
  `.initials` (or **Try Harder** from the EES stored values); from the default
  guesses it fails with *SingularJacobian* at iteration 0, even with Try Harder
  (CoolSolve hint: the default guess of 1.0 for enthalpies and pressures gives
  states outside the R407C domain; a thermodynamically consistent default
  start, as the multi-start candidates build, already at the first attempt,
  would help).
- The companion tables are the ones EES expects for the procedure's `LOOKUP`
  calls (decoded from the binary `.lkt` files, as in `CSL-0072`).
- **`CS-GAP-PROP-SV`**: property calls with the
  **(s, v)** input pair, `enthalpy(fluid$,s=…,v=…)` and
  `pressure(fluid$,s=…,v=…)`. Valid EES (the source file writes both and stores
  their solution), unsupported by CoolProp; the equivalent `(P, s)` /
  `(T, v)` pair is used instead, in the native file as well.
- **Variable bounds are not supported** (`CS-GAP-BOUNDS`): EES bounded
  `M_dot_r`, `M_dot_leak_cp` and `M_dot_s_cp` to [0, 1] kg/s, `v_thr_cp` to
  [0, ∞), `gamma_leak_cp` to [0, 2] and the flow rates to [0, ∞); the equations
  keep the results in range at this operating point.
- The compressor model is the scroll machine of the original, but the isochoric
  step is a single relation between the adapted pressure and the discharge
  pressure (no chamber volume or valve relation), and the leakage orifice is
  described by a constant area and a single isentropic coefficient: the model
  is not usable far from this operating point, and the leakage coefficient
  `gamma_leak_cp` is not identified here.
- The heat exchangers are described by three resistances and an effectiveness
  only: no plate-by-plate or tube-by-tube description, no maldistribution and
  no pressure drop; the brine and water pressure drops are neglected (the
  minimum flow rates of section 4.2.4 and 4.3.4 of the original are
  diagnostics, they feed no equation).

## Related models

- `CSL-0077` *aircooled_chiller_refsim*: same model bank and the same
  four-step scroll compressor with its fictitious envelope; that model runs on
  R22 with an air-cooled condenser and humid air.
- `CSL-0079` *brineprop_secondary_refrigerants*: the function library whose
  `BRINEPROP` procedure (included, with its tables) gives the density and
  specific heat of the 25 % propylene glycol solution.
- `CSL-0072` *centrifugal_brine_pump_refsim*: another model of the bank
  that calls the same BrineProp library (verified on its native file).
- `CSL-0007` *scroll_compressor_semi_empirical*: the same scroll machine at a
  different level of detail (semi-empirical characteristic maps).
- `CSL-0081` *vertical_ghes_refsim*: the borefield (ground source) that feeds
  such a brine loop, from the same model bank; dynamic, blocked and without a
  runnable variant.
- `CSL-0068` *heat_pump_scroll_compressor_data_check*: a data-consistency check
  of a scroll compressor heat pump on the same refrigerant family.
- `CSL-0155` *inverter_air_water_heat_pump*: air-to-water counterpart of this complete heat-pump system model (Daikin Altherma type, heating branch imported).
- `CSL-0260` *scroll_compressor_reed_valve*: the scroll compressor reference model with a discharge reed valve, same R407C family.

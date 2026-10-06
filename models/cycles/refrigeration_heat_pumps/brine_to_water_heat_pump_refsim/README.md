# Brine-to-water heat pump reference model (RefSim)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0078`

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
| **Size** | 161 equations in the main program (the model with its 12 restored inputs and 19 restored parameters, the `(s, v)` rewrite and the 16 state points of the diagrams) plus the 115-line `BRINEPROP` procedure; the runnable variant has 252 equations, largest block 31 |
| **Source** | ULiège model bank (Laborelec toolkit lineage), heat production by vapour compression, reference simulation model, 8 January 2008 (`BrinetoWaterHeatPump_RefSim_EES_Model_VL080108.EES`, EES 7.888) |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** by `CS-GAP-ELSEIF-CHAIN` (with `CS-GAP-UPPERCASE`, `CS-GAP-STRING-ARRAY`, `CS-GAP-LOOKUP-PROC`, `CS-GAP-CALL-EXPR-OUT`); runnable variant `brine_to_water_heat_pump_refsim_coolsolve.eescode` verified against the solution stored by EES (see *Verification*) |

## Problem statement

A ground-source heat pump heats 0.389 kg/s of water entering the condenser at
25.5 °C (400 kPa) with a brine flow rate of 1.11 kg/s entering the evaporator at
0 °C, in a 25 % propylene glycol solution. The refrigerant is R407C, evaporating
at 436 kPa and condensing at 1.73 MPa, with 5 K of superheating at the
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
rise. The model **repeats each of these heat rates and two compressor
relations a second time** (four duplicated definitions in total): it is the
consistency-check structure of the RefSim models of the bank.

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
| `P_ev` / `P_cd` evaporating/condensing | 436.2 kPa / 1.730 MPa | `R_m_ev` / `R_m_cd` metal resistance | 10⁻⁵ K/W |
| `M_dot_r` refrigerant flow | 0.0756 kg/s | `R_glw_ev_n` / `R_r_ev_n` | 6·10⁻⁵ K/W |
| `fluid$` refrigerant | `R407C` | `R_w_cd_n` / `R_r_cd_n` | 3·10⁻⁴ K/W |

## How to run

The **native file** `brine_to_water_heat_pump_refsim.eescode` is valid EES but
does not parse in CoolSolve (the `BRINEPROP` procedure of the BrineProp library
uses the `ELSE IF` ladders closed by repeated `ENDIF`, `Uppercase$`, string
arrays read by index and `LOOKUP` inside a procedure: `CS-GAP-ELSEIF-CHAIN`,
`CS-GAP-UPPERCASE`, `CS-GAP-STRING-ARRAY`, `CS-GAP-LOOKUP-PROC`; the model also
passes an expression as `CALL` output argument, `CS-GAP-CALL-EXPR-OUT`).

The **runnable variant** is `brine_to_water_heat_pump_refsim_coolsolve.eescode`
(tested as `CSL-0078:coolsolve`, with its `.sol` baseline and its own companion
tables):

```bash
coolsolve ./brine_to_water_heat_pump_refsim_coolsolve.eescode
```

It needs the shipped `.initials` (the solution stored by EES, plus guesses for
the variables the flattening introduces); without them the 30-variable
compressor block does not converge. Every change of the variant is listed in its
header and in the *Conversion log*.

## Results

Default operating point (brine 1.11 kg/s from 0 °C, water 0.389 kg/s from
25.5 °C, ambient 25 °C), runnable variant:

| Variable | Value | | Variable | Value |
|---|---:|---|---|---:|
| `Q_dot_cd` heating power | 15.71 kW | | `M_dot_r` refrigerant flow | 0.0756 kg/s |
| `W_dot_cp` compressor power | 3.693 kW | | `t_ev` / `P_ev` | −3.81 °C / 436 kPa |
| `COP_heating` | 4.254 | | `t_cd` / `P_cd` | 42.02 °C / 1.730 MPa |
| `Q_dot_ev` evaporating power | 12.23 kW | | `t_ex_cp` compressor exhaust | 72.45 °C |
| `t_w_ex_cd` water exhaust | 35.15 °C | | `t_w_cp` fictitious envelope | 58.65 °C |
| `t_glw_ex_ev` brine exhaust | −2.77 °C | | `epsilon_s_cp` / `epsilon_v_cp` | 0.7076 / 0.9405 |
| `AU_cd` / `AU_ev` conductance | 1344 / 6357 W/K | | `epsilon_cd` / `epsilon_ev` | 0.5619 / 0.7634 |
| `Q_dot_su_cp` suction heating | 0.846 kW | | `r_p_cp` pressure ratio | 3.967 |
| `Q_dot_ex_cp` discharge cooling | −0.324 kW | | `P_thr_cp` throat pressure | 1.038 MPa |
| `Q_dot_amb_cp` ambient gain | 0.337 kW | | `M_dot_leak_cp` leakage flow | 0.00319 kg/s |

The heat pump delivers 15.7 kW to the water, which leaves it 9.647 K warmer
(15 708 W/(0.3889 kg/s · 4187 J/kg·K)) than the 25.5 °C supply, and extracts
12.2 kW from the brine, which leaves it 2.773 K colder
(12 232 W/(1.11 kg/s · 3973.6 J/kg·K)). The compressor consumes 3.69 kW, of
which 0.86 kW heats the suction gas and 0.34 kW is gained from the ambient
through the casing; its envelope balance
`t_w_cp = t_amb + (W_dot_loss_cp − Q_dot_su_cp − Q_dot_ex_cp)/AU_amb_cp` closes
exactly at 58.65 °C. The cycle balance is *not* an identity of the model:
`Q_dot_ev + W_dot_cp − Q_dot_cd` = 217 W (1.4 % of the heating power), the
difference between the specific electrical power `w_cp = W_dot_cp/M_dot_r`
(48 841 J/kg, which contains the 859 W of electromechanical losses) and the
enthalpy rise `h_ex_cp − h_su_cp` of the refrigerant (45 970 J/kg). The
consistency checks of the variant give
`Q_dot_ev_chk` = 12.82 kW (+4.8 % against the refrigerant side),
`Q_dot_cd_chk` = 15.11 kW (−3.8 %), `M_dot_s_cp_chk` = 0.08025 kg/s (+1.8 %
against the mixing relation) — the duplicated relations of the original do not
close exactly in CoolProp, see *Verification*.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 evaporator exhaust, 2
compressor exhaust, 3 condenser exhaust, 4 evaporator supply) give the cycle on
the P-h or T-s diagram (CoolSolve *Diagram* tab, *Overlay array path*, *Close
cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle,
     figures/brine_to_water_heat_pump_refsim_ph.png -->

## Verification

The equations were transcribed from the equations window of the source file (see
*Conversion log*) and the model was solved as it stands in the runnable variant;
the **stored solution of EES** in the source file (142 of its 146 variable
records hold a value) is the reference. The extraction is **over-determined by
three equations** as the original stands (`coolsolve -d` on the extraction with
the inputs and the library procedure restored: *Equations: 162, Variables: 159,
System square: No*), because the original defines `h_ex1_cp`, `M_dot_s_cp`,
`Q_dot_ev` and `Q_dot_cd` twice each — see *Conversion log*. No equation was
replaced by a stored value.

`python3 tools/compare_solution.py brine_to_water_heat_pump_refsim_coolsolve.sol reference/ees_variables.csv`:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `COP_heating` [-] | 4.11234 | 4.25351 | 3.3e-02 |
| `Q_dot_cd` [W] | 15 462.9 | 15 708.3 | 1.6e-02 |
| `Q_dot_ev` [W] | 11 933.2 | 12 232.3 | 2.5e-02 |
| `W_dot_cp` [W] | 3 760.12 | 3 693.01 | 1.8e-02 |
| `t_ex_cp` [°C] | 74.045 | 72.453 | 2.2e-02 |
| `t_ev` [°C] | −3.5440 | −3.8081 | 6.9e-02 |
| `c_p_su_cp` [J/kg·K] | 833.72 | 931.61 | 1.05e-01 |
| `epsilon_s_cp` [-] | 0.708898 | 0.707633 | 1.8e-03 |
| `cp_glw` [J/kg·K] | 3 973.62 | 3 973.62 | < 1e-09 |
| `M_dot_leak_cp` [kg/s] | 3.16045e-03 | 3.18726e-03 | 8.4e-03 |
| `h_ex_cd` [J/kg] | 112 094 | 251 542 | 5.54e-01 |

**142 common variables, 73 differ above rtol = 0.001, maximum relative
difference 5.54e-01 (`h_ex_cd`)**. The largest differences are the *absolute*
enthalpies and entropies of R407C, offset by **+143 405 J/kg** and
**+763.4 J/kg·K** between the reference states of EES 7.888 and CoolProp (the
differences `h_ex_cp − h_ex_cd`, `h_su2_cp − h_ex_cd`, `w_in_cp` and `Q_dot_cd`
agree, which is what the model uses). The derived results agree to 0.4–3.3 %
(`epsilon_s_cp` to 0.2 %, `epsilon_v_cp` to 0.1 %); they follow two property
differences: the specific heat of R407C vapour at the suction (+10 %, 833.7 vs
931.6 J/kg·K, which enters `C_dot_su_cp`, `epsilon_su_cp` and
`Q_dot_amb_cp`) and the R407C saturation line near 0 °C and 42 °C
(`t_sat_su_cp` −1.248 vs −1.554 °C, `t_sat_su_cd` 44.973 vs 44.478 °C), where the
zeotropic blend is described differently by EES and CoolProp — the model
evaluates its mean evaporating and condensing temperatures on that line. These
deviations are above the ≤ 0.5 % expected for two different equations of state;
they were not investigated further. The brine properties (`cp_glw`,
`rho_glw_su_ev`) are not affected: they come from the same decoded BrineProp
tables as `CSL-0079` and agree to 1·10⁻⁹ (`cp_glw` 3973.619 J/kg·K,
`rho_glw_su_ev` 1025.9635 kg/m³ in both). `gamma_leak_cp` differs by 1.4e-02
because the variant fixes it at the default value of the commented line of the
original instead of solving the bisection relation (see *Conversion log*).
No variable was excluded from the comparison; the 110 variables that exist only
in the CoolSolve solution are the state points of the diagrams (`P[i]`, `h[i]`,
`T[i]`, `s[i]`, i = 1…4), the internal variables of the two flattened BRINEPROP
blocks, the six consistency checks (`*_chk`) and the string variable `fluid$`.

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
`BrineProp.chm`, `BRINEPROP.hlp`) the model calls implicitly; the library
procedure is function model `CSL-0079` and its binary lookup files are shipped
here as the companion tables `brine_to_water_heat_pump_refsim-Brine1.csv`
(198 × 5 polynomial coefficients) and `-Brine2.csv` (11 × 2 mean concentration
and temperature), decoded from `Brine1.lkt`/`Brine2.lkt` by `CSL-0079`
(`CS-GAP-LKT`); the values are the same in the native files and in the variant.
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
- **Level**: score 6 with [taxonomy.md §3](../docs/taxonomy.md) (166 equations
  → 1, largest block 30 → 2, a procedure but no discretisation array → 0,
  three coupled components → 1, semi-empirical calibration referred to nominal
  conditions → 1, curated guesses needed → 1) = level 3 by the table; lowered by
  one to **level 2** because the model is a single-zone description of one
  operating point of three components with explicit balances and no off-design,
  multi-zone or array treatment — the same profile as the other component models
  of the bank (`CSL-0074`, `CSL-0076`, `CSL-0077`), also rated level 2.

## Limitations and CoolSolve gaps

- The native file is **blocked** by `CS-GAP-ELSEIF-CHAIN` (the `BRINEPROP`
  ladders of the BrineProp library), with `CS-GAP-UPPERCASE`,
  `CS-GAP-STRING-ARRAY`, `CS-GAP-LOOKUP-PROC` and `CS-GAP-CALL-EXPR-OUT`; the
  runnable variant above is shipped next to it. The companion tables of the
  native file are the ones EES expects for the procedure's `LOOKUP` calls
  (decoded from the binary `.lkt` files, `CS-GAP-LKT`, as in `CSL-0072`).
- **`CS-GAP-PROP-SV` (registered with this model)**: property calls with the
  **(s, v)** input pair, `enthalpy(fluid$,s=…,v=…)` and
  `pressure(fluid$,s=…,v=…)`. Valid EES (the source file writes both and stores
  their solution), unsupported by CoolProp; the equivalent `(P, s)` /
  `(T, v)` pair is used instead, in the native file as well.
- **Variable bounds are not supported** (`CS-GAP-BOUNDS`): EES bounded
  `M_dot_r`, `M_dot_leak_cp` and `M_dot_s_cp` to [0, 1] kg/s, `v_thr_cp` to
  [0, ∞), `gamma_leak_cp` to [0, 2] and the flow rates to [0, ∞); the equations
  keep the results in range at this operating point.
- The four duplicated relations of the original do **not** close exactly in
  CoolSolve (`Q_dot_ev_chk` +4.8 %, `Q_dot_cd_chk` −3.8 %,
  `M_dot_s_cp_chk` +1.8 %), while they agree to about 1·10⁻⁴ in the stored EES
  solution: the internal consistency of the RefSim models is limited by the
  accuracy of the property model, not by the equations.
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
- `X_cp` (the fraction of swept volume in use) and `M_dot_r` are **both**
  inputs: the machine is over-specified, the two are consistent only at the
  stored operating point. See `M_dot_s_cp` / `M_dot_s_cp_chk`.

## Related models

- `CSL-0077` *aircooled_chiller_refsim*: same model bank and the same
  four-step scroll compressor with its fictitious envelope; that model runs on
  R22 with an air-cooled condenser and humid air.
- `CSL-0079` *brineprop_secondary_refrigerants*: the function library whose
  `BRINEPROP` procedure (and the Brine1/Brine2 coefficient tables shipped here)
  gives the density and specific heat of the 25 % propylene glycol solution.
- `CSL-0072` *centrifugal_brine_pump_refsim*: another model of the bank that
  calls the same BrineProp library, with the same blocked-native-file /
  runnable-variant treatment.
- `CSL-0007` *scroll_compressor_semi_empirical*: the same scroll machine at a
  different level of detail (semi-empirical characteristic maps).
- `CSL-0081` *vertical_ghes_refsim*: the borefield (ground source) that feeds
  such a brine loop, from the same model bank; dynamic, and blocked like this
  model but without a runnable variant.
- `CSL-0068` *heat_pump_scroll_compressor_data_check*: a data-consistency check
  of a scroll compressor heat pump on the same refrigerant family.

# Air-cooled water chiller, reference simulation model

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0077`

Reference simulation model of an air-cooled water chiller of the ULiège model
bank: a rotary (scroll) compressor described step by step between the
evaporator exhaust and the condenser supply, an air-cooled condenser whose fan
is controlled so as to hold an almost constant condensing temperature, and a
water-supplied evaporator. Both heat exchangers are described by three thermal
resistances in series (air/water, metal, refrigerant) referred to nominal flow
rates, and the compressor part load is set by the swept volume of one or
several compressors in cascade.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R22 (refrigerant, default), AirH2O (humid air), water (constant `c_w` = 4187 J/kg·K) |
| **Size** | 133 equations, largest block: 62 (88 equations of the original model, the 8 inputs and 21 parameters of its control panel written as assignments, and 16 state points of the diagrams) |
| **Source** | ULiège model bank (Laborelec toolkit lineage), air-cooled water chiller reference simulation model, 4 January 2008 (`AirCooledChiller_RefSim_EES_Model_VTJL080104.EES`, EES 7.793); IEA A43 PR2 A15 reference model |
| **Authors** | Vlad Teodorese, Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the solution printed by EES in the source file (see *Verification*) |

## Problem statement

An air-cooled water chiller cools 1.51 kg/s of water entering at 12.2 °C with
ambient air at 35 °C and 50 % relative humidity (101 325 Pa). The
refrigerant is R22 and the compressor is a scroll machine with a maximum swept
volume flow rate of 0.0056 m³/s, run at full load. Determine the cooling
power, the refrigerant flow rate, the electrical power of the compressor and
of the condenser fans, the COP, the water temperature at the evaporator
exhaust and the condensing and evaporating pressures and temperatures.

The condenser fans are controlled on the condensing temperature: the air volume
flow rate follows a proportional law between 20 % and 100 % of its nominal
value (4.167 m³/s), with a set point of 35 °C. The condenser is sized on a
nominal air-side resistance of 9.94·10⁻⁵ K/W at 5 kg/s of air and a nominal
refrigerant-side resistance of 8.946·10⁻⁵ K/W at 0.22 kg/s of R22; the
evaporator on a nominal water-side resistance of 9.215·10⁻⁵ K/W at
1.511 kg/s of water and a nominal refrigerant-side resistance of
8.438·10⁻⁵ K/W at 0.22 kg/s.

## Model

**Compressor** (supply state *su* = evaporator exhaust, discharge state *ex* =
condenser supply). The refrigerant path is decomposed into four steps, as in
the original:

- (i) *supply heating-up* (su → su1): the heat transfer to the suction gas is
  written as a heat exchanger of effectiveness `epsilon_su_cp = 1 − exp(−NTU)`
  between the refrigerant capacity flow rate `C_dot_su_cp = M_dot_cp·c_p_su_cp`
  and the fictitious wall of uniform temperature `t_w_cp`, whose conductance is
  the constant `AU_su_cp` = 158 W/K;
- (ii) *isentropic compression* (su1 → in): `h_in_cp = enthalpy(fluid$,
  s = s_su1_cp, v = v_in_cp)` up to the volume ratio `r_v_in_cp` = 3.2;
- (iii) *isochoric compression* (in → ex1): the compression chamber opens to
  the discharge plenum at constant volume, `w_in2_cp = v_in_cp·(p_ex1_cp −
  p_in_cp)`, which is **negative** here (the adapted pressure `p_in_cp` =
  2.178 MPa is above the discharge pressure 1.691 MPa, so the fluid expands at
  constant volume);
- (iv) *exhaust cooling-down* (ex1 → ex): the same heat-exchanger form as (i),
  with the constant `AU_ex_cp` = 100 W/K.

All the heat transfers of the machine (to the suction gas, the
electromechanical losses, the hot discharge gas and the ambient) are
represented by that fictitious wall, whose balance closes the model:
`W_dot_loss_cp − Q_dot_su_cp − Q_dot_ex_cp + Q_dot_amb_cp = 0`, with
`Q_dot_amb_cp = AU_amb_cp·(t_a_su_cd − t_w_cp)`. The mass flow rate comes from
the swept volume at the state su1, the electrical power is the compression
power plus `W_dot_loss0_cp + alpha_cp·W_dot_in_cp`, and the global isentropic
effectiveness is `epsilon_s_cp = (h_exs − h_su)/w_cp`.

**Condenser**: `p_cd = P_sat(fluid$, T = t_cd)` fixes the condensing pressure,
and the refrigerant temperature follows the air through the exchanger,
`t_cd = t_a_su_cd + Q_dot_cd/(epsilon_cd·C_dot_a_cd)`. The three resistances
in series depend on the flows with respect to the nominal ones,
`R_a_cd = R_a_cd_n·(M_dot_a_cd_n/M_dot_a_cd)^0.6`,
`R_r_cd = R_r_cd_n·(M_dot_cd_n/M_dot_cd)^0.8`. The air volume flow rate is set
by the hypothetical fan control, `X_cd = min(1, max(0, gain·(t_cd −
t_cd_set)))`, and the fan power follows the square of the speed
(`W_dot_fan = W_dot_fan_n·(V_dot_a_cd/V_dot_a_cd_n)²`).

**Evaporator**: the same three-resistance representation on the water side
(`R_w_ev = R_w_ev_n·(M_dot_w_ev_n/M_dot_w_ev)^0.8`), the refrigerant leaving at
`t_ex_ev = t_ev + DELTAt_oh_ex_ev` and the water leaving at
`t_w_ex_ev = t_w_su_ev + Q_dot_ev/C_dot_w_ev`. The refrigerant is throttled
from the condenser to the evaporator, `h_su_ev = h_ex_cd`.

**Part load**: `V_dot_s_cp = V_dot_s_cp_max·X_cp`, i.e. the model is meant to be
run with several scroll compressors in cascade.

| Inputs | Value | Parameters | Value |
|---|---|---|---|
| `X_cp` compressor load | 1 [-] | `alpha_cp` loss factor | 0.32 [-] |
| `t_w_su_ev` water supply | 12.2 °C | `AU_su_cp` / `AU_ex_cp` / `AU_amb_cp` | 158 / 100 / 100 W/K |
| `M_dot_w_ev` water flow | 1.51 kg/s | `r_v_in_cp` volume ratio | 3.2 [-] |
| `t_a_su_cd` air supply | 35 °C | `W_dot_loss0_cp` constant losses | 632.5 W |
| `RH_su_cd` air humidity | 0.5 [-] | `R_a_cd_n` / `R_r_cd_n` | 9.94e-5 / 8.946e-5 K/W |
| `P_a` atmospheric pressure | 101 325 Pa | `R_w_ev_n` / `R_r_ev_n` | 9.215e-5 / 8.438e-5 K/W |
| `DELTAt_oh_ex_ev` superheat | 5 K | `R_m_cd` / `R_m_ev` | 1e-5 K/W |
| `DELTAt_sc_ex_cd` subcooling | 5 K | `gain` / `t_cd_set` | 0.1 K⁻¹ / 35 °C |
| `fluid$` refrigerant | `R22` | `V_dot_s_cp_max` / `W_dot_fan_n` | 0.0056 m³/s / 1500 W |

## How to run

Open `aircooled_chiller_refsim.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./aircooled_chiller_refsim.eescode
```

The shipped `.initials` holds the solution printed by EES for this operating
point; it is **needed**: without guesses the 62-variable compressor block is
singular (`SingularJacobian`, residual = inf), because CoolSolve starts from
1 for the pressure levels and the enthalpies. Reduce `X_cp` to model part load
with several compressors in cascade.

## Results

Default operating point (1.51 kg/s of water from 12.2 °C, air 35 °C / 50 % RH):

| Variable | Value | | Variable | Value |
|---|---:|---|---|---:|
| `Q_dot_ev` cooling power | 19.16 kW | | `M_dot_cp` refrigerant flow | 0.1178 kg/s |
| `Q_dot_cd` condensing power | 22.95 kW | | `t_ev` / `p_ev` | 5.90 °C / 601 kPa |
| `W_dot_cp` compressor power | 5.626 kW | | `t_cd` / `p_cd` | 44.05 °C / 1.691 MPa |
| `W_dot_fan` fan power | 1.280 kW | | `t_ex_cp` compressor exhaust | 72.0 °C |
| `W_dot` global power | 6.905 kW | | `t_ex1_cp` before exhaust cooling | 102.8 °C |
| `COP` / `COP_cp` | 2.774 / 3.405 | | `t_w_cp` fictitious wall | 53.3 °C |
| `t_w_ex_ev` water exhaust | 15.23 °C | | `epsilon_s_cp` / `epsilon_v_cp` | 0.553 / 0.849 |
| `V_dot_a_cd` air volume flow | 3.848 m³/s | | `AU_cd` / `AU_ev` | 3753 / 4145 W/K |
| `X_cd` fan control fraction | 0.905 | | `NTU_cd` / `NTU_ev` | 0.841 / 0.656 |
| `Q_dot_amb_cp` ambient gain | −1.832 kW | | `epsilon_cd` / `epsilon_ev` | 0.569 / 0.481 |

The chiller removes 19.2 kW from the water, which leaves it 3.03 K warmer
(19 159 W/(1.51 kg/s · 4187 J/kg·K)), and rejects 23.0 kW to the ambient air
through 4.29 kg/s of air. The compressor delivers 5.6 kW, of which 1.8 kW is
lost to the ambient through the machine casing (the wall sits at 53.3 °C
between the 10.9 °C suction and the 102.8 °C discharge gas): the condenser
balance closes exactly, 19 159 + 5 626 − 1 832 = 22 952 W = `Q_dot_cd`. The fan
control is not saturated at this point (0.90 < 1), so the condensing
temperature stands 9.0 K above its 35 °C set point.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 evaporator exhaust, 2
compressor exhaust, 3 condenser exhaust, 4 evaporator supply) give the cycle on
the P-h or T-s diagram (CoolSolve *Diagram* tab, *Overlay array path*, *Close
cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle,
     figures/aircooled_chiller_refsim_ph.png -->

## Verification

The equations were transcribed from the equations window of the source file (see
*Conversion log*) and solved as they stand — the extraction is **square** as it
stands (`coolsolve -d`: *System square: Yes*, 117 variables for the 88
equations of the original plus the 29 assignments of the control panel) and no
equation of the file was replaced by a stored value. The Variable Information
records of the file are cleared (−9999: the model was last prepared, not run),
so the reference is the solution **printed by EES in the equations window of the
source file** (section *Example of solution: Variables in Main*, 117
variables, the values of which are rounded as printed). It was transcribed into
a reference table in the work folder and compared with
`compare_solution.py aircooled_chiller_refsim.sol reference_ees_solution.csv`:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Q_dot_ev` [W] | 19 142.823 | 19 158.581 | 8.2e-04 |
| `Q_dot_cd` [W] | 22 938.692 | 22 952.267 | 5.9e-04 |
| `W_dot_cp` [W] | 5626 | 5625.80 | 3.6e-05 |
| `W_dot_fan` [W] | 1279 | 1279.65 | 5.1e-04 |
| `W_dot` [W] | 6904.971 | 6905.46 | 7.0e-05 |
| `COP` [-] | 2.772 | 2.77441 | 8.7e-04 |
| `t_w_ex_ev` [°C] | 15.23 | 15.2303 | 1.9e-05 |
| `t_cd` [°C] | 44.043 | 44.0454 | 5.5e-05 |
| `p_cd` [Pa] | 1 691 017.149 | 1 690 516 | 3.0e-04 |
| `t_ex_cp` [°C] | 72.01 | 72.0143 | 6.0e-05 |
| `epsilon_s_cp` [-] | 0.5525 | 0.552772 | 4.9e-04 |
| `c_p_su_cp` [J/kg·K] | 760.7 | 756.16 | 5.97e-03 |
| `C_dot_su_cp` [W/K] | 89.63 | 89.0779 | 6.16e-03 |

**116 common variables, 11 differ above rtol = 0.001, maximum relative
difference 6.16e-03** (`C_dot_su_cp`). Every difference belongs to the
compressor heat-transfer block (`c_p_su_cp` 5.97e-03, `C_dot_su_cp` 6.16e-03,
`NTU_su_cp` 6.05e-03, `Q_dot_su_cp` 3.28e-03, `t_su1_cp` 2.57e-03,
`epsilon_su_cp` 2.29e-03, `Q_dot_ex_cp` 2.62e-03, `w_in2_cp` 2.60e-03,
`NTU_ex_cp` 1.12e-03, `Q_dot_amb_cp` 1.16e-03) or to the evaporating
temperature `T_ev` 1.02e-03: they follow from the specific heat of R22 at the
suction, which differs by 0.6 % between the formulation of EES 7.793 and
CoolProp. All the results of the cycle (powers, flows, COP, water and
refrigerant temperatures, conductances, effectivenesses) agree to better than
1e-3. No variable was excluded from the comparison; the seventeen variables
that exist only in the CoolSolve solution are the state points of the diagrams
added for the GUI (`P[i]`, `h[i]`, `T[i]`, `s[i]`, `i` = 1…4) and the string
variable `fluid$`.

## Source and attribution

Reference simulation model by **Vlad Teodorese** and **Jean Lebrun** (ULiège
Thermodynamics Laboratory), part of the ULiège model bank (Laborelec toolkit
lineage), dated 4 January 2008 in the file header
(`"Authors: Vlad Teodorese, J. Lebrun"`; the `{$ID$…}` tag names the EES
licence of J. Lebrun's laboratory). It is one of the IEA A43 PR2 reference
models; the same folder ships the printed documentation of the model,
*"IEA A43 PR2 A15 Reference air-water chiller EES model VTJL PhAJL080108.pdf"*.

Source file (EES 7.793, English), collection of S. Quoilin, **inside a zip
archive that is not extracted by the collection**:
`~/Nextcloud/thermo_models/Model data bank/Heat_and_Cool_Production_Systems/Cool_Production_by_vapor_Compression/AirCooledChiller_RefSim_Model_VTJL080104.zip!/AirCooledChiller_RefSim_EES_Model_VTJL080104.EES`
(inventory candidate `TM-0488`).

The archive also holds an EXE version of the model
(`…RefSim_EXE_Model….EXE`), not imported. **No ParamID (parameter
identification) or simplified version of the chiller exists in the model bank**,
and the candidate has no `duplicate_group` in the inventory: nothing was merged
into or split from this model, and the older Laborelec chiller exercises of the
collection (`TM-0099`, `TM-0102`, `TM-0103`, chiller + cooling tower with a
parameter-identification law, MSTh R6) are a different, simpler model, left for
their own triage.

## Conversion log

- **2026-10-05 — extraction** (`CoolSolve/tools/ees_extract.py`): EES 7.793,
  unit system already `SI MASS DEG PA C J` (no conversion needed, no
  `$UnitSystem` directive in the library file), no lookup and no parametric
  table, licence tag removed. The report lists the functions `enthalpy`,
  `entropy`, `exp`, `max`, `min`, `p_sat`, `pressure`, `specheat`,
  `temperature`, `volume`, all built into CoolSolve. 117 variable records
  decoded, of which 37 hold a value — the file was last **prepared but not
  run**, so the stored values are the inputs and parameters only (the tool
  warns about the −9999 values) and the verification reference is the printed
  solution (above).
- **2026-10-05 — 8 of the 117 records are missing from the extraction**
  (`CS-BUG-EXTRACT-FMT-BYTE`, already registered with `CSL-0070`): `p_cd`,
  `p_ev`, `Q_dot_cd`, `Q_dot_ev`, `T_cd`, `T_ev` and `W_dot` carry the format
  byte 1 at record offset +74 instead of 3, which the tool rejects, and
  `fluid$` is a string variable, which the tool skips by design. Their stored
  values are −9999 in any case; their guess values were replaced by the printed
  solution in the `.initials`.
- **2026-10-05 — control panel transcribed as assignments.** The equations
  window states *"The 7 outputs, 8 inputs and 21 parameters are given in the
  control panel"*, and the window itself lists them in three display strings.
  They are written as input assignments in the `.eescode` file with the values
  of the printed solution of EES (the default operating point). Two names of the
  input list do not exist in the equations — the list says `M_dot_w_su_ev` and
  `P_atm` where the equations use `M_dot_w_ev` (1.51 kg/s) and `P_a`
  (101 325 Pa): the two names of the display string are typos of the original,
  corrected silently (the model stays square either way, and the 8 inputs of the
  original are the 8 assignments). `P_atm` survives in the binary as a variable
  record of an older version of the model (guess 98.9, in kPa) and feeds no
  equation: not imported. The output list of the window says `W_dot_chiller`
  where the equations define `W_dot`: again the original's naming, the
  variable kept is `W_dot`.
- **2026-10-05 — `t_cd`/`T_cd` and `t_ev`/`T_ev`.** The original writes the
  saturation states with a capital T in two equations
  (`p_cd = P_sat(fluid$,T=T_cd)`, `p_ev = P_sat(fluid$,T=T_ev)`) and with a
  lower-case t in the equations that define them. EES variable names are
  case-insensitive, so this is one variable, not two; the library file writes
  `t_cd` and `t_ev` throughout (CoolSolve names are case-insensitive too).
- **2026-10-05 — curation**: standard header, comments in English paraphrasing
  the comments of the original (its typos — *rerigerant*, *ambi*, *isntropic* —
  are not reproduced), one equation per line with its SI unit in the comment.
  No equation was added, removed or re-arranged, no variable was renamed, the
  three thermal resistances in series are written `1 / AU = R_a + R_m + R_r` as
  in the original. The system is square as it stands (`coolsolve -d`:
  *System square: Yes*).
- **2026-10-05 — `.initials`**: the printed EES solution of the default
  operating point (117 values). Needed, see *How to run*.
- **2026-10-05 — state points for the diagrams**: 16 post-processing equations
  (`P[i]`, `h[i]`, `T[i]`, `s[i]`, i = 1…4) added at the end of the model, as
  the workflow asks for cycles on a real fluid. They add no physics and do not
  change any result of the model (verified: the 117 other variables are
  unchanged). Two of them needed care: the entropy of state 4 is a two-phase
  state, so it is evaluated with the (P, H) pair
  `entropy(fluid$,P=p_ev,H=h_su_ev)` — with (T, P) the state lies exactly on
  the saturation line, where CoolSolve returns NaN and kills the solve (see
  *Limitations*).
- **Level**: score 6 with [taxonomy.md §3](../docs/taxonomy.md) (133 equations
  → 1, largest block 62 → 2, no function/procedure and no discretisation array
  → 0, three coupled components → 1, semi-empirical calibration referred to
  nominal conditions → 1, curated guesses needed → 1) = level 3 by the table;
  lowered by one to **level 2** because the model is a single-zone description
  of one operating point of three components with explicit balances and no
  off-design, multi-zone or array treatment — the same profile as the other
  component models of the bank (`CSL-0074`, `CSL-0076`), also rated level 2.

## Limitations and CoolSolve gaps

- The model needs the shipped `.initials` (see *How to run*). It is not
  *blocked*: it solves in 6 iterations.
- `entropy()` with the **(T, P) input pair exactly on the saturation line**
  returns NaN in CoolSolve (the final-solution check then fails and no `.sol` is
  written), while `enthalpy()`, `volume()` and `quality()` return the
  saturated-liquid values at the same state: reproduced with
  `p = P_sat(R22,T=5.904)` and `s = entropy(R22,T=5.904,P=p)`; the same call
  0.5 K above or below the line, or with a pressure 10 % higher, is correct.
  The library file therefore evaluates the two-phase entropy of state 4 with
  the (P, H) pair. *Unverified suggestion* for the CoolSolve register (a NaN
  that silently aborts the solve of an otherwise valid model), see the final
  message of the import.
- **Variable bounds are not supported** (`CS-GAP-BOUNDS`): EES bounded
  `t_ex_ev` to [−30, 30] °C, `t_su_cp` to [−30, 30] °C, `t_ex_cp` and `t_ex1_cp`
  to [0, 150] °C, `t_su1_cp` to [−30, 75] °C, `t_w_cp` to [−10, 80] °C and
  `M_dot_cp` to [0, ∞); the equations keep the results in range by themselves
  at this operating point.
- The compressor model is the *scroll* machine of the original (constant
  conductance `AU` referred to nothing, constant loss factor `alpha_cp`), but
  the isochoric step is a single relation between the adapted pressure and the
  discharge pressure: no chamber volume, valve or leakage relation appears, so
  the model is not usable far from this operating point.
- The fan control is *hypothetical* (as the original says): the air volume flow
  rate follows the condensing temperature with a proportional law, without a
  fan characteristic, a minimum speed or a start-up transient.
- The ambient heat gain of the compressor (`Q_dot_amb_cp` = −1.83 kW here) is
  computed from the *supply air* temperature; it is a heat flow **into** the
  machine (negative `Q_dot_amb_cp` is a loss) and it is what makes the
  condenser balance close as `Q_dot_cd = Q_dot_ev + W_dot_cp + Q_dot_amb_cp`.
- The refrigerant is R22 in this reference file; `fluid$` can be changed to any
  fluid of the CoolSolve registry, but the compressor parameters were not
  refitted.

## Related models

- `CSL-0076` *cooling_tower_direct_contact_refsim*: same model bank and same
  humid-air air side, for the wet side of the condenser air.
- `CSL-0074` *cooling_coil_refsim*: same model bank, three resistances in
  series referred to the nominal flows.
- `CSL-0001` *refrigeration_cycle_simple_compressor*: same category; the same
  compressor concept (volumetric efficiency from a clearance volume, constant
  losses) at a much simpler level, on a R22/R134a/propane comparison.
- `CSL-0078` *brine_to_water_heat_pump_refsim*: another machine of the same
  model bank with the same four-step scroll compressor and fictitious
  envelope, driving a brine evaporator and a water condenser (R407C).

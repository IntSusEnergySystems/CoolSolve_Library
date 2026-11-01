# Inverter air-to-water heat pump (Daikin Altherma type), heating mode

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (`CS-GAP-USER-STRING-FUNC`; runnable variant verified, adapted from the original) &nbsp;|&nbsp; `CSL-0155`

Detailed steady-state model of an inverter-driven reversible air-to-water heat
pump of the Daikin Altherma type (2007): inverter compressor modelled as an
isentropic compression followed by an isochoric one, condenser and evaporator
with effectiveness/NTU models on the refrigerant, air and water sides, fans with
a flow-pressure characteristic, water pump, and a frost/ice correction of the
outdoor coil. The original EES file selects heating or cooling mode through two
SUBPROGRAMs; this import flattens the heating-mode branch (the mode of the EES
stored run).

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R410A (default), Water, AirH2O |
| **Size** | 343 equations in the main program (largest block: 151); source: 560 equations, 57 FUNCTIONs, 2 SUBPROGRAMs |
| **Source** | ULiège Thermodynamics Laboratory model bank — `~/Nextcloud/thermo_models/modeles/HP_INVERTER_REV_VLD05092007_DAIKIN-ALTHERMA3.EES` (EES 7.793, 2007, inventory candidate `TM-0274`) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory; file initials `VLD`, EES licence of the J. Lebrun lab) |
| **License** | MIT |
| **CoolSolve** | **blocked** by `CS-GAP-USER-STRING-FUNC` (five user FUNCTIONs returning display labels); every numeric block of the native file converges. Runnable variant `inverter_air_water_heat_pump_coolsolve.eescode` (labels written as literals) verified. Adapted from the original on 2026-11-01 (four corrections, see *Review of 2026-11-01*) |

## Problem statement

Catalogue-type simulation of a reversible air-to-water heat pump: given the
outdoor conditions (`t_out`, `RH_out`), the indoor air conditions (`t_in`,
`RH_in`), the water supply conditions (`t_w_su`, `p_w_su`) and the compressor/fan/pump
characteristics, compute the heating (or cooling) capacity, the electrical
consumption of compressor, fans and pump, and all intermediate states
(evaporating/condensing conditions, air exhaust states, condensate and frost
flows). The default operating point shipped here is the EES stored run:
heating mode, `t_out` = −15 °C, `RH_out` = 0.8, water 40 °C (pump speed High,
compressor 3100 rpm).

## Model

- **Compressor** (inverter, R410A): suction/discharge heat transfers, then an
  isentropic compression to an "adapted" pressure `p_r_in_cp` (state at
  `v = v_su/r_v_in_cp`, found from the (s, v) pair) followed by an isochoric
  compression to the discharge pressure; electrical power = internal power +
  losses + heater.
- **Heat exchangers**: effectiveness–NTU with refrigerant-phase-change
  temperatures; the evaporator is solved for a dry and a wet/frost coil, the
  branch selected by comparing the two capacities through the EES five-argument
  `IF(A,B,X,Y,Z)` built-in (X if A<B, Y if A=B, Z if A>B; 14 call sites); frost flow from the wet-coil condensate below 0 °C
  (`IceFactor`).
- **Fans/pump**: polynomial flow–pressure characteristics (`alpha_i`, `beta_i`),
  speed corrections as FUNCTIONs of `t_out` and the operating mode.
- The original is a *child diagram*: all inputs came from its mother diagram.
  They are given here as equations at the values of the EES stored run (or the
  EES guesses when not stored); the three strings are
  `Operating_mode$='Heating_mode'`, `Pump_speed$='High'`, `fluid$='R410A'`.
- The 46 wrapper FUNCTIONs of the original (each calling a SUBPROGRAM and
  returning one output) are absorbed by the flattening: the main program reads
  the outputs directly.

## How to run

```bash
coolsolve ./inverter_air_water_heat_pump_coolsolve.eescode   # runnable variant, 8 iterations
coolsolve ./inverter_air_water_heat_pump.eescode             # native file: stops at the labels (CS-GAP-USER-STRING-FUNC)
```

Both files ship the same `.initials` (the converged solution). The native file converges every numeric block
and then stops at `warning$ = change$(t_out, Operating_mode$)`, a user FUNCTION returning a string; the variant
writes the five labels as the strings these functions return in heating mode at −15 °C (`''`, `'Outdoor Unit'`,
`'Indoor Unit'`, `'Available'`, `'Not available'`). **Hard start:** without the shipped `.initials` the
151-variable block does not converge (see *Review of 2026-11-01* for how the starting point was obtained).

## Results

Default operating point (heating, outdoor −15 °C / RH 0.8, water 40 °C, 3100 rpm), runnable variant:

| Quantity | Value | Quantity | Value |
|---|---:|---|---:|
| heating power `Q_dot_cd` | 8.909 kW | evaporating `t_ev` / `p_ev` | −19.40 °C / 405.3 kPa |
| evaporator duty `Q_dot_ev` | 4.238 kW (dry coil, SHR 100 %) | condensing `t_cd` / `p_cd` | 46.72 °C / 2.847 MPa |
| compressor `W_dot_cp` | 5.017 kW | refrigerant flow `M_dot_r_cp` | 0.02820 kg/s |
| outdoor fan `W_dot_fan_ev` | 92.8 W (4776 m³/h, 25.0 Pa, η 0.357) | water pump `W_dot_pump_cd` | 111.9 W |
| `COP_cp` (heat / compressor) | 1.789 | `COP` (whole unit) | 1.717 |
| discharge `t_r_ex_cp` | 176.9 °C | compressor `epsilon_s_cp` / `epsilon_v_cp` | 0.324 / 0.720 |
| water `t_w_ex_cd` | 41.97 °C (1.090 kg/s) | compressor shell loss | 346 W |

The compressor-only COP (1.79) is below the Carnot value at the refrigerant temperatures (4.84). The low
global isentropic effectiveness (0.32, the value EES stored as well) comes from the compressor parameters of the
file at a pressure ratio of 7 (large constant electromechanical losses), hence the high discharge temperature.

## Verification

The EES file stores the values of its last run (226 of 492 variables). That
stored solution is **partly self-inconsistent**, which limits its use as a
reference and suggests it is a mid-edit state (the file dates from 2007 and its
equations were changed after the run):

- `t_cd_water` = 18.49 °C (dew point at the stored `p_cd` = 13.89 bar, R410A)
  while `t_cd_mean_water` = 46.6 °C and the condenser heats water from 40 °C to
  41.96 °C — thermodynamically impossible;
- the stored R410A enthalpies and entropies are in EES's own reference state (see below), 142 kJ/kg below
  CoolProp's for the enthalpy;
- `SHR_ev` = 95.8 (a sensible heat ratio above 1), `W_dot_fan_cd` = 0 and
  `M_dot_a_cd` = 0 while ≈ 8.9 kW are rejected.

CoolSolve status:
the native file parses, the 14 `IF` call sites evaluate (checked on a small file and in the model), 180 of 181
blocks converge, but **block 106** (151 variables: the dry/wet evaporator selection, the compressor
(heat transfers, isentropic + isochoric stages) and the condenser/water coupling, reached through the
selection variables `Q_dot_ev_dry`/`Q_dot_ev_wet`) does not: from the EES stored values alone Newton stops with
*SingularJacobian* and `TrustRegion` with *MaxIterations* (NaN at the initial point on the R410A and Water
property calls, because 118 of the 151 variables have no stored value); neither the deep-search pipeline
(Newton, TrustRegion, LM, Homotopy, Partitioned, multi-start, tearing and symbolic reduction on) from these
guesses, nor LM with tearing from the improved guesses below, converges.

Tests of better initial guesses (bounded effort, 2026-10-10):

- **The stored EES values cannot be used as they are for R410A enthalpy and entropy.** EES stores them in a
  different reference state from CoolProp's (consistent with h = 0 and s = 0 for the saturated liquid at −40 °C):
  `h_CP − h_EES = 142 244.6 J/kg`, checked on five stored states (saturated liquid and vapour at 0.8 and
  1.4 MPa, superheated vapour), which then agree within 2 %, the rest being the R410A equation of state; the
  same convention gives `s_CP − s_EES = 773.6 J/(kg·K)` (no R410A entropy is stored, so not checked). A stored enthalpy of 79 506 J/kg for the condenser exit, put in `.initials` as it is, is 142 kJ/kg
  away from the CoolProp value.
- The 118 unstored variables (cleared in the file) were completed with a hand-built, CoolProp-consistent cycle
  point (evaporation at 385 kPa / −21 °C, 5 K superheat, suction at −3 °C after the compressor-shell heating,
  (s, v) intermediate state at `r_v_in_cp` = 3, condensation at 2.7 MPa / 44.5 °C, 5 K subcooling, wet-coil contact
  temperature −19 °C). With this point the initial residual drops from 1.3·10⁸ (shipped guesses of the
  first import: mixed reference states, vapour and liquid saturation enthalpies exchanged) to 1.2·10⁶, and
  `TrustRegion` reduces it by 99 % (to ≈ 1·10⁴) before stalling; Newton fails in its line search at iteration 0
  (step norm ≈ 6·10⁵, nearly singular Jacobian); LM ends in *SingularJacobian*. This is the shipped
  `.initials`.
- The EES stored solution is not usable as a converged reference anyway (see the bullets above): the condenser
  pressure it stores (1.389 MPa) is inconsistent with the heated water, so `p_cd` = 2.7 MPa was used.

Remaining problem for the register (convergence of one coupled block, not a language gap): at the stalled
point the largest residuals are the wet-coil cooling power
`Q_dot_ev_wet = M_dot_a_ev*((h_a_su_ev - h_a_ex_ev_wet) - (w_a_su_ev - w_a_ex_ev_wet)*c_w_ev*t_c_ev_wet) - M_dot_ice*H_ice`
(matched to the contact temperature `t_c_ev_wet`) and the three expressions of the dry-coil power
`Q_dot_ev_dry`; the block is driven through the discontinuous selectors `IF(Q_dot_ev_dry, Q_dot_ev_wet, …)` and
`M_dot_ice = IF(t_c_ev_wet, 0.001, M_dot_w_condens_wet, 0, 0)` (zero derivative with respect to their conditions).
A decomposition by hand (cutting the loop at `h_r_ex_cd`, or fixing the evaporating and condensing pressures) was
not tried.

### Review of 2026-11-01

**Classification: blocked** (missing CoolSolve feature), after four corrections of the original that make the
model thermodynamically consistent and give it a single physical solution. Every finding below was checked on the
solution of the variant.

Corrections of the original (marked `ADAPTED` in the file, the original lines kept as comments):

1. **Frost latent heat, sign (first law).** The wet-coil balance wrote `… − M_dot_ice·H_ice`; freezing the
   condensate releases its latent heat, which the refrigerant must remove: `+ M_dot_ice·H_ice`. (Inactive at
   this point: the coil is dry.)
2. **Crankcase heater (first law).** `W_dot_cp = W_dot_in_cp + W_dot_loss_cp + W_dot_heater` counted the 30 W
   heater, but its heat appeared in no balance; it now enters the compressor wall balance. With it the
   compressor balance `W_dot_cp + Q_dot_out_cp = M_dot_r_cp·(h_ex − h_su)` closes to 7·10⁻¹⁰ W and the cycle
   balance `Q_dot_ev + W_dot_cp + Q_dot_out_cp = Q_dot_cd` to 8·10⁻¹⁰ W.
3. **Condenser driving temperature (no physical root).** The lumped effectiveness model was driven by
   `t_cd_mean_water`, an average that weights the whole superheat zone at the compressor **discharge**
   temperature (177 °C here; `t_cd_mean_water` = 108 °C for a 46.7 °C condensation). A continuation on the
   condensing pressure (pressures imposed, see below) shows that this balance has **no root with condensation
   above the water temperature**: at 2.2 MPa (36 °C, below the 42 °C water outlet) the water side would still
   absorb 51 kW more than the refrigerant gives. This, not the solver, is why every earlier attempt stalled at a
   residual of about 1·10⁴. The mean condensing temperature `t_cd_water` is now used, as in the other models of
   the same bank (`CSL-0078`); the root is then at 46.7 °C, above the water outlet (42.0 °C), as it must be.
4. **Fan characteristic outside its fit (two solutions).** The cubic `phi(psi)` falls to about 0 at
   `psi` = 0.33 (shut-off) and rises again beyond it; together with the coil curve `phi ≈ 0.78·sqrt(psi)` it gave a
   second, non-physical operating point (`psi` = 0.58, fan efficiency 0.99, 14 450 m³/h, 926 W) next to the
   physical one (`psi` = 0.064, efficiency 0.357). The characteristic is now evaluated on its decreasing branch
   (`psi` ≤ 0.30); the solution is unique and matches the EES stored fan point (below).

Other checks of the equations (no change needed): the compressor (supply heating, isentropic + isochoric
compression through the `(s, v)` state, exhaust cooling, fictitious wall, no leakage, so `M·w_in` is the internal
power), the effectiveness models of both exchangers, the Braun-type wet-coil contact model, the dry/wet
selection (larger capacity; here the contact temperature −16 °C is above the frost point of the −15 °C air, so the
dry regime is selected and the wet branch, whose condensation comes out negative, is inactive), the connections
(isenthalpic expansion, superheat and subcooling imposed, saturation states consistent), and the second law
(`COP_cp` 1.79 < Carnot 4.84).

**Verification against the EES stored solution** (226 of 492 values; its condenser part is self-inconsistent, see
*Verification* above): the air side agrees — air flow 4776 vs 4778 m³/h, fan power 92.8 vs 92.9 W, compressor
`epsilon_s_cp` 0.324 vs 0.3245 — while the compressor power (5017 vs 3311 W), the evaporator duty
(4238 vs 5843 W) and the COP (1.72 vs 2.68) differ because EES stored a condensing pressure of 1.39 MPa (dew point
18.5 °C) that cannot heat water to 42 °C; with it the refrigerating effect is larger and the pressure ratio lower.

**How the solution was found** (for a re-check): the model was decomposed by imposing the condensing pressure
(in place of the condenser balance) and the evaporating pressure (in place of the wet-coil effectiveness
relation); that problem converges (Try Harder); a continuation on the condensing pressure located the root of
the condenser balance (item 3); releasing both relations from there, the full variant converges in 18 Newton
iterations, and in 8 from the shipped `.initials`.

**CoolSolve findings**: `CS-GAP-USER-STRING-FUNC` (new register row; it was hidden behind the convergence
failure); the AD bug `CS-BUG-PROC-NEG-POW` (fixed on branch `fix/ad-pow-negative-base`) made the earlier Try Harder
runs worse (residual 369 → 0.37 with the fix). Hints: a regime selector or a fitted characteristic used outside
its range easily creates spurious roots — a CoolSolve warning when an IF-selected or polynomial branch changes
during the iterations would help diagnose them.

## Source and attribution

ULiège Thermodynamics Laboratory model bank (collection of S. Quoilin), file
`~/Nextcloud/thermo_models/modeles/HP_INVERTER_REV_VLD05092007_DAIKIN-ALTHERMA3.EES`
(EES 7.793, stored as RTF, licence tag of the J. Lebrun laboratory). Author
initials in the file name: `VLD` (05092007 = 2007-09-05); no author name inside
the file, hence `TBD`. No student or personal data in the file.

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`): RTF converted to text,
  licence tag removed, unit system already SI-°C-Pa-J (no conversion). 492
  variables, 226 with stored values, no lookup/parametric tables.
- **2026-10-08 — SUBPROGRAM flattening (decision D10).** The two SUBPROGRAMs
  `CoolingMode` and `HeatingMode` share all 46 output names and are selected at
  run time by the mode; only one branch can exist in a flattened main program.
  The **heating** branch (the one of the EES stored run: `t_out` = −15 °C,
  water 40 °C, frost active) is flattened: the 46 wrapper FUNCTIONs are
  absorbed (each returned one output of the same single subprogram call), the
  body equations are copied unchanged. The cooling branch stays in the source
  file only. `language_features`: `SUBPROGRAM flattened`.
- **2026-10-08 — string variable rename (CoolSolve-forced).** CoolSolve only
  recognises string variables ending in `$` (`Operating_mode` →
  `Operating_mode$`, 29 occurrences, inputs/functions/calls); `$` names are
  valid EES. `Pump_speed$` and `fluid$` already carried `$`.
- **2026-10-08 — `Enthalpy_Fusion` stand-in.** The EES built-in property
  function is not in CoolSolve (gap `CS-GAP-ENTHALPY-FUSION`); a FUNCTION of
  the same name returning 333 605.9169 J/kg (the value EES stored for Water)
  is added before the body; the call site is unchanged.
- **2026-10-08 — inputs from the mother diagram.** The 56 formal inputs of the
  subprogram are defined at the top with the stored (or guessed) values; the
  three strings deduced from the stored run: `Operating_mode$='Heating_mode'`
  (frost active, water heated to 42 °C, outdoor fan on the evaporator),
  `Pump_speed$='High'` (`N_pump` = 1300 rpm/60 × 1 = stored 21.667 Hz),
  `fluid$='R410A'` (the Daikin Altherma refrigerant; stored saturation points
  agree within 0.7 %, R32 within 1.9 %; `R410A`/`R407C` named in the file).


## Limitations and CoolSolve gaps

- **Blocked** by `CS-GAP-USER-STRING-FUNC` (user FUNCTIONs returning a string, five display labels); the
  runnable variant writes their heating-mode values as literals.
- **Adapted from the original** (2026-11-01): frost latent-heat sign, crankcase-heater heat in the wall balance,
  condenser effectiveness driven by the mean condensing temperature, fan characteristic limited to its fitted
  branch — see *Review of 2026-11-01*.
- **Hard start**: the 151-variable block needs the shipped `.initials` (obtained by decomposition and
  continuation, see *Review*).
- `CS-GAP-ENTHALPY-FUSION`: `Enthalpy_Fusion` missing —
  worked around by a stand-in FUNCTION.
- The heating-mode branch only; the cooling branch of the original (identical
  structure, other parameters) was not imported.
- The EES stored solution is partly inconsistent (see *Verification*): the variant is verified on balances,
  the second law and the consistent subset of the stored values (air side, fan, compressor effectiveness).

## Related models

- `CSL-0078` *brine_to_water_heat_pump_refsim*: similar complete heat-pump
  system model (refsim structure) on a brine-to-water unit.
- `CSL-0116` *heat_pump_vitocal_300g*: another heat-pump system model of the
  model bank, with catalogue-map compressor.

# Inverter air-to-water heat pump (Daikin Altherma type), heating mode

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ❌ **Failing** &nbsp;|&nbsp; `CSL-0155`

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
| **CoolSolve** | 0.3.0+fix/library-gaps-2@59b2862 — **failing**: the native file now parses and evaluates every five-argument `IF` (`CS-GAP-IF5` closed), but the 151-variable block 106 does not converge (register §8, C-147; see *Verification*) |

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
  `IF(A,B,X,Y,Z)` built-in (X if A<B, Y if A=B, Z if A>B; 14 call sites, gap
  `CS-GAP-IF5`, closed in CoolSolve `fix/library-gaps-2`); frost flow from the wet-coil condensate below 0 °C
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

The native file needs a CoolSolve with `CS-GAP-IF5` fixed (branch `fix/library-gaps-2`) and
**does not converge yet**:

```bash
coolsolve ./inverter_air_water_heat_pump.eescode
# Block 106 (size 151) failed to converge: MaxIterations (residual ≈ 1e4)
```

The `.initials` file is the best starting point found (see *Verification*: stored EES values with the R410A
enthalpies and entropies moved to CoolProp's reference state, completed by consistent guesses for the 118
unstored variables); `coolsolve.conf` raises the iteration limit and adds `TrustRegion` for the large selection
block. Even so, Newton fails at the first iteration and `TrustRegion` stalls (see below), so no `.sol` is
committed.

## Results

No converged CoolSolve run yet; see *Verification* for the EES reference values
of the default operating point (heating, −15 °C): Q̇_ev = 5843 W, Ẇ = 3522 W,
t_ev = −20.86 °C, Ṁ_r = 0.0293 kg/s (but the condenser part of the stored
solution is inconsistent, see below).

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

CoolSolve status (`fix/library-gaps-2` @59b2862, 2026-10-10, re-check after `CS-GAP-IF5` was closed):
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
- **2026-10-08 — variant (removed 2026-10-10).** `inverter_air_water_heat_pump_coolsolve.eescode` differed
  from the native file only by the 14 five-argument `IF` rewrites into nested three-argument CoolSolve `IF`
  with comparison conditions (`IF(A<B, X, IF(A=B, Y, Z))`).
- **2026-10-10 — re-check with CoolSolve `fix/library-gaps-2` @59b2862 (T-RECHECK, `CS-GAP-IF5`
  closed).** The native file parses and evaluates every `IF`; block 106 still does not converge, so the
  model is now *failing* (workflow §3: a convergence failure without a registered gap; it was *blocked* by
  `CS-GAP-IF5` alone, `missing_features` is now empty). The variant was removed: it never solved (no `.sol`) and its `IF(A=B, …)` rewrite fails
  by itself in a coupled block with *"Unknown fluid"*, because CoolSolve reads the equality inside the
  call as a named argument (this was the cause of the *"Unknown fluid ''"* error recorded in the register
  entry C-147 of 2026-10-08, not a string-variable propagation problem). `.initials` replaced by the
  reference-state-consistent starting point described in *Verification*. The earlier statement that
  `p_ev = IF(Q_dot_ev_dry, Q_dot_ev_wet, …)` "returns a power as a pressure" came from a wrong reading of
  the argument order (`IF(A,B,X,Y,Z)`: the third and fourth arguments are the values, here `p_ev_wet` and
  `p_ev_dry`) and was removed.

## Limitations and CoolSolve gaps

- `CS-GAP-IF5` — **closed** in CoolSolve `fix/library-gaps-2` (commit 59b2862); CoolSolve v0.3.0 stops on
  the first five-argument `IF`.
- **Block 106 does not converge** (151 variables, register §8, C-147): the model is *failing*, no `.sol`.
  See *Verification* for the tests of initial guesses and the stored-solution reference-state offset of the
  R410A enthalpies and entropies.
- `CS-GAP-ENTHALPY-FUSION` (registered here): `Enthalpy_Fusion` missing —
  worked around by a stand-in FUNCTION.
- The heating-mode branch only; the cooling branch of the original (identical
  structure, other parameters) was not imported.
- The EES stored solution is partly inconsistent (see *Verification*), so even
  a converged CoolSolve run could only be verified on the consistent subset
  (evaporator/compressor side).

## Related models

- `CSL-0078` *brine_to_water_heat_pump_refsim*: similar complete heat-pump
  system model (refsim structure) on a brine-to-water unit.
- `CSL-0116` *heat_pump_vitocal_300g*: another heat-pump system model of the
  model bank, with catalogue-map compressor.

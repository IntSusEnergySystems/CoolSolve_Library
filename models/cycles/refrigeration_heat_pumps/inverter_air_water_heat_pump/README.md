# Inverter air-to-water heat pump (Daikin Altherma type), heating mode

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0155`

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
| **CoolSolve** | v0.3.0 — blocked by `CS-GAP-IF5`; `_coolsolve` variant does not converge yet (see *Verification*) |

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
  `CS-GAP-IF5`); frost flow from the wet-coil condensate below 0 °C
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

The native file does not run in CoolSolve (gap `CS-GAP-IF5`, already
registered):

```bash
coolsolve ./inverter_air_water_heat_pump.eescode
# error: Unknown or unsupported function: IF with 5 arguments
```

`inverter_air_water_heat_pump_coolsolve.eescode` is the variant in which the 14
five-argument `IF` calls are rewritten with the CoolSolve-only three-argument
`IF` as `IF(A<B, X, IF(A=B, Y, Z))` (the registered EES semantics; every change
logged below); it parses and reaches the last solver block but does not converge
yet (no `.sol` committed). Both files need the guesses of their `.initials`;
`coolsolve.conf` raises the iteration limit for the large selection block.

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
- with the EES `IF(A,X,Y,B,Z)` semantics, `p_ev = IF(Q_dot_ev_dry, Q_dot_ev_wet, …)`
  would return a power (≈ 5.8 kW) as a pressure whenever the dry-coil capacity
  is positive; the stored `p_ev` = 385 267 Pa corresponds to the wet/dry branch
  values instead;
- `SHR_ev` = 95.8 (a sensible heat ratio above 1), `W_dot_fan_cd` = 0 and
  `M_dot_a_cd` = 0 while ≈ 8.9 kW are rejected.

CoolSolve status: the native file is **blocked** by `CS-GAP-IF5` (the
five-argument `IF` built-in, 14 call sites; registered, `CSL-0009`). The
`_coolsolve` variant rewrites only those calls and reaches the last solver
block (181 blocks; 180 converge); block 106 (151 variables: the wet/dry
evaporator selection plus the compressor and evaporator branches) fails with
`EvaluationError - Unknown fluid: ''` from the (x, P) two-phase property calls
inside the block (with a fallback to `MaxIterations`, residual ≈ 4·10⁵, when
the branches select otherwise). The 118 variables of that block have no stored
values (cleared in the file) and were given physical guesses (documented in
`inverter_air_water_heat_pump_coolsolve.initials`, condenser cluster set to a
consistent ≈ 2.65 MPa / 43.8 °C point). Diagnosis: discontinuous branch
selectors plus two-phase R410A (zeotrope) property calls in the 151-variable
coupled block; not resolved within this task.

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
- **2026-10-08 — variant.** `inverter_air_water_heat_pump_coolsolve.eescode`
  differs from the native file only by the 14 five-argument `IF` rewrites
  `IF(A,X,Y,B,Z)` → `IF(A>0, X, IF(A<0, Y, B))` (EES semantics; the fifth
  argument only covers NaN and is unreachable for real arguments). CoolSolve
  3-argument IF is CoolSolve-only syntax, not valid EES.

## Limitations and CoolSolve gaps

- `CS-GAP-IF5` (registered, `CSL-0009`): the five-argument `IF` built-in is
  not supported — blocks the native file.
- `CS-GAP-ENTHALPY-FUSION` (registered here): `Enthalpy_Fusion` missing —
  worked around in both files by a stand-in FUNCTION.
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

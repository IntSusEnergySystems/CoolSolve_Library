# Complete gas engine: throttle, carburettor, combustion, cooling and recovery circuits

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (runnable variant verified) &nbsp;|&nbsp; `CSL-0149`

Steady-state model of the 5 L four-stroke natural-gas engine of the ULiège
*machines et systèmes thermiques* course (repetition TP 08, exercises 1–5) at
its **maximum-power operating point**: 2400 rpm, shaft power (≈ 90 kW) solved
from the imposed indicated efficiency. The model chains the butterfly valve
(throttle), the carburettor, the intake pressure drop through the valve area,
an adiabatic combustion chamber whose products are described by the `cpbar`
mean specific heat of the ULiège combustion library, the expansion, the
cooling-water circuit (jacket + water-to-environment exchanger) and, for
exercise 5, two recovery heat exchangers (water–water and water–gas). The
stand-by throttling pressure drop of exercise 1 is read in an engine map
(external lookup table, recovered from the sibling file of the same exercise
series). **CSL-0034** is the stand-by (zero-power) point of the same engine
family.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air, CH4 (ideal-gas fuel), Water |
| **Size** | 105 equations (largest block: 10) — about 50 of them are the copied `cpbar` routine |
| **Source** | ULiège MSTh repetition TP 08, exercises 1–5, S. Bertagnolio (`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 08/SB/MSTH-SB-R8-EX1-2-3-4-5.EES`, EES X7.458) |
| **Authors** | ULiège MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7addbbc — native file blocked by `CS-GAP-INTERP-EES`; the runnable variant `gas_engine_complete_model_coolsolve.eescode` is verified against the stored EES solution (97 common variables, all deviations explained) |

## Problem statement

*As in the original (comments translated).*

Exercise 1 (stand-by): the throttling pressure drop is read in an engine map
`DELTAP_throttling(W_dot_sh)` at `W_dot_sh = 0`. Exercises 2–4
(maximum power): the engine runs at 2400 rpm with a fuel–air ratio of 0.055;
the throttle is wide open (`DELTAP_throttling = 0`); the indicated efficiency
is 0.3282 and the friction torque 39.79 N·m. Exercise 5 adds two recovery
exchangers: the jacket water preheats a recovery water stream, which is then
brought to 80 °C by the exhaust gases. Determine the operating point: air and
fuel flow rates, flame and exhaust temperatures, cooling-water temperatures,
shaft power and the recovered powers.

## Model

All the equations of the original are kept; nothing was added or removed.

* **States 1–4 (throttle, carburettor, pressure drop).** `P_2 = P_1 −
  DELTAP_throttling`, `T_2 = T_1` (carburettor), `M_dot_p = M_dot_a + M_dot_f`
  with `M_dot_f = f·M_dot_a = M_dot_f_kgh/3600` (two definitions, both kept as
  in the original). The charge then accelerates through the valves: the
  kinetic-energy balance `c_p_23·(T_2 − T_3) = C_3²/2` on the isentropic path
  `s_2`, with `V_dot_3 = A_soupapes·C_3`, closes the intake pressure `P_3`
  (98 633 Pa, i.e. a 2.7 kPa drop) and `C_3` = 67.2 m/s.
* **Cylinder and combustion.** `V_dot_4 = V_dot_s = i·N·ncV_s` fixes the
  charge flow `M_dot_p = V_dot_4/v_4`. The adiabatic chamber balances the
  reactants (air and methane brought to the 25 °C reference) and the products,
  `Q_dot_1 + … + Q_dot_5 = 0`, with the mean specific heat of the products
  between 25 °C and the flame temperature `t_6` from `cpbar(m_f, n_f, f, 25,
  t_6)`.
* **Expansion and power terms.** `W_dot_sh = M_dot_p·cp_p_67·(T_6 − T_7)`,
  `W_dot_in = W_dot_sh + W_dot_m + W_dot_pumping`, and the imposed indicated
  efficiency `eta_in_actif = W_dot_in/(M_dot_f·LHV_f)` closes the system on
  `W_dot_sh` (≈ 90 kW) and `T_7`. The pumping-power correlation of exercise 3
  (`W_dot_pumping_bis`) is kept as the unused alternative of the original.
* **Cooling and recovery.** The products cross the jacket (ε-NTU, `AU_gw`,
  cross-flow formula of the original; `cp_p_78` and `cp_w_gw` keep their
  provisional constant values of the original), the water rejects
  `Q_dot_wenv` to the environment (ε-NTU, `AU_wenv`), then gives `Q_dot_recup_1`
  to the recovery water (ε = 0.75) and the gases bring it to
  `T_w_recup_ex_2 = 80 °C` in the second recovery exchanger.

| Inputs | Value | Outputs (CoolSolve) | Value |
|---|---|---|---|
| `rpm`, `i`, `ncV_s` | 2400 rpm, 0.5, 5·10⁻³ m³ | `M_dot_a` air flow | 0.11115 kg/s |
| `f` | 0.055 | `M_dot_f` fuel flow | 6.113·10⁻³ kg/s |
| `eta_in_actif`, `T_m` | 0.3282, 39.79 N·m | `W_dot_sh` shaft power | 90 051 W |
| `A_soupapes` | 1.477·10⁻³ m² | `t_6` flame temperature | 1961.5 °C |
| `T_1`, `P_1` | 20 °C, 101 325 Pa | `t_7` exhaust temperature | 1440.6 °C |
| `AU_gw`, `AU_wenv` | 83.8, 127.4 W/K | `t_8` products after the jacket | 860.8 °C |
| `M_dot_w`, `T_w_su` | 0.9 kg/s, 60 °C | `Q_dot_gw`, `Q_dot_wenv` | 88 379, 7 949 W |
| `M_dot_w_recup` | 3.16 kg/s | `Q_dot_recup` total recovered | 119 365 W |
| `LHV_f` | 50·10⁶ J/kg | `eta_sh` shaft efficiency | 0.2946 |

The stand-by throttle value of exercise 1, `DELTAP_throttling_stb =
INTERPOLATE(..., W_dot_sh=0)`, comes out at 83 275.3 Pa (83 275.40418 in EES,
which interpolates cubically; CoolSolve interpolates linearly — the
1.4·10⁻⁶ relative difference is within tolerance).

## How to run

The **native file** is blocked: CoolSolve parses the native EES `INTERPOLATE`
call form as a property call (*"Unknown fluid: 'lookup_1'"*, gap
`CS-GAP-INTERP-EES`). It is kept in valid EES syntax.

The **runnable variant** solves as is (note the `./`):

```bash
coolsolve ./gas_engine_complete_model_coolsolve.eescode
```

It needs the companion files `gas_engine_complete_model_coolsolve.initials`
(guess values from the EES stored solution; the flame temperature sits inside
the `cpbar` calls), `gas_engine_complete_model_coolsolve-lookup_1.csv` (the
engine map) and, for the native file, `gas_engine_complete_model-lookup_1.csv`.

## Results

At 2400 rpm the engine burns 0.111 kg/s of air and 6.1 g/s of methane, produces
90 kW of shaft power at a shaft efficiency of 0.295, and rejects 88.4 kW to the
jacket water (60 → 83.5 °C); 7.9 kW of it are lost to the environment and 29.4 kW
are recovered in the water–water exchanger, before the exhaust gases bring the
recovery water to 80 °C (90.1 kW, total recovered 119.4 kW — of the same order
as the shaft power). The flame temperature (1961 °C) is the zero-power point
value of **CSL-0034** (same fuel–air ratio): the charge enters the cylinder at
ambient temperature in both exercises.

## Verification

Reference: the stored solution of the EES original (`reference/ees_variables.csv`
produced by `tools/ees_extract.py` in the temporary work folder, not shipped;
98 variables, of which 97 have a value — `m` is a phantom variable of the
original, not present in any equation). The comparison concerns the **runnable
variant**:

```
97 common variables, 6 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 9
```

The 9 CoolSolve-only variables are the constant `PI` and the eight unused
outputs of the two `CALL cpbar` transcriptions (`Q_4_a`, `x_a`, `e_min_a`,
`e_a`, `Q_4_67`, `x_67`, `e_min_67`, `e_67`), as in CSL-0034.

The six deviations above rtol = 0.001, all explained:

| Variable | EES | CoolSolve | rel. diff | Cause |
|---|---:|---:|---:|---|
| `cp_f` | 2241.7 | 2220.6 | 9.4·10⁻³ | `CP(CH4)`: EES ideal-gas vs CoolProp real-fluid heat capacity (same deviation as CSL-0034) |
| `Q_dot_2` | 68.50 | 67.88 | 9.0·10⁻³ | follows `cp_f` (0.6 W term of the chamber balance) |
| `s_2` | 5678.3 | 3863.5 | 0.32 | absolute air entropy: CoolProp reference-state offset; every entropy-*difference* result agrees (`t_3` 5.8·10⁻⁵, `C_3` 2.5·10⁻⁵) |
| `cp_p_67` | 1471.9 | 1474.3 | 1.6·10⁻³ | mean cp of the products between `t_6` and `t_7`: EES vs CoolSolve ideal-gas enthalpies of the species (`t_6` itself at 8.4·10⁻⁴, the same deviation as CSL-0034) |
| `Q_dot_recup_1` | 29 350 | 29 312 | 1.3·10⁻³ | difference of two close temperatures (2.22 K) computed from water properties; the temperatures themselves agree to ≤ 1.3·10⁻⁴ |
| `W_dot_pumping` | 269.2 | 268.5 | 2.6·10⁻³ | difference of two close pressures (`P_1 − P_4` ≈ 2.7 kPa out of 1 bar); `P_4` agrees to 7.0·10⁻⁵ |

All the other results agree within 1·10⁻³ relative: `W_dot_sh` 4.2·10⁻⁴,
`M_dot_a`/`M_dot_f` 3.7·10⁻⁴, `t_7` 5.8·10⁻⁴, `t_8` 3.7·10⁻⁴, `Q_dot_gw`
5.1·10⁻⁴, `Q_dot_recup` 3.5·10⁻⁴, `DELTAP_throttling_stb` 1.4·10⁻⁶ (linear vs
cubic interpolation). Sanity checks: the charge mass balance and the chamber
energy balance are closed, `eta_in_actif` is imposed and recovered, the jacket
effectiveness (0.420) and `C_dot_p_78 < C_dot_w_gw` are consistent with the
small `AU_gw`, and the recovered powers add up (`Q_dot_recup_1 + Q_dot_recup_2
= Q_dot_recup`).

The descending order of the map's `W_dot_sh` column (as in the original data)
is handled correctly by this build (the `CS-BUG-INTERP-DESC` fix).

## Source and attribution

* **Original model (EES, X7.458)**:
  `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 08/SB/MSTH-SB-R8-EX1-2-3-4-5.EES`
  (candidate **TM-0136**), MSTh repetition TP 08, exercises 1–5 by
  S. Bertagnolio; ULiège MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio).
  The `{$ID$}` tag names the Laboratoire de Thermodynamique (Université de
  Liège) as the EES licence holder. The file names no author; the `SB` folder
  name and the inventory identify S. Bertagnolio.
* **Engine map (`Lookup 1`)**: external table, not present in the collection;
  its content was recovered from the sibling file of the same series
  `MSTh-SB-R8-Ex1-2-3-4.EES` (candidate **TM-0137**, parametric `Table 3`,
  120×2, columns `W_dot_sh` / `DELTAP_throttling`): its 50 valid rows span
  `W_dot_sh` = 18 189 … −3 886 W for `DELTAP_throttling` = 5 000 … 100 000 Pa,
  and the linear interpolation at `W_dot_sh = 0` gives 83 275.29 Pa against
  83 275.40418 Pa in the stored solution (EES interpolates cubically) — the
  table is confirmed.
* **`cpbar`**: `P. Ngendakumana`, *CombCmHn_SI_PNG2003_V2.LIB* (ULiège
  Thermodynamics Laboratory, 2003), shipped as **CSL-0005** and copied into
  this model as in CSL-0034/CSL-0006 (`CS-FEAT-IMPORT`, `$INCLUDE library:…`,
  is not available yet).
* All sources are published under the library license (MIT).

## Conversion log

* **2026-10-08 — import** (`tools/ees_extract.py`, EES X7.458): the unit
  system of the original is already `SI MASS DEG PA C J`, i.e. the CoolSolve
  unit system: **no unit conversion was needed**. 98 variables, no embedded
  table; the report flags `Lookup 1` as an external lookup file and `cpbar` as
  an external routine that the file does not define; the EES licence tag was
  removed.
* **2026-10-08 — lookup table**: the external `Lookup 1` is not in the
  collection; recovered from TM-0137's parametric `Table 3` (see *Source and
  attribution*) and shipped as the companion tables
  `gas_engine_complete_model-lookup_1.csv` (native) and
  `gas_engine_complete_model_coolsolve-lookup_1.csv` (variant), identical,
  original row order kept. The table name was renamed `'Lookup 1'` →
  `'lookup_1'` in the equations (CoolSolve companion-table convention, as the
  extractor does for embedded tables).
* **2026-10-08 — `cpbar`**: the file does not define the routine (implicit
  ULiège user library, gap `CS-GAP-INCLUDE`); the five-output `PROCEDURE` of
  CSL-0005 is copied verbatim. The **native file** keeps the two active calls
  in *function position*, exactly as in the original (`cp_p = cpbar(m_f,n_f,f,
  T_ref,T_6)`, `cp_p_67 = cpbar(m_f,n_f,f,T_6,T_7)`); the **variant**
  transcribes them to the valid-EES `CALL` form
  (`CALL cpbar(m_f,n_f,f,T_ref,T_6:cp_p,Q_4_a,x_a,e_min_a,e_a)`, only `cp_p`/
  `cp_p_67` used; the other outputs named `…_a`/`…_67` to avoid clashes, as in
  CSL-0034/CSL-0006) because CoolSolve refuses the function form with a
  five-output procedure (see *Limitations*). The third call site of the
  original (`cp_p_78 = cpbar(m_f,n_f,f,T_7,T_8)`) is an *inactive comment*
  there; it is kept as a comment and `cp_p_78 = 1300` keeps its provisional
  value, exactly as in the original.
* **2026-10-08 — curation**: French comments translated to English with SI
  units; section titles as display strings; the inactive operating-point
  strings of the original (`rpm=500`, `W_dot_sh=90E3`, `M_dot_f_kgh=22`,
  `Q_dot_gw=90000`, `W_dot_m=10E3`, `Q_dot_wenv=8E3`, `T_1=0`,
  `DELTAP_throttling=DELTAP_throttling_stb`, provisional values `s_2=6000`,
  `cp_p=1300`, `cp_p_67=1300`, `cp_w_gw=4187` vs `CP(Water,…)` — both forms
  kept where the original keeps them) are quoted in the comments. No equation
  was added, removed or modified.
* **2026-10-08 — blocked status**: the native file fails on the native
  `INTERPOLATE('lookup_1','DELTAP_throttling','W_dot_sh',W_dot_sh=0)` call
  form — *"Unknown fluid: 'lookup_1'"* — registered gap `CS-GAP-INTERP-EES`
  (no new gap to report; the implicit `cpbar` user library is
  `CS-GAP-INCLUDE`). It also cannot run for a second reason, the function-
  position `cpbar` calls with the five-output procedure (see *Limitations*).
  Runnable variant changes (logged in its header): 1. the same call in
  CoolSolve's positional form `INTERPOLATE('lookup_1','W_dot_sh',
  'DELTAP_throttling',0)` (CoolSolve-only syntax, column roles reversed
  w.r.t. EES); 2. the two `cpbar` calls in the valid-EES `CALL` form.
  Everything else, including all variable names, is unchanged.
* **2026-10-08 — review (C-141)**: the file headers shortened to the library
  rule (~10–20 lines, details moved to this README); the native file restored
  to the source's function-position `cpbar` calls (see *Limitations*), the
  `CALL` transcription moved to the variant. Re-solved: the variant gives the
  same solution (`97 common variables, 6 differ (rtol=0.001)` as before).
* **2026-10-08 — numerics**: `.initials` = the guess column of the EES stored
  solution (the flame temperature sits inside the `cpbar` calls); no
  `coolsolve.conf` needed (the expansion is not degenerate here, unlike
  CSL-0034: `W_dot_sh ≈ 90 kW ≠ 0`).
* **Level 2** (card): the taxonomy score is 6 (105 equations, largest block
  10, procedures, ≥ 3 coupled components, engine-map off-design data, curated
  guesses → level 3), lowered by one as for CSL-0034: about 50 of the 105
  equations are the copied `cpbar` routine and the exercise itself is a
  single operating point of explicit, mostly sequential bookkeeping balances.

## Limitations

* The original treats the jacket, the environment exchanger and the recovery
  exchangers as given component data; the water circuit is not closed on
  itself (the water is supplied at 60 °C and leaves the recovery section at
  73.6 °C), as in the original.
* `cp_p_78` and `cp_w_gw` keep the provisional constant values of the original
  (1300 and 4187 J/kg-K); the `cpbar`/`CP(Water,…)` alternatives are inactive
  comments there.
* The engine is not a cycle model on a real fluid: no thermodynamic diagram
  can be overlaid (`CS-FEAT-DIAGRAM-IDEAL`, all fluids are ideal gases in
  EES); a sweep plot (e.g. `W_dot_sh` vs `rpm`) is the expected figure.
* **Function-position `cpbar` calls with a multi-output `PROCEDURE`.** The
  native file calls `cpbar(...)` in function position, exactly as in the EES
  original (valid EES syntax); the library routine (CSL-0005) is a five-output
  `PROCEDURE`, and CoolSolve refuses the function form with it (*"Procedure
  cpbar has 5 outputs and cannot be called as a function (inline syntax
  requires exactly 1 output)"*; minimal reproducer: a two-line call of the
  CSL-0005 procedure in function position). Whether EES accepts the function
  form with a multi-output procedure is an open question (unverified
  suggestion `CS-GAP-PROC-MULTIOUT` in the maintainer's pending list, not
  registered — the 2005 exercise may have used a one-output `cpbar`): it is
  therefore **not** listed in `missing_features`; the variant uses the
  valid-EES `CALL` form.

## Related models

* **CSL-0034** *gas_engine_full_power_cpbar*: the stand-by (zero-power)
  operating point of the same engine family (TP 08 exercise 4); this model is
  its maximum-power counterpart with the recovery circuits of exercise 5.
* **CSL-0005** *cpbar_combustion_products*: the `cpbar` routine (function
  library) copied into this model.

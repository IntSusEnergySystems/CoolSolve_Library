# Waste-heat-recovery ORC with a scroll expander, REFPROP mixtures and an equipment cost model

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0153`

A complete organic Rankine cycle recovering heat from an exhaust-gas stream
(through variable names `T_a_su`, `M_dot_a`, the heat source is the
Therminol VP-1 secondary loop of `fluidev$`, as in the original): three-zone
plate evaporator and condenser rated with the Thonon, Kuo and Hsieh plate
correlations, a scroll expander with fixed volume ratio and mechanical
efficiency, a pump, pipe sizing and a full equipment/investment cost model.
All refrigerant properties are taken from the EES REFPROP interface
(`CALL EES_REFPROP`) on the mixture file `C:\REFPROP8\R245fa+R134a`; the
stored run is at composition `MM_fraction = 1`, i.e. pure R245fa
(molar mass stored: 134.048 kg/kmol). A `Summary` procedure writes the key
results of each run into the `optim` lookup table (row 8), used for the
optimisation sweeps of the original study.

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R245fa+R134a (REFPROP mixture file; stored run: pure R245fa), Therminol VP-1, Water, Air |
| **Size** | 361 equations, largest block 24 (runnable variant; EES stored solution: 386 variables) |
| **Source** | ULiège Thermodynamics Laboratory, EES 8.652 (`cycle ORC with refprop.EES`) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory) — the 2011-10-29 copies of the same model are by Sylvain Quoilin |
| **License** | MIT |
| **CoolSolve** | v0.3.0, re-checked with 0.3.0@57b22d3 — native **blocked** (`CS-GAP-REFPROP`, `CS-GAP-END-PROCEDURE`; `CS-GAP-IF5` and `CS-GAP-CALL-EXPR-OUT` are closed in CoolSolve `fix/library-gaps-2` @59b2862 and @57b22d3); runnable variant verified against the EES stored solution |

## Problem statement

Size and cost a small waste-heat-recovery ORC: an exhaust-gas/thermal-oil
stream (0.3 kg/s at 180 °C) is cooled in a plate evaporator boiling R245fa at
26.18 bar; a scroll expander (built-in volume ratio 3.4, mechanical efficiency
0.7) expands the vapour to the condenser pressure; water at 15 °C (0.5 kg/s)
condenses it; a pump closes the cycle (isentropic efficiency 0.6). The model
computes the cycle states zone by zone in both heat exchangers, the expander
power and isentropic efficiency, the pipe diameters from velocity
recommendations, and the total equipment cost (TEC) and specific investment
cost (SIC). The stored operating point carries the result of an earlier
optimisation (`"optimisation 2xb:"` pinch points, plate numbers and
evaporation pressure in the input block).

## Model

- **Evaporator** (procedure `hx_ev`) and **condenser** (`hx_cd`): three
  refrigerant zones each (preheating/boiling/superheating, desuperheating/
  condensing/subcooling) with LMTD-based `AU` per zone, plate correlations for
  the heat-transfer coefficients — Thonon single-phase, Hsieh & Lin flow
  boiling (`Hsieh_new`), Kuo condensation (with a quality integral over
  0.01–0.95) — zone areas, plate lengths, refrigerant charge (void fraction
  approximation) and pressure drops; fluid prices from a `Prix Fluides`
  lookup table (the price function is stubbed to 15 €/kg in the file).
- **Expander**: supply state from the evaporator outlet, built-in volume
  ratio 3.4 (`v_r_in_exp = r_v_in_exp * v_r_su_exp` gives the discharge
  volume, from which the discharge pressure follows), shaft power
  `W_dot_shaft = epsilon_m_exp * W_dot_in` with
  `W_dot_in = M_dot_r*(h_su - h_in) + M_dot_r*v_in*(P_in - P_ex)`;
  isentropic efficiency is an output.
- **Pump** (isentropic efficiency 0.6) and secondary-fluid pump power from
  the evaporator-side pressure drop.
- **Pipes**: velocities imposed (suction 10 m/s, discharge 12 m/s, liquid
  0.6 m/s), diameters computed.
- **Cost**: expander = 1.5 × hermetic-compressor law (170×swept volume + 225
  €), exchangers 190 + 310×area €, pump 900×(W/300)^0.25, pipes and hardware,
  refrigerant charge cost, +30 % labour → TIC, SIC = TIC / net power.

The `Summary` procedure stores 19 key results per run in the `optim` lookup
table (the 22×9 embedded grid of the file is an archived sweep). The
five-argument `IF(DELTAC_dot, 0, …)` selects the condenser water-side
temperatures depending on the sign of the heat-capacity difference (native
EES, see gaps).

## How to run

Open `orc_whr_refprop_cost_coolsolve.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./orc_whr_refprop_cost_coolsolve.eescode
```

The variant is the native file with the REFPROP blocks, the `$common` lines,
the two 5-argument `IF` calls and the `End procedure` terminator rewritten
(every change logged in the conversion log); the guess values of
`orc_whr_refprop_cost_coolsolve.initials` come from the EES stored solution
(66 iterations, no `coolsolve.conf`). The native file
`orc_whr_refprop_cost.eescode` is kept in valid EES and does not run in
CoolSolve (gaps below); in EES it solves as stored (386 variables) and
`optim` row 8 collects the summary of the run.

## Results

EES stored solution vs the CoolSolve variant (default operating point):

| Quantity | EES | CoolSolve | dev. | Quantity | EES | CoolSolve | dev. |
|---|---:|---:|---:|---|---:|---:|---:|
| `M_dot_r` [kg/s] | 0.2235 | 0.2255 | 0.9 % | `A_ev` [m²] | 2.334 | 2.343 | 0.4 % |
| `Q_dot_ev` [kW] | 49.19 | 49.47 | 0.6 % | `A_cd` [m²] | 5.459 | 5.249 | 3.9 % |
| `W_dot_net` [kW] | 3.425 | 3.442 | 0.5 % | `DELTAp_ev` [kPa] | 26.1 | 23.2 | 11 % |
| `eta_cycle` [%] | 6.964 | 6.959 | 0.07 % | `DELTAp_cd` [kPa] | 44.9 | 41.6 | 7.4 % |
| `epsilon_s_exp` [-] | 0.6370 | 0.6363 | 0.1 % | `TEC` [€] | 7 114 | 7 055 | 0.8 % |
| `epsilon_ev` [%] | 52.9 | 53.3 | 0.6 % | `SIC` [€/kW] | 2 700 | 2 664 | 1.3 % |

The deviations on the cycle quantities come from the property backend
(EES REFPROP vs CoolProp, both Helmholtz EOS for R245fa); the heat-exchanger
pressure drops and areas additionally amplify the differences on the
viscosity/conductivity correlations (see *Verification*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/orc_whr_refprop_cost_ph.png)  + one-line caption -->

## Verification

The runnable variant is compared with the EES stored solution of the source
file (`compare_solution.py orc_whr_refprop_cost_coolsolve.sol
ees_variables.csv`):

> 356 common variables, 224 differ (rtol=0.001); only in EES: 30; only in
> CoolSolve: 6

- **Key results within the property tolerance** (§11 of CoolSolve
  `docs/ees_import.md`, different-EOS case): `eta_cycle` 7.1e-4,
  `W_dot_net` 5.0e-3, `Q_dot_ev` 5.7e-3, `M_dot_r` 9.1e-3, `TEC`/`TIC`
  8.4e-3, `SIC` 1.3e-2.
- **Correlation-heavy outputs**: `DELTAp_ev` 1.14e-1, `DELTAp_cd` 7.4e-2,
  `A_cd` 3.9e-2, `M_fluid_cd` 3.8e-2 — the Thonon/Kuo/Hsieh correlations
  amplify the REFPROP vs CoolProp differences on viscosity and thermal
  conductivity of R245fa.
- **Reference-state offset (excluded)**: the absolute air enthalpies
  `h_a_ex_vap` (2.2e-1) and `h_a_ex_liq` (2.5e-1) carry the offset between
  the EES ideal-gas JANAF reference and CoolProp's `Air`; they are pure
  diagnostics (each appears only in its own `Temperature(Air, h=…)` inverse,
  whose temperature agrees).
- **Printed maximum over all common variables**: 2.5e-1 (the pair above).
- **Only in EES (30)**: the 9 REFPROP pseudo-quality outputs `Q_r_*` outside
  0..1 (wrapper diagnostics, not reproduced), plus 21 stale values of an
  older EES session (`A`, `A_tp`, `AU`, `AU_tp`, `C`, `Cp`, `d`, `h`,
  `h_a_ex_tp`, `h_a_su_liq`, `h_a_su_tp`, `h_a_su_vap`, `N_p`, `P`, `Q`,
  `Q_dot_cd`, `rho`, `s`, `v`, `v[5]`, `V_tot`) that belong to no equation of
  the file.
- **Only in CoolSolve (6)**: the five string variables and `pi` (not exported
  to the reference CSV).

Regression: `tools/test_models.py CSL-0153` solves the variant and compares
it with `orc_whr_refprop_cost_coolsolve.sol`.

## Source and attribution

Source file (EES 8.652, comments in French, EES licence of the J. Lebrun
laboratory — ULiège), collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/cycle ORC with refprop.EES`
(inventory candidate `TM-0268`, duplicate group DG-0122 with the byte-equivalent
`optim/R245fa SQ101129 - thermodynamic.EES` and `…thermoeconomic.EES`
copies, TM-0555/TM-0556, by Sylvain Quoilin). No author is named in the file
itself.

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`): unit system already
  `SI MASS DEG PA C J`; decimal comma converted to dot by the tool; licence
  tag `{$ID$ …}` removed; `$UnitSystem` line removed. Comments translated to
  English. No equation changed: the CoolSolve statistics (293 equations,
  331 variables, not square) are identical before and after the edits.
- **Embedded tables**: the file stores four grids all named `Lookup 2`
  (59×2, 22×8, 22×2, 22×9) and one external table `Prix Fluides` (fluid
  prices, referenced only from the commented-out body of `FluidPrice`, stubbed
  to the constant 15). No equation reads `Lookup 2`; the grids are archived
  sweep results. The extractor wrote all four grids to the same companion CSV
  (name clash — only the last, the 22×9 `optim`-layout sweep, survives in
  `orc_whr_refprop_cost-lookup_2.csv`; tool quirk, not reported as a bug since
  no table is used by the equations). The `Summary` procedure *writes* the
  `optim` table as a run side-effect (row 8).
- **Kind**: `steady` (the file never calls Min/Max; the stored input block is
  labelled "optimisation 2xb:", i.e. the operating point typed in from an
  earlier optimisation). `CS-GAP-OPTIM` therefore not listed.
- **Level** (docs/taxonomy.md §3): equations 361 (1) + largest block > 30
  (2, coupled cycle) + procedures/arrays (1) + multi-zone multi-component
  (1) + semi-empirical correlations (1) + curated guesses (1, EES stored
  guesses needed, 66 iterations) = 7 → level 3 (level moved −1 from the
  score: the model is a plain engineering sizing/cost model, as the
  inventory).

- **2026-10-08 — runnable variant `orc_whr_refprop_cost_coolsolve.eescode`**
  (orchestrator review of C-145; every change forced by a gap, pattern of
  `CSL-0124`; verified above):
  1. **`CALL EES_REFPROP` blocks (29 sites: 13 in the main program, 16 in the
     procedures `hx_cd`, `hx_ev`, `Thonon`, `Hsieh_new`, `kuo`) replaced by
     pure-fluid property calls on R245fa** — faithful only at `MM_fraction =
     1` (pure R245fa), the composition of the stored EES run (`MM` =
     134.048 kg/kmol). Each output expression of a call becomes one equation
     defining the same variable: REFPROP molar outputs follow the caller's
     scalings (`T` K, `p` kPa, `rho` kmol/m³, `v` m³/kmol, `h`/`s`
     kJ/kmol → `×MM/1000` gives the stored J/kg values; `cp`/`cv` are
     reproduced in their stored kmol convention `×MM/1000`). The molar
     convention of `h_l`, `h_v` in `Hsieh_new`/`kuo` (their `h_ref` is
     kJ/kmol, so `i_fg` stays in kJ/kmol as in the original) is kept; the
     stored `A_cd`/`A_ev` confirm it. The expander-inlet call, whose
     `(T, P)` inputs are unknowns, is written through its two determined
     constraints (`v_r_in_exp` from the built-in volume ratio,
     `s_r_in_exp = s_r_su_exp`). The original's pressure inputs
     `P/1000.1` kPa (a 1e-4 fudge in the original) are kept as
     `P*1000/1000.1` Pa; its `273.1` K↔°C offsets (0.05 K below the exact
     conversion) are dropped — 0.05 K on every affected state.
  2. **The 9 REFPROP pseudo-quality outputs outside 0..1** (`Q_r_su_liq`,
     `Q_r_ex_vap`, `Q_r_in_exp`, `Q_r_ex_exp_s`, `Q_r_ex_exp`,
     `Q_r_ex_sc_cd`, `Q_r_ex_pp_s`, `Q_r_ex_pp`, `Q_r_su_exp`) are **not
     reproduced**: they are wrapper diagnostics (subcooled/superheated
     flags), unused elsewhere; the four exactly-0/1 ones are kept. Named as
     excluded in *Verification*.
  3. **`$common` lines dropped** (`CS-BUG-COMMON-PROC`: shared variables are
     silently zero): the procedures use their `fluid$` argument (`'R245fa'`
     at every call site) or the literal `'R245fa'` — the original's REFPROP
     blocks used the `$common` mixture whatever the `fluid$` argument, which
     the literal reproduces — and `MM` is computed locally with
     `molarmass()`.
  4. **The two 5-argument `IF(DELTAC_dot, 0, X, Y, Z)` calls** (condenser
     water-side temperatures) **rewritten with CoolSolve's 3-argument
     `if()`** — CoolSolve-only syntax, not valid EES (`CS-GAP-IF5`); the
     branch selection (sign of `DELTAC_dot`, > 0 at the stored point) is
     unchanged.
  5. **`End procedure` written `End`** (`CS-GAP-END-PROCEDURE`, registered
     with this file as evidence): CoolSolve does not recognise the
     terminator, swallowing `Function FluidPrice`.
  6. **The dead `if fluidev$='glycol'` block of `hx_cd` removed**:
     `fluidev$` is not an argument of `hx_cd` (EES evaluated the comparison
     as false; CoolSolve errors on the undefined procedure-local string);
     its outputs are unused or overwritten in the original (`cp_sf` is set
     just below).
  The equation count of the variant is 361 (largest block 24), vs the 293/331
  of the native parse, in which the REFPROP blocks are dropped with their
  output equations and variables.
- **2026-10-10 — re-check with CoolSolve `fix/library-gaps-2` @59b2862 (T-RECHECK, `CS-GAP-IF5` closed).** The five-argument `IF` of the native file is now implemented; the native file is still blocked, the first error now comes from another gap (the system is not square (293 equations, 331 unknowns: `CALL EES_REFPROP` outputs and `End procedure`), `CS-GAP-REFPROP`, `CS-GAP-END-PROCEDURE`). The variant is kept.
- **2026-10-10 — re-check with CoolSolve `fix/library-gaps-2` @57b22d3 (T-RECHECK, `CS-GAP-CALL-EXPR-OUT` closed).** The 13 `CALL EES_REFPROP` calls with an expression output (lines 696 ff., `T_r_su_vap+273.1`, `rho_r_su_vap/MM`, …) now parse: each expression gets an auxiliary variable `__out<k>_EES_REFPROP_L<line>` and an equation `expression = auxiliary`. The native file is still blocked and the first errors are lines 541 and 543 (`End procedure`, `CS-GAP-END-PROCEDURE`), then `EES_REFPROP` is an unknown procedure (`CS-GAP-REFPROP`). Evidence, in a scratch copy with only `End procedure` written `End`: the file is square (447 equations, 447 unknowns, largest block 54; it was 293 equations and 331 unknowns while the expression outputs were dropped) and the solve stops in block 26 (10 variables, `w_r_su_vap`, `Q_r_su_vap`, `Cv_r_su_vap`, …) with *"Unknown procedure: EES_REFPROP"*. The variant is kept; the replacement of the `CALL EES_REFPROP` blocks by pure-fluid CoolProp calls is still forced by `CS-GAP-REFPROP`.

## Limitations and CoolSolve gaps

- `CS-GAP-REFPROP` — all refrigerant properties go through
  `CALL EES_REFPROP(WorkingFluidMix$, code, …)` (codes 0, 12, 17, 25, 26, 27,
  90) on the mixture file `C:\REFPROP8\R245fa+R134a`; the EES REFPROP
  interface is not available in CoolSolve. The variant substitutes pure
  R245fa CoolProp calls, faithful only for the stored run (`MM_fraction = 1`).
- `CS-GAP-CALL-EXPR-OUT` — **closed in CoolSolve `fix/library-gaps-2` @57b22d3**: 13
  `CALL EES_REFPROP` calls of the main program use an expression as output, e.g.
  `… : T_r_su_vap+273.1` (line 693 ff.); CoolSolve v0.3.0 refused them
  (*"Output 1 of 'EES_REFPROP' must be a variable, not the expression
  'T_r_su_vap+273.1': …"*) and now accepts them (see the conversion log).
  Removed from `missing_features`. The variant replaces the calls (each
  output expression becomes one equation, see the conversion log), which is
  forced by `CS-GAP-REFPROP`.
- `CS-GAP-IF5` — **closed in CoolSolve `fix/library-gaps-2` @59b2862**: the 5-argument intrinsic
  `IF(DELTAC_dot, 0, X, Y, Z)` used twice in the condenser block for the
  water-side temperatures (not supported in CoolSolve v0.3.0); the variant
  keeps its 3-argument `if()`.
- `CS-GAP-END-PROCEDURE` — the `Procedure Summary` is closed with
  `End procedure` (valid EES, this file is the register evidence); the
  variant writes bare `End`.
- The cost model prices are dated (2011) and the fluid price function is
  stubbed to 15 €/kg in the original.

## Related models

- `CSL-0019` *orc_simple_r245fa*: simple ORC on pure R245fa with imposed
  component performance — same cycle family, component-level detail here.
- `CSL-0113` *condenser_3_zones_plate_correlations*: the same Thonon/Kuo
  plate-condenser approach on a single-zone basis.
- `CSL-0114` *evaporator_3_zones_plate_correlations*: the same Thonon/Hsieh
  plate-evaporator approach.
- `CSL-0121` *heat_transfer_fluid_properties*: the `prop_htf` procedure
  (Therminol VP-1, glycol) as a library function.
- `CSL-0124` *plate_hx_pressure_drop_identification*: same REFPROP-based
  plate-HX correlations (Thonon, Kuo, Hsieh) and the same blocked/variant
  pattern.

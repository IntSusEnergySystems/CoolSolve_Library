# CSL-0326 — thermosyphon_hx

Thermosyphon (heat-pipe) tube-bank heat exchanger — **status: `failing`** (see
[Why the model fails](#why-the-model-fails)).

Steady-state crossflow heat-pipe heat exchanger: hot flue gas (air) flows over
the evaporator bank of vertical thermosyphon tubes, water boils and condenses
inside each thermosyphon, and a cold process fluid (Cyclopentane at 31 bar,
which boils on the condenser side) flows over the condenser bank. Each tube row
is modelled with the detailed thermal-resistance network of the source:
external convective HTC (Zukauskas-type inline-tube-bank correlation with
regime selection and row-count correction), external radiative HTC (flue-gas
emissivity polynomial with bilinear-interpolated coefficients), wall
conduction, ESDU internal pool-boiling/film-condensation resistances
(ESDU 81038 via MacGregor, Kew & Reay 2005), internal vapour pressure drop and
axial wall conduction. The ESDU operating limits (entrainment, boiling, sonic,
dry-out, vapour pressure) are added as post-processing outputs. The row
marching of the source (fsolve per column) becomes simultaneous array
equations; the outer bisection on the cold-outlet state becomes the direct
boundary condition `h_c[62] = h_su_C`. Inlet and exhaust nozzles use the
tabulated isentropic-flow functions of the source.

- Main file: `thermosyphon_hx.eescode` (full 61-row bank, 3421 equations,
  square; the demo case of `hex_thermosyphon_example.py`).
- Companion: `thermosyphon_hx_row.eescode` (+ `.initials`): three independent
  rows (rows 1, 31, 61 of the source run) — the small verification
  configuration. Fails in CoolSolve like the full file.

## Source and attribution

- Original model: `HexThermosyphon` in
  [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy) (ULiège Thermodynamics
  Laboratory), commit `f03f7f47`:
  [`labothappy/component/heat_exchanger/hex_thermosyphon.py`](https://github.com/PyLaboThap/LaboThapPy/blob/f03f7f47/labothappy/component/heat_exchanger/hex_thermosyphon.py),
  example `labothappy/component/examples/heat_exchanger/hex_thermosyphon_example.py`,
  correlations `labothappy/correlations/heat_pipe/HP_h_coeffs.py`,
  nozzle `labothappy/toolbox/nozzle/airflow.py`. Local clone: `~/git/LaboThapPy`.
- Authors of the translated files (repository history): **Basile Chaudoir**
  (`hex_thermosyphon.py`, `HP_h_coeffs.py`, `airflow.py`, author `ba-chaudoir`)
  and **Elise Neven**.
- License of the source: Apache-2.0 (`LICENSE.txt`). Translated and credited;
  published under the library license.
- Scientific references cited by the source and used here: ESDU 81038 *Heat
  Pipes — Performance of Two-Phase Closed Thermosyphons* (1981); MacGregor,
  Kew & Reay (2005) *Investigation of Low Global Warming Potential Working
  Fluids for a Closed Two-Phase Thermosyphon*; Zukauskas/Incropera
  tube-bank correlations; Beale, *Tube Banks, Crossflow over* (ThermoPedia)
  for the Euler number; Churchill–Bernstein for the transitional regime.

## Niche

Nearest library model: **CSL-0099** (*air_cooler_air_side* — air-side HTC,
pressure drop and fan noise of a finned tube bundle, function library). CSL-0326
adds what no library model has: the complete thermosyphon heat pipe — internal
ESDU thermal-resistance network (pool boiling / falling-film condensation,
vapour pressure drop, axial wall conduction), the water-side saturation loop
closed through the internal vapour pressure drop, the flue-gas radiative
component with the source's emissivity-polynomial tables, and the ESDU
operating limits. Related: CSL-0014 (`hx_constant_pinch`, LaboThapPy pilot),
CSL-0013 (`heat_pump_basic_tespy`, TESPy pilot). The tube-bank external HTC
correlations are the overlap with CSL-0099; they are kept here in the source's
own form (Zukauskas regimes + C2 row correction + Euler-number pressure drop)
because the resistance network, the two-phase rows and the marching solution
are the model's substance.

## Translation notes (conversion log)

- Python solver plumbing removed: the fsolve-per-row (`equ_syst`, 17
  equations) becomes simultaneous equations over arrays `i=1..61`; the outer
  bisection of `solve()` becomes `h_c[62] = h_su_C` (the cold fluid is indexed
  from the outlet, row 1, to the inlet, row 62, as in the source arrays);
  `vect_init` guesses become `.initials` (shipped for the row companion only).
- The source's `try/except` on the CoolProp cold-side state (which selects the
  forced-convection-boiling HTC `ext_conv_boil` when the fluid sits on the
  saturation plateau, and the inline-bank single-phase correlation otherwise)
  becomes the indicator `in2ph[i] = 1-Step(abs(T_c[i]-Tsat_C)-1e-6)`. The
  `ext_conv_boil` branch is evaluated with `min(T_c[i], Tsat_C)` as saturation
  temperature: off the plateau the original never evaluates this branch, and
  the flag zeroes it, so the clamp only keeps CoolProp calls in their domain.
  The `flag_1_phase`/`ext_conv_boil` path of the *hot* side and the `Oil`
  property tables of `HP_h_coeffs.py` are not translated (dead in the example;
  the cold fluid of the example is Cyclopentane, not the tabulated oil).
- Regime selections (`if Re...`, `F_1`, `F_2`, `F_3`, laminar/turbulent vapour
  friction, low/high-velocity boiling) are transcribed with the unit step
  `Step(x) = 0.5*(sign(x)+1)` — pure arithmetic, no `IF`.
- The bilinear interpolation of the flue-gas emissivity coefficients
  `a_0..a_3` (`fg_radiative_htc_corr`) becomes `interpolate2` over the grid
  tables `thermosyphon_hx-fg_a*.csv` (clamping at the grid ends, like the
  source's interpolator). The nozzle isentropic-function tables
  (`nozzle_tables`) become `thermosyphon_hx-nozzle.csv`; the Zukauskas C2 row
  correction becomes `thermosyphon_hx-c2.csv`. Tables were generated from the
  source module itself (work folder, deleted after the import).
- Temperatures: property calls use °C (CoolSolve unit system), the
  correlation variables keep K (radiation, sound speed, ESDU figures of
  merit), as in the source formulas.
- Fluid names: CoolProp `Cyclopentane` and `Air` keep their names (CoolSolve
  resolves them as CoolProp fluids, matching the source's property backend);
  the heat-pipe fluid `Water` is the real-fluid name.
- The source computes but does not return the ESDU operating limits
  (`operating_limits` called in `thermosyphon_model`, result discarded). They
  are kept and exposed as outputs `Q_dot_ent[i]`, `Q_dot_boil[i]`,
  `Q_dot_son[i]`, `Q_dot_dry[i]`, `Q_dot_vap[i]`.
- `DUPLICATE` bounds: CoolSolve requires literal/constant-expression bounds,
  so the bounds are written as 61 (the `N_col = FLOOR(L_core/S_T)-1` equation
  is kept as a variable for the row count); main-program references
  `T_h[N_col+1]` etc. are written as `T_h[62]` (CoolSolve would otherwise
  create unresolved `T_h[expr]` pseudo-variables). Valid EES either way.
- The two nozzle CALLs are inlined in the main program (their outputs were
  unsovlable blocks in early attempts); the correlations stay as
  FUNCTION/PROCEDURE per the card's T-FUNC convention: `Step`, `Phi_cond_HP`,
  `Phi_boil_HP`, `ThResESDU`, `DeltaPV_HP`, `OpLimitsHP`, `RadAcoeff`,
  `RadHTC_FG`, `EuBank`, `BankHTC`, `ExtConvBoil` (+ the inlined `Nozzle`).
- Row 1 of the cold side is superheated vapour, rows ~15–37 sit exactly on the
  saturation plateau (two-phase), the rest is compressed liquid — the source
  model handles all three; the translation keeps that (the `in2ph` branch).
- **2026-11-01 — review of the failing models** (see *Why the model fails*):
  temperature-unit errors corrected (main file: `in2ph`, `ExtConvBoil` wall
  temperature, `cp_wf`, `cp_H`, `cp_h_m`, `rho_h_out`, `cp_h_exit`; row
  companion: cold-side `BankHTC` inputs, `ExtConvBoil`, `cp_H`), `rho_wf_in`
  at the cold outlet `h_c[1]` as in the source, row-companion `u_h` set to the
  source run's 6.718 m/s, row-companion `.initials` replaced by the source's
  converged row states (instrumented re-run). No other equation changed.

## Reference results (re-run of the source example)

`hex_thermosyphon_example.py` was re-run in a throw-away virtual environment
(`pip install` of the local clone, CoolProp 8.0.0, scipy; script and raw
results in the deleted work folder; converged in 7 bisection iterations,
relative residual 9.7e-4 ≤ its `res_tol` 1e-3 — the source itself stops at
~1e-3, so CoolSolve solutions should agree to that order):

| quantity | LaboThapPy example |
|---|---|
| rows N_col / tubes per row | 61 / 74 |
| L_e, L_c, L_a [m] | 1.824 / 1.026 / 0.15 |
| cold outlet T_c[1] [K] | 516.861 |
| cold inlet T_c[62] [K] | 434.094 |
| hot inlet T_h[1] / P_h[1] | 738.261 K / 101853.8 Pa |
| hot outlet T_h[62] / P_h[62] | 543.364 K / 101092.0 Pa |
| Q_dot_row[1] / [31] / [61] [kW] | 93.34 / 118.28 / 69.86 |
| sum Q_dot_row [MW] | 5.869 |
| T_HP_h[1] / P_HP_h[1] | 626.186 K / 17.155 MPa |
| exhaust nozzle T_h_out / P_h_out | 543.458 K / 101153.0 Pa |

## Why the model fails

### Review of 2026-11-01 (supersedes the diagnosis below)

The failure has three distinct causes; the first two are fixed.

1. **CoolSolve bug `CS-BUG-PROC-NEG-POW` — root cause found and fixed on a
   CoolSolve branch.** `RadHTC_FG` evaluates `log10(pL)^2` and `log10(pL)^3`
   with `pL` < 1 (a negative base). CoolSolve's forward-mode AD wrote the
   derivative of `x^y` as `x^y·(y'·ln x + y·x'/x)`: with `x` < 0, `ln x` is NaN
   and `0·NaN = NaN`, so the whole Jacobian row of the CALL output became NaN,
   and so did the row of `h_e_o = h_r_e_o + h_c_e_o` (a CALL output keeps the
   procedure's AD value inside its block). Newton/KINSOL then stop with
   *SingularJacobian* at iteration 0 and tearing reports a singular Schur
   complement, exactly the symptoms seen since the import. The fix (power rule
   for `d/dx`, the `ln x` term only where the exponent varies) is on the
   CoolSolve branch **`fix/ad-pow-negative-base`** (not merged; regression
   tests `[neg-pow]`, `[autodiff]`), which also fixes the
   `solver_singular_diagnostics.md` dump: it printed a garbled Jacobian
   (`J.row(r).data()` on a column-major matrix), which had led to the wrong
   reading "the singular equation is the unused output `a_g`".
2. **Unit errors of the first translation — corrected in both files.** In the
   main file: `in2ph[i]` compared `T_c` (K) with `Tsat_C` (°C), so the boiling
   branch was never selected; `ExtConvBoil` received `T_wc_o` in K for a °C
   argument; `cp_wf`, `cp_H`, `cp_h_m`, `rho_h_out` and `cp_h_exit` passed
   temperatures in K to property calls that take °C; `rho_wf_in` was evaluated
   at the cold *inlet* `h_c[62]` instead of the outlet `h_c[1]`
   (the source's `h_wf_out_guess`). In the row companion: the cold-side
   `BankHTC` received °C temperatures for K arguments (Cyclopentane evaluated
   at −29 °C as a liquid: 1091 instead of 228 W/(m²·K)), `ExtConvBoil` and
   `cp_H` had the same K/°C slips, and `u_h` was hard-coded to 10.663 m/s
   while the source run uses 6.718 m/s.
3. **The two-phase rows of the source are numerically degenerate (open).**
   On the saturation plateau (rows ≈ 15–37) the source uses `ext_conv_boil`,
   i.e. `h = q_max/(T_wall − T_sat)` with `q_max` the Lienhard–Eichhorn
   *critical* heat flux. With the cold fluid at `T_sat`, the condenser-side
   heat flow `A·h·(T_wall − T_cold)/(1+foul)` collapses to the constant
   `A·q_max/(1+foul)`: the equation loses its dependence on the wall
   temperature (the source's own row-31 solution has a wall superheat of
   0.063 K and `h` = 4.7·10⁵ W/(m²·K)). Physically the critical heat flux is
   imposed as the operating flux. scipy's `fsolve` (MINPACK hybrd) tolerates
   the resulting near-singular Jacobian; CoolSolve's pipeline does not: the
   row-31 block of the companion fails even when started from the source's
   solution (Try Harder: tearing singular Schur complement).

**Verification of the corrected translation (row companion, patched CoolSolve,
Try Harder).** With row 31 replaced by row 61 to test the single-phase rows
alone, the block converges in 29 iterations and reproduces the re-run of the
source (LaboThapPy `f03f7f47`, CoolProp 8.0.0, rows 0 and 60 of the final
bisection iteration, recorded by instrumenting `thermosyphon_model`):

| Row | Quantity | CoolSolve | LaboThapPy | diff |
|---|---|---:|---:|---:|
| 1 | heat per tube | 1259.91 W | 1261.36 W | −0.12 % |
| 1 | `T_HP_h` | 626.10 K | 626.19 K | −0.01 % |
| 1 | `P_HP_h` | 17.137 MPa | 17.155 MPa | −0.11 % |
| 1 | hot / cold HTC | 113.22 / 227.85 W/(m²·K) | 113.22 / 227.85 | < 1e-5 |
| 1 | radiative HTC | 7.880 W/(m²·K) | 7.878 | +0.02 % |
| 61 | heat per tube | 938.89 W | 944.03 W | −0.55 % |
| 61 | `T_HP_h` | 464.67 K | 464.80 K | −0.03 % |
| 61 | hot / cold HTC | 122.20 / 700.30 W/(m²·K) | 122.20 / 700.32 | < 3e-5 |

The remaining 0.1–0.6 % is the order of the source's own tolerance (its
`fsolve` and bisection stop at a relative residual of about 1e-3) and of the
CoolProp 8.0.0 vs 8.1.0-dev Water/Cyclopentane property differences.

**Source issues noticed (LaboThapPy `f03f7f47`, to report upstream):**
`nozzle()` computes the critical area as `m/(ρ_in·a_in)` (without the
critical-flow factor 0.5787 = (2/(γ+1))^((γ+1)/(2(γ−1)))) and interpolates
the Mach table linearly, so the casing velocity it returns (6.72 m/s) violates
continuity (`m/(ρ·A)` ≈ 10.7 m/s); in `equ_syst`, `cp_H` is read from `AS_H`
after updating `AS_C` (it returns the air `c_p` at the wall temperature of the
last bank call); the per-tube balances `f14`/`f15` use the heat of one tube
with the flow of the whole bank (the internal `T_e_o_ex`, `T_c_o_su` barely
move; the row marching itself uses `Q_dot_row`). The translation keeps these
as in the source.

**Hints for CoolSolve** (beyond the merged-or-not fix above): (a) a
MINPACK-hybrd-like dogleg that keeps progressing on rank-deficient blocks
(the source solves the same rows with scipy `fsolve`); (b) when a Jacobian
contains NaN/Inf, report the offending equation and variable in the error
message (the new diagnostics section of the branch does it in debug mode);
(c) the full file has one 2923-variable block (the 61 rows are coupled through
the marching of both streams): a block-sequential strategy that solves the
rows one after the other inside an outer iteration on the cold-side boundary
(the source's own strategy) would replace one huge Newton system by 61 small
ones.

**Full file.** Without `.initials`, CoolSolve's default-guess inference
does not recognise the temperatures held in K (they enter the property calls
as `T-273.15`, procedure arguments or linear relations), so they all start at
**1 K**: 488 residuals of the 2926-variable block are NaN/inf at iteration 0
(`ThResESDU`, `DeltaPV_HP`, `ExtConvBoil`: Water properties at −272 °C, a
division by zero in the boiling HTC), and Try Harder then iterated on ‖F‖ = inf
for 33 min without reporting it (stopped). Registered in the CoolSolve
register as `CS-BUG-GUESS-INFER` (type inference limited to two syntactic
patterns; improvement: propagate types through affine relations, CALL
arguments and procedure bodies) and `CS-BUG-NONFINITE-START` (fail fast and
list the non-finite equations). A `thermosyphon_hx.initials` built from the
instrumented source run (all 61 rows: wall, heat-pipe and stream states,
1409 values) is now shipped: with it the residual is finite (4.7·10⁵), but
Newton stalls at ‖F‖∞ = 4.72·10⁵ (line search failed after 17 iterations,
patched CoolSolve, Try Harder), a value of the order of the boiling HTC of the
two-phase rows (4.7·10⁵ W/(m²·K) in the source), consistent with cause 3.

**Status: failing** (kept). To make the model run, the maintainer can either
(i) keep the source physics and wait for a solver that copes with the
degenerate boiling rows, or (ii) adapt the model: replace the CHF-based
`ext_conv_boil` by a flow-boiling HTC that depends on the wall superheat
(e.g. a Cooper/Gorenflo nucleate-boiling term) — a change of the source
physics, which would make the model `modified`.

### Diagnosis of the import (2026-10-31, superseded)


CoolSolve 0.4.0 (`coolsolve --version`: 0.4.0, CoolProp 8.1.0-dev
`75af78166`) cannot solve either file; the failure was reproduced on a
235-variable truncation (5 rows) and is fully diagnosed:

1. Full file, 3421 equations (square, largest block 2923): `Newton` and
   `KINSOL` stop with `SingularJacobian` at iteration 0; `Partitioned` does
   not move from the initial residual in 20000 iterations; tearing reduces the
   block to a 1098-variable Newton (one Jacobian ≈ 20 min) — not tractable.
2. Row companion (three 43-var blocks): `Tearing → singular Schur complement`;
   the singular equation named in the CoolSolve debug output is the BankHTC
   output `a_g` (sound speed, computed but used by no other equation); plain
   `Newton` on the same block also stops with `SingularJacobian`.
3. The same equations with every procedure CALL replaced by its (independent)
   constants converge, and every CALL converges standalone at the exact
   initial states of the model (`bank_test`, `oplim_test` in the work folder):
   the equations and the procedures are correct; the failure is in CoolSolve's
   Jacobian/tearing treatment of procedure CALLs inside DUPLICATE blocks.
   A missing initial value (`P_HP_c`, found via a frozen `maxIterations = 0`
   debug run) was corrected along the way; the failure persists.

Not registered as a gap (no minimal reproducer and no EES-manual evidence at
hand that procedure CALLs inside DUPLICATE loops must be differentiable across
the call boundary — they are standard EES practice): reported to the
maintainer as an unverified suggestion, together with the observation that
CoolSolve's `max(..., i=1, N)` indexed form is not implemented (SUM is).

## Verification status

Not verified end-to-end: no `.sol` could be produced (status `failing`). The
single-phase rows of the corrected row companion agree with the source within
0.6 % with the CoolSolve fix of branch `fix/ad-pow-negative-base` (see *Why the
model fails*). Earlier checks (2026-10-31; note that the standalone cold-side
value 59.1 W/(m²·K) below is not the source's row-1 value, 227.85, which the
corrected translation reproduces):
every correlation procedure was solved standalone at the model's own operating
points and agrees with CoolProp values (e.g. cold-side bank at row 1:
h = 59.1 W/m²K, Re = 1399; ESDU resistances R_cond = 3.44e-3 K/W,
R_evap = 4.27e-3 K/W; radiative HTC = 7.5 W/m²K; operating limits at
T_HP_h[1] = 626.19 K: Q_ent = 22.1 MW, Q_boil = 2.14 MW, Q_son = 18.3 GW,
Q_dry = 0.73 MW, Q_vap = 1.05 TW); the constants-substituted variant of the
row equations converges to the source's row states. The reference numbers
above come from re-running the source example.

## Files

- `thermosyphon_hx.eescode` + `.initials` — full model (failing); the `.initials` are the 61 converged rows of the source example (2026-11-01).
- `thermosyphon_hx_row.eescode` + `.initials` — single-row configuration (failing).
- `thermosyphon_hx-{fg_a0..fg_a3,nozzle,c2}.csv` and the
  `thermosyphon_hx_row-*` copies — correlation and nozzle tables extracted
  from the source modules.

## Follow-up of 2026-10-31 (CS-BUG-PROC-NEG-POW check)

CS-BUG-PROC-NEG-POW was registered after the first import. The procedures did
contain integer powers of quantities that go negative during solver
exploration (`BankHTC`: `V_mx^2` of a velocity input; `EuBank`: `Re^2..Re^4`;
`ExtConvBoil`: `V_flow^2`) plus fractional powers of the same quantities. In a
work copy all integer powers were rewritten as products and the fractional
bases guarded with `abs()` (solution-invariant: every base is positive at the
solution), with proper initial values for all inlined variables — the system
still does not converge (Newton/KINSOL singular Jacobian, tearing singular
Schur complement, Partitioned and TrustRegion no convergence in up to 20000
iterations). The neg-pow bug was therefore present but is not the only
blocker; the native file is unchanged and no runnable variant could be
produced. The rewrite evidence was added to the CS-BUG-PROC-NEG-POW register
row. The 3-row companion was additionally rebuilt with every procedure inlined
into the main program (D10-style flattening, per-call suffixes): it still fails
in the same way, so it is not shipped with a `.sol`.

Unverified suggestions closed or kept open: the earlier "CALL-in-DUPLICATE"
suggestion could not be reproduced in isolation (minimal CALL-in-DUPLICATE,
function-in-procedure, property-in-procedure and feedback-loop reproducers all
solve — 8 test files in the deleted work folder), so it remains an unresolved
observation tied to the full model context, not a registered gap. The indexed
`max(x[i], i=1, N)` form (SUM exists, MAX does not) has no EES-file evidence in
`EES_ok.zip`/`thermo_models` and stays unregistered. FLOOR in DUPLICATE bounds
and the Partitioned no-progress stall likewise stay unregistered (no minimal
reproducer / no EES-side evidence).

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

Not verified end-to-end: no `.sol` could be produced. What *was* checked:
every correlation procedure was solved standalone at the model's own operating
points and agrees with CoolProp values (e.g. cold-side bank at row 1:
h = 59.1 W/m²K, Re = 1399; ESDU resistances R_cond = 3.44e-3 K/W,
R_evap = 4.27e-3 K/W; radiative HTC = 7.5 W/m²K; operating limits at
T_HP_h[1] = 626.19 K: Q_ent = 22.1 MW, Q_boil = 2.14 MW, Q_son = 18.3 GW,
Q_dry = 0.73 MW, Q_vap = 1.05 TW); the constants-substituted variant of the
row equations converges to the source's row states. The reference numbers
above come from re-running the source example.

## Files

- `thermosyphon_hx.eescode` — full model (failing).
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

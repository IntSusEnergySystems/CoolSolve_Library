# CSL-0326 — thermosyphon_hx

Thermosyphon (heat-pipe) tube-bank heat exchanger — **status: `verified` (adapted from the original)**, see
[Adaptation of 2026-11-01](#adaptation-of-2026-11-01-second-review).

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
boundary condition `h_c[62] = h_su_C`. The external side (cold-side boiling, stream velocities, row states,
nozzles, operating limits) was corrected on 2026-11-01.

- Main file: `thermosyphon_hx.eescode` (+ `.initials`, `.sol`): full 61-row bank, 4597 equations, one
  3599-variable block; the demo case of `hex_thermosyphon_example.py`. Converges with the default Newton from the
  shipped `.initials`; **slow** (about 10 min, dense Jacobian of the 3599-variable block).
- Companion: `thermosyphon_hx_row.eescode` (+ `.initials`, `.sol`): three independent rows fed with the row
  states of the source run (rows 1, 31, 61: superheated vapour, boiling, subcooled liquid on the cold side) — the
  small verification configuration (1.4 s).

## Problem statement

Recover heat from a hot flue-gas stream into a boiling process fluid with a
crossflow thermosyphon (heat-pipe) tube-bank heat exchanger: hot flue gas (air)
flows over the evaporator bank of vertical thermosyphon tubes, water boils and
condenses inside each thermosyphon, and a cold process fluid (Cyclopentane at
31 bar, which boils on the condenser side) flows over the condenser bank. The
demonstrated case is the demo case of the source example
`hex_thermosyphon_example.py` (61 rows, 74 tubes per row).

## Model

Each tube row is modelled with the detailed thermal-resistance network of the
source: external convective HTC (Zukauskas-type inline-tube-bank correlation
with regime selection and row-count correction), external radiative HTC
(flue-gas emissivity polynomial with bilinear-interpolated coefficients), wall
conduction, ESDU internal pool-boiling/film-condensation resistances (ESDU
81038 via MacGregor, Kew & Reay 2005), internal vapour pressure drop and axial
wall conduction. The ESDU operating limits (entrainment, boiling, sonic,
dry-out, vapour pressure) are added as post-processing outputs. The row
marching of the source (fsolve per column) becomes simultaneous array
equations; the outer bisection on the cold-outlet state becomes the direct
boundary condition `h_c[62] = h_su_C`. The external side (cold-side boiling,
stream velocities, row states, nozzles, operating limits) was corrected on
2026-11-01 (see *Adaptation of 2026-11-01*); the transcription of the
correlations and the solver-plumbing mapping are in *Conversion log*.

## How to run

```bash
coolsolve ./thermosyphon_hx.eescode        # full 61-row bank (about 10 min)
coolsolve ./thermosyphon_hx_row.eescode    # three-row verification configuration (1.4 s)
```

Both files need their shipped `.initials`: the main file converges with the
default Newton from them (they come from a row-by-row marching of the
adapted model; from the source states alone Newton creeps, 0.4 % per
iteration); the row companion is fed with the row states of the source run
(rows 1, 31, 61: superheated vapour, boiling, subcooled liquid on the cold
side). Correlation tables ship as `thermosyphon_hx-{fg_a0..fg_a3,c2}.csv`
(see *Files*).

## Results

Default operating point (shipped `.sol`, adapted model): 6.061 MW exchanged
(source run 5.869 MW); flue gas 738.2 → 536.7 K (exhaust 536.7 K, 100 397 Pa;
casing pressure drop 1411 Pa); Cyclopentane 434.0 → 522.0 K, outlet
superheated vapour. Per tube: about 1.4 kW in the superheated-vapour rows
(1–15), 1.5 to 2.4 kW in the nucleate-boiling rows (16–33), down to 0.62 kW in
the subcooled-liquid rows (34–61). Heat-pipe saturation temperature 641.6 K in
row 1 down to 488.6 K in row 61. The re-run of the source example is tabulated
in *Results of the source example (re-run of the reference)* below; design flags of
the source example (entrainment limit in row 1, dry-out limit exceeded in
every row) are in *Adaptation of 2026-11-01*.

## Adaptation of 2026-11-01 (second review)

The first review (section *Why the model failed*, below) fixed the CoolSolve AD bug and the unit errors of the
translation and showed that the single-phase rows reproduce the source within 0.6 %, but left the two-phase rows
degenerate. The second review checked the source physics itself; **the external side of the source is not
right** in several places, and the model was adapted to standard correlations of the source's own reference
(Incropera). Changes (marked `ADAPTED` in both files):

1. **Boiling on the cold side.** The source's `ext_conv_boil` computes the Lienhard–Eichhorn **critical** heat
   flux (it is called `q_max` in the code) and divides it by the wall superheat to make a "heat transfer
   coefficient": the cold-side heat flow of every two-phase row is then pinned at the CHF, whatever the wall
   temperature (source row 31: 1598 W per tube = q_max·A/(1+foul) = 1608 W), which makes the equations degenerate
   and is physically wrong (the CHF is the upper limit of nucleate boiling, not its operating flux). Moreover the
   correlation is used at 0.06 m/s, essentially pool boiling, where its "high-velocity" branch gives a CHF ten times
   below the pool-boiling value. Replaced by the **superposition** of forced convection (Zukauskas, as the
   source's single-phase rows) and **Rohsenow nucleate boiling** (Incropera eq. 10.5) with the constants the same
   authors use in their own `pool_boiling` function (C_sf = 0.013, n = 1.7, pentane on polished nickel),
   active where liquid is present and the wall is above saturation, and **capped at the critical heat flux**
   (Zuber/Lienhard pool value, Incropera eq. 10.7, C = 0.149): above it Rohsenow does not apply — near the dew
   point the hot wall is about 100 K above saturation. The forced-convection HTC blends the liquid and vapour
   branches with the vapour quality, so the cold-side flux is continuous across the bubble and dew points. The
   Lienhard–Eichhorn CHF is kept as an informative output (`q_max_LE`), the ratio flux/CHF as `q_ratio_CHF[i]`
   (at most 0.11).
2. **Stream velocities.** The source uses one cold velocity for all rows, computed with the density of the cold
   **outlet** (vapour) state — the code was written for an incompressible oil ("oil density at 110 °C") — so the
   liquid rows had a velocity six times too high; and one hot velocity from `nozzle()`. Both are replaced by
   continuity at each row, `u = G/rho(row state)` (for the cold side, per phase branch).
3. **Nozzle.** `nozzle()` computes the critical area without the critical-flow factor 0.5787 and interpolates the
   Mach table linearly: its casing velocity (6.72 m/s) violates continuity (10.70 m/s); the exhaust nozzle used the
   condenser casing area. Replaced by continuity and the steady-flow energy balance (Mach < 0.05).
4. **Row states.** The per-tube balances `f14`/`f15` of the source use the heat of one tube against the flow of the
   whole bank (their internal gas and cold temperatures barely move). The row states are now those of the row
   marching (`T_h[i]`→`T_h[i+1]`, `h_c[i]`→`h_c[i+1]`), both streams on enthalpy, with the row-mean
   temperatures as driving temperatures.
5. **Operating limits.** The source returns the ESDU 81038 limits as heat **fluxes** but labels them in W
   (dimensional check: every expression is in W/m²); the heat-rate limits per tube are now computed with the pipe
   cross-section (entrainment, sonic, dry-out, vapour pressure) and the evaporator wall (boiling), and given as
   ratios (`ratio_ent[i]`, `ratio_dry[i]`). They are explicit FUNCTION calls (`OpLimHP`): as a PROCEDURE CALL their
   huge values (up to 1E14 W/m²) formed an implicit block whose absolute tolerance could not be met.
6. **CoolSolve powers** — at import, `lpL^2`, `lpL^3` (`lpL = log10(pL)` < 0) and `Q_rad^2` were written as
   products to dodge the AD bug `CS-BUG-PROC-NEG-POW` of the then-current release; restored to the power forms of
   the Python source on 2026-11-02 (re-check card C-484, bug closed in CoolSolve `07bf9dc`, build `0.4.0@2dc1367`).
   Row companion `.sol` byte-for-byte identical; main file: max rel. diff 6.5·10⁻¹⁰ (at `q_dry[4]`) over all
   variables of magnitude above 1e-6 — within rtol 1e-9; the only larger raw ratios are machine noise on values of
   |v| <= 7.8e-8 (absolute differences <= 2e-16, e.g. `f_v[41]` = -6.6e-30 vs -6.7e-27, zero to within 1e-26).

**Checks**: hot- and cold-stream energy balances closed to 1.4·10⁻⁶ W (6 MW exchanged); cold inlet boundary met
exactly; the coupled full model agrees with an **independent row-by-row marching** (each row solved alone,
secant on the cold outlet, 5 passes) to 1.7·10⁻⁶ on every row heat; cold-side flux ≤ 11 % of the CHF; no
temperature cross. The translation of the correlations was verified against the source in the first review
(single-phase rows within 0.6 % of an instrumented re-run of LaboThapPy before the adaptation).

**Design flags of the source example** (results of the model, not errors): the water thermosyphons of the
first rows run at 641.6 K, 5.5 K below the critical point of water, and row 1 sits at its **entrainment limit**
(1408 W per tube for a limit of 1410 W); the **dry-out** limit as coded in the source (constant 447, fill ratio
0.6) is exceeded in every row (by 2.8 to 43 times) — this correlation could not be checked against ESDU 81038.

**Solver notes / CoolSolve hints**: the coupled model (counter-flow marching of both streams) is one
3599-variable block; it converges with the default Newton from the shipped `.initials`, which come from the
row-by-row marching above (from the source states alone Newton creeps, 0.4 % per iteration). Each solve takes
about 10 min because CoolSolve's forward-mode AD carries a dense 3599-component gradient on every intermediate
value and factors a dense Jacobian — **sparse AD / sparse Jacobians** would make such models fast. A
block-sequential strategy for marching structures (solve the rows in order inside an outer iteration on the
boundary, as the source and the marching script do) would also remove the need for curated initials.

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

## Conversion log

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

## Results of the source example (re-run of the reference)

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

## Why the model failed (first review of 2026-11-01, history)

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
   CoolSolve branch **`fix/ad-pow-negative-base`** (merged in CoolSolve main `07bf9dc` on 2026-11-01, closed in
   register §7; regression
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

Verified (adapted model, 2026-11-01): energy balances, independent row-by-row marching, CHF and phase-continuity
checks, see *Adaptation of 2026-11-01*; the correlation translation against an instrumented re-run of the source
(first review). History of the earlier checks (2026-10-31; the standalone cold-side value 59.1 W/(m²·K) quoted
there is not the source's row-1 value, 227.85, which the corrected translation reproduces):
every correlation procedure was solved standalone at the model's own operating points and agrees with CoolProp
values (ESDU resistances R_cond = 3.44e-3 K/W, R_evap = 4.27e-3 K/W; radiative HTC = 7.5 W/m²K); the
operating-limit values of that time (Q_ent = 22.1 MW, …) are heat fluxes in W/m², not watts (see item 5).

## Files

- `thermosyphon_hx.eescode` + `.initials` + `.sol` — full model (verified, adapted); the `.initials` are its
  converged solution, first obtained from a row-by-row marching (2026-11-01).
- `thermosyphon_hx_row.eescode` + `.initials` + `.sol` — three-row verification configuration.
- `thermosyphon_hx-{fg_a0..fg_a3,c2}.csv` and the `thermosyphon_hx_row-*` copies — correlation tables extracted
  from the source modules (the nozzle tables were removed with the source's `nozzle()`, see item 3).

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

## Limitations and CoolSolve gaps

- The external side of the **source** was not right in several places
  (CHF-based boiling HTC, one outlet-density velocity for all rows, nozzle
  without the critical-flow factor, per-tube balances); the model adapts them
  to standard correlations of the source's own reference (Incropera), marked
  `ADAPTED` (see *Adaptation of 2026-11-01*).
- Design flags of the source example (results of the model, not errors): row 1
  sits at its entrainment limit (1408 W per tube for a limit of 1410 W); the
  dry-out limit as coded in the source is exceeded in every row (by 2.8 to 43
  times) and could not be checked against ESDU 81038.
- **Slow solve**: one 3599-variable block, dense AD gradient and dense
  Jacobian, about 10 min per solve; sparse AD / sparse Jacobians and a
  block-sequential strategy for marching structures are the CoolSolve
  improvements suggested in *Adaptation of 2026-11-01* (unregistered
  suggestions, with the CALL-in-DUPLICATE observation of the history below).
- No CoolSolve gap blocks the model: both files solve with the shipped
  `.initials` (`missing_features` empty).

## Related models

- `CSL-0099` *air_cooler_air_side*: air-side HTC, pressure drop and fan noise
  of a finned tube bundle (function library) — the tube-bank external HTC
  correlations are the overlap; kept here in the source's own form.
- `CSL-0014` *hx_constant_pinch*: LaboThapPy pilot.
- `CSL-0013` *heat_pump_basic_tespy*: TESPy pilot.

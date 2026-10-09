# Void-fraction correlations for two-phase flow (13 models)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ⛔ **Blocked** (runnable variant verified) &nbsp;|&nbsp; `CSL-0131`

EES `FUNCTION` library of the void-fraction correlations of
[LaboThapPy](https://github.com/PyLaboThap/LaboThapPy) (ULiège Thermodynamics
Laboratory): the thirteen models of `labothappy/correlations/void_fraction/
void_fraction.py`, one `FUNCTION` each, spanning the homogeneous, slip-ratio,
empirical, *K·α_h* and drift-flux families. Saturated properties are
arguments, so the calling model evaluates them; the Reynolds and Weber numbers
Premoli needs are helper functions. The demonstration program reproduces the
case of the original example, `void_fraction_example.py`: R410A at 1.2 MPa in
an 8 mm pipe at a mass flux of 300 kg/m²·s, ten qualities from 0.05 to 0.95.

The native file is **blocked** by the registered CoolSolve bug
`CS-BUG-IMPLICIT-PROC`: the Hughmark correlation is implicit (the mixture
viscosity depends on the void fraction it corrects) and CoolSolve silently does
not solve an implicit equation sitting inside a multi-statement `FUNCTION` body.
The native file is left in valid EES; the runnable variant
`void_fraction_correlations_coolsolve.eescode` writes that one implicit equation
in the main program and is **verified** against the original (130 values, max
deviation 2.2·10⁻⁵).

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | the correlations are fluid-independent; the demonstration program uses R410A (CoolProp `'R410A'` is the EES fluid `R410A`, a real fluid — no renaming needed) |
| **Size** | 161 equations after analysis (largest block: 1) in the native file, 171 in the variant; 15 functions of 4–37 lines |
| **Source** | [`LaboThapPy`](https://github.com/PyLaboThap/LaboThapPy), commit `f03f7f47`, file `labothappy/correlations/void_fraction/void_fraction.py` (Apache-2.0 `LICENSE.txt`, MIT `pyproject.toml`), helpers `compute_reynolds`/`compute_weber` of `labothappy/correlations/properties/dimensionless.py` and `get_saturated_phase_properties` of `labothappy/correlations/properties/two_phase.py`; inventory row `LTP-033` of `sources/labothappy/inventory.csv` |
| **Authors** | Elise Neven (the `void_fraction.py` module); the authors of the correlations are credited in the comment block of each function and in `model.json` |
| **License** | MIT (library decision D3) |
| **CoolSolve** | 0.3.0 — native file **blocked** by `CS-BUG-IMPLICIT-PROC`; runnable variant **verified** against LaboThapPy `f03f7f47` (130 values, max deviation 2.2·10⁻⁵) |

## Problem statement

Given the saturated densities `rho_l`, `rho_v`, the vapour quality `x`, and
whichever of the viscosities, surface tension, mass flux, diameter, pressure and
inclination the chosen correlation needs, compute the void fraction `alpha` of a
two-phase refrigerant or ORC flow. Which correlation applies depends on the flow
regime, the orientation and the fluid, so the library exposes all thirteen and
lets the caller choose — as `CSL-0130` does for the friction factors.

## Model

| EES `FUNCTION` | Arguments | Equation | Family / validity (as quoted in the source) |
|---|---|---|---|
| `void_fraction_homogeneous` | rho_l, rho_v, x | α = 1/(1 + (rho_v/rho_l)(1−x)/x) | homogeneous, S = 1; accurate above x = 0.7 |
| `void_fraction_Zivi` | rho_l, rho_v, x | S = (rho_l/rho_v)^(1/3) in the same slip-ratio form | slip ratio; annular, high quality |
| `void_fraction_Fauske` | rho_l, rho_v, x | S = (rho_l/rho_v)^(1/2) | slip ratio; water–steam, high mass flux |
| `void_fraction_Premoli` | rho_l, rho_v, x, mu_l, sigma, d_hyd, G | y = α_h/(1−α_h), F1 = 1.578·Re_l^−0.19·(rho_l/rho_v)^0.22, F2 = 0.0273·We_l·Re_l^−0.51·(rho_l/rho_v)^−0.08, S = 1 + F1·√(y/(1+y·F2) − y·F2) | slip ratio (CISE); vertical adiabatic upward flow |
| `void_fraction_Hughmark` | rho_l, rho_v, x, mu_l, mu_v, d_hyd, G | Z = (d_hyd·G/mu_mix)^(1/6)·((G·x/(9.81·d_hyd·rho_v·α_h(1−α_h)))²)^(1/8), mu_mix = mu_l + α(mu_v − mu_l), ln K_h = degree-4 polynomial in ln Z, α = K_h·α_h | implicit slip ratio; vertical and horizontal gas–liquid hold-up |
| `void_fraction_Lockhart_Martinelli` | rho_l, rho_v, x, mu_l, mu_v | X_tt = ((1−x)/x)^0.9·(mu_l/mu_v)^0.1·(rho_v/rho_l)^0.5; α = (1+X_tt^0.8)^−0.378 for X_tt ≤ 10, α = 0.823 − 0.157·ln X_tt above | empirical; both phases turbulent |
| `void_fraction_Graham` | rho_v, x, d_hyd, G | F_t = √(x³G²/(9.81·rho_v²·d_hyd(1−x))), α = 1 − exp(−1 − 0.3·ln F_t − 0.0328·ln²F_t) for F_t > 0.01032, else 0 | condensation only |
| `void_fraction_Cioncolini_Thome` | rho_l, rho_v, x | h = −2.129 + 3.129·(rho_v/rho_l)^−0.2186, n = 0.3487 + 0.6513·(rho_v/rho_l)^0.515, α = h·xⁿ/(1 + (h−1)xⁿ) | empirical; annular, 1.05–45.5 mm, macro and microscale |
| `void_fraction_Armand_Treschev` | rho_l, rho_v, x | K = 0.833 + 0.167·x, α = K·α_h | *K·α_h*; steam–water, vertical heated high-pressure |
| `void_fraction_Bankoff` | rho_l, rho_v, x, P | K = 0.71 + 0.0145·(P/1 MPa), α = K·α_h | *K·α_h*; steam–water |
| `void_fraction_Rouhani_Axelsson` | rho_l, rho_v, x, G, sigma | J_l = (1−x)G/rho_l, J_v = xG/rho_v, C0 = 1 + 0.2(1−x), V_drift = 1.18·(9.81·sigma·(rho_l−rho_v)/rho_l²)^0.25 | drift flux; vertical, α > 0.1 |
| `void_fraction_Dix` | rho_l, rho_v, x, G, sigma | C0 = (J_v/(J_l+J_v))(1 + (J_l/J_v)^n), n = (rho_v/rho_l)^0.1, V_drift = 2.9·(…)^0.25 | drift flux; vertical |
| `void_fraction_Woldesemayat_Ghajar` | rho_l, rho_v, x, G, sigma, D, P, theta | Dix C0, V_drift = 2.9·(9.81·sigma·D·(1+cos θ)·(rho_l−rho_v)/rho_l²)^0.25·(1.22 + 1.22·sin θ)^(101325/P) | drift flux; horizontal and upward-inclined only |
| `Re_void`, `We_void` | G, d_hyd, mu / sigma, rho | Re = max(1, G·d_hyd/mu), We = G²·d_hyd/(sigma·rho) | helpers of the original |

Arguments (SI): `rho_l`, `rho_v` saturated liquid and vapour densities
`[kg/m³]`, `x` vapour quality `[-]`, `mu_l`, `mu_v` dynamic viscosities `[Pa·s]`,
`sigma` surface tension `[N/m]`, `d_hyd` hydraulic diameter `[m]` (the pipe
inner diameter for a round pipe), `G` mass flux `[kg/(m²·s)]`, `P` system
pressure `[Pa]`, `D` pipe internal diameter `[m]`, `theta` inclination from the
horizontal `[deg]` (`COS`/`SIN` take degrees in CoolSolve, as in EES).

### Relationship to `CSL-0130`

`CSL-0130` (*pipe_pressure_drop_correlations*, the LaboThapPy `pipe_DP.py`
translation of the same triage batch) already defines `alpha_homogeneous` and
`alpha_Zivi` as helper functions of its two-phase acceleration term. Those two
names are kept here unchanged — same equations, same arguments — so that the
`$INCLUDE library:void_fraction_correlations` resolution of `CS-FEAT-IMPORT`
yields identical values from either entry point; the other eleven models are
new. `Re_void` / `We_void` are likewise the same relations as `Re_pipe` /
`We_pipe` of `CSL-0130`, kept under this model's names so that each file stays
self-contained (the register does not forbid a shared relation under two names,
only under two *different* definitions of the same name).

## How to run

```bash
coolsolve ./void_fraction_correlations.eescode              # native file (Hughmark not solved)
coolsolve ./void_fraction_correlations_coolsolve.eescode   # runnable variant
```

The native file solves with `Solver: SUCCESS (0 iterations)` and reports
`ALL EQUATIONS SATISFIED`, but the ten `alpha_Hughmark[i]` values are the
unsolved guess of the implicit equation (see *Blocking gap*). The variant
solves with `Solver: SUCCESS (40 iterations)` and is the regression baseline
`void_fraction_correlations_coolsolve.sol`.

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies the
definitions in a block `{--- Library functions copied from CSL-0131 ---}` and
lists `CSL-0131` in its `related` field.

## Results

Values of the demonstration program (full precision in the `.sol` files). The
reference is the re-run of the original example (see *Verification*).

Saturated R410A properties at 1.2 MPa (T_sat = 13.346 °C): `rho_l` = 1113.80
kg/m³, `rho_v` = 46.6021 kg/m³, `mu_l` = 1.38901·10⁻⁴ Pa·s, `mu_v` =
1.28820·10⁻⁵ Pa·s, `sigma` = 6.78324·10⁻³ N/m; `Re_l` = 1.72785·10⁴,
`We_l` = 95.2991, `M_dot` = 1.50796·10⁻² kg/s.

Void fractions `alpha [-]` on the quality grid of the original example:

| x | Homog. | Zivi | Fauske | Premoli | L-M | Hughmark | Graham | A-T | Bankoff | R-A | Dix | W-G | C-T |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.05 | 0.5571 | 0.3040 | 0.2046 | 0.4482 | 0.6019 | 0.4249 | 0.4823 | 0.4687 | 0.4052 | 0.4073 | 0.3802 | 0.4764 | 0.5668 |
| 0.15 | 0.8083 | 0.5942 | 0.4632 | 0.6800 | 0.7442 | 0.6572 | 0.6723 | 0.6936 | 0.5880 | 0.6436 | 0.6204 | 0.6969 | 0.7382 |
| 0.25 | 0.8885 | 0.7344 | 0.6197 | 0.7745 | 0.8094 | 0.7376 | 0.7551 | 0.7772 | 0.6463 | 0.7363 | 0.7260 | 0.7866 | 0.8157 |
| 0.35 | 0.9279 | 0.8171 | 0.7247 | 0.8304 | 0.8514 | 0.7796 | 0.8052 | 0.8272 | 0.6750 | 0.7915 | 0.7889 | 0.8391 | 0.8645 |
| 0.45 | 0.9513 | 0.8716 | 0.8000 | 0.8697 | 0.8823 | 0.8068 | 0.8403 | 0.8640 | 0.6920 | 0.8318 | 0.8320 | 0.8750 | 0.8994 |
| 0.55 | 0.9669 | 0.9102 | 0.8566 | 0.9001 | 0.9071 | 0.8270 | 0.8672 | 0.8942 | 0.7033 | 0.8648 | 0.8643 | 0.9020 | 0.9263 |
| 0.65 | 0.9780 | 0.9391 | 0.9008 | 0.9255 | 0.9283 | 0.8441 | 0.8894 | 0.9208 | 0.7114 | 0.8939 | 0.8901 | 0.9237 | 0.9478 |
| 0.75 | 0.9862 | 0.9614 | 0.9362 | 0.9480 | 0.9473 | 0.8607 | 0.9090 | 0.9451 | 0.7174 | 0.9209 | 0.9117 | 0.9421 | 0.9657 |
| 0.85 | 0.9927 | 0.9792 | 0.9652 | 0.9690 | 0.9655 | 0.8800 | 0.9283 | 0.9678 | 0.7221 | 0.9466 | 0.9310 | 0.9588 | 0.9809 |
| 0.95 | 0.9978 | 0.9937 | 0.9893 | 0.9897 | 0.9850 | 0.9151 | 0.9525 | 0.9895 | 0.7258 | 0.9718 | 0.9498 | 0.9757 | 0.9941 |

Branch checks of the demonstration program:

| Case | Quantity | Value |
|---|---|---:|
| Same pipe inclined by 45° (Woldesemayat-Ghajar, x = 0.45) | `alpha_Woldesemayat_Ghajar_45` | 0.872250 |
| Graham below its cutoff (G = 1 kg/m²·s, x = 0.05, F_t = 2.636·10⁻¹ at G = 300) | `alpha_Graham_lowG` | 0 (condensation branch off) |
| Lockhart-Martinelli below the branch cut (x = 0.5, X_tt = 0.2595) | `alpha_LM_low` | 0.895314 |
| Lockhart-Martinelli above it (x = 0.001, X_tt = 129.92) | `alpha_LM_high` | 0.0588920 |

Physical reading: at x = 0.05 the slip-ratio models spread from 0.205 (Fauske,
S ∝ √(rho_l/rho_v), the strongest slip) to 0.602 (Lockhart-Martinelli, which
ignores slip and over-predicts at low quality), the homogeneous model sits at
0.557 between them, and the two *K·α_h* models scale it by K < 1
(Bankoff 0.7274, Armand-Treschev 0.8413 at this pressure). At x = 0.95 all models
except Bankoff — whose pressure factor 0.7274 no longer suits a 1.2 MPa
refrigerant, it was fitted on steam–water — collapse into 0.95–0.998, so the
model choice matters only below about x = 0.8.

## Verification

The card names `void_fraction_example.py` (LaboThapPy commit `f03f7f47`) as the
source's own demonstration. It was re-run in a throw-away virtual environment
under `work/void_fraction/` (`python3 -m venv`, then
`pip install ~/git/LaboThapPy`, which brings CoolProp 8.0.0); the venv has been
deleted with the rest of `work/`. Two scripts, both under `work/`:

- `ref_void_fraction.py` — the original example, unchanged inputs (R410A,
  P = 1.2 MPa, d_hyd = 8 mm, `m_dot = 300·A_cross`, ten qualities from 0.05 to
  0.95), writing `ref_void_fraction.csv`: one row per quality with the thirteen
  void fractions of `compute_void_fraction()`, plus the saturated properties. It
  prints the same table as the original example.
- `compare_void_fraction.py` — matches the 130 table values against a `.sol`
  file (rtol = 10⁻³, the `compare_solution.py` default) and reports the largest
  deviation.

| File | 130 values compared | differing | largest relative deviation |
|---|---:|---:|---|
| `void_fraction_correlations_coolsolve.sol` (variant) | 130 | **0** | 2.203·10⁻⁵ (`void_fraction_Dix`, x = 0.95) |
| `void_fraction_correlations.sol` (native) | 130 | 10 (all `alpha_Hughmark`) | 4.748·10⁻² (Hughmark, x = 0.05) |

`tools/compare_solution.py` is not used directly here: it reads a
`name,value` list or one row of a parametric table, whereas the reference of a
quality sweep is a 10×13 table; `compare_void_fraction.py` is the same
comparison (same rtol and same definition of the relative deviation) written for
that shape, 25 lines, and it is quoted verbatim in the table above.

Deviations below the 10⁻³ tolerance: the largest is 2.2·10⁻⁵ on `Dix` at
x = 0.95, and comes from the surface tension — see the next section. All other
differences are at the 10⁻¹⁶ level (double-precision round-off of the same
arithmetic). Every other model agrees to the last printed digit of the original
table.

Excluded from the comparison: the branch-check variables of the demonstration
program (`alpha_Woldesemayat_Ghajar_45`, `alpha_Graham_lowG`, `alpha_LM_low`,
`alpha_LM_high`), which the original example does not compute, and the
properties themselves (`rho_l`, `rho_v`, `mu_l`, `mu_v`, `sigma`), which agree
to 10⁻¹⁵ between the two runs (same CoolProp backend) except for `sigma`, see
below.

### Surface tension at the state quality

The original obtains `sigma` from `AS.surface_tension()` at the two-phase state
(P, x). CoolProp returns 6.78324·10⁻³ N/m at x = 0 and 6.76719·10⁻³ N/m at
x = 1, interpolated linearly in between, so the value used by the source varies
by 0.24 % over the quality grid. `SURFACETENSION(R410A, T=…, x=…)` returns NaN in
CoolSolve for a two-phase quality (verified: `SURFACETENSION(R410A,T=T_sat,x=0.45)`
fails with *"CoolProp returned invalid result (NaN or Inf) for I(R410A) with
inputs: T=286.496 K, Q=0.45"*), so the model takes the saturated-liquid value at
the saturation temperature, `x = 0`. This is a one-line difference of 0.24 % at
worst in one argument of four correlations (Premoli, Rouhani-Axelsson, Dix,
Woldesemayat-Ghajar) and explains the whole of the 2.2·10⁻⁵ residual: those
correlations carry `sigma` as `sigma^0.25` (drift velocity) or inside `F2`,
so the effect on `alpha` is at the 10⁻⁵ level. It is not a CoolSolve gap — the
property function works as documented on the saturated boundary — and it is
recorded here because the model does not reproduce the source's `sigma(x)`
exactly.

## Blocking gap

**`CS-BUG-IMPLICIT-PROC`** (registered, P1 silent, found while importing
`CSL-0158`): *"An implicit equation in a `FUNCTION`/`PROCEDURE` body that has
other statements is silently not solved: the implicit variable keeps its
guess/default."* This model is the second occurrence, and the first with a
`FUNCTION` rather than a `PROCEDURE`.

`void_fraction_Hughmark` is such a body: `mu_mix = mu_l +
void_fraction_Hughmark*(mu_v - mu_l)` uses the function's own (unknown) result
before the last statement defines it. CoolSolve evaluates the body
procedurally — as the `CS-BUG-COMMON-PROC` note of the register describes —
and the result is the *last statement evaluated with the default guess* rather
than the root, with `SUCCESS` and no warning. Evidence on this build:

- the native file solves with `Solver: SUCCESS (0 iterations)` and
  `coolsolve -d` reports `ALL EQUATIONS SATISFIED` (max residual 5.6·10⁻¹⁷),
  yet `alpha_Hughmark[1]` = 0.446082 instead of 0.424902 (4.7 %);
- the reproducer of the register row applies unchanged to a `FUNCTION`
  (valid EES, deleted with `work/`):

  ```
  FUNCTION fq(r:x)
    g = r*2
    1/SQRT(x) = -2*LOG10(0.001/3.7 + 2.51/(1E5*SQRT(x)))
  END
  x = 0.0175
  z = fq(1)*0
  ```

  → *SUCCESS*, `x` = 0.0175 (EES: 0.0222) — the implicit variable keeps its
  initial value, exactly as in the register row;
- a **single-statement** implicit body does solve (the register already notes
  this), and moving the same Hughmark equations to the main program solves them
  to the root: the 14-equation standalone equivalent of
  `void_fraction_Hughmark` converges in 19 iterations to 0.4249030, i.e. the root
  that both the original `zero_brent` and the variant return.

No new row was registered: the gap is already in §5 of
`CoolSolve/docs/model_library_support.md`, and this model is added there as
further evidence (see *Back-links*). The same analysis applies to the original
Python solver: `zero_brent(1e-6, 1-1e-6, …)` on the residual returns
0.4249024218189828 for x = 0.05, which is the root found here — the source and
the variant agree; only CoolSolve's function-body evaluation does not.

### Runnable variant: `void_fraction_correlations_coolsolve.eescode`

One change, forced by the gap, and it is the workaround the register row itself
recommends ("move the implicit equation and the variables it needs to the main
program and pass the result to the routine"):

| Native | Variant |
|---|---|
| `FUNCTION void_fraction_Hughmark(rho_l, rho_v, x, mu_l, mu_v, d_hyd, G)` — the implicit relation inside the body | `FUNCTION K_Hughmark(alpha, rho_l, rho_v, x, mu_l, mu_v, d_hyd, G)` — returns the explicit correction factor K_h for a given trial void fraction `alpha`; the local names of the body keep their `_H` suffix, the caller's `void_fraction_Hughmark` disappears |
| `alpha_Hughmark[i] = void_fraction_Hughmark(...)` (one statement) | `alpha_hughmark_h[i] = void_fraction_homogeneous(...)` and `alpha_Hughmark[i] = K_Hughmark(alpha_Hughmark[i], ...)*alpha_hughmark_h[i]` — the same relation, written as an equation of the main program, with the homogeneous void fraction named `alpha_hughmark_h[i]` because `alpha_h` is already the local of the `K_Hughmark` body |

Everything else is byte-identical: the other twelve correlations, their comment
blocks, the demonstration inputs, the quality grid and the branch checks. No
CoolSolve-only syntax is used; the variant is valid EES as well (EES solves the
implicit equation of a main program directly). The block sizes stay at 1 (the ten
Hughmark equations form one 5-variable block each), and the whole file converges
in 40 Newton iterations.

### Native file status

`blocked`, with `CS-BUG-IMPLICIT-PROC` in `missing_features`. The other twelve
correlations of the native file are correct — 120 of the 130 compared values
agree within 10⁻³, the ten exceptions being `alpha_Hughmark` — so a model that
needs only, say, the drift-flux correlations can use the native file as it
stands; it is the Hughmark function alone that is affected. Because the file is
a function library whose demonstration program does call Hughmark, the model is
shipped as a whole with the blocked status rather than pretending the native
file runs correctly.

## Source and attribution

- **LaboThapPy** — <https://github.com/PyLaboThap/LaboThapPy>, commit
  `f03f7f47`, module `labothappy/correlations/void_fraction/void_fraction.py`
  (Elise Neven), plus the helpers `compute_reynolds` / `compute_weber` of
  `labothappy/correlations/properties/dimensionless.py` and
  `get_saturated_phase_properties` of
  `labothappy/correlations/properties/two_phase.py`. Licence: the repository
  ships an Apache-2.0 `LICENSE.txt` and declares MIT in `pyproject.toml`; the
  equations of an open-source library are translated, not copied, and this model
  is published under the CoolSolve Library MIT licence (decision D3). The
  original authors are credited in the header of every function.
- **Scientific sources of the correlations**, as named by the module and in each
  function's comment block: S. M. Zivi, *J. Heat Transfer* **86**(2): 247–251,
  1964; H. K. Fauske, ANL-6633, 1962; A. Premoli, D. D. Francesco, A. Prina,
  *La Termotecnica* **25**: 17–26, 1971; R. W. Lockhart, R. C. Martinelli,
  *Chem. Eng. Prog.* **45**(1): 39–48, 1949 (with the Chisholm 1967 closed-form
  approximation actually used); G. A. Hughmark, *Chem. Eng. Prog.* **58**(4):
  62–65, 1962; G. B. Wallis, *One-dimensional two-phase flow*, 1969; V. I.
  Armand and G. G. Treschev (no paper cited by the module); S. G. Bankoff,
  *ASME J. Heat Transfer* **82**: 265–272, 1960; S. Z. Rouhani, E. Axelsson,
  *Int. J. Heat Mass Transfer* **13**: 383–393, 1970; G. E. Dix, PhD thesis,
  Berkeley, 1971 (with Chexal, Horowitz, Lellouche, EPRI NSAC-107, 1986);
  M. A. Woldesemayat, A. J. Ghajar, *Int. J. Multiphase Flow* **33**: 347–370,
  2007; A. Cioncolini, J. R. Thome, *Int. J. Multiphase Flow* **43**: 72–84,
  2012. The module also names R. Dickes, *Charge-sensitive methods for the
  off-design performance characterization of organic Rankine cycle (ORC) power
  systems*, PhD thesis, ULiège, and J. R. Thome, A. Cioncolini, *Void Fraction*,
  Woodhead Publishing Series in Energy, pp. 85–112, 2014 (DOI
  10.1142/9789814623216_0021) as its presentation sources.

## Related models

- `CSL-0130` *pipe_pressure_drop_correlations* — the sibling translation of the
  same batch (`pipe_DP.py`); its two-phase acceleration term uses
  `alpha_homogeneous` / `alpha_Zivi`, and it needs a void fraction for the
  frictional multipliers.
- `CSL-0103` *shell_and_tube_dp* — the only void-fraction-adjacent model the
  library held before this one (shell-and-tube pressure drop, no void fraction).
- `CSL-0121` *heat_transfer_fluid_properties* — property calls for the HTF side
  when the two-phase fluid is a heat-transfer fluid.
- `CSL-0138` *hx_moving_boundary_bell*, `CSL-0113` /
  `CSL-0114` *three-zone plate condenser/evaporator* — two-phase HX models whose
  hold-up and volume estimates can use these correlations.
- `CSL-0132` *r1233zd_thermal_conductivity* — the thermal conductivity of
  R1233zd(E), the other property-correlation translation of the same
  LaboThapPy triage; both models read the saturated densities of their fluid
  from the built-in property functions.

## Back-links

Added to the existing lists, nothing removed or reordered:

- `models/heat_transfer/pressure_drop/pipe_pressure_drop_correlations/model.json`
  and README: `CSL-0131` in `related` (it ships the same homogeneous and Zivi
  void-fraction relations).
- `models/heat_transfer/pressure_drop/pipe_pressure_drop_correlations/README.md`,
  *Relationship to `CSL-0131`* section: the full void-fraction family.

## Conversion log

1. **Physics, not code.** `compute_void_fraction()` is a string dispatcher; it is
   not translated. The caller picks the `FUNCTION` it wants, the convention
   already used by `CSL-0130` for its friction factors and `CSL-0087` for its
   method-dispatch functions. The only thing lost is the single entry point.
2. **The `EPS` clamps are dropped.** Every `max(EPS, …)` of the Python
   (`EPS = 10⁻¹²`) guards a division by a density, a quality or a denominator
   that is non-zero for any physical two-phase state (0 < x < 1, `rho_l` >
   `rho_v`); writing them in EES would add variables without changing a
   physical result. The **quality clip of Hughmark** (`x` to [0.001, 0.95]→
   [0.001, 0.99]) is kept, because the module comments call it a deliberate
   safeguard against the correlation's own asymptotes rather than a
   round-off guard, and it does change results near the ends of the grid.
3. **The output clip `alpha = max(EPS, min(1-EPS, alpha))`** of the dispatcher is
   dropped for the same reason: no correlation of the demonstration case
   returns a value outside (10⁻¹², 1 − 10⁻¹²) — the largest is 0.9978.
4. **`MIN`/`MAX` are used where the Python calls `min`/`max` on a computed
   result** (Lockhart-Martinelli's `min(1, max(0, …))`, Premoli's
   `max(0, ·)` under the square root, `Re_void`'s `max(1, ·)`, the Hughmark
   quality clip, Graham's `min(1, max(0, …))`); both are EES built-ins
   (`ees_vs_coolsolve.csv` line 88–89) and both work in a `FUNCTION` body.
5. **The `theta` argument of Woldesemayat-Ghajar is kept in degrees** and
   `COS`/`SIN` are used directly, since CoolSolve (like EES with its default
   `DEG` setting) evaluates them in degrees (`CS-DOC-TRIG` in the register's
   closed-bugs section documents this). The Python converts with
   `np.radians`; the conversion is the identity for this unit choice and the
   variable meaning is unchanged.
6. **`M_dot` → mass flux `G`.** The Python dispatcher computes
   `G = m_dot/(pi*d_hyd²/4)` from a mass flow rate and a diameter; the functions
   take `G` as an argument, as the Python correlation functions themselves do.
   The demonstration program keeps both, with `G_demo = 300` and
   `M_dot_demo = 300*PI*d_hyd_demo²/4`, so the numbers of the original example
   are reproduced.
7. **`sigma` at the saturation temperature instead of at the quality** — see
   *Verification*.
8. **`COS`/`SIN` in `K_Hughmark`**: none needed; the variant only reorders the
   Hughmark equations (see *Runnable variant*).
9. **Fluid name.** The example uses CoolProp `'R410A'`, which is the EES real
   fluid `R410A` as well — the EES ideal-gas substances are the chemical
   formulas only, so no renaming applies (contrast `CO2` → `R744` in the
   `CSL-0014` translation).
10. **Level.** Taxonomy §3 score: 2 (intermediate) — 13 short algebraic
    correlations, one implicit relation, a property backend and a 10-case sweep
    in the demonstration program; no network, no design loop, no iteration
    variables.

## Notes and open points

- The Lockhart-Martinelli and Hughmark closed forms are, in the module's own
  words, *later curve-fit approximations* of the original papers' chart data
  (Chisholm 1967 for L-M, a polynomial fit for Hughmark), and the homogeneous
  and Armand-Treschev models are presented in the module without a paper. Each
  function's comment block repeats this qualification rather than attributing a
  closed form to the 1949/1962 papers.
- The three other LM regimes (laminar-liquid, laminar-vapour, and the original
  three-parameter parameter) and the `theta` dependency of the drift-flux models
  other than Woldesemayat-Ghajar are not in the source and are not invented
  here.
- `void_fraction_homogeneous` and `void_fraction_Zivi` are the same two
  relations as `alpha_homogeneous` / `alpha_Zivi` of `CSL-0130`, kept under both
  names so that either model can be included on its own. If a future
  `$INCLUDE library:` resolution prefers a single definition, the two pairs can
  be merged without touching an equation.
- Figure placeholder (maintainer, workflow §7 step 2): the parametric tab of the
  CoolSolve GUI, x = `x_demo[1..10]`, y = the thirteen `alpha_*` arrays — the
  comparison the original example plots.

## References

1. E. Neven et al., *LaboThapPy — thermophysical correlations* (ULiège
   Thermodynamics Laboratory), <https://github.com/PyLaboThap/LaboThapPy>,
   commit `f03f7f47`, module
   `labothappy/correlations/void_fraction/void_fraction.py` and its example
   `void_fraction_example.py`.
2. J. R. Thome, A. Cioncolini, *Void Fraction*, Woodhead Publishing Series in
   Energy, pp. 85–112, 2014, DOI [10.1142/9789814623216_0021](https://doi.org/10.1142/9789814623216_0021).
3. R. Dickes, *Charge-sensitive methods for the off-design performance
   characterization of organic Rankine cycle (ORC) power systems*, PhD thesis,
   Université de Liège.
4. S. Quoilin, *CoolSolve Library*, model `CSL-0131`; CoolSolve 0.3.0 build
   `7addbbc`; register `CS-BUG-IMPLICIT-PROC` of
   `CoolSolve/docs/model_library_support.md` §5.
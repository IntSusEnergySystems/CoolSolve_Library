# Shell-and-tube pressure drop: Kern and the Bell-Delaware correction factors

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0103`

Six EES `FUNCTION`s for the shell side of a shell-and-tube heat exchanger: the
pressure drop across the tube bundle by the equivalent-diameter method of Kern,
and the five correction factors of the Bell-Delaware method — baffle
configuration `Jc`, baffle leakage `Jl`, bundle bypassing `Jb`, unequal baffle
spacing `Js` and the laminar-flow correction `Jr` — plus one helper
(`Kern_knot_step`, not a correlation). All arguments are in SI (m, m², kg/s,
Pa·s) or dimensionless; no property call is made inside a function, so the
calling model passes the fluid properties (rule 5 of `sources/ht/README.md` §7).
A sixth correlation of the `ht` family, `dP_Zukauskas`, is **not** translated
(reason in *Limitations*).

| | |
|---|---|
| **Category** | Heat transfer › Pressure drop |
| **Fluids** | none (the correlations are fluid-independent; `m`, `rho`, `mu` are arguments) |
| **Size** | 67 equations after analysis (largest block: 1); 6 correlations + 1 helper of 3–62 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_tube_bank.py` (MIT); inventory row `HT-017` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (23 values, max deviation 3.8·10⁻¹³) |

## Problem statement

The shell side of a shell-and-tube exchanger is a crossflow bundle interrupted
by segmental baffles. Its pressure drop and its heat-transfer coefficient are
not those of an open tube bank: Kern's method works with an *equivalent
diameter* built from the shell flow area, and the Bell-Delaware method corrects
an open-bundle coefficient by five dimensionless factors. Given the mass flow
rate, the fluid properties and the shell geometry (shell diameter, baffle
spacing and count, tube pitch and diameter, leakage and bypass areas), compute
the bundle pressure drop and the five `J` factors.

## Model

| EES `FUNCTION` | Arguments | Equation | Form used |
|---|---|---|---|
| `dP_Kern` | m, rho, mu, mu_w, DShell, LSpacing, pitch, Do, NBaffles | dP = f·(m/Ss)²·DShell·(NB+1) / {2·rho·De·(mu/mu_w)^0.14}, Ss = DShell(pitch−Do)·LSpacing/pitch, De = 4(pitch² − πDo²/4)/(πDo) | exact |
| `Jc_Bell` | Fc, method | Jc = 0.55 + 0.72·Fc | method = 1: Chebyshev fit of the digitized graph; method = 2: HEDH linear fit |
| `Jl_Bell` | Ssb, Stb, Sm | Jl = 0.44(1−r_s) + [1 − 0.44(1−r_s)]·exp(−2.2·r_lm), r_s = Ssb/(Ssb+Stb), r_lm = (Ssb+Stb)/Sm | HEDH curve fit (closed form) |
| `Jb_Bell` | Fsbp, n_seal_strips, n_crossflow_rows, laminar | Jb = exp{−c·Fsbp·[1 − (2z)^(1/3)]}, z = strips/rows, c = 1.35 laminar / 1.25 | HEDH curve fit (closed form) |
| `Js_Bell` | nb, B, B_in, B_out, laminar | Js = {(nb−1) + (B_in/B)^(1−n) + (B_out/B)^(1−n)} / {(nb−1) + B_in/B + B_out/B}, n = 1/3 laminar / 0.6 | exact |
| `Jr_Bell` | Re, total_row_passes | Jr* = (10/N)^0.18, interpolated between Re = 20 and Re = 100, 1 above Re = 100, clipped at 0.4 | exact |

Arguments: `m` (mass flow rate, `[kg/s]`), `rho` (density, `[kg/m³]`), `mu`
(bulk viscosity, `[Pa·s]`), `mu_w` (viscosity at the tube wall temperature,
`[Pa·s]`), `DShell` (shell diameter, `[m]`), `LSpacing` (baffle spacing,
`[m]`), `pitch` (tube pitch, `[m]`), `Do` (tube outside diameter, `[m]`),
`NBaffles` (number of baffles, `[-]`), `Fc` (fraction of the tubes in crossflow
between baffle tips, `[-]`), `Ssb` (shell-to-baffle leakage area, `[m²]`), `Stb`
(total baffle leakage area, `[m²]`), `Sm` (crossflow area, `[m²]`), `Fsbp`
(bypass area fraction, `[-]`), `n_seal_strips` and `n_crossflow_rows` (counts,
`[-]`), `nb` (number of baffles, `[-]`), `B`, `B_in`, `B_out` (baffle spacings,
`[m]`), `Re` (shell Reynolds number of the Bell-Delaware method, `[-]`),
`total_row_passes` (tube rows passed by the fluid, `[-]`), `laminar` and
`method` (flags: 1 or 0 / 1 or 2).

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The scientific basis is
Kern, *Process Heat Transfer*, McGraw-Hill, 1950, and the two Delaware reports
of Kenneth J. Bell (1963 final report, 1988 in Shah et al., *Heat Transfer
Equipment Design*, CRC Press), with the curve fits of the *Heat Exchanger
Design Handbook* (Schlünder, 1987) and of Serth (2014).

The friction factor `f` of the Kern method is read from a graph in the original
book; `ht` fits a cubic B-spline to the digitized points and this file
**reproduces that spline in EES arithmetic** (44 Cox-de Boor basis functions
`B0_i`, `B1_i`, `B2_i`, `B3_i` and the weighted sum `f_Kern`), so no lookup table
is needed inside the function. Zero-length knot intervals (the four repeated
knots at each end) have an identically zero term in the recursion and are
dropped, which leaves the equations mathematically identical to `ht`'s; the four
trailing zero coefficients of the `ht` spline are unused by `scipy` and are not
written out.

## How to run

Open `tube_bank_dp_bell_delaware.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./tube_bank_dp_bell_delaware.eescode
```

The demonstration program after the definitions calls each function twice: once
(case *A*) with the input set of the `ht` doctest of the corresponding
correlation, once (case *B*) with a second input set (8 kg/s of a light oil,
rho = 82 kg/m³, 600 mm shell, 200 mm baffle spacing, 32 mm pitch, 25 mm tubes,
16 baffles, leakage areas of 0.004 / 0.012 / 0.08 m², a bypass fraction of
0.12). Both cases are tabulated against `ht` below. The file solves without any
iteration (`Solver: SUCCESS (0 iterations)`, every equation is explicit) and is
the regression baseline (`tube_bank_dp_bell_delaware.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies the definitions
in a block `{--- Library functions copied from CSL-0103 ---}` and lists
`CSL-0103` in its `related` field.

## Results

Values of the demonstration program (full precision in
`tube_bank_dp_bell_delaware.sol`):

| Quantity (case A) | Value | | Quantity (case B) | Value |
|---|---:|---|---|---:|
| `dP_Kern_A` | 18 980.6 Pa | | `dP_Kern_B` | 23 711.6 Pa |
| `dP_Kern_equalmu_A` | 19 521.4 Pa | | `dP_Kern_equalmu_B` | 22 877.0 Pa |
| `Jc_Bell_A` (Chebyshev) | 1.12472 | | `Jc_Bell_B` | 1.13898 |
| `Jc_Bell_HEDH_A` | 1.14040 | | `Jc_Bell_HEDH_B` | 1.16200 |
| `Jl_Bell_A` | 0.55302 | | `Jl_Bell_B` | 0.76150 |
| `Jb_Bell_A` | 0.84832 | | `Jb_Bell_B` | 0.96129 |
| `Jb_Bell_laminar_A` | 0.83723 | | `Jb_Bell_laminar_B` | 0.95826 |
| `Js_Bell_A` | 0.96401 | | `Js_Bell_B` | 0.98517 |
| `Js_Bell_equal_A` | 1.00000 | | `Js_Bell_equal_B` | 1.00000 |
| `Js_Bell_laminar_A` | 0.97893 | | `Js_Bell_laminar_B` | 0.99125 |
| `Jr_Bell_A` | 0.72680 | | `Jr_Bell_B` | 0.88958 |
| `Jr_Bell_turbulent_A` | 1.00000 | | | |

Sanity checks on those numbers: `Js_Bell_equal = 1` and
`Jr_Bell_turbulent = 1` (a laminar factor is applied only to a laminar shell
flow, and equal baffle spacings need no correction); `Jl_Bell` and `Jb_Bell`
decrease as the leakage area and the bypass fraction grow; `Jc_Bell` stays in
the 1.12–1.16 range quoted by `ht` for a realistic window fraction, and the
Kern pressure drops are a few tens of kPa for a shell-side velocity of
0.49 m/s (case A) and 2.97 m/s (case B).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. the five
     Bell-Delaware factors along the crossflow, or dP_Kern against the
     baffle spacing, figures/tube_bank_dp_bell_delaware_jbell.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_tube_bank.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*. The 23 output values of the demonstration
program were compared with `CoolSolve/tools/compare_solution.py`
(tolerance `rtol = 0.001`):

```
23 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 44
```

(the 44 “only in CoolSolve” variables are the inputs of the demonstration
program — `m_A`, `rho_A`, `mu_A`, `mu_w_A`, `DShell_A`, `LSpacing_A`,
`pitch_A`, `Do_A`, `NBaffles_A`, `Fc_A`, `Ssb_A`, `Stb_A`, `Sm_A`, `Fsbp_A`,
`n_seal_A`, `n_rows_A`, `nb_A`, `B_A`, `B_in_A`, `B_out_A`, `Re_A`, `n_pass_A`
and their twenty-one `_B` counterparts —; the reference table holds only the 23
outputs). The largest relative deviation over the 23 values is **3.8·10⁻¹³**
(`dP_Kern_equalmu_B`), i.e. round-off in the double-precision evaluation.

| Output (case A) | `ht` | CoolSolve | rel. dev. | | Output (case B) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|---|---|---:|---:|---:|
| `dP_Kern_A` | 18980.5876875903 | 18980.58768759 | 1.6e-14 | | `dP_Kern_B` | 23711.6117196364 | 23711.61171964 | 1.5e-13 |
| `dP_Kern_equalmu_A` | 19521.3873864767 | 19521.38738648 | 1.7e-13 | | `dP_Kern_equalmu_B` | 22877.0494766014 | 22877.049476601 | 3.8e-13 |
| `Jc_Bell_A` | 1.12472297015881 | 1.124722970159 | 1.7e-13 | | `Jc_Bell_B` | 1.13898063120896 | 1.138980631209 | 3.5e-14 |
| `Jc_Bell_HEDH_A` | 1.1404 | 1.1404 | 0 | | `Jc_Bell_HEDH_B` | 1.162 | 1.162 | 0 |
| `Jl_Bell_A` | 0.553023626077713 | 0.5530236260777 | 2.4e-14 | | `Jl_Bell_B` | 0.761504402125705 | 0.7615044021257 | 6.6e-15 |
| `Jb_Bell_A` | 0.848321097057910 | 0.8483210970579 | 1.2e-14 | | `Jb_Bell_B` | 0.961290087961428 | 0.9612900879614 | 2.9e-14 |
| `Jb_Bell_laminar_A` | 0.837230592455363 | 0.8372305924554 | 4.5e-14 | | `Jb_Bell_laminar_B` | 0.958258811415100 | 0.9582588114151 | 0 |
| `Js_Bell_A` | 0.964008780280520 | 0.9640087802805 | 2.1e-14 | | `Js_Bell_B` | 0.985172772283677 | 0.9851727722837 | 2.3e-14 |
| `Js_Bell_equal_A` | 1.0 | 1.0 | 0 | | `Js_Bell_equal_B` | 1.0 | 1.0 | 0 |
| `Js_Bell_laminar_A` | 0.978930077456050 | 0.9789300774560 | 5.1e-14 | | `Js_Bell_laminar_B` | 0.991250729392583 | 0.9912507293926 | 1.7e-14 |
| `Jr_Bell_A` | 0.726799545436138 | 0.7267995454361 | 5.2e-14 | | `Jr_Bell_B` | 0.889582289830250 | 0.8895822898302 | 5.6e-14 |
| `Jr_Bell_turbulent_A` | 1.0 | 1.0 | 0 | | | | | |

The three values that are **not** those of the default `ht` method are the ones
the table above already labels: `Jc_Bell_*` is the Chebyshev fit of `ht` (its
own `'chebyshev'` method, which differs from the digitized spline by 0.1% at
Fc = 0.82, well inside the error of the digitization), and `Jl_Bell_*`,
`Jb_Bell_*` are the `'HEDH'` methods of `ht`, whose spline counterparts are
0.5906621 / 0.8469612 (case A) and 0.7603511 / 0.9560945 (case B). Both forms
are published in the same original documents; the choice is logged below.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the shell-side pressure-drop correlations of `ht`, the
heat-transfer component of ChEDL, file `ht/conv_tube_bank.py`, functions
`dP_Kern`, `baffle_correction_Bell`, `baffle_leakage_Bell`,
`bundle_bypassing_Bell`, `unequal_baffle_spacing_Bell` and
`laminar_correction_Bell`, version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named `dP_Kern` or `J<letter>_Bell`, the Python `method` string of
`baffle_correction_Bell` became an integer flag (`1` = Chebyshev fit, `2` =
HEDH fit) and the `method` strings of `baffle_leakage_Bell` and
`bundle_bypassing_Bell` became the HEDH closed form; the Python `laminar`
booleans became 1/0 integer arguments handled by an EES `IF`; the optional
`mu_w` of `dP_Kern` and the optional `baffle_spacing_in` / `baffle_spacing_out`
of `unequal_baffle_spacing_Bell` became mandatory arguments (pass `mu_w = mu`,
or `B_in = B_out = B`, for the forms without the correction), both variants
being exercised in the demonstration program; the Python `math.log`/`**` became
EES `^`, and the spline evaluation `scipy.splev` of the Kern friction factor
became the Cox-de Boor recursion written out in the function body. No equation
was changed.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`): D. Q. Kern (1950),
K. J. Bell (1963, 1988), E. U. Schlünder (1987), R. W. Serth (2014).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-112, family `HT-017`).** One EES
  `FUNCTION` per `ht` correlation (6 + 1 helper), named `dP_Kern` and
  `Jc_Bell` / `Jl_Bell` / `Jb_Bell` / `Js_Bell` / `Jr_Bell`, with the formula,
  the validity range as quoted by `ht`, the original reference and the `ht`
  module/function/version/commit in the comment block. Arguments are the Python
  arguments, in SI (`kg/s`, `kg/m³`, `Pa·s`, `m`, `m²`) or dimensionless; no
  property function is used inside the functions, so the calling model passes
  `m`, `rho` and `mu` itself (rule 5 of `sources/ht/README.md` §7).
- **Digitized curves** (`features` = `table-lookup`; rule 7 of
  `sources/ht/README.md` §7): the friction factor of the Kern method is
  implemented **exactly** as the cubic B-spline of `ht` in EES arithmetic
  (Cox-de Boor), so no table and no `LOOKUP` inside the function is needed
  (`CS-GAP-LOOKUP-PROC` is therefore not hit). For `Jc`, `Jl` and `Jb` the
  **plain forms that the original documents publish** are used: the Chebyshev
  fit of `ht` for `Jc` (its maximum error is 0.142% and its average error
  0.04%, i.e. within the error of the digitization of the graph — `ht` itself
  recommends it over the spline for speed) and the HEDH curve fits for `Jl` and
  `Jb` (`ht` notes they are "rather poor" and "not recommended" but they are
  the closed forms of the *Heat Exchanger Design Handbook*). Both `Jc` methods
  are exposed through the `method` flag and both are exercised in the
  demonstration program, so the user can choose.
- `dP_Zukauskas` is **not translated**: its friction factor and its pitch-ratio
  correction are bivariate splines of four digitized graphs with 104 to 228
  coefficients each (`ht/conv_tube_bank.py`), they have no published closed form
  and `ht` offers no polynomial alternative, so neither a lookup table inside the
  function (`CS-GAP-LOOKUP-PROC`, registered) nor a spline expanded into EES
  equations (several hundred per branch) is acceptable in a function library.
- The boolean options `laminar` are **1/0 integer arguments** and the choice of
  the coefficient is made with an EES `IF` block (a non-smooth regime switch,
  not a function call).
- The conditions of `dP_Kern` are written with the **block** form
  `IF … THEN … ELSE … ENDIF` instead of the single-line `IF (c) THEN a ELSE b`,
  because CoolSolve 0.3.0 evaluates the single-line form wrongly inside a
  `FUNCTION` body (`CS-BUG-IF-SINGLELINE`, registered with a minimal
  reproducer). Both forms are valid EES with the same behaviour, so the native
  file needs no runnable variant.
- **Selectors not translated**: none of the seven functions of the family is a
  dispatcher; `dP_Zukauskas` is excluded for the reason above.
- **Level**: equations 67 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- `dP_Zukauskas` is missing, as described in the *Conversion log*: a model that
  needs the Zukauskas bundle pressure drop must read the friction factor and the
  pitch-ratio correction from its own tables, or use `dP_Kern`.
- The `Jc`, `Jl` and `Jb` functions reproduce the **closed forms** of the
  original documents, not the digitized curves of the default `ht` method: the
  differences are 0.1% (Jc, Chebyshev vs spline), 6.4% and 0.16% at the case-A
  inputs. Use the `method` flag of `Jc_Bell` to compare the two fits, and read
  the *Verification* table before treating a `Jl` / `Jb` value as a spline value.
- The Kern friction factor is only defined on the range of the `ht` spline,
  Re = 9.95 … 1.012·10⁶; outside it the recursion extrapolates the cubic pieces,
  as `scipy.splev` does.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- `CS-BUG-IF-SINGLELINE` (registered by this card, not blocking): the
  single-line `IF (c) THEN a ELSE b` inside a `FUNCTION` body returns the
  `THEN`-branch value whatever the condition. All the conditionals of this file
  use the block form, which is evaluated correctly.

## Related models

- `CSL-0018` *pipe_pressure_drop_colebrook*: the pipe friction factor that a
  model pairing the shell-side drop of this file with a tube-side drop needs.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family of the library
  and the layout followed here (one `FUNCTION` per correlation, per-function
  comment block with the dual citation, demonstration program with case A = the
  `ht` doctest and case B = a second input set).
- `CSL-0095` *tube_bank_nusselt*: the tube-bank Nusselt-number family of the
  same `ht` module; a shell-side model pairs its bundle coefficient with the
  factors of this file.
# Heat exchangers: effectiveness-NTU relations

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0090`

Seventeen EES `FUNCTION`s for the **effectiveness-NTU (ε-NTU) method** of a
heat exchanger: the heat capacity rates `Cmin` and `Cmax`, their ratio `Cr`,
the conversions `NTU = UA/Cmin` and `UA = NTU·Cmin`, and the effectiveness
`eps(NTU, Cr)` with its inverse `NTU(eps, Cr)` for counterflow, parallel
flow, crossflow (both fluids unmixed — exact integral formula and closed
approximate formula; Cmin mixed; Cmax mixed) and boiler/condenser flow
arrangements. All arguments are SI (mass flow rates `[kg/s]`, heat
capacities `[J/kg·K]`, heat capacity rates and `UA` `[W/K]`); `NTU`, `Cr` and
`eps` are dimensionless. Fourth family of the `ht` triage translated for the
library (roadmap card C-99), after `CSL-0087`/`CSL-0088`/`CSL-0089`.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | none (the relations are fluid-independent; the mass flow rates, heat capacities and `UA` are arguments) |
| **Size** | 407 equations after analysis (largest block: 1, all explicit except the two implicit inversions); 17 functions of 1–9 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/hx.py` (MIT); inventory row `HT-004` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the relations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (50 values, 0 differ at rtol = 0.001; max deviation 8.3·10⁻⁸, the quadrature of the exact crossflow integral) |

## Problem statement

A heat exchanger is described by the two heat capacity rates `C_h = ṁ_h·cp_h`
and `C_c = ṁ_c·cp_c` `[W/K]`, by the number of transfer units `NTU = UA/Cmin`
`[-]` and by the flow arrangement. The ε-NTU method gives the effectiveness

> ε = (actual heat duty) / (maximum possible heat duty) = Q / (Cmin·(T_h,i − T_c,i))

as an explicit function of `NTU` and `Cr = Cmin/Cmax`, and conversely `NTU`
as a function of a prescribed ε. Which of the two is given depends on the
problem: sizing an exchanger (ε known, `NTU` to be found) or rating an
existing one (`NTU` known from `UA`, ε to be found). The functions below
cover the arrangements for which a closed form exists, plus the exact and the
approximate formula of the crossflow exchanger with both fluids unmixed.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `calc_Cmin` | ṁ_h, ṁ_c, cp_h, cp_c | Cmin = min(ṁ_h·cp_h, ṁ_c·cp_c) | none quoted |
| `calc_Cmax` | ṁ_h, ṁ_c, cp_h, cp_c | Cmax = max(ṁ_h·cp_h, ṁ_c·cp_c) | none quoted |
| `calc_Cr` | ṁ_h, ṁ_c, cp_h, cp_c | Cr = min(C_h, C_c)/max(C_h, C_c) | none quoted |
| `NTU_from_UA` | UA, Cmin | NTU = UA/Cmin | none quoted |
| `UA_from_NTU` | NTU, Cmin | UA = NTU·Cmin | none quoted |
| `eps_counterflow` | NTU, Cr | ε = {1 − exp[−NTU(1−Cr)]}/{1 − Cr·exp[−NTU(1−Cr)]}; ε = NTU/(1+NTU) if Cr = 1 | 0 ≤ Cr ≤ 1 |
| `eps_parallel` | NTU, Cr | ε = {1 − exp[−NTU(1+Cr)]}/(1+Cr) | 0 ≤ Cr ≤ 1 |
| `eps_crossflow_approx` | NTU, Cr | ε = 1 − exp[(NTU^0.22/Cr)·{exp(−Cr·NTU^0.78) − 1}] | 10⁻⁷ < NTU < 10⁵ for the inversion, 0 < Cr ≤ 1 |
| `eps_crossflow_mixed_Cmin` | NTU, Cr | ε = 1 − exp[−(1/Cr)·{1 − exp(−Cr·NTU)}] | 0 < Cr ≤ 1 |
| `eps_crossflow_mixed_Cmax` | NTU, Cr | ε = (1/Cr)·{1 − exp[−Cr·{1 − exp(−NTU)}]} | 0 < Cr ≤ 1 |
| `eps_boiler_condenser` | NTU | ε = 1 − exp(−NTU) | none quoted |
| `NTU_counterflow` | ε, Cr | NTU = ln[(ε−1)/(ε·Cr−1)]/(Cr−1); NTU = ε/(1−ε) if Cr = 1 | 0 ≤ Cr ≤ 1 |
| `NTU_parallel` | ε, Cr | NTU = −ln[1 − ε(1+Cr)]/(1+Cr) | 0 ≤ Cr ≤ 1; ε(1+Cr) ≤ 1 |
| `NTU_crossflow_mixed_Cmin` | ε, Cr | NTU = −(1/Cr)·ln[Cr·ln(1−ε) + 1] | 0 < Cr ≤ 1; ε ≤ 1 − exp(−1/Cr) |
| `NTU_crossflow_mixed_Cmax` | ε, Cr | NTU = −ln[1 + (1/Cr)·ln(1 − ε·Cr)] | 0 < Cr ≤ 1; ε ≤ [exp(Cr) − 1]·exp(−Cr)/Cr |
| `NTU_boiler_condenser` | ε | NTU = −ln(1 − ε) | none quoted |
| `crossflow_effectiveness_to_int` | v, NTU, t0 | f(v) = (1 + NTU − v²t0)·exp(−v²t0)·v·I₀(v), the integrand of the exact crossflow formula | 0 < Cr ≤ 1 |

Arguments: `m_dot_h`, `m_dot_c` (hot and cold stream mass flow rates,
`[kg/s]`), `Cp_h`, `Cp_c` (averaged heat capacities, `[J/kg·K]`), `UA`
(combined area-heat transfer coefficient term, `[W/K]`), `Cmin` (`[W/K]`),
`NTU` and `Cr` and `effectiveness` (`[-]`), `v` (integration variable of the
exact crossflow formula, `[-]`) and `t0 = 1/(4·Cr·NTU)` (its scaling, `[-]`).

`ht` groups these relations in two dispatchers (`effectiveness_from_NTU`,
`NTU_from_effectiveness`) that select the arrangement by name; each
arrangement is one `FUNCTION` here, named after its `ht` subtype. Every
function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the
`ht` module, function, version and commit it was taken from. The scientific
basis is Incropera, Bergman, Lavine & DeWitt, *Introduction to Heat
Transfer*, 6E, Wiley, 2011; Shah & Sekulic, *Fundamentals of Heat Exchanger
Design*, Wiley, 2002; Holman, *Heat Transfer*, 10th ed., McGraw-Hill, 2009
(the three books `ht` confirms these equations with), and Triboix, *Exact and
Approximate Formulas for Cross Flow Heat Exchangers with Unmixed Fluids*,
Int. Commun. Heat Mass Transfer 36(2): 121–124, 2009 for the exact and
approximate crossflow formulas.

**Not translated** (and why):

- `effectiveness_NTU_method` and `P_NTU_method`: dispatchers that map a method
  name to a relation; an EES caller calls the chosen `FUNCTION` directly.
- The **TEMA E shell-and-tube branches** of the two dispatchers
  (`subtype = 'S&T'`, one to *n* shells in series): they belong to the P-NTU
  / TEMA family of the same triage (card **HT-016**), which is where the TEMA
  temperature-effectiveness relations are translated.
- The **exact inversion** `NTU_from_effectiveness(subtype = 'crossflow')`:
  `ht` runs a Newton iteration on the exact crossflow formula, which needs
  both the modified Bessel function I₀ and the quadrature of the integral —
  neither is available inside an EES function in CoolSolve (see *Limitations*).
  The inverse of the **approximate** crossflow relation is shipped: it has no
  closed form either, so the demonstration program writes `NTU` as an unknown
  of the effectiveness equation (as `ht` itself solves it with a
  secant/bisection solver).

## How to run

Open `hx_effectiveness_ntu.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./hx_effectiveness_ntu.eescode
```

The demonstration program after the definitions calls each of the 17
functions, twice:

- case *A* uses the input set of the `ht` doctests (NTU = 5, Cr = 0.7,
  ṁ_h = 22 kg/s, cp_h = 2200 J/kg·K, ṁ_c = 5.5 kg/s, cp_c = 4400 J/kg·K,
  UA = 4400 W/K, Cmin = 22 W/K) plus the `Cr = 1` limit of the two singular
  counterflow expressions;
- case *B* is the steam/oil crossflow rating of the `ht` docstring
  (ṁ_steam = 5.2 kg/s, cp_steam = 1860 J/kg·K, ṁ_oil = 0.725 kg/s,
  cp_oil = 1900 J/kg·K, U = 275 W/m²·K, A = 10.82 m², from which
  NTU = UA/Cmin = 2.160 and Cr = 0.1424).

It solves in 13 iterations without any guess file and is the regression
baseline (`hx_effectiveness_ntu.sol`). The only iterative part is the two
implicit inversions of the approximate crossflow relation (`NTU` as an
unknown); everything else is explicit.

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these relations copies their
definitions in a block `{--- Library functions copied from CSL-0090 ---}` and
lists `CSL-0090` in its `related` field.

## Results

Values of the demonstration program (full precision in
`hx_effectiveness_ntu.sol`):

| Quantity (case A) | value | Quantity (case B) | value |
|---|---:|---|---:|
| `calc_Cmin` | 24 200 W/K | | 1377.5 W/K |
| `calc_Cmax` | 48 400 W/K | | 9672 W/K |
| `calc_Cr` | 0.5 | | 0.14242 |
| `NTU_from_UA` (UA = 4400 W/K, Cmin = 22 W/K) | 200 | (UA = 2975.5 W/K) | 2.16007 |
| `UA_from_NTU` | 4400 W/K | | 2975.5 W/K |
| `eps_counterflow` | 0.92067 | | 0.86241 |
| `eps_parallel` | 0.58812 | | 0.80112 |
| `eps_crossflow` (exact, Simpson quadrature) | 0.84448 | | 0.84616 |
| `eps_crossflow_approx` | 0.84448 | | 0.85079 |
| `eps_crossflow_mixed_Cmin` | 0.74978 | | 0.84424 |
| `eps_crossflow_mixed_Cmax` | 0.71581 | | 0.83122 |
| `eps_boiler_condenser` | 0.99326 | | 0.88468 |
| `NTU_counterflow` | 5 | | 2.16007 |
| `NTU_parallel` | 5 | | 2.16007 |
| `NTU_crossflow_approx` | 5 | | 2.16007 |
| `NTU_crossflow_mixed_Cmin` | 5 | | 2.16007 |
| `NTU_crossflow_mixed_Cmax` | 5 | | 2.16007 |
| `NTU_boiler_condenser` | 5 | | 2.16007 |
| `eps_counterflow` at Cr = 1 | 0.83333 | | 0.68355 |
| `NTU_counterflow` at Cr = 1 | 5 | | 2.16007 |
| integral term I_int of the exact crossflow formula | 473.888 | | 1.58993 |

The effectiveness increases from parallel flow through the crossflow
arrangements to counterflow, as expected (for the same NTU and Cr): in case A
0.588 < 0.716 < 0.750 < 0.844 ≈ 0.844 < 0.921, and the boiler/condenser case
(ε = 0.993 at NTU = 5) is the best of all because the condensing stream is
isothermal. The `Cr = 1` line uses the limiting expression NTU/(1+NTU)
(0.8333 at NTU = 5) instead of the singular closed form, and the exact
crossflow value (0.84448) agrees with the approximate closed form
(0.84448) to 2·10⁻⁶ relative in case A (0.844 482 2 against
0.844 480 4), as the two formulas of Triboix should.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the six
     effectiveness curves eps(NTU) at Cr = 0.7 and 0.1424 (parallel, mixed
     Cmin, mixed Cmax, exact and approximate crossflow, counterflow, boiler),
     figures/hx_effectiveness_ntu_eps_ntu.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/hx.py`, commit `85e0ee6`, installed from the local clone in a throw-away
virtual environment) for case *A*, plus values computed with the same Python
functions for the same case *A* calls and for case *B*. The 50 output values
of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
50 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 357
```

(the 357 “only in CoolSolve” variables are the 17 inputs of the
demonstration program, the 324 elements of the two quadrature arrays
`v_A[i]`/`f_A[i]` and `v_B[i]`/`f_B[i]`, the 8 quadrature scalars
`h_int`, `I_odd`, `I_even`, `I_int` of each case and the 8 point values
`v_eval_*`; the reference table holds the 50 outputs of the relations only).

The largest relative deviation over the 50 values is **8.3·10⁻⁸**
(`eps_crossflow_B`), and **1.4·10⁻⁸** on `eps_crossflow_A`: it is the
truncation error of the composite Simpson quadrature (80 intervals) of the
exact crossflow integral, not a difference of equations — `ht` integrates with
an adaptive quadrature and CoolSolve has no quadrature function (§*Limitations*
below). Over the other **48** values the largest relative deviation is
**5.1·10⁻¹⁰**, on `NTU_crossflow_approx_A`: it is the convergence tolerance of
the implicit inversion (`ht` runs a secant solver, CoolSolve solves the same
equation simultaneously and returns 4.999 999 997 instead of 5). The other 47
values agree to **3.1·10⁻¹³** (`crossflow_effectiveness_to_int_A_v6`) or
better, i.e. round-off in the double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `calc_Cmin` | 24200 | 24200 | 0 |
| `calc_Cmax` | 48400 | 48400 | 0 |
| `calc_Cr` | 0.5 | 0.5 | 0 |
| `NTU_from_UA` | 200 | 200 | 0 |
| `UA_from_NTU` | 4400 | 4400 | 0 |
| `eps_counterflow` | 0.920670368605 | 0.920670 | 1.2e-14 |
| `eps_parallel` | 0.588115606842 | 0.588116 | 7.1e-14 |
| `eps_crossflow` (exact) | 0.844482179975 | 0.844482 | 1.4e-08 |
| `eps_crossflow_approx` | 0.844480448191 | 0.844480 | 5.5e-14 |
| `eps_crossflow_mixed_Cmin` | 0.749784394151 | 0.749784 | 6.1e-14 |
| `eps_crossflow_mixed_Cmax` | 0.715809983120 | 0.715810 | 4.2e-14 |
| `eps_boiler_condenser` | 0.993262053001 | 0.993262 | 1.5e-14 |
| `NTU_counterflow` | 5.0 | 5.0 | 0 |
| `NTU_parallel` | 5.0 | 5.0 | 2.5e-15 |
| `NTU_crossflow_approx` | 5.0 | 5.0 | 3.6e-16 |
| `NTU_crossflow_mixed_Cmin` | 5.0 | 5.0 | 8.9e-16 |
| `NTU_crossflow_mixed_Cmax` | 5.0 | 5.0 | 3.6e-15 |
| `NTU_boiler_condenser` | 5.0 | 5.0 | 1.8e-16 |
| `eps_counterflow` (Cr = 1) | 0.833333333333 | 0.833333 | 4.0e-14 |
| `NTU_counterflow` (Cr = 1) | 5.0 | 5.0 | 3.6e-16 |
| `crossflow_effectiveness_to_int` (v = 0.5) | 3.12465612414 | 3.12466 | 2.1e-14 |
| `crossflow_effectiveness_to_int` (v = 2) | 19.5777896267 | 19.5778 | 5.3e-14 |
| `crossflow_effectiveness_to_int` (v = 3.5) | 55.1702393194 | 55.1702 | 5.8e-14 |
| `crossflow_effectiveness_to_int` (v = 6) | 105.705793712 | 105.706 | 3.1e-13 |

Case *B* (NTU = 2.1600726, Cr = 0.1424214, computed with the same Python
functions):

| Function | `ht` | CoolSolve | Function | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|
| `calc_Cmin_B` | 1377.5 | 1377.5 | `NTU_parallel_B` | 2.160073 | 2.160073 |
| `calc_Cmax_B` | 9672 | 9672 | `NTU_crossflow_approx_B` | 2.160073 | 2.160073 |
| `calc_Cr_B` | 0.1424214 | 0.142421 | `NTU_crossflow_mixed_Cmin_B` | 2.160073 | 2.160073 |
| `NTU_from_UA_B` | 2.160073 | 2.160073 | `NTU_crossflow_mixed_Cmax_B` | 2.160073 | 2.160073 |
| `UA_from_NTU_B` | 2975.5 | 2975.5 | `NTU_boiler_condenser_B` | 2.160073 | 2.160073 |
| `eps_counterflow_B` | 0.8624106 | 0.862411 | `eps_counterflow_Cr1_B` | 0.683552 | 0.683552 |
| `eps_parallel_B` | 0.8011242 | 0.801124 | `crossflow_effectiveness_to_int_B_v01` | 0.313426 | 0.313426 |
| `eps_crossflow_B` (exact) | 0.8461629 | 0.846163 | `crossflow_effectiveness_to_int_B_v05` | 1.283242 | 1.283242 |
| `eps_crossflow_approx_B` | 0.8507863 | 0.850786 | `crossflow_effectiveness_to_int_B_v1` | 1.318641 | 1.318641 |
| `eps_crossflow_mixed_Cmin_B` | 0.8442363 | 0.844236 | `crossflow_effectiveness_to_int_B_v2` | −0.015985 | −0.015985 |
| `eps_crossflow_mixed_Cmax_B` | 0.8312180 | 0.831218 | | | |
| `eps_boiler_condenser_B` | 0.8846833 | 0.884683 | | | |
| `NTU_counterflow_B` | 2.160073 | 2.160073 | | | |

The quadrature truncation error was checked independently in Python (same
composite Simpson rule, 80 intervals, against `scipy.integrate.quad`): 1.4·10⁻⁸
in case A and 8.3·10⁻⁸ in case B on ε, i.e. the whole deviation is explained
by the quadrature.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the effectiveness-NTU relations of `ht`, the
heat-transfer component of ChEDL, file `ht/hx.py`, functions `calc_Cmin`,
`calc_Cmax`, `calc_Cr`, `NTU_from_UA`, `UA_from_NTU`,
`effectiveness_from_NTU`, `NTU_from_effectiveness` and
`crossflow_effectiveness_to_int`, version 1.2.0, commit 85e0ee6
(2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; each flow arrangement of the
two `ht` dispatchers became one EES `FUNCTION` named after its `ht` subtype
(`eps_counterflow`, `eps_parallel`, `eps_crossflow_approx`,
`eps_crossflow_mixed_Cmin`, `eps_crossflow_mixed_Cmax`,
`eps_boiler_condenser` and the five `NTU_*` inverses), the `min`/`max` of
`calc_Cmin`/`calc_Cmax`/`calc_Cr` became `IF` branches, the singular
`Cr = 1` case of the counterflow relations became an `IF` with the limiting
expression of the original, the Python `log` became the EES `LN`, and the
modified Bessel function I₀(v) of the exact crossflow integrand is evaluated
by its power series (25 terms, `DUPLICATE` loop inside the function body)
because CoolSolve has no Bessel function. No equation was changed. The
`ht` name `subtype` string became a separate function per arrangement; the
Python default `subtype = 'counterflow'` therefore has no counterpart (the
caller chooses the function).

The scientific authors are credited in the comment block of each function and
in `model.json` (`origin.authors`).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-99, family `HT-004`).** The two
  `ht` dispatchers were split into one EES `FUNCTION` per flow arrangement
  (11 effectiveness/inverse functions), the five "trivial" relations
  (`calc_Cmin`, `calc_Cmax`, `calc_Cr`, `NTU_from_UA`, `UA_from_NTU`) kept
  their `ht` names, and the eighth `ht` function of the family
  (`crossflow_effectiveness_to_int`, the integrand of the exact crossflow
  formula) became a `FUNCTION` with the I₀ power series. 17 functions in all,
  each with the formula, the validity range as quoted by `ht`, the original
  reference and the `ht` module/function/version/commit in its comment block.
  Arguments are the Python arguments, in SI (`kg/s`, `J/kg·K`, `W/K`); no
  property function is used inside a function, so the calling model passes the
  mass flow rates, heat capacities and `UA` itself (rule 5 of
  `sources/ht/README.md` §7).
- **`effectiveness_from_NTU` / `NTU_from_effectiveness`**: these are
  dispatchers on a `subtype` string; EES has no string arguments here, so
  each branch is a separate `FUNCTION`. The two non-smooth points of the
  original (the `Cr = 1` limit of the counterflow relations, `min`/`max` of
  the heat capacity rates) use an EES `IF`, never a function call.
- **`NTU_from_effectiveness(subtype = 'crossflow')` and
  `'crossflow approximate'`**: `ht` solves them with `secant`/bisection. In
  EES the inversion is written as a simultaneous equation with `NTU` as the
  unknown (`NTU_crossflow_approx_A = eps_crossflow_approx(NTU_crossflow_approx_A, Cr_A)`
  is written with the known effectiveness on the left); this is the same
  prescription as the ht triage gives for the P-NTU inversions of card HT-016.
  The exact-crossflow inversion is **not** shipped: it would need the
  quadrature of the integral *and* a Newton step inside the same equation, so
  it is documented as a limitation instead of being approximated.
- **Exact crossflow effectiveness**: `ht` calls `scipy.integrate.quad` on the
  integrand. CoolSolve has no quadrature function and no reduction of a
  `DUPLICATE` array (`sum(array)` returns the array itself, which is then an
  unmatched variable), so the demonstration program performs a composite
  Simpson rule with 80 intervals over the array `f[i]` of the integrand and
  writes the odd and even partial sums out explicitly. The I₀(v) power series
  inside the function needs a `DUPLICATE` loop in a function body (supported,
  and derivative-propagating).
- **Level**: equations 407 → 2 points (300–1500), largest block 1 → 0,
  functions and `DUPLICATE` arrays present → 1, multi-zone no → 0,
  semi-empirical/off-design no → 0, curated guesses no → 0 (the file solves
  without a `.initials`). Score 3 → **level 2**.

## Limitations and CoolSolve gaps

- **No quadrature, no Bessel function in CoolSolve.** The exact effectiveness
  of a crossflow exchanger with both fluids unmixed needs I₀(v) (evaluated
  here by its power series) *and* a definite integral. The function can
  therefore return the integrand only, and the caller has to integrate it
  (composite Simpson rule in the demonstration program, 8·10⁻⁸ relative error
  for the two cases). Two unverified suggestions for the maintainer, **not
  registered** (no EES manual reference gathered): a general quadrature of a
  user function, and the modified Bessel functions `i0`/`i1`/`k0`/`k1`/`iv`
  (the evaluator has no Bessel dispatch; the ht triage already flagged the
  Bessel functions as an open question for the B-09 cards, and the P-NTU
  crossflow term of card HT-016 needs them too).
- **Array reduction**: `sum(array)` over a `DUPLICATE`-generated array leaves
  the whole array as an unmatched variable, so a `DUPLICATE` loop cannot
  accumulate a sum; only explicit element sums work. The same limitation
  forces the long `I_odd`/`I_even` equations. Also an unverified suggestion.
- The `ht` functions raise an error for `Cr > 1` (by definition) and for an
  effectiveness above the maximum of an arrangement; the EES functions do not
  check their arguments and return the value of the closed form (as in the
  library convention for the other `ht` families). The maximum effectiveness
  of each arrangement is quoted in the validity line of the function.
- `eps_crossflow_approx` and the two mixed-crossflow relations are singular at
  `Cr = 0`; the original has the same limitation for these subtypes (the
  `1 - exp(-NTU)` form of a latent-heat exchanger is available as
  `eps_boiler_condenser`).
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  relations copies the definitions for now.
- No gap registered for this card: the file is plain EES
  (`FUNCTION`, `IF/THEN/ELSE`, `LN`, `EXP`, `DUPLICATE`) and runs in
  CoolSolve v0.3.0.

## Related models

- `CSL-0112` *three_zone_hx_procedures*: the counterflow eps-NTU and the
  latent-heat `eps = 1 - exp(-NTU)` relations of this file, as they are used
  inside the three-zone condenser/evaporator procedures of a heat exchanger
  that splits its surface into zones.

- `CSL-0096` *plate_hx_heat_transfer*: the plate-heat-exchanger heat-transfer
  coefficients (single-phase Nu and flow boiling) that a plate rating model
  combines with the effectiveness-NTU relations of this file.
- `CSL-0002` *counterflow_hx_oil_water*, `CSL-0026`
  *crossflow_hx_hot_gas_water*, `CSL-0027`
  *shell_and_tube_steam_condenser*: three eps-NTU heat-exchanger models that
  apply exactly these relations to real fluids and real temperatures; they
  copy the definitions of this file (`related` back-link).
- `CSL-0087` *internal_turbulent_nusselt*, `CSL-0088`
  *nucleate_boiling_and_chf*, `CSL-0089` *condensation_film*: the other
  families of the same `ht` triage, same layout (definitions + demonstration
  program of two cases).
- `CSL-0005` *cpbar_combustion_products* and `CSL-0079`
  *brineprop_secondary_refrigerants*: the two older function libraries of the
  library (same layout).
- `sources/ht` HT-016 (P-NTU / TEMA temperature effectiveness, including the
  shell-and-tube branches left out of this file) and HT-019 (LMTD and the
  F/Ft correction factors): the other heat-exchanger families of the same
  triage.
- `sources/thermo_models` TSP-030 (TESPy eps-NTU relations, cross-validated
  against `ht` by the TESPy test suite) and `sources/labothappy` LTP-014 /
  LTP-042 (LaboThapPy eps-NTU with geometry and F-LMTD): the same relations
  in other tools; keep both, the `ht` family is the reference for the
  equations.
- `CSL-0094` *external_crossflow_cylinder*: the single-cylinder crossflow
  Nusselt numbers (Zukauskas, Churchill-Bernstein, Sanitjai-Goldstein,
  Whitaker, Perkins-Leppert, 8 functions), the other family of the same `ht`
  triage, same layout; they give the single-stream side of a crossflow
  exchanger.
- `CSL-0097` *two_phase_nonboiling_in_tube*: the two-phase non-boiling
  in-tube heat-transfer coefficients of the same `ht` triage (9 functions),
  same layout; together with the relations of this file they rate a
  condenser or an evaporator.
- `CSL-0098` *flow_boiling_in_tubes*: the in-tube flow-boiling
  coefficients (10 functions), same layout; together with the relations of this
  file they rate a boiler or an evaporator.
- `CSL-0105` *lmtd_and_f_correction*: the LMTD relations of the same `ht`
  triage (`LMTD`, `F_LMTD_Fakheri`, `Ft_aircooler`, same layout); a rating
  model uses either the ε-NTU method of this file or the LMTD method of that
  one.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
- `CSL-0126` *hx_constant_effectiveness*: a constant-effectiveness exchanger
  with an *enthalpy-based* `Q_max` (no area, no ε-NTU inversion); the relations
  of this file size or rate the duty that model computes.

- `CSL-0128` *hx_eps_ntu_plate_pipe*: translation of the LaboThapPy
  `HexeNTU` component, whose `e_NTU` relations (counter, parallel, crossflow
  unmixed and mixed, 1-2 and n-pass shell-and-tube) are the same closed forms
  as `eps_counterflow`, `eps_parallel`, `eps_crossflow_approx` and
  `eps_crossflow_mixed_Cmin` of this file; the model computes the
  conductance-area product from a plate geometry and calls its own copy of the
  relations.
- `CSL-0127` *hx_constant_effectiveness_discretised* (level 4): the imposed
  effectiveness taken to its discretised, pinch-limited form (`HexCstEffDisc`,
  LaboThapPy): the duty is additionally bounded by a minimum segment
  temperature difference and by an internal zero-pinch limit.

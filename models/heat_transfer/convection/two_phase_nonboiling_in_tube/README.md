# In-tube two-phase non-boiling heat-transfer coefficients

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0097`

Nine EES `FUNCTION`s returning the forced-convection heat-transfer coefficient
of a liquid and a gas flowing inside a tube **without phase change**
(condensing or evaporating), the classic ratings of a condenser or an
evaporator tube: Davis-David, Elamvaluthi-Srinivas, Groothuis-Hendal, Hughmark,
Knott, Kudirka-Grosh-McFadden, Martin-Sims, Ravipudi-Godbold and Aggour. All
of them return h_tp in W/m²/K from the mass flow rate, the quality and the
properties of the liquid and of the gas; **no property function is called
inside a function** (rule 5 of `sources/ht/README.md` §7), so the calling model
evaluates the properties itself and passes them as arguments. The family is
the ninth `ht` family of the library (roadmap cards C-96…C-119) and follows the
layout of `CSL-0087`: one `FUNCTION` per correlation, a comment block per
function with the formula, the validity range and the dual citation, and a
demonstration program calling every function.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; the two-phase properties are arguments) |
| **Size** | 65 equations after analysis (largest block: 1); 9 functions of 31–56 lines, most of it comment block |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_two_phase.py` (MIT); inventory row `HT-011` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (37 values, max deviation 4.0·10⁻¹²) |

## Problem statement

For a two-phase liquid-gas mixture flowing inside a tube (mass flow rate `m`,
quality `x`, tube diameter `D`, length `L`, void fraction `alpha`) at given
liquid and gas properties, compute the two-phase forced-convection
heat-transfer coefficient h_tp [W/m²/K] that a condenser or evaporator rating
needs. Nine historical correlations are available for that, each developed on
a different flow pattern, geometry and fluid pair, each with its own validity
range; the choice between them is left to the user, who knows the fluid, the
geometry and the flow regime.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `h_Davis_David` | m, x, D, rhol, rhog, Cpl, kl, mul | h·D/kl = 0.060·(rho_l/rho_g)^0.28·(D·G·x/mu_l)^0.87·Pr_l^0.4, G = m/(π/4·D²) | vertical and horizontal flow, annular and mist annular patterns; steam-water and air-water only, quality 0.1 to 1; AAE 17 % |
| `h_Elamvaluthi_Srinivas` | m, x, D, rhol, rhog, Cpl, kl, mug, mu_b, mu_w | h·D/kl = 0.5·(mu_g/mu_l)^0.25·Re_M^0.7·Pr_l^(1/3)·(mu_b/mu_w)^0.14 | vertical flow, bubbly and slug patterns; gas/liquid superficial velocity ratio 0.3–4.6, liquid mass flux 200–1600 kg/m²·s⁻¹, Di = 1 cm, L/D = 86 |
| `h_Groothuis_Hendal` | m, x, D, rhol, rhog, Cpl, kl, mug, mu_b, mu_w, water | h·D/kl = 0.029·Re_M^0.87·Pr_l^(1/3)·(mu_b/mu_w)^0.14 (air-water, `water` = 1) or 2.6·Re_M^0.39·Pr_l^(1/3)·(mu_b/mu_w)^0.14 (gas / air-oil, `water` = 0) | vertical pipes, superficial velocity ratio 0.6–250; air-water and gas / air-oil |
| `h_Hughmark` | m, x, alpha, D, L, Cpl, kl, mu_b, mu_w | h·D/kl = 1.75·(1-alpha)^(-0.5)·{m_l·Cpl/[(1-alpha)·kl·L]}^(1/3)·(mu_b/mu_w)^0.14 | horizontal pipes, laminar slug flow; air-water, air-SAE 10 oil, gas-oil, air-diethylene glycol, air-aqueous glycerine |
| `h_Knott` | m, x, D, rhol, rhog, hl | h/h_l = (1 + V_gs/V_ls)^(1/3) | none quoted |
| `h_Kudirka_Grosh_McFadden` | m, x, D, rhol, rhog, Cpl, kl, mug, mu_b, mu_w | Nu = 125·(V_gs/V_ls)^0.125·(mu_g/mu_l)^0.6·Re_ls^0.25·Pr_l^(1/3)·(mu_b/mu_w)^0.14 | air-water and air-ethylene glycol, L/D = 17.6, low gas-liquid ratios; bubble, slug and froth flow |
| `h_Martin_Sims` | m, x, D, rhol, rhog, hl | h/h_l = 1 + 0.64·(V_gs/V_ls)^0.5 | none quoted |
| `h_Ravipudi_Godbold` | m, x, D, rhol, rhog, Cpl, kl, mug, mu_b, mu_w | Nu = 0.56·(V_gs/V_ls)^0.3·(mu_g/mu_l)^0.2·Re_ls^0.6·Pr_l^(1/3)·(mu_b/mu_w)^0.14 | vertical pipe, superficial gas/liquid velocity ratio 1–90, froth regime; air-water, toluene, benzene, methanol |
| `h_Aggour` | m, x, alpha, D, rhol, Cpl, kl, mu_b, mu_w, L, turbulent | laminar (Re_l ≤ 2000): h = 1.615·(kl/D)·(Re_l·Pr_l·D/L)^(1/3)·(mu_b/mu_w)^0.14·(1-alpha)^(-1/3); turbulent: h = 0.0155·(kl/D)·Re_l^0.83·Pr_l^0.5·(1-alpha)^(-0.83) | vertical tests, air-water / helium-water / freon-12-water; bubbly, slug, annular, bubbly-slug, slug-annular; superficial velocity ratio 0.02–470 |

With the superficial velocities
V_ls = m·(1-x)/(rho_l·π/4·D²) and V_gs = m·x/(rho_g·π/4·D²), the Prandtl number
Pr_l = Cpl·mu_b/kl, Re_M = D·V_ls·rho_l/mu_b + D·V_gs·rho_g/mu_g,
Re_ls = D·V_ls·rho_l/mu_b and, for `h_Aggour`, Re_l = rho_l·V_l·D/mu_l with
V_l = V_ls/(1-alpha).

Arguments: `m` (mass flow rate, `[kg/s]`), `x` (quality, `[-]`), `D` (tube
diameter, `[m]`), `L` (tube length, `[m]`), `alpha` (void fraction, `[-]`),
`rhol`/`rhog` (densities of the liquid and of the gas, `[kg/m³]`), `Cpl`
(constant-pressure heat capacity of the liquid, `[J/kg·K]`), `kl` (thermal
conductivity of the liquid, `[W/m·K]`), `mul`, `mug`, `mu_b`, `mu_w`
(viscosities: of the liquid, of the gas, of the liquid at bulk conditions and
of the liquid at the wall temperature, `[Pa·s]`), `hl` (liquid-phase
heat-transfer coefficient, `[W/m²/K]`, `h_Knott` and `h_Martin_Sims` only),
`water` and `turbulent` (flags, `[-]`).

`h_Knott` and `h_Martin_Sims` take `hl` as an input. In the original, `hl` is
optional and is then computed with the Sieder-Tate laminar thermal entry
correlation `Nu_l = 1.86·(Di/L·Re·Pr)^(1/3)·(mu_b/mu_w)^0.14` with Re and Pr of
the liquid taken on the **combined superficial velocity** V_ls + V_gs; that
correlation belongs to another family (laminar internal convection, `HT-005`),
so the caller passes `hl`. Its equation is repeated in the comment block of
both functions and the demonstration program applies it, which reproduces the
published values of the two correlations.

Every function carries in its comment block (i) the equation, (ii) the
validity range **as quoted by `ht`**, (iii) the original paper or thesis and
(iv) the `ht` module, function, version and commit it was taken from. The
scientific basis is, for all nine correlations, the original paper (Groothuis
& Hendal 1959, Knott, Anderson, Acrivos & Petersen 1959, Hughmark 1965,
Kudirka, Grosh & McFadden 1965, Davis & David 1964, Martin & Sims 1971,
Ravipudi & Godbold 1978, Elamvaluthi & Srinivas 1984, Aggour's Ph.D. thesis
1978), as reviewed by Kim, D., V. K. Ryali, A. J. Ghajar and R. L. Dougherty,
*Comparison of 20 Two-Phase Heat Transfer Correlations with Seven Sets of
Experimental Data, Including Flow Pattern and Tube Inclination Effects*, Heat
Transfer Engineering 20(1): 15-40, 1999.

Two members of the `ht` family are **not** translated: `h_two_phase` and
`h_two_phase_methods` are dispatchers that map a method name to a correlation
(and, in `ht`, list the correlations applicable to a given set of inputs); an
EES caller calls the chosen `FUNCTION` directly.

## How to run

Open `two_phase_nonboiling_in_tube.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./two_phase_nonboiling_in_tube.eescode
```

The demonstration program after the definitions calls each of the 9 functions
twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation, once (case *B*) with a single uniform input set
(m = 0.2 kg/s, x = 0.35, D = 0.02 m, L = 2 m, alpha = 0.6, rho_l = 800 kg/m³,
rho_g = 20 kg/m³, Cpl = 1500 J/kg·K, kl = 0.12 W/m·K, mul = 2.8·10⁻⁴ Pa·s,
mug = 1.2·10⁻⁵ Pa·s, mu_b = 2.5·10⁻⁴ Pa·s, mu_w = 2.2·10⁻⁴ Pa·s). It solves
without any iteration (`Solver: SUCCESS (0 iterations)`, every equation is
explicit) and is the regression baseline
(`two_phase_nonboiling_in_tube.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0097 ---}` and
lists `CSL-0097` in its `related` field.

## Results

Values of the demonstration program (full precision in
`two_phase_nonboiling_in_tube.sol`):

| Quantity (case A) | h_tp [W/m²·K⁻¹] | Quantity (case B) | h_tp [W/m²·K⁻¹] |
|---|---:|---|---:|
| `h_Davis_David` | 1437.33 | | 7552.49 |
| `h_Elamvaluthi_Srinivas` | 3901.21 | | 17578.07 |
| `h_Groothuis_Hendal` (gas / air-oil, `water` = 0) | 1192.95 | | 3568.87 |
| `h_Groothuis_Hendal_water` (air-water, `water` = 1) | 6362.90 | | 19555.04 |
| `h_Hughmark` | 212.74 | | 214.05 |
| `h_Knott` | 4225.54 | | 916.85 |
| `h_Kudirka_Grosh_McFadden` | 303.99 | | 3573.97 |
| `h_Martin_Sims` (hl = 141.2 W/m²·K⁻¹ prescribed) | 5563.28 | | |
| `h_Martin_Sims` (hl computed, L = 24 m) | 5977.51 | (hl computed, L = 2 m) | 1288.65 |
| `h_Ravipudi_Godbold` | 299.38 | | 3525.37 |
| `h_Aggour` (Re_l = 4244 → turbulent) | 420.93 | (Re_l = 8.28·10⁴ → turbulent) | 4246.11 |
| `h_Aggour_laminar` (laminar forced) | 144.97 | (laminar forced) | 183.78 |

Intermediate quantities of the demonstration program:

| Quantity | case A | case B |
|---|---:|---:|
| `V_ls` (superficial liquid velocity) [m/s] | 1.4147·10⁻³ | 0.51725 |
| `V_gs` (superficial gas velocity) [m/s] | 5.0930 | 11.1408 |
| `Re_l` (liquid Reynolds number on V_ls + V_gs) [−] | 1.5283·10⁶ | 7.4612·10⁵ |
| `Pr_l` (liquid Prandtl number) [−] | 3.8333 | 3.1250 |
| `hl` (Sieder-Tate laminar entry coefficient) [W/m²·K⁻¹] | 275.68 (L = 4 m), 151.71 (L = 24 m) | 324.58 |
| `Nu_ST` (Sieder-Tate Nusselt number) [−] | 137.84 (L = 4 m), 75.857 (L = 24 m) | 54.097 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the nine
     correlations over a quality sweep at constant mass flow rate, e.g. h vs x
     for x = 0.1…0.9,
     figures/two_phase_nonboiling_in_tube_h_x.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_two_phase.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*. The 37 output and intermediate values of
the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
37 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 29
```

(the 29 “only in CoolSolve” variables are the 28 inputs of the demonstration
program — `m`, `x`, `D`, `L`, `alpha`, `rhol`, `rhog`, `Cpl`, `kl`, `mul`,
`mug`, `mu_b`, `mu_w` of both cases plus `L_Knott_A` and `L_Martin_Sims_A` —
and the constant `pi`, which the reference table does not hold). The largest
relative deviation over the 37 values is **4.0·10⁻¹²**
(`h_Groothuis_Hendal_water_A`), i.e. round-off in the double-precision
evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `h_Davis_David` | 1437.32828699551 | 1437.328286996 | 3.4e-13 |
| `h_Elamvaluthi_Srinivas` | 3901.21344715786 | 3901.213447166 | 2.1e-12 |
| `h_Groothuis_Hendal` | 1192.95434454558 | 1192.954344548 | 2.0e-12 |
| `h_Groothuis_Hendal_water` | 6362.89896776345 | 6362.898967789 | 4.0e-12 |
| `h_Hughmark` | 212.741163612717 | 212.7411636127 | 8.2e-14 |
| `h_Knott` | 4225.53675804584 | 4225.536758046 | 3.8e-14 |
| `h_Kudirka_Grosh_McFadden` | 303.994125590359 | 303.9941255895 | 2.8e-12 |
| `h_Martin_Sims_hl` (hl = 141.2) | 5563.28000000000 | 5563.280000000 | 1.6e-16 |
| `h_Martin_Sims` (hl computed, L = 24 m) | 5977.50546578175 | 5977.505465782 | 4.2e-14 |
| `h_Ravipudi_Godbold` | 299.379628645929 | 299.3796286457 | 7.6e-13 |
| `h_Aggour` (turbulent branch) | 420.934714688567 | 420.9347146886 | 7.9e-14 |
| `h_Aggour_laminar` | 144.973752788844 | 144.9737527888 | 3.0e-13 |

Case *B* (second input set, computed with the same Python functions):

| Function | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `h_Davis_David_B` | 7552.4877687755 | 7552.487768776 | 6.7e-14 |
| `h_Elamvaluthi_Srinivas_B` | 17578.0717312693 | 17578.07173126 | 5.3e-13 |
| `h_Groothuis_Hendal_B` | 3568.87157009441 | 3568.871570093 | 3.9e-13 |
| `h_Groothuis_Hendal_water_B` | 19555.044859638 | 19555.04485963 | 9.2e-13 |
| `h_Hughmark_B` | 214.052114370728 | 214.0521143707 | 1.3e-13 |
| `h_Knott_B` | 916.847901483594 | 916.8479014836 | 6.1e-15 |
| `h_Kudirka_Grosh_McFadden_B` | 3573.97195668066 | 3573.971956683 | 6.6e-13 |
| `h_Martin_Sims_B` | 1288.65343601424 | 1288.653436014 | 1.9e-13 |
| `h_Ravipudi_Godbold_B` | 3525.36786680242 | 3525.367866803 | 1.6e-13 |
| `h_Aggour_B` (turbulent branch) | 4246.11401087965 | 4246.11401088 | 8.2e-14 |
| `h_Aggour_laminar_B` | 183.781039998443 | 183.7810399984 | 2.3e-13 |

The intermediates of the demonstration program (`V_ls`, `V_gs`, `Re_l`, `Pr_l`,
`hl`, `Nu_ST`) also agree (37 variables in total, all below 4.1·10⁻¹²): they
are the equations the correlations are built from, and `hl`/`Nu_ST` check the
Sieder-Tate laminar entry relation quoted in the comment block of `h_Knott` and
`h_Martin_Sims` against the Python `ht.conv_internal.laminar_entry_Seider_Tate`.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the two-phase non-boiling in-tube correlations of `ht`,
the heat-transfer component of ChEDL, file `ht/conv_two_phase.py`, functions
`Davis_David`, `Elamvaluthi_Srinivas`, `Groothuis_Hendal`, `Hughmark`, `Knott`,
`Kudirka_Grosh_McFadden`, `Martin_Sims`, `Ravipudi_Godbold` and `Aggour`,
version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named after the `ht` function, the Python boolean options became
integer flags (`water` = 1/0 for `Groothuis_Hendal`, `turbulent` = 1/0/-1 for
`Aggour`), the optional arguments became mandatory (pass `mu_b = mu_w` for the
form without the wall-viscosity correction), `hl` became a mandatory input of
`Knott` and `Martin_Sims` (see above), and `pi` is written as the local
constant `pi_val`. No equation was changed. Scientific basis per function: the
original paper or thesis quoted in its comment block.

The scientific authors of the correlations are credited in the comment block
of each function and in `model.json` (`origin.authors`); the review all nine
come from in `ht` is Kim, Ryali, Ghajar & Dougherty, *Heat Transfer
Engineering* 20(1), 1999.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-106, family `HT-011`).** One EES
  `FUNCTION` per `ht` correlation (9 functions), named `h_<method>`, with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in the comment block. Arguments are the
  Python arguments, in SI (`kg/s`, `m`, `kg/m³`, `J/kg·K`, `W/m·K`, `Pa·s`,
  `W/m²·K`); no property functions are used inside the functions, so the
  calling model passes the two-phase properties itself (rule 5 of
  `sources/ht/README.md` §7). The source is already SI: no unit conversion was
  needed.
- The boolean option `water` of `Groothuis_Hendal` is an **1/0 argument** and
  the choice of the correlation form is made with a two-branch EES `IF` (the
  non-smooth regime switch, not a function call); both branches are exercised
  in the demonstration program.
- `Aggour`: the Python flag `turbulent` is tri-state (None → select on
  `Re_l > 2000`, True/False → force a branch); the EES argument `turbulent`
  uses `1` (force turbulent), `0` (force laminar) and `-1` (select on
  `Re_l > 2000`, the default of the original). The `IF` is nested, as the
  choice of the original is a condition on the argument *and* on the Reynolds
  number.
- The optional wall-viscosity arguments (`mu_w` of `Elamvaluthi_Srinivas`,
  `Groothuis_Hendal`, `Kudirka_Grosh_McFadden`, `Ravipudi_Godbold`, `Aggour`,
  and the pair `mu_b`/`mu_w` of `Hughmark`) are **mandatory** in EES, which has
  no optional arguments: the caller passes `mu_b = mu_w` for the form without
  the correction, which is then a factor of exactly 1.
- **`Knott` and `Martin_Sims`**: in `ht`, `hl` is optional and is then computed
  internally with `ht.conv_internal.laminar_entry_Seider_Tate` (a correlation
  of another family, HT-005, which cannot be imported yet — `CS-FEAT-IMPORT`).
  In this file `hl` is a mandatory input, its equation is written in the comment
  block of both functions, and the demonstration program evaluates it, which
  reproduces the two published values of `ht` (4225.536758045839 for `Knott`
  with L = 4 m, 5977.505465781747 for `Martin_Sims` with L = 24 m). This
  changes no equation of the correlation itself.
- **`pi` inside a function body**: written as the local constant
  `pi_val = 3.141592653589793` in the eight bodies that need it, because
  CoolSolve does not resolve the `pi`/`PI` constant inside a `FUNCTION` body and
  evaluates it as **1**, silently (`CS-BUG-PI-FUNCTION`, registered with
  `CSL-0089`; the EES function form `pi()` also works in CoolSolve, but a plain
  local assignment is valid in both). This changes no equation.
- **Selectors not translated**: `h_two_phase` (dispatcher) and
  `h_two_phase_methods` (returns the names of the correlations applicable to a
  given set of inputs) only choose or list a method; the caller chooses the
  `FUNCTION` directly.
- **Level**: equations 65 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The two demonstration input sets are chosen to be realistic, not to stay
  inside every quoted validity range. Case *A* is the published set of `ht`
  (m = 1 kg/s, x = 0.9, D = 0.3 m, so superficial gas velocity 5.09 m/s and
  quality 0.9), which lies outside most of the quoted ranges — e.g. the gas/liquid
  superficial velocity ratio is 3600 for `Elamvaluthi_Srinivas`, `Groothuis_Hendal`
  and `Kudirka_Grosh_McFadden` (quoted 0.3–4.6, 0.6–250) and for
  `Ravipudi_Godbold` (quoted 1–90) — and `h` is a liquid viscosity of
  10⁻³ Pa·s with a gas viscosity of 10⁻⁵ Pa·s, i.e. air-water properties.
  `ht` does not check the ranges, so its values are reproduced as they are; the
  numbers of the *Results* and *Verification* tables check the **equations**,
  not recommended design values. The validity column above is the one to use
  when choosing an input.
- `h_Hughmark` and the laminar form of `h_Aggour` rest on a laminar
  entry-length relation: for a sufficiently long tube they predict unrealistically
  low coefficients (as in the original).
- The wall-viscosity correction `(mu_b/mu_w)^0.14` is applied to the
  **turbulent** form of `Aggour` never (as in the original, where it is only
  suggested for the laminar regime).
- `h_Knott` and `h_Martin_Sims` boost a liquid-phase coefficient `hl` that the
  caller must supply; `ht` computes it internally with the Sieder-Tate laminar
  entry correlation when it is not given (see the *Conversion log*).
- **CoolSolve bug `CS-BUG-PI-FUNCTION`** (registered with `CSL-0089`): the
  `pi` constant evaluates as 1 inside a `FUNCTION` body, silently. Worked
  around with the local constant `pi_val`; the model is not blocked, so the ID
  is not listed in `missing_features`.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No other gap registered for this card: everything else is plain EES
  (`FUNCTION`, `IF/THEN/ELSE`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0089` *condensation_film*: the condensing side of the same physical
  problem (in-tube condensation of `Cavallini_Smith_Zecchin` and the film
  correlations); same layout, same comment blocks, and the same
  `CS-BUG-PI-FUNCTION` workaround.
- `CSL-0087` *internal_turbulent_nusselt*: the single-phase turbulent
  Nusselt-number correlations of `ht` (same triage, same layout); a condenser or
  evaporator tube combines its single-phase coefficients with the two-phase
  multipliers of this file.
- `CSL-0088` *nucleate_boiling_and_chf*: the other phase-change side of
  in-tube heat transfer (nucleate boiling and critical heat flux); the laminar
  thermal entry correlation used for `hl` in this file belongs to the
  single-phase family HT-005 of the same triage.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations that turn
  the coefficients of this file into a condenser or evaporator rating.
- `CSL-0027` *shell_and_tube_steam_condenser* and `CSL-0031`
  *refrigeration_evaporator_wet_coil*: two component models that need
  in-tube two-phase heat-transfer coefficients.
- `sources/labothappy` LTP-034 (in-tube HTC correlations quoting two-phase
  in-tube correlations): the `ht` family is more complete and is the reference
  for the equations.
- `CSL-0098` *flow_boiling_in_tubes*: the in-tube flow-boiling
  coefficients of the same `ht` triage plus Shah 1982 and Gungor-Winterton 1987
  from ThermoCycle (10 functions), same layout; this file rates the two-phase
  flow below the boiling onset that this one describes.

# Free convection from cylinders: Nusselt-number correlations for vertical and horizontal cylinders

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0092`

Thirteen EES `FUNCTION`s returning the Nusselt number of natural convection
from a cylinder — ten for a vertical cylinder (Griffiths, Davis & Morgan 1922;
Jakob & Linke 1935; Carne 1937; Eigenson 1940; Touloukian, Hawkins & Jakob 1948;
Weise 1935 / Saunders 1936 / McAdams; Eckert & Jackson 1950 / Kreith, Manglik &
Bohn; Hanesian & Kalish 1970; Al-Arabi & Khamis 1982; Popiel, Wojtkowiak &
Bober 2007) and three for a horizontal one (Churchill & Chu 1975; Kuehn &
Goldstein 1976; Morgan 1975). All of them take dimensionless arguments only
(Pr, Gr and, where the geometry enters, the height `L` and the diameter `D`);
the surface heat-transfer coefficient follows from `h = Nu*k/D` and is left to
the caller, as in the source library. This is the free-convection counterpart of
`CSL-0087` (`internal_turbulent_nusselt`) and follows the same layout: one
`FUNCTION` per correlation, a comment block per function with the formula, the
validity range and the dual citation, and a demonstration program calling every
function.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Pr and Gr are arguments) |
| **Size** | 62 equations after analysis (largest block: 1); 13 functions of 3–20 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_free_immersed.py` (MIT); inventory row `HT-006` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (42 values, max deviation 2.8·10⁻¹³) |

## Problem statement

For a given fluid state and geometry (Prandtl number `Pr`, Grashof number `Gr`
on the cylinder height for a vertical cylinder or on the diameter for a
horizontal one, height `L` and diameter `D`), compute the Nusselt number Nu of
the cylinder; multiply it by `k/D` to obtain the surface heat-transfer
coefficient. Ten historical correlations are available for the vertical
cylinder and three for the horizontal one, each with its own validity range;
the choice between them is left to the user, who knows the fluid and the
geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_vertical_cylinder_Griffiths_Davis_Morgan` | Pr, Gr, turbulent | Nu = 0.67·Ra^0.25 for 1E7 < Ra < 1E9, Nu = 0.0782·Ra^0.357 for 1E9 < Ra < 1E11 | the two Ra ranges above |
| `Nu_vertical_cylinder_Jakob_Linke_Morgan` | Pr, Gr, turbulent | Nu = 0.555·Ra^0.25 for 1E4 < Ra < 1E8, Nu = 0.129·Ra^(1/3) for 1E8 < Ra < 1E12 | the two Ra ranges above |
| `Nu_vertical_cylinder_Carne_Morgan` | Pr, Gr, turbulent | Nu = 1.07·Ra^0.28 for 2E6 < Ra < 2E8, Nu = 0.152·Ra^0.38 for 2E8 < Ra < 2E11 | the two Ra ranges above |
| `Nu_vertical_cylinder_Eigenson_Morgan` | Pr, Gr, turbulent | Nu = 0.48·Ra^0.25 (Ra ≤ 1E9), Nu = 51.5 + 7.26·10⁻⁵·Ra^0.63 for 1E9 < Ra < 1.69E10, Nu = 0.148·Ra^(1/3) − 127.6 above | the three Ra ranges above |
| `Nu_vertical_cylinder_Touloukian_Morgan` | Pr, Gr, turbulent | Nu = 0.726·Ra^0.25 for 2E8 < Ra < 4E10, Nu = 0.0674·(Gr·Pr^1.29)^(1/3) for 4E10 < Ra < 9E11 | the two Ra ranges above |
| `Nu_vertical_cylinder_McAdams_Weiss_Saunders` | Pr, Gr, turbulent | Nu = 0.59·Ra^0.25 for 1E4 < Ra < 1E9, Nu = 0.13·Ra^(1/3) for 1E9 < Ra < 1E12 | the two Ra ranges above |
| `Nu_vertical_cylinder_Kreith_Eckert` | Pr, Gr, turbulent | Nu = 0.555·Ra^0.25 for 1E5 < Ra < 1E9, Nu = 0.021·Ra^0.4 for 1E9 < Ra < 1E12 | the two Ra ranges above |
| `Nu_vertical_cylinder_Hanesian_Kalish_Morgan` | Pr, Gr | Nu = 0.48·Ra^0.23 | 1E6 < Ra < 1E8 (laminar only) |
| `Nu_vertical_cylinder_Al_Arabi_Khamis` | Pr, Gr, L, D, turbulent | Nu = 2.9·Ra^0.25/Gr_D^(1/12) for 9.88E7 ≤ Ra ≤ 2.7E9, Nu = 0.47·Ra^(1/3)/Gr_D^(1/12) for 2.7E9 ≤ Ra ≤ 2.95E10, Gr_D = Gr·(D/L)³ | 1.08E4 ≤ Gr_D ≤ 6.9E5 and the two Ra ranges |
| `Nu_vertical_cylinder_Popiel_Churchill` | Pr, Gr, L, D | Nu = Nu_fp·{1 + B·[32^0.5·Gr^−0.25·(L/D)]^C}, B = 0.0571322 + 0.20305·Pr^−0.43, C = 0.9165 − 0.0043·Pr^0.5 + 0.01333·ln Pr + 4.809·10⁻⁴/Pr, Nu_fp = [0.825 + 0.387·Ra^(1/6)/{1+(0.492/Pr)^(9/16)}^(8/27)]² | 0.01 < Pr < 100 |
| `Nu_horizontal_cylinder_Churchill_Chu` | Pr, Gr | Nu = [0.60 + 0.387·Ra^(1/6)/{1+(0.559/Pr)^(9/16)}^(8/27)]² | Ra ≥ 1E−5, no upper limit in the original (Incropera et al. suggest Ra ≤ 1E12) |
| `Nu_horizontal_cylinder_Kuehn_Goldstein` | Pr, Gr | 2/Nu = ln[1 + 2/{[{0.518·Ra^0.25·[1+(0.559/Pr)^0.6]^−5/12}^15 + (0.1·Ra^(1/3))^15]^(1/15)}] | all cases except low-Pr fluids |
| `Nu_horizontal_cylinder_Morgan` | Pr, Gr | Nu = C·Ra^n with (C, n) = (0.675, 0.058), (1.02, 0.148), (0.850, 0.188), (0.480, 0.250), (0.125, 0.333) for Ra < 1E−2, < 1E2, < 1E4, < 1E7 and above | the five Ra ranges (up to 1E12) |

Arguments: Pr (Prandtl number, `[-]`), Gr (Grashof number, `[-]`, on the
cylinder height for a vertical cylinder and on the cylinder diameter for a
horizontal one, as stated in each comment block), `L` (cylinder height, `[m]`),
`D` (cylinder diameter, `[m]`) and `turbulent` (regime flag: `-1` = automatic
selection from Ra, the `ht` default `None`; `0` = force the laminar branch;
`1` = force the turbulent branch). Eight of the ten vertical-cylinder
correlations are piecewise in Ra and take that flag.

Every function carries in its comment block (i) the equation, (ii) the
validity range **as quoted by `ht`**, (iii) the original paper or book and
(iv) the `ht` module, function, version and commit it was taken from. The
scientific basis is the presentation of Morgan, V. T., *The Overall Convective
Heat Transfer from Smooth Circular Cylinders*, Advances in Heat Transfer 11,
199–264 (1975), with the original papers named individually (Griffiths 1922,
Jakob & Linke 1935, Carne 1937, Eigenson 1940, Touloukian 1948, Weise 1935,
Saunders 1936, McAdams 1954, Eckert & Jackson 1950, Hanesian & Kalish 1970,
Al-Arabi & Khamis 1982, Popiel et al. 2007, Churchill & Chu 1975, Kuehn &
Goldstein 1976) and Popiel's 2008 review and Boetcher's 2014 chapter as the
secondary presentations `ht` quotes.

Two members of the `ht` family are **not** translated:
`Nu_vertical_cylinder` and `Nu_vertical_cylinder_methods` (and their
horizontal counterparts `Nu_horizontal_cylinder` and
`Nu_horizontal_cylinder_methods`) are dispatchers that map a method name to a
correlation; an EES caller calls the chosen `FUNCTION` directly.

## How to run

Open `free_conv_cylinders.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./free_conv_cylinders.eescode
```

The demonstration program after the definitions calls each of the 13 functions
at least once: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation, then (cases *A_lam* and *A_turb*) with the same
inputs and each branch of the eight regime switches forced, and once (case *B*)
with a single uniform input set (Pr = 0.71, Gr = 1E10, L = 1.5 m, D = 0.15 m,
`turbulent = -1`). It solves without any iteration
(`Solver: SUCCESS (0 iterations)`, every equation is explicit; the analysis
reports `System square: Yes`, 62 equations and 62 variables) and is the
regression baseline (`free_conv_cylinders.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0092 ---}` and
lists `CSL-0092` in its `related` field.

## Results

Values of the demonstration program (full precision in
`free_conv_cylinders.sol`):

| Quantity (case A, `turbulent = -1`) | Nu [−] | Quantity (case B) | Nu [−] |
|---|---:|---|---:|
| `Nu_vertical_cylinder_Griffiths_Davis_Morgan` | 327.62 | | 257.10 |
| `Nu_vertical_cylinder_Jakob_Linke_Morgan` | 310.91 | | 247.94 |
| `Nu_vertical_cylinder_Carne_Morgan` | 204.31 | | 842.02 |
| `Nu_vertical_cylinder_Eigenson_Morgan` | 230.56 | | 168.24 |
| `Nu_vertical_cylinder_Touloukian_Morgan` | 249.73 | | 210.74 |
| `Nu_vertical_cylinder_McAdams_Weiss_Saunders` | 313.32 | | 249.86 |
| `Nu_vertical_cylinder_Kreith_Eckert` | 240.25 | | 183.11 |
| `Nu_vertical_cylinder_Hanesian_Kalish_Morgan` | 18.01 | | 88.52 |
| `Nu_vertical_cylinder_Al_Arabi_Khamis` | 280.40 | | 235.79 |
| `Nu_vertical_cylinder_Popiel_Churchill` | 228.90 | | 240.29 |
| `Nu_horizontal_cylinder_Churchill_Chu` | 139.13 | | 215.65 |
| `Nu_horizontal_cylinder_Kuehn_Goldstein` | 122.99 | | 193.20 |
| `Nu_horizontal_cylinder_Morgan` | 151.39 | | 238.44 |

Forced branches (case *A* inputs, i.e. at the Ra of each `ht` doctest): the
laminar form gives 230.47 (Griffiths-Davis-Morgan), 190.91 (Jakob-Linke-Morgan),
204.31 (Carne, Ra = 1.4E8 is below its 2E8 transition, so the automatic call and
the forced-laminar call agree), 165.11 (Eigenson), 249.73 (Touloukian, same
reason), 202.95 (McAdams-Weiss-Saunders), 190.91 (Kreith-Eckert) and 246.63
(Al-Arabi-Khamis); the turbulent form gives 327.62, 310.91, 189.40, 229.10,
156.94, 313.32, 240.25 and 280.40 respectively. The discontinuity at the
transition is not numerical noise but a property of these correlations (see
*Limitations*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the 13 correlations
     over a Rayleigh-number sweep at Pr = 0.71 (e.g. Nu vs Ra), with the regime
     transitions of the vertical-cylinder forms,
     figures/free_conv_cylinders_nu_ra.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_free_immersed.py`, commit `85e0ee6`, installed from the local clone in
a throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for the forced branches and for case *B*. The 42 output
values of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
42 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 20
```

(the 20 “only in CoolSolve” variables are the 20 inputs of the demonstration
program — `Pr_A_vert`, `Gr_A_vert`, `Pr_A_Carne`, `Gr_A_Carne`,
`Pr_A_Hanesian`, `Gr_A_Hanesian`, `Pr_A_Al_Arabi`, `Gr_A_Al_Arabi`,
`L_A_Al_Arabi`, `D_A_Al_Arabi`, `Pr_A_Popiel`, `Gr_A_Popiel`, `L_A_Popiel`,
`D_A_Popiel`, `Pr_A_horiz`, `Gr_A_horiz` and `Pr_B`, `Gr_B`, `L_B`, `D_B` —;
the reference table holds only the 42 outputs). The largest relative deviation
over the 42 values is **2.8·10⁻¹³**
(`Nu_horizontal_cylinder_Morgan_A`), i.e. round-off in the double-precision
evaluation.

Per-value results, `ht` / CoolSolve:

| Function (case A, automatic regime) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_vertical_cylinder_Griffiths_Davis_Morgan` | 327.623059610 | 327.623059610 | 4.2e-14 |
| `Nu_vertical_cylinder_Jakob_Linke_Morgan` | 310.908352079 | 310.908352079 | 1.5e-14 |
| `Nu_vertical_cylinder_Carne_Morgan` | 204.314706291 | 204.314706291 | 2.1e-13 |
| `Nu_vertical_cylinder_Eigenson_Morgan` | 230.559465255 | 230.559465255 | 1.2e-14 |
| `Nu_vertical_cylinder_Touloukian_Morgan` | 249.728799611 | 249.728799611 | 8.6e-14 |
| `Nu_vertical_cylinder_McAdams_Weiss_Saunders` | 313.318494343 | 313.318494343 | 6.5e-14 |
| `Nu_vertical_cylinder_Kreith_Eckert` | 240.253934730 | 240.253934730 | 1.3e-13 |
| `Nu_vertical_cylinder_Hanesian_Kalish_Morgan` | 18.014150493 | 18.014150493 | 1.9e-13 |
| `Nu_vertical_cylinder_Al_Arabi_Khamis` | 280.397932091 | 280.397932091 | 1.7e-13 |
| `Nu_vertical_cylinder_Popiel_Churchill` | 228.897900551 | 228.897900551 | 4.5e-15 |
| `Nu_horizontal_cylinder_Churchill_Chu` | 139.134939701 | 139.134939701 | 2.6e-13 |
| `Nu_horizontal_cylinder_Kuehn_Goldstein` | 122.993235256 | 122.993235256 | 1.5e-13 |
| `Nu_horizontal_cylinder_Morgan` | 151.388199723 | 151.388199723 | 2.8e-13 |

The first thirteen values are the published `ht` doctest values of the
family, reproduced exactly to the digits printed by `ht`. Forced branches and
case *B* (computed with the same Python functions):

| Function | `ht` | CoolSolve | rel. dev. | Function | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|---:|
| `…_Griffiths_Davis_Morgan_A_lam` | 230.4660 | 230.4660 | 1.0e-13 | `…_Griffiths_Davis_Morgan_A_turb` | 327.6231 | 327.6231 |
| `…_Jakob_Linke_Morgan_A_lam` | 190.9084 | 190.9084 | 1.7e-14 | `…_Jakob_Linke_Morgan_A_turb` | 310.9084 | 310.9084 |
| `…_Carne_Morgan_A_lam` | 204.3147 | 204.3147 | 2.1e-13 | `…_Carne_Morgan_A_turb` | 189.3966 | 189.3966 |
| `…_Eigenson_Morgan_A_lam` | 165.1100 | 165.1100 | 1.1e-13 | `…_Eigenson_Morgan_A_turb` | 229.1011 | 229.1011 |
| `…_Touloukian_Morgan_A_lam` | 249.7288 | 249.7288 | 8.6e-14 | `…_Touloukian_Morgan_A_turb` | 156.9382 | 156.9382 |
| `…_McAdams_Weiss_Saunders_A_lam` | 202.9476 | 202.9476 | 1.3e-13 | `…_McAdams_Weiss_Saunders_A_turb` | 313.3185 | 313.3185 |
| `…_Kreith_Eckert_A_lam` | 190.9084 | 190.9084 | 1.7e-14 | `…_Kreith_Eckert_A_turb` | 240.2539 | 240.2539 |
| `…_Al_Arabi_Khamis_A_lam` | 246.6328 | 246.6328 | 1.8e-13 | `…_Al_Arabi_Khamis_A_turb` | 280.3979 | 280.3979 |

| Function (case B) | `ht` | CoolSolve | Function (case B) | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|
| `Nu_vertical_cylinder_Griffiths_Davis_Morgan_B` | 257.1023 | 257.1023 | `Nu_vertical_cylinder_Al_Arabi_Khamis_B` | 235.7856 | 235.7856 |
| `Nu_vertical_cylinder_Jakob_Linke_Morgan_B` | 247.9377 | 247.9377 | `Nu_vertical_cylinder_Popiel_Churchill_B` | 240.2877 | 240.2877 |
| `Nu_vertical_cylinder_Carne_Morgan_B` | 842.0187 | 842.0187 | `Nu_horizontal_cylinder_Churchill_Chu_B` | 215.6488 | 215.6488 |
| `Nu_vertical_cylinder_Eigenson_Morgan_B` | 168.2426 | 168.2426 | `Nu_horizontal_cylinder_Kuehn_Goldstein_B` | 193.2045 | 193.2045 |
| `Nu_vertical_cylinder_Touloukian_Morgan_B` | 210.7421 | 210.7421 | `Nu_horizontal_cylinder_Morgan_B` | 238.4400 | 238.4400 |
| `Nu_vertical_cylinder_McAdams_Weiss_Saunders_B` | 249.8597 | 249.8597 | | | |
| `Nu_vertical_cylinder_Kreith_Eckert_B` | 183.1145 | 183.1145 | | | |
| `Nu_vertical_cylinder_Hanesian_Kalish_Morgan_B` | 88.5178 | 88.5178 | | | |

All 42 relative deviations are below 2.9·10⁻¹³.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the free-convection correlations of `ht`, the
heat-transfer component of ChEDL, file `ht/conv_free_immersed.py`, functions
`Nu_vertical_cylinder_Griffiths_Davis_Morgan`,
`Nu_vertical_cylinder_Jakob_Linke_Morgan`, `Nu_vertical_cylinder_Carne_Morgan`,
`Nu_vertical_cylinder_Eigenson_Morgan`,
`Nu_vertical_cylinder_Touloukian_Morgan`,
`Nu_vertical_cylinder_McAdams_Weiss_Saunders`,
`Nu_vertical_cylinder_Kreith_Eckert`,
`Nu_vertical_cylinder_Hanesian_Kalish_Morgan`,
`Nu_vertical_cylinder_Al_Arabi_Khamis`,
`Nu_vertical_cylinder_Popiel_Churchill`,
`Nu_horizontal_cylinder_Churchill_Chu`,
`Nu_horizontal_cylinder_Kuehn_Goldstein` and
`Nu_horizontal_cylinder_Morgan`, version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one
EES `FUNCTION` named after the `ht` function, the optional Python argument
`turbulent` became a mandatory three-state flag (`-1` automatic, `0` laminar,
`1` turbulent) and the non-smooth regime switches use EES `IF`, the Python
`log` became the EES `LN`, and `math.log(Pr)` inside the Popiel correlation
became `LN(Pr)`. No equation was changed. Scientific basis per function: the
original paper or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`); the reference most of them
come from in `ht` is Morgan's 1975 review in *Advances in Heat Transfer* 11,
presented in Popiel's 2008 review and in Boetcher's 2014 chapter.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-101, family `HT-006`).** One EES
  `FUNCTION` per `ht` correlation (13 functions), named `Nu_<method>`, with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in the comment block. Arguments are the
  Python arguments, all dimensionless or in SI (`m`); no property function is
  used inside the functions, so the calling model passes Pr and Gr itself (rule
  5 of `sources/ht/README.md` §7).
- The optional boolean `turbulent` of the eight piecewise correlations is a
  **three-state integer argument**: `-1` for `ht`'s `None` (select the branch
  from Ra), `0` for `False` (laminar) and `1` for `True` (turbulent). EES has
  no optional arguments, so every call must state which regime it wants; the
  demonstration program exercises all three states (cases *A*, *A_lam*,
  *A_turb*), which is what makes the 42-value verification possible.
- `Nu_vertical_cylinder_Popiel_Churchill` calls, inside `ht`, its
  `Nu_vertical_plate_Churchill` (Churchill & Chu for a vertical plate), which
  belongs to another family of the same module (family `HT-007`). Its three
  equations are **repeated inside** the function (variable `Nu_fp`) instead of
  calling a second function, so this file stays self-contained and no function
  name is duplicated across the library; the vertical-plate correlation is
  cited in the comment block as well.
- `Nu_vertical_cylinder_Al_Arabi_Khamis`: the switch between the two forms is at
  Ra = 2.6E9 in the `ht` **code** and at 2.7E9 in its docstring (the two
  validity ranges overlap there); the EES function follows the code, as
  documented in its comment block.
- `Nu_vertical_cylinder_Eigenson_Morgan`: the `ht` docstring prints the range of
  its first form as 10^9 < Ra, which its own code contradicts (that form is
  used for Ra ≤ 1E9). The EES function follows the code; the local variable
  `sel` selects the three forms.
- **Selectors not translated**: `Nu_vertical_cylinder`,
  `Nu_vertical_cylinder_methods`, `Nu_horizontal_cylinder` and
  `Nu_horizontal_cylinder_methods` only map a method name to a correlation; the
  caller chooses the `FUNCTION` directly.
- **Level**: equations 62 → 1 point (50–300), largest block 1 → 0,
  functions present → 1, multi-zone no → 0, semi-empirical/off-design no → 0,
  curated guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The two demonstration input sets are chosen to be realistic and to reproduce
  the `ht` doctests, not to stay inside every quoted validity range. Case *B*
  (Ra = 0.71·1E10 = 7.1E9) is outside the ranges of
  `Nu_vertical_cylinder_Hanesian_Kalish_Morgan` (1E6 < Ra < 1E8), of the
  `Al-Arabi-Khamis` first form (Ra > 2.7E9) and of the `Eigenson-Morgan` third
  form (Ra < 1.69E10); case *A* uses the `ht` doctest inputs, which are outside
  the quoted ranges of a few correlations as well (`Al-Arabi-Khamis` is
  developed for Gr_D between 1.08E4 and 6.9E5, while its doctest inputs give
  Gr_D = 2E10·(1/10)³ = 2E7). `ht` does not check the ranges in these functions,
  so its values are reproduced as they are; the numbers of the *Results* and
  *Verification* tables are a check of the **equations**, not recommended
  design values. The validity column of the table above is the one to use when
  choosing an input.
- Eight of the correlations are **discontinuous** at their laminar/turbulent
  transition: the branch changes at a fixed Rayleigh number and the two forms do
  not join. Computed with `ht` at the transition itself (Pr = 1), the jump from
  the laminar to the turbulent form is +7.2 % (Griffiths-Davis-Morgan at
  Ra = 1E9), +7.9 % (Jakob-Linke-Morgan at 1E8), −3.9 % (Carne-Morgan at 2E8),
  +23.9 % (McAdams-Weiss-Saunders at 1E9), −15.3 % (Kreith-Eckert at 1E9),
  −29.0 % (Touloukian-Morgan at 4E10) and −1.3 % (Al-Arabi-Khamis at 2.6E9);
  away from it the two branches diverge (Carne-Morgan at Ra = 1E10, turbulent
  over laminar = 1.42). This is a property of the original correlations,
  reproduced as in `ht`, not of the translation; the `turbulent` argument lets a
  caller stay on one branch. A sweep of Ra through a transition therefore shows
  a jump — the correlations are not meant to be used that close to it.
- `Nu_vertical_cylinder_Popiel_Churchill` is a *laminar* correlation with no
  regime argument and its validity range in `ht` is given on Pr alone; outside it
  the correction exponent `C` is no longer physical.
- No property calls are made: Pr and Gr are arguments, so a model using these
  functions must evaluate them itself (`Gr = g·|ρ_∞ − ρ_w|·L³/(μ²)·…` in its own
  SI variables).
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES
  (`FUNCTION`, nested `IF/THEN/ELSE`, `LN`, `^`) and runs in CoolSolve v0.3.0
  (`System square: Yes`, 0 solver iterations).

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the same `ht` triage and the same
  layout for **internal** turbulent convection (23 `FUNCTION`s); its
  demonstration program uses the same regime-flag convention (`CSL-0086`
  *in_cylinder_htc_correlations* is a third function library of the same kind).
- `CSL-0089` *condensation_film*: film condensation on the same geometries (its
  `h_Nusselt_plate` uses a laminar-film natural-convection number of a vertical
  plate).
- `CSL-0088` *nucleate_boiling_and_chf*: the other natural-convection function
  library (pool boiling and critical heat flux); both files take fluid
  properties as plain arguments.
- `sources/labothappy` LTP-039 and LTP-038 (finned-tube air side, external tube
  bundles): natural convection from a bundle in a forced crossflow — the same
  dimensionless groups (`Pr`, `Gr`) plus a forced-convection term, not covered
  here.
- `CSL-0093` *free_conv_plates_and_sphere*: the plate and sphere family of the
  **same `ht` module** (Churchill & Chu vertical plate, McAdams / VDI / Rohsenow
  horizontal plate, Churchill sphere, 5 functions), same layout; it completes
  this file, whose `Nu_vertical_cylinder_Popiel_Churchill` repeats the vertical-
  plate correlation of `CSL-0093` inline.

- `CSL-0094` *external_crossflow_cylinder*: crossflow (forced convection) over
  a single cylinder (8 functions), the forced-convection counterpart of this
  natural-convection family; same `ht` layout.
- `CSL-0100` *free_conv_enclosed_and_jackets*: the enclosed-plate, helical-coil
  and vessel-jacket correlations of the same `ht` layout (10 functions); this file
  gives the free convection of an *immersed* body, that one of an enclosed layer.
- `CSL-0101` *external_forced_conv_plates*: the other **external** forced-convection geometry of the same `ht` module `ht/conv_external.py` (isothermal flat plate in crossflow: Baehr-Stephan and Churchill-Ozoe laminar, Schlichting and Kreith turbulent), same layout.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.

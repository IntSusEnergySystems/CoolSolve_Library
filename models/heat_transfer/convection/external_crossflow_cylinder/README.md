# External forced convection: crossflow over a single cylinder

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0094`

Eight EES `FUNCTION`s returning the Nusselt number of a single circular cylinder
(tube) in crossflow: Zukauskas (piecewise in Re, with the optional
wall-Prandtl correction), Churchill-Bernstein, Sanitjai-Goldstein, Fand, McAdams,
Whitaker and the two forms of Perkins-Leppert (1962 and 1964), the last three
with the optional viscosity-ratio correction. The arguments are dimensionless
(`Re` on the cylinder diameter, `Pr`, `Prw`) except the two viscosities `mu` and
`muw` in `[Pa·s]`; the surface heat-transfer coefficient follows from `h = Nu·k/D`
and is left to the caller, as in the source library. This is the external
(forced-convection) counterpart of `CSL-0087`
(`internal_turbulent_nusselt`), the free-convection cylinder correlations are in
`CSL-0092`, and the tube-bank extensions of the same physics are the next `ht`
family (`HT-009`).

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Re, Pr, Prw, mu and muw are arguments) |
| **Size** | 36 equations after analysis (largest block: 1); 8 functions of 1 code line each, except `Nu_cylinder_Zukauskas` (24 lines, the piecewise selection of C, m and n) |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_external.py` (MIT); inventory row `HT-008` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (24 values, max deviation 1.9·10⁻¹³) |

## Problem statement

For a fluid flowing across a single cylinder of diameter `D` — a heat-exchanger
tube, a wire, a boiler-tube bundle element — compute the average Nusselt number
Nu on `D` from the Reynolds number Re and the Prandtl number Pr; multiply it by
`k/D` to obtain the average surface heat-transfer coefficient. Eight
correlations of the family are available, each with its own data basis and
validity range; the choice between them is left to the user, who knows the fluid,
the geometry and the wall temperature.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_cylinder_Zukauskas` | Re, Pr, Prw | Nu = C·Re^m·Pr^n·(Pr/Prw)^0.25, C = 0.75 / 0.51 / 0.26 / 0.076 and m = 0.4 / 0.5 / 0.6 / 0.7 for Re ≤ 40, 40–10³, 10³–2·10⁵, > 2·10⁵; n = 0.37 if Pr ≤ 10, else 0.36 | the four Re ranges, up to Re = 10⁶; outside them the nearest range is used blindly |
| `Nu_cylinder_Churchill_Bernstein` | Re, Pr | Nu = 0.3 + {0.62·Re^0.5·Pr^(1/3)/[1+(0.4/Pr)^(2/3)]^0.25}·{1+(Re/282000)^(5/8)}^0.8 | laminar and turbulent, no range quoted; a lower bound for Re·Pr > 0.4 |
| `Nu_cylinder_Sanitjai_Goldstein` | Re, Pr | Nu = 0.446·Re^0.5·Pr^0.35 + 0.528·{6.5^(−5)·e^(−5·Re/5000) + (0.031·Re^0.8)^(−5)}^(−1/5)·Pr^0.42 (the form of the `ht` code, see the conversion log) | laminar and turbulent; 2·10³ ≤ Re ≤ 9·10⁴, 0.7 ≤ Pr ≤ 176 (water, glycol-water, air) |
| `Nu_cylinder_Fand` | Re, Pr | Nu = (0.35 + 0.34·Re^0.5 + 0.15·Re^0.58)·Pr^0.3 | laminar and turbulent; developed for water, 10⁴ ≤ Re ≤ 10⁵, claimed 0.1 ≤ Re ≤ 10⁵ |
| `Nu_cylinder_McAdams` | Re, Pr | Nu = (0.35 + 0.56·Re^0.52)·Pr^0.3 | laminar and turbulent; water only, very limited data, no range quoted |
| `Nu_cylinder_Whitaker` | Re, Pr, mu, muw | Nu = (0.4·Re^0.5 + 0.06·Re^(2/3))·Pr^0.3·(mu/muw)^0.25 (the `ht` code uses the exponent 0.3, its docstring prints 0.4, see the conversion log) | laminar and turbulent; 1 ≤ Re ≤ 10⁵, 0.67 ≤ Pr ≤ 300, 0.25 ≤ mu/muw ≤ 5.2; agrees with the data within 25 % |
| `Nu_cylinder_Perkins_Leppert_1962` | Re, Pr, mu, muw | Nu = (0.30·Re^0.5 + 0.10·Re^0.67)·Pr^0.4·(mu/muw)^0.25 | laminar and turbulent; 40 ≤ Re ≤ 10⁵, 1 ≤ Pr ≤ 300, 0.25 ≤ mu/muw ≤ 4 |
| `Nu_cylinder_Perkins_Leppert_1964` | Re, Pr, mu, muw | Nu = (0.31·Re^0.5 + 0.11·Re^0.67)·Pr^0.4·(mu/muw)^0.25 | laminar and turbulent; 2·10³ ≤ Re ≤ 1.2·10⁵, 1 ≤ Pr ≤ 7, surface-to-bulk 11–66 K |

Arguments: Re (Reynolds number on the cylinder diameter, `[-]`), Pr (Prandtl
number, `[-]` — at the **film temperature** for `Churchill_Bernstein`,
`Sanitjai_Goldstein`, `Fand` and `McAdams`, at the **free-stream temperature**
for `Zukauskas`, `Whitaker` and `Perkins_Leppert_*`, as stated in `ht` and
repeated in each comment block), Prw (Prandtl number at the wall temperature,
`[-]`, argument of `Nu_cylinder_Zukauskas`) and `mu` / `muw` (free-stream and
wall viscosity, `[Pa·s]`, arguments of the three viscosity-corrected forms).

`ht` declares `Prw`, `mu` and `muw` as **optional** (without them the correction
is simply not applied and is left to an outside function); EES has no optional
argument, so they are **mandatory** and the caller passes `Prw = Pr`, resp.
`mu = muw`, for the uncorrected form. The demonstration program calls both forms
of each of those four functions.

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The scientific basis is
the original article of each correlation: Zukauskas 1972 (*Advances in Heat
Transfer* 8, also the form of Example 7.3 of Bergman-Lavine-Incropera-DeWitt
2011), Churchill & Bernstein 1977 (*J. Heat Transfer* 99), Sanitjai & Goldstein
2004 (*Int. J. Heat Mass Transfer* 47), Fand 1965 (*Int. J. Heat Mass Transfer*
8), McAdams, *Heat Transmission*, 3E, 1985, Whitaker 1972 (*AIChE Journal* 18),
Perkins & Leppert 1962 (*J. Heat Transfer* 84) and 1964 (*Int. J. Heat Mass
Transfer* 7).

Two members of the `ht` family are **not** translated: `Nu_external_cylinder`
and `Nu_external_cylinder_methods` are dispatchers that map a method name to a
correlation; an EES caller calls the chosen `FUNCTION` directly. The `ht`
ranking of the family (Sanitjai-Goldstein, Churchill-Bernstein, Zukauskas,
Whitaker, Perkins-Leppert 1964, McAdams, Fand, Perkins-Leppert 1962) is
repeated in the file header; it is not translated either.

## How to run

Open `external_crossflow_cylinder.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./external_crossflow_cylinder.eescode
```

The demonstration program after the definitions calls each of the 8 functions
twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation (Re = 7992, Pr = 0.707, Prw = 0.69 for Zukauskas;
Re = 6071, Pr = 0.7 for the seven others; mu = 10⁻³ Pa·s, muw = 1.2·10⁻³ Pa·s for
the viscosity corrections), once (case *B*) with a single uniform input set
(Re = 3.5·10⁴, Pr = 4.5, Prw = 5.1, mu = 8.5·10⁻⁴ Pa·s, muw = 6·10⁻⁴ Pa·s).
It solves without any iteration (`Solver: SUCCESS (0 iterations)`, every
equation is explicit) and is the regression baseline
(`external_crossflow_cylinder.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0094 ---}` and
lists `CSL-0094` in its `related` field.

## Results

Values of the demonstration program (full precision in
`external_crossflow_cylinder.sol`):

| Quantity (case A) | Nu [−] | Quantity (case B) | Nu [−] |
|---|---:|---|---:|
| `Nu_cylinder_Zukauskas` (Prw = 0.69) | 50.52 | (Prw = 5.1) | 234.16 |
| `Nu_cylinder_Zukauskas_equalprw` (Prw = Pr) | 50.22 | | 241.60 |
| `Nu_cylinder_Churchill_Bernstein` | 40.64 | | 222.05 |
| `Nu_cylinder_Sanitjai_Goldstein` | 40.38 | | 274.17 |
| `Nu_cylinder_Fand` | 45.20 | | 202.20 |
| `Nu_cylinder_McAdams` | 46.98 | | 203.35 |
| `Nu_cylinder_Whitaker` (mu = muw) | 45.95 | | 218.31 |
| `Nu_cylinder_Whitaker_visc` (mu/muw = 0.833) | 43.90 | (mu/muw = 1.417) | 238.18 |
| `Nu_cylinder_Perkins_Leppert_1962` (mu = muw) | 49.97 | | 304.65 |
| `Nu_cylinder_Perkins_Leppert_1962_visc` (mu/muw = 0.833) | 47.75 | (mu/muw = 1.417) | 332.36 |
| `Nu_cylinder_Perkins_Leppert_1964` (mu = muw) | 53.62 | | 328.28 |
| `Nu_cylinder_Perkins_Leppert_1964_visc` (mu/muw = 0.833) | 51.23 | (mu/muw = 1.417) | 358.15 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the eight correlations
     over a Reynolds-number sweep, e.g. Nu vs Re at Pr = 0.7 and Pr = 5 on a log-log plot,
     figures/external_crossflow_cylinder_nu_re.png -->

## Verification

Reference: for case *A*, the **doctest values published in the docstrings of
`ht` 1.2.0** (`ht/conv_external.py`, commit `85e0ee6`) and the viscosity-ratio
values of `ht/tests/test_conv_external.py`, the Python functions being run from
the local clone installed in a throw-away virtual environment; for case *B*,
values computed with the same Python functions. The 24 output values of the
demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
36 common variables, 0 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 0
Only in EES reference: Pr_Zukauskas_B, Re_Zukauskas_B
```

The two “only in EES” entries are the Zukauskas inputs of case *B*, which the
Python reference lists twice although the demonstration program passes the
uniform `Re_B` and `Pr_B` to `Nu_cylinder_Zukauskas` (case *B* is a single
uniform input set). The largest relative deviation over the 24 values is
**1.9·10⁻¹³** (`Nu_cylinder_Churchill_Bernstein_B`), i.e. round-off in the
double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_cylinder_Zukauskas` | 50.523612661934 | 50.5236126619 | 8.7e-14 |
| `Nu_cylinder_Zukauskas_equalprw` | 50.217121655860 | 50.2171216559 | 4.8e-15 |
| `Nu_cylinder_Churchill_Bernstein` | 40.637085941250 | 40.6370859412 | 6.5e-15 |
| `Nu_cylinder_Sanitjai_Goldstein` | 40.383270835195 | 40.3832708352 | 1.2e-13 |
| `Nu_cylinder_Fand` | 45.199843254811 | 45.1998432548 | 2.8e-14 |
| `Nu_cylinder_McAdams` | 46.981792358679 | 46.9817923587 | 1.4e-14 |
| `Nu_cylinder_Whitaker` | 45.945274615891 | 45.9452746159 | 2.7e-14 |
| `Nu_cylinder_Whitaker_visc` | 43.898081467604 | 43.8980814676 | 8.1e-14 |
| `Nu_cylinder_Perkins_Leppert_1962` | 49.971642911755 | 49.9716429118 | 1.0e-13 |
| `Nu_cylinder_Perkins_Leppert_1962_visc` | 47.745046034647 | 47.7450460346 | 6.8e-14 |
| `Nu_cylinder_Perkins_Leppert_1964` | 53.617670386200 | 53.6176703862 | 2.5e-15 |
| `Nu_cylinder_Perkins_Leppert_1964_visc` | 51.228616705284 | 51.2286167053 | 8.2e-14 |

Case *B* (second input set, computed with the same Python functions):

| Function | `ht` | CoolSolve | Function | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|
| `Nu_cylinder_Zukauskas_B` | 234.1604 | 234.1604 | `Nu_cylinder_Whitaker_B` | 218.3131 | 218.3131 |
| `Nu_cylinder_Zukauskas_equalprw_B` | 241.6033 | 241.6033 | `Nu_cylinder_Whitaker_visc_B` | 238.1753 | 238.1753 |
| `Nu_cylinder_Churchill_Bernstein_B` | 222.0548 | 222.0548 | `Nu_cylinder_Perkins_Leppert_1962_B` | 304.6468 | 304.6468 |
| `Nu_cylinder_Sanitjai_Goldstein_B` | 274.1743 | 274.1743 | `Nu_cylinder_Perkins_Leppert_1962_visc_B` | 332.3637 | 332.3637 |
| `Nu_cylinder_Fand_B` | 202.1979 | 202.1979 | `Nu_cylinder_Perkins_Leppert_1964_B` | 328.2826 | 328.2826 |
| `Nu_cylinder_McAdams_B` | 203.3492 | 203.3492 | `Nu_cylinder_Perkins_Leppert_1964_visc_B` | 358.1499 | 358.1499 |

All 24 relative deviations are below 1.9·10⁻¹³.

The eight case-*A* values of the first table that carry a method name are the
published `ht` doctests (`>>> Nu_cylinder_Zukauskas(7992, 0.707, 0.69)` →
50.523612661934386, `>>> Nu_cylinder_Churchill_Bernstein(6071, 0.7)` →
40.63708594124974, and the six other doctests). Three more values come from the
viscosity-ratio calls of `ht/tests/test_conv_external.py` (mu = 10⁻³,
muw = 1.2·10⁻³): `Nu_cylinder_Whitaker_visc` 43.89808146760356,
`Nu_cylinder_Perkins_Leppert_1962_visc` 47.74504603464674 and
`Nu_cylinder_Perkins_Leppert_1964_visc` 51.22861670528418. The last value,
`Nu_cylinder_Zukauskas_equalprw` 50.21712165586024, is the uncorrected form of
Zukauskas (Prw = Pr), which `ht` only produces when `Prw` is not passed.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the single-cylinder crossflow correlations of `ht`, the
heat-transfer component of ChEDL, file `ht/conv_external.py`, functions
`Nu_cylinder_Zukauskas`, `Nu_cylinder_Churchill_Bernstein`,
`Nu_cylinder_Sanitjai_Goldstein`, `Nu_cylinder_Fand`, `Nu_cylinder_McAdams`,
`Nu_cylinder_Whitaker`, `Nu_cylinder_Perkins_Leppert_1962` and
`Nu_cylinder_Perkins_Leppert_1964`, version 1.2.0, commit 85e0ee6
(2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one
EES `FUNCTION` named after the `ht` function, the Python default `None` of the
optional `Prw` argument of `Nu_cylinder_Zukauskas` and of the optional `mu` /
`muw` arguments of `Nu_cylinder_Whitaker`, `Nu_cylinder_Perkins_Leppert_1962`
and `Nu_cylinder_Perkins_Leppert_1964` became mandatory arguments (pass
`Prw = Pr`, resp. `mu = muw`, for the form without the correction), the Python
`exp` and `**` became the EES `EXP` and `^`, and the piecewise selection of `C`
and `m` in `Nu_cylinder_Zukauskas` became a nested EES `IF` block. No equation
of the `ht` **code** was changed; where a printed `ht` docstring and its code
disagree (`Whitaker`, `Sanitjai_Goldstein`), the code is followed — see the
conversion log. Scientific basis per function: the original paper or book
quoted in its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-103, family `HT-008`).** One EES
  `FUNCTION` per `ht` correlation (8 functions), named after the `ht` function,
  with the formula, the validity range as quoted by `ht`, the original reference
  and the `ht` module/function/version/commit in the comment block. Arguments
  are the Python arguments, all dimensionless or in SI (`Pa·s`); no property
  functions are used inside the functions, so the calling model passes Re, Pr,
  Prw and the viscosities itself (rule 5 of `sources/ht/README.md` §7).
- **Optional arguments made mandatory**: `ht` applies the wall-Prandtl
  correction of `Nu_cylinder_Zukauskas` and the viscosity correction of
  `Nu_cylinder_Whitaker`, `Nu_cylinder_Perkins_Leppert_1962` and
  `Nu_cylinder_Perkins_Leppert_1964` only when `Prw` / `mu`, `muw` are passed.
  EES has no optional argument, so those arguments are mandatory and the
  uncorrected form is obtained with `Prw = Pr` resp. `mu = muw`; both forms are
  exercised in the demonstration program (same decision as `CSL-0087` for
  `Nu_Sieder_Tate`).
- **Non-smooth regime switch**: the four `C`, `m` pairs of
  `Nu_cylinder_Zukauskas` and the `n` exponent are selected with a **nested EES
  `IF` block** (the one-word `ELSEIF` keyword is not used: CoolSolve 0.3.0 reads
  it as an unknown function, see `CSL-0088`; the EES idiom of `ELSE` + `IF` is
  used instead, as in `CSL-0087`).
- **`Nu_cylinder_Sanitjai_Goldstein`**: the equation printed in the `ht`
  docstring shows `(6.5·exp(Re/5000))^(−5)` in the second term; its **code**
  carries the power inside the exponential, `6.5^(−5)·exp(−5·Re/5000)`, to
  avoid an overflow error for a large-diameter cylinder. The EES function
  follows the code (the exponent is moved inside the exponential, as in the
  original comment of `ht`), which is also the form that reproduces the
  doctest value 40.38327083519522 at Re = 6071, Pr = 0.7.
- **`Nu_cylinder_Whitaker`**: the exponent of Pr is **0.3 in the `ht` code**,
  which is the form that reproduces its doctest value 45.94527461589126, while
  the formula printed in the `ht` docstring shows `Pr^0.4` (it gives 44.335 at
  the same point). The EES function follows the code; the discrepancy is noted
  in the function comment. (The two Perkins-Leppert forms, whose paper Sanitjai &
  Goldstein also review, do use `Pr^0.4`.)
- **Selectors not translated**: `Nu_external_cylinder` and
  `Nu_external_cylinder_methods` only map a method name to a correlation; the
  caller chooses the `FUNCTION` directly. The `ht` ranking list
  `conv_external_cylinder_turbulent_methods_ranked` is a Python list of method
  names, not a correlation: it is quoted in the file header only.
- **Level**: equations 36 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0 (the same
  reading as `CSL-0087` and `CSL-0088`: closed-form fits of one operating
  point), curated guesses no → 0. Score 1 → **level 1**; raised to **level 2**
  (± 1, docs/taxonomy.md §3), the reading of the other `ht` function libraries
  of the library (`CSL-0087`, `CSL-0088`, `CSL-0092`, `CSL-0093`), since the
  user has to know eight different data bases and validity ranges to pick a
  correlation.

## Limitations and CoolSolve gaps

- **The `ht` reference row `HT-008` is stale on one point**: it says that
  `Nu_cylinder_Whitaker` "also takes the `D^2/(L D)` geometry parameter". The
  signature of `ht` 1.2.0 (`ht/conv_external.py`, line 320) is
  `Nu_cylinder_Whitaker(Re, Pr, mu=None, muw=None)` — there is no `L` or `D`
  argument, so nothing was translated for it. The `ht` row of the inventory is
  not modified by this card.
- `ht` checks no validity range and returns the value of the branch the input
  falls in. Both demonstration input sets stay inside every quoted range, except
  that the case-*A* calls of the two Perkins-Leppert forms use the `ht` doctest
  value Pr = 0.7, just below the quoted `1 ≤ Pr` (their doctest input, kept
  unchanged). The numbers of the *Results* and *Verification* tables are a check
  of the **equations**, not recommended design values; the validity column of
  the table above is the one to use when choosing an input.
- The functions return an average over the cylinder surface, not the local
  distribution. Two of the originals are papers on a uniformly heated cylinder
  (Perkins & Leppert 1962 and 1964, the latter on local heat-transfer
  coefficients), and `ht` notes that Sanitjai & Goldstein "also presents results
  for local heat transfer coefficients"; a model that needs the local value must
  use those correlations, which are not part of this family.
- No property call is available inside the functions, so the calling model must
  supply `Re`, `Pr`, `Prw` and the viscosities at the temperature each comment
  block names (film, free-stream or wall).
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- **No gap registered for this card**: everything is plain EES
  (`FUNCTION`, nested `IF/THEN/ELSE`, `EXP`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family of the library
  (single-phase turbulent **internal** convection), same file layout, same
  comment blocks; a model that flows inside a crossflow tube bank uses both.
- `CSL-0092` *free_conv_cylinders* and `CSL-0093`
  *free_conv_plates_and_sphere*: the free-convection (natural-convection)
  counterparts of this file, same layout; their arguments are Pr and Gr instead
  of Re and Pr.
- `CSL-0018` *pipe_pressure_drop_colebrook*: the pipe flow Reynolds number
  Re that most of these correlations take as an argument, and the friction
  factor of the same pipe.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations of a
  crossflow heat exchanger, whose single-stream side uses the Nu of this file.
- `CSL-0088` *nucleate_boiling_and_chf*, `CSL-0089` *condensation_film*: the
  other two `ht` wave-1 families that a crossflow tube bundle may need (boiling
  or condensation on the tubes instead of single-phase crossflow).
- `sources/labothappy` LTP-038 (external tube bundles): the LaboThapPy
  integration of bundle-scale correlations; the `ht` single-cylinder family
  here is the reference for the equations and the natural input of a bundle
  model.
- `CSL-0095` *tube_bank_nusselt*: the **tube-bank** forced-convection family of
  the same `ht` triage (Zukauskas with the Bejan fit, ESDU 73031, HEDH, and the
  row and inclination correction factors), same layout; a crossflow bundle
  combines its row/angle corrections with the single-cylinder Nu of this file.
- `CSL-0101` *external_forced_conv_plates*: the other **external** forced-convection geometry of the same `ht` module `ht/conv_external.py` (isothermal flat plate in crossflow: Baehr-Stephan and Churchill-Ozoe laminar, Schlichting and Kreith turbulent), same layout.

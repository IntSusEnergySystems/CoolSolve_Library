# Packed-bed forced convection: Nusselt-number correlations

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0108`

Four EES `FUNCTION`s returning the particle Nusselt number of forced
convection in a packed (fixed) bed: the Gnielinski single-sphere form
scaled by the packing shape factor, Wakao-Kagei, Achenbach and the KTA
rule for spherical fuel elements. The wall heat-transfer coefficient
follows from `h = Nu*k/dp` and is left to the caller, as in the source
library. This is the `HT-022` family of the `ht` triage (roadmap card
C-117); same layout and same comment blocks as the first family,
`CSL-0087` *internal_turbulent_nusselt*.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations take the bed operating point or Re, Pr and the void fraction as arguments) |
| **Size** | 25 equations after analysis (largest block: 1); 4 functions of 3–24 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_packed_bed.py` (MIT); inventory row `HT-022` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (10 values, max deviation 1.4·10⁻¹²) |

## Problem statement

For a packed bed of given particles (equivalent spherical diameter `dp`,
void fraction `voidage`) crossed by a fluid (superficial velocity `vs`,
density `rho`, viscosity `mu`, Prandtl number `Pr`), compute the particle
Nusselt number Nu; multiply it by `k/dp` to obtain the particle-to-fluid
heat-transfer coefficient. Four correlations are available for that, each
with its own validity range; the choice between them is left to the user,
who knows the packing and the fluid.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_packed_bed_Gnielinski` | dp, voidage, vs, rho, mu, Pr, fa | Nu = fa·Nu_sphere, Nu_sphere = 2 + (Nu_lam² + Nu_turb²)^0.5, Nu_lam = 0.664·Re^0.5·Pr^(1/3), Nu_turb = 0.037·Re^0.8·Pr / [1 + 2.443·Re^(−0.1)·(Pr^(2/3) − 1)], Re = rho·vs·dp/(mu·voidage); fa ≤ 0 selects fa = 1 + 1.5·(1 − voidage) | 10⁻¹ < Re < 10³, 0.4 < Pr < 1000 for spheres; smaller limits for other shapes |
| `Nu_Wakao_Kagei` | Re, Pr | Nu = 2 + 1.1·Pr^(1/3)·Re^0.6 | 3 ≤ Re ≤ 3000 (claimed reasonable to 10⁶) |
| `Nu_Achenbach` | Re, Pr_unused, voidage | Nu = [(1.18·Re^0.58)⁴ + (0.23·(Re/(1 − voidage))^0.75)⁴]^0.25 | Re/voidage < 7.7·10⁵; wind-tunnel data to 30 bar |
| `Nu_KTA` | Re, Pr, voidage | Nu = 1.27·Pr^(1/3)·Re^0.36/voidage^1.18 + 0.033·Pr^0.5·Re^0.86/voidage^1.07 | 100 < Re < 10⁵, 0.36 < voidage < 0.42, D/d > 20, H > 4d |

Arguments: `dp` (equivalent spherical particle diameter, `[m]`),
`voidage` (void fraction of the bed, `[-]`), `vs` (superficial fluid
velocity, `[m/s]`), `rho` (fluid density, `[kg/m3]`), `mu` (fluid
viscosity, `[Pa·s]`), `Pr` (fluid Prandtl number, `[-]`), `fa` (packing
shape factor, `[-]`: ≤ 0 for the sphere default, 1.6 for cylinders and
cubes, 2.1 for Raschig rings, 2.3 for Berl saddles), `Re` (particle
Reynolds number, `[-]`). `Pr_unused` is accepted for API consistency but
does not enter the Achenbach equation, as in `ht`.

Every function carries in its comment block (i) the equation, (ii) the
validity range **as quoted by `ht`**, (iii) the original paper or book and
(iv) the `ht` module, function, version and commit it was taken from. The
scientific basis is, per function: Gnielinski 1981 / 1982 and the VDI Heat
Atlas 2010 (`Nu_packed_bed_Gnielinski`); Wakao & Kagei, *Heat and Mass
Transfer in Packed Beds*, 1982 (`Nu_Wakao_Kagei`); Achenbach 1995
(`Nu_Achenbach`); the KTA rule 3102.2, 1983 (`Nu_KTA`) — each as cited in
the review of Abdulmohsin & Al-Dahhan, *Nuclear Engineering and Design*
284, 2015.

No member of the `ht` module is a dispatcher: all four functions are
translated.

## How to run

Open `packed_bed_nusselt.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./packed_bed_nusselt.eescode
```

The demonstration program after the definitions calls each of the 4
functions twice: once (case *A*) with the input set of the `ht` doctest of
the corresponding function, once (case *B*) with a single uniform input
set describing one air bed (dp = 5 mm, voidage = 0.38, vs = 0.5 m/s,
rho = 1.2 kg/m3, mu = 1.8·10⁻⁵ Pa·s, Pr = 0.71; Re = 438.60 follows from
the Gnielinski definition). It solves without any iteration
(`Solver: SUCCESS (0 iterations)`, every equation is explicit) and is the
regression baseline (`packed_bed_nusselt.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0108 ---}`
and lists `CSL-0108` in its `related` field.

## Results

Values of the demonstration program (full precision in
`packed_bed_nusselt.sol`):

| Quantity (case A) | Nu [−] | Quantity (case B) | Nu [−] |
|---|---:|---|---:|
| `Nu_Gnielinski` (sphere default) | 61.38 | (sphere default) | 29.45 |
| `Nu_Gnielinski_fa2` (fa = 2) | 64.61 | `Nu_Gnielinski_fa21` (fa = 2.1, Raschig rings) | 32.05 |
| `Nu_Wakao_Kagei` (Re = 2000, Pr = 0.7) | 95.41 | (Re = 438.60, Pr = 0.71) | 39.76 |
| `Nu_Achenbach` (Re = 2000, voidage = 0.4) | 117.70 | (Re = 438.60, voidage = 0.38) | 43.57 |
| `Nu_KTA` (Re = 2000, Pr = 0.7, voidage = 0.4) | 102.09 | (Re = 438.60, Pr = 0.71, voidage = 0.38) | 46.37 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the 4 correlations
      over a Reynolds-number sweep, e.g. Nu vs Re at Pr = 0.7 and voidage = 0.4,
      figures/packed_bed_nusselt_nu_re.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_packed_bed.py`, commit `85e0ee6`, installed from the local clone
in a throw-away virtual environment) for case *A* — including the second
`fa = 2` regression value of `tests/test_conv_packed_bed.py` — plus values
computed with the same Python functions for case *B*. The 10 output values
of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
10 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 15
```

(the 15 “only in CoolSolve” variables are the 15 inputs of the
demonstration program — `dp_A`, `voidage_A`, `vs_A`, `rho_A`, `mu_A`,
`Pr_A`, `Re_A`, `Pr_Wakao_A` and `dp_B`, `voidage_B`, `vs_B`, `rho_B`,
`mu_B`, `Pr_B`, `Re_B` —; the reference table holds only the 10 outputs).
The largest relative deviation over the 10 values is **1.4·10⁻¹²**
(`Nu_Achenbach_B`), i.e. round-off in the double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_Gnielinski_A` | 61.37823202546954 | 61.37823202547 | 7.4e-15 |
| `Nu_Gnielinski_fa2_A` | 64.60866528996795 | 64.60866528997 | 3.2e-14 |
| `Nu_Wakao_Kagei_A` | 95.40641328041248 | 95.40641328041 | 2.6e-14 |
| `Nu_Achenbach_A` | 117.70343608599121 | 117.7034360860 | 7.5e-14 |
| `Nu_KTA_A` | 102.08516480718129 | 102.0851648072 | 1.8e-13 |
| `Nu_Gnielinski_B` | 29.452850852579207 | 29.45285085261 | 1.0e-12 |
| `Nu_Gnielinski_fa21_B` | 32.04714341472349 | 32.04714341475 | 8.3e-13 |
| `Nu_Wakao_Kagei_B` | 39.76167294933614 | 39.76167294938 | 1.1e-12 |
| `Nu_Achenbach_B` | 43.56951990000972 | 43.56951990007 | 1.4e-12 |
| `Nu_KTA_B` | 46.365694195033186 | 46.36569419508 | 1.0e-12 |

All 10 relative deviations are below 1.4·10⁻¹².

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the packed-bed convection correlations of `ht`, the
heat-transfer component of ChEDL, file `ht/conv_packed_bed.py`, functions
`Nu_packed_bed_Gnielinski`, `Nu_Wakao_Kagei`, `Nu_Achenbach` and `Nu_KTA`,
version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one
EES `FUNCTION` named as in `ht`; the optional shape factor `fa` of
`Nu_packed_bed_Gnielinski` (default `None` in `ht`) became a mandatory
argument with `fa <= 0` selecting the sphere relation (EES has no optional
arguments); both calls are exercised in the demonstration program. No
equation was changed. Scientific basis per function: the original paper or
book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block
of each function and in `model.json` (`origin.authors`): V. Gnielinski
1981/1982 and the VDI Heat Atlas 2010 (`Nu_packed_bed_Gnielinski`); N. Wakao
and S. Kagei 1982 (`Nu_Wakao_Kagei`); E. Achenbach 1995 (`Nu_Achenbach`);
the KTA rule 3102.2, 1983 (`Nu_KTA`) — the last three as cited in the
review of Abdulmohsin & Al-Dahhan 2015.

## Conversion log

- **2026-10-07 — translation (T-FUNC card C-117, family `HT-022`).** One EES
  `FUNCTION` per `ht` correlation (4 functions), named as in `ht`, with the
  formula, the validity range as quoted by `ht`, the original reference and
  the `ht` module/function/version/commit in the comment block. Arguments are
  the Python arguments, all in SI (`m`, `m/s`, `kg/m3`, `Pa·s`) or
  dimensionless (rule 5 of `sources/ht/README.md` §7); no property function
  is used inside a function.
- `Nu_packed_bed_Gnielinski`: the optional `fa` became mandatory with the
  sentinel `fa <= 0` for the sphere default (EES `IF/THEN/ELSE`, the
  non-smooth switch, not a function call); the demonstration program calls
  both the default form (case *A*: 61.37823202546954, case *B*:
  29.452850852579207) and an explicit factor (case *A*: `fa = 2`,
  64.60866528996795, the regression value of
  `tests/test_conv_packed_bed.py`; case *B*: `fa = 2.1`, Raschig rings).
- `Nu_Achenbach`: the `Pr` argument is accepted but unused, exactly as in
  `ht` (neither its docstring formula nor its code uses it); the function
  comment says so.
- **No selector in this family**: all four members of `ht/conv_packed_bed.py`
  are correlations and all four are translated.
- **Level**: equations 25 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 1 → **level 1**; raised to **level 2** (± 1,
  docs/taxonomy.md §3), following the other `ht` function libraries of the
  library (`CSL-0087`, `CSL-0107`), since the user has to know packed-bed
  heat transfer to pick a correlation.
- `stats.n_equations = 25`: the `coolsolve` analysis of the whole file reports
  `Equations: 25`, `Variables: 25`, `System square: Yes`, `Largest block: 1`.
  The file is written directly in the model folder and solves with the given
  input values, so no `.initials` file is needed.

## Limitations and CoolSolve gaps

- The demonstration input sets are the `ht` doctest values (case *A*) and
  one realistic air bed (case *B*); `ht` checks no validity range in these
  functions, so the numbers of the *Results* and *Verification* tables are a
  check of the **equations**, not recommended design values (case *B*:
  `Re_B = 438.60` is inside every quoted range: Gnielinski 10⁻¹–10³,
  Wakao-Kagei 3–3000, KTA 100–10⁵ with voidage 0.38 in 0.36–0.42,
  Achenbach Re/voidage = 1154 < 7.7·10⁵).
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES
  (`FUNCTION`, `IF/THEN/ELSE`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` function library of
  the batch; same layout, comment blocks and demonstration program (two cases
  *A* doctest values and *B* Python values, README verification table
  `ht` vs CoolSolve).

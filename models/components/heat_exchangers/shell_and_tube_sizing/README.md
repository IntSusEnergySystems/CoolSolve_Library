# Shell-and-tube mechanical sizing: tube counts, bundle diameters and TEMA rules

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0110`

Thirteen EES `FUNCTION`s for the mechanical sizing of a shell-and-tube heat
exchanger, from the Python library [`ht`](https://github.com/CalebBell/ht):
the TEMA tubing check, the minimum bundle diameter, the shell-bundle
clearance, the baffle and support-plate thickness, the baffle hole diameter,
the maximum unsupported tube length, the rough tube counts of Perry's
Handbook, VDI Heat Atlas and HEDH with their bundle-diameter inverses, and
the two method dispatchers `Ntubes` and `size_bundle_from_tubecount`. These
are geometric estimates and TEMA table rules, not heat-transfer correlations;
they pair naturally with the shell-side correlations of `CSL-0095`/`CSL-0103`
and complete a sizing workflow together with `CSL-0090` (eps-NTU) and
`CSL-0105` (LMTD).

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | none (geometry and tabulated rules; no properties) |
| **Size** | 43 equations after analysis (largest block: 1); 13 functions |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/hx.py` (MIT); inventory row `HT-024` of `sources/ht/inventory.csv` |
| **Authors** | Caleb Bell and Contributors (library); the tabulated rules come from TEMA (9th ed., 2007), Perry's Chemical Engineers' Handbook (8th ed., 2007), the VDI Heat Atlas (2nd ed., 2010) and the HEDH (1983) |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (43 values, max deviation 2.4·10⁻¹³) |

## Problem statement

Given a tube outer diameter `Do`, a pitch, a layout angle (30/45/60/90
degrees) and a number of tube passes, how many tubes fit in a bundle of a
given outer diameter `DBundle`, and how large must the bundle be for a
wanted tube count? Around those tube counts, TEMA fixes the mechanical
details: which (NPS, BWG) tubing combinations are listed, the clearance
between shell and bundle, the baffle and support-plate thickness for the
shell diameter and the unsupported tube span, the baffle hole diameter, and
the maximum length a tube may span without a support.

## Model

| EES `FUNCTION` | Arguments | Content | Validity (as quoted in `ht`) |
|---|---|---|---|
| `check_tubing_TEMA` | NPS [inch], BWG [-] | returns 1 if the (NPS, BWG) tubing pair is listed by TEMA (29 listed pairs), else 0; `ht` returns a Boolean | TEMA tubing tables |
| `DBundle_min` | Do [m] | initial bundle diameter: 0.1 m (Do ≤ 0.01 m), 0.3 (≤ 0.014), 0.5 (≤ 0.02), 1.0 (≤ 0.03), else 1.5 m | rough guidance (lookup) |
| `shell_clearance` | mode [-], D [m] | shell–bundle clearance: mode = 1 reads the DShell table, mode = 0 the DBundle table; 0.0032 … 0.011 m | TEMA shell sizes |
| `baffle_thickness` | Dshell [m], L_unsupported [m], service [-] | baffle/support-plate thickness, tables 5×5 (service = 1: TEMA "R") and 5×6 (service = 0: "C"/"B"); 0.0016 … 0.0191 m | latitudinal baffles only |
| `D_baffle_holes` | Do [m], L_unsupported [m] | hole diameter = Do + 0.8 mm (Do > 0.0318 m or L_unsupported ≤ 0.914 m), else Do + 0.4 mm | TEMA, all geometries |
| `L_unsupported_max` | Do [m], material [-] | maximum unsupported tube span, 12-row table per material (material = 0: "CS", = 1: "aluminium"); 0.559 … 3.175 m | 1/4 ≤ Do ≤ 3 inch (optimistic below, as in `ht`) |
| `Ntubes_Perrys` | DBundle, Do [m], Ntp [-], angle [°] | quartic polynomial in C = 0.75·DBundle/Do − 36 (30/60°) or DBundle/Do − 36 (45/90°), one set of coefficients per Ntp; FLOOR(Nt) | Ntp = 1, 2, 4, 6; claimed accuracy 24 tubes |
| `Ntubes_VDI` | DBundle [m], Ntp, Do, pitch [m], angle [°] | closed-form rearrangement of the VDI equation (mm), factors f1 = 1.1/1.3 (layout), f2 = 0/22/70/90/105 (passes); FLOOR(N) | Ntp = 1, 2, 4, 8 (6 estimated by `ht`) |
| `D_for_Ntubes_VDI` | N, Ntp [-], Do, pitch [m], angle [°] | DBundle = √(f1·N·t² + f2·√N·t + Do) (mm → m), the inverse of `Ntubes_VDI` | as `Ntubes_VDI` |
| `Ntubes_HEDH` | DBundle, Do, pitch [m], angle [°] | N = FLOOR(0.78·(DBundle−Do)²/(C1·pitch²)), C1 = 13/15 (30/60°) or 1 (45/90°) | single-pass bundles |
| `DBundle_for_Ntubes_HEDH` | N, Do, pitch [m], angle [°] | DBundle = Do + (1/0.78)^0.5·pitch·(C1·N)^0.5, the inverse of `Ntubes_HEDH` | single-pass bundles |
| `Ntubes` | DBundle, Do, pitch [m], Ntp, angle [°], Method [-] | dispatcher: Method = 1 → `Ntubes_HEDH`, 2 → `Ntubes_VDI`, 3 → `Ntubes_Perrys` | those of the chosen method |
| `size_bundle_from_tubecount` | N, Do, pitch [m], Ntp, angle [°], Method [-] | dispatcher: Method = 1 → `DBundle_for_Ntubes_HEDH`, 2 → `D_for_Ntubes_VDI` | those of the chosen method |

The string options of `ht` (`service = 'R'/'C'/'B'`, `material = 'CS'/'aluminium'`,
`Method = 'Perry'/'VDI'/'HEDH'/'Phadkeb'`) became integer flags, documented in
each comment block (EES has no optional arguments; the flag makes the choice
explicit). The Python `int()` truncation of the tube counts became `FLOOR`
(the counts are positive, so the two agree).

Four members of the `ht` family are **not** translated, as decided by the
triage card: `get_tube_TEMA` (BWG wall-gauge table), `Ntubes_Phadkeb` and
`DBundle_for_Ntubes_Phadkeb` (highly accurate but backed by binary `.npy`
coefficient tables) and their helpers (`_load_coeffs_Phadkeb`,
`to_solve_Ntubes_Phadkeb`, `_tubecount_objf_Perry`). The default `"Phadkeb"`
method of `Ntubes`/`size_bundle_from_tubecount` is therefore unavailable; the
`"Perry"` inverse of `size_bundle_from_tubecount` is not in the function
either (it solves `Ntubes_Perrys` iteratively), but in EES the caller gets it
for free by making `DBundle` an unknown of the main program and writing
`Ntubes_Perrys(DBundle, Do, Ntp, angle) = N` — the idiomatic implicit solve.

Every function carries in its comment block (i) the equation or table, (ii)
the validity range as quoted by `ht`, (iii) the original source (TEMA 9th
edition 2007; Green & Perry, *Perry's Chemical Engineers' Handbook*, 8th
edition, McGraw-Hill, 2007, equation 11-74; *VDI Heat Atlas*, 2nd edition,
Springer, 2010; Schlunder & International Center for Heat and Mass Transfer,
*Heat Exchanger Design Handbook* (HEDH), Hemisphere, 1983) and (iv) the `ht`
module, function, version and commit the equations were taken from.

## How to run

Open `shell_and_tube_sizing.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./shell_and_tube_sizing.eescode
```

The demonstration program after the definitions calls each of the 13
functions at least twice: once (case *A*) with the input set of the `ht`
doctest of the corresponding function, once (case *B*) with a second input
set computed with the same Python functions (0.01905 m = 3/4 inch tubes,
pitch 0.0238 m, mixed layouts and pass counts). It solves without any
iteration (`Solver: SUCCESS (0 iterations)`, every equation explicit) and is
the regression baseline (`shell_and_tube_sizing.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these functions copies their
definitions in a block `{--- Library functions copied from CSL-0110 ---}` and
lists `CSL-0110` in its `related` field.

## Results

Values of the demonstration program (full precision in
`shell_and_tube_sizing.sol`):

| Quantity (case A) | Value | Quantity (case B) | Value |
|---|---:|---|---:|
| `check_tubing_TEMA` (2 inch, BWG 22) | 0 | `check_tubing_TEMA` (1.25 inch, BWG 18) | 0 |
| `check_tubing_TEMA_ok` (0.375 inch, BWG 22) | 1 | `check_tubing_TEMA_ok` (0.75 inch, BWG 16) | 1 |
| `DBundle_min` (Do = 0.0254 m) | 1.0 m | `DBundle_min` (Do = 0.015 m) | 0.5 m |
| `shell_clearance` (DBundle = 1.245 m) | 0.0064 m | `shell_clearance` (DBundle = 0.5 m) | 0.0048 m |
| `shell_clearance_DShell` (DShell = 1.9 m) | 0.0095 m | `shell_clearance_DShell` (DShell = 0.61 m) | 0.0048 m |
| `baffle_thickness_R` (Dshell = 0.3 m, L = 50, R) | 0.0095 m | `baffle_thickness_C` (Dshell = 1.2 m, L = 0.7 m) | 0.0095 m |
| | | `baffle_thickness_R` (Dshell = 1.2 m, L = 0.7 m) | 0.0095 m |
| `D_baffle_holes` (Do = 0.0508 m, L = 0.75 m) | 0.0516 m | `D_baffle_holes` (Do = 0.0254 m, L = 1.2 m) | 0.0258 m |
| `D_baffle_holes` (Do = 0.01905 m, L = 0.3 m) | 0.01985 m | | |
| `D_baffle_holes` (Do = 0.01905 m, L = 1.5 m) | 0.01945 m | | |
| `L_unsupported_max` (Do = 0.0254 m, CS) | 1.88 m | `L_unsupported_max` (Do = 0.01905 m, aluminium) | 1.321 m |
| | | `L_unsupported_max` (Do = 0.03 m, CS) | 1.88 m |
| `Ntubes_Perrys` (1.184 m, 28 mm, 2 p, 45°) | 803 | `Ntubes_Perrys` (0.8 m, 19.05 mm, 4 p, 30°) | 901 |
| | | `Ntubes_Perrys` (0.8 m, 19.05 mm, 2 p, 90°) | 792 |
| `Ntubes_VDI` (1.184 m, 2 p, 28 mm, 36 mm, 30°) | 966 | `Ntubes_VDI` (0.8 m, 4 p, 19.05 mm, 25 mm, 45°) | 729 |
| | | `Ntubes_VDI` (0.5 m, 1 p, 19.05 mm, 23.8 mm, 60°) | 401 |
| `D_for_Ntubes_VDI` (970 tubes, 2 p, 7.35 mm, 15 mm, 30°) | 0.500360 m | `D_for_Ntubes_VDI` (500, 4 p, 19.05 mm, 23.8 mm, 60°) | 0.590605 m |
| `Ntubes_HEDH` (1.184 m, 28 mm, 36 mm, 30°) | 928 | `Ntubes_HEDH` (0.8 m, 19.05 mm, 23.8 mm, 90°) | 839 |
| | | `Ntubes_HEDH` (0.5 m, 19.05 mm, 23.8 mm, 30°) | 367 |
| `DBundle_for_Ntubes_HEDH` (928, 28 mm, 36 mm, 30°) | 1.18399 m | `DBundle_for_Ntubes_HEDH` (600, 19.05 mm, 23.8 mm, 60°) | 0.633563 m |
| `Ntubes` (1.2 m, 25 mm, 31.25 mm, 1 p, 30°, Perry) | 1297 | `Ntubes` (0.8 m, 19.05 mm, 23.8 mm, 2 p, 30°, Perry) | 960 |
| `Ntubes` (…, VDI) | 1340 | `Ntubes` (…, VDI) | 1000 |
| `Ntubes` (…, HEDH) | 1272 | `Ntubes` (…, HEDH) | 969 |
| `size_bundle_VDI` (1285 tubes, 25 mm, 31.25 mm, 1 p, 30°) | 1.17490 m | `size_bundle_VDI` (800, 19.05 mm, 23.8 mm, 1 p, 30°) | 0.706036 m |
| `size_bundle_HEDH` (1285 tubes, 25 mm, 31.25 mm, 1 p, 30°) | 1.20581 m | `size_bundle_HEDH` (800, 19.05 mm, 23.8 mm, 1 p, 30°) | 0.728629 m |

The `ht` doctest of `baffle_thickness` passes `L_unsupported = 50` — an inch
value fed to a metre function in the original doctest itself; it only selects
the last column of the table, so it is reproduced as published.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. a
     parametric sweep of the tube count Ntubes_HEDH/VDI/Perry vs the bundle
     diameter for 25 mm tubes, pitch 31.25 mm, figures/shell_and_tube_sizing_ntubes.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/hx.py`, commit `85e0ee6`, imported from the local clone `~/git/ht`) for
case *A*, plus values computed with the same Python functions for case *B*.
The 43 output values of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
43 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0
```

The largest relative deviation over the 43 values is **2.4·10⁻¹³**
(`size_bundle_VDI_A`), i.e. round-off in the double-precision evaluation
(the `check_tubing_TEMA`, tube-count and table-value results are exact).

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `check_tubing_TEMA` | 0 (False) | 0 | exact |
| `check_tubing_TEMA_ok` | 1 (True) | 1 | exact |
| `DBundle_min` | 1.0 | 1.0 | exact |
| `shell_clearance` | 0.0064 | 0.0064 | exact |
| `shell_clearance_DShell` | 0.0095 | 0.0095 | exact |
| `baffle_thickness_R` | 0.0095 | 0.0095 | exact |
| `D_baffle_holes` (3 doctests) | 0.0516 / 0.01985 / 0.01945 | 0.0516 / 0.01985 / 0.01945 | exact |
| `L_unsupported_max` | 1.88 | 1.88 | exact |
| `Ntubes_Perrys` | 803 | 803 | exact |
| `Ntubes_VDI` | 966 | 966 | exact |
| `D_for_Ntubes_VDI` | 0.5003600119829544 | 0.5003600119830 | 9.1·10⁻¹⁴ |
| `Ntubes_HEDH` | 928 | 928 | exact |
| `DBundle_for_Ntubes_HEDH` | 1.1839930795640605 | 1.1839930795640 | 5.1·10⁻¹⁴ |
| `Ntubes` (Perry / VDI / HEDH) | 1297 / 1340 / 1272 | 1297 / 1340 / 1272 | exact |
| `size_bundle_from_tubecount` (VDI) | 1.1749025890472795 | 1.1749025890473 | 2.4·10⁻¹³ |
| `size_bundle_from_tubecount` (HEDH) | 1.205810838411941 | 1.2058108384119 | 4.9·10⁻¹⁴ |

Case *B* (second input set, computed with the same Python functions): all 26
values agree likewise — the largest relative deviation is 6.9·10⁻¹⁴
(`DBundle_for_Ntubes_HEDH_B`), all table and count results exact.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the shell-and-tube mechanical sizing functions of `ht`,
the heat-transfer component of ChEDL, file `ht/hx.py`, functions
`check_tubing_TEMA`, `DBundle_min`, `shell_clearance`, `baffle_thickness`,
`D_baffle_holes`, `L_unsupported_max`, `Ntubes_Perrys`, `Ntubes_VDI`,
`D_for_Ntubes_VDI`, `Ntubes_HEDH`, `DBundle_for_Ntubes_HEDH`, `Ntubes` and
`size_bundle_from_tubecount`, version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; the Python string options
(`service`, `material`, `Method`) became integer flags documented in each
comment block, `int()` truncation became `FLOOR`, the `ht` dispatcher
`Ntubes`/`size_bundle_from_tubecount` dispatch to the translated methods
only (flag 1/2/3), and the mm conversion of the VDI equations is done inside
the functions (SI arguments). No equation was changed. Scientific basis per
function: TEMA, *Standards of the Tubular Exchanger Manufacturers
Association*, 9th edition, 2007 (six functions); Green & Perry, *Perry's
Chemical Engineers' Handbook*, 8th edition, McGraw-Hill, 2007, equation
11-74; *VDI Heat Atlas*, 2nd edition, Springer, 2010; Schlunder, E. U. and
International Center for Heat and Mass Transfer, *Heat Exchanger Design
Handbook* (HEDH), Hemisphere, Washington, 1983.

## Conversion log

- **2026-10-08 — translation (T-FUNC card C-119, family `HT-024`).** One EES
  `FUNCTION` per `ht` function (13 functions, the card's list), named after
  the `ht` function, with the formula/table, the validity range as quoted by
  `ht`, the original source and the `ht` module/function/version/commit in
  the comment block.
- **String options → integer flags.** `shell_clearance`: `mode` (1 = D is
  DShell, 0 = D is DBundle — `ht` has two optional keyword arguments, EES has
  no optional arguments). `baffle_thickness`: `service` (1 = "R", 0 = "C" and
  "B"). `L_unsupported_max`: `material` (0 = "CS", 1 = "aluminium").
  `Ntubes`/`size_bundle_from_tubecount`: `Method` (1 = HEDH, 2 = VDI,
  3 = Perry; see below).
- **Table rules as cascades of single-line `IF`s** (the EES one-line form,
  valid EES): the 29 listed (NPS, BWG) pairs of `check_tubing_TEMA`, the
  threshold tables of `DBundle_min`, `shell_clearance` and
  `L_unsupported_max`, and the 2-D thickness tables of `baffle_thickness`
  (flattened with the row-major index k = 5·j + i for the 5-column "R" table
  and k = 6·j + i for the 6-column "C/B" table). No lookup table is used
  inside a function (`CS-GAP-LOOKUP-PROC`).
- **`D_for_Ntubes_VDI`: docstring/code discrepancy as in `ht`** — the code
  adds `Do` inside the root, the docstring prints a subtraction; the code
  (which reproduces the doctest 0.5003600119829544) is followed.
- **Dispatchers.** `Ntubes` and `size_bundle_from_tubecount` are translated
  as flag dispatchers calling the translated correlations (functions may
  call functions in CoolSolve; the ht string argument became the flag).
  Their `"Phadkeb"` default method is not translated (binary `.npy` tables,
  excluded by the triage) and the `"Perry"` inverse of
  `size_bundle_from_tubecount` is left to the caller as an implicit equation
  (see *Model*).
- **Tube counts are `FLOOR`ed** as Python `int()` truncates; all counts are
  positive so the semantics agree.
- **Level**: equations 43 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical no → 0, curated guesses no
  → 0. Score 1 → **level 1** (the blanket `level_guess = 2` of the triage
  sweep is refined by the actual score: 13 short geometric functions, no
  property input, no implicit loop).

## Limitations

- All tube counts and bundle diameters are **rough estimates** (Perry's:
  claimed accuracy 24 tubes, `ht` notes ~20–40 in practice; VDI and HEDH
  give no accuracy); use them for first sizing only, as in the sources.
- The excluded methods (`Phadkeb`, `get_tube_TEMA`) are the accurate ones:
  a model needing a graded tube count should take the TEMA-published counts
  or ship the `.npy` tables as CoolSolve lookup tables (possible follow-up,
  kept out of this card to stay table-free).
- `ht` raises `ValueError` for invalid flags (Ntp not in {1, 2, 4, 6, 8},
  angle not in {30, 45, 60, 90}, unknown material): the EES functions do not
  check, they document the valid inputs — as in the original tables.
- No gap registered for this card: everything is plain EES (`FUNCTION`,
  single-line and block `IF/THEN/ELSE`, `AND`/`OR`, `FLOOR`, `^`, functions
  calling functions) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family of the same
  triage and the layout pattern of this file (one `FUNCTION` per correlation,
  comment block with formula, validity and dual citation, demonstration
  program with doctest cases *A* and Python cases *B*).
- `CSL-0090` *hx_effectiveness_ntu* and `CSL-0105` *lmtd_and_f_correction*:
  the thermal side of the same design workflow — this file sizes the bundle,
  those give the eps-NTU relations and the LMTD/F factor of the exchanger.
- `CSL-0095` *tube_bank_nusselt*: shell-side/tube-bank heat-transfer
  coefficients for the bundle this file counts.
- `CSL-0103` *tube_bank_dp_bell_delaware*: the shell-side pressure drop
  (Kern, Bell-Delaware) of the same geometry — baffle spacing and clearances
  of this file are its geometric inputs.
- `CSL-0027` *shell_and_tube_steam_condenser*: a rated shell-and-tube
  condenser (30 000 tubes) whose tube count and shell size are of the kind
  this file estimates.
- `sources/labothappy` LTP-069/LTP-070 (LaboThapPy shell-and-tube sizing by
  particle-swarm optimisation): same intent, different method; the `ht`
  families are the correlation reference.

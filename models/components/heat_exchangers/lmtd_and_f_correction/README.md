# Log-mean temperature difference and its correction factors

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0105`

Three EES `FUNCTION`s for the rating of heat exchangers by the LMTD method:
`LMTD` (log-mean temperature difference of an ideal counterflow or co-current
exchanger), `F_LMTD_Fakheri` (Fakheri correction factor of a shell-and-tube
exchanger with one or several shell passes) and `Ft_aircooler` (Roetzel-Nicole
`Ft` factor of a crossflow air cooler with given tube passes and tube rows).
The arguments are the four end temperatures (only differences and ratios
enter, so any consistent unit gives the same result; they are shown in °C)
plus dimensionless flags and counts (`counterflow` 1/0, `shells`, `Ntp`,
`rows`). This is the `HT-019` family of the `ht` triage (roadmap card C-114);
same layout and same comment blocks as the first family, `CSL-0087`
*internal_turbulent_nusselt*.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | none (the relations are fluid-independent; end temperatures are arguments) |
| **Size** | 20 equations after analysis (largest block: 1); 3 functions of 10–130 lines (`Ft_aircooler` carries the eight 16-coefficient sets) |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), files `ht/core.py`, `ht/hx.py`, `ht/air_cooler.py` (MIT); inventory row `HT-019` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the relations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (16 values, max deviation 5.4·10⁻¹⁴) |

## Problem statement

For given end temperatures of the hot stream (`Thi`, `Tho`) and the cold
stream (`Tci`, `Tco`) of a heat exchanger, compute the log-mean temperature
difference of the equivalent ideal exchanger and, for a shell-and-tube or an
air-cooler geometry, its correction factor `F ≤ 1` (the true mean difference
is `F·LMTD`). Three relations are available: the ideal LMTD itself
(counterflow or co-current), the Fakheri closed form for shell-and-tube
exchangers, and the Roetzel-Nicole fit for crossflow air coolers; the choice
between them is left to the user, who knows the geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `LMTD` | Thi, Tho, Tci, Tco, counterflow | counterflow: dT_1 = Thi − Tco, dT_2 = Tho − Tci; co-current: dT_1 = Thi − Tci, dT_2 = Tho − Tco; LMTD = (dT_2 − dT_1)/LN(dT_2/dT_1); counterflow limit (ratio ≤ 0 or = 1): dT_1; co-current limit: 0 | no limit quoted |
| `F_LMTD_Fakheri` | Thi, Tho, Tci, Tco, shells | R = (Thi − Tho)/(Tco − Tci), P = (Tco − Tci)/(Thi − Tci), W = ((1 − P·R)/(1 − P))^(1/shells), S = √(R² + 1)/(R − 1); Ft = S·LN(W)/LN((1 + W − S + S·W)/(1 + W + S − S·W)); R = 1: W2 = (shells − shells·P)/(shells − shells·P + P), Ft = √2·(1 − W2)/W2/LN((W2/(1 − W2) + 1/√2)/(W2/(1 − W2) − 1/√2)) | one or an even number of tube passes; no temperature limit quoted |
| `Ft_aircooler` | Thi, Tho, Tci, Tco, Ntp, rows | Ft = 1 − Σ_{k=1..4} q^k·Σ_{i=1..4} c_{k,i}·SIN(i·φ); q = 1 − r_lm, r_lm = dT_lm/(Thi − Tci), dT_lm = counterflow LMTD, φ = 2·ARCTAN(R), R = (Thi − Tho)/(Tco − Tci); c_{k,i}: the 16-coefficient set of the (Ntp, rows) pair | fitted air coolers up to 4 rows and 4 passes (other combinations reuse the nearest set, as in the original); fit error < 0.1 % |

Arguments: `Thi`, `Tho` (hot inlet and outlet temperatures, `[C]`), `Tci`,
`Tco` (cold inlet and outlet temperatures, `[C]`), `counterflow` (1 for
counterflow, 0 for co-current — EES has no boolean arguments, so the Python
flag is an integer), `shells` (number of shell-side passes, `[-]`), `Ntp`
(number of tube passes, `[-]`) and `rows` (number of tube rows, `[-]`).

Every function carries in its comment block (i) the equation, (ii) the
validity range **as quoted by `ht`**, (iii) the original paper or book and
(iv) the `ht` module, function, version and commit it was taken from.

No dispatcher of `ht` is involved: `ht` ships no selector over these three
relations (the `LMTD` flag and the `(Ntp, rows)` table choice are arguments,
not dispatchers); the caller chooses the `FUNCTION` directly.

## How to run

Open `lmtd_and_f_correction.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./lmtd_and_f_correction.eescode
```

The demonstration program after the definitions calls each of the 3
functions, once (case *A*) with the input set of the `ht` doctest of the
corresponding relation, once (case *B*) with one coherent shell-and-tube /
air-cooler rating point (Thi = 150 °C, Tho = 90 °C, Tci = 20 °C,
Tco = 60 °C; the `Ft` calls span the 1-row-1-pass, 2-rows-2-passes,
3-rows-3-passes, 4-rows-2-passes and 6-rows-1-pass sets, and the Fakheri
calls span one shell pass, two shell passes and the singular branch R = 1).
It solves without any iteration (`Solver: SUCCESS (0 iterations)`, every
equation is explicit) and is the regression baseline
(`lmtd_and_f_correction.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these relations copies their
definitions in a block `{--- Library functions copied from CSL-0105 ---}` and
lists `CSL-0105` in its `related` field.

## Results

Values of the demonstration program (full precision in
`lmtd_and_f_correction.sol`):

| Quantity (case A) | Value | Quantity (case B) | Value |
|---|---:|---|---:|
| `LMTD_cf_A` (counterflow) | 43.2004 K | `LMTD_cf_B` (counterflow) | 79.5816 K |
| `LMTD_coc_A` (co-current) | 39.7525 K | `LMTD_coc_B` (co-current) | 68.1971 K |
| `LMTD_eq_A` (equal differences) | 40.0 K | `F_Fakheri_B` (1 shell) | 0.933054 |
| `LMTD_eqcoc_A` (equal differences) | 0.0 K | `F_Fakheri_2shells_B` (2 shells) | 0.983993 |
| `F_Fakheri_A` (1 shell) | 0.943836 | `F_Fakheri_R1_B` (R = 1) | 0.967241 |
| `Ft_aircooler_A` (1 pass, 4 rows) | 0.550509 | `Ft_1r1p_B` | 0.948192 |
| | | `Ft_2r2p_B` | 0.985107 |
| | | `Ft_3r3p_B` | 0.991153 |
| | | `Ft_4r2p_B` | 0.983244 |
| | | `Ft_6r1p_B` (4-row set) | 0.952585 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): a parametric
      sweep plot, e.g. Ft vs R for the Fakheri factor and the air-cooler sets,
      figures/lmtd_and_f_correction_ft.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/core.py`, `ht/hx.py`, `ht/air_cooler.py`, commit `85e0ee6`, installed
from the local clone in a throw-away virtual environment) for case *A*, plus
values computed with the same Python functions for case *B*. The 16 output
values of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
16 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 4
```

(the 4 “only in CoolSolve” variables are the 4 inputs of the demonstration
program — `Thi_B`, `Tho_B`, `Tci_B`, `Tco_B` —; the reference table holds
only the 16 outputs). The largest relative deviation over the 16 values is
**5.4·10⁻¹⁴** (`Ft_aircooler_A`), i.e. round-off in the double-precision
evaluation.

Per-function values, `ht` / CoolSolve:

| Function | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `LMTD_cf_A` | 43.200409294132 | 43.200409294130 | 3.5e-14 |
| `LMTD_coc_A` | 39.752511180490 | 39.752511180490 | 7.2e-16 |
| `LMTD_eq_A` | 40.0 | 40.0 | 0 |
| `LMTD_eqcoc_A` | 0.0 | 0.0 | 0 |
| `F_Fakheri_A` | 0.943835882965 | 0.943835882965 | 7.1e-15 |
| `Ft_aircooler_A` | 0.550509360409 | 0.550509360409 | 5.3e-14 |
| `LMTD_cf_B` | 79.581582867360 | 79.581582867360 | 6.3e-15 |
| `LMTD_coc_B` | 68.197143841071 | 68.197143841070 | 1.7e-14 |
| `F_Fakheri_B` | 0.933053631357 | 0.933053631357 | 2.6e-14 |
| `F_Fakheri_2shells_B` | 0.983992765817 | 0.983992765817 | 2.4e-14 |
| `F_Fakheri_R1_B` | 0.967241282186 | 0.967241282186 | 3.0e-14 |
| `Ft_1r1p_B` | 0.948192436916 | 0.948192436916 | 4.3e-14 |
| `Ft_2r2p_B` | 0.985107391468 | 0.985107391468 | 4.7e-14 |
| `Ft_3r3p_B` | 0.991153373690 | 0.991153373690 | 3.4e-14 |
| `Ft_4r2p_B` | 0.983244433197 | 0.983244433197 | 4.4e-14 |
| `Ft_6r1p_B` | 0.952585379882 | 0.952585379882 | 1.7e-14 |

All 16 relative deviations are below 5.4·10⁻¹⁴.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the LMTD relations of `ht`, the heat-transfer component
of ChEDL, file `ht/core.py`, function `LMTD`; file `ht/hx.py`, function
`F_LMTD_Fakheri`; file `ht/air_cooler.py`, function `Ft_aircooler`, version
1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; each relation became one EES
`FUNCTION` named as in `ht`; the Python boolean argument `counterflow` of
`LMTD` became an explicit 1/0 flag with the branch choice made by nested EES
`IF` blocks (the non-smooth limit switch, not a function call); the Python
`log` became the EES `LN`; the 4×4 Roetzel-Nicole coefficient tables of
`Ft_aircooler` became 16 scalar assignments per `(Ntp, rows)` set selected by
a nested `IF/ELSE` chain that follows the branch order of the `ht` code
(including its two "reasonable assumption" reuses and its fall-through
default); the radian composition `sin((i+1)·2·atan(R))` became
`SIN((i+1)·2·ARCTAN(R))`, which is identical since `SIN` takes degrees and
`ARCTAN` returns degrees in EES and CoolSolve; the counterflow `LMTD` inside
`Ft_aircooler` is evaluated by calling the `LMTD` function of this file, as
in the original. No equation was changed. Scientific basis per function: the
original paper or book quoted in its comment block.

The scientific authors of the relations are credited in the comment block of
each function and in `model.json` (`origin.authors`): Bergman, Lavine,
Incropera and DeWitt, *Introduction to Heat Transfer*, 6E, Wiley, 2011
(`LMTD`); Fakheri, *Journal of Heat Transfer* 125(3), 2003 (`F_LMTD_Fakheri`);
Roetzel and Nicole, *Journal of Heat Transfer* 97(1), 1975 (`Ft_aircooler`).

## Conversion log

- **2026-10-07 — translation (T-FUNC card C-114, family `HT-019`).** One EES
  `FUNCTION` per `ht` relation (3 functions), named as in `ht`, with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in the comment block. Arguments are the
  Python arguments, all in SI (°C for the four end temperatures — only
  differences and ratios enter, so any consistent unit gives the same result)
  or dimensionless (rule 5 of `sources/ht/README.md` §7); no property function
  is used inside a function.
- `LMTD`: the boolean `counterflow` flag is a **1/0 integer argument** and the
  choice of the end differences and of the limit branch is made with nested
  EES `IF` blocks (the library convention for a non-smooth switch,
  `CSL-0101`); the exact-equality test `ratio = 1` is the one of the `ht`
  code, which is what reproduces its limit values 40.0 and 0.0.
- `F_LMTD_Fakheri`: the exact-equality test `R_F = 1` is the one of the `ht`
  code; the demonstration program exercises the singular branch with
  Thi = 130 °C, Tho = 95 °C, Tci = 15 °C, Tco = 50 °C (R = 1 exactly).
- `Ft_aircooler`: the eight coefficient sets are written out as scalar
  assignments (EES functions have no local arrays); the selection chain
  follows the `if/elif/else` order of the `ht` code, including the reuse of
  the 4-row-1-pass set for `Ntp = 1, rows > 4` (exercised with rows = 6), the
  reuse of the 4-row-4-pass set for `Ntp = rows > 4`, and the fall-through to
  the 4-rows-2-passes set (exercised with `Ntp = 2, rows = 4`).
- **No selector translated**: `ht` ships no dispatcher over these three
  relations (unlike the convection families); the `counterflow` flag and the
  `(Ntp, rows)` table choice are arguments of the functions themselves.
- **Level**: equations 20 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 1 → **level 1**; raised to **level 2** (± 1,
  docs/taxonomy.md §3), the reading of the other `ht` function libraries of
  the library (`CSL-0087`, `CSL-0101`), since the user has to know three data
  bases, validity ranges and three exchanger geometries to pick a relation.
- `stats.n_equations = 20`: the `coolsolve` analysis of the whole file reports
  `Equations: 20`, `Variables: 20`, `System square: Yes`, `Largest block: 1`.
  The file is written directly in the model folder and solves with the given
  input values, so no `.initials` file is needed.

## Limitations and CoolSolve gaps

- The demonstration input sets are chosen to be realistic, not to stay inside
  every quoted validity range: case *B* reuses one rating point for all three
  relations (a shell-and-tube point for `F_LMTD_Fakheri`, an air-cooler point
  for `Ft_aircooler`), as `ht` does not check the ranges; the numbers of the
  *Results* and *Verification* tables are a check of the **equations**, not
  recommended design values. The validity column of the table above is the one
  to use when choosing an input.
- `Ft_aircooler` assumes the hot fluid is tubeside, as in an air cooler; the
  model is not symmetric, as stated by `ht` — swap the inputs when the cold
  fluid is tubeside.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  relations copies the definitions for now.
- No gap registered for this card: everything is plain EES
  (`FUNCTION`, nested `IF/THEN/ELSE` with `AND`/`OR`, `LN`, `SQRT`, `SIN`,
  `ARCTAN`, function-to-function call) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations of the
  same `ht` triage (same file `ht/hx.py`, same layout); a rating model uses
  either the LMTD method of this file or the ε-NTU method of that one.
- `CSL-0102` *hx_temperature_effectiveness_pntu*: the P-NTU temperature
  effectiveness relations of the same `ht` triage, including the TEMA E/G/H/J
  shell-and-tube branches that complement the Fakheri factor of this file.
- `CSL-0099` *air_cooler_air_side*: the finned-bundle air-side correlations
  of the same `ht` module (`ht/air_cooler.py`), same layout; its `Ft` factor
  is the `Ft_aircooler` function of this file.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` function library of
  the batch; same layout, comment blocks and demonstration program.
- `CSL-0002` *counterflow_hx_oil_water*, `CSL-0026`
  *crossflow_hx_hot_gas_water*, `CSL-0027`
  *shell_and_tube_steam_condenser*: three rated heat exchangers that would
  use the LMTD relations of this file as an alternative to ε-NTU.

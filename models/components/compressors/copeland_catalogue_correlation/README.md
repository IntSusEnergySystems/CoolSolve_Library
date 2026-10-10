# ARI/Copeland catalogue polynomial for scroll compressors (function library)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0123`

`FUNCTION copeland_ari(table$, coef$, T_ev, T_cd)` evaluates the ARI 10-coefficient
third-order catalogue polynomial of a Copeland scroll compressor. It is the
compressor correlation that the Vitocal 300-G heat pump model `CSL-0116` calls
in its `'ari'` mode. Five catalogue tables recovered from the source file ship
with the library: ZH15K4E-TFD, ZH21K4E-TFD, ZH38K4E-TFD, ZH45K4E-TFD and
ZRD42KCE-TFD_copy, each with the columns `W` (electrical power [W]), `A`
(a second power column [W], meaning not stated in the source), `M` (refrigerant
mass flow [lbm/hr]) and `Vs` (swept volume per revolution, read at row 1
[cm³]).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Kind / level** | Function library (one FUNCTION + demonstration program), level 1 |
| **Fluids** | R134a (demonstration only; the correlation itself is fluid-independent) |
| **Size** | 19 equations, all explicit (largest block: 1); 1 FUNCTION |
| **Source** | ULiège Thermodynamics Laboratory — `ARI compressor correlation.EES` (procedures EES folder) |
| **Authors** | Sylvain Quoilin (ULiège Thermodynamics Laboratory) — folder convention of the collection; the `{$ID$}` tag names the EES licence (Laboratoire de Thermodynamique, ULiège), not the author |
| **License** | MIT |
| **CoolSolve** | 0.3.0@d5d6b37 (branch `fix/library-gaps-2`) — the native file runs and returns the same values as the former variant (`CS-BUG-LOOKUP-COL-ARG` closed); status **runs**: the property states agree with the EES stored solution, the catalogue-dependent outputs have no reference (see *Verification*) |

## The function

- Inputs: `table$` catalogue name (one of the five tables below), `coef$`
  column name (`'W'`, `'M'`, …), `T_ev`, `T_cd` evaporation/condensation
  temperatures [°C].
- The function converts the temperatures to Fahrenheit, reads the ten
  coefficients C0…C9 from rows 1…10 of the column, and returns
  `C0 + C1·TevF + C2·TcdF + C3·TevF² + C4·TevF·TcdF + C5·TcdF² + C6·TevF³ +
  C7·TcdF·TevF² + C8·TevF·TcdF² + C9·TcdF³` — the ARI rating polynomial.
- Catalogue tables (companion CSVs of this model, 10 rows each):

| Table | `Vs` row 1 [cm³] | File |
|---|---:|---|
| ZH15K4E-TFD | 180.09 | `copeland_catalogue_correlation-ZH15K4E-TFD.csv` |
| ZH21K4E-TFD | 139.85 | `copeland_catalogue_correlation-ZH21K4E-TFD.csv` |
| ZH38K4E-TFD | 211.22 | `copeland_catalogue_correlation-ZH38K4E-TFD.csv` |
| ZH45K4E-TFD | 227.04 | `copeland_catalogue_correlation-ZH45K4E-TFD.csv` |
| ZRD42KCE-TFD_copy | 268.30 | `copeland_catalogue_correlation-ZRD42KCE-TFD_copy.csv` |

## Demonstration program

The main program of the source file, at its operating point: R134a,
evaporation at 3 bar (superheating 5 K), condensation at 20 bar. The exhaust
state equations of the original (`h_ex_cp = h_su_cp + W_dot/M_dot` and the
`(p,h)` temperature call) are not part of the demonstration: with the
catalogues embedded in the source file the catalogue power is ≈ 3× the power
of the stored run and `W/M` leaves the range of the fluid (next section).

| Variable | Value | Variable | Value |
|---|---:|---|---:|
| `T_ev` | 0.672 °C | `W_dot` (catalogue, ZH38K4E-TFD) | 11 270.1 W |
| `T_cd` | 67.481 °C | `M_lbmhr` / `M_dot` | 4.283 lbm/hr / 5.397e-4 kg/s |
| `Vs` | 211.22 cm³ | `epsilon_v` | 3.549e-3 |
| `W_dot_zh45` (ZH45K4E-TFD) | 20 631.9 W | `W_err` (self-check) | 0 |

(Values of the native file, CoolSolve 0.3.0@d5d6b37; before the fix of
`CS-BUG-LOOKUP-COL-ARG` it returned the first column for `M_lbmhr`, 11 270 lbm/hr,
and `M_dot` was wrong by four orders of magnitude.) `W_err` is the difference between `W_dot`
and the same polynomial recomputed in the main program: 0 exactly, so the
function and its table read are exact.

## Results

The values above are what the catalogues embedded in the source file give at
the demonstration point. They are **not** the values of the EES stored
solution of the source file — see the next section.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): catalogue power vs condensing
     temperature (parametric sweep calling copeland_ari); function library - add if useful -->

## Verification

**The stored EES solution cannot be reproduced, by construction of the
collection: the catalogue table it used is not in it.** Hand decoding of the
binary (80-bit Extended runs between the variable records and the plot data —
the embedded-table heuristic of `ees_extract.py` reports five spurious
242×2 "M/index" tables for this file and finds no lookup table) recovered six
catalogue blocks, five of them named. All five named tables have `Vs` row 1 =
139–335 cm³, while **both** stored runs that call this correlation (this file
and TM-0596/CSL-0116) read `Vs` = **82.61 cm³**, and their catalogue powers
(3449.9 W / 3004.2 W) are a factor ≈ 3–4 below what the embedded tables give
at the same points (11 266 W / 12 100 W for ZH38K4E-TFD). The stored runs
therefore used an older, external version of the `ZH38K4E-TFD` table (an
external `.lkt` resolved by name; none exists anywhere in
`~/Nextcloud/thermo_models/`), which the file does not embed and the
collection does not keep. The same conclusion was reached independently for
TM-0596 at import (CSL-0116 README, *How to run*); the four coefficient sets
embedded there evaluate to the same values as the ZH15/21/38/45 tables
recovered here (5.84 / 3.98 / 2.70 / 4.73 at its stored point).

What **is** compared with the stored solution of the source file
(`compare_solution.py` on the native file, re-run on 2026-10-10 with CoolSolve
0.3.0@d5d6b37; 12 common variables; the former variant gave the same table):

| Variable | EES stored | CoolSolve | Deviation | Explanation |
|---|---:|---:|---|---|
| `T_ev` | 0.6527 °C | 0.6721 °C | 0.019 K | saturation pressure call, EES 9 vs CoolProp R134a (absolute difference, 2.9 % relative near 0 °C) |
| `T_cd` | 67.452 °C | 67.481 °C | 0.028 K | same |
| `T_su_cp` | 5.653 °C | 5.672 °C | 0.019 K | follows from `T_ev` |
| `v_su_cp` | 0.069445 m³/kg | 0.069453 m³/kg | 0.011 % | within the property tolerance |
| `h_su_cp` | 255 313 J/kg | 403 477 J/kg | 148.16 kJ/kg | reference-state offset of R134a between EES 9 and CoolProp (enthalpy differences and derived results unaffected; the original exhaust-state equations are excluded from the demo, see above) |
| `W_dot`, `M_lbmhr`, `Vs`, `epsilon_v` | 3449.9 W, 437.70 lbm/hr, 82.61 cm³, 0.9272 | 11 270.1 W, 4.283 lbm/hr, 211.22 cm³, 3.549e-3 | factor 3–4 / 102 | catalogue vintage: the stored run's table version is absent (see above) |

Status **`runs`**, not `verified`. The native file now solves as written
(`SUCCESS`, 0 iterations, 20 equations in 20 blocks of size 1), and its `.sol`
equals the one of the former `_coolsolve` variant on all 13 variables (max
relative difference 2e-12, on `h_su_cp`). The function is exact where an exact
reference exists (`W_err` = 0; the recovered tables reproduce the coefficients
bit-for-bit from the binary; the `M` polynomial recomputed in Python from the
shipped CSV agrees to the last digit) and the property calls agree within the
property tolerances; but the catalogue-dependent outputs (`W_dot`, `M_dot`,
`Vs`, `epsilon_v`: the purpose of the model) differ from the EES stored
solution by the factor 3–4 / 102 explained above and cannot be checked against
an independent reference, because the reference table is lost. As for the other
models of the library whose stored solution cannot be reproduced for a
documented reason (`CSL-0067`, `CSL-0112`, `CSL-0114`), the status is `runs`.
(Before the re-check the native file was `blocked` and the variant was the
checked file; the numbers above are identical.)

## Source and attribution

`~/Nextcloud/thermo_models/procedures EES/ARI compressor correlation.EES`
(EES 9.493, comments in English, inventory candidate `TM-0560`), ULiège
Thermodynamics Laboratory collection of S. Quoilin, published under the
library licence (MIT). The catalogue correlation follows the ARI rating
polynomial of the Copeland ZH scroll-compressor data sheets; the file names
no author (initials `SQ` by the folder convention of the collection).

## Conversion log

- **Function name**: the function is shipped as `copeland_ari` (the unique-function-name
  rule, docs/model_workflow.md §4.4): `CSL-0116` carries a copied `copeland` block
  until `CS-FEAT-IMPORT` exists; models that copy this function should use
  `copeland_ari` or rename it locally.
- **2026-10-07 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-C-Pa-J; decimal comma in the stored text converted
  by the extractor; `{$ID$}` licence tag removed. Function, main program and
  comments kept (already English).
- **Tables recovered by hand** (the extractor's embedded-table heuristic
  finds none): six blocks of five 10-value Extended-float columns between the
  variable records and the plot data, five with their table names
  (ZH15K4E-TFD, ZH21K4E-TFD, ZH38K4E-TFD, ZH45K4E-TFD, "ZRD42KCE-TFD(copy)")
  in short-string form after each block; the sixth block has no name, no
  index column and no descriptor and was **not** shipped (noted here for the
  record). Each table = columns W, A, M, Vs × 10 rows, plus a string column
  `index` ("1"…"10") that the function does not use and the companion CSVs
  omit. `ZRD42KCE-TFD(copy)` renamed `ZRD42KCE-TFD_copy` (file-name-safe
  table name). The import shipped a second copy of the tables for the variant
  (`copeland_catalogue_correlation_coolsolve-<table>.csv`, identical values;
  removed on 2026-10-10 with the variant).
- **`until (i>9)`**: the original writes `until i>9` without parentheses —
  registered gap `CS-GAP-REPEAT-UNTIL-BARE`; the parenthesised form (valid
  EES as well) is used. Note: a trailing comment after `until (i>9)` on the
  same line is rejected by the CoolSolve parser even in the parenthesised
  form (the comment was moved to its own line; unverified suggestion, see
  above).
- **`convert(lbm/hr,kg/s)`**: the original converts the `M` column with
  `convert(lbm/hr,kg/s)`. CoolSolve returns **1** for this conversion, quoted
  or not (new bug `CS-BUG-CONVERT-UNIT`: 1 lbm/hr = 1.259978805556e-4 kg/s
  applied by EES, see its stored `M_dot`); the demonstration multiplies by
  the exact factor `0.0001259978805556` instead ([ees_import.md
  §6.2](https://github.com/CoolProp/CoolSolve/blob/main/docs/ees_import.md):
  prefer converted numbers), keeping the file runnable and correct.
- **Exhaust-state equations of the original demo omitted** (see
  *Demonstration program*): with the embedded catalogues `W_dot/M_dot` ≈
  20.9 MJ/kg and the `(p,h)` call leaves the fluid range — a consequence of
  the catalogue vintage, not of the function.
- **Blocked native file + runnable variant (import, superseded)**: the native
  `copeland_catalogue_correlation.eescode` keeps the verbatim function and was
  blocked by `CS-BUG-LOOKUP-COL-ARG`; the variant
  `copeland_catalogue_correlation_coolsolve.eescode` (+ `.sol`, + its own
  copies of the five tables) mapped `coef$` to the column number of the
  shipped tables (W=1, A=2, M=3, Vs=4) with four single-line `IF`s, the only
  change.
- **2026-10-10 — re-check (`T-RECHECK`) with CoolSolve `fix/library-gaps-2`
  @d5d6b37**: `CS-BUG-LOOKUP-COL-ARG` is closed (a string expression as the
  column argument of `lookup` is read as a name, in the main program and in a
  FUNCTION body; the earlier `CS-GAP-LOOKUP-PROC` is closed too). The native
  file solves as written and equals the variant on all 13 variables, so the
  variant (`.eescode`, `.sol` and its five table copies) was removed and the
  native `.sol` replaced (the former one held the wrong first-column values).
  Status `blocked` → `runs`; no equation of the native file changed. Models
  that copy the function before `CS-FEAT-IMPORT` exists can now copy the
  native version.
- **Level**: score of docs/taxonomy.md §3 — equations 19 (< 50) → 0;
  largest block 1 → 0; a FUNCTION definition → 1; no multi-zone/discretised
  structure → 0; explicit catalogue correlation, no calibration inside the
  model → 0; no curated guesses (0 iterations) → 0. Total 1 → level 1.

## Limitations and CoolSolve notes

- **`CS-BUG-LOOKUP-COL-ARG`** — **closed** in CoolSolve `fix/library-gaps-2`
  (commit `d5d6b37`). It was found by this model: inside a FUNCTION/PROCEDURE
  body, `lookup(table$, row, col$)` with the column given as a **name string**
  ignored it and returned the first column, so the native file's
  `C[i] = lookup(table$, i+1, coef$)` silently returned the `W` coefficients
  for every column (`M_lbmhr` = `W_dot` = 11 270.07, the mass flow wrong by 4
  orders of magnitude with no warning). Valid EES: the stored solution of the
  source file proves EES reads the `M` column (`M_dot` = 437.70 lbm/hr, while
  the `W` polynomial gives 3449.9 W). The native file now returns
  `M_lbmhr` = 4.283 for the recovered ZH38K4E-TFD table. No gap is left
  (`missing_features` is empty).
- `lookup(table$, …)` with the table name passed **as an argument** resolved
  the companion table already in CoolSolve v0.3.0@7addbbc (checked with a probe
  before the import); a literal table name inside a FUNCTION hit
  `CS-GAP-LOOKUP-PROC`, also closed in `fix/library-gaps-2`.
- Unverified suggestions (not registered, no evidence of EES validity at
  hand): a trailing comment after `until (…)` in a `REPEAT` loop is rejected
  by the CoolSolve parser (this import moved the comment to its own line).

## Related models

- `CSL-0116` *heat_pump_vitocal_300g*: the heat-pump model that calls this
  correlation in its `'ari'` compressor mode (its native file stays blocked;
  see its README for why the recovered catalogues do not lift the block).
- `CSL-0007` *scroll_compressor_semi_empirical*: the Winandy et al. (2002)
  semi-empirical scroll compressor identified on catalogue data (the other
  compressor model of the same heat-pump studies).
- `CSL-0157` *reciprocating_catalogue_r717*: the same catalogue-data approach
  (effectiveness maps from manufacturer rows) for the R717 reciprocating
  member of the same 2002 Laborelec 5-file family, as a `DUPLICATE` array
  model instead of a correlation function.

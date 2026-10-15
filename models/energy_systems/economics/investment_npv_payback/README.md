# Economic evaluation of an energy-saving investment: net present value and simple payback time

🟢 **Level 1 · Introductory** | ⚙️ **Steady-state** | ⛔ **Blocked** | `CSL-0154`

<!-- Badges (copy exactly, see docs/taxonomy.md):
  🟢 **Level 1 · Introductory** | 🔵 **Level 2 · Intermediate** | 🟠 **Level 3 · Advanced** | 🔴 **Level 4 · Research**
  ⚙️ **Steady-state** | ⏱️ **Dynamic** | 🎯 **Optimisation** | 🧩 **Function library**
  ✅ **Verified** | ⚠️ **Runs (modified)** | ⛔ **Blocked** | ❌ **Failing** | 📄 **Documented only**
-->

Year-by-year cash flow of an energy-saving measure over its lifetime, with the
two classic payback methods: the discounted cash flow (DCF) method, whose
accumulated net present value `NPV_1[i]` tells in which year the discounted
investment is recovered, and the simple (undiscounted) payback method, whose
accumulated cash flow `NPV_2[i]` crosses zero at the payback time `PBT_2`. The
model is a small economic model with no thermodynamics: it is meant to be
combined with an energy model that provides the yearly costs and benefits of a
measure (e.g. the equipment cost model of `CSL-0153`).

| | |
|---|---|
| **Category** | Energy systems › Economics |
| **Fluids** | none (economic model, currencies in €) |
| **Size** | 176 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/modeles/Economical_evaluation_of_investment/INVESTISSEMENT_RENTABILITE_SB080108.EES` (EES 7.888) |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@2d15382 — native file blocked by `CS-BUG-DUPLICATE-INDEX-EXPR`; the runnable variant `investment_npv_payback_coolsolve.eescode` reproduces the EES stored solution |

## Problem statement

Economic evaluation of an energy-saving measure (a renovation, a heat
recovery, a boiler replacement…): given the initial investment and the yearly
benefit (avoided energy cost) and running cost (electricity) of the measure,
decide whether the investment is profitable and when it is paid back. The
model is the one distributed with the ULiège course *Machines et systèmes
thermiques*; it is parameterised by hand (investment, first-year inflow and
outflow, lifetime, escalation rates and discount rate) and produces the two
payback series year by year.

## Model

Notations of the original file (kept as is): `T_lifetime` [year], `j_fuel`
escalation of the benefit [-], `j_el` escalation of the cost [-], `k`
capital cost / discount rate [-], `INV` [€], `inflow_1` and `outflow_1` [€] the
benefit and the cost of the first year.

*Discounted cash flow method* (arrays indexed by the year `i`, year 0 being the
investment date):

$$ B[i] = B[1]\,(1+j_{fuel})^{i-1},\qquad C[i] = C[1]\,(1+j_{el})^{i-1} $$
$$ CF[i] = B[i] - C[i] $$
$$ DPV_1[i] = DPV_1[i-1] + CF[i]\,(1+k)^{-i},\qquad NPV_1[i] = -INV + DPV_1[i] $$

*Pay-back time method* (no discounting, as in the original: the cash flow of
the first year is repeated over the whole lifetime):

$$ PBT_2 = \frac{INV}{B[1]-C[1]},\qquad DPV_2[i] = DPV_2[i-1] + (B[1]-C[1]),\qquad NPV_2[i] = -INV + DPV_2[i] $$

`NPV_1[i]` becomes positive in the payback year (discounted payback), while
`NPV_2[i]` is zero in the year of the simple payback time `PBT_2`.

| Input | Value | Meaning |
|---|---|---|
| `INV` | 20 000 € | initial investment |
| `inflow_1` | 4 000 €/year | first-year benefit |
| `outflow_1` | 2 000 €/year | first-year cost |
| `T_lifetime` | 20 year | lifetime of the measure |
| `j_fuel` | 0.045 /year | escalation of the energy cost (original: 3–6 % fossil, 5–10 % biomass) |
| `j_el` | 0.03 /year | escalation of the electricity cost (original: 1–3 %) |
| `k` | 0.08 /year | discount rate |

No property call, no iterative block: every equation is explicit, so no
`.initials` file is needed.

## How to run

```bash
coolsolve investment_npv_payback_coolsolve.eescode   # runnable variant (tested as CSL-0154:coolsolve)
```

The **native file** `investment_npv_payback.eescode` is the faithful import and
**does not run in CoolSolve**: the two cumulative recurrences use an array index
with arithmetic inside a `DUPLICATE` loop (`DPV_1[i] = DPV_1[i-1] + …`,
`DPV_2[i] = DPV_2[i-1] + …`), which CoolSolve does not expand
(`CS-BUG-DUPLICATE-INDEX-EXPR`: 178 unknowns for 176 equations, the two extra
ones being `DPV_1[expr]` and `DPV_2[expr]`). The file is kept in valid EES.

The **runnable variant** `investment_npv_payback_coolsolve.eescode` changes
only what the gap forces: those two recurrences are written out with explicit
indices (`DPV_1[2] = DPV_1[1] + (CF[2])*1/(1+k)^2`, … up to year 20). Every
other equation, variable name and value is identical to the native file, and the
variant is valid EES (no CoolSolve-only syntax). **Consequence:** the variant
unrolls the accumulations for `T_lifetime = 20` years (the default value); a
different lifetime requires re-unrolling them.

## Results

Default operating point of the original file (`INV` = 20 000 €, `inflow_1` =
4 000 €/year, `outflow_1` = 2 000 €/year, 20 years, `j_fuel` = 4.5 %/year,
`j_el` = 3 %/year, `k` = 8 %/year):

| Result | Value |
|---|---|
| `PBT_2` (simple payback time) | 10.0 year |
| `NPV_2[9]`, `NPV_2[10]` | −2 000 €, 0 € (simple payback in year 10) |
| `NPV_1[12]`, `NPV_1[13]` | −33.3 €, +1 412.5 € (discounted payback in year 12) |
| `NPV_1[20]`, `DPV_1[20]` | +10 650.9 €, +30 650.9 € |
| `B[20]`, `C[20]`, `CF[20]` | +9 231.4 €, 3 507.0 €, +5 724.4 € |

The measure is profitable: the simple payback is 10 years and the discounted
payback year 12 (the discounted present value at the end of the lifetime is
+10.7 k€).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of NPV_1[i]
     and NPV_2[i] against the year i (parametric tab), saved in figures/ -->

## Verification

The **runnable variant** was compared with the solution stored by EES in the
source file (`reference/ees_variables.csv`, the last EES calculation):

```
176 common variables, 0 differ (rtol=0.001); only in EES: 121; only in CoolSolve: 0
```

Lowering the tolerance to `rtol=1e-12`, the largest residual difference is
**3.6e-10** on `NPV_1[5]` (−11 084.186 vs −11 084.186), i.e. the rounding of the
9-digit values stored by EES; the model is entirely explicit, so no deviation is
expected. The 121 values stored by EES but absent from the model (`D`, `TIR`,
`a[]`, and the arrays `DPV`, `NPV`, `PBT` without the `_1`/`_2` subscripts)
belong to an earlier version of the file, which also computed an internal rate
of return; they are leftovers, not part of the imported equations.

An independent Python recomputation of the two series (not committed) gives the
same values: `PBT_2` = 10 years exactly, `NPV_2[10]` = 0 €, `NPV_1[12]` =
−33.33 €, `NPV_1[20]` = +10 650.90 €.

The **parametric table** of the card, `table1` (23×2), could **not** be used as
a reference: it decodes to two columns named `Z` and `ZZ` (the EES placeholder
names of a table that was created but never filled), with a single row of zeros
and 21 empty rows, so it stores no run result
(`compare_solution.py … --row 1` → *0 common variables*). The stored solution
is therefore the only reference, and it is complete (all the 176 variables of
the equations agree).

The native file was not solved (it is blocked); the comparison above concerns
the variant, which reproduces the equations of the native file exactly.

## Source and attribution

Stéphane Bertagnolio, *Economic evaluation of investment* (economic evaluation
of energy-saving measures: NPV and simple payback), 8 January 2008, ULiège,
Faculté des Sciences Appliquées, Laboratoire de Thermodynamique; EES 7.888.
Source file of the local collection:
`~/Nextcloud/thermo_models/modeles/Economical_evaluation_of_investment/INVESTISSEMENT_RENTABILITE_SB080108.EES`
(inventory row `TM-0270`, duplicate group `DG-0059` with `TM-0252`, an identical
copy of the same file in `Model data bank/`). The same folder holds the two
course references cited in the header of the original model, not EES files:
Pilavachi, Chletsis & Nikolaidis (2007), *Economic Evaluation of Energy Saving
Measures in Buildings*, Heat SET 2007, and IBGE (2006), *Évaluation de la
rentabilité d'un projet d'investissement* (Formations Responsables Énergie).
The original carries the laboratory disclaimer that the model is freely
distributed, may not be sold, and that its origin must be cited; it is
published here under the library license (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`, 297 stored variables, 2 `DUPLICATE`
  loops, no lookup table, no warning): the file is already in
  `SI MASS DEG PA C J` — **no unit conversion was needed** and the
  `$UnitSystem` directive was removed. Comments translated to English, standard
  header added, personal e-mail address of the author dropped. Section titles
  kept, with the dead `!1. OUTPUTS` line of the original (`NPV,DPV,CF,PBT (see
  plots)`, a comment on the EES plot windows) removed and the sections renumbered
  `!1. INPUTS`, `!2. PARAMETERS`, `!3. EQUATIONS`. The nomenclature, the
  references and the full disclaimer of the original are in *Source and
  attribution* above. No equation was changed. No `.initials` file is shipped:
  the system is explicit (largest block 1) and needs no guess.
- **2026-10-15 — blocked native file**: the native file is the faithful import
  (valid EES) and is blocked by `CS-BUG-DUPLICATE-INDEX-EXPR`; it is not
  rewritten around the gap.
- **2026-10-15 — runnable variant** `investment_npv_payback_coolsolve.eescode`:
  the two cumulative recurrences `DPV_1[i] = DPV_1[i-1] + (CF[i])*1/(1+k)^i`
  and `DPV_2[i] = DPV_2[i-1] + (B[1] - C[1])` are written out with explicit
  indices 2…20 (and 1…20), and the equations `NPV_1[i] = -INV + DPV_1[i]` were
  moved into the remaining `DUPLICATE` loop (they keep their index `i`, which is
  not an arithmetic expression). Same equations, same values, valid EES, no
  CoolSolve-only syntax.
- **Level**: taxonomy §3 — equations 176 (50–300) → 1; largest algebraic block
  1 (≤ 5) → 0; arrays/`DUPLICATE` → 1; no multi-zone, no semi-empirical
  calibration, no curated guesses → 0. Score 2 → level 2, lowered by 1 to
  level 1 (all equations explicit and elementary): **level 1**.

## Limitations and CoolSolve gaps

- The simple payback method of the original repeats the *first-year* net cash
  flow over the whole lifetime (no escalation), which is why `PBT_2` has the
  closed form `INV/(B[1] - C[1])`; the payback time is therefore an integer
  here. Kept as in the original.
- `CS-BUG-DUPLICATE-INDEX-EXPR` (CoolSolve `docs/model_library_support.md` §5,
  already registered, P1) blocks the **native** file: an array index with
  arithmetic inside a `DUPLICATE` loop of the main program is not expanded
  (`DPV_1[i-1]`, `DPV_2[i-1]` become the unknown `DPV_1[expr]`, `DPV_2[expr]`;
  178 unknowns for 176 equations, *System square: No*). Minimal reproducer
  (valid EES):

  ```
  n = 3
  DUPLICATE i = 1, n
    x[i] = i
    y[i] = y[i-1] + x[i]
  END
  ```

  → *Equations: 7, Variables: 8, System square: No*, with `y[expr]` among the
  unknowns. The register already documents this bug (reproducer
  `T[i+1] = T[i] + 1`, and the `y[expr]` symptom as extra evidence of
  `CSL-0144`), so no new row was added.

## Related models

- `CSL-0153` (waste-heat-recovery ORC with an equipment cost model): the cost
  model that gives this economic evaluation its investment figures.
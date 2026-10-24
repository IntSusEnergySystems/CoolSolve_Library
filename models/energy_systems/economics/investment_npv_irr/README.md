# Economic evaluation of an investment: net present value and internal rate of return

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0262`

<!-- Badges (copy exactly, see docs/taxonomy.md):
  🟢 **Level 1 · Introductory** | 🔵 **Level 2 · Intermediate** | 🟠 **Level 3 · Advanced** | 🔴 **Level 4 · Research**
  ⚙️ **Steady-state** | ⏱️ **Dynamic** | 🎯 **Optimisation** | 🧩 **Function library**
  ✅ **Verified** | ⚠️ **Runs (modified)** | ⛔ **Blocked** | ❌ **Failing** | 📄 **Documented only**
-->

Year-by-year cash-flow evaluation of an energy-saving investment over its
lifetime, written with two `PROCEDURE`s: `NPV` builds the escalated benefit and
cost series, taxes them, adds the annuity and the linear depreciation of the
investment, discounts them at the rate `k`, and reports the net present value
and the discounted payback year; `procIRR` re-discounts the cash flows at the
unknown rate `k_IRR` and lets the main program solve `NPV_IRR = 0`, i.e. the
internal rate of return. The model is a small economic model with no
thermodynamics (currencies in euro), meant to be fed with the cost and saving
figures of an energy model.

| | |
|---|---|
| **Category** | Energy systems › Economics |
| **Fluids** | none (economic model, currencies in €) |
| **Size** | 17 equations in the runnable variant (largest block: 2); the native file does not parse in CoolSolve |
| **Source** | `~/Nextcloud/thermo_models/modeles/Economical_evaluation_of_investment/INVESTISSEMENT_RENTABILITE_SB080108SQ080206.EES` (EES X7.991) |
| **Authors** | Stéphane Bertagnolio, Sylvain Quoilin (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — native file blocked by `CS-BUG-LOOKUP-WRITE`; runnable variant verified against the EES stored solution |

## Problem statement

Economic evaluation of an energy-saving measure (a renovation, a heat
recovery, a boiler replacement…): given the initial investment, the yearly
benefit (avoided energy cost) and running cost, the lifetime, the escalation
of the energy and electricity prices, taxation, the loan interest and the
discount rate, decide whether the investment is profitable — net present
value method — and at which rate it pays — internal rate of return. The file
is the extended (February 2008) version of `CSL-0154`'s source: the cash flows
are now computed by a `PROCEDURE` and stored in a lookup table, tax, annuity
and depreciation terms are added, and the IRR is solved instead of being
imposed.

## Model

Notations of the original file (kept as is), all money in €, years in year,
rates per year:

| Symbol | Meaning |
|---|---|
| `INV` | initial investment |
| `inflow_1`, `outflow_1` | benefit and cost of the first year |
| `salvage` | salvage value at the end of the lifetime |
| `T_lifetime` | investment lifetime [year] |
| `j_fuel`, `j_el` | escalation of the benefit / of the cost [-] (original: 3–6 %/year fossil, 5–10 % biomass; 1–3 % electricity) |
| `k` | capital cost / discount rate [-] |
| `r` | interest rate of the loan [-] |
| `tax` | taxation of the net benefit [-] |
| `annuite = INV·r/(1 − 1/(1+r)^T_lifetime)` | loan annuity |
| `amortissement = INV/T_lifetime` | linear depreciation |

*PROCEDURE `NPV`* (arrays indexed by the year `i`, year 0 being the investment
date; the `_bis` series carry tax, annuity and depreciation):

$$B^{bis}[i] = inflow_1\,(1+j_{fuel})^{i-1},\qquad C^{bis}[i] = outflow_1\,(1+j_{el})^{i-1} + annuite$$
$$B_{net}[i] = (B^{bis}[i]-C^{bis}[i])\,(1-tax),\qquad CF^{bis}[i] = B_{net}[i] + amortissement$$
$$DPV_1^{bis}[i] = DPV_1^{bis}[i-1] + \frac{CF^{bis}[i]}{(1+k)^{i}},\qquad NPV_1^{bis}[i] = -INV + DPV_1^{bis}[i]$$

and, without tax/annuity/depreciation, the plain series `B`, `C`, `CF`,
`DPV_1`, `NPV_1`. The loan balance is `interet[i] = k·SRD[i-1]`,
`SRD[i] = SRD[i-1] − annuite + interet[i]`. All series are written into the
lookup table `data` (14 columns: `Year`, `B_bis`, `C_bis`, `B_net`, `CF`,
`DPV`, `NPV`, `Column8`–`Column12`, `Interest`, `SRD`), the first year with
`NPV_1_bis[i] ≥ 0` is returned as the discounted payback year `DDP`, and
`NPVvalue = NPV_1_bis[T_lifetime]` is the cash-flow part of the net present
value.

*Main program:*

```
annuite = INV*r/(1-1/(1+r)^T_lifetime)
amortissement = INV/T_lifetime
CALL NPV(… : DDP, NPV_part)
NPV = NPV_part + salvage/(1+k)^T_lifetime          "net present value"
CALL procIRR(… : NPV_IRR)
NPV_IRR = 0                                        "IRR: solved for k_IRR"
```

*PROCEDURE `procIRR`* re-discounts the same cash flows at the unknown rate:
`DPV[i] = DPV[i-1] + CF[i]/(1+k_IRR)^i`, `NPV[i] = −INV + DPV[i]`,
`NPV_IRR = NPV[T_lifetime]`; the single equation `NPV_IRR = 0` of the main
program makes `k_IRR` the internal rate of return.

| Input | Value | Meaning |
|---|---|---|
| `INV` | 100 € | initial investment |
| `inflow_1` | 40 €/year | first-year benefit |
| `outflow_1` | 22 €/year | first-year cost |
| `salvage` | 20 € | salvage value at the end of the lifetime |
| `T_lifetime` | 10 year | lifetime of the measure |
| `j_fuel`, `j_el` | 0 /year | escalation rates in the default point (comments of the file: 3–6 % fossil, 5–10 % biomass, 1–3 % electricity) |
| `r` | 1e-5 /year | interest rate (annuity ≈ `INV/T_lifetime`) |
| `k` | 0.12 /year | discount rate |
| `tax` | 0 | taxation |

## How to run

The native file stays in EES syntax and is **blocked** by `CS-BUG-LOOKUP-WRITE`
(the `NPV` procedure writes the lookup table `data` that the `procIRR`
procedure reads, which CoolSolve rejects as an error). Run the runnable
variant, which reproduces it:

```bash
coolsolve investment_npv_irr_coolsolve.eescode
```

`.initials` holds the EES stored values as guesses (`k_IRR` = 0.12414…); the
model also solves without it (9 iterations). The `.sol` baseline is tested as
`CSL-0262:coolsolve`.

## Results

Default operating point of the original file (100 € investment, 40 €/year
benefit, 22 €/year cost, 20 € salvage, 10 years, `k` = 12 %/year):

| Result | Value | EES stored solution |
|---|---|---|
| `NPV` (net present value) | 8.140371573814 € | 8.140371574 € |
| `k_IRR` (internal rate of return) | 0.1241407535564 = 12.414 %/year | 0.1241407535 |
| `DDP` (discounted payback year) | 10 | 10 |
| `NPV_part` (before salvage) | 1.700906842000 € | 1.700906842 € |
| `annuite` | 10.00055000818 €/year | 10.00055001 €/year |
| `amortissement` | 10 €/year | 10 €/year |
| `NPV_IRR` | 0 (by construction) | 0 |

The net cash flow is flat at 17.99944999 €/year because both escalation rates
are zero in this point. Consistency checks: the IRR (12.414 %) exceeds the
discount rate (12 %), so `NPV` > 0; the discounted cash flow crosses zero
between year 9 (−4.094434329 €) and year 10 (+1.700906842 €, the values of
the EES lookup table), so the payback year is `DDP` = 10, as stored.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of the
     discounted cash flow DPV_1_bis[i] and of NPV_1_bis[i] against the year
     (parametric tab), saved in figures/ -->

## Verification

The runnable variant was compared with the solution stored by EES in the
source file (`reference/ees_variables.csv`, 478 variables, the last EES
calculation):

```
17 common variables, 0 differ (rtol=0.001); only in EES: 461; only in CoolSolve: 0
```

At `--rtol 1e-12` the tool prints *1 differ (rtol=1e-12)*; the printed
residuals of the three non-zero entries are `annuite` 1.82e-10, `k_IRR`
4.54e-10 and `NPV` 2.28e-11, the largest therefore **4.54e-10 on `k_IRR`**
(rounding of the 9–10 digit values stored by EES).

Of the 461 values present only in the EES reference, 341 are the local
variables of the two `PROCEDURE`s (`year[]`, `B_bis[]`, `C_bis[]`, `B_net[]`,
`CF_bis[]`, `DPV_1_bis[]`, `NPV_1_bis[]`, `B[]`, `C[]`, `CF[]`, `DPV_1[]`,
`NPV_1[]`, `SRD[]`, `interet[]`, `NPV[]`, `i`) and 120 are leftovers of an
earlier version of the file (`a[]`, `annuite[]`, `D`, `D[]`, `PBT`, `R[]`,
`TIR`, `YEAR`, `j`). CoolSolve never writes procedure locals to the `.sol`
(registered `CS-GAP-BODY-LOCALS-SOL`), so only the 17 main-program variables
are comparable. The stored local values are moreover **stale** (registered
`CS-BUG-EXTRACT-STALE`): `B[2]` is stored as 6270 = 6000·1.045, the value of
the earlier parameter set `inflow_1` = 6000 €, `j_fuel` = 0.045 (the defaults
of the sibling file `TM-0269`), while the current equations give `B[2]` =
`B[1]`·(1+`j_fuel`) = 40 €; the main-program records and lookup rows 1–11 do
belong to the last (default) run.

Two further checks of the variant:

- a scratch run of the native file with only the 14 table-write lines removed
  (not shipped) reads EES's own stored table `data` and agrees with the
  variant on all 17 variables: *17 common variables, 0 differ (rtol=1e-9)*,
  largest printed residual **8.06e-12 on `k_IRR`** — i.e. the cash flows
  recomputed inside `procIRR` equal the ones EES wrote;
- an independent Python hand calculation of the default point gives
  `annuite` 10.000550008180202, `NPV` 8.140371574323868, IRR
  0.12414075355640218 and `DDP` = 10, agreeing with the solution above.

The **parametric table** `table1` (12502×2, columns `v` and `Year`) decoded by
`ees_extract.py` could **not** be used: it is a phantom table whose "values"
are record fragments (`compare_solution.py … --row 1` → no usable run),
registered as `CS-BUG-EXTRACT-TABLE-FP`: the comparison prints *0 common
variables, 0 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 17* with
the reference columns `v` and `Year` only.

## Source and attribution

Stéphane Bertagnolio, *Economic evaluation of investment*, 8 January 2008
(extended by S. Quoilin, 6 February 2008 — the `SB080108`/`SQ080206` of the
file name), ULiège, Faculté des Sciences Appliquées, Laboratoire de
Thermodynamique; EES X7.991. Source file of the local collection:
`~/Nextcloud/thermo_models/modeles/Economical_evaluation_of_investment/INVESTISSEMENT_RENTABILITE_SB080108SQ080206.EES`
(inventory row `TM-0271`, representative of duplicate group `DG-0062`; the
other row `TM-0269` is the earlier version with the 20 000 € parameter set and
a fixed `k_IRR` = 0.2). The original header cites two course references, not
EES files: Pilavachi, Chletsis & Nikolaidis (2007), *Economic Evaluation Of
Energy Saving Measures In Buildings*, Heat SET 2007, Chambéry; and Martin, C.
(2006), *Évaluation de la rentabilité d'un projet d'investissement*, notes de
cours, Institut Bruxellois pour la Gestion de l'Environnement (IBGE). The
original carries the laboratory disclaimer that the model is freely
distributed, may not be sold, and that its origin must be cited; it is
published here under the library license (MIT).

## Conversion log

- **2026-10-21 — import** (`ees_extract.py`: 478 stored variables, 2 decoded
  tables, 0 warnings): the file is already in `SI MASS DEG PA C J` — **no unit
  conversion was needed** and the `$UnitSystem` directive was removed. The
  original comment block (title, address, nomenclature, references,
  disclaimer; the personal contact address was dropped) moved to this README;
  the dead `!1. OUTPUTS` comment (`NPV,DPV,CF,PBT (see plots)`, pointing at
  EES plot windows) removed; sections renumbered `!1. INPUTS`, `!2.
  PARAMETERS`, `!3. EQUATIONS` (with `!3.1`, `!3.2`). No equation of the
  native file was changed.
- **Lookup table `data` — hand-decoded and checked**: `ees_extract.py`
  reported `data (44×13)` starting at `B_bis`; the binary holds **14 column
  headers** at bytes 130812–136974 with the constant step 474 = 31 + 10·44 + 3
  (`Year`, `B_bis`, `C_bis`, `B_net`, `CF`, `DPV`, `NPV`, `Column8`–`Column12`,
  `Interest`, `SRD`), i.e. the first column `Year` of the procedure's writes is
  missing from the decode: the phantom `v`/`Year` chain of
  `CS-BUG-EXTRACT-TABLE-FP` claims that header. The table shipped here was
  decoded by hand (Extended floats at `header + 31 + 10·row`) and checked
  against the writes of `NPV` (row 2 = year 1, `B_bis` 40, `C_bis`
  32.00055001, `CF` 17.99944999, `SRD` 100 ✓) and against the stored solution;
  rows 1–11 hold the default run, rows 12–21 the older 20 000 € run, rows
  22–43 `inf`, row 44 empty. With the 13-column decode, `lookup('data',ii,5)` would read the
  DPV column and give `k_IRR` = 0.4028 instead of 0.12414 — the reason for the
  hand-decode. `investment_npv_irr_coolsolve-data.csv` is the variant's own
  copy of the same table (default values agree), although the variant no
  longer reads it.
- **Variant `investment_npv_irr_coolsolve.eescode`**: the gap forces the read
  `CF[i] = lookup('data',ii,5)` of `procIRR` to go; the procedure instead
  receives the cash-flow parameters (`inflow_1`, `outflow_1`, `j_fuel`,
  `j_el`, `tax`, `annuite`, `amortissement`) and recomputes `CF[i] =
  (B_bis_i − C_bis_i)·(1 − tax) + amortissement` with
  `B_bis_i = inflow_1·(1+j_fuel)^(i-1)`, `C_bis_i = outflow_1·(1+j_el)^(i-1) +
  annuite`, the exact formulas of `NPV` (they hold for `i` = 1 as well, since
  any number to the power 0 is 1); the `CALL` was extended accordingly. Every
  other line is identical to the native file; no CoolSolve-only syntax. The 14
  table writes of `NPV` stay (they warn and are dropped by `CS-BUG-LOOKUP-WRITE`
  but feed no equation).
- **Level**: taxonomy §3 — equations 17 (< 50) → 0; largest block 2 (≤ 5) → 0;
  procedures and arrays → 1; no multi-zone/discretisation → 0; no
  semi-empirical calibration or part-load → 0; no curated guesses needed (it
  solves without `.initials` in 9 iterations) → 0. Score 1 → **level 1**.

## Limitations and CoolSolve gaps

- `CS-BUG-LOOKUP-WRITE` (registered): `NPV` writes the lookup table `data`
  that `procIRR` reads — CoolSolve reports the write+read of one table as an
  error, so the **native file does not parse**. This is the only gap in
  `missing_features`; it is worked around by the runnable variant above.
- `CS-GAP-BODY-LOCALS-SOL` (registered, not blocking): the local variables of
  a `FUNCTION`/`PROCEDURE` are never written to the `.sol`, so the verification
  covers the 17 main-program variables only.
- `CS-BUG-EXTRACT-TABLE-FP` (registered, tool): the phantom parametric table
  of the extraction and the dropped first column of the lookup decode (see the
  conversion log).
- The model has no thermodynamics: it is meant to receive the cost and saving
  figures of an energy model; the default point is a small demo case (100 €).

## Related models

- `CSL-0154` (*Economic evaluation of an energy-saving investment: net present
  value and simple payback time*): the earlier file of the same folder
  (`TM-0270`), the same discounted-cash-flow idea written with `DUPLICATE`
  loops and a closed-form simple payback, without tax, annuity, depreciation
  or IRR. This model adds those terms and solves the IRR through a second
  procedure.

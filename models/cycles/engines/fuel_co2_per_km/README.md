# CO2 emissions from fuel consumption

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0188`

Teaching exercise (ULiège MCI, TP7, exercise 3): the CO2 mass emitted per
kilometre for complete combustion of a hydrocarbon CmHn, from a volumetric
fuel consumption. The fuel is a chemical formula, a density and a volume
consumption. The default branch is diesel; gasoline is the other `$IF` branch.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | CO2 (ideal gas, molar mass only) |
| **Size** | 9 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP7/Ex_3_PNG_2019.EES` (EES X10.589) |
| **Authors** | TBD (ULiège MCI) |
| **License** | MIT |
| **CoolSolve** | native file **blocked** (`CS-GAP-MOLARMASS-ELEMENT`); runnable variant `fuel_co2_per_km_coolsolve.eescode` verified against the EES stored solution (max rel. diff 4.54e-06) |

## Problem statement

Compute the CO2 emissions in g/km from a fuel consumption in L/100 km.

The original states the principle: for complete combustion, 1 kmol of CmHn
produces m kmol of CO2.

Data, as written in the file. `Fuel$ = 'diesel'` selects the first branch.
The original comments `Fuel$ = 'essence'` as the other choice.

Diesel (`Fuel$ = 'diesel'`):

- `m = 12`, `n = 26` (C12H26)
- `rho_f = 850` kg/m³

The original comments an alternative `m = 16`, `n = 34` (hexadecane). That
line is a comment. The active formula, and the formula stored in the EES
solution (`MM_f` = 170.33484 kg/kmol), is C12H26.

Gasoline (`Fuel$ = 'essence'`):

- `m = 8`, `n = 18` (C8H18)
- `rho_f = 720` kg/m³

Consumption, both branches: `Conso = 5` L/100 km.

## Model

The `$IF` on `Fuel$` keeps one fuel. The solved point is the diesel branch.

Molar mass of the fuel and of CO2, fuel amount per kilometre, and CO2 mass
per kilometre:

\[
MM_f = m\,M_C + n\,M_H, \qquad MM_{CO_2} = M_{CO_2}
\]

\[
Conso_{kmol} = (Conso \times 10^{-3}/100)\,\rho_f / MM_f
\]

\[
CO_2 = m \times Conso_{kmol} \times M_{CO_2} \times 10^{3}
\]

`Conso` stays in L/100 km, as written. The factor \(10^{-3}/100\) converts
it to m³ of fuel per km. The last factor \(10^{3}\) converts kilograms of
CO2 per km into g/km. In the native file, \(M_C\) and \(M_H\) are
`MolarMass(C)` and `MolarMass(H)`. In the runnable variant they are the EES
element values 12.0107 and 1.00794 kg/kmol. \(M_{CO_2}\) is `MolarMass(CO2)`
in both files.

| Quantity | Role | Value (diesel branch) |
|---|---|---|
| `Fuel$` | branch selector | `'diesel'` |
| `m`, `n` | atoms in CmHn | 12, 26 |
| `rho_f` | fuel density | 850 kg/m³ |
| `Conso` | fuel consumption | 5 L/100 km |
| `MM_f`, `MM_CO2` | molar masses | solved |
| `Conso_kmol` | fuel amount | solved, kmol/km |
| `CO2` | CO2 emissions | solved, g/km |

Every equation is explicit (largest block 1). The gasoline equations are in
the file and are left out of this count while `Fuel$` is `'diesel'`.

## How to run

The native file `fuel_co2_per_km.eescode` is valid EES and does not solve in
CoolSolve (`CS-GAP-MOLARMASS-ELEMENT`: `MolarMass(C)` and `MolarMass(H)`).

The runnable variant changes only those two calls. From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./fuel_co2_per_km_coolsolve.eescode
```

`fuel_co2_per_km_coolsolve.initials` holds the six decoded stored values.
With that file the solver reports 0 iterations. Without it, 0 iterations.
The two solutions are identical. The shipped `.sol` is the run with the
guesses. No `coolsolve.conf`. The regression name of the variant is
`CSL-0188:coolsolve`.

Setting `Fuel$ = 'essence'` selects gasoline (m = 8, n = 18, 720 kg/m³).
The stored solution is the diesel branch, and that is the run compared below.

## Results

Diesel branch, `Conso` = 5 L/100 km. Values from the runnable variant.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `Conso` [L/100 km] | 5 | 5 |
| `m` [-] | 12 | 12 |
| `n` [-] | 26 | 26 |
| `rho_f` [kg/m³] | 850 | 850 |
| `MM_f` [kg/kmol] | 170.33484 | 170.33484 |
| `MM_CO2` [kg/kmol] | 44.0098 | 44.01 |
| `Conso_kmol` [kmol/km] | 2.495085562061×10⁻⁴ | not in the decoded list |
| `CO2` [g/km] | 131.769859883 | not in the decoded list |

`CO2` and `Conso_kmol` are computed by the equations and were not among the
6 decoded variables. Applying the same emission equation to the stored
`MM_f` and `MM_CO2` gives `CO2` = 131.770458704 g/km. The variant differs
from that figure by 4.54×10⁻⁶ relative, the `MM_CO2` gap.

Order of magnitude: 5 L/100 km at 850 kg/m³ is 42.5 g of fuel per km. With
12 carbon atoms out of a molar mass of 170.33 kg/kmol, complete combustion
emits about 132 g of CO2 per km, in line with about 2.6 kg of CO2 per litre
of diesel.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Stoichiometry exercise: the maintainer's figure is a parametric sweep (for
example `CO2` against `Conso`), saved as `figures/fuel_co2_per_km_sweep.png`.

## Verification

The comparison is of the runnable variant. The native file stops on
`MolarMass(C)` before a solution exists.

Reference: the solution stored in the EES file (6 variables decoded by
`ees_extract.py`). The unit system is already `SI MASS DEG PA C J`, so the
comparison is without `--ees-units`. `compare_solution.py` on
`fuel_co2_per_km_coolsolve.sol` against `reference/ees_variables.csv`:

> 6 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 3

Maximum relative difference over all common variables, as printed with
`--all`: **4.54e-06** (`MM_CO2`). Nothing exceeds rtol 0.001.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Conso` | 5 | 5 | 0.00e+00 |
| `m` | 12 | 12 | 0.00e+00 |
| `MM_CO2` | 44.01 | 44.0098 | 4.54e-06 |
| `MM_f` | 170.335 | 170.335 | 0.00e+00 |
| `n` | 26 | 26 | 0.00e+00 |
| `rho_f` | 850 | 850 | 0.00e+00 |

The tool prints `MM_f` with six significant figures. The stored value and
the solution are both 170.33484 kg/kmol (`12*12.0107 + 26*1.00794`).

`MM_CO2 = MolarMass(CO2)` is where CoolProp (44.0098 kg/kmol) and the stored
EES value (44.01 kg/kmol) differ. `CO2` is proportional to `MM_CO2` and
carries the same relative difference; it is one of the three names present
only in the CoolSolve solution, together with `Conso_kmol` and `Fuel$`.
`Fuel$` is the string `'diesel'`. CoolSolve also writes that string variable
as 0 in the numeric list, as it does for other string variables.

CoolSolve reports all 9 equations satisfied (max relative residual
2.7×10⁻¹⁷).

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP7/Ex_3_PNG_2019.EES`
(EES X10.589, equation window in plain text). The equation window names no
author. The `{$ID$}` tag is the EES licence of Philippe Ngendakumana (ULG
Thermotechnics, Liège), which is the licence holder and not an author line.
The inventory row TM-0250 attributes the file to P. Ngendakumana and
R. Dickes. Authors in `model.json` stay `TBD (ULiège MCI)` until that
attribution is confirmed. ULiège course MCI, TP7, exercise 3. Published
under the library licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`): EES X10.589, plain-text
  equations, `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or parametric
  table, 6 variables decoded, no extract warnings. Unit system already
  `SI MASS DEG PA C J`: `$UnitSystem` removed, no value rescaled. `$TABSTOPS`
  removed (it is not an equation). The unmodified extract, with those two
  directives removed, is square (9 equations, 9 variables, largest block 1),
  so no Diagram-window value was restored and no computed unknown was
  replaced by a stored number. Stored values of the six decoded variables
  are the `.initials` guesses of the variant. Comments translated to English.
  `m = 12 ; n = 26` and `m = 8 ; n = 18` split onto one equation per line.
  The original writes `conso` in the consumption equation and `Conso` in the
  assignment; both names are the variable `Conso`. The commented assignments
  `Fuel$ = 'essence'` and `m = 16 ; n = 34` (hexadecane) are recorded in
  comments; they are alternatives, and they stay out of the equation list.
  The native file keeps `MolarMass(C)` and `MolarMass(H)` and is blocked by
  `CS-GAP-MOLARMASS-ELEMENT` (*Unknown fluid: 'C'*). The runnable variant
  `fuel_co2_per_km_coolsolve.eescode` replaces those two calls by the EES
  element molar masses 12.0107 and 1.00794 kg/kmol and leaves `MolarMass(CO2)`
  unchanged. The variant is valid EES and uses no CoolSolve-only syntax.
- **Level**: equations 9 (< 50) → 0; largest block 1 (≤ 5) → 0; no user
  function, procedure, array or `DUPLICATE` → 0; one explicit combustion
  relation, no multi-zone discretisation → 0; the formula, the density and
  the consumption are given data (no calibration, off-design, part-load or
  dynamics) → 0; converges from the default guess in 0 iterations, without
  a tuned configuration → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- The native file is blocked by `CS-GAP-MOLARMASS-ELEMENT`. CoolSolve has no
  elemental fluids `C` and `H` (`H2` is a different substance). The variant
  uses 12.0107 and 1.00794 kg/kmol, the values EES returns for those two
  calls. `missing_features` lists that gap and no other.
- `MolarMass(CO2)` solves. It prints the cosmetic warning *Did you mean
  'CO2'?* (`CS-BUG-FLUID-HINT-CO2`). The warning does not change the value
  and is not a blocking gap.
- The fuel is a formula, a density and a volume consumption. The file does
  not call a fluid named Diesel.
- The solved point is C12H26 at 5 L/100 km. Hexadecane is the commented
  alternative in the original. The gasoline branch is present and is not
  the stored solution.
- `MM_CO2`, and therefore `CO2`, follow `MolarMass(CO2)` and differ slightly
  between CoolProp and EES (see Verification). The common-variable comparison
  stays inside rtol 0.001.

## Related models

- `CSL-0185` — diesel injection sizing, ULiège MCI TP5 exercise 4. Another
  MCI diesel exercise: injection duration, volumetric efficiency and mixture
  richness. This exercise converts a volumetric consumption into CO2 per
  kilometre.

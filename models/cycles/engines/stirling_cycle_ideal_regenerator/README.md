# Ideal Stirling cycle with a perfect regenerator

⛔ **Blocked** &nbsp;|&nbsp; 🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; `CSL-0059`

The theoretical Stirling cycle (two isotherms and two isochores) with an ideal
regenerator, solved exactly as the original exercise does it: air as a perfect
gas with a specific heat held constant over each transformation, the four
transformations analysed in terms of work and heat exchanged, and two
efficiencies — with and without regenerator — compared with the Carnot
efficiency. Every quantity is computed a second time with the real-gas air
property functions (the `_bis` variables of the original), and the works of the
two isotherms are computed both in closed form and with the EES definite
integral of `p dv`. The native file still cannot run on CoolSolve (a single
integration variable per model and the decreasing direction of one of the two
integrals); the shipped variant
`stirling_cycle_ideal_regenerator_coolsolve.eescode` runs and is verified
against the EES stored solution.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (perfect gas: ideal-gas `Air`; real-gas comparison: `Air_ha`, which CoolSolve maps to the real fluid `Air`) |
| **Size** | 65 equations (native file) / 69 (runnable variant), largest algebraic block ≤ 5; four state arrays `p[i]`, `T[i]`, `v[i]`, `s[i]` |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition R5, exercise 3 — EES file `R05_E03_2022.EES` |
| **Authors** | TBD (ULiège course MECA0002; the session statement sheet `ThAp22_R05.docx` of the same folder lists the repetiteurs N. Paulus, A. Zeoli and V. Lemort; the EES file itself carries no author name, only the laboratory licence tag) |
| **License** | MIT |
| **CoolSolve** | the **native file is blocked** by `CS-GAP-INTEGRAL-MULTIVAR` and `CS-GAP-INTEGRAL-DECREASING`; the shipped `_coolsolve` variant runs and reproduces the EES stored solution (see *Verification*) |

## Problem statement

A theoretical Stirling cycle is equipped with an ideal regenerator. The minimum
pressure and temperature of the cycle are 100 kPa and 25 °C, the compression
ratio (a volumetric ratio) is 10 and the maximum temperature of the cycle is
1000 °C. Analyse each of the four transformations of the cycle in terms of the
work and the heat exchanged, determine the overall efficiency of the machine and
compare it with the Carnot efficiency evaluated between the minimum and maximum
temperatures of the cycle. What becomes of the efficiency of the Stirling cycle
without regenerator?

## Model

The four states are numbered as in the original: 1 = start of the isothermal
compression, 2 = end of the compression, 3 = end of the isochoric heating,
4 = end of the isothermal expansion (the isochoric cooling 4‑1 closes the
cycle). The sign convention of the original is kept: `w` is the work **done on**
the gas, so `w_12 > 0` (compression work required) and `w_34 < 0` (work
delivered).

- **Perfect gas** (`r_bis = R#/MOLARMASS(Air_ha)` = 287.05 J/(kg·K)): the ideal
  gas law `p·v = r·T` at each state (the state temperatures are in °C, so the
  equations carry `+273.15`), `v[2] = v[1]/r_v`, `v[3] = v[2]` and
  `v[4] = v[1]`, `T[2] = T[1]` and `T[4] = T[3]`.
- **Closed isothermal works** (the closed forms of `−∫p dv` of the original):
  `w_12 = r·T₁·ln(r_v)` and `w_34 = r·T₃·ln(v[3]/v[4])`; the works of the
  isochores are zero (`w_23 = w_41 = 0`).
- **Heats**: the first law for a closed system
  `w_ij + q_ij = cv_ij·(T[j] − T[i])` on the four transformations, with
  `cv_ij = cv(Air, T=(T[i]+T[j])/2)` — the specific heat is held constant over
  each transformation, which the original comments point out would not be
  judicious over large temperature variations. Since the two isotherms are
  isothermal, this route returns `q_12 = −w_12` and `q_34 = −w_34`.
- **Efficiencies**: `q_couteux = q_23 + q_34` is what has to be supplied
  **without** regenerator and `q_c = q_34` **with** it (the heat of the
  isochoric heating `q_23` is stored by the regenerator and given back during
  the isochoric cooling `q_41`, both equal in absolute value in an ideal
  regenerator); `w_net = −(w_34 + w_12)`; `eta_stirling = w_net/q_couteux`,
  `eta_stirling_regen = w_net/q_c`, and `eta_carnot = 1 − T₁/T₃`.
- **Real-gas route (`_bis` variables, "as in the original")**: the same cycle
  is recomputed with the `Air_ha` property functions — `volume`, `pressure`,
  `intenergy` — the heats through the internal-energy differences
  (`w_ij_bis + q_ij_bis = u[j] − u[i]`) and the works of the two isotherms
  through the **EES definite integral** of `p dv` along the isotherm
  (`w_12_bis = −integral(p_integrale12, v12, v[1], v[2], 0.1)` and the same for
  34); `eta_stirling_regen_bis` closes the comparison.
- **For information**: the entropies `s[1..4]` of the perfect-gas states.

With a perfect gas the two efficiencies are exact closed-form results, so this
exercise also checks the consistency of the first-law route: `eta_stirling_regen`
comes out **equal** to `eta_carnot` (0.7658), as the original comment states,
because `w_net = R(T₃−T₁)ln(r_v)` and `q_c = RT₃ln(r_v)` — the ratio does not
depend on `r_v` at all.

| Inputs | Value | Outputs (perfect gas) | Value |
|---|---|---|---|
| `p[1]` minimum pressure | 100 kPa | `p_max` (`p[3]`) | 4.270 MPa |
| `T[1]` minimum temperature | 25 °C | `w_net` net work per unit mass | 644.4 kJ/kg |
| `r_v` compression ratio | 10 | `eta_stirling` efficiency without regenerator | 0.3955 |
| `T[3]` maximum temperature | 1000 °C | `eta_stirling_regen` efficiency with regenerator | 0.7658 |
| `fluid$` working fluid | Air | `eta_carnot` | 0.7658 |
| | | `eta_stirling_regen_bis` (real gas) | 0.7664 |

## How to run

The native `stirling_cycle_ideal_regenerator.eescode` does **not** run on
CoolSolve (see *Limitations and CoolSolve gaps*); solve the runnable
variant, from the GUI or from a terminal:

```bash
coolsolve ./stirling_cycle_ideal_regenerator_coolsolve.eescode
```

It converges in about 30 s (1000 integration steps, `SUCCESS`). The shipped
`.initials` (the EES stored solution, converted by
hand) is loaded automatically; without it the model converges to the same
values, so it is only a bootstrap. No `coolsolve.conf`, no lookup table.

## Results

State points (per unit mass), perfect gas and real gas:

| | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| `p[i]` [Pa] | 100 000 | 1.000·10⁶ | 4.270·10⁶ | 4.270·10⁵ |
| `p_bis[i]` [Pa] | 100 000 | 9.970·10⁵ | 4.319·10⁶ | 4.275·10⁵ |
| `T[i]` [°C] | 25.0 | 25.0 | 1000.0 | 1000.0 |
| `v[i]` [m³/kg] | 0.855832 | 0.0855832 | 0.0855832 | 0.855832 |
| `v_bis[i]` [m³/kg] | 0.855559 | 0.0855832 | 0.0855832 | 0.855832 |
| `s[i]` [J/(kg·K)] | 3884.3 | 3217.3 | 4359.8 | 5021.3 |

Work and heat of each transformation, perfect gas (real gas in brackets):

| Transformation | `w_ij` [kJ/kg] | `q_ij` [kJ/kg] |
|---|---:|---:|
| 1‑2 isothermal compression | 197.06 (196.82) | −197.06 (−198.64) |
| 2‑3 isochoric heating | 0 (0) | 787.97 (787.07) |
| 3‑4 isothermal expansion | −841.49 (−845.20) | 841.49 (845.95) |
| 4‑1 isochoric cooling | 0 (0) | −787.97 (−786.00) |
| **cycle** | **w_net = 644.43** | q_c = 841.49, q_couteux = 1629.46 |

| Indicator | Value |
|---|---|
| `eta_stirling` (no regenerator) | 0.39548 |
| `eta_stirling_regen` (perfect gas) | 0.76582 |
| `eta_stirling_regen_bis` (real gas) | 0.76645 |
| `eta_carnot` | 0.76582 |
| `cv12` / `cv23` / `cv34` / `cv41` | 717.9 / 808.2 / 897.6 / 808.2 J/(kg·K) |

The four checks of the exercise come out as follows:

- **isothermal compression 1‑2** — the work that must be supplied is
  197.06 kJ/kg and the heat that must be removed is exactly the same in
  absolute value (`q_12 = −w_12`, since the transformation is isothermal and
  `Δu = 0`); the pressure rises from 100 kPa to 1 MPa, i.e. the factor
  `r_v` = 10 of the statement is a *volumetric* ratio, not a pressure ratio;
- **isochoric heating 2‑3** — no work, 787.97 kJ/kg of heat supplied at constant
  volume; this is the heat the ideal regenerator stores;
- **isothermal expansion 3‑4** — 841.49 kJ/kg delivered and the same amount of
  heat received, again with `q_34 = −w_34`;
- **isochoric cooling 4‑1** — no work, 787.97 kJ/kg rejected, i.e. exactly the
  heat stored during 2‑3 (`q_41 = q_23` in absolute value): **this is what makes
  the ideal regenerator possible** and is visible in the numbers above.

Efficiency: with the regenerator the Stirling cycle reaches the **Carnot**
efficiency between its extreme temperatures, 76.58 %, to the last digit of the
model (`eta_stirling_regen = eta_carnot = 0.76582`, because
`w_net = r_bis·(T₃−T₁)·ln(r_v)` = 644 427 J/kg and `q_c = r_bis·T₃·ln(r_v)` =
841 490 J/kg); without regenerator the heat of the isochoric heating must be
supplied by the source as well and the efficiency drops to 39.55 %, i.e.
**51.6 % of the Carnot efficiency** — which is what the original comment
("almost 55 %", on the purely analytic perfect-gas result) expresses.

The real-gas route (`_bis`) confirms the perfect-gas result to 0.08 %
(`eta_stirling_regen_bis` = 0.76645 against 0.76582): at up to 43 bar and
1000 °C, the departure of air from the perfect-gas law is small. The two
routes are not identical by construction, because the heats of the `_bis` route
come from the internal energies while those of the perfect-gas route come from
`cv·ΔT`, which is why the original notes that the two do not give exactly the
same result.

The charge is an ideal gas, so CoolSolve has no ideal-gas diagram
(`CS-FEAT-DIAGRAM-IDEAL`) and the four states are only available as the model's
own `p[i]`, `T[i]`, `v[i]`, `s[i]` arrays; the figure of this model is a
parametric sweep (roadmap decision D7).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the charge is an
     ideal gas and CoolSolve has no ideal-gas diagram (CS-FEAT-DIAGRAM-IDEAL), so the
     figure of this model is a parametric sweep plot (roadmap decision D7), e.g. the
     efficiency without regenerator eta_stirling and the net work w_net as functions of
     the compression ratio r_v, obtained with the Parametric tab of the GUI (values
     below checked by re-solving the runnable variant with r_v = 2, 4, 10, 20, 40):
      r_v             2        4       10       20       40
      eta_stirling  0.1863   0.2997   0.3955   0.4453   0.4833
      w_net [kJ/kg]  194.0   388.0    644.4    838.4  1032.4
     (eta_stirling_regen = eta_carnot = 0.7658 does not depend on r_v at all)
     saved as figures/stirling_cycle_ideal_regenerator_rv.png  -->

## Verification

**Reference 1 — the stored EES solution (main reference).** The source file was
saved with a complete solution (all 68 of its variables hold a real value), and
`compare_solution.py stirling_cycle_ideal_regenerator_coolsolve.sol
reference/ees_variables.csv --ees-units` prints on the **runnable variant**:

```
66 common variables, 13 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 5
```

The 13 differences are all explained, and none of them is a disagreement on a
quantity the model uses:

- **absolute entropies** `s[1..4]` (3.18e-01, 3.61e-01, 2.94e-01, 2.65e-01) carry
  the entropy reference state of their backend: EES returns the values of its
  ideal-gas `Air` table, CoolSolve those of CoolProp `Air`
  (`CS-GAP-IDEAL-ENTROPY` family). They are "for information" post-processing,
  and what is physically meaningful — the isothermal entropy steps — comes out
  right: `s[2]−s[1]` = −667.0 and `s[4]−s[3]` = +661.5 J/(kg·K) in CoolSolve
  against exactly −660.95 = −`r_bis`·ln(r_v) in EES (both isotherms are
  isentropic to within the real-gas residual of the property backend, which is
  the largest on the cold isotherm, where the gas is densest);
- **absolute internal energies** `u[1..4]` (3.72e-01, 3.74e-01, 1.12e-01,
  1.12e-01) carry the same kind of reference-state offset (EES integrates `cv`
  from 0 K: `u(298.15 K)` = 212.8 kJ/kg, CoolProp's `Air` = 338.9 kJ/kg); the
  differences, which are what the `_bis` heats use, agree: `u[2]−u[1]` =
  −1817.7 J/kg against −1818.0 J/kg in EES;
- **the two isothermal works `w_12_bis` (2.88e-02) and `w_34_bis` (4.31e-02)**,
  and the heats and efficiency derived from them (`q_12_bis` 2.85e-02,
  `q_34_bis` 4.30e-02, `eta_stirling_regen_bis` 4.49e-03), differ because **EES
  computes them with a coarse quadrature**: its step is 0.1 m³/kg over a range of
  0.77 m³/kg, i.e. 8 steps. Recomputing EES's own trapezoidal rule with CoolProp
  properties (Python/CoolProp, step 0.1 m³/kg) gives −204 923 and 880 721 J/kg
  against the stored −202 654 and 883 256 J/kg (1.1 % and 0.3 %: the remaining
  difference is EES's own `Air_ha` property data), while the *accurate* value of
  the same integrals (20 001-point Simpson rule) is −196 811 and 845 195 J/kg,
  i.e. the CoolSolve variant is the accurate one (196 824 and −845 201 J/kg, see
  reference 2). This is the same situation as `CSL-0047`.

Excluding exactly those 13 variables, the same command gives

```
53 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 18
```

and with `--rtol 1e-9 --all` the **largest deviation of the whole comparison is
1.51e-05**, on every quantity that scales with the specific gas constant
(`v[i]`, `p[i]`, `w_12`, `w_34`, `w_net`, …): EES uses `R#` = 8314.3 J/(kmol·K)
against 8314.4626 J/(kmol·K) in CoolSolve. The two variables only in EES are
`p` and `v`, stale records of the EES workspace that no equation uses; the five
only in CoolSolve are `fluid$` (and its string copy in the `.sol`,
`CS-BUG-SOL-STRING`), `R#`, the two integrals `w_int_12`/`w_int_34` split out of
the state equations by the variant, and its integration variable `x`.

**Reference 2 — an independent re-implementation in Python/CoolProp** (not
shipped): the same equations written from scratch against CoolProp's `Air`
properties, with the two definite integrals evaluated by a 40 001-point Simpson
rule. `compare_solution.py <variant .sol> <reference.csv> --rtol 1e-6` gives

```
49 common variables, 5 differ (rtol=1e-6); only in EES: 0; only in CoolSolve: 22
```

The five differences are `w_12_bis` (5.04e-05), `w_34_bis` (2.13e-05),
`q_12_bis` (4.99e-05), `q_34_bis` (2.12e-05) and `eta_stirling_regen_bis`
(8.82e-06), i.e. only the quadrature of the two integrals (RK4 with a step of
0.001 in x against the Simpson rule). All 44 other quantities agree to better
than 1e-6, which checks the equations and the hand unit conversion. The course
also ships a Python/CoolProp solution of the *same exercise* from the previous
year (`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R5/old/`,
script `ThAp21_R04E03.py`, same data); it prints 39.54 %, 76.59 % and 76.59 %
for the three efficiencies, i.e. the stored EES values, which is an independent
check of the exercise statement.

**CoolSolve solution check.** The solve reports `Solver: SUCCESS (1000
iterations)`, and the `-d` analysis reports *System square: No*,
which is the known analysis bug `CS-DOC-SQUARE-INTEGRAL` (each integral state is
counted as an unknown without an algebraic equation although the integrator
closes it); the model is **square** — the `System square: No` line must not be
read as a defect of the model. `tools/test_models.py CSL-0059` re-solves the
variant and reproduces the shipped baseline (`CSL-0059:coolsolve … OK`; the
native file is skipped because the model is blocked).

## Source and attribution

ULiège, course *Thermodynamique appliquée* (MECA0002, Faculté des Sciences
Appliquées, Département d'Aérospatiale et de Mécanique, Laboratoire de
Thermodynamique), repetition R5 "exercices sur le chapitre 9 (partie 1) – moteurs
à combustion", exercise 3, 2022‑2023. The EES file is
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R5/R05_E03_2022.EES`
(inventory candidate `TM-0431`, duplicate group `DG-0103`; the same file is
saved a second time in `…/R5/save/`, candidate `TM-0434`, and the exercise
exists again in the repetition R4bis, `R05_E03_2022.EES`, candidate `TM-0428`,
another exercise of the collection and not processed here). The session
statement sheet `ThAp22_R05.docx` of the same folder gives the text of the
exercises. No source file is copied into the library.

## Conversion log

- **2026-10-05 — import (card C-63, candidate TM-0431)**: extracted with
  `CoolSolve/tools/ees_extract.py` (EES X10.836, 119 equation-window lines,
  68 variables, **no** lookup and **no** parametric table, decimal comma
  converted by the tool, the `{$ID$…}` laboratory licence tag and the
  `{$PX$…}`/`{$ST$…}` display tags removed). Comments translated from French,
  standard header and section titles added, the CTRL+Y hint of the last line
  (EES GUI) removed. **Every equation of the original is kept**, including the
  `_bis` real-gas route, the two definite integrals and the "for information"
  entropies.
- **2026-10-05 — unit conversion by hand** (the file is in
  `SI MASS DEG KPA K KJ`, [ees_import.md §6](https://github.com/CoolProp/CoolSolve/blob/main/docs/ees_import.md)):
  - `p[1] = 100 [kPa]` → `p[1] = 100E3 [Pa]`; all other pressures follow from
    the equations, in Pa;
  - `T[1] = 25[K]+273.15 [K]` → `T[1] = 25 [C]` and
    `T[3] = 1273.15 [K]` → `T[3] = 1000 [C]`; the state temperatures are now in
    °C, so the **three perfect-gas equations that need an absolute temperature
    carry `+273.15`** (`v[1] = r_bis*(T[1]+273.15)/p[1]`, `p[2]`, `p[3]`, `p[4]`)
    as well as the **two closed isothermal works** (`w_12`, `w_34`) and the
    **Carnot efficiency** (`1-(T[1]+273.15)/(T[3]+273.15)`); the temperature
    *differences* of the first law (`T[j]-T[i]`) and of the `cv` evaluations are
    unchanged;
  - `r = 0.287 [kJ/kg-K]` → `r = 287 [J/(kg-K)]` (that `r` is not used by any
    equation of the original, which uses `r_bis = R#/MOLARMASS(Air_ha)`; it was
    kept and annotated);
  - the integral step `0.1` is a specific volume in m³/kg: no conversion, and
    the `$UnitSystem` line was removed. No equation contained an explicit unit
    factor other than the gas constant.
- **2026-10-05 — `.initials`**: the stored EES solution converted by hand
  (pressures ×1000, energies and specific heats ×1000, temperatures −273.15).
  Two stale records of the EES workspace (`p` = inf and `v` = 0.7557 m³/kg, no
  equation uses them) were dropped, and the two integration variables were given
  the value of the **beginning** of their interval (`v12 = v[1]`, `v34 = v[3]`).
- **2026-10-05 — runnable variant** `stirling_cycle_ideal_regenerator_coolsolve.eescode`
  (workflow §6): the native file stays in valid EES; the variant changes only
  what the open `INTEGRAL` gaps force, and every change is repeated in
  its own header:
  1. the two definite integrals use the state volumes `v12` and `v34` as
     integration variables, which CoolSolve rejects (a single integration
     variable per model, `CS-GAP-INTEGRAL-MULTIVAR`; increasing limits only,
     `CS-GAP-INTEGRAL-DECREASING`). Both integrals are written on **one**
     integration variable `x` over the constant interval [0,1], the state
     volumes being mapped on it by the change of variable
     `v12 = v[1] + (v[2]-v[1])*x` and `v34 = v[3] + (v[4]-v[3])*x`; the
     integrals `w_int_12` and `w_int_34` are new intermediate variables;
  2. the factor of the change of variable, sign included, is applied in its own
     equation (`w_12_bis = -w_int_12*(v[2]-v[1])`); this split is kept although
     CoolSolve now applies a factor in front of an `INTEGRAL` call;
  3. the integration step is 0.001 in `x` (≈ 0.00077 m³/kg) instead of the
     original 0.1 m³/kg (≈ 0.13 in `x`): CoolSolve integrates with RK4 and is
     much more accurate than EES's trapezoidal rule, which is why the works
     differ from the stored EES values by 3–4 % (see *Verification*). No other
     equation, name, constant or input value was modified, and no CoolSolve-only
     syntax is used: the variant is valid EES.
- **Level** (taxonomy.md §3): 65 equations native / 69 variant (50–300 → 1);
  largest algebraic block ≤ 5 (0, estimated by reading the equations: the
  perfect-gas part is explicit and the real-gas part has blocks of 1–2
  equations — the `-d` block statistics are unusable here, see
  `CS-DOC-SQUARE-INTEGRAL`); arrays used for the four states, no
  function or procedure (1); no multi-zone discretisation (0); no
  semi-empirical calibration, off-design or dynamics (0); curated guesses not
  required — the variant converges cold to the same values (0). Score 2 →
  **level 2**, consistent with the inventory row and with the card.

## Limitations and CoolSolve gaps

- **The native file is blocked** by two CoolSolve limitations, met by the two
  `INTEGRAL` calls of the original (they are *definite integrals used as a
  numerical quadrature*, in a steady model — no time integration at all):
  - `CS-GAP-INTEGRAL-MULTIVAR`: a model may have only one integration variable —
    *"All INTEGRAL() calls must share the same integration variable; found 'v34'
    and 'v12'"*. The EES file solves both integrals; its stored solution holds
    `w_12_bis` = 202.65 and `w_34_bis` = −883.26 kJ/kg;
  - `CS-GAP-INTEGRAL-DECREASING`: the upper limit must be greater than the lower
    one — *"Invalid integration interval [0.855832, 0.085583]: the upper limit
    must be greater than the lower limit"*; `w_12_bis` integrates from `v[1]` to
    `v[2]` = `v[1]/r_v` (EES integrates downwards: `INTEGRAL(1, t, 2, 1, 0.1)` = −1
    per the CoolSolve register).
  The runnable variant works around the two gaps by a change of variable on one
  integration variable over [0,1].
- **The `-d` analysis of a model with `INTEGRAL` calls is unusable**
  (`CS-DOC-SQUARE-INTEGRAL`): it reports *System square: No* and zero blocks
  although the solve succeeds and verifies. The block/loop statistics used for
  the level rating were therefore taken from the equations, not from `-d`.
- The entropy and internal-energy reference states differ between EES and
  CoolProp (`CS-GAP-IDEAL-ENTROPY` and the same family for `u`): only
  differences are meaningful, and the model uses them (the `_bis` heats and the
  two posted `s[i]`).
- The EES fluid name `Air_ha` (humid air in EES) is mapped by CoolSolve to the
  **real** fluid `Air`, which is the intention of the original's "air as a real
  gas" route; the ideal-gas route uses the EES ideal-gas substance `Air`
  (`cv`, `entropy`), as in the original. CoolSolve prints a warning for every
  property call on `'Air'` ("*For moist air properties use AirH2O*"); it is a
  hint, the model wants dry air and its results are unaffected.
- Physical simplifications of the original, kept as they are: perfect gas,
  `cv` constant over each transformation, an ideal (perfect, counter-flow,
  equal-capacity) regenerator, no pressure drop, no leakage, no friction and no
  volume of the regenerator counted in the states.
- The two definite integrals are a numerical quadrature of `∫p dv` along an
  isotherm; their results depend on the quadrature (the original's step of
  0.1 m³/kg gives 3–4 % more work than the exact integral).

## Related models

- `CSL-0049` *otto_cycle_air_standard*: the other air-standard cycle of the
  same repetition (exercise 1), solved with the same method — perfect gas with
  a temperature-dependent `cv` evaluated at a mean temperature, state arrays
  `p[i]`, `T[i]`, `v[i]`, `s[i]`, and an engine power on top of the cycle.
- `CSL-0047` *nonideal_gas_isothermal_work*: the same idea on a single
  isothermal process — a non-ideal gas whose boundary work is computed with an
  EES definite integral and with the closed form; verified on its native file
  (symbolic limits and factor in front of the call), whereas this model also
  needs several integration variables and a decreasing direction.
- `CSL-0050` *two_shaft_gas_turbine_compressor_map*: the gas-turbine cycle of
  the same course family, also walked through station by station on air, with a
  real gas-turbine regenerator instead of the ideal Stirling one.
- The exercise session also contains the **Diesel** counterpart
  (`R05_E02_2022.EES`, inventory `TM-0430`/`TM-0433`) and the earlier years'
  Brayton and Otto/Diesel repetitions; they are different exercises and are not
  in the library.

# Air-standard Diesel cycle with a 60 % efficiency target (THD R08 exercise 4)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0280`

Theoretical (air-standard) Diesel cycle solved as in the original ULiège
exercise: air is an ideal gas whose specific heats depend on temperature,
`c_v` is held constant over each transformation and `gamma = c_p/c_v` is
evaluated at the mean temperature of each of the two isentropic
transformations. The exercise is an *inverse* problem — the thermal efficiency
is imposed (60 %) and the model solves for the maximum temperature the cycle
must reach — and it also returns the four state points, the heat added, the
net work and the mean effective pressure.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal-gas behaviour, `cp`/`cv` of `Air`) |
| **Size** | 36 equations (largest block: 13) |
| **Source** | `~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R08.zip!/THD10_R08_E4.EES` (EES X8.423, unit system SI MASS DEG KPA C KJ) |
| **Authors** | TBD — no author name in the file; `sources/thermo_models` credits S. Bertagnolio and S. Borguet for the 2009-2010 THD exercise sets (the `{$ID$}` tag is the laboratory student licence, not an author) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (max rel. diff **3.29e-03**, all of it property backend; see *Verification*) |

## Problem statement

Paraphrase of exercise 4 of session R08 (the file's statement follows the
French edition of Çengel and is not reproduced here): an ideal Diesel cycle
starts from 100 kPa and 300 K with a volumetric (compression) ratio of 18, and
one asks for the peak temperature the cycle must reach so that its thermal
efficiency is 60 %. The file itself warns that the quoted compression ratio is
in fact a *volumetric* ratio `v[1]/v[2]`. The statement sheet of the session is
`THD10_R08E.pdf` inside the same zip.

## Model

Data: `eta_diesel = 0.6`, `R = 287 J/(kg·K)`, `r_v = 18`, `p[1] = 100 kPa`,
`T[1] = 300 K = 26.85 °C`, `fluid$ = 'Air'`.

The four states are numbered as in the original: 1 = start of compression,
2 = end of compression, 3 = end of the isobaric heat addition, 4 = end of the
expansion.

- **Ideal-gas law** at states 1 and 3, `v = R·(T + 273.15)/p` (absolute
  temperature), and back `T = p·v/R − 273.15` at states 2 and 4.
- **Isentropic model** (`p·v^gamma = cste`) on 1-2 and 3-4:
  `p[2] = p[1]·r_v^gamma12` and `p[4] = p[3]·(v[3]/v[4])^gamma34`, with
  `gamma12 = cp12/cv12` and `gamma34 = cp34/cv34` evaluated at the mean
  temperature of the transformation (`c_p`, `c_v` calls with a temperature
  argument only, i.e. they depend on temperature alone).
- **Volumes**: `v[2] = v[1]/r_v`, `v[4] = v[1]` (4-1 is isochoric).
- **First law for a closed system** on every step,
  `w_ij + q_ij = c_v,ij·(T[j] − T[i])`, with `q_12 = q_34 = 0` (isentropic),
  `w_23 = −p[2]·(v[3] − v[2])` (isobaric, from −∫p dv), `w_41 = 0` (isochoric);
  `q_23 = q_c` is the heat received and `q_41` the heat rejected.
- **Closure**: `eta_diesel = w_net/q_c` with
  `w_net = −(w_12 + w_23 + w_34 + w_41)` — this is what makes the system
  square: `q_c` and `T[3]` are *outputs* solved from the imposed efficiency,
  not inputs. `pme = w_net/(v[1] − v[2])` is the definition of the mean
  effective pressure; `T_MAX = T[3]`.

| Quantity | Role | Value |
|---|---|---|
| `eta_diesel`, `r_v`, `p[1]`, `T[1]`, `R` | imposed by the exercise | 0.6, 18, 100 kPa, 26.85 °C, 287 J/(kg·K) |
| `T[2..4]`, `p[2..4]`, `v[1..4]` | state points | solved, °C, Pa, m³/kg |
| `q_c`, `w_net`, `pme` | cycle performance | solved, J/kg, J/kg, Pa |
| `T_MAX` | answer of the exercise | solved, °C |

## How to run

```bash
coolsolve ./diesel_cycle_air_standard.eescode
```

The committed `.initials` carries the EES stored values as guesses (workflow
§3: stored values of unknowns belong in `.initials`). Without them the model
does **not** converge from the default guesses: block 8
(`cp12, cv12, T[2], …`) fails with `MaxIterations` — the recursive
`T[2] ↔ gamma12` coupling that the original itself flags in its last comment
("first guesses `cp = 1000`, `cv = 750`, `gamma_12 = 1.4`, `gamma_34 = 1.3`").
No `coolsolve.conf` and no variant are needed; there is no lookup table.

## Results

Default operating point of the file (kept as the regression case); CoolSolve
against the EES stored solution:

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `T_MAX` = `T[3]` | 1272.42 °C (1545.57 K) | 1273.85 °C (1547.00 K) |
| `T[2]` | 617.86 °C (891.01 K) | 617.13 °C (890.28 K) |
| `T[4]` | 445.41 °C (718.56 K) | 446.70 °C (719.85 K) |
| `p[2]` = `p[3]` | 5.346 MPa | 5.342 MPa |
| `p[4]` | 239.5 kPa | 240.0 kPa |
| `q_c` | 770.45 kJ/kg | 772.99 kJ/kg |
| `w_net` | 462.27 kJ/kg | 463.79 kJ/kg |
| `pme` | 568.5 kPa | 570.4 kPa |
| `eta_diesel` | 0.600 | 0.600 |
| cut-off ratio `v[3]/v[2]` | 1.7346 | 1.7377 |

Checks recomputed from the output: `w_net/q_c = 0.6000` (the imposed
efficiency, satisfied exactly), and the heat-based efficiency
`(q_c + q_41)/q_c = 0.5957` — the two differ because `c_v` is held constant
over each transformation with a different value on each of them (the original
carries the same inconsistency; the model defines `eta_diesel` with `w_net`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![...](figures/<name>_efficiency.png)  + one-line caption
     (ideal-gas model: CoolSolve has no ideal-gas diagram, CS-FEAT-DIAGRAM-IDEAL -> parametric
      sweep plot, roadmap decision D7) -->

## Verification

Reference: the solution stored in the EES file itself (36 names decoded by
`ees_extract.py`; the file was saved with a complete solution, unlike the Otto
sister exercise `CSL-0049`). Command and printed summaries:

```text
python3 tools/compare_solution.py diesel_cycle_air_standard.sol reference/ees_variables.csv --ees-units
35 common variables, 13 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 1
Only in EES reference: gamma

python3 tools/compare_solution.py ... --ees-units --rtol 0.004
35 common variables, 0 differ (rtol=0.004); only in EES: 1; only in CoolSolve: 1
```

The printed **maximum relative difference over all common variables is
3.29e-03** (`w_23`); the other twelve exceedances are `w_net`, `q_c`, `q_23`,
`pme` (3.28e-03), `q_41` (3.13e-03), `T[4]` (2.91e-03), `p[4]` (1.80e-03),
`v[3]` (1.75e-03), `w_12` (1.46e-03), `T[2]` (1.19e-03), `T[3]` and `T_MAX`
(1.12e-03). All of them are the property backend, amplified by the isentropic
exponent, and nothing else:

- `cp12` and `cv12` themselves agree to 4.27e-04 and 2.20e-04 (EES vs CoolProp
  ideal-gas Air), `gamma12` to 2.07e-04 relative.
- `T[2] = T[1]·r_v^(gamma12−1)`, so the state carries the exponent difference
  through `ln(18)·Δgamma12`: with the two stored/solved gammas,
  `18 = math.log(18)*(1.376621653311 − 1.376336588) = 8.239e-04`, and the
  observed shift is `(891.013 − 890.279)/890.279 = 8.244e-04` in K — printed
  as 1.19e-03 because `compare_solution.py` divides by the °C value 617.129.
  The same chain (`T[3]` from the imposed efficiency, then `w_*`, `q_c`,
  `pme`) produces the 3.3e-03 maximum, i.e. 0.33 %, inside the 0.5 % the
  verification policy allows for two different property backends
  (`CoolSolve docs/ees_import.md` §11).

Excluded variables, by name: `gamma` (stored as 1.4 by EES but appearing in no
equation of the equation window — a leftover, not recreated) and `fluid$`
(only in CoolSolve; the reference CSV skips strings).

## Niche

Nearest models of the library, by equation overlap
(`audit.py --cand TM-0530`: `CSL-0201` 0.31, `CSL-0049` 0.25 — shared
fragments are the ideal-gas/`cp`/`cv` lines) and by topic:

- `CSL-0049` *otto_cycle_air_standard*: the same course family and the same
  mean-temperature `c_p`/`c_v` closure, but the **Otto** cycle (constant-volume
  heat addition) solved as a *forward* problem with the heat given;
- `CSL-0192` *otto_cycle_cengel*: cold air-standard Otto cycle with specific
  heats fixed once at the intake temperature (textbook closure);
- `CSL-0059` *stirling_cycle_ideal_regenerator*: the third air-standard cycle
  of the library, with a regenerator and integral-based work.

What this model adds: the **isobaric heat-addition (Diesel) topology** — no
air-standard Diesel cycle exists in the library (the forward Diesel exercise
`TM-0430` is still `todo`) — plus an **inverse formulation** (efficiency
imposed, peak temperature solved) and the mean effective pressure, verified
against a full EES stored solution of a different exercise than the two Otto
models.

## Source and attribution

- Source file: `~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R08.zip!/THD10_R08_E4.EES`
  (member of `THD10_R08.zip`, dated 2010-04-01; EES version X8.423, unit
  system `SI MASS DEG KPA C KJ`, licence tag removed by the extractor).
- Authors: none named in the file. `sources/thermo_models` credits the
  2009-2010 THD exercise sets to S. Bertagnolio and S. Borguet; recorded as
  `TBD` for the maintainer to confirm.
- ULiège, course *Thermodynamique appliquée* (THD10), session R8, 2010,
  exercise 4. Course material published under the library licence (MIT,
  maintainer decision 2026-10-04); the statement is paraphrased, the exercise
  is presented as an example.

## Conversion log

- **2026-10-23 — import**: `ees_extract.py` (36 variables, no table, 1 warning).
  `$UnitSystem SI MASS DEG KPA C KJ` removed and every value converted by hand
  to SI-°C-Pa-J: `R` 0.287 kJ/(kg·K) → 287 J/(kg·K); `p[1]` 100 kPa → 100E3 Pa
  (pressures of the equations scale with it: `p[2] = p[1]·r_v^gamma12`,
  `w_23 = −p[2]·(v[3]−v[2])`, `pme = w_net/(v[1]−v[2])`); energies kJ/kg → J/kg
  (`q_*`, `w_*`, `q_c`, `w_net`); `T[1] = 300 K → 26.85 °C` and `+273.15` in
  the three ideal-gas-law equations (with `−273.15` after `p·v/R`). The
  `cp`/`cv` calls take °C: the original's `(T[i]+T[j])/2 − 273` (K→°C with the
  rounded 273) becomes `(T[i]+T[j])/2`, i.e. the evaluation temperature is
  0.15 K lower than in EES — a second-order effect, quantified in *Verification*
  next to the dominant property-backend difference.
- **2026-10-23 — curation**: standard header, French comments translated (no
  meaning added, units given in SI), the statement paraphrased, the two
  "convergence hints" comments of the original kept as one line in *How to
  run*. No equation added or removed; the stray stored variable `gamma` was
  not recreated.
- **Level**: score of `docs/taxonomy.md` §3 → equations 36 (< 50) = 0,
  largest block 13 (6-30) = 1, arrays present = 1, no multi-zone = 0, no
  semi-empirical/off-design = 0, needs curated guesses (convergence fails
  without `.initials`) = 1 → 3 → **level 2**.

## Limitations and CoolSolve gaps

- Physical: `c_v` constant over each transformation and `gamma` evaluated at
  one mean temperature — the exercise's own approximation (the heat-based
  efficiency of the solution is 0.5957 instead of the imposed 0.600).
- CoolSolve: none — `missing_features` is empty; the native file runs as it
  stands (after the unit conversion required by decision D5).

## Related models

- `CSL-0049` (*otto_cycle_air_standard*): same course family and same
  mean-temperature specific-heat closure, **Otto** cycle (constant-volume heat
  addition) with the heat given instead of the efficiency.
- `CSL-0192` (*otto_cycle_cengel*): the cold air-standard Otto cycle
  (specific heats fixed at the intake temperature), the simplest
  air-standard cycle of the library.

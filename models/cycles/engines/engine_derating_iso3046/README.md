# Engine derating according to ISO 3046/1 (ambient conditions)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0151`

Derating of a Diesel engine between the reference conditions of the standard
ISO 3046/1 and the site conditions (altitude, ambient temperature, humidity):
the correction factor `K` combines the dry atmospheric-pressure ratio, the
absolute intake-air temperature ratio and the coolant-temperature ratio, with
the factor `a` and the exponents `m`, `n`, `s` taken from the table of the
standard; the power-correction factor is `alpha = K - 0.7*(1-K)*(1/eta_m - 1)`
and the site shaft power is `W_dot_sh_x = W_dot_sh_ref*alpha`. The atmospheric
pressure comes from an altitude polynomial (`FUNCTION patm`) and the
water-vapour saturation pressure from the steam tables. Two exercises are
provided, selected by a `$if` directive in the native file.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Water/steam (`STEAM`, for the saturation pressure of the intake-air moisture) |
| **Size** | native file: 43 equations (largest block: 1, fully explicit); runnable variant: 22 equations |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP2_Ex_1-3/Détarage moteurs_Exercices_1-2.EES` (EES X10.589) |
| **Authors** | Philippe Ngendakumana (ULiège, course MCI), solution Rémi Dickes (ULiège) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** by `CS-GAP-IF-DIRECTIVE` (both `$if` branches kept → over-determined) and `CS-GAP-ACCENTED-IDENT` (accented variable names do not parse); the variant `engine_derating_iso3046_coolsolve.eescode` runs and is verified against the EES stored solution (14/14 common variables, max rel. diff 3.9e-6) |

## Problem statement

- **Exercise 1** (stored run, default): a naturally aspirated Diesel engine
  must deliver 372 kW on site at 400 m altitude, 45 °C ambient temperature
  and 80 % relative humidity; mechanical efficiency 0.85. ISO 3046/1
  reference conditions: 100 kPa, intake air 298 K (24.85 °C), 30 % RH;
  factor `a = 1`, exponents `m = 1`, `n = 0.75`, `s = 0`. Find the required
  catalogue (reference-condition) power `W_dot_sh_ref` and the derating
  factor `alpha`.
- **Exercise 2**: a supercharged Diesel with charge-air cooling, catalogue
  1000 kW, operated at 3000 m, 15 °C, 40 % RH; reference conditions 200 m,
  27 °C, 80 % RH, coolant 45 °C, `eta_m = 0.87`; `a = 0`, `m = 0.7`,
  `n = 1.2`, `s = 1`. Find the site power `W_dot_sh_x`.

## Model

- Atmospheric pressure from altitude (polynomial of the original,
  kPa in the original → Pa here): `patm(h) = (101.248815 - 0.0118062234*h + 4.72680601E-07*h^2)*1000`.
- Water-vapour saturation pressure at the intake-air temperature:
  `p_w_s = pressure(STEAM, T=T_a, x=1)` (steam tables, as in the original).
- ISO 3046/1 correction factor (absolute temperatures, K in the original):
  `K = ((p_atm_x - a*(phi_a_x/100)*p_w_s_x)/(p_atm_ref - a*(phi_a_ref/100)*p_w_s_ref))^m
  * ((T_a_ref)/(T_a_x))^n * ((T_c_ref)/(T_c_x))^s`.
- Derating factor: `alpha = K - 0.7*(1-K)*(1/eta_m - 1)`; site power
  `W_dot_sh_x = W_dot_sh_ref*alpha` (`alpha <= 1`).
- In exercise 1 the engine is naturally aspirated, so `T_c_x = T_a_x`
  (value assigned only to close the `s` exponent term, `s = 0`, as in the
  original).

| Inputs (exercise 1, default) | Value | Main outputs | Value |
|---|---|---|---|
| `W_dot_sh_x` site power | 372 kW | `alpha` derating factor | 0.8368 |
| `altitude` | 400 m | `K` correction factor | 0.8547 |
| `T_a_x` / `phi_a_x` | 45 °C / 80 % | `W_dot_sh_ref` required catalogue power | 444.6 kW |
| `eta_m` | 0.85 | `p_atm_x` | 96.60 kPa |

Exercise 2 (branch not shipped in the variant; recomputed with the same
equations as a sanity check, see *Conversion log*): `K` = 0.8383,
`alpha` = 0.8214, site power `W_dot_sh_x` = 821.4 kW from the 1000 kW
catalogue rating.

## How to run

The native file `engine_derating_iso3046.eescode` keeps the original EES
syntax (`$if` selection between the two exercises, accented variable names)
and does **not** run in CoolSolve v0.3.0 (see *Limitations and CoolSolve
gaps*). The runnable variant

```bash
coolsolve ./engine_derating_iso3046_coolsolve.eescode
```

resolves the `$if` branches to the stored run (exercise 1) and renames the
accented variables in ASCII (mapping in the *Conversion log*). It is fully
explicit (largest block: 1 equation) and needs no particular guess (see
`engine_derating_iso3046_coolsolve.initials`).

## Results

Default run (exercise 1): the naturally aspirated engine needs
`W_dot_sh_ref` = 444.6 kW of catalogue power to deliver 372 kW on site
(derating factor `alpha` = 0.8368, correction factor `K` = 0.8547).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g. a Parametric plot of alpha vs altitude (400 m … 3000 m) for the two exercises
     + one-line caption -->

## Verification

Reference: the EES stored solution of the source file (17 variables decoded;
the stored run is exercise 1). Comparison of the runnable variant
`engine_derating_iso3046_coolsolve.eescode` with
`compare_solution.py … --ees-units` (the source unit system is kPa/K/kW):

> 14 common variables, 0 differ (rtol=0.001); only in EES: 3; only in
> CoolSolve: 8

Maximum relative difference over the common variables: **3.9e-6** (on
`alpha`), driven by the steam saturation pressures (`p_w_s_x`: EES
9595.34 Pa vs CoolProp 9594.999 Pa at 45 °C, i.e. 3.5e-5). All fixed inputs
agree exactly.

- The 3 variables "only in EES" (`altitude_x`, `q`, `Test_x`) are stale
  variable records of exercise 2 and of the commented *Influence de
  l'humidité* block; they do not belong to the stored run (exercise 1).
- The 8 variables "only in CoolSolve" are the reference-condition inputs of
  exercise 1 and `W_dot_sh_ref`; EES did not store records for them (the
  accented names are absent from the decoded records; `W_dot_sh_ref` =
  `W_dot_sh_x/alpha` = 444 559.8 W with the EES `alpha`, 444 558.1 W with
  the CoolSolve one — the same 3.9e-6 difference).

Exercise 2 has no stored EES reference (the stored run is exercise 1); its
results above are a sanity check run with the same equations (hand-checked:
`K` = 0.785737 × 1.050180 × 1.015967 = 0.838340, `alpha` = 0.821431).

## Source and attribution

Source file `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP2_Ex_1-3/Détarage
moteurs_Exercices_1-2.EES` (EES X10.589, stored as RTF), from the ULiège MCI
course exercises (TP2, exercises 1-2), EES licence of Philippe Ngendakumana
(ULiège Thermotechnics); solution attributed to Rémi Dickes (ULiège) by the
source inventory. Correction law and factors/exponents per ISO 3046/1
(*Reciprocating internal combustion engines — Performance*, the standard's
reference conditions: 100 kPa, 298 K... as used by the original file).
Published under the library licence (MIT).

## Conversion log

- **2026-10-08 — import** (`ees_extract.py`): EES X10.589, RTF equations
  converted to text, `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or
  parametric table, 17 variables decoded. Unit system of the source
  `SI MASS DEG KPA K KJ` converted by hand to SI-°C-Pa-J:
  - `FUNCTION patm` now returns Pa (×1000 on the original kPa polynomial);
  - `p_atm_réf = 100` kPa → `p_atm_réf = 100E3` Pa; `W_dot_sh_x = 372` kW →
    `372E3` W; `W_dot_sh_réf = 1000` kW → `1E6` W (exercise 2);
  - temperatures were K in the original, °C here: `T_a_x = 45 + T_réf` →
    `T_a_x = 45` °C; the reference temperatures `T_a_réf = T_c_réf = 298` K →
    `24.85` °C; exercise 2: `T_a_réf = 27`, `T_c_réf = 45`, `T_a_x = 15`,
    `T_c_x = 40` °C. The temperature ratios of `K` are written with absolute
    temperatures: `(T_a_réf/T_a_x)^n` → `((T_a_réf+T_réf)/(T_a_x+T_réf))^n`
    (and likewise for `T_c`), the helper `T_réf = 273.15` kept as the K/°C
    offset; `pressure(STEAM,…)` now returns Pa;
  - the exponents and factors (`a`, `m`, `n`, `s`, `phi_a_*`, `eta_m`),
    altitudes and the correction equation are unchanged.
- **2026-10-08 — runnable variant** `engine_derating_iso3046_coolsolve.eescode`
  (only what the gaps force; the file stays valid EES):
  - `$if` branches resolved to the stored run: exercise 1 kept, exercise-2
    block omitted (`CS-GAP-IF-DIRECTIVE`); `Exercice$ = '1'` kept as
    documentation;
  - accented names renamed (`CS-GAP-ACCENTED-IDENT`): `W_dot_sh_réf` →
    `W_dot_sh_ref`, `p_atm_réf` → `p_atm_ref`, `T_a_réf` → `T_a_ref`,
    `T_c_réf` → `T_c_ref`, `T_réf` → `T_ref` (exercise 2 also has
    `Altitude_réf` → `Altitude_ref`; not used in the variant);
  - the commented `Test_réf`/`Test_x` diagnostic block of the original is
    kept commented out, with `Test_ref` renamed as above.
- **2026-10-08 — comment**: the exercise-2 comment of the original names the
  exponents "m, n et q" (the equation uses `s`); translated as in the
  original ("m, n and q"). No equation was changed for this.
- **Level**: equations 21 (< 50) → 0; largest block 1 → 0; a `FUNCTION` is
  used → 1; no multi-zone/multi-component structure → 0; semi-empirical
  correction law (ISO derating) → 1; no curated guesses needed → 0.
  Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- `CS-GAP-IF-DIRECTIVE` (registered): compile-time `$if`/`$endif` are parsed
  and ignored — **all** branches are kept, so the native two-exercise file is
  over-determined (e.g. `p_atm_réf` assigned twice: 100 kPa and
  `patm(Altitude_réf)`).
- `CS-GAP-ACCENTED-IDENT` (registered with this model): variable names with
  accented letters (`W_dot_sh_réf`, `T_a_réf`, …), valid in EES (the source
  file stores a solution), fail to parse in CoolSolve (*"Could not parse
  line"* on every line containing them).
- Physical note: the ISO 3046/1 correction uses the *saturation* vapour
  pressure at the intake-air temperature as the partial vapour pressure of
  the ambient humidity (multiplying the relative humidity), as in the
  original.

## Related models

None yet in the library (engine derating per ISO 3046/1).

# Approximate temperature of the Earth

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0357`

The Sun-Earth-space system is written as a radiation resistance network, as in
the original: the Sun (blackbody, 5800 K) and the Earth (blackbody) exchange
with each other and with space (2.7 K). In steady state the Sun-to-Earth heat
rate equals the Earth-to-space rate, which fixes the blackbody emissive power
of the Earth and hence its effective temperature (about 6 °C = 279.4 K).
Textbook example 10.3-3 of Nellis & Klein, *Heat Transfer* (2009).

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none (blackbody radiation network) |
| **Size** | 22 equations, all explicit (largest block: 1) |
| **Source** | Nellis & Klein, *Heat Transfer*, Cambridge University Press, 2009, example 10.3-3 ([EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/example_10.3-3_approximate_temperature_of_the_earth.ees)) |
| **Authors** | G. F. Nellis and S. A. Klein (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The Sun (diameter D_1 = 1.390e9 m, blackbody at 5800 K) is R = 1.497e11 m
away from the Earth (diameter D_2 = 1.276e7 m); space is a blackbody at
2.7 K. Write the radiation exchanges as a resistance network (view factors
from the disc-to-sphere geometry) and find the effective blackbody
temperature of the Earth.

## Model

Resistance network (kept as written in the original; resistances in 1/m²,
since the "conductance" of a radiative surface is A·F):

- Sun-to-Earth: F_12 = (π·D_2²/4)/(4π·R²), R_12 = 1/(A_1·F_12);
- Earth-to-space: F_23 = 1, R_23 = 1/(A_2·F_23);
- Sun-to-space: F_13 = 1, R_13 = 1/(A_1·F_13) (defined in the original but
  not used by the heat-rate equations).

Emissive powers E_b_i = σ·T_i⁴ (Stefan-Boltzmann law, absolute temperatures
T_1_K = T_1 + 273.15 and T_3_K = T_3 + 273.15 since T_1 and T_3 are stored
in °C, card decision C-519). Steady state: q̇_1→2 = (E_b_1 − E_b_3)/(R_12 + R_23)
= q̇_2→3, hence E_b_2 = E_b_1 − q̇_1→2·R_12 and
T_2_K = (E_b_2/σ)^(1/4), reported as T_2 = T_2_K − 273.15.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| D_1 / D_2 | 1.390e9 / 1.276e7 m | E_b_1 / E_b_3 | 6.4169e7 / 3.013e-6 W/m² |
| T_1 (Sun) | 5526.85 °C (5800 K in the original) | q̇_1→2 = q̇_2→3 | 1.769e17 W |
| T_3 (space) | −270.45 °C (2.7 K in the original) | E_b_2 (Earth) | 345.77 W/m² |
| R | 1.497e11 m | **T_2 (Earth)** | **6.293 °C (279.44 K)** |

## How to run

```bash
coolsolve ./earth_effective_temperature.eescode
```

No `.initials` needed: all 22 equations are explicit assignments (0
iterations). No `coolsolve.conf`, no variants.

## Results

T_2 = 6.293 °C, i.e. 279.44 K: the effective temperature of the Earth
modeled as a bare blackbody, before greenhouse-effect and albedo
considerations — textbook order of magnitude (~279 K).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of T_2 vs R (parametric sweep),
     figures/earth_effective_temperature_sweep.png + one-line caption -->

## Verification

Reference: the solution stored in the binary `.eez` companion of the source
file (`ees-examples-raw/uncategorized/example_10.3-3_approximate_temperature_of_the_earth.eez`,
EES X11.912), extracted with `tools/ees_extract.py`, compared with
`compare_solution.py --ees-units` (the stored T_1, T_2, T_3 are in K):

> 19 common variables, 0 differ (rtol=0.001); only in EES: 2; only in
> CoolSolve: 5 — "Only in EES reference: T_2C, T_2F"

The two only-in-EES variables are the Fahrenheit and °C output conversions
of the original, dropped by the card decision (see *Conversion log*); the
five only-in-CoolSolve variables are `pi`, `sigma#` and the three
absolute-temperature helpers `T_1_K`, `T_2_K`, `T_3_K`. Maximum relative
difference over the 19 common variables: 2.5e-7 (on `E_b_1`, `E_b_2`,
`E_b_3`, `q_dot_1to2`, `q_dot_2to3`, the σ·T⁴ quantities: EES stores the
Stefan-Boltzmann constant with slightly different last digits; the other
variables agree to ≤ 2.4e-9). Hand cross-checks: T_2 from the stored E_b_2,
(345.7699785/σ)^(1/4) = 279.44342 K against the stored 279.44344 K; the
stored T_2C/T_2F records (6.2934 °C / 43.328 °F) are consistent with the
stored T_2 = 279.4434 K.

## Source and attribution

Example 10.3-3 of **G. F. Nellis and S. A. Klein**, *Heat Transfer*,
Cambridge University Press, 2009, distributed as an EES example by F-Chart
Software. The plain-text mirror of the file is published under MIT by
[EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/example_10.3-3_approximate_temperature_of_the_earth.ees)
(inventory candidate `EEX-012`); the binary `.eez` with the stored solution
is `ees-examples-raw/uncategorized/example_10.3-3_approximate_temperature_of_the_earth.eez`
of the same repository (licence tag `{$ID$ … S.A. Klein, F-Chart Software}`:
licence holder, not authorship).

## Conversion log

- **2026-11-15 — import** (`tools/ees_extract.py` on the inner `.EES` of the
  `.eez` companion): EES X11.912, unit system `SI MASS RAD PA K J`. Unit
  conversion by hand to SI-°C-Pa-J (card C-519): `T_1 = 5526.85 [°C]` (5800 K
  in the original) and `T_3 = -270.45 [°C]` (2.7 K in the original); the
  Stefan-Boltzmann equations use the added absolute-temperature helpers
  `T_1_K = T_1 + 273.15`, `T_3_K = T_3 + 273.15`, and the Earth temperature
  comes back through `T_2_K = (E_b_2/sigma#)^(1/4)`, `T_2 = T_2_K - 273.15`.
  Per card decision: the `ConvertTemp` calls are not transcribed and the
  Fahrenheit output `T_2F` is dropped; the °C output `T_2C` is dropped too
  (`T_2` itself is now in °C). `sigma#` is a CoolSolve built-in constant
  (W/m²-K⁴) — no missing feature. The `[-]` unit annotations of the original
  comments are not written (library rule); the view-factor comments say
  "dimensionless". Display-only directives `$Tabstops` removed;
  `{$ID$}`, `{$PX$}`, `{$ST$}` tags removed by the extractor. The resistance
  network is kept as written, including `R_13` (defined but unused in the
  original). No lookup or parametric tables; comments kept (already English).
  No `.initials`: linear system, converges from the default guesses (0
  iterations, system square).
- **Level**: 22 equations → 0; largest block 1 → 0; no functions/arrays → 0;
  not multi-zone → 0; no semi-empirical/off-design physics → 0; no curated
  guesses → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- None. The bare-blackbody Earth ignores albedo and the greenhouse effect —
  as in the original (it gives ~6 °C, between the ~255 K of a bare Earth with
  albedo 0.3 and the 288 K observed mean surface temperature).
- No CoolSolve gap: `sigma#` is a built-in constant and the rest is plain
  algebra (`missing_features` empty).

## Related models

None: the other models of the category are conduction-oriented (resistance
and shape-factor library `CSL-0106`, 2-D plate `CSL-0341`, transient wall
`CSL-0340`, fuel element `CSL-0348`) and none models a radiation resistance
network. The nearest radiation models are the blackbody band-fraction
library `CSL-0346` (`blackbody_band_fraction`) and `radiation_heat_flux`.

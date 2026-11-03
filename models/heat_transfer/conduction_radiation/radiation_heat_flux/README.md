# Radiation heat flux: blackbody emission, grey-surface exchange, transmittance

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0107`

Three EES `FUNCTION`s for thermal radiation: `blackbody_spectral_radiance`
(Planck spectral radiance of a blackbody), `q_rad` (net radiant heat flux of
a grey surface exchanging with isothermal surroundings, with
back-radiation) and `grey_transmittance` (Beer-Lambert transmittance of a
grey absorbing medium). Temperatures are in °C, as everywhere in the
library; the functions add 273.15 internally (`ht` takes kelvin). This is
the `HT-021` family of the `ht` triage (roadmap card C-116); same layout
and same comment blocks as the first family, `CSL-0087`
*internal_turbulent_nusselt*.

| | |
|---|---|
| **Category** | Heat transfer › Radiation |
| **Fluids** | none (the relations take temperatures, an emissivity and medium properties as arguments) |
| **Size** | 8 equations after analysis (largest block: 1); 3 functions of 5–19 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/radiation.py` (MIT); inventory row `HT-021` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the relations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (8 values, max deviation 7.2·10⁻¹⁴) |

## Problem statement

For a surface at temperature `T` (emissivity `epsilon`), compute either its
spectral radiance at a wavelength `lambda` (Planck law), or its net radiant
heat flux when it exchanges with isothermal surroundings at `T2`
(back-radiation subtracted); and for a homogeneous grey (absorbing) medium,
compute the fraction of spectral radiance transmitted along a path of
length `L`. The three relations are independent; the choice between them is
left to the user, who knows the surface and the medium.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `blackbody_spectral_radiance` | T, wavelength | I = 2·h·c² / {wavelength⁵·[EXP(h·c/(wavelength·k·T_K)) − 1]}, T_K = T + 273.15; returns 0 when h·c/(wavelength·k·T_K) > 709.7 (exponential overflow, radiance below machine precision) | exact law, no range; wavelength > 0, T_K > 0 |
| `q_rad` | emissivity, T, T2 | q = emissivity·sigma·(T_K⁴ − T2_K⁴), T_K = T + 273.15, T2_K = T2 + 273.15 | grey diffuse surface in large isothermal surroundings, no range |
| `grey_transmittance` | extinction_coefficient, molar_density, length, base | tau = base^(−extinction_coefficient·molar_density·length) | homogeneous absorbing medium along the path, no range |

Arguments: `T` (surface temperature, `[C]`), `wavelength` (wavelength,
`[m]`), `emissivity` (fraction of blackbody emission, `[-]`, at most 1),
`T2` (surroundings temperature, `[C]`; `T2` may exceed `T`, giving a
negative flux), `extinction_coefficient` (at the modelled frequency,
`[m2/mol]`), `molar_density` (`[mol/m3]`), `length` (path length, `[m]`),
`base` (exponent base, `[-]`: `e` is more theoretically sound, 10 is often
used by chemists).

Constants used inside the functions (the values shipped by
`fluids.constants` with `ht` 1.2.0): h = 6.62607004·10⁻³⁴ J-s (Planck),
c = 299792458 m/s (speed of light), k = 1.380649·10⁻²³ J/K (Boltzmann),
sigma = 5.670367·10⁻⁸ W/m2-K4 (Stefan-Boltzmann).

Every function carries in its comment block (i) the equation, (ii) the
validity range **as quoted by `ht`**, (iii) the original paper or book and
(iv) the `ht` module, function, version and commit it was taken from.

The fourth member of the `ht` module, `solar_spectrum`, is **not**
translated: it only reads a 1.4 MB measured solar-spectrum data file, it is
not a correlation.

## How to run

Open `radiation_heat_flux.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./radiation_heat_flux.eescode
```

The demonstration program after the definitions calls each of the 3
functions twice: once (case *A*) with the input set of the `ht` doctest of
the corresponding function, once (case *B*) with a second input set. It
solves without any iteration (`Solver: SUCCESS (0 iterations)`, every
equation is explicit) and is the regression baseline
(`radiation_heat_flux.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these relations copies their
definitions in a block `{--- Library functions copied from CSL-0107 ---}` and
lists `CSL-0107` in its `related` field.

## Results

Values of the demonstration program (full precision in
`radiation_heat_flux.sol`):

| Quantity (case A) | CoolSolve | Quantity (case B) | CoolSolve |
|---|---:|---|---:|
| `I_blackbody_A` (800 K, 4 µm) | 1.311694129743e9 W/m2-sr-m | `I_blackbody_B` (1500 K, 2 µm) | 3.101260613135e10 W/m2-sr-m |
| `q_black_A` (black, 400 K, no back-radiation) | 1451.613952 W/m2 | `I_cold_B` (300 K, 10 µm) | 9.924033962032e6 W/m2-sr-m |
| `q_grey_A` (ε = 0.85, 400 K vs 305 K) | 816.7821722650 W/m2 | `q_hot_B` (ε = 0.9, 1000 K vs 300 K) | 50619.93324570 W/m2 |
| `tau_water_A` (1 cm water vapour, base e) | 0.8104707721191 [-] | `tau_base10_B` (base 10) | 0.8709635899561 [-] |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the Planck
     spectrum at two temperatures, e.g. spectral radiance vs wavelength at
     800 K and 1500 K, figures/radiation_heat_flux_planck.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/radiation.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*. The 8 output values of the demonstration
program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
8 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0
```

The largest relative deviation over the 8 values is **7.2·10⁻¹⁴**
(`I_blackbody_A`), i.e. round-off in the double-precision evaluation (the
kelvin inputs of `ht` were entered in °C: 800 K → 526.85 °C,
400 K → 126.85 °C, 305 K → 31.85 °C, 1500 K → 1226.85 °C,
1000 K → 726.85 °C, 300 K → 26.85 °C, 0 K → −273.15 °C).

Per-function values, `ht` / CoolSolve:

| Function | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `I_blackbody_A` | 1311694129.7430933 | 1.311694129743e9 | 7.1e-14 |
| `q_black_A` | 1451.613952 | 1451.613952 | 0.0e0 |
| `q_grey_A` | 816.7821722650002 | 816.7821722650 | 2.8e-16 |
| `tau_water_A` | 0.8104707721191062 | 0.8104707721191 | 7.7e-15 |
| `I_blackbody_B` | 31012606131.349194 | 3.101260613135e10 | 2.6e-14 |
| `I_cold_B` | 9924033.962031735 | 9924033.962032 | 2.7e-14 |
| `q_hot_B` | 50619.9332457 | 50619.93324570 | 0.0e0 |
| `tau_base10_B` | 0.8709635899560807 | 0.8709635899561 | 2.2e-14 |

All 8 relative deviations are below 7.2·10⁻¹⁴.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the radiation relations of `ht`, the heat-transfer
component of ChEDL, file `ht/radiation.py`, functions
`blackbody_spectral_radiance`, `q_rad` and `grey_transmittance`, version
1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every relation became one EES
`FUNCTION` named as in `ht`; temperatures are in °C (the library unit) with
`T_K = T + 273.15` evaluated inside each function (`ht` takes kelvin); the
optional surroundings temperature `T2` of `q_rad` (default 0 K in `ht`) and
the optional exponent base of `grey_transmittance` (default `e` in `ht`)
became mandatory arguments (EES has no optional arguments: pass
`T2 = -273.15` for no back-radiation, `base = EXP(1)` for `e`); the Python
`exp` became the EES `EXP`; the overflow guard `to_exp > 709.7` became an
EES `IF/THEN/ELSE`. No equation was changed. Scientific basis per function:
the original paper or book quoted in its comment block.

The scientific authors of the relations are credited in the comment block
of each function and in `model.json` (`origin.authors`): M. Planck, "Ueber
das Gesetz der Energieverteilung im Normalspectrum", Annalen der Physik
309(3), 1901 (`blackbody_spectral_radiance`); J. Stefan (1879) and
L. Boltzmann (1884) for the blackbody law (`q_rad`); P. Bouguer (1729),
J. H. Lambert (1760) and A. Beer (1852) for the attenuation law
(`grey_transmittance`).

## Conversion log

- **2026-10-07 — translation (T-FUNC card C-116, family `HT-021`).** One EES
  `FUNCTION` per `ht` relation (3 functions), named as in `ht`, with the
  formula, the validity range as quoted by `ht`, the original reference and
  the `ht` module/function/version/commit in the comment block. Arguments are
  the Python arguments, all in SI (°C for the temperatures — the absolute
  temperature `T + 273.15` is formed inside the functions, CoolSolve
  `docs/ees_import.md` §6.5 —, m for the wavelength and the path length) or
  dimensionless (rule 5 of `sources/ht/README.md` §7); no property function
  is used inside a function.
- `blackbody_spectral_radiance`: the Planck, light-speed and Boltzmann
  constants are local variables of the function with the values shipped by
  `fluids.constants` with `ht` 1.2.0 (h = 6.62607004E-34, not the exact SI
  6.62607015E-34 — this is what reproduces the doctest value); the
  docstring header says W/m²/sr/µm but the code returns per metre of
  wavelength, which is what the function returns (1.311694129743e9, not
  1.311694129743e3); the overflow guard of the `ht` code is an EES
  `IF/THEN/ELSE`.
- `q_rad`: the Stefan-Boltzmann constant is a local variable with the
  `fluids.constants` value (5.670367E-8); the optional `T2` became mandatory
  (the demonstration program passes −273.15 °C = 0 K for the no-back-radiation
  doctest, and 31.85 °C = 305 K for the grey case).
- `grey_transmittance`: the optional `base` became mandatory (the
  demonstration program passes `EXP(1)` for the `e` doctest and 10 for the
  chemist-base case); the power uses the EES `^` operator with a negative
  exponent, as the convection families of the batch do.
- **Not translated**: `solar_spectrum` only reads the 1.4 MB measured
  solar-spectrum data file `ht/data/solar_iss_2018_spectrum.dat`, it is not a
  correlation (excluded in the `ht` triage, `sources/ht/README.md` §6).
- **Level**: equations 8 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 1 → **level 1**; raised to **level 2** (± 1,
  docs/taxonomy.md §3), the reading of the other `ht` function libraries of
  the library (`CSL-0087`, `CSL-0105`), since the user has to know Planck's
  law, grey-surface exchange and Beer-Lambert attenuation to pick a relation.
- `stats.n_equations = 8`: the `coolsolve` analysis of the whole file reports
  `Equations: 8`, `Variables: 8`, `System square: Yes`, `Largest block: 1`.
  The file is written directly in the model folder and solves with the given
  input values, so no `.initials` file is needed.

## Limitations and CoolSolve gaps

- The demonstration input sets are the `ht` doctest values (case *A*) and
  one realistic second set (case *B*); `ht` checks no validity range in these
  functions, so the numbers of the *Results* and *Verification* tables are a
  check of the **equations**, not recommended design values.
- `q_rad` is the grey-surface-in-large-surroundings form only; view factors
  and multi-surface enclosures are not in `ht` and are not translated here.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  relations copies the definitions for now.
- No gap registered for this card: everything is plain EES
  (`FUNCTION`, `IF/THEN/ELSE`, `EXP`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` function library of
  the batch; same layout, comment blocks and demonstration program (two cases
  *A* doctest values and *B* Python values, README verification table
  `ht` vs CoolSolve).
- `CSL-0106` *conduction_resistances_and_shapes*: the conduction counterpart of this file in the same `ht` triage (resistances, shape factors, R-value conversions, 14 relations), same layout and same attribution.

# Blackbody band fraction f_1_2 (Planck law integral)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0346`

Fraction of the blackbody emissive power emitted between two wavelengths
$\lambda_1$ and $\lambda_2$ by a blackbody at the absolute temperature $T$,
obtained by numerical integration of the Planck spectral emissive power and
normalisation by the Stefan-Boltzmann law. A classic radiation-calculation
building block (glass, solar, furnace spectrum bands), kept as in the original
EES example: one page, three equations.

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none |
| **Size** | 8 equations (largest block: 0 — all explicit, one quadrature `INTEGRAL`) |
| **Source** | EES example *Blackbody* (F-Chart Software example set, `blackbody.ees`) |
| **Authors** | S. A. Klein (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The example of the EES documentation set calculates $f_{1\to2}$, the fraction
of the blackbody emissive power between the wavelengths $\lambda_1$ and
$\lambda_2$ at temperature $T$. In the original, $T$, $\lambda_1$ and
$\lambda_2$ are entered in the *Diagram window*; here they are equations, with
the values of the stored solution (T = 5000 K, band 0.3–0.7 µm).

## Model

- Planck spectral emissive power (first and second radiation constants $C_1$,
  $C_2$): $E_{\lambda b} = C_1 / [\lambda^5 (\exp(C_2/(\lambda\,T)) - 1)]$;
- total blackbody emissive power: $E_b = \sigma T^4$ (built-in `sigma#`);
- band fraction: $f_{1\to2} = \int_{\lambda_1}^{\lambda_2} E_{\lambda b}\,
  \mathrm{d}\lambda \,/\, E_b$ (EES `INTEGRAL`, fixed step 0.01 µm).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T` absolute temperature | 5000 K | `f_1_2` band fraction | 0.3700 |
| `lambda_1` / `lambda_2` | 0.3 / 0.7 µm | `E_b` total emissive power | 3.544e7 W/m² |
| | | `E_lambda_b` at $\lambda_2$ | 3.711e7 W/m²·µm |

Units are those of the original example: absolute temperature in K and
wavelength in µm, the micrometre convention of the EES radiation constants
`C1#` = 3.7420E8 W·µm⁴/m² and `C2#` = 14388 µm·K (written explicitly here,
see *Conversion log*). $f_{1\to2}$ is independent of this convention.

## How to run

```bash
coolsolve ./blackbody_band_fraction.eescode
```

Change `T`, `lambda_1`, `lambda_2` for another band; the integration step 0.01
(in µm) follows the original. `.initials` holds the stored values of the
original file (guess for the integration variable `lambda`).

## Results

For T = 5000 K, 0.3–0.7 µm: `f_1_2` = 0.3700 (37.0 % of the emissive power in
the visible/near-IR band), `E_b` = 3.544e7 W/m². The solve also writes the
`-integral.csv` table: the quadrature trajectory of `f_1_2` and `E_lambda_b`
from $\lambda_1$ to $\lambda_2$ (source of the figure below).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of f_1_2 and E_lambda_b vs lambda
     (Integral tab, from blackbody_band_fraction-integral.csv) -->

## Verification

Compared with the solution stored in the source EES file
(`compare_solution.py blackbody_band_fraction.sol reference/ees_variables.csv --all`):

| Variable | EES | CoolSolve | rel. diff | |
|---|---:|---:|---:|---|
| E_b | 3.54351e+07 | 3.54398e+07 | 1.35e-04 | ok |
| E_lambda_b | 3.71082e+07 | 3.71082e+07 | 1.06e-10 | ok |
| f_1_2 | 0.370049 | 0.370047 | 4.86e-06 | ok |
| lambda | 0.7 | 0.7 | 0.00e+00 | ok |
| lambda_1 | 0.3 | 0.3 | 0.00e+00 | ok |
| lambda_2 | 0.7 | 0.7 | 0.00e+00 | ok |
| T | 5000 | 5000 | 0.00e+00 | ok |

7 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 3
(C1, C2, sigma# — constants of the transcription, see *Conversion log*).

The 1.35e-04 deviation on `E_b` is the Stefan-Boltzmann constant: the stored
value implies σ = 5.66961e-8 W/m²-K⁴, CoolSolve ships the CODATA value
5.670374419e-8 (`sigma#`); it propagates to `f_1_2` at 4.9e-06 relative — the
triage value f_1_2 = 0.3700 at T = 5000 K between 0.3 and 0.7 µm is
reproduced.

The parametric table stored in the original (100 rows of $E_{\lambda b}(T{=}5000\,K)$
from 0.05 to 626 µm, a Planck-curve sweep) was used to pin the constants: the
transcribed $C_1$, $C_2$, T reproduce all 100 rows to a relative residual of
1e-16, and the CoolSolve integral-table value at 0.37 µm (2.26277e7 W/m²·µm)
matches the table row at 0.37001 µm (2.26298e7 W/m²·µm, 0.001 µm apart).

## Source and attribution

EES example file `Blackbody.EES` of the F-Chart Software example set
(documented in the EES manual; plain-text MIT mirror
`https://github.com/EES-Community/ees-examples`, `uncategorized/blackbody.ees`,
which carries the same equations and the download link
`https://fchartsoftware.com/ees/examples/blackbody.ees`). No personal data.
Source binary: `~/Nextcloud/thermo_models/EES_library/Blackbody.EES`
(EES X8.806, inventory candidate `EEL-024`).

## Conversion log

- **2026-11-14 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `$UnitSystem SI MASS DEG KPA C KJ` — no pressure or energy
  quantity appears in the equations, so the kPa/kJ setting has no effect and
  the model keeps its own consistent working units (T in K, λ in µm), as in
  the original; no property call is involved. The EES licence tag was removed.
  Diagram-window inputs `T`, `lambda_1`, `lambda_2` are not part of the
  equations window: they were written into the file with the values of the
  stored solution (per card C-517; no diagram-window gap registered).
- **2026-11-14 — built-in constants.** The original uses the EES built-in
  radiation constants `C1#` and `C2#`; CoolSolve does not provide them (they
  are read as unknown variables and the system is not square), while `sigma#`
  is provided. The model writes their documented values explicitly:
  `C1 = 3.7420E8` [W-µm⁴/m²], `C2 = 14388` [µm-K]. The values were confirmed
  against the file itself: they reproduce the stored solution and all 100 rows
  of the stored parametric table (see *Verification*). This is the only change
  to the original equations; no `_coolsolve` variant is needed.
- **Level**: 8 equations (< 50) + largest block ≤ 5 + no function/array
  structure + no multi-zone + no calibration + no curated guesses → score 0 →
  level 1.

## Limitations and CoolSolve gaps

- No physical limitation beyond the model itself: exact laws, valid for any
  T > 0 K and any band; the fixed step 0.01 (in µm) is the original's.
- CoolSolve does not provide the EES built-in constants `C1#`/`C2#` (not
  registered in the gap register at the decision of the card: the model writes
  their values explicitly). `sigma#` is provided.

## Related models

- `CSL-0107` *radiation_heat_flux*: the radiation function library
  (Planck spectral radiance, grey-surface net flux, grey transmittance); this
  model adds the integrated band fraction, which it does not carry. Link the
  two when computing grey-surface exchange over a spectral band.

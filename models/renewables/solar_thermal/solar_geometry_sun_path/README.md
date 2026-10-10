# Solar geometry and sun path

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0119`

Solar geometry for a fixed site (Port-au-Prince, Haiti): day of the year
from month and day, solar declination, hour angle, angle of incidence on a
south-facing vertical surface, zenith angle, solar altitude and azimuth, and
the sunrise/sunset hour angle with the corresponding solar times, plus the
solar-noon point used for the sun-path plot.

| | |
|---|---|
| **Category** | Renewable energy › Solar thermal |
| **Fluids** | none |
| **Size** | 22 equations, all explicit (largest block: 1) |
| **Source** | ULiège collection, `solar/angles.EES` (inventory `TM-0589`) |
| **Authors** | TBD (ULiège, J. Lebrun laboratory — the file carries only the laboratory licence stamp; to be completed by the maintainer) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file blocked by `CS-GAP-NDAY` (`nDay_`; `CS-GAP-IF-DIRECTIVE` is closed in `fix/library-gaps-2` @9423934); runnable variant `solar_geometry_sun_path_coolsolve.eescode` verified against EES (see *Verification*) |

## Problem statement

For the site of Port-au-Prince, Haiti (latitude 18.53 °N, longitude
72.335 °W) and a given date (month, day) and solar time `t`, compute the
sun position: declination `delta`, hour angle `omega`, incidence angle on a
south-facing vertical surface `theta_s`, zenith angle `theta_z`, solar
altitude `alpha_s` and solar azimuth `gamma_s`, and the sunrise/sunset hour
angle `omega_s` with the sunset and sunrise solar times `t_coucher` and
`t_lever`. A second block evaluates the same quantities at a plot time
`t_solaire` (solar noon by default) for the sun-path plot (`t[1]`,
`alpha_s[1]`).

## Model

Day of the year `n` from month and day (EES date function `nDay_` in the
original), declination `delta = 23.45·sin(360·(284 + n)/365)`, hour angle
`omega = 15·(t − 12)`, incidence and zenith angles from their cosine laws,
altitude `alpha_s = max(0, 90 − theta_z)`, azimuth equated to the hour angle
`gamma_s = omega` (as in the original), and sunrise/sunset from
`omega_s = arccos(−tan(phi)·tan(delta))`. The site longitude `L_loc` is
carried as in the original (it documents the site and feeds no equation).

| Inputs | Value (default run) | Outputs (default run) | Value |
|---|---|---|---|
| `phi` site latitude | 18.53 ° | `n` day of the year | 338 |
| `month` / `day` | 12 / 4 | `delta` declination | −22.48 ° |
| `t` solar time | 24 h (midnight, stored EES run) | `omega` hour angle | 180 ° |
| `t_solaire` plot time | 12 h (solar noon) | `theta_z` zenith angle | 176.05 ° |
| | | `alpha_s` solar altitude | 0 ° (night) |
| | | `omega_s` sunset hour angle | 82.03 ° |
| | | `t_coucher` / `t_lever` | 17.47 / 6.53 h |
| | | `alpha_s_t` noon altitude | 48.99 ° |

## How to run

The native file is blocked by `nDay_` (see *Limitations and CoolSolve gaps*); since
`fix/library-gaps-2` @9423934 CoolSolve keeps its `$ifnot parametrictable` block
(`t = 0`) and the system is square (22 equations, 22 unknowns). Run the
variant instead, in the CoolSolve GUI (*Solve*) or from a terminal:

```bash
coolsolve ./solar_geometry_sun_path_coolsolve.eescode
```

Change `t` (0–24 h), `month`/`day` and `phi` for another hour, date or site.
No `.initials` or `coolsolve.conf` is needed (fully explicit cascade, 24
iterations). The variant is regression-tested as `CSL-0119:coolsolve`.

## Results

Default run (stored EES run: 4 December, solar midnight; noon point at
`t_solaire` = 12 h):

| Quantity | EES | CoolSolve (variant) |
|---|---:|---:|
| `n` | 338 | 338 |
| `delta` [°] | −22.4819 | −22.4819 |
| `omega` [°] | 180 | 180 |
| `theta_s` [°] | 86.0481 | 86.0481 |
| `theta_z` [°] | 176.0478 | 176.0481 |
| `alpha_s` [°] | 0 | 0 |
| `omega_s` [°] | 82.0267 | 82.0267 |
| `t_coucher` [h] | 17.4684 | 17.4684 |
| `t_lever` [h] | 6.5316 | 6.5316 |
| `alpha_s_t` (noon) [°] | 48.9881 | 48.9881 |

At midnight the sun is below the horizon (`theta_z` = 176 °, `alpha_s` = 0);
at solar noon it culminates at 49.0 ° altitude. Sunrise and sunset are
symmetric about noon (6.53 h / 17.47 h, day length 10.94 h).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot of
      the solar altitude vs solar time over one day (CoolSolve has no sun-path diagram) -->

## Verification

**Runnable variant vs the EES stored solution** of `solar/angles.EES`
(22 variables decoded by `tools/ees_extract.py`):

`22 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

Maximum relative difference 1.5e-6 (on `theta_z`, pure trigonometric
round-off near the flat cosine extremum; all other variables agree to at
least 1e-7). No variable was excluded. Spot checks against closed-form
re-evaluation: `n` = 338 for 4 December, `omega_s` = 82.03 °,
`t_coucher` = 12 + 82.03/15 = 17.47 h, noon `theta_z` = 41.01 °.

## Source and attribution

No author is named in the file; it carries only the J. Lebrun laboratory
licence stamp (`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique,
Univ. Liege}`). Origin to be completed by the maintainer.

Source file (EES X8.198, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/solar/angles.EES` (inventory candidate `TM-0589`).

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`): unit system already
  SI-C-Pa-J (`SI MASS DEG PA C J`), no conversion needed; the EES licence
  tag was removed; comments translated to English and the standard header
  added. No lookup or parametric tables in the file.
- **2026-10-07 — diagram/parametric inputs restored as defaults.** Four
  variables have no equation in the extracted text (commented out by the
  author when the inputs moved to the EES Diagram window / parametric
  table): `phi`, `month`/`day`, `t` and `t_solaire`. The unmodified
  extraction is 18 equations for 22 unknowns (`coolsolve -d`: *"There are
  18 equations and 22 unknowns"*), which is the Diagram-window use of the
  file, not an under-determined model. They were restored with the values
  of the stored EES run (`phi` = 18.53 °, `month` = 12, `day` = 4,
  `t_solaire` = 12 h); `t` follows the `$ifnot parametrictable` branch
  (`t` = 0 outside a parametric table). Note: the commented date in the
  text is June 4 (`month` = 6), the stored run used December 4 (`n` = 338).
- **2026-10-07 — runnable variant** `solar_geometry_sun_path_coolsolve.eescode`
  (valid EES, verified above): (1) the EES date function `n = nDay_(month, day)`
  is replaced by an explicit `FUNCTION day_of_year(month, day)` summing the
  month lengths before `month` with eleven sequential block `IF/ELSE/ENDIF`s
  (`CS-GAP-NDAY`; block form, since the single-line `IF…THEN…ELSE` must not
  be followed by `ENDIF`); (2) the `$ifnot parametrictable` branch is
  resolved for the stored run — the `t = 0` line is dropped and `t` is set
  to 24 h, the solar time of the stored EES run (parametric-table inputs
  become the default run, `CS-GAP-IF-DIRECTIVE`). Nothing else changes
  (same variable names, same equations).
- **2026-10-10 — re-check** with CoolSolve `fix/library-gaps-2` @9423934
  (`CS-GAP-IF-DIRECTIVE` closed): the `$ifnot parametrictable` directive is now
  evaluated (the block `t = 0` is kept, as EES does outside a parametric table);
  the native file is square (22 equations) and stops at *Unknown function nDay_*
  (`CS-GAP-NDAY`), so it stays **blocked**. Check in a scratch copy: with
  `n = nDay_(month, day)` replaced by `n = 338` and `t = 24`, the native file gives
  the same `.sol` as the variant (22 variables, identical). The variant is kept: its
  `nDay_` replacement is still needed; its `t = 24` setting is not a workaround
  but the default run chosen to reproduce the stored (parametric-table) EES values.
- **2026-10-07 — checks.** The solar azimuth is equated to the hour angle
  (`gamma_s = omega`), as in the original; kept faithfully. The site
  longitude `L_loc` feeds no equation, as in the original; kept as site
  documentation.
- **Level**: equations 22 (< 50: 0) + largest block 1 (0) + arrays `t[1]`,
  `alpha_s[1]` (1) + single-zone, explicit physics (0) + no curated guesses
  needed (0) = score 1 → level 1.

## Limitations and CoolSolve gaps

- `CS-GAP-NDAY` (new, registered with this model): the EES date function
  `nDay_(month, day)` is unknown to CoolSolve — the native file fails with
  *"Unknown or unsupported function: nDay_ with 2 arguments"* although the
  system is square (22 equations / 22 unknowns, largest block 1).
- `CS-GAP-IF-DIRECTIVE` (already registered; **closed** in CoolSolve
  `fix/library-gaps-2` @9423934): `$ifnot parametrictable` was parsed but ignored.
  It is now evaluated (the `t = 0` block is kept, as in EES outside a parametric
  table); the stored parametric run (`t` = 24) is a table value, not the default of
  the native file, hence the `t = 24` of the variant.
- The model covers one site and one date per run; a full sun-path curve is a
  parametric sweep of `t` (no EES parametric table is shipped with the file).

## Related models

- `CSL-0082` *parabolic_trough_receiver_forristal*: same sub-category; a
  steady 1D parabolic-trough receiver balance that needs solar geometry as
  input.
- `CSL-0083` *parabolic_trough_loss_correlations*: same sub-category;
  empirical collector efficiency and loss correlations.

# Intake valve sizing for a square engine

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0178`

Teaching exercise (ULiège MCI, TP5, exercise 1): size the intake valves of a
square four-cylinder engine. The bore follows from the total displacement, the
mean piston speed from the stroke and the rotational speed, and the speed of
sound is evaluated at the intake-air temperature. The total intake area is the
lecture rule of the original, shared by two valves.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 18 equations (largest block: 2) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_1_Dimensionnement de soupapes_PNG.EES` (EES X10.409) |
| **Authors** | TBD (ULiège MCI) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (max rel. diff 9.78e-04) |

## Problem statement

Size the intake valves of a square engine (stroke equal to bore).

Data, as written in the file:

- total displacement `V_s = 2.8e-3` m³
- `nc = 4` cylinders
- rotational speed `Rpm = 7500` 1/min
- intake air temperature `T_a = 60` °C
- `ns = 2` valves
- universal gas constant `R_u = 8314` J/(kmol·K)

The total intake area follows the lecture rule cited in the file (course 4,
2015-2016, slide 33):

\[
A_{\mathrm{eff,in}} = 1.3\, D^{2}\, (C_m / C_i)
\]

The valve diameter shares that area between the valves. The maximum lift sets
the curtain area equal to the valve-head area; the original neglects the
valve-stem blockage in the intake port. The original recalls that the objective
is intake-area to piston-area ratios up to 0.5.

## Model

Square engine and displacement (the second equation solves the bore):

\[
L/D = 1, \qquad V_s = n_c \, \pi \, (D^{2}/4) \, L
\]

Mean piston speed, with `N = Rpm/60`:

\[
C_m = 2\, L\, N
\]

Speed of sound in the intake air. `gamma` is `CP(Air,T=T_a)/CV(Air,T=T_a)` and
`r_a = R_u/MOLARMASS(Air)`:

\[
C_i = \sqrt{\gamma\, r_a\, (T_a + 273.15)}
\]

`C_i_bis` repeats the speed of sound with `SOUNDSPEED`. CoolSolve requires a
pressure for that call on ideal-gas Air, so the file passes `P=101325` Pa (the
reference pressure CoolSolve uses for other temperature-only ideal-gas
properties). The original call is `SOUNDSPEED(Air,T=T_a)`.

Area ratio, valve diameter and maximum lift:

\[
\mathrm{Ratio} = A_{\mathrm{eff,in}} / (\pi D^{2}/4), \qquad
A_{\mathrm{eff,in}} = n_s \, \pi \, (d_v^{2}/4), \qquad
\pi\, d_v\, h_{\max} = \pi\, (d_v^{2}/4)
\]

The last equation gives `h_max = d_v/4`.

| Quantity | Role | Value |
|---|---|---|
| `V_s` | total displacement | 2.8×10⁻³ m³ |
| `nc` | number of cylinders | 4 |
| `Rpm` | rotational speed | 7500 1/min |
| `T_a` | intake air temperature | 60 °C |
| `ns` | number of valves | 2 |
| `L/D` | square engine | 1 |
| `R_u` | universal gas constant, as written | 8314 J/(kmol·K) |
| `D`, `L` | bore and stroke | solved |
| `C_m`, `C_i` | mean piston speed, speed of sound | solved |
| `A_eff_in`, `d_v`, `h_max`, `Ratio` | intake area, valve diameter, lift, area ratio | solved |

One algebraic block couples `L` and `D`. Every other equation is explicit.
`C_i_bis` is a check: it is not used by the sizing equations.

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./intake_valve_sizing.eescode
```

`intake_valve_sizing.initials` holds the EES stored values. `d_v` and `h_max`
are absent from that list and start from the default guess. With the file the
solver reports 13 iterations, and the bore matches the stored value. Without
the file it reports 22 iterations and reaches the same bore within 7×10⁻⁸
relative. The shipped `.sol` is the run that starts from the stored guesses.
No `coolsolve.conf` and no variant.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `D`, `L` [m] | 0.09623566527 | 0.09623566527 |
| `N` [1/s] | 125 | 125 |
| `C_m` [m/s] | 24.05891632 | 24.05891632 |
| `r_a` [J/(kg·K)] | 287.03152 | 287.03142 |
| `gamma` [-] | 1.400191 | 1.398821 |
| `C_i` [m/s] | 365.913 | 365.734 |
| `C_i_bis` [m/s] | 365.898 | 365.742 |
| `Ratio` [-] | 0.108831 | 0.108884 |
| `A_eff_in` [m²] | 7.91613×10⁻⁴ | (not stored) |
| `d_v` [m] | 0.022449 | (not stored) |
| `h_max` [m] | 0.005612 | (not stored) |

Orders of magnitude: a square 2.8 L four-cylinder engine has a bore near 96 mm;
at 7500 1/min the mean piston speed is about 24 m/s; the speed of sound in air
at 60 °C is about 366 m/s; the area ratio 0.11 sits below the 0.5 objective
recalled in the file; `h_max = d_v/4`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Ideal-gas sizing model: the maintainer's figure is a parametric sweep (for
example `Ratio` against `Rpm`), saved as `figures/intake_valve_sizing_sweep.png`.

## Verification

Reference: the solution stored in the EES file (15 variables decoded by
`ees_extract.py`; the unit system is already `SI MASS DEG PA C J`, so the
comparison is without `--ees-units`). `compare_solution.py` on
`intake_valve_sizing.sol` against `reference/ees_variables.csv`:

> 15 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 4

Maximum relative difference over all common variables, as printed in the tool's
table: **9.78e-04** (`gamma`). Nothing exceeds rtol 0.001.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `gamma` | 1.39882 | 1.40019 | 9.78e-04 |
| `C_i` | 365.734 | 365.913 | 4.89e-04 |
| `Ratio` | 0.108884 | 0.108831 | 4.89e-04 |
| `C_i_bis` | 365.742 | 365.898 | 4.26e-04 |
| `r_a` | 287.031 | 287.032 | 3.45e-07 |
| `C_m` | 24.0589 | 24.0589 | 1.04e-10 |

`D`, `L`, `N`, `Rpm`, `V_s`, `nc`, `ns`, `R_u` and `T_a` agree exactly (rel. diff `0.00e+00`).

`gamma = CP(Air,T=60)/CV(Air,T=60)` is where CoolProp and EES differ. `C_i`
uses that `gamma` (and `r_a`), and `Ratio` is proportional to `C_m/C_i`, so
those two carry the same 4.89e-04. `r_a` follows the molar mass of Air
(3.45e-07). `C_i_bis` is `SOUNDSPEED(Air,T=60,P=101325)` against the stored
`SOUNDSPEED(Air,T=60)`; moving the added pressure from 101325 Pa to 1×10⁵ Pa
changes the CoolProp value by about 5×10⁻⁶ relative, so the 4.26e-04 is the
property backend.

The four names present only in the CoolSolve solution are `A_eff_in`, `d_v`
and `h_max` (the stored list stops at 15 variables) and `pi` (the built-in
constant written into the `.sol`).

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_1_Dimensionnement de soupapes_PNG.EES`
(EES X10.409, stored as RTF). The equation window names no author. The
`{$ID$}` tag is the EES licence of Philippe Ngendakumana (ULG Thermotechnics,
Liège), which is the licence holder and not an author line. The inventory row
TM-0241 attributes the file to P. Ngendakumana and R. Dickes. Authors in
`model.json` stay `TBD (ULiège MCI)` until that attribution is confirmed.
ULiège course MCI, TP5, exercise 1. Published under the library licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`): EES X10.409, RTF equations
  converted to text, `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or
  parametric table, 15 variables decoded, no extract warnings. Unit system
  already `SI MASS DEG PA C J`: `$UnitSystem` removed, no value rescaled. The
  formatting directive `$TABSTOPS` was removed (it is not an equation). The
  unmodified extract, with the NUL byte and the `$UnitSystem` line removed, is
  square (18 equations, 18 variables), so no Diagram-window value was restored
  and no computed unknown was replaced by a stored number. Stored values are
  the `.initials` guesses. Comments translated to English; variable names kept
  (`Rpm` and `rpm` are the same variable). 
- **2026-10-15 — soundspeed call**: `C_i_bis = SOUNDSPEED(Air,T=T_a)` rewritten
  as `SOUNDSPEED(Air,T=T_a,P=101325)`. CoolSolve rejects the temperature-only
  call (`Ideal gas property 'soundspeed' requires pressure input`); `cp` and
  `cv` of Air at `T` alone are accepted. 101325 Pa is the reference pressure
  CoolSolve uses internally for other temperature-only ideal-gas properties.
  The call stays valid EES syntax. Same equation count. Logged here, not as a
  variant and not as a missing feature.
- **Level**: equations 18 (< 50) → 0; largest block 2 (≤ 5) → 0; no user
  function, procedure, array or `DUPLICATE` → 0; one component, no multi-zone
  discretisation → 0; the factor 1.3 is a given lecture constant (no
  calibration, off-design, part-load or dynamics) → 0; converges from the
  default guess without a tuned configuration → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- The coefficient 1.3 and the neglect of the valve stem are the hypotheses of
  the exercise.
- `gamma`, `C_i`, `C_i_bis` and `Ratio` follow the ideal-gas properties of
  `Air` and therefore differ slightly between CoolProp and EES (see
  Verification). All stay inside rtol 0.001.
- Calling `SOUNDSPEED` on `Air` prints a warning that moist air should use
  `AirH2O`. The fluid in the file is ideal-gas `Air`; the warning is the name
  check, and the fluid is unchanged.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

- `CSL-0185` (*diesel_injection_sizing*): TP5 exercise 4, diesel
  injection duration and mixture richness. This model is exercise 1, the
  intake valve.
- `CSL-0275` (*square_v6_engine_exercise*): MCI TP3 exercises 1-3 on a
  square V6 engine (bore/stroke from the displacement, mean piston speed).

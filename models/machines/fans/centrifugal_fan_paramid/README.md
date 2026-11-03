# Centrifugal fan parameter identification from four catalogue points

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0165`

Parameter identification of a centrifugal fan from the ULiège model bank.
Four manufacturer points (volume flow, total pressure rise, isentropic
effectiveness, outlet velocity), taken at one supply state and one rotation
speed, determine the eight coefficients of the cubic maps

`phi = alpha_0 + alpha_1·psi + alpha_2·psi² + alpha_3·psi³`

`lambda = beta_0 + beta_1·psi + beta_2·psi² + beta_3·psi³`

and the average equivalent exhaust area. The reference simulation
`CSL-0071` uses these coefficients, rounded, as data.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | AirH2O |
| **Size** | 113 equations (largest block: 4) |
| **Source** | ULiège model bank, fan parameter-identification model (2008-03-18) |
| **Authors** | Vlad Teodorese, Andrés Rodríguez; reviewed by Jean Lebrun |
| **License** | MIT |
| **CoolSolve** | 0.3.0@261f0b9 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The manufacturer gives four operating points of a fan (impeller diameter
0.323 m, 4000 min⁻¹, supply air 20 °C, relative humidity 0.5, 101 325 Pa).
Identify the dimensionless flow and power maps and the mean equivalent
exhaust area. The reference is ASHRAE HVAC Systems and Equipment (2004), as
cited in the original file.

## Model

Each point uses the same relations as `CSL-0071`:

- flow factor `phi = V_dot/(A·U)`, reference area `A = pi·D²/4`, peripheral
  speed `U = pi·D·N`, `N = rpm/60`;
- pressure factor `psi = Δp_total / (U²/(2·v))`, with the exhaust dynamic
  pressure `C_ex²/(2·v)` and `Δp_total = Δp_stat + P_dynam_ex`;
- power factor `lambda = phi·psi/epsilon_s`, isentropic power
  `W_dot_s = V_dot·Δp_total`;
- humid-air specific volume and specific heat at the supply state.

The four points share `alpha_0…3` and `beta_0…3`, so the two cubics are
exactly determined. `A_bar_ex` is the mean of the four equivalent exhaust
areas `V_dot/C_ex`.

| Point | Volume flow | Total pressure | Effectiveness | Outlet velocity |
|---|---:|---:|---:|---:|
| 0 | 4000 m³/h | 2750 Pa | 0.65 | 6.95 m/s |
| 1 | 9100 m³/h | 2100 Pa | 0.75 | 15.8 m/s |
| 2 | 13000 m³/h | 1075 Pa | 0.50 | 22.3 m/s |
| 3 | 14500 m³/h | 375 Pa | 0.22 | 25.02 m/s |

In the original these values, and `D`, `rpm`, `T_su`, `RH_su`, `P_su`, are
Diagram-window inputs (quoted strings, marked `! in diagram`). Each is
assigned its stored value. The stored run is the regression case.

## How to run

```bash
coolsolve ./centrifugal_fan_paramid.eescode
```

The model solves from the default guesses (106 iterations). The shipped
`.initials` are the EES stored values and bring that down to 24 iterations.

## Results

Identified coefficients. The EES column is the stored solution.

| Coefficient | CoolSolve | EES |
|---|---:|---:|
| `alpha_0` | 0.77331 | 0.77331 |
| `alpha_1` | −0.38909 | −0.38896 |
| `alpha_2` | 0.44737 | 0.44709 |
| `alpha_3` | −0.61840 | −0.61781 |
| `beta_0` | 0.40790 | 0.40803 |
| `beta_1` | 0.35700 | 0.35700 |
| `beta_2` | −0.07775 | −0.07773 |
| `beta_3` | −0.36734 | −0.36711 |
| `A_bar_ex` | 0.16069 m² | 0.16069 m² |

`CSL-0071` uses the rounded catalogue values `alpha = (0.7733, −0.389,
0.4471, −0.6178)` and `beta = (0.408, 0.357, −0.07773, −0.3671)`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against the stored solution:

> 113 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

The one difference, quoted as printed:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `DELTAP_stat3` | 2.43636 | 2.31853 | 4.84e-02 |

Maximum relative difference **4.84e-02**. Point 3 imposes `DELTAP_total3` =
375 Pa and the static rise is the remainder `375 − P_dynam_ex3`. The exhaust
dynamic pressure, the specific volume and the pressure factors all differ by
**3.16e-04** (CoolProp humid air against the EES formulation, at 20 °C,
101 325 Pa, RH = 0.5). That absolute difference, 0.118 Pa, is 4.84 % of the
2.44 Pa remainder. At rtol = 1e-4, 36 variables differ and 35 of them are
this same 3.16e-04. `A_bar_ex` agrees: the areas are `V_dot/C_ex` and do not
use the density.

The name only in the CoolSolve solution is `pi`. The empty stored name `b`
is a Diagram-window leftover and is not a variable of the model.

## Source and attribution

Vlad Teodorese and Andrés Rodríguez, University of Liège, Thermodynamics
Laboratory, 18 March 2008; reviewed by Jean Lebrun. Contact in the file:
`aarodriguez@ulg.ac.be`. The equations window carries the laboratory
disclaimer (freely distributed, may not be sold, cite the origin). EES
licence stamp: Jean Lebrun, Laboratoire de Thermodynamique, Université de
Liège (`{$ID$ #1206}`), EES X7.966. Reference cited in the file: ASHRAE
(2004), HVAC Systems and Equipment Handbook.

Source:
`~/Nextcloud/thermo_models/Model data bank/Distribution_Systems/Fans/CENTRIFUGAL_FAN_PARAMID_REFERENCE_MODEL_ARJL080121.zip!/Centrifugal_Fan_ParamID_Reference_EES_Model_ARJL080121.EES`
(inventory `TM-0485`). Companion of the reference simulation `TM-0251`
(`CSL-0071`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py` on the zip member):
  equations stored as **RTF**; unit system already `SI MASS DEG PA C J`, so
  no unit conversion; `$UnitSystem` removed; no lookup or parametric table;
  licence tag removed. `Phi` at point 0 is the same variable as `phi` (EES
  names are case-insensitive) and is written `phi`.
- **Diagram-window inputs restored as equations.** Twenty-one manufacturer
  and geometry values are quoted strings. Each is assigned its stored value,
  which makes the identification square (113 equations). The original equations that relate `V_dot_mh`, `DELTAP_total` and
  `epsilon_s` to the other unknowns are kept, so those assignments close the
  system rather than replace it.
- **Export block omitted.** The original ends with
  `results_file$ = concat$(EESFILEDIR$, 'results_RZR315.txt')` and
  `$Export results_file$ alpha_0, …, A_bar_ex`, which write the coefficients
  to a text file. CoolSolve will not implement `$Export`. The two lines do
  not enter the identification, so they are deleted from the model. No
  variant, and the omission is not listed in `missing_features`.
- The original labels `P_dynam_ex3 = C_ex3^2/(2*v3)` as "peripheral dynamic
  pressure"; the comment is kept as written. The peripheral dynamic pressure
  is the next equation, `U3^2/(2*v3)`.
- **Level**: 113 equations (1), largest block 4 (0), no procedure or array
  (0), one fan (0), catalogue identification (1), solves from the default
  guesses (0) → score 2 → level 2.

## Limitations and CoolSolve gaps

The four points are at the same diameter, speed and supply state, so the fit
does not separate a speed or a diameter effect: it is the map at that
condition. The cubics pass through the four points exactly; they are not a
least-squares fit of a larger catalogue.

The original `$Export` of the coefficients to `results_RZR315.txt` is not in
this file. CoolSolve will not implement that directive, and the text file is
not an input of the identification.

## Related models

- `CSL-0071` *centrifugal_fan_reference_model*: the RefSim sibling. It takes
  the `alpha_i` and `beta_i` as data (the values above, rounded) and solves
  one operating point.

# Steam turbine with heat loss (example 5.10)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0224`

1.5 kg/s of steam enters a turbine that gives up 8.5 kW of heat. Pressure,
temperature or quality, velocity and elevation are known at the inlet and at
the outlet. The first law for a steady open system gives the power. Teaching
example 5.10, ULiège THD, 2017-2018.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Water |
| **Size** | 27 equations (largest block: 1) |
| **Source** | thermo_models, ULiège THD, 2017-2018, file `R2_E5_borguet.EES` |
| **Authors** | TBD (ULiège THD) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

Example 5.10. The mass flow at the inlet of a steam turbine is 1.5 kg/s and
the heat given up by the turbine is 8.5 kW. The following data are known for
the steam at the inlet and at the outlet of the turbine. Calculate the power
delivered by the turbine.

| | Inlet | Outlet |
|---|---:|---:|
| Pressure | 2000 kPa | 0.1×10³ kPa (100 kPa) |
| Temperature or quality | 350 °C | quality 1 |
| Velocity | 50 m/s | 200 m/s |
| Elevation | 6 m | 3 m |

The heat transfer rate is written negative because the turbine loses that
heat. The gravitational acceleration in the file is 9.8066 m/s². The source
is a teaching example, not an exam.

## Model

One mass flow is used. The original comment states mass conservation as
equality of the outlet and inlet mass flows. The fluid is Water. The inlet
state is fixed by pressure and temperature. The outlet state is fixed by
pressure and quality. The specific enthalpy change is the difference of those
two enthalpies. Specific kinetic and potential energy are kept. The steady-flow
energy balance, cited in the source as equation 25, slide 35, chapter 4, with
one inlet and one outlet, is

\[
\dot Q + \dot W = \dot m\,(\Delta h + \Delta e_c + \Delta e_p)
\]

with

\[
\Delta e_c = \tfrac12(c_\mathrm{out}^2 - c_\mathrm{in}^2), \qquad
\Delta e_p = g(z_\mathrm{out} - z_\mathrm{in}).
\]

In the original unit system those two changes were divided by 1000 so that
they were in kJ/kg. In this file they are in J/kg, like the enthalpies, and
\(\dot Q\) and \(\dot W\) are in W.

The two percentages are the kinetic and potential changes divided by the
enthalpy change. The original comment says the potential-energy change is
negligible beside the enthalpy change, and that the kinetic-energy change is
about 4 % of the enthalpy change, mainly because the exit velocity is fairly
high.

| Input | Value |
|---|---|
| `q_m` | 1.5 kg/s |
| `Q_dot` | −8500 W (−8.5 kW in the original) |
| `p_in` | 2 MPa (2000 kPa in the original) |
| `T_in` | 350 °C |
| `c_in` | 50 m/s |
| `z_in` | 6 m |
| `p_out` | 0.1 MPa (0.1×10³ kPa in the original) |
| `x_out` | 1 |
| `c_out` | 200 m/s |
| `z_out` | 3 m |
| `g` | 9.8066 m/s² |

Those eleven assignments are already equations in the EES equation window.
Together with the eight relations for the enthalpy change, the two mechanical
changes, the power, and the two percentages, the window is 19 equations and
19 variables. CoolSolve reports `System square: Yes` on that window. The
stored values of the unknowns are guesses in `.initials`, not equations. No
Diagram-window input was restored.

The eight equations `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 inlet, i = 2
outlet) are post-processing for the CoolSolve diagram. The window already
computes both states. `s[1]` is `entropy(Water, T=T_in, p=p_in)`. `T[2]` and
`s[2]` are `temperature` and `entropy` of Water at `x_out` and `p_out`. They
do not change the nineteen physical results.

## How to run

```bash
coolsolve ./steam_turbine_heat_loss.eescode
```

Every block is explicit. CoolSolve reports 2 iterations with the shipped
`.initials` and 14 iterations without them. The `.initials` file is the EES
stored solution with pressures, powers and specific energies converted to Pa,
W and J.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `Q_dot` | −8500 W | −8500 W |
| `h_in` | 3137652.618 J/kg | 3136558.307 J/kg |
| `h_out` | 2674947.677 J/kg | 2675101.661 J/kg |
| `Deltah` | −462704.941 J/kg | −461456.646 J/kg |
| `DeltaEC` | 18750 J/kg | 18750 J/kg |
| `DeltaEP` | −29.4198 J/kg | −29.4198 J/kg |
| `W_dot` | −657476.541 W | −655604.098 W |
| `pctEC` | −4.05226 % | −4.06322 % |
| `pctEP` | 0.00635822 % | 0.00637542 % |

`W_dot` is the unknown of the first-law equation, and the stored value is
negative. `T[2]` is 99.6059 °C. EES stored no exit temperature and no
entropy. Because `x_out` is 1, that temperature is the saturation temperature
at the exit pressure. `W_dot`, `h_in` and `h_out` are given here at more
digits than `compare_solution.py` prints; the tool prints `W_dot` as −657477 W
against −655604 W.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R2_E5_borguet.EES` (EES X8.423, 19 stored variables):

> 19 common variables, 4 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8

The preamble of that run is:

> Converted EES reference values: Q_dot (kW x1000), p_in (kPa x1000), p_out (kPa x1000), W_dot (kW x1000), Deltah (kJ x1000), DeltaEC (kJ x1000), DeltaEP (kJ x1000), h_out (kJ x1000), h_in (kJ x1000)

The maximum relative difference over all common variables is **2.85e-03**
(`W_dot`), the value `compare_solution.py` prints. The exact ratio is
2.847923747×10⁻³.

`h_in` and `h_out` stay inside rtol = 0.001. Their residuals are a property
difference of Water, not a missed unit conversion: `DeltaEC` and `DeltaEP`
match the stored solution exactly, and the two enthalpy residuals are not
equal, so they are not one reference-state offset.

| Variable | EES | CoolSolve | CoolSolve − EES | rel. diff |
|---|---:|---:|---:|---:|
| `W_dot` | −655604.0981 | −657476.5412 | −1872.443 | 2.85e-03 |
| `Deltah` | −461456.6456 | −462704.9410 | −1248.295 | 2.70e-03 |
| `pctEC` | −4.063220278 | −4.052258435 | +0.010962 | 2.70e-03 |
| `pctEP` | 0.006375420157 | 0.006358220411 | −1.720e-05 | 2.70e-03 |
| `h_in` | 3136558.307 | 3137652.618 | +1094.311 | 3.49e-04 |
| `h_out` | 2675101.661 | 2674947.677 | −153.984 | 5.76e-05 |

The `Deltah` residual is the exit residual minus the inlet residual. `pctEC`
and `pctEP` carry the same relative difference because `DeltaEC` and
`DeltaEP` agree exactly and the percentages divide by `Deltah`. The power
residual equals the mass flow times the `Deltah` residual:
1.5 × (−1248.295 J/kg) = −1872.443 W. All 27 equations are satisfied (maximum
residual 0), so the power is reported against the stored value separately
from the absolute enthalpies. The heat loss and the mass flow were left as
written.

The other common variables are exact (`--all`): `q_m`, `Q_dot`, `p_in`,
`T_in`, `c_in`, `z_in`, `p_out`, `x_out`, `c_out`, `z_out`, `g`, `DeltaEC`,
`DeltaEP`.

The eight names only in the CoolSolve solution are the diagram arrays. A
solve of the equation window alone and a solve of this file give the same
nineteen original variables (relative difference 0).

## Source and attribution

The equation window names no author. The file name contains `borguet`; that
is not a full name written in the window. The `{$ID$}` tag is the laboratory
licence of the Laboratoire de Thermodynamique, University of Liège, not an
author. Authors are recorded as TBD (ULiège THD). Teaching example 5.10,
course folder THD, 2017-2018. Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R02/R2_E5_borguet.EES`
(EES X8.423, inventory row TM-0363). The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X8.423, unit
  system `SI MASS DEG KPA C KJ`, decimal commas already converted to dots by
  the extractor, 19 variables, no tables, no warnings besides the unit
  system). The functions called are `enthalpy` only. The converted equation
  window, before the diagram block, is square (19 equations, 19 variables,
  `System square: Yes`), so no Diagram-window input was restored and no
  stored unknown was turned into an equation. `$UnitSystem` was deleted.
  The file contains no `$TABSTOPS` and no `$Export`.
- **2026-10-15 — units**: pressures ×1000 (`p_in` 2000 kPa → `2000e3` Pa,
  `p_out` `0.1e3` kPa → `0.1e6` Pa), `Q_dot` −8.5 kW → −8500 W. Specific
  energies are in J/kg and the power in W, so the original `/1000` on
  `DeltaEC` and `DeltaEP` (the factor that produced kJ/kg from J/kg) was
  removed. `T_in` stays 350 °C. Percentages, mass flow, velocities,
  elevations, `g` and `x_out` are unchanged. The `.initials` file is the
  stored solution with the same factors. `DeltaEC` = 18750 J/kg and
  `DeltaEP` = −29.4198 J/kg match the scaled stored values exactly.
- **2026-10-15 — names**: the fluid `water` was written `Water`. The property
  calls wrote `P_in` and `P_out`; they were aligned to `p_in` and `p_out`,
  the spelling of the assignments. EES names are case-insensitive. Comments
  were translated to English. Each dimensional quantity has its SI unit.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1 (inlet) and i = 2 (outlet) only. A solve without that block and a
  solve of this file give the same nineteen original variables (relative
  difference 0).
- **2026-10-15 — sibling**: inventory row TM-0412 is the other file of
  duplicate group DG-0083. It was not imported and was not edited.
- **Level**: equations 27 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges with and
  without guesses, no `coolsolve.conf` → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The balance is the one written in the source: one inlet, one outlet, with
heat transfer and with kinetic and potential energy. No CoolSolve gap blocks
the file. The solver prints a hint that the inlet temperature 350 °C is
Celsius and not 350 K. The value used is still 350 °C, and `T_in` matches
the stored solution.

## Related models

None.

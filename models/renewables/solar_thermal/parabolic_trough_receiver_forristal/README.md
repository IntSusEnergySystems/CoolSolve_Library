# Parabolic-trough receiver (HCE): steady 1D radial energy balance, Forristal/NREL model

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0082`

First-principles model of the heat collector element (HCE) of a parabolic-trough solar collector: a 1D radial energy balance from the heat-transfer fluid, through the absorber tube wall, across the evacuated annulus and the glass envelope, to the wind and the sky. It is a translation of the `SolAbsForristal` model of the ThermoCycle Modelica library (the model of R. Forristall, NREL). The equations contain no property call, so the model is a pure heat-transfer model: it needs only the geometry of the receiver, its optical properties, the ambient conditions and the fluid temperature. Useful to size the heat loss of a receiver, to compare receiver designs (vacuum vs air-filled annulus, coating emissivity, wind) and as the reference model against which empirical receiver loss correlations are calibrated.

| | |
|---|---|
| **Category** | Renewables › Solar thermal |
| **Fluids** | none (the heat-transfer fluid enters through the wall temperature `T_int_t`; the annulus gas is air, taken as a constant set of properties) |
| **Size** | 85 equations (largest block: 20) |
| **Source** | ThermoCycle Modelica library, `ThermoCycle/Components/HeatFlow/Walls/SolarAbsorber/SolAbsForristal.mo` (parameters of `SolarField_Forristal.mo`), commit `b4f16c0b`, MIT — <https://github.com/thermocycle/Thermocycle-library> |
| **Authors** | Adriano Desideri and Sylvain Quoilin (ULiège Thermodynamics Laboratory); scientific model by R. Forristall (NREL/TP-550-34169, October 2003) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@536d427 — verified against an independent Python re-evaluation of the same equations (max. 2.35e-09) |

## Problem statement

Size and evaluate the heat losses of a parabolic-trough heat collector element. The absorber tube of a parabolic trough is a small (70–120 mm diameter), long, highly insulated receiver: the coating has a low emissivity, the space between the tube and the glass envelope is evacuated, and the glass envelope itself is at a much lower temperature than the tube. A first-principles radial balance is therefore needed to predict where the heat goes, and it is the model Forristall implemented in EES for NREL (the original report's title says so) and validated there against SEGS LS-2 data.

The model solves, for one cell of the receiver (one tube length at a given fluid temperature), the steady radial energy balance of:

- the **metal tube**: solar absorption on the coating, conduction through the two half-thicknesses of the wall, heat delivered to the fluid on the internal surface;
- the **evacuated annulus**: free-molecular (residual gas) conduction and radiation between the tube and the glass envelope;
- the **glass envelope**: solar absorption, conduction through the two half-thicknesses of the wall, and the losses to the environment — forced convection to the wind (Hilpert correlation on the glass diameter) and radiation to the sky (sky temperature = ambient − 8 K);
- the **optical chain** of the collector: six loss factors, the mirror reflectivity and the cosine incidence-angle modifier, giving the flux absorbed by the coating and by the glass.

## Model

Assumptions (as in the original): temperatures, heat fluxes and properties are uniform around the circumference of the HCE; solar absorption is linear; the annulus contains a residual gas at a constant pressure.

Governing equations (per unit of tube length, `N = 1` cell, `Nt = 1` tube; fluxes in W/m² referred to the external surface of the tube or of the glass):

| Step | Equation |
|---|---|
| Optical efficiency | `eta_opt = eps1·eps2·eps3·eps4·eps5·eps6·rho_cl·cos(Theta)`, `eta_opt_t = eta_opt·Alpha_t·Tau_g`, `eta_opt_g = eta_opt·Alpha_g` |
| Absorbed power | `Q_tube_tot = DNI·eta_opt_t·A_ref`, `Phi_tube_tot = Q_tube_tot/A_ext_t` (same for the glass, referred to `A_ext_g`) |
| Sky radiation | `T_sky = T_amb − 8 K` (assumption of the original) |
| Wind convection | `Re = v_wind·rho_air·Dext_g/mu_air`, `Nu = C·Re^m·Pr^n`, `Gamma_air = k_air·Nu/Dext_g`, with `C, m` from the four Reynolds-number regimes of Forristal and `n = 0.37` for `Pr < 10` |
| Annulus gas | `LAMBDA = 2.33E-20·T_g_t/(P_mmHg·DELTA²)` (mean free path, `DELTA` in cm), `Gamma_vacuum = k_st/((Dext_t/2)·ln(rint_g/rext_t) + BB·LAMBDA·(rext_t/rint_t+1))` |
| Radiation in the vacuum | `Phi_rad_gas = Sigma·(T_ext_t⁴ − T_int_g⁴)/(1/Eps_t + (Dext_t/Dext_g)·(1/Eps_g − 1))`, `Eps_t = 0.062 + 2E-7·T_ext_t²` |
| Wall conduction | cylindrical half-thickness resistances, e.g. `Phi_tube_int = lambda_t/(rint_t·ln((rint_t+rext_t)/(2·rint_t)))·(T_int_t − T_t)` |
| Energy balances | glass: `rint_g·Phi_glass_int + rext_g·Phi_glass_ext = 0`; tube: `rint_t·Phi_tube_int + rext_t·Phi_tube_ext = 0` (steady state: no accumulation in the thermal masses of the original) |
| Results | `Q_abs` (power to the fluid), `eta_th`, `eta_TOT`, `Phi_loss` (loss per reflector area), `err_bal` (energy-balance closure) |

The regime switch of `C` and `m` is written with the three-argument EES `IF` function (`C = if(Re-40, if(Re-1000, if(Re-200000, 0.076, 0.26), 0.51), 0.75)`), which is valid EES (`docs/ees_vs_coolsolve.csv` line 34) and is used by other library models (`CSL-0042`).

**Inputs**: `DNI` (W/m²), `Theta_inc` (deg), `v_wind` (m/s), `T_amb` (°C), `T_int_t` (°C, the fluid temperature on the internal surface of the tube), plus the geometry (`L`, `A_P`, `Nt`, `Dext_g`, `th_g`, `Dext_t`, `th_t`), the properties (`lambda_g`, `lambda_t`, `k_air`, `rho_air`, `mu_air`, `Pr`, `Pvacuum`, `DELTA`, `BB`, `k_st`, `Sigma`) and the optical parameters (`eps1…eps6`, `rho_cl`, `Tau_g`, `Alpha_g`, `Alpha_t`, `Eps_g`), which are left as inputs as in the original and set here to the values of `SolarField_Forristal.mo` and `SolAbsForristal.mo` (the geometry and the HCE optics of a Schott PTR70-type receiver).

**Outputs**: `eta_th`, `eta_TOT`, `Phi_loss` (W/m² of reflector), `Q_abs` (W), `T_ext_g`, `T_g`, `T_int_g`, `T_t`, `T_ext_t` (°C), and the diagnostic `err_bal` (W).

## How to run

```bash
coolsolve models/renewables/solar_thermal/parabolic_trough_receiver_forristal/parabolic_trough_receiver_forristal.eescode
```

The **`.initials` file is needed**: the 20-variable algebraic loop (the tube temperature, the glass temperatures and the radiation fluxes are mutually dependent) does not converge from the default guesses — CoolSolve then reports `SingularJacobian` — but converges in 5 Newton iterations from the values of the file (they are the solution, used as a starting point, and can be refreshed with `coolsolve -g`). Changing `T_int_t`, `v_wind`, `DNI` or the geometry may require a new starting point (`coolsolve -g` after a successful run).

The receiver is modelled at one tube temperature (one cell). To model a collector, call the model at several fluid temperatures along the tube (a `DUPLICATE` chain) and integrate the fluid along the tube — that is the translation of the `SolarField_Forristal` parent model of the source, out of scope here.

## Results

Operating point of the baseline `.sol`: DNI = 900 W/m², incidence angle 5°, wind 5 m/s, ambient 20 °C, fluid 200 °C, PTR70-type receiver (`Dext_g` = 120 mm, `th_g` = 2.5 mm, `Dext_t` = 70 mm, `th_t` = 2 mm, `Pvacuum` = 0.0133 Pa = 10⁻⁷ mmHg), `L` = 8 m, aperture 5 m.

| Variable | Value |
|---|---|
| Optical efficiency `eta_opt` | 0.8025 (0.8054 at normal incidence) |
| Total absorbed power `Q_tube_tot + Q_glass_tot` | 27.0 kW + 0.58 kW |
| Power delivered to the fluid `Q_abs` | 26.69 kW |
| Thermal efficiency `eta_th` | 0.9892 |
| Total efficiency `eta_TOT` | 0.7415 |
| Heat loss per reflector area `Phi_loss` | 26.4 W/m² (0.96 % of the absorbed) |
| Heat transfer coefficient of the residual gas `Gamma_vacuum` | 1.09E-04 W/m²·K |
| Mean free path `LAMBDA` | 72.6 m |
| Coating emissivity `Eps_t` | 0.0700 at 200.6 °C |
| External coefficient `Gamma_air` | 27.8 W/m²·K (Nu = 130 at Re = 3.88E+04) |
| Tube outer surface `T_ext_t` / tube middle `T_t` | 200.6 °C / 200.3 °C |
| Glass inner / middle / outer `T_int_g`, `T_g`, `T_ext_g` | 29.8 / 29.6 / 29.4 °C |
| Energy-balance closure `err_bal` | −187 W (−0.68 % of the absorbed power) |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): a parametric sweep, e.g. heat loss per
     metre of receiver vs fluid temperature at 1, 5 and 10 m/s wind speed, exported as
     figures/<name>_hl_t.png -->

## Verification

The source stores **no reference result** (no test assertions, no data file), so the model is verified in three independent ways.

**1. Independent re-evaluation of the equations (translation check).** The equations were re-implemented from the Modelica source in Python (NumPy/SciPy, `scipy.optimize.fsolve`, throw-away script in the conversion work folder, deleted afterwards) and evaluated at the operating point of the baseline. `tools/compare_solution.py`:

```
27 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 59
```

maximum relative difference **2.35e-09** (`err_bal`), i.e. every temperature, flux, coefficient and efficiency agrees with the independent implementation to machine precision. One variable deserves a comment: `T_g` (the temperature in the middle of the glass envelope) is the only one for which the source is self-inconsistent — its two definitions of `Phi_glass_ext` (the net absorbed flux at the external surface, and the conduction through the external half-thickness) carry opposite sign conventions, so the source does not determine `T_g` unambiguously (the two conventions differ by 0.4 K). CoolSolve returns the physically ordered solution `T_int_g > T_g > T_ext_g` (29.78 > 29.59 > 29.40 °C), and the reference re-evaluated in that (sign-consistent) form agrees to 8.8e-12 on `T_int_g`; the comparison above is made with that form. All the physical outputs (`eta_th`, `eta_TOT`, `Phi_loss`, `Q_abs`, `T_ext_g`) differ by less than 5E-04 between the two conventions.

**2. Physics cross-check against the NREL PTR70 heat-loss test** (F. Burkholder and C. Kutscher, *Heat Loss Testing of Schott's 2008 PTR70 Parabolic Trough Receiver*, NREL/TP-550-45633, May 2009). The default geometry, coating emissivity and optics of the model are those of the PTR70 receiver, so the measured values of that report apply directly. Test-stand wind speed is not published, so it was inferred from the measured glass surface temperature:

| Test | absorber [°C] | glass [°C] measured / model | heat loss [W/m] measured / model |
|---|---|---|---|
| 1 (Table 3) | 100 | 26 / 27.0 | 15 / 87 |
| 3 (Table 3) | 213 | 35 / 35.0 | 43 / 140 |
| #2 test 8 (Table 4) | 451 | 80.1 / 80.1 | 333.8 ± 10 / 616 |

The **glass surface temperature is reproduced within 1 K** at an inferred wind speed of 3–3.4 m/s (the tube-to-glass radiation path, the coating emissivity and the sky model are therefore right). The **heat loss is over-predicted by a factor 1.9 to 5.8**: the model's loss is nearly independent of the wind speed (136 W/m at 0.1 m/s vs 141 W/m at 10 m/s at the operating point of test 3, because the external coefficient and the glass temperature adjust), so the discrepancy cannot be attributed to the assumed wind; it is a difference between this first-principles model and the boundary conditions of the test stand. The same report's published behaviour is itself consistent with a low effective loss: the radiation-only loss at the measured glass temperature is 40 W/m at test 3 (measured: 43 W/m), while the empirical correlation of the same report (the Schott 2008 PTR70 coefficients `A0…A6`, used by the ThermoCycle model `AbsSchottSopo.mo`) gives 44 W/m there — both about three times below this model. The NREL field measurements of the same test programme (400 W/m at 400 °C, poster NREL/OSTI 910508) are of the order of this model instead. Conclusion: the translation is verified, the *model* disagrees with the stand data, and users needing measured-data predictions should use the empirical correlations.

**3. Energy-balance closure.** `err_bal = Q_glass_tot + Q_tube_tot − Q_abs − Q_loss = −187 W`, i.e. 0.68 % of the absorbed power. The residual is structural, not numerical: the source identifies the annulus flux `Phi_glass_int` (computed on the tube surface, with the view-factor ratio `Dext_t/Dext_g`) with the flux on the *inner glass surface*, whose area differs (`A_ext_t/A_int_g = 0.61`); the equations are kept as in the source and the residual is quantified by `err_bal` (added here, not in the original). The same residual appears in the independent Python implementation (−187.7 W).

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented) of the model `SolAbsForristal` ("1D radial energy balance around the Heat Transfer Element based on the Forristal model") from the ThermoCycle Modelica library, file `ThermoCycle/Components/HeatFlow/Walls/SolarAbsorber/SolAbsForristal.mo`, with the parameter values of `ThermoCycle/Components/Units/Solar/SolarField_Forristal.mo`, local clone `~/git/Thermocycle-library`, commit `b4f16c0b`.
ThermoCycle — https://github.com/thermocycle/Thermocycle-library
Copyright (c) 2018 Thermodynamics Laboratory (University of Liège), MIT License.
Original authors of the model: S. Quoilin and A. Desideri (see the git history of the files and the package headers; the ThermoCycle maintainers are B. Dechesne, J. Vega, S. Quoilin and J. Wronski). The scientific model is that of **R. Forristall, "Heat Transfer Analysis and Modeling of a Parabolic Trough Solar Receiver Implemented in Engineering Equation Solver", NREL/TP-550-34169, October 2003** (the original model cites it and notes that it was validated against Sandia SEGS LS-2 data); the published coefficients are taken from that report (pp. 18 and following: `Eps_t`, `Eps_g`, `Alpha_g`, the Reynolds regimes of the external convection). The reference data used for the verification are from **F. Burkholder and C. Kutscher, "Heat Loss Testing of Schott's 2008 PTR70 Parabolic Trough Receiver", NREL/TP-550-45633, May 2009**.

## Conversion log

- **2026-10-06 — translation (T-TRANSLATE)**: Modelica → CoolSolve. `der()` terms dropped: a thermal mass in a steady model means `der = 0`, so the two energy balances (glass, tube) are written with zero accumulation and the densities and heat capacities of the glass and of the tube (`rho_g`, `Cp_g`, `rho_t`, `Cp_t`) disappear with them. One cell (`N = 1`) instead of the `N`-cell chain of the original: `Phi_glass_tot_N` and `Phi_tube_tot_N` become `Phi_glass_tot` and `Phi_tube_tot`; the averages `Eta_th`/`Eta_TOT` and the `1/N` of `Phi_loss` are gone. Parameters without default in the original (`eps1…eps6`, `rho_cl`, `Pr`, `Pvacuum`, `L`, `A_P`, `rho_*`, `Cp_*`, `lambda_*`, `Patm`) are given the values of the parent `SolarField_Forristal.mo`; `Patm` is not used by any equation and is not translated.
- **2026-10-06 — corrections of source defects** (each with its impact):
  - `Eps_t[N]` instead of `Eps_t[i]` in the radiation term across the vacuum (flagged in `sources/thermocycle/README.md` §8): with `N = 1` the two are the same element, so the translation writes `Eps_t`; no numerical change here, but the source is wrong for `N > 1`.
  - **Sign of the useful heat**: the original computes `Q_abs = Phi_tube_int·2·rint_t·pi·L`, which is *negative* for a receiver that works, because `Phi_tube_int` is positive when the fluid is colder than the tube (`T_int_t − T_t < 0`); the thermal efficiency would come out negative (−0.989 instead of 0.989). The translation writes `Q_abs = -Phi_tube_int·2·rint_t·pi·L·Nt`. Impact: the sign of `eta_th` and `eta_TOT` only.
  - **Reynolds regimes**: the chain of strict inequalities of the original falls through to the last branch (`C = 0.076`, `m = 0.7`) at exactly `Re = 40` and `Re = 1000`. The translation uses half-open ranges (`Re ≤ 40`, `Re ≤ 1000`, `Re ≤ 200000`). Impact: two isolated Reynolds numbers, no physical consequence (the coefficients of two neighbouring regimes differ by < 40 %).
  - **Units**: the original works in K, EES in °C. `Eps_t = 0.062 + 2E-7·(T_ext_t − 273.15)²` becomes `Eps_t = 0.062 + 2E-7·T_ext_t²`; the T⁴ and mean-free-path terms use explicit absolute temperatures `T_…_K` (7 equations added, so that no term mixes °C and K); the incidence angle, in rad in the original, is in deg because CoolSolve's trigonometry is in deg (`Theta_inc = 5` deg = 0.0873 rad in the original).
  - **`DELTA`** (molecular diameter of the annulus gas) is annotated `[cm]` in the original, where it is a bare number: the mean-free-path correlation is written with that unit. The literal is therefore kept dimensionless and the unit stated in its comment; writing `DELTA = 3.53E-08 [cm]` would silently change the value by 10⁶ and the mean free path by 10¹².
  - **Removed as dead code**: `pi` (predefined in CoolSolve and in EES), `GAMMA`, `gg`, `Am_g`, `Am_t`, `Patm`, `T_g_start_*`, `T_t_start_*`, the commented-out `PTR`/`UVAC` alternatives, the `IF Q_tube_tot > 0 THEN … ELSE …` branch on `eta_th` (kept as `if(Q_tube_tot, …, …)`, the EES inline conditional), and the `wall_int` thermal port (the fluid enters through `T_int_t`).
  - **Added here** (not in the original): `Q_loss` and `err_bal`, the energy-balance closure diagnostic quoted above, and the `Eps_g` assignment, moved up with the other optical parameters.
- **2026-10-06 — arithmetic check of the source**: the comment of `SolarField_Forristal.mo` states that its optical parameter values give `eta_opt = 0.7263`; their product is `0.9754·0.994·0.98·0.962566845·0.981283422·0.96·0.935 = 0.8054` at normal incidence (0.8025 at 5°). The parameters are kept as they are and the comment is not reproduced.
- **2026-10-06 — level**: taxonomy §3 — criterion "number of coupled subsystems": one (the receiver), 1/3; "property calls / external tools": none, 0/3; "non-linear couplings needing an iterative scheme": the 20-variable algebraic loop of the radiation balance, 2/3; "arrays / discretisation": none, 0/2; "optimisation": none, 0/2. Total 3/13 → **level 2** (the level-3 threshold is 5).

## Limitations and CoolSolve gaps

- The **`.initials` file is part of the model**: the algebraic loop does not converge from the default guesses (see *How to run*). Not a gap, but a constraint on the user.
- No registered CoolSolve gap blocks this model (`missing_features` is empty). One **observation**, not registered as a gap: a computed variable value below about 1E-16 is stored as 0 (`2.33E-20` written as a statement gives 0). The model is not affected — its mean free path is the *result* of the expression (72.6 m) — but a constant of that magnitude written as a statement would be lost.
- Physical limitations: 1D radial (no longitudinal conduction along the tube, no end losses), constant air properties and constant residual-gas pressure, four wind regimes with a step at `Re = 40`, 1000 and 200000, no natural-convection/forced-convection blending, no wind shield, no coating degradation, no direct solar reflection on the glass.

## Related models

- `CSL-0119` *solar_geometry_sun_path*: solar geometry (declination, hour
  angle, sun position) of the same sub-category; provides the sun-position
  inputs such collector models need.
- None yet otherwise. The complementary empirical receiver loss correlations of the same ThermoCycle family (Schott PTR70, Sopogy, Soltigua; inventory row `THC-002`) are not in the library; the comparison between them and this first-principles model is discussed in *Verification*.
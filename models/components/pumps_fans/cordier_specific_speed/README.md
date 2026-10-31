# Cordier specific-speed line and 0D efficiency pre-design of turbomachines

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0318`

Translation of the 0D turbomachinery pre-design of LaboThapPy: from the speed, the inlet volume flow
and the specific work of a pump, compressor or turbine, the **specific speed** `omega_s`, the
**specific diameter** read on the tabulated **Cordier line**, the **rotor diameter** and the
**machine-type zone** (radial-vane, Francis-vane, mixed-flow, axial); plus a **bilinear pump-efficiency
estimate** on a (volume flow, specific speed) chart, with the optional band limits of the chart. The
demonstration program re-runs the sizing cases of the three LaboThapPy scripts (cyclopentane ORC pumps and
compressor, CO2 pump, compressor and turbine) and the main example of the radial-pump design class.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | Cyclopentane, R744 (the demonstration program only; the functions take numbers) |
| **Size** | 234 equations in the demonstration program (largest block 5) + 4 `FUNCTION` + 1 `PROCEDURE` |
| **Source** | [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy) commit `f03f7f47` (permanent link in `model.json`), files `labothappy/correlations/turbomachinery/correlations_0D.py`, `labothappy/sizing/turbomachinery/{pump,turbine,compressor}/sizing_0D/*_0D_design.py`, `labothappy/sizing/turbomachinery/pump/radial/radial_pump_0D_design.py`; inventory rows `LTP-053` (kept) and `LTP-065` (duplicate of `LTP-053`) |
| **Authors** | Basile Chaudoir (the only author of the five files in the repository history) |
| **License** | Original: Apache-2.0 (`LICENSE.txt` of LaboThapPy); translation published under the library MIT licence |
| **CoolSolve** | 0.4.0 — **verified** against a re-run of the Python code (112 values, max deviation 4.3·10⁻⁹) |

## Niche

Nothing in the library computes a **specific speed** or uses a **Cordier-type diagram**: a search of
`library.json` and of every model folder for *Cordier*, *specific speed*, *omega_s*, *Balje* finds no
turbomachine model (the only hits are variables named `omega_s...` for humidity ratio or effectiveness in an
HVAC and a heat-exchanger model). The nearest models are
`CSL-0069` *centrifugal_compressor_design_similarity* and `CSL-0235` *turbomachine_optimal_diameter*
(diameter and speed from a *given* flow factor and enthalpy factor of the best-efficiency point: the
Cordier line here *supplies* that diameter from `omega_s` instead), `CSL-0125` *pump_curve_similarity*,
`CSL-0183`/`CSL-0203` (pump characteristics from dimensionless polynomials fitted to catalogue
points: an off-design model of a *selected* pump) and `CSL-0207` *turboexpander_parameter_identification*.
This model is the **pre-design step before them**: from the duty only (no catalogue point, no
curve), size the machine type, diameter and efficiency.

## Problem statement

Research/component function library. In the original, `pump_0D_design`, `compressor_0D_design` and
`turbine_0D_design` return `(Omega_s, D_s, D, geom)` for a given rotation speed `Omega`, volume flow
`Q` and thermodynamic states; `RadialPumpODDesign` additionally estimates the isentropic efficiency of
`n_parallel` identical pumps with `pump_efficiency_0D_estimation`.

## Model

All quantities are SI (`Omega` in rad/s, `Q` in m³/s, specific work `gH` in J/kg; the original uses
the head `DH` in m and `g = 9.81 m/s²`, here `gH = g·DH`).

| Block | Equation |
|---|---|
| `Head_pump(P_1, P_2, rho_1, z_1, z_2, v_1, v_2)` | $gH = \dfrac{P_2-P_1}{\rho_1} + g\,(z_2-z_1) + \dfrac{v_2^2-v_1^2}{2}$ (pump and compressor scripts: inlet density, incompressible) |
| turbine | $gH = h_1 - h_2$ (turbine script) |
| `Cordier_design` | $\omega_s = \dfrac{\Omega\sqrt{Q}}{(gH)^{3/4}}$, $D = D_s\,\dfrac{\sqrt{Q}}{(gH)^{1/4}}$, $\omega_{s,imp} = 2733\,\omega_s$ |
| zone | $\omega_{s,imp}<1500$ radial-vane (1), $<4000$ Francis-vane (2), $<7500$ mixed-flow (3), else axial (4); the strings of the original are in the table `zones` |
| `Cordier_Ds(omega_s)` | piecewise-linear interpolation of the 19 points of the table `cordier` (`omega_s` 0.3 ... 30, `D_s` 9.66 ... 0.48), **end segments extended linearly** |
| `Cordier_Ds_clamped(omega_s)` | same line, **end values kept** beyond the table |
| `Pump_eta_0D(omega_s, Q_h, enforce_limits, allow_extrap)` | bilinear interpolation in the table `eta_pump` (8 flows 18 ... 18000 m³/h × 17 values of `omega_s` = 10, 15, ... 90), efficiency in %; `enforce_limits = 1` returns -1 outside the band of the table `eta_limits`; `allow_extrap = 0` returns -1 outside the grid |

The constant 2733 is the factor from the SI specific speed to the US customary one (rpm, gpm, ft):
a one-liner (`rpm·√gpm·g^0.75/ft^0.75`, with `g` = 9.80665) gives 2733.0, so the thresholds 1500/4000/7500 are on
the US specific speed. The comment of the original does not state the unit of the `omega_s` axis of the
efficiency chart (10 ... 90); the data are used as given.

**Choices and differences between the original scripts** (all checked by running them):

* The Cordier line is evaluated in two ways in LaboThapPy: `np.interp` (end values kept) in
  `correlations_0D.py`, `pump_0D_design.py` and the radial pump class, and `scipy.interpolate.interp1d(...,
  fill_value='extrapolate')` (linear extension) in `turbine_0D_design.py` and `compressor_0D_design.py`. Both are
  kept: the argument `extrap` of `Cordier_design` selects them (pump: 0, turbine and compressor: 1). They differ
  below `omega_s` = 0.3 and above 30: for the turbine case of the demonstration
  (`omega_s` = 0.102) `D_s` = 14.97 and `D` = 1.623 m with the extension, 9.66 and 1.047 m with the end value.
  The comment of `correlations_0D.py` says that `np.interp` does a "linear extrapolation"; it does not
  (`cordier_line()(0.1)` = 9.66, `(50)` = 0.48 when run).
* The `pump_efficiency_0D_estimation` of the original returns NaN where the point is outside the grid or the
  band; EES has no NaN: `Pump_eta_0D` returns **-1**.
* With `allow_extrap = True` the docstring says the values are "snapped to the edge"; the code clamps the
  *cell index* but not the interpolation fractions, i.e. it **extends the edge cell linearly**
  (`pump_efficiency_0D_estimation(55, 30000, enforce_limits=False, allow_extrap=True)` = 95.20 %, above every
  value of the chart, the maximum of which is 93.50 %). The translation reproduces the code, not the docstring.
* The `enforce_limits` default is `True` in `correlations_0D.py` and `False` in the radial pump class; it is
  an argument here.
* Interpolation is coded with `LOOKUP` and a search loop instead of the EES `INTERPOLATE`, because the
  register states that `INTERPOLATE` is cubic in EES (`CS-GAP-INTERP-CUBIC`) whereas the original is
  piecewise linear. EES `Lookup` tables in `FUNCTION`s and `REPEAT/UNTIL` are used as in EES; the tables
  are the companion CSV files `cordier_specific_speed-<table>.csv` (CoolSolve convention); an EES user
  creates the same Lookup tables `cordier`, `eta_pump`, `eta_limits`, `zones` and the two case lists.
* `Omega_s_imp` is only an intermediate in `Cordier_design`; the machine zone is returned as the number 1 ... 4
  (string arrays are not supported, decision D14), the table `zones` holds the names.

## How to run

```bash
coolsolve ./cordier_specific_speed.eescode
```

The default guesses converge (28 iterations, no `.initials`). The case lists of sections 5 and 6 are the
tables `cordier_specific_speed-rp_cases.csv` and `cordier_specific_speed-eta_cases.csv`; to size another
machine, copy one block of the demonstration program and change the inputs.

## Results

Demonstration program (`gH` in J/kg, `Q` in m³/s; every case, inputs and `D_s` as in the original):

| Case (original script) | `Q` | `gH` | `omega_s` | 2733·`omega_s` | `D_s` | `D` [m] | Zone |
|---|---:|---:|---:|---:|---:|---:|---|
| pump Cuerva, cyclopentane, 3000 rpm | 0.0628 | 1736.1 | 0.2927 | 799.9 | 9.66 (end value) | 0.3750 | radial-vane |
| pump Zorlu, cyclopentane, 3000 rpm | 0.0470 | 1173.4 | 0.3398 | 928.8 | 8.593 | 0.3184 | radial-vane |
| pump Torrecid, cyclopentane, 3000 rpm | 0.00487 | 4541.5 | 0.0396 | 108.3 | 9.66 (end value) | 0.0821 | radial-vane |
| pump R744, 3000 / 12000 / 21000 / 30000 rpm | 0.1292 | 10675 | 0.1075 / 0.4302 / 0.7528 / 1.0754 | 293.9 / 1175.6 / 2057.4 / 2939.1 | 9.66 / 6.579 / 3.797 / 2.926 | 0.3416 / 0.2327 / 0.1343 / 0.1035 | radial, radial, Francis, Francis |
| turbine R744 140 bar/121 °C to 40 bar/40 °C, 1500 rpm | 1.963 | 27890 | 0.1020 | 278.7 | 14.97 (extended) | 1.623 | radial-vane |
| compressor cyclopentane, 12000 rpm | 2.945 | 67597 | 0.5144 | 1405.9 | 5.513 | 0.5868 | radial-vane |
| compressor R744, 3000 rpm | 0.9146 | 105183 | 0.0514 | 140.6 | 16.32 (extended) | 0.8667 | radial-vane |

Radial pump example (R744 40 bar/5.15 °C to 160 bar, 500 kg/s, `gH` = 13404.5 J/kg, `rho_1` = 895.2 kg/m³), four
cells of the efficiency matrix of the original:

| `n_parallel`, speed | `Q` per pump [m³/s] | 2733·`omega_s` | `D` [m] | `eta` [%] |
|---|---:|---:|---:|---:|
| 1 pump, 750 rpm | 0.5585 | 128.8 | 0.6709 | -1 (NaN: outside the chart, 10 ... 90) |
| 3 pumps, 750 rpm | 0.1862 | 74.34 | 0.3874 | 87.29 |
| 6 pumps, 750 rpm | 0.0931 | 52.57 | 0.2739 | 89.04 |
| 6 pumps, 1000 rpm | 0.0931 | 70.09 | 0.2739 | 86.61 |

`omega_s` is below 0.3 in all four cells, so the end value `D_s` = 9.66 is used and `D` does not depend on the
speed (rows 3 and 4 have the same `D`). The class of the original, run for its 8 × 4 cells, gives NaN in 21 of 32
cells (the efficiency is defined only for 2733·`omega_s` in 10 ... 90).

The `W_dot_rp` of the demonstration is the `W_dot_pp` of the original, `m_dot·(h_ex − h_is)/n_parallel`
= 3.18·10⁵ W (3 pumps, 750 rpm), which is the *dissipated* part of the pump work; the shaft power
`m_dot·(h_ex − h_1)/n_parallel` is 2.50·10⁶ W for the same cell (`W_dot_shaft_rp`, an addition). In the
original `W_dot_pp` feeds `cost_estimation` as the shaft power in kW (`50000 + 1500·W_dot_pp/1000`):
reading of the code, the cost correlation itself was not translated or checked.

The 13 argument sets of `Pump_eta_0D` (table `eta_cases`) cover the interior, the corners, the band limits and
the extrapolation; for example (55, 500 m³/h) = 89.482 % (the demo values of the original file), (60, 100,
limits on) = -1 (outside the band), (60, 100, limits off) = 83.884 %.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric plot of D_s and of the machine
     zone against omega_s (Cordier line), or of Pump_eta_0D against omega_s for several flows, saved as
     figures/cordier_specific_speed_<type>.png -->

## Verification

LaboThapPy commit `f03f7f47` was re-run in a throw-away virtual environment under `work/`
(`numpy`, `scipy`, `CoolProp 8.0.0`, `requests`, `pandas`; the clone was put on `PYTHONPATH`, not installed;
Python 3.12). One driver script (`make_ref.py`, in `work/cordier/`, deleted with the work folder as the workflow
requires) did the following:

1. executed the function definitions of `pump_0D_design.py`, `turbine_0D_design.py` and
   `compressor_0D_design.py` (the module-level case selector was cut off, `import __init__` stubbed) and called
   them with the case inputs of the scripts, the density and enthalpies from `CoolProp.PropsSI` at the
   given `(P, T)` (the Python `'CO2'` is R744 here, the cyclopentane cases use `'Cyclopentane'`);
2. imported `RadialPumpODDesign` and called its `Omega_system()` on the four cells above (inputs of the class
   main example), reading `Omega_s`, `Omega_s_imp`, `D`, `eta_is`, `W_dot_pp`, `h_ex`;
3. called `pump_efficiency_0D_estimation` on the 13 argument sets of the table `eta_cases` (NaN replaced by -1);
4. wrote everything as `name,value` and compared it with the `.sol` with
   `tools/compare_solution.py cordier_specific_speed.sol python_ref.csv --all`.

Result: **112 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 123** (inputs and
intermediate or unit-converted values). The largest relative deviation is 4.27·10⁻⁹ (`W_dot_rp`,
`W_dot_shaft_rp`, differences of enthalpies); all the others are below 6·10⁻¹³. The reference used CoolProp 8.0.0,
the CoolSolve build CoolProp 8.1.0dev (revision 75af781): the HEOS fluid models agree at round-off. The three data tables were also checked
against the source functions: the 19 points of the Cordier line (`cordier_line()` at its nodes), the 136 values
of the efficiency chart (`pump_efficiency_0D_estimation` at every node with the limits off) and the 8 band limits
(points just inside and outside the band, with the limits on): **0 mismatches**.

No published value is compared: the Cordier line and the efficiency chart are taken from the Python code (the
original does not name the source of its data); this model is a faithful translation of that code, not a
validation of the correlations. The `Omega_s_imp` factor 2733 is the only constant checked against a
hand calculation (above).

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented) of the 0D turbomachinery
correlations and sizing scripts of LaboThapPy, files `labothappy/correlations/turbomachinery/correlations_0D.py`,
`labothappy/sizing/turbomachinery/{pump,turbine,compressor}/sizing_0D/*_0D_design.py` and
`labothappy/sizing/turbomachinery/pump/radial/radial_pump_0D_design.py`, commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy — Copyright (C) 2025 Universite catholique de Louvain
(UCLouvain), Universite de Liege (ULiege), Universite de Mons (UMONS), Apache License 2.0. Original author of the
translated files (repository history): Basile Chaudoir (ULiège); other authors of the library are listed in its
`AUTHORS.txt`. Changes: translated from Python to the CoolSolve language; the NumPy/SciPy interpolation replaced by explicit
piecewise-linear code on Lookup tables; NaN replaced by -1; zone names replaced by a number; example
cases flattened into the main program (CO2 → R744). Scientific basis: the classical Cordier diagram
(O. Cordier, 1955) and the US specific-speed classification; neither paper was consulted, and the source code
does not cite any reference for its numbers.

## Conversion log

- **2026-10-31 — translation (T-FUNC, card C-366)**: five routines + demonstration program; Python temperatures in
  K converted to °C (value − 273.15); `PropsSI` calls replaced by `density`, `enthalpy`, `entropy` of
  Cyclopentane/R744; the `case_study` selectors of the scripts are blocks of the main program; the
  `Torrecid` pump sweep (100 points, all at 3000 rpm in the original) is one point, and the `TCO2` pump
  sweep (28 speeds, 3000 ... 30000 rpm) is reduced to the four speeds 3000, 12000, 21000, 30000 rpm.
- Variable names that differ only in case are one variable in EES (`N_rp`/`n_rp`): the speed arrays are called `rpm_rp`, `rpm_pCO`.
- Functions and procedures take no variables from the main program (no `$COMMON`).
- **Level** (taxonomy §3): equations 234 → 1; largest block 5 → 0; functions/procedures and arrays → 1; no
  multi-zone structure, no calibration or off-design, no curated guesses → 0 + 0 + 0; score 2 → level 2.

## Limitations and CoolSolve gaps

* The Cordier line and the efficiency chart are valid only where the original's data are; the compressor
  and the pump scripts use the *incompressible* pump head `Head_pump` with the inlet density (also for
  the compressor cases, as in the original), not an isentropic head.
* The chart of the efficiency estimate has no stated origin or unit for `omega_s`; the radial pump class of
  the original feeds it with 2733·`omega_s` (verified by running it), so only 11 of its 32 cells have a value.
* Nothing in this model needs a CoolSolve gap: no gap registered or reported (`missing_features` empty).

## Related models

- `CSL-0125` *pump_curve_similarity*: the LaboThapPy off-design pump from catalogue curves; this model is its pre-design counterpart.
- `CSL-0183` *pump_polynomial_identification*, `CSL-0203` *variable_speed_pump_simulation*: dimensionless head and power polynomials of a selected pump.
- `CSL-0069` *centrifugal_compressor_design_similarity*, `CSL-0235` *turbomachine_optimal_diameter*: diameter and speed from given flow and enthalpy factors; the Cordier line supplies such a diameter from `omega_s`.
- `CSL-0207` *turboexpander_parameter_identification*: turbo-expander identification from test data.

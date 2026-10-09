# Parabolic-trough collector with a discretised absorber (Soponova MicroCSP efficiency map)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0129`

Translation of the LaboThapPy component `PTCollector`: the absorber of a
Sopogy SopoNova MicroCSP parabolic-trough collector is split into `n_disc`
elements; each element absorbs the solar power it receives times the collector
efficiency of the manufacturer's 6 × 17 datasheet map, read at the irradiance
and at the temperature of the fluid entering it, and the fluid enthalpy marches
along the absorber at constant pressure. The model gives the absorbed power, the
exhaust state of the heat transfer fluid and the mean efficiency of the
collector field; it is the absorber counterpart of the receiver model
`CSL-0082` and of the loss correlations of `CSL-0083`.

| | |
|---|---|
| **Category** | Renewables › Solar thermal |
| **Fluids** | Water (`fluid$` can be any CoolProp fluid) |
| **Size** | 140 equations (largest block: 1) |
| **Source** | LaboThapPy, `labothappy/component/solar/parabolic_trough_collector.py` (+ geometry and example), commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Elise Neven (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7addbbc — verified against the example of the source (absorbed power, exhaust state, 20 element states) |

## Problem statement

A parabolic trough concentrates the direct solar beam onto a receiver tube
running along its focal line. The heat transfer fluid enters the absorber,
picks up the solar power that the absorber transmits to it (what is left after
the optical and the thermal losses of the collector) and leaves it warmer.

The absorbed power depends on the temperature of the fluid (the collector
efficiency decreases when the absorber gets hot), so the absorber is discretised
along its length: the efficiency of each element is evaluated with the
temperature of the fluid at the inlet of that element, and the enthalpy of the
fluid is marched from element to element. The convergence of the result with
respect to the number of elements is the study the example of the source runs
(1 to 50 elements).

## Model

Collector: Sopogy SopoNova MicroCSP, one collector module of the geometry
record of the source (`PT_Collector_Geom.set_parameters("Soponova_MicroCSP")`):

| Parameter | Value | Meaning |
|---|---|---|
| `L` | 3.657 m | length of one collector module |
| `W` | 1.524 m | aperture width |
| `A`, `A_r` | 5.574 / 5.07 m² | aperture / reflective area |
| `alpha_r`, `refl_m`, `envel_tau`, `eta_other` | 0.92 / 0.91 / 0.95 / 0.89 | receiver absorptivity, mirror reflectivity, envelope transmittance, other optical efficiency |

The example puts **10 collector modules in series**, so the model uses
`L_coll = 36.57 m` and `W = 1.524 m`.

Equations, with `i = 1 … n_disc` the elements and `h[i]` the specific enthalpy
at the inlet of element `i` (`h[1]` at the suction side, `h[n_disc+1]` at the
exhaust side), as in the `solve()` method of the source:

```
DT[i]             = T[i] - T_amb                                       [degC]
eta_coll[i]       = coll_eff(DNI, DT[i])                                [-]      (datasheet map, bilinear here)
Q_dot_disc[i]     = DNI*cos(Theta)*L_disc*W                             [W]
Q_dot_abs_disc[i] = Q_dot_disc[i]*eta_coll[i]                           [W]
h[i+1]            = h[i] + Q_dot_abs_disc[i]/m_dot                      [J/kg]
p[i+1]            = p[i]                                                [Pa]
T[i+1]            = temperature(fluid$, h=h[i+1], p=p[i+1])              [degC]
Q_dot             = sum_i Q_dot_abs_disc[i]                             [W]
```

Assumptions (as in the source): the pressure is constant along the absorber
(no pressure drop), the fluid is perfectly mixed in each element (the inlet
temperature of an element is the outlet temperature of the previous one), there
is no thermal inertia and no residence time, and the collector is in tracking
mode with a single incidence angle.

The collector-efficiency map (`parabolic_trough_collector_discretised-sopo_map.csv`,
6 irradiance nodes from 500 to 1000 W/m² × 17 nodes of fluid temperature rise
over the ambient from 55.6 to 277.8 °C, values 0.351 to 0.652) is read with
`interpolate2('sopo_map','Irrad','DT_C','eta_coll',DNI,DT[i])`. It is the
datasheet map of the Soponova MicroCSP collector shipped in the geometry record
of the source; the temperature rise nodes are the tabulated Fahrenheit
differences (100 to 500 °F) converted to °C by the source (`* 5/9`).

### Inputs / outputs

| Input | Value of the example | Unit |
|---|---|---|
| `fluid$` | `Water` | – |
| `m_dot` | 0.6 | kg/s |
| `P_su` | 500 | kPa |
| `T_su` | 100 | °C |
| `T_amb` | 25 | °C |
| `DNI` | 900 | W/m² |
| `Theta` | 10 | deg |
| `v_wind` | 5 | m/s (input of the source, unused by the map path) |
| `n_disc` | 20 | – |
| `L_coll`, `W` | 36.57, 1.524 | m |

| Output | Value | Unit |
|---|---|---|
| `Q_dot` (absorbed power) | 31 370.0 | W |
| `h_ex` (exhaust enthalpy) | 471 748.9 | J/kg |
| `T_ex` (exhaust temperature) | 112.382 | °C |
| `eta_coll_avg` (mean efficiency) | 0.63505 | – |
| `Q_dot_bal` (energy-balance check) | 31 370.0 | W |

## How to run

```bash
cd models/renewables/solar_thermal/parabolic_trough_collector_discretised
/sylvain/git/csl-lanes/bunny/CoolSolve/build/coolsolve ./parabolic_trough_collector_discretised.eescode
```

The model solves without guesses (no `.initials`) and without `coolsolve.conf`;
all blocks are of size 1 and the solution is reached in 0 Newton iterations
from the default values. Changing the number of elements means editing the
literal `20` in `DUPLICATE i=1,20` **and** unrolling the enthalpy march to the
same number of lines (see *Conversion log*).

## Results

10 collectors in series (36.57 m × 1.524 m), water at 0.6 kg/s, 5 bar, 100 °C,
900 W/m², incidence angle 10°, ambient 25 °C, 20 elements:

| Quantity | Value |
|---|---|
| Incident solar power `Q_dot_sun_tot` | 49 397.4 W |
| Absorbed power `Q_dot` | 31 370.0 W |
| Mean efficiency `eta_coll_avg` | 0.63505 |
| Exhaust enthalpy `h_ex` | 471 748.9 J/kg |
| Exhaust temperature `T_ex` | 112.382 °C |
| Efficiency of the first element `eta_coll[1]` | 0.63760 |
| Efficiency of the last element `eta_coll[20]` | 0.63252 |

Convergence with the number of elements (same study as the example of the
source; the CoolSolve values come from copies of the model file with the
literal `20` replaced by the number of elements, generated and deleted for this
import):

| `n_disc` | `Q_dot` LaboThapPy [W] | `Q_dot` CoolSolve [W] | rel. diff |
|---:|---:|---:|---:|
| 1 | 31 495.18 | 31 495.77 | 1.9e-05 |
| 2 | 31 428.88 | 31 429.38 | 1.6e-05 |
| 5 | 31 889.44* | 31 389.75 | 1.0e-05 |
| 10 | 31 376.34 | 31 376.57 | 7.5e-06 |
| 20 | 31 369.80 | 31 369.99 | 6.1e-06 |
| 50 | 31 365.88 | 31 366.04 | 5.2e-06 |

\* value 31 389.4366 W.

The absorbed power falls by 0.41 % between 1 and 50 elements, by 0.034 %
between 10 and 50 and by 0.013 % between 20 and 50: 20 elements are well past
the convergence (10 already give 0.03 %), which is why 20 is the shipped value
(the `plant_sizing` case study of the source also uses 20).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of the absorbed
     power or of the efficiency profile along the absorber, e.g.
     ![efficiency along the absorber](figures/parabolic_trough_collector_discretised_eta.png)
     + one-line caption. A temperature profile along the absorber (T_su_el[i]) or an
     eta_coll[i] vs DT plot would be the natural figure; the array columns of the
     solution give the data. -->

## Verification

**Reference**: the example of the source,
`labothappy/component/examples/solar/parabolic_trough_collector_example.py`
(case study `study_disc`, i.e. the convergence study over 1 to 50 elements
that is reproduced above), re-run in a throw-away virtual environment:

```bash
python3 -m venv work/ptc/venv
work/ptc/venv/bin/pip install ~/git/LaboThapPy matplotlib      # CoolProp 8.0.0
MPLBACKEND=Agg work/ptc/venv/bin/python work/ptc/run_example.py  # the example file itself (study_disc)
MPLBACKEND=Agg work/ptc/venv/bin/python work/ptc/run_pt.py       # same loop, values printed
work/ptc/venv/bin/python work/ptc/gen_ref.py 20                  # -> work/ptc/ref_20.csv
python3 tools/compare_solution.py \
  models/renewables/solar_thermal/parabolic_trough_collector_discretised/parabolic_trough_collector_discretised.sol \
  work/ptc/ref_20.csv --rtol 1e-3
```

`run_example.py` runs the example file of the source itself: it only draws
`Q_dot` against the number of elements and stores no values, so the numbers
compared here come from `run_pt.py`, the same loop with the same inputs and a
printout. Both need two environment patches, which do not touch the physics:
the `import __init__` line of the example (a packaging quirk of the repository,
`ModuleNotFoundError: No module named '__init__'`) is replaced by `pass`, and
the `RectBivariateSpline` call of the geometry record is wrapped with
`np.squeeze` (see *Conversion log*). With them the example runs to completion
(`study_disc`, 50 collectors solved). Both scripts and the virtual environment
were deleted at the end of the import (`work/` is not part of the library).

Result of `compare_solution.py` (64 common variables, reference CSV rows named
as in the model, units W, J/kg, °C):

```
64 common variables, 0 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 76
```

**Maximum relative difference 3.4e-05** (default tolerance of
`compare_solution.py`, `rtol = 1e-3`), reached on `eta_coll[20]` and on
`Q_dot_abs_disc[20]`; `Q_dot` differs by 6.1e-06 and `T_ex` by 7.8e-07. The cause
is the interpolation scheme of the efficiency map: the source interpolates the
6 × 17 table with a **bicubic** `RectBivariateSpline`
(`labothappy/toolbox/geometries/solar/parabolictrough_geometry.py`), the model
with the **bilinear** `interpolate2` of CoolSolve (docs/language_reference.md
§11.2), which is the standard interpolation of an EES two-variable lookup table.
On the 11.1 °C column spacing the two schemes differ by up to 3.4e-05 in
efficiency; the deviation of the total absorbed power shrinks with the number of
elements (1.9e-05 at 1 element, 5.2e-06 at 50) because the map difference is
largest at the inlet of the absorber, where `DT` is smallest and where fewer and
fewer cells sample it. Everything else — the CoolProp enthalpy/temperature of
the water, the geometry, the marching — is identical.

Excluded from the comparison: `h_su` of the reference (the model names this
state `h[1]`, which is compared through `h_ex` and the element states), and the
arrays `DT[i]`, `T_su_el[i]`, `Q_dot_disc[i]`, `p[i]` (they are functions of the
compared inputs, not independent results).

Sanity checks (not part of the source's output):

* energy balance of the march: `Q_dot_bal = m_dot*(h_ex - h[1])` = 31 370.0 W =
  `Q_dot` to 13 significant digits (identity of the marching, kept as a
  diagnostic output);
* the exhaust temperature rises by 12.4 K over 36.57 m of absorber, i.e.
  0.34 K/m, and the mean efficiency 0.635 is inside the range of the map
  (0.628 to 0.652 at 900 W/m²), between the first (0.6376) and last (0.6325)
  element;
* `CSL-0083` carries the heat-loss correlations of the same absorber family
  (Schott PTR70 with its Sopogy Soponova record). They are **not** used here:
  the source's `solve()` uses the datasheet efficiency map, while its
  `heat_losses()` / `Q_dot_abs()` methods (the 10-coefficient semi-empirical
  correlation of R. Dickes, V. Lemort and S. Quoilin,
  https://hdl.handle.net/2268/182680, with the coefficient vector `a` of the
  geometry record) are defined but never called. The heat loss implied by the
  map (about 98 W/m at 106 °C of fluid, 900 W/m², 5 m/s, i.e. 18.0 kW of the
  49.4 kW incident minus 14.4 kW of optical loss, with the optical efficiency
  of the source `eta_opt = eta_other*alpha_r*refl_m*envel_tau = 0.70785`) is
  above the 13.6 W/m that the NREL PTR70 (vacuum) correlation of `CSL-0083`
  returns at the mean fluid temperature of 106.19 °C for the same ambient
  temperature, irradiance, wind speed and incidence angle: the
  datasheet map of the MicroCSP collector is a whole-collector value, end losses
  included, and is not the NREL receiver loss.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of `PTCollector` from LaboThapPy, file
`labothappy/component/solar/parabolic_trough_collector.py`, with the collector
data of `labothappy/toolbox/geometries/solar/parabolictrough_geometry.py` and
the study case of
`labothappy/component/examples/solar/parabolic_trough_collector_example.py`,
commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy
Copyright (C) 2025 Universite catholique de Louvain (UCLouvain), Universite de
Liege (ULiege), Universite de Mons (UMONS). Original authors: B. Chaudoir,
E. Neven et al. (see `AUTHORS.txt` of the repository).
Changes: translated from Python to CoolSolve; the Python loop over the
discretisation elements became a `DUPLICATE` array of cells; the map
interpolation is bilinear instead of bicubic (see *Verification*); the semi-
empirical heat-loss methods of the source, unused by its `solve()`, were not
translated. Scientific basis: Sopogy SopoNova MicroCSP collector datasheet
(efficiency map); heat-loss correlation (not used here) of R. Dickes,
V. Lemort and S. Quoilin, https://hdl.handle.net/2268/182680.

The model is published under the library licence (MIT).

## Conversion log

- **2026-10-08 — translation**: LaboThapPy `PTCollector.solve()` →
  `parabolic_trough_collector_discretised.eescode`. The `numpy` arrays of the
  source (`T`, `p`, `h`, `Q_dot_disc`, `Q_dot_abs_disc`, `eta_coll`) became
  EES arrays; the Python loop became a `DUPLICATE` block; `AbstractState.update
  (HmassP_INPUTS)` + `.T()` became `temperature(fluid$,h=…,p=…)`; `cos(Theta)`
  of the source takes radians (`10*pi/180`) and is `cos(Theta)` on a degree
  value here (`Theta = 10 [deg]`); the state indices are 1-based
  (`T[i]` in the source is the inlet of element `i`, `T[i+1]` its outlet).
- **2026-10-08 — sum and energy balance**: the source sums the element powers
  with `sum(Q_dot_abs_disc)`; the indexed `SUM(X[i],i=1,N)` is not available
  (`CS-GAP-SUM-INDEXED`), so the 20 terms are written out in the variadic `sum`
  of CoolSolve (same result). `Q_dot_bal = m_dot*(h_ex-h[1])` is added as a
  diagnostic identity (it is not an extra constraint on the solution).
- **2026-10-08 — enthalpy march unrolled**: a `DUPLICATE` loop cannot shift an
  array index in CoolSolve: with `DUPLICATE i=1,20`, `T[i+1]` is parsed as
  `T[(2.000000 + 1.000000)]`, a variable that does not match `T[i]` or
  `T[n_disc+1]`, so the model is refused as not square (19 unmatched equations
  of 23). The 20 enthalpy states are therefore written out explicitly, and only
  the per-element quantities (inlet temperature, temperature rise, efficiency on
  the map, incident and absorbed power) stay in the `DUPLICATE` loop. This is
  the CoolSolve bug `CS-BUG-DUPLICATE-INDEX-EXPR` (index expressions inside a
  `DUPLICATE` body are not folded); it is listed in `missing_features` although
  it does not block the model, the march being written out (same convention as
  for `CS-GAP-SUM-INDEXED` in the entry above).
- **2026-10-08 — map table**: `coll_eff` is the 6 × 17 Soponova efficiency map
  as a companion table `parabolic_trough_collector_discretised-sopo_map.csv`
  (`Irrad,DT_C,eta_coll`, 102 rows), read with `interpolate2`. The Fahrenheit
  temperature-rise nodes of the source (`[100…500]*5/9`) are stored already
  converted to °C.
- **2026-10-08 — source defect found while re-running the example**: with
  NumPy ≥ 1.25 the example does not run unmodified, because
  `RectBivariateSpline` returns a 1 × 1 array for scalar arguments and the
  source stores it in an array element
  (`self.Q_dot_abs_disc[i] = ... * self.params['coll_eff'](DNI, DT)` →
  *"ValueError: setting an array element with a sequence"*). The verification
  script wraps the spline call with `np.squeeze` (no change of the physics).
  This is a defect of the source, not of CoolSolve.
- **Level**: equations 140 after analysis (1 point, criterion 50–300); largest
  block 1 (0); `DUPLICATE` arrays present (1); discretisation (1);
  semi-empirical calibration (1); no curated guesses, no `coolsolve.conf`, 0
  Newton iterations (0) → score 4 → level 3 (docs/taxonomy.md §3).

## Limitations and CoolSolve gaps

* No CoolSolve gap or bug blocks the model: it runs as it stands
  (`status: verified`). `missing_features` lists the two IDs whose workaround
  the native file uses, as `CSL-0122` does for its sum:
  - `CS-BUG-DUPLICATE-INDEX-EXPR`: an index expression inside a `DUPLICATE`
    body is not folded, so `h[i+1] = h[i] + Q[i]/m_dot` cannot be written inside
    the loop; the 20 enthalpy states are written out instead (see *Conversion
    log*);
  - `CS-GAP-SUM-INDEXED`: the indexed `SUM(X[i],i=1,N)` is not available, so
    `Q_dot` uses the variadic `sum` of the 20 element terms.
* Physics: isobaric absorber, no pressure drop, no thermal inertia, no
  residence time, one incidence angle (tracking), datasheet map extrapolated
  flat outside its range (CoolSolve clamps, `CS-GAP-INTERP-EXTRAP`); the map is
  read at the *inlet* temperature of each element, as in the source.
* The heat-loss correlations of `CSL-0083` and the semi-empirical
  `heat_losses()` / `Q_dot_abs()` methods of the source (not used by its
  `solve()`) are not part of this model; see *Verification*.

## Related models

- `CSL-0083` *parabolic_trough_loss_correlations*: function library of the
  empirical receiver/collector heat-loss and efficiency correlations of the
  same sub-category, including the Sopogy Soponova receiver record; it can
  replace the efficiency map of this model (a variant is not shipped).
- `CSL-0082` *parabolic_trough_receiver_forristal*: first-principles 1D radial
  receiver balance of the same collector family, the counterpart of this
  absorber/efficiency-map model.
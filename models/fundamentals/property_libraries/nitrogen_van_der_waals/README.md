# Van der Waals equation of state for nitrogen

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0355`

Textbook example on a cubic equation of state: nitrogen is brought to the
reduced conditions P_r = 1.2, T_r = 1.2 and its specific volume and
compressibility factor are computed from the van der Waals equation of state,
then compared with the same quantities from the built-in real-fluid
properties. The comparison shows the accuracy of the van der Waals EOS away
from the critical point (here the volume is 2.9 % too low).

| | |
|---|---|
| **Category** | Fundamentals › Property libraries |
| **Fluids** | Nitrogen |
| **Size** | 17 equations, all explicit (largest block: 1) |
| **Source** | *Thermodynamics*, S. A. Klein and G. F. Nellis, Cambridge University Press, 2011, example 10.1-1 (F-Chart Software EES example) |
| **Authors** | S. A. Klein, G. F. Nellis (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Apply the van der Waals equation of state to nitrogen at the reduced
conditions P_r = 1.2 and T_r = 1.2: determine the specific volume and the
compressibility factor from the van der Waals EOS and compare them with the
values obtained from the built-in (real-fluid) nitrogen properties.

## Model

Fluid constants from the built-in functions: `MW = MolarMass(F$)`,
`R = R#/MW`, `P_c = P_crit(F$)`, `T_c = T_crit(F$)`. The van der Waals
coefficients are those of the example (molar form divided by the molar mass):

$$a = \frac{27\,R^2\,T_{c}^2}{64\,P_{c}}, \qquad b = \frac{R\,T_{c}}{8\,P_{c}}$$

State: `P = P_r*P_c`, `T = T_r*T_c_abs − 273.15` (reported in °C, absolute
`T_abs` used inside the EOS). The van der Waals EOS is implicit in v:

$$P = \frac{R\,T_{abs}}{v-b} - \frac{a}{v^2}, \qquad Z = \frac{P\,v}{R\,T_{abs}}$$

and the reference values come from the built-in properties:
`v_EES = Volume(F$,T=T,P=P)`, `Z_EES = P*v_EES/(R*T_abs)`.

## How to run

```bash
coolsolve ./nitrogen_van_der_waals.eescode
```

No guesses needed (all explicit except one one-unknown block). Change `P_r`
or `T_r` for another reduced state; other fluids work by editing `F$` (the
example logic is fluid-independent).

## Results (P_r = 1.2, T_r = 1.2)

| Quantity | van der Waals | Built-in properties |
|---|---:|---:|
| P [Pa] | 4 074 960 | 4 074 960 |
| T [°C] | −121.72 | −121.72 |
| v [m³/kg] | 0.0079707 | 0.0082086 |
| Z, dimensionless | 0.7227 | 0.7442 |

At this state the van der Waals EOS underestimates the specific volume by
2.9 % against the built-in nitrogen properties (relative to `v_EES`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. a parametric sweep of
     Z (van der Waals) and Z_EES vs P_r, figures/nitrogen_van_der_waals_z_pr.png -->

## Verification

The EES file stores the solution of a run at **P_r = 40, T_r = 1.2** (the
stored `P_r = 40` contradicts the equation `P_r = 1.2` of the file: stale
record, flagged by the extraction tool). The conversion was therefore checked
at that state: a copy of the model with `P_r = 40` was solved and compared
with the stored solution (`compare_solution.py --ees-units`, EES values in K
converted to °C). 12 common variables, 0 differ at rtol = 0.001; at rtol =
1e-12:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| v | 0.001599 | 0.00159902 | 1.19e-05 |
| Z | 4.83253 | 4.83253 | 7.51e-09 |
| v_EES | 0.00120215 | 0.00120215 | 2.86e-06 |
| Z_EES | 3.63317 | 3.63312 | 1.47e-05 |

Maximum over all 12 common variables: 2.38e-05 (on `a`). The deviations come
from the gas-constant value: the stored solution implies EES `R#` =
8314.34 J/(kmol-K) against CoolSolve `R#` = 8314.462618 (CODATA 2018),
i.e. 1.2e-05 on `R` (propagated to 2.4e-05 on `a`), plus 2.9e-06 on `MW`
(28.0134 vs 28.01348 kg/kmol). Shipped model (P_r = 1.2): `.sol` baseline;
`v`, `Z` re-checked by hand from a, b, R.

## Source and attribution

Example 10.1-1 of *Thermodynamics*, S. A. Klein and G. F. Nellis, Cambridge
University Press, 2011, distributed as an EES example by F-Chart Software
(the original file header links
`https://fchartsoftware.com/ees/examples/examples_thermodynamics_2011/chapter%2010/example%2010.1-1.eez`).
Library candidate `EEX-113` of the `ees_examples` collection (raw `.eez` in
`ees-examples-raw/Case_Study/example_10.1-1.eez`; the inner `.EES`, EES
version X11.913, was extracted before conversion).

## Niche

Nearest library models: `CSL-0317` *pseudo_critical_properties* (supercritical
state characterisation of real fluids, function library) and `CSL-0047`
*nonideal_gas_isothermal_work* (piston-cylinder work with a vdW-like EOS,
`v*(P+k/v^2)=R*T`). Neither computes state properties from a cubic EOS and
compares them with the built-in real-fluid properties; this model is the
library's introductory example of a cubic equation of state and of reduced
variables.

## Conversion log

- **2026-11-15 — import** (`tools/ees_extract.py` on the inner `.EES` of the
  `.eez`): unit system `$UnitSystem SI MASS RAD PA K J` converted by hand to
  CoolSolve SI-°C-Pa-J. No trigonometric function is used (the RAD setting is
  irrelevant). Temperatures: `T_crit(F$)` returns °C in CoolSolve (126.192 K
  in the original), so absolute temperatures are carried explicitly
  (`T_c_abs = T_c + 273.15` in `a`, `b`; `T_abs = T + 273.15` in the EOS and
  in `Z`); the state temperature `T` is reported in °C. Pressures, energies
  and `MW`, `R`, `a`, `b` are unchanged (already Pa/J-based, built with K).
- **2026-11-15 — directive dropped**: the `$ifnot ParametricTable / $elseif /
  $ShowWindow Plot` block kept only its single point `P_r = 1.2` (as
  instructed; the stored solution shows a last run at `P_r = 40` — see
  *Verification*); `$TabStops` removed.
- **2026-11-15 — renaming**: the variables `P_crit` and `T_crit` (same names
  as the built-in calls) are renamed `P_c` and `T_c`; all other variable
  names are kept (`v_EES`, `Z_EES` keep their original names, comments say
  "built-in properties" where the original said "EES").
- **2026-11-15 — verification reference**: the shipped model runs at
  `P_r = 1.2`; the numerical verification against the EES stored solution was
  done at the stored state `P_r = 40` with a temporary copy (deleted with the
  work folder).
- **Level**: equations 17 < 50 → 0; largest block 1 ≤ 5 → 0; no
  functions/arrays → 0; no multi-zone → 0; no semi-empirical physics → 0; no
  curated guesses → 0; score 0 → level 1.

## Limitations and CoolSolve gaps

- The van der Waals EOS is a teaching approximation; near the critical point
  its accuracy degrades (the example compares only one state).
- No CoolSolve gap blocks this model (`MolarMass`, `P_crit`, `T_crit`, `R#`
  and `Volume` are supported; `T_crit` returns °C, the absolute temperature
  is rebuilt by +273.15).

## Related models

- `CSL-0047` *nonideal_gas_isothermal_work*: boundary work of a gas obeying a
  vdW-like EOS in a piston-cylinder (work problem, not a property comparison).
- `CSL-0317` *pseudo_critical_properties*: pseudo-critical state functions for
  supercritical real fluids.

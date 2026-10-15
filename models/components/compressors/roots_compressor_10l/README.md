# Roots compressor, 10 L (exercise 2 bis)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ❌ **Failing** &nbsp;|&nbsp; `CSL-0202`

Teaching exercise for a Roots compressor of 10 L displacement, tested on dry
air at a discharge pressure of 1.4 bar. The volumetric efficiency is 85 % and
the mechanical efficiency is 95 %. The equation window builds the inlet
pressure drop through a 5 cm orifice and a fictitious leakage nozzle, and it
asks for the isentropic efficiency at that test point. CoolSolve accepts the
syntax and reports a square system, and the inlet-orifice block has no real
root.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 50 equations (largest block: 7) |
| **Source** | thermo_models, file `R2 - EX 2 - SB - Bis.EES` |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@ae7946e — failing (see *Verification*) |

## Problem statement

A Roots compressor with a displacement of 10 litres is tested as follows.
The fluid is dry pure air. The suction pressure and temperature are 1 bar and
20 °C. The discharge pressure is 1.4 bar. The volumetric efficiency is then
85 % and the mechanical efficiency is 95 %.

Show how the volumetric and isentropic efficiencies could vary with the
discharge pressure at constant rotational speed, and with the rotational speed
at constant discharge pressure. Also show how the discharge temperature could
vary in both cases.

The equation window is the single test point. The rotational speed is set to
3000/60 rev/s. The two sweeps are described in the statement and in a closing
comment; the file stores no parametric table.

## Model

The fluid name in the property calls is `Air`. A CoolSolve hint suggests
`AirH2O` for moist air; the statement says dry pure air, and the fluid is
left as `Air`.

- Displacement `V_s` = 10×10⁻³ m³. Suction state `P_su_0` = 1×10⁵ Pa,
  `T_su` = 20 °C. Discharge pressure `P_ex` = 1.4×10⁵ Pa.
- Volumetric efficiency `epsilon_v` = `V_dot_su` / `V_dot_s` = 0.85, with
  `V_dot_s` = `N`·`V_s` and `V_dot_su` = `M_dot`·`v_su`. This fixes the
  fresh-charge mass flow from the suction specific volume.
- Mechanical efficiency `eta_m` = `W_dot_in` / `W_dot` = 0.95. The Roots
  characteristic is `W_dot_in` = `V_dot_s`·(`P_ex` − `P_su`). The shaft power
  is `W_dot` = `M_dot`·`w`.
- Overall isentropic efficiency `epsilon_s` = `w_s` / `w`, with
  `w_s` = `h_ex_s` − `h_su_0` along the isentropic path from the fresh-charge
  suction state to `P_ex`.
- Inlet orifice `A_thr` = 0.05²/4·π (diameter 5 cm). The throat is isentropic
  from the fresh charge. `P_thr` = max(`P_su`, `P_crit`) with `gamma` = 1.4.
  The isentropic temperature–pressure relation that would have computed
  `gamma` is commented out in the original; the provisional value 1.4 is the
  equation that remains.
- Leakage returns through a second nozzle. `P_thr_l` = max(`P_crit_l`, `P_su`),
  and `gamma_l` is computed from the isentropic relation written with `+273`
  (the file does not write +273.15). The leakage area `A_thr_l` is an unknown.
- The fresh charge and the leakage mix at the compressor inlet. `h_su` is set
  equal to `h_su_0`.

`P_su` is an unknown of `P_thr` = max(`P_su`, `P_crit`). The system is square
(50 equations, 50 variables), so no diagram-window value was copied in.

The original comments, and does not solve, three other closures:
`M_dot_l` = 0.1·`M_dot`, `M_dot_l` = 0.1577·`M_dot`, and `P_su` = `P_su_0`.
It also comments two fixed areas (`A_thr_l` = 0.0002773 m² and
`A_thr` = 0.004601 m²) as data for varying `P_ex` and `N`. Those lines are
not in this file.

## How to run

The file does not converge:

```bash
coolsolve ./roots_compressor_10l.eescode
# Block 16 (size 6) failed: MaxIterations, residual 3.438
```

Block 16 is the inlet throat (`C_thr`, `V_dot_thr`, `v_thr`, `h_thr`,
`T_thr`, `P_thr`). The `.initials` file is the starting point described in
*Verification*. There is no `.sol` and no `coolsolve.conf`.

## Results

No converged CoolSolve run.

The EES file's last recorded numbers, which do not satisfy the active
equations, are:

| Quantity | Stored EES value |
|---|---|
| Fresh-charge mass flow `M_dot` | 0.505095 kg/s |
| Mixed inlet flow `M_dot_in` | 0.555605 kg/s |
| Leakage `M_dot_l` | 0.050510 kg/s |
| Roots internal power `W_dot_in` | 22690.9 W |
| Shaft power `W_dot` | 23885.1 W |
| Volumetric efficiency `epsilon_v` | 0.85 (data) |
| Mechanical efficiency `eta_m` | 0.95 (data) |
| Isentropic efficiency `epsilon_s` | 0.62836 |
| Inlet pressure `P_su` | 94618.3 Pa |
| Throat pressure `P_thr` | −74168.5 Pa |

`M_dot_l` / `M_dot` = 0.1 and `epsilon_s` ≈ 0.6284 match the author's commented
note for the trial `M_dot_l` = 0.1·`M_dot`. In that same note the inlet area is
0.004601 m². The stored `A_thr` is already 0.0019635 m², the active 5 cm
orifice, and the stored throat state has left the energy balance
(`P_thr` is negative). The author wrote that this orifice gives a problem in
the definition of `h_thr`.

Other numbers written in comments, from trials that are not the active window:

| Trial, as commented | `epsilon_s` | `M_dot` | `M_dot_l` | `A_thr` | `A_thr_l` |
|---|---|---|---|---|---|
| No suction pressure drop | 0.7129 | 0.5051 kg/s | 0.07969 kg/s | — | 0.0002773 m² |
| `M_dot_l` = 0.1·`M_dot` | 0.6284 | 0.5051 kg/s | 0.05051 kg/s | 0.004601 m² | 0.0001711 m² |
| `M_dot_l` = 0.1577·`M_dot` | 0.7128 | 0.5051 kg/s | 0.07965 kg/s | 0.1183 m² | 0.0002771 m² |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the model has no converged solution yet, so there is no plot. -->

## Verification

`compare_solution.py` was not run. CoolSolve does not produce a solution, so
there is no `max_rel_diff`.

The active window is square: 50 equations, 50 variables, largest block 7
(the mixture). The failing block is the inlet orifice, size 6. The fresh-charge
flow is fixed by the volumetric efficiency before the orifice is solved.
With CoolSolve's ideal-gas Air, the isentropic mass flow through
`A_thr` = 0.05²/4·π peaks near 0.463 kg/s at about 52.8 kPa. The fresh-charge
flow is 0.505 kg/s. Every positive throat pressure leaves a continuity
residual; the mass-flow ratio never reaches 1 (the peak ratio on that sweep
is 0.917).

| Start | Newton result |
|---|---|
| Shipped `.initials` | iteration 100, residual 3.438073 |
| No `.initials` | line search failed at iteration 0, residual 1038.346181 |
| Raw stored EES values, including `P_thr` < 0 | iteration 100, residual 20599.127227 |

The same six orifice equations, started from a CoolProp-consistent sonic
state and tried with Newton, trust region, Levenberg–Marquardt, BisectionND,
homotopy and the partitioned solver, stall near residual 0.024.

Ideal-gas Air enthalpy at the suction state (20 °C, 1×10⁵ Pa) is
419404.9217559 J/kg in CoolSolve and 293534.3441 J/kg in the stored solution.
CoolSolve − EES = +125870.5776559 J/kg. The entropy difference at the same
state is 3867.259359479 − 5682.126158 = −1814.866798521 J/kg·K. Specific
volume is 0.8411720268193 m³/kg against 0.8414254791 m³/kg (relative
difference 3.0×10⁻⁴). The enthalpy offset is a reference-state difference. It
is separate from the power, the efficiencies and the missing root: a start
that already uses CoolSolve enthalpies still has no orifice solution.

The unit system stored in the file is `SI MASS DEG PA C J`. The comparison
flag `--ees-units` was not used. Stored enthalpies are already in J/kg
(about 2.94×10⁵, not a few hundred kJ). The variable-info unit string on
`epsilon_s` is `J/kg`, and the author's comment repeats `[J/kg]`, while the
value is 0.628. That label is not a scaling error. `M_dot_in` and `M_dot_l`
carry the unit string `-`.

The extractor lists 51 names. `C` has an empty value and the default guess 1.
It is the letter in `20°C`, and it is not a variable of the equation window.
Fifty names have a stored value, which is the inventory's 50/51.

## Source and attribution

The equation window names no person. The file name carries the mark `SB`, and
the EES licence tag is `{$ID$ #202: Laboratoire de Thermodynamique, U. de Liege}`.
Neither is used here as an author. The inventory attributes the course to
J. Lebrun, V. Lemort and S. Bertagnolio; the authors field stays
`TBD (ULiège MSTh)` until the maintainer confirms a name written for this file.

ULiège course *Machines et systèmes thermiques* (MSTh), repetition R2,
exercise 2 bis. Source file, not copied into the library:

`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/SB/R2 - EX 2 - SB - Bis.EES`

EES X7.458. The text is plain, not RTF. Candidate `TM-0036`.

## Conversion log

- **2026-10-15 — import**: `tools/ees_extract.py` on `R2 - EX 2 - SB - Bis.EES`.
  The stored unit system is already SI, mass, degrees, Pa, °C, J, so values
  were not rescaled and `--ees-units` was not used. The `$UnitSystem` line
  inserted by the extractor was deleted. The licence tag was dropped by the
  extractor. Comments were translated into English. Commented closures and
  the author's result lists were removed from the equation file; the numbers
  are in *Results*. The system is square, so no diagram-window input was
  restored. The extract report lists no lookup table and no parametric table;
  the comment that mentions parametric tables has no table behind it.
  The decoded name `C` was ignored.
- **2026-10-15 — initials**: enthalpies in `.initials` are the stored values
  plus 125870.5776559 J/kg, and entropies are the stored values minus
  1814.866798521 J/kg·K (CoolSolve − EES for ideal-gas Air at 20 °C and
  1×10⁵ Pa). `P_thr`, `h_thr`, `C_thr`, `V_dot_thr`, `v_thr` and `T_thr` use
  the EES guess column. Their stored values differ from those guesses, and
  the stored `P_thr` is negative. The guesses satisfy the inlet energy balance
  in the EES enthalpy reference (`h_thr` + `C_thr`²/2 = `h_su_0`). There is
  no second physical root to select: the active orifice equations have no
  positive-pressure solution.
- **Level**: equations 50 → 1; largest block 7 → 1; no function, procedure or
  array → 0; one component, no multi-zone discretisation → 0; the efficiencies
  are data and the window is one test point → 0; a curated start and the full
  solver pipeline still leave a residual, because the orifice block has no
  root → 0. Score 2 → level 2. No pedagogical shift.

## Limitations and CoolSolve gaps

The 5 cm inlet orifice cannot pass the fresh-charge flow fixed by the
volumetric efficiency: the isentropic throat chokes near 0.463 kg/s and the
equation window requires 0.505 kg/s. The statement asks for curves against
discharge pressure and speed; the window is the one test point, and the file
contains no parametric table.

`gamma` = 1.4 is the provisional value left active. The leakage-nozzle
relation converts Celsius with `+273`. Property calls use `Air`.

No CoolSolve language feature is missing. `missing_features` is empty.
`max()` and the property calls are accepted. The failure is the residual of
block 16.

## Related models

No library model is this calculation.

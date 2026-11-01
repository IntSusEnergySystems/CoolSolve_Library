# Roots compressor, 10 L (exercise 2 bis)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** (adapted from the original) &nbsp;|&nbsp; `CSL-0202`

Teaching exercise for a Roots compressor of 10 L displacement, tested on dry
air at a discharge pressure of 1.4 bar. The volumetric efficiency is 85 % and
the mechanical efficiency is 95 %. The equation window builds the inlet
pressure drop through a 5 cm orifice and a fictitious leakage nozzle, and it
asks for the isentropic efficiency at that test point. As written, the 5 cm
orifice cannot pass the fresh-charge flow and the window has no solution;
the model uses the orifice area commented by the author (0.004601 m², the
operating point of the stored EES solution) — see *Adaptation*.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 50 equations (largest block: 7) |
| **Source** | thermo_models, file `R2 - EX 2 - SB - Bis.EES` |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the stored EES solution after one documented adaptation (orifice area); variant verified too |

> **Which file to open.** `roots_compressor_10l.eescode` (with the inlet orifice,
> adapted area). The variant `roots_compressor_10l_no_inlet_drop.eescode` (same
> exercise without the inlet orifice, verified against its own EES stored
> solution) is described in *Variant: no inlet pressure drop* below.

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
- Inlet orifice `A_thr` = 0.004601 m² (diameter 76.5 mm; the original writes
  0.05²/4·π, see *Adaptation*). The throat is isentropic
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

## Adaptation (2026-11-01)

The equation window of the original has **no solution**: with the 5 cm
orifice (`A_thr` = 0.0019635 m²) the isentropic throat chokes at about
0.463 kg/s (ideal-gas Air, 1 bar, 20 °C, critical pressure 52.8 kPa), while
the volumetric efficiency imposes 0.505 kg/s of fresh charge. The author
notes it in a comment ("this orifice gives a problem in the definition of
h_thr"), and the stored EES solution is not a solution of that window (its
throat pressure is −74 168 Pa). Every other stored value is the operating
point of the author's commented trial `M_dot_l` = 0.1·`M_dot`, whose inlet
area the author wrote down as 0.004601 m² ("data for varying P_ex and N").

The model therefore uses `A_thr` = 0.004601 m² (the original line is kept as
a comment). Nothing else changes. With it the window is consistent and
CoolSolve reproduces the stored EES solution (*Verification*): the throat is
subsonic (`P_thr` = `P_su` = 94.6 kPa > `P_crit`, `C_thr` = 96 m/s). Physical
checks of the solution: the inlet throttling keeps the total enthalpy
(`h_su` = `h_su_0`, entropy rises across the orifice), the leakage nozzle is
isentropic up to its throat and the mixing balance closes
(`M_dot`·`h_su` + `M_dot_l`·`h_ex_1` = `M_dot_in`·`h_su_1`), the shaft power
exceeds the isentropic power (`epsilon_s` = 0.628 < 1) and the Roots internal
work `V_dot_s`·(`P_ex` − `P_su`) rises when the orifice lowers `P_su`, as it
should.

The original comments, and does not solve, three other closures:
`M_dot_l` = 0.1·`M_dot`, `M_dot_l` = 0.1577·`M_dot`, and `P_su` = `P_su_0`.
It also comments two fixed areas (`A_thr_l` = 0.0002773 m² and
`A_thr` = 0.004601 m²) as data for varying `P_ex` and `N`. Those lines are
not in this file.

## How to run

```bash
coolsolve ./roots_compressor_10l.eescode
```

It converges in 27 iterations from the shipped `.initials` (EES guesses, with
the enthalpies and entropies moved to CoolSolve's Air reference, see
*Conversion log*). **Hard start without them:** from the default guesses the
normal solve fails (block 20, the 7-variable mixture block, line search failed
at iteration 10); the GUI **Try Harder** button converges it (549 iterations).
No `coolsolve.conf` is needed.

## Results

CoolSolve results (adapted orifice area, `.sol`):

| Quantity | CoolSolve | Stored EES value |
|---|---:|---:|
| Fresh-charge mass flow `M_dot` | 0.505247 kg/s | 0.505095 kg/s |
| Mixed inlet flow `M_dot_in` | 0.555720 kg/s | 0.555605 kg/s |
| Leakage `M_dot_l` | 0.050473 kg/s | 0.050510 kg/s |
| Inlet pressure `P_su` | 94 613.7 Pa | 94 618.3 Pa |
| Roots internal power `W_dot_in` | 22 693.2 W | 22 690.9 W |
| Shaft power `W_dot` | 23 887.5 W | 23 885.1 W |
| Isentropic efficiency `epsilon_s` | 0.628499 | 0.628361 |
| Leakage opening `A_thr_l` | 1.70917×10⁻⁴ m² | 1.71082×10⁻⁴ m² |
| Throat velocity `C_thr` | 96.10 m/s | (151.8, not a solution) |

The EES file's last recorded numbers (they are the trial `M_dot_l` = 0.1·`M_dot`
except the throat state, which does not satisfy the active equations) are:

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

## Variant: no inlet pressure drop

`roots_compressor_10l_no_inlet_drop.eescode` (+ `.initials`, `.sol`) is the
variant to open when the native file fails. It is the file `MSTh-SB-R2-Ex2.EES`
of the same course folder (candidate `TM-0034`): the same exercise without the
inlet orifice, 34 equations, suction at `P_su` = 1 bar. The author's comment in
the native file ("no suction pressure drop" trial) describes this case.

What differs from the native file:

- There is no inlet orifice (`A_thr`, throat of the fresh charge, `P_crit`,
  `P_su_0` versus `P_su`). The suction pressure `P_su` is data, and the energy
  balance of the inlet throat is absent.
- The leakage nozzle uses `gamma` = 1.4 (provisional value of the source) in
  `P_thrmin`, where the native file computes `gamma_l` from an isentropic
  relation written with +273. The leakage entropy is `s_ex_1` = `s_su_1`.
- Variable names are those of the source file: `P_su`, `h_su`, `s_su`,
  `W_dot_s` (= `M_dot`·(`h_ex_s` − `h_su`)), `P_thrmin`, `rpm`, `A_thr_l`.
  The leakage opening `A_thr_l` is an unknown, as in the native file.

The equations are those of the EES source (valid EES, no CoolSolve gap); only
the comments are translated. Every other quantity is solved as in the native
file. The file needs its `.initials`: the stored EES values are shifted by the
enthalpy and entropy reference offset of CoolSolve's Air (see *Conversion
log*). Without `.initials` CoolSolve reports `SUCCESS` after 51 iterations, but
the final verification fails with a CoolProp error at `H` = −5.196×10⁸ J/kg:
that run is not a solution.

| Quantity (variant) | CoolSolve | EES stored solution |
|---|---:|---:|
| Fresh-charge mass flow `M_dot` | 0.505247 kg/s | 0.505095 kg/s |
| Leakage `M_dot_l` | 0.079697 kg/s | 0.079694 kg/s |
| Leakage fraction `M_dot_l` / `M_dot` | 0.1577 | 0.1578 |
| Shaft power `W_dot` | 21052.6 W | 21052.6 W |
| Isentropic efficiency `epsilon_s` | 0.713132 | 0.712902 |
| Leakage opening `A_thr_l` | 2.77228×10⁻⁴ m² | 2.77282×10⁻⁴ m² |

These are the values of the "no suction pressure drop" trial written in the
comments of the native file (`epsilon_s` 0.7129, `M_dot_l` 0.07969 kg/s,
`A_thr_l` 0.0002773 m²), and with the 0.1577 fraction of its third trial.

Candidate `TM-0037` (`R2 - Ex 2 - SB.EES`) is the same exercise as the native
file with the inlet-orifice block commented out and `P_su` = `P_su_0`. Its EES
stored solution is cleared (extractor warning: most stored values are −9999),
so it has no reference of its own and no separate variant is shipped. As a
check, the native file with the orifice block deleted and `P_su` = `P_su_0`
solves in CoolSolve (41 equations, 41 variables) and gives `epsilon_s` =
0.713132 and `A_thr_l` = 2.77212×10⁻⁴ m², the values of the variant (the small
difference of `A_thr_l` comes from `gamma_l` of the isentropic relation).

## Verification

Main file, adapted (CoolSolve 0.4.0@9768373, 2026-11-01): solves in 27
iterations (50 equations, 50 variables), compared with the stored EES solution
of `R2 - EX 2 - SB - Bis.EES` with the 8 stored enthalpies and entropies moved
by the Air reference offsets measured below (+125 870.58 J/kg,
−1814.87 J/(kg·K)); `compare_solution.py` prints

```
50 common variables, 7 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0
```

The 43 agreeing values include every result of the exercise (largest
difference 9.65×10⁻⁴ on `A_thr_l`; `epsilon_s` 2.2×10⁻⁴, `W_dot` 1.0×10⁻⁴,
`P_su` 4.9×10⁻⁵; `v_su` differs by 3.0×10⁻⁴ as in the variant). The 7
differing variables are the adapted area `A_thr` and the six throat variables
(`C_thr`, `V_dot_thr`, `v_thr`, `h_thr`, `T_thr`, `P_thr`): the stored throat
state is the one left by the 5 cm orifice, which is not a solution
(`P_thr` = −74 168 Pa). The EES guess column of these six variables, on the
contrary, is the CoolSolve throat state (`C_thr` 96.11 m/s, `T_thr` 15.41 °C,
`v_thr` 0.8754 m³/kg): it is the trial of the 0.004601 m² orifice.

Native file as originally imported (5 cm orifice; re-run with CoolSolve
0.4.0@9768373 on 2026-10-31 and 2026-11-01): block 16 stops at Newton
iteration 100 with residual 3.43807; Try Harder (full pipeline, tearing,
symbolic reduction, multi-start) stalls at residual 0.0242 — there is no root,
as analysed below.

Variant `roots_compressor_10l_no_inlet_drop.eescode` (solves in 13 iterations,
34 equations, 34 variables, largest block 6, residual 1.7e-10), compared with
its EES stored solution (`MSTh-SB-R2-Ex2.EES`, 34 values, unit system SI,
`--ees-units` not used):

```
34 common variables, 8 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0
```

The 8 differing variables are `h_ex_1`, `h_ex_s`, `h_su`, `h_su_1`, `h_thr`,
`s_ex_1`, `s_su` and `s_su_1`: the absolute enthalpy and entropy reference of
CoolSolve's Air differs from the EES one (+125870.58 J/kg and
−1814.87 J/(kg·K) at 20 °C, 1×10⁵ Pa; measured in the native-file analysis below). The other 26
values agree within the 1×10⁻³ tolerance (largest 3.22×10⁻⁴, `epsilon_s` and
`W_dot_s`; `v_su` differs by 3.0×10⁻⁴ as for the native file). With the 8 EES
enthalpies and entropies shifted by those offsets (a
temporary reference table, not shipped), the same tool prints
`34 common variables, 0 differ (rtol=0.001)` and the largest relative
difference is 3.22×10⁻⁴.

Native file, initial analysis (CoolSolve 0.3.0@ae7946e):

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

Variant source (candidate `TM-0034`, EES X7.458, same stamp
`{$ID$ #202: Laboratoire de Thermodynamique, U. de Liege}`; the file name carries
the mark `SB`, not used as an author), also not copied:

`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/SB/MSTh-SB-R2-Ex2.EES`

Candidate `TM-0037` (same exercise, cleared stored solution):

`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/SB/R2 - Ex 2 - SB.EES`

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
- **2026-10-31 — variant (T-MERGE of `TM-0034`)**: `tools/ees_extract.py` on
  `MSTh-SB-R2-Ex2.EES` (34 variables, no table, unit system SI mass deg Pa C J,
  no rescaling). `roots_compressor_10l_no_inlet_drop.eescode`: equations
  unchanged; `$UnitSystem` line deleted; French comments translated to English;
  header added. `roots_compressor_10l_no_inlet_drop.initials`: the extracted
  stored values, with the 5 enthalpies (`h_*`) plus 125870.5776559 J/kg and the
  3 entropies (`s_*`) minus 1814.866798521 J/(kg·K), the CoolSolve − EES offsets
  of the native-file analysis (10 significant digits). The `.sol` is the run of
  this file. `TM-0037`: no variant (cleared stored solution), see *Variant*.
- **2026-11-01 — adaptation (failing → verified)**: review of the failing
  models. The 5 cm orifice has no solution (choked throat, see *Adaptation*);
  `A_thr` set to the author's commented 0.004601 m², the original line kept as
  a comment, header status updated. The `.initials` (unchanged) converge the
  adapted file in 27 iterations; the `.sol` is that run. Compared with the
  stored EES solution as described in *Verification*.
- **Level**: equations 50 → 1; largest block 7 → 1; no function, procedure or
  array → 0; one component, no multi-zone discretisation → 0; the efficiencies
  are data and the window is one test point → 0; a curated start and the full
  solver pipeline still leave a residual, because the orifice block has no
  root → 0. Score 2 → level 2. No pedagogical shift.

## Limitations and CoolSolve gaps

Adapted from the original: the 5 cm inlet orifice of the original cannot pass
the fresh-charge flow fixed by the volumetric efficiency (the isentropic
throat chokes near 0.463 kg/s, the equation window requires 0.505 kg/s); the
author's commented area 0.004601 m² is used. The statement asks for curves against
discharge pressure and speed; the window is the one test point, and the file
contains no parametric table.

`gamma` = 1.4 is the provisional value left active. The leakage-nozzle
relation converts Celsius with `+273`. Property calls use `Air`.

No CoolSolve language feature is missing. `missing_features` is empty.
`max()` and the property calls are accepted. From the default guesses the
mixture block (7 variables) needs **Try Harder**; the shipped `.initials`
avoid it. CoolSolve note: the `.sol` labels the specific volumes `v_*` from
`VOLUME()` with `kg/m^3` (registered as `CS-BUG-UNIT-VOLUME`).

## Related models

No library model is this calculation.

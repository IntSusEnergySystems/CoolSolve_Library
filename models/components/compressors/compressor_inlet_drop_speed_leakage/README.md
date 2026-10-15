# Compressor with inlet pressure drop and speed-dependent leakage (exercise)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0217`

Teaching exercise for a positive-displacement air compressor. Equivalent nozzles
stand for the inlet pressure drop and the internal leakage. The throat areas and
the swept volume are the characteristics taken from the first part of the
exercise. Efficiency and the leakage ratio are results: they vary with
rotational speed. The stored point is 6000 rpm.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 51 equations (largest block: 27) |
| **Source** | thermo_models, file `R3 - SB - Ex 2 - 2.EES` |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified (see *Verification*) |

## Problem statement

Continuation of MSTh repetition 3, exercise 2. The equation window is headed
"MSTh - SB". The compressor characteristics determined in the first part are
the inlet throat area, the leakage throat area and the swept volume.

The fresh charge is air at 20 °C and 1 bar. The discharge pressure is 4 bar.
The lines `rpm = 3000`, `epsilon_s = 0.75` and `M_dot = 1` are comments, as is
`M_dot_l = 0.1*M_dot`. The text says that the efficiency and the ratio of the
leakage flow to the fresh-charge flow vary with rotational speed, and that the
hypothesis on `M_dot` is removed. The stored solution is the point at
6000 rpm.

The file stores no parametric table. A closing comment says that the inlet
pressure drop grows with speed while the effect of the internal leak falls, so
that an optimum can be determined. That optimum is not a result of this file.

## Model

The fluid name in the property calls is `Air`. CoolSolve warns that moist air
would be `AirH2O`. The exercise is dry air, and the fluid is left as `Air`.

- Swept volume `V_s` = 0.02306 m³. Inlet throat area `A_thr_su` = 0.00578 m².
  Leakage throat area `A_thr_leak` = 0.0001368 m². Suction state `T_su` = 20 °C,
  `P_su` = 1×10⁵ Pa. Discharge pressure `P_ex` = 4×10⁵ Pa. Rotational speed
  `rpm` = 6000, so `N` = `rpm`/60.
- Overall isentropic efficiency `epsilon_s` = `w_s`/`w`, with
  `w_s` = `h_ex_s` − `h_su` along the isentropic path from the fresh charge to
  `P_ex`. Shaft power from the fresh charge is `W_dot` = `M_dot`·`w`.
- Inlet nozzle, isentropic from the fresh charge.
  `P_thr` = max(`P_su_1`, `P_crit`). `gamma` is not fixed: the commented
  provisional value 1.4 is not an equation, and `gamma` comes from the
  isentropic temperature–pressure relation written with `+273`.
- The fresh-charge flow is `M_dot` = `C_thr`·`A_thr_su`/`v_thr_su`. The throat
  kinetic energy is `C_thr`²/2 = `h_su` − `h_thr`, so the velocity has two
  roots. The shipped `.initials` keep the stored positive speed.
- Internal compression is isentropic from the mixed inlet (`h_su_2`, `P_su_2`)
  to `P_ex`. The same shaft power is `W_dot` = `M_dot_in`·(`h_ex_2` − `h_su_2`).
  Displacement fixes `V_dot_su_2` = `N`·`V_s` = `M_dot_in`·`v_su_2`.
- Mixing is isobaric: `P_su_2` = `P_su_1`. The original states that the leak
  does not set the compressor inlet pressure, only the inlet pressure drop does.
  `M_dot_in` = `M_dot_l` + `M_dot`, and
  `h_su_1`·`M_dot` + `h_ex_2`·`M_dot_l` = `M_dot_in`·`h_su_2`.
- Leakage nozzle. `P_thr_l` = max(`P_su_1`, `P_crit_l`). `gamma_l` is solved
  from the isentropic relation written in the equation window, which uses the
  pressure ratio `P_thr`/`P_ex` and `+273`. The commented provisional value
  `gamma_l` = 1.4 is not an equation.
- `delta_w_1` is the specific-work effect of the leak and `delta_w_2` that of
  the inlet pressure drop, as named in the original.

At the stored point the inlet throat is not choked (`P_su_1` > `P_crit`, so
`P_thr` = `P_su_1`) and the leakage throat is choked (`P_crit_l` > `P_su_1`, so
`P_thr_l` = `P_crit_l`).

The original comments, and does not solve, the closures without leakage
(`M_dot` = `M_dot_in` and `h_su_1` = `h_su_2`). It also comments numerical
results of another point (`P_su_1` = 84994 Pa, `T_su_2` = 37.22 °C). Those
numbers match the stored guesses, not the stored solution at 6000 rpm.

## How to run

The CLI loads the sibling `.initials` and `coolsolve.conf`:

```bash
../CoolSolve/build/coolsolve ./compressor_inlet_drop_speed_leakage.eescode
```

`coolsolve.conf` sets `solverPipeline = Newton, TrustRegion`. From the stored
guesses, Newton reports `SingularJacobian` on the 27-equation block and
TrustRegion then converges. The run reports 23 iterations.

`C_thr` and `C_thr_l` are defined by squared velocities. The `.initials` are
the stored solution, including the positive speeds (`C_thr` = 299.82 m/s,
`C_thr_l` = 390.44 m/s) and the positive diameter. Without `.initials`, Newton
is `SingularJacobian` and TrustRegion stops at its limit of 500 iterations
(residual stays 4.194×10⁵). There is no second shipped root.

No diagram-state arrays: the fluid is ideal-gas `Air`.

## Results

Stored point at 6000 rpm. CoolSolve values are from the `.sol` baseline.

| Quantity | CoolSolve | EES stored | rel. diff. |
|---|---:|---:|---:|
| `rpm` [rpm] | 6000 | 6000 | 0 |
| `N` [1/s] | 100 | 100 | 0 |
| `M_dot` [kg/s] | 1.361191 | 1.361137 | 3.97e-05 |
| `M_dot_l` [kg/s] | 0.0943395 | 0.0942575 | 8.69e-04 |
| `M_dot_in` [kg/s] | 1.455530 | 1.455394 | 9.34e-05 |
| `W_dot` [W] | 340193 | 340017 | 5.19e-04 |
| `w` [J/kg] | 249923 | 249803 | 4.80e-04 |
| `w_s` [J/kg] | 143113 | 143028 | 5.93e-04 |
| `epsilon_s` [-] | 0.572626 | 0.572561 | 1.13e-04 |
| `C_thr` [m/s] | 299.756 | 299.818 | 2.07e-04 |
| `C_thr_l` [m/s] | 390.822 | 390.441 | 9.74e-04 |
| `P_su_1`, `P_thr` [Pa] | 56005.4 | 56016.5 | 1.98e-04 |
| `P_crit` [Pa] | 52840.4 | 52835.3 | 9.63e-05 |
| `P_thr_l`, `P_crit_l` [Pa] | 235439 | 235445 | 2.17e-05 |
| `T_su_2` [°C] | 36.095 | 36.071 | 6.82e-04 |
| `T_ex_2` [°C] | 265.482 | 265.787 | 1.15e-03 |
| `T_thr` [°C] | −24.672 | −24.680 | 3.32e-04 |
| `T_thr_l` [°C] | 191.357 | 191.674 | 1.65e-03 |
| `gamma` [-] | 1.39928 | 1.39958 | 2.16e-04 |
| `gamma_l` [-] | 1.08147 | 1.08141 | 5.55e-05 |
| `DELTAP_su` [Pa] | 43994.6 | 43983.5 | 2.52e-04 |
| `delta_w_1` [J/kg] | 16198.6 | 16178.3 | 1.25e-03 |
| `delta_w_2` [J/kg] | 37007.0 | 37008.9 | 4.96e-05 |

`P_su_1` > `P_crit` and `P_thr_l` = `P_crit_l` > `P_su_1`, so the inlet throat
is not choked and the leakage throat is choked.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot
     (ideal-gas Air; no T-s diagram yet), e.g.  ![Shaft power against speed](figures/compressor_inlet_drop_speed_leakage_wdot.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R3 - SB - Ex 2 - 2.EES` (EES X7.458, 51
variables), compared with `compare_solution.py` without `--ees-units`. The
unit system of the file is already `SI MASS DEG PA C J`. The tool's summary
line is:

`51 common variables, 13 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1`

The maximum relative difference over the common variables is 3.36e-01 on
`h_thr` (unrounded 0.33617243636). The one name present only in CoolSolve is
`PI`, the built-in constant.

Absolute `Air` enthalpy (CoolSolve minus EES) is about +126 kJ/kg and is not
constant:

| Variable | Offset [J/kg] |
|---|---:|
| `h_su`, `h_su_1` | +125871 |
| `h_thr` | +125889 |
| `h_su_2` | +125891 |
| `h_ex_s` | +125955 |
| `h_ex_2` | +125990 |
| `h_thr_l` | +125842 |

Entropy (CoolSolve minus EES) is −1814.87 J/kg·K on `s_su`, −1814.77 J/kg·K on
`s_su_2` and −1814.96 J/kg·K on `s_ex_2`.

The offset cancels in the work difference. Isentropic specific work `w_s` is
143113 J/kg against 143028 J/kg (residual 85 J/kg, rel 5.93e-04). Shaft power
is 340193 W against 340017 W (rel 5.19e-04). Fresh-charge mass flow is
1.361191 kg/s against 1.361137 kg/s (rel 3.97e-05). Speeds stay on the stored
positive root: `C_thr` 299.756 m/s against 299.818 m/s, `C_thr_l` 390.822 m/s
against 390.441 m/s, `rpm` = 6000 and `N` = 100 in both.

`delta_w_1` (1.25e-03), `T_ex_2` (1.15e-03) and `T_thr_l` (1.65e-03) are the
other three variables above `rtol` 0.001. They are the same CoolProp-versus-EES
residual of a few parts per thousand. Specific volume `v_su` agrees within
3.01e-04. The `.sol` labels on `v_su`, `v_su_2`, `v_thr_su` and `v_thr_l` say
kg/m³; the numbers are the specific volumes returned by `volume()`.

With the stored `.initials`, the CLI reports success in 23 iterations. Block 12
is Newton then TrustRegion (19 iterations on that block). Without `.initials`,
Newton reports `SingularJacobian` and TrustRegion reaches 500 iterations with
the residual still 4.194×10⁵. No `.sol` is produced in that case.

## Source and attribution

The equation-window header is "MSTh - SB". `docs/model_workflow.md` maps SB to
Stéphane Bertagnolio. The `{$ID$}` stamp is the Laboratoire de Thermodynamique,
Université de Liège, and is not the author.

Source file (EES X7.458, French comments, not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 03/R3 - SB - Ex 2 - 2.EES`
(inventory `TM-0048`, duplicate group DG-0011, representative).

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R3 - SB - Ex 2 - 2.EES` (EES X7.458, plain text, 51 variables, no lookup or parametric table, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already Pa, °C and J, so nothing was rescaled. `$UnitSystem` was deleted. The file has no `$TABSTOPS` and no `$Export`. Comments translated to English. No D10–D14 rewrite (no `MODULE`/`SUBPROGRAM`, no unsupported property pair, no `$COMMON`, no string array). No variant. `missing_features` is empty.
- **2026-10-15 — square system**: with only `$UnitSystem` removed, CoolSolve reports 50 equations, 51 unknowns, `System square: No`. The unmatched unknown is `rpm` (it appears only in `N = rpm/60`). The line `rpm = 3000` is a comment and was not turned into an equation, nor were `epsilon_s = 0.75`, `M_dot = 1`, `M_dot_l = 0.1*M_dot`, `gamma = 1.4` or `gamma_l = 1.4`. The added equation is `rpm = 6000`, the stored value (guess 3000). The system is then square: 51 equations, 51 variables, largest block 27. No stored unknown replaced an equation. `.initials` are the stored solution, including the positive speeds.
- **Level**: equations 51 → 1 (50–300); largest block 27 → 1 (6–30); no procedure, array or `DUPLICATE` → 0; one compressor, the two nozzles are parts of that machine → 0; identified throat areas, and efficiency and the leakage ratio are results of the speed → 1; the 27-equation block needs the stored `.initials` and `solverPipeline = Newton, TrustRegion` → 1. Score 4 → level 3. No pedagogical ±1.

## Limitations and CoolSolve gaps

Ideal-gas `Air`. The enthalpy reference differs from EES by about +126 kJ/kg
and is not constant; entropy differs by about −1815 J/kg·K. The kelvin
conversion in the isentropic relations is `+273`, as written. `gamma_l` is
solved from `P_thr`/`P_ex`, as written, and is about 1.08 at this point.
One speed is stored; the optimum mentioned in the closing comment is not
computed. No CoolSolve gap blocks the file. `missing_features` is empty.

## Related models

None. `related` is empty.

# Teaching exercise: optimal diameter and speed of a turbomachine

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0235`

Teaching exercise on the optimal diameter and rotation speed of a turbomachine. The flow factor and the enthalpy factor are given. The model computes the diameter and the speed that realise those two factors for air drawn at 1 bar and 20 °C, 6000 m³/h, and discharged at 2.5 bar.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 17 equations (largest block: 1) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 4, exercise 6 (EES file `MSTh-SB-R4-Ex6.EES`) |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

The equation window is titled "MSTh - SB - R4 - Exercice 6". It does not add a prose statement. The given data and the two section labels are the exercise.

Air is drawn at `P_su = 1E5` Pa and `T_su = 20` °C, with `V_dot_su = 6000/3600` m³/s (6000 m³/h), and discharged at `P_ex = 2.5E5` Pa. The flow factor is `Phi = 0.3` and the enthalpy factor is `Psi = 1.4`. The window asks for the optimal diameter and the optimal rotation speed.

## Model

Both factors are written twice, once as the given number and once from the machine velocities. The isentropic enthalpy difference uses ideal-gas `Air` at the Celsius temperature `T_su`:

\[
\Phi = 0.3 = \frac{C_{su}}{U}, \quad
C_{su} = \frac{\dot V_{su}}{A_{su}}, \quad
A_{su} = \frac{\pi D^{2}}{4}, \quad
U = \pi D N
\]

\[
\Psi = 1.4 = \frac{2\,\Delta h_{s}}{U^{2}}, \quad
\Delta h_{s} = h_{3s} - h_{1}
\]

\[
h_{3s} = h(\mathrm{Air}, s = s_{su}, P = P_{ex}), \quad
s_{su} = s(\mathrm{Air}, T = T_{su}, P = P_{su}), \quad
h_{1} = h(\mathrm{Air}, T = T_{su})
\]

\[
D_{opt} = D, \quad \mathrm{rpm}_{opt} = 60\,N
\]

`A_su = PI*D^2/4` is even in `D`, so a negative diameter satisfies the same area. The equations are left as written. CoolSolve splits the 17 equations into 17 blocks of one equation. The system is square.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `P_su` | 1×10⁵ Pa | `D_opt` | 0.141193 m |
| `T_su` | 20 °C | `rpm_opt` | 47995.6 rev/min |
| `P_ex` | 2.5×10⁵ Pa | `DELTAh_s` | 88130.0 J/kg |
| `V_dot_su` | 6000/3600 m³/s | `U` | 354.824 m/s |
| `Phi` | 0.3 | `C_su` | 106.447 m/s |
| `Psi` | 1.4 | `N` | 799.927 rev/s |

## How to run

Open `turbomachine_optimal_diameter.eescode` in the CoolSolve GUI and press *Solve*, or from a terminal:

```bash
coolsolve ./turbomachine_optimal_diameter.eescode
```

The system is square (17 equations, 17 variables). CoolSolve reports 12 iterations with the `.initials` file and 47 iterations without it. Without that file the diameter stays positive (`D = 0.141193` m) and the speed stays positive (`rpm_opt = 47995.6` rev/min). The `.initials` file stores the EES solution, including the positive diameter and the positive speed. No `coolsolve.conf` is used.

## Results

Design outputs, reported apart from the absolute enthalpies and the entropy:

| Quantity | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `D_opt` [m] | 0.1412035306 | 0.1411927561 | 7.63e-05 |
| `rpm_opt` [rev/min] | 47984.6805 | 47995.63549 | 2.28e-04 |
| `DELTAh_s` [J/kg] | 88103.19485 | 88129.96729 | 3.04e-04 |
| `D` [m] | 0.1412035306 | 0.1411927561 | 7.63e-05 |
| `N` [rev/s] | 799.7446751 | 799.9272582 | 2.28e-04 |
| `U` [m/s] | 354.7699164 | 354.8238341 | 1.52e-04 |
| `C_su` [m/s] | 106.4309749 | 106.4471502 | 1.52e-04 |
| `A_su` [m²] | 0.01565960161 | 0.01565722204 | 1.52e-04 |

Absolute `Air` properties, which carry the reference state:

| Quantity | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h_1` [J/kg] | 293534.3441 | 419404.9218 | 3.00e-01 |
| `h_3_s` [J/kg] | 381637.5389 | 507534.8890 | 2.48e-01 |
| `s_su` [J/kg-K] | 5682.126158 | 3867.259359 | 3.19e-01 |

`Phi`, `Psi`, `P_su`, `P_ex` and `T_su` agree. `V_dot_su` differs by 2.00e-10.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Compared with the solution stored by EES X7.458 in `MSTh-SB-R4-Ex6.EES` (`tools/compare_solution.py`, `rtol=0.001`, without `--ees-units`). Summary line, quoted as printed:

> 17 common variables, 3 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

The largest relative difference over the 17 common variables is **3.19e-01** (`s_su`). Unrounded, that ratio is 0.3193992439. `h_1` prints **3.00e-01** and `h_3_s` prints **2.48e-01**. Those three are above `rtol=0.001`. Every other common variable is under it.

`h_1` is **+125870.58 J/kg** above the EES value, and `h_3_s` is **+125897.35 J/kg** above it. The offset is about +126 kJ/kg and it is not the same number at the two states. The difference of the two offsets is 26.77 J/kg, which is the difference on `DELTAh_s` (88129.967 J/kg against the stored 88103.195 J/kg, relative difference **3.04e-04**). `D_opt` differs by **7.63e-05** and `rpm_opt` by **2.28e-04**.

The name present only in the CoolSolve solution is `PI`.

With the `.initials` file, CoolSolve reports all 17 equations satisfied (max relative residual 9.1177e-11). The property gaps above are the reference state of ideal-gas `Air`. The equations of the file are satisfied, so the model stays verified.

## Source and attribution

Exercise of the ULiège course *Machines et systèmes thermiques* (repetition 4, exercise 6). The equation window is titled "MSTh - SB - R4 - Exercice 6", and the file name is `MSTh-SB-R4-Ex6.EES`. Those initials are Stéphane Bertagnolio. The EES licence tag names the ULiège Thermodynamics Laboratory, which identifies the licence holder.

Source file (EES X7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/SB/MSTh-SB-R4-Ex6.EES`
(inventory candidate `TM-0068`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): the extract report gives the unit system `$UnitSystem SI MASS DEG PA C J`, so no value was rescaled. `P_su = 1E5`, `P_ex = 2.5E5` and `T_su = 20` stay as written. `V_dot_su = 6000/3600` stays that equation. `$UnitSystem` was deleted. The file contains no `$TABSTOPS` and no `$Export`. The licence tag was removed. Comments were translated to English. No lookup table and no parametric table were decoded. **No equation was changed.**
- **2026-10-15 — square system**: CoolSolve reports `System square: Yes` (17 equations, 17 variables, largest block 1). No stored unknown was added. `Phi = 0.3` is kept beside `Phi = C_su/U`, and `Psi = 1.4` is kept beside `Psi = 2*DELTAh_s/U^2`. The property calls stay `enthalpy(Air, T=T_su)`, `entropy(Air, T=T_su, P=P_su)` and `enthalpy(Air, s=s_su, P=P_ex)`, with no added 273. The fluid stays `Air`. No diagram-state arrays were added.
- **2026-10-15 — `.initials`**: the 17 values stored by EES, with `D = 0.1412035306` m and `N = 799.7446751` rev/s. A run with no initials file also returns that positive diameter and a positive speed (47 iterations, against 12 with the file). Seeding `D`, `U` and `N` at the negative of those stored values was not kept: that run also returned the positive root. `Phi`, `Psi` and `V_dot_su` were not changed.
- **Level 1** (taxonomy.md §3): 17 equations (0) + largest block 1 (0) + no function, procedure, array or `DUPLICATE` (0) + one machine, not three coupled components (0) + one operating point from two given factors, with no calibration, part-load curve or dynamics (0) + the positive diameter is reached from default guesses, with no `coolsolve.conf` (0) = 0 → Introductory.

## Limitations and CoolSolve gaps

- The two factors are imposed. The file computes one diameter and one speed. It does not build a performance map.
- `A_su = PI*D^2/4` is even in `D`. The shipped solution is the positive root stored by EES. A run without initials also returns that positive root.
- The `ENTHALPY(): fluid 'Air'` hint (suggesting `AirH2O` for moist air) is not followed. The fluid stays `Air`.
- `T_su = 20` is the Celsius value of the original. It matches the stored solution and was not changed.
- Absolute `h_1`, `h_3_s` and `s_su` follow the CoolProp reference state of ideal-gas `Air`. The enthalpy offset against EES is about +126 kJ/kg and is not constant, so `DELTAh_s` carries the 26.77 J/kg remainder.
- No registered CoolSolve gap blocks this model (`missing_features` is empty).

## Related models

No other library model was linked before `CSL-0318`.
- `CSL-0318` *cordier_specific_speed*: Cordier line giving the specific diameter from the specific speed, as a pre-design alternative to the given flow and enthalpy factors.

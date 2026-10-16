# Turbo-expander: ideal nozzle and Laval wheel (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0234`

Steady model of one turbo-expander: an ideal nozzle followed by a Laval wheel.
Inlet air is at 1×10⁶ Pa and 850 °C and the exit pressure is 1×10⁵ Pa. The
throat pressure is the greater of the critical pressure and the exit pressure.
The power is specified as 5×10⁶ W. The model computes the mass flow, the
equivalent throat area and the wheel diameter. Teaching exercise, ULiège MSTh,
repetition R4, exercise 2.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Air |
| **Size** | 28 equations (largest block: 5) |
| **Source** | thermo_models, ULiège MSTh, file `R4-Ex2.EES` |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise 2 of repetition R4. The equation window is titled `R4 - Exercice 2`.
It does not contain a separate problem sheet. What it does contain is a
turbo-expander made of an ideal nozzle and a Laval wheel.

Inlet pressure 1×10⁶ Pa, inlet temperature 850 °C, exit pressure 1×10⁵ Pa.
Rotational speed 10000 1/min. Nozzle angle 15°. The power in the equation
window is 5×10⁶ W. `epsilon_s = 0.85` and `eta_mec = 0.98`. The commented
value `gamma = 1.4` is labelled as a first approximation. The next equation
is the exact temperature ratio, and that equation solves `gamma`. The
calculation returns the throat state, the two nozzle velocities, the mass
flow, the throat area and the wheel diameter.

## Model

Ideal-gas `Air`, the fluid name in the file. CoolSolve warns that moist air
would be `AirH2O`. The source is dry air, so the fluid stays `Air`. 850 °C
is a valid `Air` temperature.

Total enthalpy is conserved from the inlet to the throat and from the inlet
to the nozzle exit. Specific enthalpy and entropy come from `Air`. The two
steady-flow balances, as written, keep only the kinetic energy:

\[
h_{0,\mathrm{su}} = h_\mathrm{su}
= h_\mathrm{thr} + \frac{C_\mathrm{thr}^{2}}{2}
= h_\mathrm{exn} + \frac{C_\mathrm{exn}^{2}}{2}
\]

`C_thr` and `C_exn` enter as squares. The positive roots are the stored
ones. Property calls keep the original Celsius arguments:
`enthalpy(Air, T=T_su)`, `entropy(Air, T=T_su, P=P_su)` and
`temperature(Air, h=h_thr)`. `temperature` returns °C.

The throat pressure follows the choked-flow test in the file. The window
writes both `P_thr` and `p_thr`, and both `P_ex` and `p_ex`. EES is
case-insensitive, and CoolSolve treats each pair as one variable. The
converted window is square with both spellings left as written:

\[
\frac{p_\mathrm{thrmin}}{P_\mathrm{su}}
= \left(\frac{2}{\gamma+1}\right)^{\gamma/(\gamma-1)},
\qquad
p_\mathrm{thr} = \max(p_\mathrm{ex}, p_\mathrm{thrmin})
\]

At the solved point \(p_\mathrm{thrmin} > p_\mathrm{ex}\), so the throat is
choked and \(p_\mathrm{thr} = p_\mathrm{thrmin}\).

`gamma` is not assigned. The comment `gamma=1.4` stays a comment. The exact
ratio, as written, solves it:

\[
\frac{T_\mathrm{thr}+273}{T_\mathrm{su}+273}
= \left(\frac{P_\mathrm{thr}}{P_\mathrm{su}}\right)^{(\gamma-1)/\gamma}
\]

The `+273` is the original conversion inside that ratio. `T_su` is not
rewritten in kelvin.

The Laval wheel and the power balance, as written:

\[
\eta_\mathrm{laval}
= 4\,\frac{U}{C_\mathrm{exn}}
\left(\cos\alpha - \frac{U}{C_\mathrm{exn}}\right),
\qquad
U = \pi\, D\, N,
\qquad
\dot W = \dot m\, \eta_\mathrm{laval}\, C_\mathrm{exn}^{2}/2
\]

\(\alpha = 15\) is in degrees. \(\eta_\mathrm{laval}\) is fixed by
`epsilon_s = eta_mec*eta_laval`. The wheel formula then returns `U` and `D`.
The balance returns `M_dot` because `W_dot` is specified. `A_thr` follows
from `C_thr = M_dot*v_thr/A_thr`.

| Input | Value |
|---|---|
| `rpm` | 10000 1/min |
| `T_su` | 850 °C |
| `P_su` | 1×10⁶ Pa |
| `P_ex` | 1×10⁵ Pa |
| `epsilon_s` | 0.85 |
| `eta_mec` | 0.98 |
| `W_dot` | 5×10⁶ W |
| `alpha` | 15° |

No diagram-state arrays are added. The equation window has none, and the
fluid is ideal-gas air.

## How to run

```bash
coolsolve ./turboexpander_ideal_nozzle_laval.eescode
```

CoolSolve reports 29 iterations with the shipped `.initials` and returns the
positive speeds. Without `.initials` the 5-variable throat block is singular
at the default `gamma = 1` (`SingularJacobian`, initial residual 999999) and
does not converge. Starting from the stored speeds with the signs of
`C_thr`, `C_exn` and `U` reversed still returns the positive speeds
(34 iterations). The `.initials` file is the EES stored solution, including
those positive speeds and the stored `gamma`. The enthalpy guesses sit about
126 kJ/kg below the CoolSolve enthalpies because of the Air reference state.

`cos` uses degrees. There is no `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. |
|---|---:|---:|---:|
| `eta_laval` [-] | 0.8673469388 | 0.8673469388 | 0 |
| `M_dot` [kg/s] | 10.260073 | 9.238093 | 9.96e-02 |
| `D` [m] | 0.718386 | 0.706010 | 1.72e-02 |
| `C_exn` [m/s] | 1060.055 | 1041.794 | 1.72e-02 |
| `C_thr` [m/s] | 606.724 | 607.116 | 6.47e-04 |
| `U` [m/s] | 376.146 | 369.666 | 1.72e-02 |
| `A_thr` [m²] | 0.00867303 | 0.008655 | 2.08e-03 |
| `P_thr` [Pa] | 539859.93 | 485745.90 | 1.00e-01 |
| `p_thrmin` [Pa] | 539859.93 | 485745.90 | 1.00e-01 |
| `gamma` [-] | 1.332853 | 1.333659 | 6.04e-04 |
| `T_thr` [°C] | 689.770 | 689.437 | 4.82e-04 |
| `W_dot` [W] | 5000000 | 4348190.39 | 1.30e-01 |
| `P_su` [Pa] | 1000000 | 900000 | 1.00e-01 |
| `h_su` [J/kg] | 1314398.06 | 1187845.42 | 9.63e-02 |
| `h_thr` [J/kg] | 1130341.15 | 1003550.27 | 1.12e-01 |
| `h_exn` [J/kg] | 752539.87 | 645178.47 | 1.43e-01 |
| `s_su` [J/kg-K] | 4629.723 | 6473.780 | 2.85e-01 |
| `v_thr` [m³/kg] | 0.512875 | 0.568796 | 9.83e-02 |

The throat is choked: `P_thr = p_thrmin = 539859.93` Pa, above
`P_ex = 100000` Pa. The speeds in this solution are positive:
`C_thr = 606.724` m/s, `C_exn = 1060.055` m/s, `U = 376.146` m/s.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R4-Ex2.EES` (EES X7.458). The unit system
is already `SI MASS DEG PA C J`, so `compare_solution.py` was run without
`--ees-units`. The tool's summary line is:

`28 common variables, 17 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1`

The maximum relative difference over all 28 common variables, as printed in
the tool's table, is 2.85e-01 on `s_su`. The exact ratio is
0.2848500975169177. That value is `verification.max_rel_diff`.

The name present only in CoolSolve is `PI`, the built-in constant in
`U = PI*D*N`. The statistics are 28 equations and 28 variables, so `PI` is
not an extra unknown.

All 28 equations are satisfied (max relative residual 2.40e-11 on the solve
with `.initials`). Seventeen common variables are above rtol 0.001.

**The stored solution is an earlier operating point.** Its `P_su` is
900000 Pa and its `W_dot` is 4348190.393 W. The equation window, which is
the system that was solved, has `P_su = 1000000` and `W_dot = 5E6`. The
variable-info guesses of those two names are 1000000 and 5000000. Neither
pressure, nor `T_su`, nor the efficiencies, nor `W_dot` was changed to chase
the stored root. `P_su`, `W_dot`, `P_thr` and `p_thrmin` differ for that
reason. The exact relative differences are 0.1000000000 on `P_su` and
0.1002371686 on `P_thr` and on `p_thrmin`. `gamma` still agrees (6.04e-04).

**`eta_laval`, `M_dot` and `D`, separate from the absolute enthalpies.**

- `eta_laval` is 0.8673469388 in both. It is `epsilon_s/eta_mec` =
  0.85/0.98, so the property libraries do not enter it.
- `D` is 0.7183857689 m against 0.7060103283 m (1.72e-02). `U` has the same
  relative difference. With `eta_laval`, `alpha` and `N` the same, `D`
  tracks `C_exn` (also 1.72e-02): 1060.0549 m/s against 1041.7936 m/s.
- `M_dot` is 10.26007265 kg/s against 9.238092977 kg/s (9.96e-02). From
  `W_dot = M_dot*eta_laval*C_exn^2/2` and the same `eta_laval`, the mass-flow
  ratio is the power ratio 5000000/4348190.393 times
  `(1041.793598/1060.054898)^2`.

**Air reference, separate from `M_dot`, `D` and `eta_laval`.** Ideal-gas
`Air` keeps CoolProp's reference. CoolSolve − EES on `h_su` is
+126552.65 J/kg at 850 °C. On `h_thr` it is +126790.88 J/kg. The offset is
not constant. On `h_exn` the difference is +107361.40 J/kg; that state also
uses the stored inlet pressure of 900 kPa, so it is not the same comparison
as `h_su`. CoolSolve − EES on `s_su` is −1844.057 J/kg-K (relative
difference 2.85e-01). This is `verification.max_rel_diff`.

The enthalpy drops, after the reference offset cancels:

| Drop | EES [J/kg] | CoolSolve [J/kg] | CoolSolve − EES [J/kg] |
|---|---:|---:|---:|
| `h_su − h_thr` | 184295.15 | 184056.91 | −238.24 |
| `h_su − h_exn` | 542666.95 | 561858.19 | +19191.24 |

The throat drop differs by 238 J/kg. `C_thr` stays inside rtol 0.001
(6.47e-04), and `T_thr` does too (4.82e-04). The nozzle-exit drop differs
by 19.2 kJ/kg because the stored entropy was evaluated at 900 kPa.

**The other differences** follow from that operating point and from the
property residual. `v_thr` (9.83e-02) is the specific volume
`volume(Air, T=T_thr, P=P_thr)` at the solved throat pressure. `A_thr`
(2.08e-03) is `M_dot*v_thr/C_thr`. The four total enthalpies
`h_0_su`, `h_0_thr`, `h_0_exn` and `h_su` share the inlet offset
+126552.65 J/kg (relative difference 9.63e-02).

## Source and attribution

The equation window names no person. The file is an MSTh repetition,
`R4-Ex2.EES`, and the window title is `R4 - Exercice 2`. No author name is
written in the file, so the authors field is TBD (ULiège MSTh).

The EES licence tag is `{$ID$ #202: Laboratoire de Thermodynamique, U. de Liege}`.
That tag is the laboratory licence, not an author.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/R4-Ex2.EES`.

Candidate TM-0062. Teaching exercise. EES X7.458, plain text, 28 variable
records, no lookup table and no parametric table.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R4-Ex2.EES` (EES X7.458, plain text, 28 variables, no tables, no warnings). Unit settings decode to `$UnitSystem SI MASS DEG PA C J`. The equation window does not contain that directive, nor `$TABSTOPS`, nor `$Export`. The directive inserted by the extractor was deleted. No value was rescaled. `T_su = 850` stays 850 °C. Comments translated to English. Function names lowercased; EES is case-insensitive.
- **Square as converted.** 28 equations, 28 variables, `System square: Yes`, largest block 5. `gamma=1.4` was not turned into an equation. `gamma` is solved by the temperature ratio. `P_thr`/`p_thr` and `P_ex`/`p_ex` were not unified: CoolSolve already treats each pair as one variable, and the system is square with both spellings. No stored unknown was added. No diagram-state arrays were added.
- **Roots.** `C_thr` and `C_exn` are squared in the balances. `.initials` is the stored solution and holds the positive speeds (`C_thr = 607.1163762` m/s, `C_exn = 1041.793598` m/s). With that file, 29 iterations, positive speeds. Without it, `SingularJacobian` on the throat block and no solution. Negated stored speeds, 34 iterations, still the positive speeds.
- **Level**: equations 28 → 0; largest block 5 → 0; no function, procedure, array or `DUPLICATE` → 0; one machine, not discretised and not three or more coupled components → 0; no calibration, off-design or dynamics → 0; the stored guesses are required, because the default `gamma = 1` makes the throat block singular → 1. Score 1 → level 1.

## Limitations and CoolSolve gaps

`gamma = 1.4` is only the commented first approximation. The solved value is
about 1.333. Absolute Air enthalpies and the inlet entropy are not
comparable with EES without the reference offsets above. `eta_laval` matches
the stored value. `M_dot` and `D` also carry the difference between the
equation window (`P_su = 1×10⁶` Pa, `W_dot = 5×10⁶` W) and the stored
solution (`P_su = 9×10⁵` Pa, `W_dot = 4.348×10⁶` W).

The model is one operating point. The throat is choked at that point.

No CoolSolve gap. The equation window has no `$Export` directive.
`missing_features` is empty.

## Related models

No other library model is linked. `related` is empty.

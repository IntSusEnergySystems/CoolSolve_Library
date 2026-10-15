# Turbo-expander: isentropic nozzle and Laval wheel (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0199`

Steady model of one turbo-expander: an ideal isentropic nozzle followed by a
Laval wheel. Inlet air is at 10 bar and 1000 °C and the exit pressure is
1 bar. The throat pressure is the greater of the critical pressure and the
exit pressure. With the equivalent throat area set to 0.001 m², the model
computes the mass flow and the wheel power. Teaching exercise, ULiège MSTh,
repetition R4, exercise 1.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Air |
| **Size** | 27 equations (largest block: 1) |
| **Source** | thermo_models, ULiège MSTh, file `MSTh-SB-R4-Ex1.EES` |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@f5b79cd — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise 1 of repetition R4. The equation window is the SB solution of that
exercise. It does not contain a separate problem sheet. What it does contain
is a turbo-expander made of an ideal isentropic nozzle and a Laval wheel.

Inlet pressure 10×10⁵ Pa, inlet temperature 1000 °C, exit pressure 1×10⁵ Pa.
The wheel diameter is 1 m and the nozzle angle is 15°. The ratio of specific
heats used for the critical pressure is the provisional value 1.4. The
equivalent throat area is 0.001 m². The rotational speed stored with the
solution is 20000 1/min. The nozzle is fully isentropic (`epsilon_n_s = 1`) and `eta_m = 1`.
The calculation returns the throat state, the exit velocity and the wheel
power. There is no second stage.

## Model

Ideal-gas `Air`, the fluid name in the file. CoolSolve warns that moist air
would be `AirH2O`. The source is dry air, so the fluid stays `Air`.

The nozzle expands isentropically from the inlet to the throat and from the
inlet to the exit pressure. Specific enthalpy and entropy come from `Air`.
The two steady-flow balances, as written, keep only the kinetic energy:

\[
h_\mathrm{su} = h_\mathrm{thr} + \frac{C_\mathrm{thr}^{2}}{2}
= h_\mathrm{ex,n,s} + \frac{C_\mathrm{ex,n,s}^{2}}{2}
\]

`C_thr` and `C_ex_n_s` enter as squares. The positive roots are the stored
ones. The throat pressure follows the choked-flow test in the file:

\[
\frac{P_\mathrm{thrmin}}{P_\mathrm{su}}
= \left(\frac{2}{\gamma+1}\right)^{\gamma/(\gamma-1)},
\qquad
P_\mathrm{thr} = \max(P_\mathrm{thrmin}, P_\mathrm{ex})
\]

with \(\gamma = 1.4\). At this point \(P_\mathrm{thrmin} > P_\mathrm{ex}\),
so the throat is choked and \(P_\mathrm{thr} = P_\mathrm{thrmin}\). The
original note says that an unchoked throat would have
\(P_\mathrm{thr} = P_\mathrm{ex}\), and then
\(h_\mathrm{thr} = h_\mathrm{ex,n,s}\) and
\(C_\mathrm{thr} = C_\mathrm{ex,n,s}\).

The equivalent section is the active hypothesis `A_thr = 0.001` m²:

\[
\dot V_\mathrm{thr} = A_\mathrm{thr}\, C_\mathrm{thr},
\qquad
\dot m = \dot V_\mathrm{thr} / v_\mathrm{thr}
\]

The source comments an alternative `M_dot = 1` (relative values). That line
is not an equation and is not used.

The Laval wheel, as written:

\[
\eta_\mathrm{laval}
= 4\,\frac{U}{C_\mathrm{ex,n}}
\left(\cos\alpha - \frac{U}{C_\mathrm{ex,n}}\right),
\qquad
U = \pi\, d_\mathrm{laval}\, N,
\qquad
N = \mathrm{rpm}/60
\]

\(\alpha = 15\) is in degrees (`$UnitSystem` … `DEG` in the source).
\(\varepsilon_{n,s} = C_\mathrm{ex,n}^{2}/C_\mathrm{ex,n,s}^{2} = 1\), so
the nozzle is fully isentropic and the positive exit velocity equals
\(C_\mathrm{ex,n,s}\). The power and the internal isentropic efficiency are

\[
\dot W_\mathrm{in}
= \dot m\, \eta_\mathrm{laval}\, \eta_m\, C_\mathrm{ex,n}^{2}/2,
\qquad
\varepsilon_{s,\mathrm{in}}
= \varepsilon_{n,s}\, \eta_\mathrm{laval}\, \eta_m
\]

with \(\eta_m = 1\).

| Input | Value |
|---|---|
| `P_su` | 10×10⁵ Pa |
| `T_su` | 1000 °C |
| `P_ex` | 1×10⁵ Pa |
| `d_laval` | 1 m |
| `alpha` | 15° |
| `gamma` | 1.4 |
| `A_thr` | 0.001 m² |
| `rpm` | 20000 1/min (Diagram-window value) |
| `epsilon_n_s` | 1 |
| `eta_m` | 1 |

Without `rpm` the equation window is 26 equations and 27 unknowns. `rpm` is
the only variable whose information record carries a different input mark,
its stored value is 20000 and its guess is 1, and the equation window only
comments a provisional `rpm = 3000`. That stored value is restored as an
equation. No computed unknown is replaced by a stored number. The commented
throat-temperature lines are not restored: `T_thr` has no stored value.
No diagram state arrays are added: the equation window has none.

## How to run

```bash
coolsolve ./turboexpander_laval_wheel.eescode
```

CoolSolve reports 10 iterations with the shipped `.initials` and 25
iterations without them. Both runs return the same positive velocities.
Starting from the stored velocities with the signs reversed also returns
that root (13 iterations). The `.initials` file is the EES stored solution,
including those positive roots. The enthalpy guesses sit about 126 kJ/kg
below the CoolSolve enthalpies because of the Air reference state; they are
still the guesses that select the stored root.

`cos` uses degrees. There is no `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. |
|---|---:|---:|---:|
| `P_thr` [Pa] | 528281.79 | 528281.79 | 3.26e-11 |
| `P_thrmin` [Pa] | 528281.79 | 528281.79 | 3.26e-11 |
| `C_thr` [m/s] | 656.821 | 657.145 | 4.92e-04 |
| `C_ex_n` [m/s] | 1131.687 | 1131.461 | 2.00e-04 |
| `M_dot` [kg/s] | 1.10853 | 1.11100 | 2.22e-03 |
| `v_thr` [m³/kg] | 0.592515 | 0.591488 | 1.73e-03 |
| `U` [m/s] | 1047.198 | 1047.198 | 1.88e-10 |
| `eta_laval` [-] | 0.150215 | 0.149562 | 4.35e-03 |
| `epsilon_s_in` [-] | 0.150215 | 0.149562 | 4.35e-03 |
| `W_dot_in` [W] | 106631.32 | 106361.55 | 2.53e-03 |
| `h_su` [J/kg] | 1490503.20 | 1363780.77 | 8.50e-02 |
| `h_thr` [J/kg] | 1274796.20 | 1147861.25 | 9.96e-02 |
| `h_ex_n_s` [J/kg] | 850145.51 | 723677.82 | 1.49e-01 |
| `s_su` [J/kg-K] | 4776.935 | 6590.541 | 2.75e-01 |

The throat is choked: `P_thr = P_thrmin = 528281.79` Pa, above
`P_ex = 100000` Pa. Because `epsilon_n_s = 1`, the exit velocity equals the
isentropic nozzle-exit velocity, 1131.687 m/s in CoolSolve and 1131.461 m/s
in EES. The wheel power is 106631 W against 106362 W.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `MSTh-SB-R4-Ex1.EES` (EES X7.458). The
unit system is already `SI MASS DEG PA C J`, so `compare_solution.py` was
run without `--ees-units`. The tool's summary line is:

`27 common variables, 9 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1`

The maximum relative difference over all 27 common variables, as printed in
the tool's table, is 2.75e-01 on `s_su`. The exact ratio is 0.2751831696.
That value is `verification.max_rel_diff`.

The name present only in CoolSolve is `pi`, the built-in constant in
`U = pi*d_laval*N`. The statistics are 27 equations and 27 variables, so
`pi` is not an extra unknown. `T_thr` appears in the EES variable list with
an empty stored value (the temperature equations are comments). The tool
does not count it: only in EES is 0.

Nine common variables are above rtol 0.001.

**Air reference, separate from the power, the pressures and the velocities.**
Ideal-gas `Air` keeps CoolProp's reference. EES sets the enthalpy to 0 at
0 K. CoolSolve − EES is +126722.42 J/kg on `h_su` (1000 °C), +126934.95 J/kg
on `h_thr` and +126467.69 J/kg on `h_ex_n_s`, about +126.5 to +126.9 kJ/kg.
CoolSolve `docs/ees_import.md` quotes EES − CoolSolve = −126 kJ/kg on `h`
and +1815 J/kg-K on `s`. Here CoolSolve − EES on `s_su` is −1813.606 J/kg-K
(relative difference 2.75e-01). The enthalpy offset is not the same at the
three temperatures: it changes by +212.53 J/kg from the inlet to the throat
and by −254.73 J/kg from the inlet to the isentropic exit. That residual is
a difference of \(c_p(T)\) between EES and CoolProp. It is what remains in
the kinetic energies after the reference offset cancels:

| Drop | EES [J/kg] | CoolSolve [J/kg] | CoolSolve − EES [J/kg] |
|---|---:|---:|---:|
| `h_su − h_thr` | 215919.52 | 215707.00 | −212.53 |
| `h_su − h_ex_n_s` | 640102.95 | 640357.69 | +254.73 |

**Pressures.** `P_thr` and `P_thrmin` agree with the stored solution
(relative difference 3.26e-11). The throat is choked in both.

**Velocities**, from those drops. Both are under rtol 0.001:
`C_thr` 656.821 m/s against 657.145 m/s (4.92e-04), `C_ex_n` 1131.687 m/s
against 1131.461 m/s (2.00e-04). `U` agrees (1.88e-10).

**The other five differences** follow from that residual, not from the
126 kJ/kg offset:

- `v_thr` (1.73e-03). Specific volume at the isentropic throat from
  `volume(Air, h=h_thr, P=P_thr)`. Each library evaluates this at its own
  enthalpy, so the reference offset does not shift the volume. The residual
  is the property difference at that state.
- `M_dot` (2.22e-03). `A_thr*C_thr/v_thr` with `A_thr` fixed. `C_thr` is
  0.049 % low and `v_thr` is 0.173 % high.
- `eta_laval` and `epsilon_s_in` (4.35e-03). They are equal because
  `epsilon_n_s = 1` and `eta_m = 1`. `U/C_ex_n` moves only with `C_ex_n`.
  The factor \(\cos 15° - U/C\) is about 0.040, so the relative difference
  2.00e-04 on `C_ex_n` becomes 4.35e-03 on `eta_laval`.
- `W_dot_in` (2.53e-03): 106631.32 W against 106361.55 W.
  `M_dot` is 0.222 % low, `eta_laval` is 0.435 % high and `C_ex_n²` is
  0.040 % high.

## Source and attribution

The equation window names no person. The file name is `MSTh-SB-R4-Ex1.EES`,
so the filename marks an SB solution. The inventory attributes the ULiège
MSTh course to J. Lebrun, V. Lemort and S. Bertagnolio. Neither that course
line nor the letters SB are written as a person's name in the file, so the
authors field is TBD (ULiège MSTh).

The EES licence tag is `{$ID$ #202: Laboratoire de Thermodynamique, U. de Liege}`.
That tag is the laboratory licence, not an author.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/SB/MSTh-SB-R4-Ex1.EES`.

Candidate TM-0063. Teaching exercise, not an exam. EES X7.458, plain text,
28 variable records, no lookup table and no parametric table.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `MSTh-SB-R4-Ex1.EES` (EES X7.458, plain text, 28 variables, no tables, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already SI, deleted with the licence tag. No `$Export`, `concat$` or `EESFILEDIR$`. Comments translated to English. No value was rescaled.
- **Not square without the wheel speed.** The equation window has 26 equations and 27 unknowns (`System square: No`). The missing assignment is `rpm`. Its variable-information flag differs from the other variables, the stored value is 20000 and the guess is 1, and the only equation-window line is the comment `rpm = 3000` ("hypothèse provisoire"). Restored `rpm = 20000` from that stored Diagram-window value. The system is then square: 27 equations, 27 variables, largest block 1.
- **Not restored.** The throat-temperature equations are comments (`T_thr` has no stored value). The alternative `M_dot = 1` (relative values) is a comment; the active hypothesis `A_thr = 0.001` is kept. No computed unknown was replaced by a stored value. No diagram state arrays were added.
- **Fluid**: `Air` left as `Air`. The moist-air hint is not applied.
- **Roots.** `C_thr` and `C_ex_n_s` are squared in the balances. `.initials` is the stored solution and holds the positive roots. A solve with no initials (25 iterations) and a solve started from the negated velocities (13 iterations) both return that same root. With `.initials`, 10 iterations.
- **Level**: equations 27 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one machine, not discretised and not three or more coupled components → 0; no calibration, off-design or dynamics → 0; converges with and without `.initials`, no `coolsolve.conf` → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

`gamma = 1.4` is the provisional value used only for the critical pressure.
The enthalpies and the entropy use ideal-gas `Air`, so \(c_p\) is not
constant. Absolute Air enthalpies and the inlet entropy are not comparable
with EES without the reference offsets above. The power, the throat pressure
and the velocities are.

The model is one operating point. The file has no second stage. The
equivalent section is `A_thr = 0.001` m², not the commented relative mass
flow of 1 kg/s.

No CoolSolve gap. `missing_features` is empty.

## Related models

`CSL-0174` (steam turbine with isentropic efficiency), `CSL-0182`
(geothermal steam turbine) and `CSL-0189` (R134a turbine power) were read.
They are steam or R134a turbines closed by an isentropic efficiency. They
do not use this nozzle-plus-Laval-wheel calculation, so `related` is empty.

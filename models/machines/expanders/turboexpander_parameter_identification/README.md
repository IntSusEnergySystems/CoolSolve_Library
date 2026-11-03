# Turbo-expander parameter identification from new data (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0207`

Steady model of one turbo-expander: an ideal isentropic nozzle followed by a
Laval wheel. The equivalent throat area and the wheel diameter are the
parameters identified from the additional expander data. At the new inlet
state the model returns the throat state, the wheel efficiency and the shaft
power. Teaching exercise, ULiège MSTh, repetition R4, exercise 2 continued.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Air |
| **Size** | 30 equations (largest block: 5) |
| **Source** | thermo_models, ULiège MSTh, file `MSTh-SB-R4-Ex2-2.EES` |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@5a522f7 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise 2 continued of repetition R4. The equation window is the SB solution
of that exercise. It does not contain a separate problem sheet. The opening
comment says the parameters identified are the equivalent throat area and the
Laval-wheel diameter.

Inlet temperature 850 °C, exit pressure 1×10⁵ Pa. The equation window assigns
the inlet pressure as 9×10⁵ Pa. A display text `10E5` is written immediately
before that value; CoolSolve reads the value, 9×10⁵ Pa. The nozzle angle is
15° and the rotational speed is 10000 1/min. The mechanical efficiency is
0.98. The nozzle is fully isentropic (`epsilon_n_s = 1`).

The identified values written in the solution are `A_thr = 0.008831` m² and
`d_laval = 0.7182` m. The source comments a target `epsilon_s_global = 0.85`
and a target `W_dot = 5E6`. Those two lines are comments. The active
equations compute the global efficiency and the shaft power. A provisional
`gamma = 1.4` is also a comment. `gamma` is an unknown of the isentropic
temperature-pressure relation. That relation uses `+273`, as written.

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

`C_thr`, `C_ex_n_s` and `C_ex_n` enter as squares. The positive roots are the
stored ones. The throat pressure follows the choked-flow test in the file:

\[
\frac{P_\mathrm{thrmin}}{P_\mathrm{su}}
= \left(\frac{2}{\gamma+1}\right)^{\gamma/(\gamma-1)},
\qquad
P_\mathrm{thr} = \max(P_\mathrm{thrmin}, P_\mathrm{ex})
\]

`gamma` is fixed by the isentropic relation written in the file, together
with the throat temperature from the enthalpy:

\[
\frac{T_\mathrm{thr}+273}{T_\mathrm{su}+273}
= \left(\frac{P_\mathrm{thr}}{P_\mathrm{su}}\right)^{(\gamma-1)/\gamma},
\qquad
T_\mathrm{thr} = T(h_\mathrm{thr})
\]

At this point \(P_\mathrm{thrmin} > P_\mathrm{ex}\), so the throat is choked
and \(P_\mathrm{thr} = P_\mathrm{thrmin}\). The original note says that an
unchoked throat would have \(P_\mathrm{thr} = P_\mathrm{ex}\), and then
\(h_\mathrm{thr} = h_\mathrm{ex,n,s}\) and \(C_\mathrm{thr} = C_\mathrm{ex,n,s}\).
That note is a comment. The choked solution does not use it.

The equivalent section is the identified value `A_thr = 0.008831` m²:

\[
\dot V_\mathrm{thr} = A_\mathrm{thr}\, C_\mathrm{thr},
\qquad
\dot m = \dot V_\mathrm{thr} / v_\mathrm{thr}
\]

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
\(C_\mathrm{ex,n,s}\). The internal power, the shaft power and the internal
isentropic efficiency are

\[
\dot W_\mathrm{in}
= \dot m\, \varepsilon_{s,\mathrm{in}}\, C_\mathrm{ex,n,s}^{2}/2,
\qquad
\dot W = \eta_m\, \dot W_\mathrm{in},
\qquad
\varepsilon_{s,\mathrm{in}}
= \varepsilon_{n,s}\, \eta_\mathrm{laval},
\qquad
\varepsilon_{s,\mathrm{global}}
= \varepsilon_{s,\mathrm{in}}\, \eta_m
\]

with \(\eta_m = 0.98\).

| Input | Value |
|---|---|
| `P_su` | 9×10⁵ Pa |
| `T_su` | 850 °C |
| `P_ex` | 1×10⁵ Pa |
| `A_thr` | 0.008831 m² (identified) |
| `d_laval` | 0.7182 m (identified) |
| `alpha` | 15° |
| `rpm` | 10000 1/min |
| `eta_m` | 0.98 |
| `epsilon_n_s` | 1 |

The equation window is square: 30 equations and 30 variables. No
Diagram-window input is added. The commented targets `epsilon_s_global = 0.85`,
`W_dot = 5E6` and `gamma = 1.4` are not restored. No computed unknown is
replaced by a stored number. No diagram state arrays are added: the equation
window has none.

## How to run

```bash
coolsolve ./turboexpander_parameter_identification.eescode
```

CoolSolve reports 14 iterations with the shipped `.initials`. The
`.initials` file is the EES stored solution and holds the positive velocity
roots. A start from those velocities with the signs reversed also returns
the positive root (17 iterations). The enthalpy guesses sit about 126 kJ/kg
below the CoolSolve enthalpies because of the Air reference state. Without
the file the size-5 block (`P_thr`, `P_thrmin`, `gamma`, `T_thr`, `h_thr`)
stops on a singular Jacobian. The analysis report then lists 18 total
iterations; the Newton trace of that block is one step and the residual
stays 899999.

`cos` uses degrees. There is no `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. |
|---|---:|---:|---:|
| `A_thr` [m²] | 0.008831 | 0.008831 | 0 |
| `d_laval` [m] | 0.7182 | 0.7182 | 0 |
| `U` [m/s] | 376.04864 | 376.04864 | 9.23e-11 |
| `eta_laval` [-] | 0.873408 | 0.873477 | 7.86e-05 |
| `epsilon_s_global` [-] | 0.855940 | 0.856007 | 7.86e-05 |
| `P_thr` [Pa] | 485863.10 | 485745.86 | 2.41e-04 |
| `gamma` [-] | 1.332921 | 1.333659 | 5.54e-04 |
| `C_thr` [m/s] | 606.776 | 607.116 | 5.60e-04 |
| `C_ex_n` [m/s] | 1041.997 | 1041.794 | 1.95e-04 |
| `W_dot` [W] | 4370934.79 | 4378605.91 | 1.75e-03 |
| `M_dot` [kg/s] | 9.40651 | 9.42595 | 2.06e-03 |
| `v_thr` [m³/kg] | 0.569652 | 0.568796 | 1.50e-03 |
| `h_su` [J/kg] | 1314398.06 | 1187845.42 | 9.63e-02 |
| `h_thr` [J/kg] | 1130309.25 | 1003550.25 | 1.12e-01 |
| `h_ex_n_s` [J/kg] | 771519.66 | 645178.47 | 1.64e-01 |
| `s_su` [J/kg-K] | 4659.990 | 6473.780 | 2.80e-01 |

The equivalent section and the wheel diameter match the stored solution.
The wheel peripheral speed matches (`U`, relative difference 9.23e-11). The
Laval efficiency is 0.873408 against 0.873477 (7.86e-05). The throat is
choked: `P_thr = P_thrmin = 485863.10` Pa, above `P_ex = 100000` Pa.
Because `epsilon_n_s = 1`, the exit velocity equals the isentropic
nozzle-exit velocity, 1041.997 m/s in CoolSolve and 1041.794 m/s in EES.
The shaft power is 4370935 W against 4378606 W.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `MSTh-SB-R4-Ex2-2.EES` (EES X7.458). The
unit system is already `SI MASS DEG PA C J`, so `compare_solution.py` was
run without `--ees-units`. Stored unit strings are blank, except `W_dot`,
whose unit string is `-`. That flag does not scale a blank unit or that
string. The enthalpies and the shaft power in the stored solution are
already in J/kg and W. The tool's summary line is:

`30 common variables, 8 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1`

The maximum relative difference over all 30 common variables, as printed in
the tool's table, is 2.80e-01 on `s_su`. The exact ratio is 0.2801749.
That value is `verification.max_rel_diff`.

The name present only in CoolSolve is `PI`, the built-in constant in
`U = PI*d_laval*N`. The statistics are 30 equations and 30 variables, so
`PI` is not an extra unknown.

Eight common variables are above rtol 0.001.

**Air reference, separate from the equivalent section, the wheel parameters
and the shaft power.** Ideal-gas `Air` keeps CoolProp's reference. EES sets
the enthalpy to 0 at 0 K. CoolSolve − EES is +126552.65 J/kg on `h_su`
(850 °C), +126759.00 J/kg on `h_thr` and +126341.19 J/kg on `h_ex_n_s`,
about +126.3 to +126.8 kJ/kg. CoolSolve − EES on `s_su` is −1813.791 J/kg-K
(relative difference 2.80e-01). The enthalpy offset is not the same at the
three temperatures: it changes by +206.36 J/kg from the inlet to the throat
and by −211.45 J/kg from the inlet to the isentropic exit. That residual is
a difference of \(c_p(T)\) between EES and CoolProp. It is what remains in
the kinetic energies after the reference offset cancels:

| Drop | EES [J/kg] | CoolSolve [J/kg] | CoolSolve − EES [J/kg] |
|---|---:|---:|---:|
| `h_su − h_thr` | 184295.17 | 184088.81 | −206.36 |
| `h_su − h_ex_n_s` | 542666.95 | 542878.40 | +211.45 |

**Equivalent section and wheel parameters.** `A_thr` and `d_laval` agree
exactly. `U` agrees (9.23e-11). `eta_laval` and `epsilon_s_global` agree
(7.86e-05), under rtol 0.001. `alpha`, `rpm`, `eta_m` and `epsilon_n_s`
agree exactly.

**Pressures and gamma.** `P_thr` and `P_thrmin` are 485863.10 Pa against
485745.86 Pa (relative difference 2.41e-04), under rtol 0.001. The throat
is choked in both. Solved `gamma` is 1.332921 against 1.333659 (5.54e-04).

**Velocities**, from those drops. Both are under rtol 0.001:
`C_thr` 606.776 m/s against 607.116 m/s (5.60e-04), `C_ex_n` 1041.997 m/s
against 1041.794 m/s (1.95e-04).

**The other four differences** follow from that residual, not from the
126 kJ/kg offset:

- `v_thr` (1.50e-03). Specific volume at the isentropic throat from
  `volume(Air, h=h_thr, P=P_thr)`. Each library evaluates this at its own
  enthalpy, so the reference offset does not shift the volume. The residual
  is the property difference at that state. `P_thr` itself is 0.024 % high.
- `M_dot` (2.06e-03). `A_thr*C_thr/v_thr` with `A_thr` fixed. `C_thr` is
  0.056 % low and `v_thr` is 0.150 % high.
- `W_dot_in` and `W_dot` (1.75e-03): 4460138 W and 4370935 W against
  4467965 W and 4378606 W. They share this relative difference because
  `W_dot = eta_m*W_dot_in` with `eta_m = 0.98`. `M_dot` is 0.206 % low,
  `epsilon_s_in` is 0.0079 % low and `C_ex_n_s²` is 0.039 % high.

## Source and attribution

The equation window names no person. The file name is
`MSTh-SB-R4-Ex2-2.EES`, so the filename marks an SB solution. The inventory
attributes the ULiège MSTh course to J. Lebrun, V. Lemort and S. Bertagnolio.
Neither that course line nor the letters SB are written as a person's name
in the file, so the authors field is TBD (ULiège MSTh). The file itself
names nobody.

The EES licence tag is `{$ID$ #202: Laboratoire de Thermodynamique, U. de Liege}`.
That tag is the laboratory licence, not an author.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/SB/MSTh-SB-R4-Ex2-2.EES`.

Candidate TM-0064. Teaching exercise, not an exam. EES X7.458, plain text,
30 variable records, no lookup table and no parametric table.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `MSTh-SB-R4-Ex2-2.EES` (EES X7.458, plain text, 30 variables, no tables, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already SI, deleted with the licence tag. No `$Export`, `concat$`, `EESFILEDIR$` or `$TABSTOPS`. Comments translated to English. Property calls written in lowercase; the functions are unchanged. No value was rescaled.
- **Inlet pressure.** The equation window contains `P_su="10E5"9E5`. CoolSolve parses that line as `P_su = 900000`. The shipped equation is `P_su = 9E5`, the same assignment, with the display text `10E5` kept in the comment.
- **Square as extracted.** With that assignment the statistics are 30 equations, 30 variables, largest block 5 (`System square: Yes`). No Diagram-window input was restored. The commented targets `epsilon_s_global = 0.85` and `W_dot = 5E6`, and the commented provisional `gamma = 1.4`, stay comments. No computed unknown was replaced by a stored value. No diagram state arrays were added. The unchoked-flow note (`C_thr = C_ex_n_s` when `P_thr = P_ex`) stays a comment: the solution is choked.
- **Fluid**: `Air` left as `Air`. The moist-air hint is not applied. The ratio uses `+273`, as written.
- **Roots.** `C_thr`, `C_ex_n_s` and `C_ex_n` are squared. `.initials` is the stored solution and holds the positive roots. A solve with no initials does not converge (singular Jacobian on the size-5 block; analysis report: 18 total iterations). A solve started from the negated velocities returns the positive root (17 iterations). With `.initials`, 14 iterations.
- **Level**: equations 30 → 0; largest block 5 → 0; no function, procedure, array or `DUPLICATE` → 0; one machine, not discretised and not three or more coupled components → 0; one operating point, no calibration loop, off-design or dynamics → 0; the size-5 block needs the stored guesses → 1. Score 1 → level 1.

## Limitations and CoolSolve gaps

The solved `gamma` is the value consistent with ideal-gas `Air` and the
written temperature ratio. It is the unknown of that relation. The
enthalpies and the entropy use ideal-gas `Air`, so \(c_p\) is not constant.
Absolute Air enthalpies and the inlet entropy are not comparable with EES
without the reference offsets above. The equivalent section, the wheel
diameter, the peripheral speed and the Laval efficiency are.

The model is one operating point. The identified parameters are the numbers
written in the equation window.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` listed only `CSL-0310` before `CSL-0318`.
- `CSL-0310` *isentropic_nozzle_critical*: the standalone nozzle component with the same choked/unchoked throat, where the throat area is a design result instead of an identified parameter.
- `CSL-0318` *cordier_specific_speed*: 0D pre-design of a turbine (specific speed, Cordier diameter) from the duty, before any identified parameter exists.

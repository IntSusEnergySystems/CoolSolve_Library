# Double gasoline injection

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0206`

Teaching exercise (ULiège MCI, TP5, exercise 3): start and end of two gasoline
injections, fuel-air ratio, volumetric efficiency and standard air conditions
of a four-stroke engine. The injection durations follow from the crank angles
and the engine speed. The intake air flow follows from the volumetric
efficiency. The fuel flow follows from the fuel-air ratio, and the two
injected masses follow from that flow and the cycle time. The fuel is carried
as a mass.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 26 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_3_Deux injections moteur essence_PNG.EES` (EES X10.589) |
| **Authors** | TBD (ULiège MCI) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@6730bcf — verified against the EES stored solution (max rel. diff 3.24e-04) |

## Problem statement

Two gasoline injections per cylinder and per cycle of a four-stroke engine.
The course sheet (MCI, fifth exercise session, exercise 3) asks for the
nearly constant fuel flow into the engine, the two injection durations, and
the fuel flow during each injection.

Data, as written in the file:

- total displacement `V_tot = 4.8e-3` m³
- `n_c = 8` cylinders
- intermittency factor `i = 0.5` for a four-stroke engine
- rotational speed `N = 4200` rpm
- fuel-air ratio `f = 1/28`
- start and end of injection 1: `SOI_1 = -10+180` °, `EOI_1 = 80+180` °
- start and end of injection 2: `SOI_2 = -70` °, `EOI_2 = -30` °
- volumetric efficiency `epsilon_v = 0.98`
- air at `T1 = 25` °C and `p1 = 101325` Pa (the original calls these the standard conditions)

The first injection is one quarter of the fuel mass per cylinder (`m_1 = m_tot/4`).
The second injection is the rest. The fuel is a mass: the file does not call
a fuel-property function.

## Model

Intake air. `rho_a` is `DENSITY(Air, T=T1, P=P1)`. `p1` and `P1` are the same
variable. With `N` in rpm:

\[
V_s = V_{\mathrm{tot}} / n_c, \qquad
\epsilon_v = \dot{M}_a / \big(\rho_a\, V_s\, (N/60)\, n_c\, i\big), \qquad
\dot{M}_f = f\, \dot{M}_a
\]

Injection durations, in crank-angle degrees and in seconds:

\[
DOI_1 = EOI_1 - SOI_1, \qquad \Delta t_1 = DOI_1 / (360\, N/60)
\]

and the same pair for injection 2. Cycle time and masses per cylinder:

\[
\Delta t_{\mathrm{tot}} = 1/(N/60)/i, \qquad
m_{\mathrm{tot}} = (\dot{M}_f / n_c)\, \Delta t_{\mathrm{tot}}, \qquad
m_1 = m_{\mathrm{tot}}/4, \qquad m_{\mathrm{tot}} = m_1 + m_2
\]

\[
\dot{M}_1 = m_1 / \Delta t_1, \qquad \dot{M}_2 = m_2 / \Delta t_2
\]

`1/(N/60)/i` is left-associative, as written: at 4200 rpm and `i = 0.5` it is
the time of two revolutions.

| Quantity | Role | Value |
|---|---|---|
| `V_tot`, `n_c`, `i`, `N` | displacement, cylinders, intermittency, speed | 4.8×10⁻³ m³, 8, 0.5, 4200 rpm |
| `f` | fuel-air ratio | 1/28 |
| `SOI_1`, `EOI_1` | injection 1 | 170 °, 260 ° |
| `SOI_2`, `EOI_2` | injection 2 | −70 °, −30 ° |
| `epsilon_v` | volumetric efficiency | 0.98 |
| `T1`, `p1` | air temperature and pressure | 25 °C, 101325 Pa |
| `rho_a`, `M_dot_a` | intake-air density and flow | solved |
| `M_dot_f` | fuel flow into the engine | solved |
| `DOI_1`, `DELTAt_1`, `DOI_2`, `DELTAt_2` | injection durations | solved |
| `m_tot`, `m_1`, `m_2` | fuel masses per cylinder | solved |
| `M_dot_1`, `M_dot_2` | fuel flow during each injection | solved |

Every equation is explicit (largest block 1).

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./gasoline_double_injection.eescode
```

`gasoline_double_injection.initials` holds the 20 stored values of the
variables that exist in the equation window. `M_dot_f`, `m_tot`, `m_1`,
`m_2`, `M_dot_1` and `M_dot_2` are not in the stored solution and are not in
that file. With the file the solver reports 4 iterations. Without it, 4
iterations. The two solutions are identical. There is no `abs()` call and no
second root: the largest block is 1, and the initials are the stored values
of an explicit system. The shipped `.sol` is the run with those guesses. No
`coolsolve.conf` and no variant.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `epsilon_v` [-] | 0.98 | 0.98 |
| `rho_a` [kg/m³] | 1.184318 | 1.183935 |
| `M_dot_a` [kg/s] | 0.1949862 | 0.1949230 |
| `DOI_1` [°] | 90 | 90 |
| `DOI_2` [°] | 40 | 40 |
| `DELTAt_1` [s] | 0.003571429 | 0.003571429 |
| `DELTAt_2` [s] | 0.001587302 | 0.001587302 |
| `DELTAt_tot` [s] | 0.02857143 | 0.02857143 |
| `M_dot_f` [kg/s] | 0.006963793 | — |
| `m_tot` [kg] | 2.487069×10⁻⁵ | — |
| `m_1` [kg] | 6.217672×10⁻⁶ | — |
| `m_2` [kg] | 1.865302×10⁻⁵ | — |
| `M_dot_1` [kg/s] | 0.001740948 | — |
| `M_dot_2` [kg/s] | 0.01175140 | — |

`M_dot_f`, `m_tot`, `m_1`, `m_2`, `M_dot_1` and `M_dot_2` are not in the
20-variable list `compare_solution.py` reads. Applying the same equations to
the stored `M_dot_a` gives 0.006961535 kg/s, 2.486263×10⁻⁵ kg,
6.215657×10⁻⁶ kg, 1.864697×10⁻⁵ kg, 0.001740384 kg/s and 0.01174759 kg/s.
Each is 3.24e-04 below the CoolSolve value, the same ratio as `rho_a`.

The course sheet prints 6.962×10⁻³ kg/s, 3.571 ms, 1.587 ms, 1.740×10⁻³ kg/s
and 1.175×10⁻² kg/s. Those rounded figures follow the EES density.

Orders of magnitude: 4.8 L over eight cylinders is 0.60 L each; at 4200 rpm a
90° injection lasts 3.57 ms and a 40° injection lasts 1.59 ms; the engine air
flow is about 0.195 kg/s and the fuel flow about 0.0070 kg/s; the fuel mass
per cylinder and per cycle is about 0.025 g.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Ideal-gas injection calculation: the equation window has no cycle state
points. A maintainer figure would be a timing sketch of the two injections.

## Verification

Reference: the solution stored in the EES file (20 variables decoded by
`ees_extract.py`; the unit system is already `SI MASS DEG PA C J`, so the
comparison is without `--ees-units`). `compare_solution.py` on
`gasoline_double_injection.sol` against `reference/ees_variables.csv`:

> 20 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 6

Maximum relative difference over all common variables, as printed in the tool's
table: **3.24e-04** (`rho_a` and `M_dot_a`). Nothing exceeds rtol 0.001.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `rho_a` | 1.18393 | 1.18432 | 3.24e-04 |
| `M_dot_a` | 0.194923 | 0.194986 | 3.24e-04 |
| `DELTAt_2` | 0.0015873 | 0.0015873 | 1.90e-10 |
| `DELTAt_1` | 0.00357143 | 0.00357143 | 1.20e-10 |
| `f` | 0.0357143 | 0.0357143 | 1.20e-10 |
| `DELTAt_tot` | 0.0285714 | 0.0285714 | 5.00e-11 |

`DOI_1`, `DOI_2`, `EOI_1`, `EOI_2`, `epsilon_v`, `i`, `N`, `n_c`, `p1`,
`SOI_1`, `SOI_2`, `T1`, `V_s` and `V_tot` agree exactly (rel. diff `0.00e+00`).

`rho_a = DENSITY(Air, T=25, P=101325)` is where CoolProp and EES differ.
`M_dot_a` is proportional to `rho_a` and carries the same 3.24e-04. `f = 1/28`
differs from the stored decimal 0.03571428571 by 1.20e-10 as printed. The
three durations differ from the stored decimals by the amounts in the table.

The six names present only in the CoolSolve solution are `M_dot_f`, `m_tot`,
`m_1`, `m_2`, `M_dot_1` and `M_dot_2`. They were not in the stored solution.
They scale with `rho_a` (see Results).

No enthalpy and no entropy are computed. The ideal-gas `Air` enthalpy offset
of about +126 kJ/kg, often seen against EES, does not appear. The injected
masses and the flows are the density ratio above, separate from that offset.
`p1` is already stored in Pa. No value was in kJ, and none was rescaled by
hand. A stored unit string that is blank is left as stored; `--ees-units`
was not used.

CoolSolve reports all 26 equations satisfied.

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_3_Deux injections moteur essence_PNG.EES`
(EES X10.589, plain-text equations). The file itself names nobody. The header
line is `PNG09042018` (initials and the date 2018-04-09), which is not a full
name. The `{$ID$}` tag is the EES licence of Philippe Ngendakumana (ULG
Thermotechnics, Liège), which is the licence holder and not an author line.
The inventory row TM-0243 attributes the file to P. Ngendakumana and R. Dickes.
Authors in `model.json` stay `TBD (ULiège MCI)` until that attribution is
confirmed. ULiège course MCI, TP5, exercise 3. Published under the library
licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`): EES X10.589, plain-text equations,
  `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or parametric table, 20
  variables decoded, no extract warnings. Unit system already
  `SI MASS DEG PA C J`: `$UnitSystem` removed, no value rescaled. `$TABSTOPS`
  and the four `$Bookmark` lines were removed (they are not equations). The
  equation window with those directives removed is square (26 equations, 26
  variables), so no Diagram-window value was restored and no computed unknown
  was replaced by a stored number. Stored values of the variables that exist
  in the equation window are the `.initials` guesses. Comments translated to
  English; variable names kept, including `P1` in the `DENSITY` call beside
  the assignment `p1` (one variable).
- **Level**: equations 26 (< 50) → 0; largest block 1 (≤ 5) → 0; no user
  function, procedure, array or `DUPLICATE` → 0; one set of explicit injection
  relations, no multi-zone discretisation → 0; volumetric efficiency and the
  fuel-air ratio are given data (no calibration, off-design, part-load or
  dynamics) → 0; converges from the default guess in 4 iterations, without a
  tuned configuration → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- The coefficient values (`epsilon_v`, `f`, the crank angles) are the data of
  the exercise. The fuel is a mass and a fuel-air ratio.
- `rho_a`, and therefore `M_dot_a` and the six fuel masses and flows, follow
  the ideal-gas density of `Air` and differ slightly between CoolProp and EES
  (see Verification). The common-variable comparison stays inside rtol 0.001.
- Calling `DENSITY` on `Air` prints a warning that moist air should use
  `AirH2O`. The fluid in the file is ideal-gas `Air`; the warning is the name
  check, and the fluid is unchanged.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

`related` is empty. This equation window is the double-injection calculation
of TP5 exercise 3.

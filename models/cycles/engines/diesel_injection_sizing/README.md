# Diesel injection sizing

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0185`

Teaching exercise (ULiège MCI, TP5, exercise 4): start and end of injection,
volumetric efficiency and mixture richness of a four-stroke diesel engine.
The injection duration follows from the two crank angles and the engine
speed. The air mass in one cylinder follows from the volumetric efficiency.
The injected fuel mass follows from the richness. The fuel is carried as a
mass.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 21 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_4_Injection moteur diesel_PNG.EES` (EES X10.393) |
| **Authors** | TBD (ULiège MCI) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (max rel. diff 3.24e-04) |

## Problem statement

Size the injection of a four-stroke diesel: duration, air mass in one
cylinder, and injected fuel mass.

Data, as written in the file:

- `n_c = 5` cylinders
- total displacement `V_s_tot = 3.2e-3` m³
- rotational speed `Rpm = 2400` 1/min
- start of injection `SI = -20` °
- end of injection `EI = 5` °
- volumetric efficiency `epsilon_v = 0.95`
- air at `T_a = 25` °C and `p_a = 101325` Pa (the original calls these the standard conditions)
- mixture richness `phi = 0.8`
- stoichiometric air-fuel ratio `Afr_st = 14.5`
- intermittency factor `i = 0.5` for a four-stroke engine

The richness is the fuel-air ratio over the stoichiometric fuel-air ratio.
The injector flow is the injected fuel mass divided by the injection duration.
The fuel is a mass: the file does not call a fuel-property function.

## Model

Injection duration, in crank-angle degrees and in seconds, with `N = Rpm/60`:

\[
DI = EI - SI, \qquad \Delta t_{\mathrm{inj}} = DI / (360\, N)
\]

The original labels `DI` as `° V`.

Swept volume of one cylinder and air mass from the volumetric efficiency.
`rho_a` is `DENSITY(Air, T=T_a, P=P_a)`:

\[
V_s = V_{s,\mathrm{tot}} / n_c, \qquad
\epsilon_v = M_a / (\rho_a\, V_s)
\]

`p_a` and `P_a` are the same variable. Richness and fuel:

\[
f_{st} = 1/Afr_{st}, \qquad \phi = f / f_{st}, \qquad
M_f = f\, M_a, \qquad \dot{M}_{f,\mathrm{inj}} = M_f / \Delta t_{\mathrm{inj}}
\]

| Quantity | Role | Value |
|---|---|---|
| `V_s_tot` | total displacement | 3.2×10⁻³ m³ |
| `n_c` | number of cylinders | 5 |
| `Rpm` | rotational speed | 2400 1/min |
| `SI`, `EI` | start and end of injection | −20 °, 5 ° |
| `epsilon_v` | volumetric efficiency | 0.95 |
| `T_a`, `p_a` | air temperature and pressure | 25 °C, 101325 Pa |
| `phi` | mixture richness | 0.8 |
| `Afr_st` | stoichiometric air-fuel ratio | 14.5 |
| `i` | intermittency factor | 0.5, not used by any other equation |
| `DI`, `DELTAt_inj` | injection duration | solved |
| `rho_a`, `M_a` | intake-air density and mass in one cylinder | solved |
| `f`, `M_f`, `M_dot_f_inj` | fuel-air ratio, fuel mass, injector flow | solved |

Every equation is explicit (largest block 1). `i` is assigned and then unused,
as in the original.

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./diesel_injection_sizing.eescode
```

`diesel_injection_sizing.initials` holds the decoded stored values of the
variables that exist in the equation window. The decoded name `t` is not one
of them (the duration is `DELTAt_inj`) and is not in the file. With the file
the solver reports 3 iterations. Without it, 4 iterations. The two solutions
differ by at most 5.62×10⁻¹¹ relative, on `f`, `M_f` and `M_dot_f_inj`: the
stored `f` is already inside the solver tolerance, so the run with guesses
keeps that value. The shipped `.sol` is that run. No `coolsolve.conf` and no
variant.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `SI` [°] | −20 | −20 |
| `EI` [°] | 5 | 5 |
| `DI` [°] | 25 | 25 |
| `N` [1/s] | 40 | 40 |
| `DELTAt_inj` [s] | 0.001736111111 | 0.001736111111 |
| `epsilon_v` [-] | 0.95 | 0.95 |
| `rho_a` [kg/m³] | 1.184318 | 1.183935 |
| `phi` [-] | 0.8 | 0.8 |
| `f_st` [-] | 0.06896551724 | 0.06896551724 |
| `f` [-] | 0.05517241379 | 0.05517241379 |
| `V_s` [m³] | 6.4×10⁻⁴ | 6.4×10⁻⁴ |
| `V_s_tot` [m³] | 3.2×10⁻³ | 3.2×10⁻³ |
| `M_a` [kg] | 7.200656×10⁻⁴ | 7.198322×10⁻⁴ |
| `M_f` [kg] | 3.972776×10⁻⁵ | 3.971488×10⁻⁵ |
| `M_dot_f_inj` [kg/s] | 0.02288319 | 0.02287577 |

`DELTAt_inj`, `V_s`, `V_s_tot`, `M_a`, `M_f` and `M_dot_f_inj` are not in the
16-variable list `compare_solution.py` reads. They are stored in the EES file
(`DELTAt_inj` under the name `t_inj`). `V_s`, `V_s_tot` and the duration match.
`M_a`, `M_f` and `M_dot_f_inj` follow `rho_a`.

Orders of magnitude: 3.2 L over five cylinders is 0.64 L each; at 2400 1/min
a 25° injection lasts 1.74 ms; the air mass in one cylinder is about 0.72 g;
at richness 0.8 the fuel mass is about 0.040 g, so the injector flow during
the injection is about 0.023 kg/s.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Ideal-gas sizing model: the maintainer's figure is a parametric sweep (for
example `M_dot_f_inj` against `Rpm`), saved as `figures/diesel_injection_sizing_sweep.png`.

## Verification

Reference: the solution stored in the EES file (16 variables decoded by
`ees_extract.py`; the unit system is already `SI MASS DEG PA C J`, so the
comparison is without `--ees-units`). `compare_solution.py` on
`diesel_injection_sizing.sol` against `reference/ees_variables.csv`:

> 15 common variables, 0 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 6

Maximum relative difference over all common variables, as printed in the tool's
table: **3.24e-04** (`rho_a`). Nothing exceeds rtol 0.001.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `rho_a` | 1.18393 | 1.18432 | 3.24e-04 |
| `f_st` | 0.0689655 | 0.0689655 | 2.00e-11 |

`Afr_st`, `DI`, `EI`, `epsilon_v`, `f`, `i`, `N`, `n_c`, `p_a`, `phi`, `Rpm`,
`SI` and `T_a` agree exactly (rel. diff `0.00e+00`).

`rho_a = DENSITY(Air, T=25, P=101325)` is where CoolProp and EES differ.
`f_st = 1/14.5` differs from the decoded value by 2.00e-11 as printed.

The name present only in the decoded EES list is `t`. Its value,
0.001736111111 s, is the injection duration. The equation variable is
`DELTAt_inj`; the file stores that duration as `t_inj` (the `DELTA` prefix).
The six names present only in the CoolSolve solution are `DELTAt_inj`, `M_a`,
`M_f`, `M_dot_f_inj`, `V_s` and `V_s_tot`. The same file stores `M_a`, `M_f`,
`M_dot_f_inj`, `V_s` and `V_s_tot` in records the extractor did not emit.
`V_s` and `V_s_tot` match. `M_a`, `M_f` and `M_dot_f_inj` are proportional to
`rho_a` and carry the same 3.24e-04.

With the stored guesses the solver keeps `f` at the stored value. Then
`phi = f/f_st` holds to about 6×10⁻¹¹ relative, and CoolSolve reports all 21
equations satisfied (max relative residual 4.5×10⁻¹¹).

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_4_Injection moteur diesel_PNG.EES`
(EES X10.393, stored as RTF). The equation window names no author. The
`{$ID$}` tag is the EES licence of Philippe Ngendakumana (ULG Thermotechnics,
Liège), which is the licence holder and not an author line. The inventory row
TM-0244 attributes the file to P. Ngendakumana and R. Dickes. Authors in
`model.json` stay `TBD (ULiège MCI)` until that attribution is confirmed.
ULiège course MCI, TP5, exercise 4. Published under the library licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`): EES X10.393, RTF equations
  converted to text, `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or
  parametric table, 16 variables decoded, no extract warnings. Unit system
  already `SI MASS DEG PA C J`: `$UnitSystem` removed, no value rescaled. The
  formatting directive `$TABSTOPS` was removed (it is not an equation). The
  trailing NUL byte was removed. The unmodified extract, with the NUL byte and
  the `$UnitSystem` line removed (`$TABSTOPS` still present), is square (21
  equations, 21 variables), so no Diagram-window value was restored and no
  computed unknown was replaced by a stored number. Stored values of the
  variables that exist in the equation window are the `.initials` guesses.
  The decoded name `t` is not copied: it is not an equation variable.
  Comments translated to English; variable names kept, including `P_a` in the
  `DENSITY` call beside the assignment `p_a` (one variable).
- **Level**: equations 21 (< 50) → 0; largest block 1 (≤ 5) → 0; no user
  function, procedure, array or `DUPLICATE` → 0; one set of explicit sizing
  relations, no multi-zone discretisation → 0; volumetric efficiency and
  richness are given data (no calibration, off-design, part-load or
  dynamics) → 0; converges from the default guess in 4 iterations, without a
  tuned configuration → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- `i = 0.5` is stated and unused. The injector flow is the fuel mass divided
  by the injection duration; it does not apply the four-stroke intermittency
  factor.
- The coefficient values (`epsilon_v`, `phi`, `Afr_st`) are the data of the
  exercise.
- `rho_a`, and therefore `M_a`, `M_f` and `M_dot_f_inj`, follow the ideal-gas
  density of `Air` and differ slightly between CoolProp and EES (see
  Verification). The common-variable comparison stays inside rtol 0.001.
- Calling `DENSITY` on `Air` prints a warning that moist air should use
  `AirH2O`. The fluid in the file is ideal-gas `Air`; the warning is the name
  check, and the fluid is unchanged.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

- `CSL-0178` — intake valve sizing for a square engine, ULiège MCI TP5
  exercise 1. Same course session, a different exercise.
- `CSL-0188` — CO2 emissions in g/km from a fuel consumption, ULiège MCI
  TP7 exercise 3. The fuel there is a chemical formula, not an injected mass.
- `CSL-0277` — fuel injection in an atmospheric CI engine, ULiège MCI TP6
  exercise 3 (after Pulkrabek 5-9/5-10). Same engine/injection skeleton with
  other inputs; it computes the stoichiometric fuel-air ratio from the C12H26
  composition and adds the injector sizing (discharge coefficient, injection
  pressure differential, outlet diameter).

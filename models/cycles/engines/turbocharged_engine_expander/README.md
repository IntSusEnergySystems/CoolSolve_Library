# Turbocharged engine with expander temperature drop

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0223`

Teaching exercise (ULiège MCI, sixth exercise session, statement 2): air
and fuel mass flows of a turbocharged eight-cylinder engine, then the
useful power of an expander whose temperature drop is given. The volumetric
efficiency is defined on the ambient density, so the given value is greater
than one. The fuel is stoichiometric C8H18. A second evaluation of the same
efficiency uses the built-in density of Air.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air, O2, N2 |
| **Size** | 31 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP6/EX2_PNG_2019.EES` (EES X10.589) |
| **Authors** | P. Ngendakumana |
| **License** | MIT |
| **CoolSolve** | native file runs (4 iterations); verified against the EES stored solution (max rel. diff 3.31325e-04 on `rho_a_bis`) — 0.3.0@4798e2b |

## Problem statement

Sixth exercise session, statement 2. The window heading is
`PNG_18042019`: initials plus a date (18 April 2019), not a full name.

Data, as written in the file:

- total displacement `V_tot = 5.6e-3` m³
- `n_c = 8` cylinders
- `i = 0.5` cycles per revolution
- volumetric compression ratio `r_v = 9.4`; the original says it is unused
- rotational speed `RPM = 2800` 1/min
- volumetric efficiency `epsilon_v = 1.9`, referenced to the ambient air and not to the intake manifold
- temperature drop in the expander `DELTAT_exp = -44` K
- mechanical efficiency of the expander `eta_mec = 0.87`
- ambient air `T_amb = 23` °C, `p_amb = 98e3` Pa
- specific heat of the exhaust gas `cp_g = 1150` J/(kg·K)
- fuel `m = 8`, `n = 18` (C8H18), stoichiometric (`f = f_st`)

`epsilon_v` is greater than 1 because the original defines it on the ambient
density. The value 1.9 is the given data. `DELTAT_exp` is a temperature drop,
and the original writes it negative.

The air mass flow follows from that definition of `epsilon_v`. The fuel flow
is the stoichiometric fraction of the air flow. The expander specific work is
`cp_g` times the temperature drop, and the useful power is the power available
to drive the compressor. The original then repeats the flows and the power
with the built-in properties of air.

## Model

Swept volume, stoichiometric fuel-air ratio of C8H18, and the ideal-gas
ambient density used for the combustion air. `R#` is the built-in universal
gas constant.

\[
V_s = V_{tot}/n_c
\]

\[
f_{st} = \frac{m\,M_C + n\,M_H}{(m+n/4)\,(M_{O_2} + (79/21)\,M_{N_2})}, \qquad f = f_{st}
\]

\[
MM_a = 0.21\,M_{O_2} + 0.79\,M_{N_2}, \qquad r_a = R_u/MM_a, \qquad R_u = R\#
\]

\[
\rho_a = p_{amb}/\big(r_a\,(T_{amb}+273.15)\big)
\]

\(M_C\) and \(M_H\) are `MolarMass(C)` and `MolarMass(H)`, the standard atomic
weights 12.0107 and 1.00794 kg/kmol, as in EES; `MolarMass(O2)` and
`MolarMass(N2)` are calls too.

The original writes the stoichiometric reaction as a comment, with `H20` in
that comment. It is not an equation, and there is no heating-value call.

Air, fuel and exhaust flows. `epsilon_v = 1.9` is the input. The same name
is written again as the definition that solves `M_dot_a`:

\[
\epsilon_v = \dot{M}_a / \big(\rho_a \, V_s \, (RPM/60) \, n_c \, i\big)
\]

\[
\dot{M}_f = f\,\dot{M}_a, \qquad \dot{M}_p = \dot{M}_a + \dot{M}_f
\]

Second evaluation, as in the original ("if the properties of air are used").
The property call writes `P_amb`; the assignment writes `p_amb`. The two
spellings are one variable.

\[
MM_{a,bis} = M_{Air}, \qquad \rho_{a,bis} = \rho(Air, T_{amb}, p_{amb})
\]

\[
\epsilon_v = \dot{M}_{a,bis} / \big(\rho_{a,bis} \, V_s \, (RPM/60) \, n_c \, i\big)
\]

\[
\dot{M}_{f,bis} = f\,\dot{M}_{a,bis}, \qquad \dot{M}_{p,bis} = \dot{M}_{a,bis} + \dot{M}_{f,bis}
\]

Expander. The temperature drop is negative, so the specific work is negative.
The leading minus sign makes the useful power positive: it is the power
available to drive the compressor.

\[
w_{exp} = c_{p,g}\,\Delta T_{exp}
\]

\[
\dot{W}_{exp,utile} = -\eta_{mec}\,\dot{M}_p\,w_{exp}, \qquad
\dot{W}_{exp,utile,bis} = -\eta_{mec}\,\dot{M}_{p,bis}\,w_{exp}
\]

| Quantity | Role | Value |
|---|---|---|
| `V_tot`, `n_c`, `i` | displacement, cylinders, cycles per revolution | 5.6×10⁻³ m³, 8, 0.5 |
| `RPM` | rotational speed | 2800 1/min |
| `epsilon_v` | volumetric efficiency on ambient density | 1.9 |
| `DELTAT_exp` | expander temperature drop | −44 K |
| `eta_mec` | mechanical efficiency | 0.87 |
| `m`, `n` | fuel C8H18 | 8, 18 |
| `T_amb`, `p_amb` | ambient air | 23 °C, 98000 Pa |
| `cp_g` | exhaust specific heat | 1150 J/(kg·K) |
| `M_dot_a`, `M_dot_f` | air and fuel mass flows | solved |
| `W_dot_exp_utile` | useful expander power | solved |
| `M_dot_a_bis`, `W_dot_exp_utile_bis` | same results with `Density(Air)` | solved |

Every equation is explicit (largest block 1). `r_v` is assigned and is not
used in another equation, as the original says.

## How to run

From this folder:

```bash
coolsolve ./turbocharged_engine_expander.eescode
```

The solver reports 4 iterations from the default guess; no guess file and no
`coolsolve.conf` are needed.

## Results

The combustion-air column uses
`rho_a = p/(r*T)`. The Air column uses `Density(Air)`.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `f` [-] | 0.066516905 | 0.066517683 |
| `rho_a` [kg/m³] | 1.148238 | 1.148242 |
| `M_dot_a` [kg/s] | 0.285069 | 0.285070 |
| `M_dot_f` [kg/s] | 0.0189619 | 0.0189622 |
| `M_dot_p` [kg/s] | 0.304031 | 0.304032 |
| `w_exp` [J/kg] | −50600 | −50600 |
| `W_dot_exp_utile` [W] | 13384.06 | 13384.11 |
| `rho_a_bis` [kg/m³] | 1.153199 | 1.152817 |
| `M_dot_a_bis` [kg/s] | 0.286301 | 0.286206 |
| `M_dot_f_bis` [kg/s] | 0.0190438 | 0.0190378 |
| `W_dot_exp_utile_bis` [W] | 13441.88 | 13437.44 |

The equation window has no enthalpy and no entropy, so there is no absolute
enthalpy to set beside these flows and this power.

Orders of magnitude: 5.6 L over eight cylinders is 0.7 L each. At 2800 1/min
with `i = 0.5` and `epsilon_v = 1.9`, the intake volume flow at the ambient
density is about 0.25 m³/s, and the air mass flow is about 0.285 kg/s. The
stoichiometric fuel fraction of C8H18 is about 0.0665, so the fuel flow is
about 0.019 kg/s. The expander specific work is 1150×(−44) = −50600 J/kg, and
the useful power is about 13.4 kW.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Air-and-fuel flow exercise: the maintainer's figure is a schematic of the
air path and the expander, saved as
`figures/turbocharged_engine_expander_airpath.png`.

## Verification

Reference: the solution stored in `EX2_PNG_2019.EES` (34 names decoded by
`ees_extract.py`, 31 with a stored value). The unit system is already
`SI MASS DEG PA C J`, so the comparison is without `--ees-units`.
`compare_solution.py` on `turbocharged_engine_expander.sol` against
`reference/ees_variables.csv`:

> 31 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

Maximum relative difference over all common variables: **3.31325e-04**
(`rho_a_bis`). The table printed by the tool gives `3.31e-04`.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `rho_a_bis` | 1.15282 | 1.1532 | 3.31e-04 |
| `M_dot_a_bis` | 0.286206 | 0.286301 | 3.31e-04 |
| `M_dot_p_bis` | 0.305244 | 0.305345 | 3.31e-04 |
| `W_dot_exp_utile_bis` | 13437.4 | 13441.9 | 3.31e-04 |
| `M_dot_f_bis` | 0.0190378 | 0.0190438 | 3.20e-04 |
| `R_u` | 8314.34 | 8314.46 | 1.47e-05 |
| `M_dot_f` | 0.0189622 | 0.0189619 | 1.47e-05 |
| `M_dot_a` | 0.28507 | 0.285069 | 3.06e-06 |
| `W_dot_exp_utile` | 13384.1 | 13384.1 | 3.79e-06 |

`M_dot_a` is 0.2850692438 kg/s versus 0.285070116 kg/s (rel 3.06e-06).
`M_dot_f` is 0.01896192387 kg/s versus 0.01896220351 kg/s (rel 1.47e-05).
`W_dot_exp_utile` is 13384.06006 W versus 13384.11077 W (rel 3.79e-06).
`w_exp` is −50600 J/kg on both sides. Those three results follow
`rho_a = p_amb/(r_a*(T_amb+273.15))`. That ideal-gas density is 1.148238
kg/m³ versus 1.148242 kg/m³ (rel 3.06e-06). It does not carry the CoolProp
density residual.

`rho_a_bis = Density(Air, T=23 °C, P=98000 Pa)` is 1.15319874 kg/m³ versus
1.152816658 kg/m³. `M_dot_a_bis` scales with that density (rel 3.31325e-04).
`W_dot_exp_utile_bis` is 13441.882 W versus 13437.438 W (rel 3.306e-04). The
fuel fraction `f` moves only with the molar masses of O2 and N2 (rel
1.17e-05), because `MolarMass(C)` and `MolarMass(H)` are the EES constants
12.0107 and 1.00794 kg/kmol. `R_u = R#` is 8314.462618 J/(kmol·K) versus the
stored 8314.34 (rel 1.47e-05). `MM_a_bis` is 28.96546 kg/kmol versus 28.96547
(rel 3.45e-07).

CoolSolve reports all 31 equations satisfied (max relative residual 0).

The three decoded names that are not in the equation window are `L`, `D` and
`r`. Each has a guess and no stored value (`L` and `D` guess 0.09623567124;
`r` guesses 287.0172507). They are not in the comparison (`only in EES: 0`).
The one name present only in CoolSolve is `R#`, the built-in constant written
into the solution next to `R_u = R#`.

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP6/EX2_PNG_2019.EES`
(EES X10.589, equation window stored as RTF). The equation window is headed
`6ème séance d'exercices : énoncé 2_PNG_18042019`. `PNG_18042019` is initials
plus a date, not a full name. The `{$ID$}` tag is the EES licence of
Philippe Ngendakumana (ULG Thermotechnics, Liège). The window does not name
another person. Author in `model.json`: P. Ngendakumana. ULiège course MCI,
TP6, sixth exercise session, statement 2. Published under the library
licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`): EES X10.589, RTF equation window
  converted to text, one NUL byte at the end of the extract removed,
  `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or parametric table,
  34 names decoded, no extract warnings. Unit system already
  `SI MASS DEG PA C J`: `$UnitSystem` removed, no value rescaled. `$TABSTOPS`
  removed. The file has no `$Export` line. The unmodified extract, with the
  NUL and those directives removed, is square (31 equations, 31 variables,
  largest block 1). CoolSolve treats `p_amb` and `P_amb` as one variable, so
  both spellings are left as written. `L`, `D` and `r`
  were not restored: the system is square without them, and none has a stored
  value. Comments translated to English. `m = 8 ; n = 18` split onto one
  equation per line. The combustion line that writes `H20` stays a comment.
  `epsilon_v = 1.9` and `DELTAT_exp = -44` are unchanged. `R#` is kept. No
  heating-value call was added, and no diagram-state arrays. The file keeps
  `MolarMass(C)`, `MolarMass(H)`, `MolarMass(O2)`, `MolarMass(N2)`,
  `MolarMass(Air)` and `Density(Air, …)` as in the original.
- **Level**: equations 31 (< 50) → 0; largest block 1 (≤ 5) → 0; no user
  function, procedure, array or `DUPLICATE` → 0; the two flow evaluations and
  the expander power are sequential assignments, not a multi-zone model → 0;
  the efficiency, the fuel formula and the temperature drop are given data
  (no calibration, off-design, part-load or dynamics) → 0; converges from the
  default guess in 4 iterations, without a tuned configuration → 0. Score 0
  → **level 1**.

## Limitations and CoolSolve gaps

- `MolarMass` of an element (`C`, `H`) is the IUPAC standard atomic weight
  (12.0107 and 1.00794 kg/kmol), the values EES returns for those two calls.
  `MolarMass(Air)` returns 28.96546 kg/kmol; the fluid in the file is
  ideal-gas `Air`.
- `epsilon_v = 1.9` is the data of the exercise. It is greater than one
  because the original defines it on the ambient density, not on the intake
  manifold.
- `DELTAT_exp = -44` K is the temperature drop as written. `w_exp` is
  −50600 J/kg.
- `rho_a` is the ideal-gas density `p/(r*T)` and does not carry the CoolProp
  density residual. `rho_a_bis` does. The equations are
  satisfied.
- `r_v` is unused, as the original says.

## Related models

None.

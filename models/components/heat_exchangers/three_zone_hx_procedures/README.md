# Heat exchangers: three-zone and epsilon-NTU zone procedures

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0112`

Seven EES `PROCEDURE`s of the J. Lebrun laboratory (ULiège) files of the
`thermo_models` collection that rate a heat exchanger **zone by zone**: the
three-zone condenser and evaporator built on a regularised log-mean
temperature difference, the effectiveness-NTU zone procedures of an
automotive condenser, and an epsilon-NTU evaporator with a vapour and a
two-phase zone. The definitions are at the top of the file; the program after
them calls each procedure with the operating point stored in its source file.
No equation was changed: this is a transcription, not a translation.

| | |
|---|---|
| **Category** | Components and machines › Heat exchangers |
| **Fluids** | R245fa, R123, R134a, Water, Air (`air_ha` = humid air) |
| **Size** | 139 equations (largest block: 6); 7 procedures of 13–94 equations each |
| **Source** | `~/Nextcloud/thermo_models/procedures EES/`: `condenseur 3 zones.EES` (X8.652), `evaporator 1 2 & 3 zones SQ110729.EES` (X9.249), `LMTD.EES` (X8.652), `epsilon NTU single phase - EV - CD SQ081222.EES` (X8.198), `Evaporator epsilon-NTU SQ080311.EES` (X7.991) |
| **Authors** | Sylvain Quoilin (ULiège) for the four signed files; `condenseur 3 zones.EES` and `LMTD.EES` carry only the *J. Lebrun laboratory* licence stamp → `TBD (ULiège, J. Lebrun laboratory)` |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — runs; the energy balance of every procedure closes exactly, the stored EES solutions are reproduced between 0.1 % and 8.4 % (see *Verification*) |

## Problem statement

A plate heat exchanger used as a condenser or an evaporator does not work at
one single temperature difference. It works in three zones at once — a
sensible zone, a two-phase (condensing or boiling) zone and a sensible zone —
and each of them has its own heat-transfer coefficient, its own log-mean
temperature difference and its own share of the surface. The laboratory files
of this model encode that decomposition:

* **`lmtd_xi1000`** returns the counterflow log-mean temperature difference
  from the four terminal temperatures, with a regularisation (`xi = 1000 K⁻¹`,
  a 1 K dead band) that keeps the block solvable when a zone reaches its
  pinch point.
* **`hx_cd_three_zones`** is a three-zone condenser: the refrigerant enters
  superheated, condenses at `p_cd` and leaves as liquid. From the four
  terminal temperatures it returns, per zone, the duty `Q`, the UA and the
  area, plus the total area, the refrigerant charge and the pinch.
* **`hx_ev_three_zones`** is the three-zone evaporator, written the other way
  round: it is *given* the supply and exhaust enthalpies of the refrigerant
  and the supply enthalpy of the secondary fluid, and it decides how many
  zones are active, where the phase changes, and what the exhaust enthalpy of
  the secondary fluid is. A zone with no duty is given `AU = 0` and does not
  update the pinch.
* **`single_phase_HX_eps_ntu`**, **`EV_eps_ntu`** and **`CD_eps_ntu`** are the
  three zone ratings of an automotive three-zone condenser
  (`single_phase_HX` = desuperheating/subcooling zones, `EV` = evaporating
  zone, `CD` = condensing zone). Their heat-transfer coefficient is written
  as a pair of *thermal resistances* that scale with the mass flow rates,

  > `AU = alpha/(C_cf·ṁ_cf^(−n_cf) + C_hf·ṁ_hf^(−n_hf))` (single phase),
  > `AU = alpha/(C_cf·ṁ_cf^(−n_cf) + C_r·ṁ_r^(−n_r))` (condensing),
  > `AU = 1/(R_hf + R_r)` (evaporating)

  where `alpha` is the surface fraction of the zone, and the effectiveness is
  the counterflow ε-NTU relation for the single-phase zone and the
  latent-heat relation `ε = 1 − exp(−NTU)` for the two two-phase zones.
* **`evaporator2_eps_ntu`** splits an evaporator into a boiling and a
  superheating zone on the secondary side; the two-phase zone is rated with
  `AU = −C_sf·ln(1 − ΔT/ΔT_max)` (latent heat) and the vapour zone with
  `AU = Q/ΔT_lm` and an ε-NTU effectiveness used as a diagnostic.

## Model

| Procedure | Source | Kind of zone | Outputs |
|---|---|---|---|
| `lmtd_xi1000` | `LMTD.EES` (TM-0579), also in TM-0564/TM-0569 | — | `DELTAT_log` [K] |
| `hx_cd_three_zones` | `condenseur 3 zones.EES` (TM-0564) | condenser, liquid / two-phase / vapour | `A_cd` [m²], `M_fluid` [kg], `pinch` [K], `Q_dot_cd` [W] |
| `hx_ev_three_zones` | `evaporator 1 2 & 3 zones SQ110729.EES` (TM-0569) | evaporator, liquid / two-phase / vapour | `h_sf_ex_ev` [J/kg], `Q_dot_ev` [W], `A_l`, `A_tp`, `A_v` [m²], `pinch` [K] |
| `single_phase_HX_eps_ntu` | `epsilon NTU single phase - EV - CD SQ081222.EES` (TM-0566) | desuperheating / subcooling | `Q_dot` [W], `epsilon`, `NTU`, `AU` [W/K] |
| `EV_eps_ntu` | same file | evaporating | `Q_dot` [W], `epsilon`, `NTU`, `AU` [W/K], `P_ev_out`, `P_crit_ev` [Pa] |
| `CD_eps_ntu` | same file | condensing | `Q_dot` [W], `epsilon`, `NTU`, `AU` [W/K], `P_cd_out`, `P_crit_cdz` [Pa] |
| `evaporator2_eps_ntu` | `Evaporator epsilon-NTU SQ080311.EES` (TM-0571) | evaporator, two-phase / vapour | `T_sf_ex_ev` [°C], `Q_dot_ev` [W], `AU_ev_l`, `AU_ev_tp`, `AU_ev_v` [W/K] |

`lmtd_xi1000` is byte-identical in `LMTD.EES` (TM-0579) and in the two
three-zone files; it is transcribed **once** and both call sites use it. The
two three-zone procedures are close relatives but keep their own equations
(the condenser works in temperatures, the evaporator in enthalpies, and the
evaporator decides the phase distribution itself), so they are kept apart.

`EV_eps_ntu` and `CD_eps_ntu` are the same procedure with the two fluids
exchanged (`hf` ↔ `cf`, `t_ev` ↔ `t_cd`) — they are kept as the two
functions of the source file because they are called as such, but they are
the two branches of one model: see *Not merged* below.

### The correlation constants are calibrated data, not physical constants

Every coefficient that appears inside a procedure (`h_l_nom = 425.8`,
`h_tp_nom = 1453`, `C_cf = 0.1993E−3`, `n_cf = 0.5`, …) is a fitted value of
the laboratory model, valid for the fluid and the geometry of its source
file. The procedures take no geometry: they cannot be used for another
exchanger than the one they were fitted on.

### Known defect of TM-0566, kept as it is

In `single_phase_HX_eps_ntu` the cold-fluid heat capacity is evaluated on the
**hot** fluid:

```
cp_cf = specheat(hf$, T = t_bar_cf, P = P_bar_cf)   "!Air properties (as in the original)"
cp_hf = specheat(hf$, T = t_bar_hf, P = P_bar_hf)
```

The same procedure in `CSL-0008` (Cristian Cuevas, Universidad de
Concepción), from which the laboratory file descends, reads
`cp_cf = specheat(cf$, ...)`. The transcription keeps the defect (the file is
the reference), and the demonstration program reports both heat capacities and
the effectiveness the procedure would give with the cold fluid
(`epsilon_sp` against `epsilon_sp_cf`).

### Not merged

- The three `LOOKUP('ev', i, j) = …` write statements of `hx_ev_three_zones`
  (the laboratory stores the zone enthalpies and temperatures in an external
  table for its post-processing). They are kept, valid EES, but CoolSolve does
  not execute them — see `CS-BUG-LOOKUP-WRITE`.
- `P_ev`/`P_crit` (`EV_eps_ntu`) and `P_cd`/`P_crit` (`CD_eps_ntu`) are
  computed by the source procedures and used by none of their equations; they
  are declared as outputs here so that the transcription is identical, and
  renamed (`P_ev_out`, `P_crit_ev`, `P_cd_out`, `P_crit_cdz`) because a
  procedure body shares the variable namespace of the calling program in
  CoolSolve: `P_ev` would collide with the evaporating pressure of the
  `hx_ev_three_zones` demonstration and `P_crit` with the one of the other
  procedure.

## How to run

Open `three_zone_hx_procedures.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./three_zone_hx_procedures.eescode
```

The file solves in 24 Newton iterations (largest algebraic block: 6
equations). `three_zone_hx_procedures.initials` is **required**: it fixes the
only unknown of the main program, the evaporating pressure `p_ev2` of the
`evaporator2_eps_ntu` demonstration. Without the guess the Newton solver
converges to a second, unphysical solution of the same equations
(`p_ev2 = 3.00 MPa`, `AU_ev_v2 = −941 W/K`, i.e. a negative vapour-zone UA).
With the guess of the source file's stored solution (`1.263 MPa`) the solver
returns to the physical branch (`1.302 MPa`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these procedures copies their
definitions in a block `{--- Library functions copied from CSL-0112 ---}` and
lists `CSL-0112` in its `related` field.

## Results

Values of the demonstration program (full precision in
`three_zone_hx_procedures.sol`):

**`lmtd_xi1000`, the four branches** (terminal temperatures in °C)

| case | `T_hf_su` | `T_hf_ex` | `T_cf_su` | `T_cf_ex` | `DELTAT_log` [K] | branch |
|---|---:|---:|---:|---:|---:|---|
| 1 | 100 | 60 | 20 | 60 | 40.0000 | equal terminal differences (singular form avoided) |
| 2 | 10 | 5 | 3.5 | 8.5 | 1.5000 | plain counterflow difference (the stored value of the source file) |
| 3 | 30 | 25 | 24.5 | 26 | 4.3194e−3 | `T_cf_su` ≥ `T_hf_ex`−1: pinch at the cold supply, regularised with `xi(T_cf_su+1−T_hf_ex)` |
| 4 | 30 | 26 | 20 | 31 | 1.3946e−3 | temperature cross-over (`T_cf_ex` > `T_hf_su`), regularised with `xi(T_cf_ex+1−T_hf_su)` |
| 5 | 30 | 26 | 28 | 31 | 1.6653e−7 | temperature cross-over at both ends, both terms regularised |

**`hx_cd_three_zones`** (R245fa / water, `p_cd` = 343.2 kPa, `ṁ_r` = 0.2594 kg/s,
`ṁ_sf` = 2 kg/s, water 39.62 → 46.03 °C, refrigerant 79.31 °C → saturated
liquid − 1 K):

| Quantity | value |
|---|---:|
| `A_cd` total area (the three zone areas are internal to the procedure, as in the source file) | 7.9009 m² |
| `M_fluid` charge | 9.5131 kg |
| `pinch` | 4.7815 K |
| `Q_dot_cd` = secondary-side duty (energy balance) | 53 620.97 W = 53 620.97 W |

**`hx_ev_three_zones`** (R123 / water, `p_ev` = 200 kPa, `ṁ_r` = `ṁ_sf` =
0.1 kg/s, water 170 °C at 1 MPa, refrigerant 200 kJ/kg → 340 kJ/kg, total
area 1 m²):

| Quantity | value |
|---|---:|
| `Q_dot_ev` = secondary-side duty (energy balance) | 14 000 W = 14 000 W |
| `A_l`, `A_tp`, `A_v` | 0.7607, 0.2327, 0 m² (sum 0.9933 m²) |
| `h_sf_ex_ev` | 579 197 J/kg |
| `pinch` | 100.95 K |
| `T_r_su_ev`, `T_r_ex_ev` (read back from the enthalpies) | −0.063 °C, 48.05 °C |

The evaporator runs entirely in its two-phase zone (the refrigerant enters as
a two-phase mixture and leaves as a two-phase mixture), so the vapour zone
has no area and the 1 m² is shared between the liquid and the boiling zone,
as expected.

**`single_phase_HX_eps_ntu`, `EV_eps_ntu`, `CD_eps_ntu`** (the operating
points and correlation constants of `CSL-0008`, an air-cooled R134a
condenser):

| Procedure | `AU` [W/K] | `NTU` | `epsilon` | `Q_dot` [W] |
|---|---:|---:|---:|---:|
| `single_phase_HX_eps_ntu` (desuperheating, `NTU` = 1.8997) | 902.34 | 1.8997 | 0.78517 | 13 053.4 |
| `EV_eps_ntu` (R123 at 5 °C, water 40 → 30 °C) | 3041.4 | 6.0423 | 0.99762 | 17 575.3 |
| `CD_eps_ntu` (R134a at 45 °C, air 20 → 28 °C) | 2846.1 | 1.8855 | 0.84825 | 32 009.1 |

The defect of the original costs 1.4 % on the effectiveness of the
desuperheating zone here (`epsilon_sp` = 0.78517 against `epsilon_sp_cf` =
0.79613 with the cold-fluid heat capacity): the air heat capacity is used for
both streams, but the minimum heat capacity rate is the refrigerant one, so
`NTU` is unchanged and only `epsilon` is affected.

The air-cooled zones are single-phase on the air side, so the counterflow
ε-NTU relation is the right one and `NTU ≈ 1.9` gives `ε ≈ 0.79–0.85`. The
evaporating zone of water against R123 at 5 °C is a latent-heat exchanger, so
`NTU = 6.04` gives `ε = 0.998` (nearly isothermal) and `P_ev_out` = 40.8 kPa,
the saturation pressure of R123 at 5 °C.

**`evaporator2_eps_ntu`** (R123 / humid air, `T_sf_su` = 180 °C,
`ṁ_sf` = 4 kg/s, `ṁ_r` = 0.2 kg/s, refrigerant 40 → 150 °C, total UA
800 W/K):

| Quantity | value |
|---|---:|
| `p_ev2` evaporating pressure (unknown) | 1.30241 MPa |
| `AU_ev_l2`, `AU_ev_tp2`, `AU_ev_v2` | 226.40, 454.06, 119.54 W/K |
| `Q_dot_ev2` | 47 039.5 W |
| `T_sf_ex_e2` | 173.92 °C |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the four
     branches of lmtd_xi1000 as a function of the hot-fluid exhaust
     temperature for a fixed cold-fluid profile,
     figures/three_zone_hx_procedures_lmtd.png -->

## Verification

Two kinds of verification are reported.

**1. Internal energy balance (exact).** Every procedure that couples the two
fluids must satisfy its own energy balance, and it does, to the last digit
printed:

| Procedure | primary side | secondary side | rel. diff |
|---|---:|---:|---:|
| `hx_cd_three_zones` | `Q_dot_cd` = 53 620.97039 W | `Q_dot_cd_bal` = 53 620.97039 W | 0 |
| `hx_ev_three_zones` | `Q_dot_ev` = 14 000 W | `Q_dot_ev_bal` = 14 000 W | 0 |

**2. Comparison with the EES stored solutions** of the four source files that
store one, with `CoolSolve/tools/compare_solution.py` (tolerance
`rtol = 0.001`):

```
14 common variables, 12 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 135
```

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `DELTAT_2` (`LMTD.EES`, TM-0579) | 1.5 | 1.5 | 0 |
| `AU_2` (`AU = 1/DELTAT`, TM-0579) | 0.666667 | 0.666667 | 0 |
| `A_cd` (TM-0564) | 7.62154 | 7.90094 | **3.5e-02** |
| `M_fluid_cd` (TM-0564) | 8.88765 | 9.51313 | **6.6e-02** |
| `pinch_cd` (TM-0564) | 4.96284 | 4.78148 | **3.7e-02** |
| `Q_dot_ev` (TM-0569) | 13 824.6 | 14 000 | **1.3e-02** |
| `h_sf_ex_ev` (TM-0569) | 581 150 | 579 197 | **3.4e-03** |
| `pinch` (TM-0569) | 101.744 | 100.953 | **7.8e-03** |
| `p_ev2` (TM-0571) | 1.26325e+06 | 1.30241e+06 | **3.0e-02** |
| `T_sf_ex_e2` (TM-0571) | 168.306 | 168.500 | **1.2e-03** |
| `Q_dot_ev2` (TM-0571) | 47 842.9 | 47 039.5 | **1.7e-02** |
| `AU_ev_l2` (TM-0571) | 224.869 | 226.397 | **6.8e-03** |
| `AU_ev_tp2` (TM-0571) | 444.677 | 454.061 | **2.1e-02** |
| `AU_ev_v2` (TM-0571) | 130.454 | 119.543 | **8.4e-02** |

The largest deviation is **8.4e-02** (`AU_ev_v2`), so the status of the model
is *runs*, not *verified*: the tolerances of CoolSolve
`docs/ees_import.md` §11 (≤ 0.5 % typical for a different equation of state)
are exceeded. The deviations are explained, not unexplained:

- **`lmtd_xi1000`, `EV_eps_ntu`, `CD_eps_ntu`, `single_phase_HX_eps_ntu` are
  exact.** The LMTD procedure has no property call at all: its five
  demonstration cases were recomputed independently in Python (same `if`
  tree, same `xi = 1000`) and agree to 10 significant digits (4.319446230207e−3
  against 4.319446230206e−3, 1.394579276740e−3 against 1.394579276740e−3,
  1.665278657192e−07 against 1.665278656906e−07). The other three have no
  stored EES solution (their source file, `epsilon NTU single phase - EV - CD
  SQ081222.EES`, is EES X8.198 and its variable records could not be decoded,
  see `CS-BUG-EXTRACT-FMT-BYTE`), so they are checked on the published
  relations they implement (counterflow ε-NTU, `ε = 1 − exp(−NTU)`) and on
  `CSL-0008`, whose `single_phase_HX` is the same procedure.
- **`hx_cd_three_zones` (+3.5 % on the area, +6.6 % on the charge, −3.7 % on
  the pinch)** — the demonstration point of the source file sits **exactly on
  the saturation line**: `T_ex_cd` = 49.99 °C is the saturation temperature of
  R245fa at `p_cd` = 343 220 Pa in EES. Three things happen there:
  (i) the subcooling zone of the procedure is *degenerate* — its duty is
  `ṁ_r·(h_sat,l − h(T_ex_cd))`, which is 0 at the saturation point and becomes
  −45.7 kW as soon as the exhaust state is only 0.08 K superheated, so the
  whole zone appears or disappears over a hundredth of a kelvin; (ii) CoolProp's
  saturation line of R245fa is **0.09 K lower** than the EES one there (EES
  49.99 °C against CoolProp 49.906 °C at 343.22 kPa), so the same (p, T) state
  falls on the vapour side and the total area becomes **−6.85 m²**;
  (iii) a state *on* the saturation line cannot be evaluated at all:
  `enthalpy(R245fa, p = 343220, t = T_sat(R245fa, p = 343220))` returns NaN
  from CoolProp, and CoolSolve then reports *"CoolProp returned invalid
  result (NaN or Inf)"* and exits with code 1 (unverified suggestion, see
  *Limitations*). A 1 K subcooling is therefore imposed
  (`DELTAT_sc_cd = 1`). The remaining 3.5 % is that subcooling (1 K of
  subcooling adds about 0.3 m² of liquid zone and takes some off the
  two-phase zone) plus the R245fa enthalpy difference between the two fluid
  databases — `CSL-0019` *orc_simple_r245fa* already documents a systematic
  +0.4–0.5 % on the R245fa saturation pressures between EES and CoolProp.
- **`hx_ev_three_zones`** is the *same file* run in its other mode: the source
  file offers two alternative equations (`A_ev_tot_pred = A_ev_tot` with
  `A_ev_tot` = 1 m², or the commented-out `h_r_ex_ev = 3.4E5`), and its
  stored solution was produced by the first one (`h_r_ex_ev` = 338 246 J/kg,
  i.e. 0.5 % from the second). The demonstration program uses the commented
  alternative `h_r_ex_ev = 3.4E5` — the only way to keep every variable of the
  model determined (see *Conversion log*) — and then
  `A_l + A_tp + A_v` = 0.9933 m², i.e. **−0.67 %** on the 1 m² of the stored
  solution: the source's two alternative equations agree with each other and
  with CoolSolve to that accuracy. The remaining differences
  (`h_sf_ex_ev` −0.34 %, `pinch` −0.78 %) come from the R123 saturation
  properties. The stored values of `A_l`, `A_tp`, `A_v`, `A_ev_l`, `A_ev_tp`
  and `A_ev_v` were **not** compared: they are stale (they belong to a
  previous revision of the file — `A_ev_l + A_ev_tp + A_ev_v` = 1 m² exactly,
  the total imposed by the *other* alternative equation, while
  `A_l + A_tp + A_v` = 9.6 m², and `h_sf_n`, `M_dot_sf_ref`, `M_dot_r_ref` are
  literals of the procedure that are also stored as if they were unknowns).
- **`evaporator2_eps_ntu` (+3.0 % on the pressure, −8.4 % on the vapour-zone
  UA)** — the imposed 800 W/K of total UA is met at a pressure 3 % higher
  than EES's, and the three zone UAs move accordingly. The secondary fluid is
  humid air, whose enthalpy reference and heat capacity differ between EES's
  `Air_ha` and CoolProp's `AirH2O`; the duty, which is a pure R123
  enthalpy difference, is −1.7 %, and the exhaust air temperature, a
  temperature, −0.11 %. The vapour-zone UA is the most sensitive quantity of
  the whole file: it is `Q_dot_v/ΔT_lm` and both terms nearly cancel
  (the two `ΔT_lm` end points of the zone differ by less than 1 K out of 30).
  The two-phase zone UA, `−C_sf·ln(1 − ΔT/ΔT_max)`, is at +2.1 % and the
  liquid-zone UA at +0.68 %.

## Source and attribution

Five EES files of the *Laboratoire de Thermodynamique*, Université de Liège
collection, all in `~/Nextcloud/thermo_models/procedures EES/`. The four that
name an author in their file name carry the initials `SQ` (Sylvain Quoilin):
`evaporator 1 2 & 3 zones SQ110729.EES`, `epsilon NTU single phase - EV - CD
SQ081222.EES`, `Evaporator epsilon-NTU SQ080311.EES` and `LMTD.EES`.
`condenseur 3 zones.EES` carries only the licence tag
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege
Owner}`, so its author is `TBD (ULiège, J. Lebrun laboratory)` — to be
completed by the maintainer. All files are in the SI-°C-Pa-J unit system
(`$UnitSystem SI MASS DEG PA C J`); **no unit conversion was needed** and the
directive was removed as required by the style guide.

The scientific reference quoted in the header of `single_phase_HX_eps_ntu`
is the one of the family of procedures the file belongs to (Cuevas C. et
Winandy E. 2002, *Simplified 3 zones modelling of a car air-conditioning
condenser*, IIR Zero Leakage – Minimum Charge Conference, Stockholm; Cuevas
C., Winandy E. et Lebrun J. 2003, *Modelling of an air condenser working in
critical zone for engine cooling by refrigeration loop*, Vehicle Thermal
Management Systems, Brighton; Cuevas C. 2006, PhD thesis, *Contribution to the
modelling of refrigeration systems*). The laboratory file cites no other
reference: the ε-NTU relations it uses (counterflow, and
`ε = 1 − exp(−NTU)` for a latent-heat exchanger) are the classical ones of
Incropera et al., *Introduction to Heat Transfer*, and Shah & Sekulic,
*Fundamentals of Heat Exchanger Design*.

The same procedure family is already in the library as `CSL-0008`
*condenser_three_zones* (Cristian Cuevas, Universidad de Concepción), which
contains a `single_phase_HX` and a `two_phase_CD` written for the same
condenser but with the crossflow ε-NTU relation and with the refrigerant
pressure drops; the laboratory file is the same model with the counterflow
relation and without pressure drops. They coexist: `CSL-0008` rates one
condenser, this file is the reusable procedure set of the laboratory.

## Conversion log

- **2026-10-07 — import (T-FUNC card C-123, candidates TM-0564, TM-0569,
  TM-0579, TM-0566, TM-0571).** `ees_extract.py` on the five source files; all
  five are in `SI MASS DEG PA C J`, so no manual unit conversion
  (ees_import.md §6) was needed and the `$UnitSystem` directive was dropped.
  No `MODULE`/`SUBPROGRAM` (decision D10) and no (T, H) property call
  (decision D11) in these five files, so neither decision applies.
  The `lookup('ev', …)` write statements of TM-0569 are kept as they are.
- **`lmtd_xi1000`**: the procedure is byte-identical in `LMTD.EES` (TM-0579),
  `condenseur 3 zones.EES` (TM-0564) and `evaporator 1 2 & 3 zones
  SQ110729.EES` (TM-0569) (checked equation by equation, comments stripped);
  it is transcribed **once** under a library-unique name and all three call
  sites use it, as workflow §4 requires.
- **Names**: every procedure was renamed for library-wide uniqueness
  (workflow §4.4), because `single_phase_HX` is already the name of a
  procedure of `CSL-0008` and `lmtd`, `hx_cd`, `hx_ev`, `EV`, `CD`,
  `evaporator2` are the bare names of the source files:
  `lmtd` → `lmtd_xi1000`, `hx_cd` → `hx_cd_three_zones`, `hx_ev` →
  `hx_ev_three_zones`, `single_phase_HX` → `single_phase_HX_eps_ntu`,
  `EV` → `EV_eps_ntu`, `CD` → `CD_eps_ntu`, `evaporator2` →
  `evaporator2_eps_ntu`. Argument and local names are unchanged. No equation
  was changed.
- **Output added to `hx_cd_three_zones`**: `Q_dot_cd` is added to the output
  list. It is computed by the source procedure but not returned; the
  demonstration program needs it to print the energy balance of the procedure.
- **Outputs added and renamed in `EV_eps_ntu` / `CD_eps_ntu`**: `P_ev` and
  `P_cd`, `P_crit` are computed by the source procedures and used by none of
  their equations; CoolSolve rejects a call that provides more outputs than
  the procedure declares, so they are declared, and renamed (`P_ev_out`,
  `P_crit_ev`, `P_cd_out`, `P_crit_cdz`) because a procedure body shares the
  namespace of the calling program. Values unchanged (40 820.94 Pa = the
  saturation pressure of R123 at 5 °C; 4 059 276 Pa = the critical pressure of
  R134a).
- **Main program of the `hx_ev_three_zones` demonstration**: the source file
  ends with two *alternative* equations and asks the user to comment one out
  (`"Comment one of the two equations below:"`: `A_ev_tot_pred = A_ev_tot` or
  `//h_r_ex_ev = 3.4E5`) — as it stands the file is one equation too many.
  The commented alternative `h_r_ex_ev = 3.4E5` is used here, and
  `A_ev_tot_pred = A_l + A_tp + A_v` plus its residual against the 1 m² of the
  source file are reported. This is the only form in which every variable of
  the demonstration is determined: with `A_ev_tot_pred = A_ev_tot` as the
  second equation (the EES way), CoolSolve treats the duplicate left-hand side
  as a *check* equation and aborts with *"Check equation failed: residual =
  1.4 … overdetermined or inconsistent system"*. The two dead inputs
  `T_r_su_ev` and `T_r_ex_ev` of the source file are read back from the
  enthalpies instead of being declared and unused.
- **Main program of the `hx_cd_three_zones` demonstration**: `T_ex_cd` is
  `T_sat(R245fa, p_cd) − DELTAT_sc_cd` with `DELTAT_sc_cd = 1 K` instead of the
  literal `49.99 °C` of the source file, because that literal *is* the
  saturation temperature in EES and a state on the saturation line cannot be
  evaluated in CoolSolve (see *Verification*). No other input is changed.
- **Main programs of the four ε-NTU procedures**: TM-0566 has **no**
  demonstration program (its stored solution could not be decoded, EES X8.198
  layout), so demonstration points had to be written. The operating points and
  the correlation constants of the three-zone condenser of `CSL-0008` were
  used (air-cooled R134a condenser, `t_r_sat` = 45 °C, `DELTAT_oh` = 10 K,
  `ṁ_r` = 0.5 kg/s, `ṁ_cf` = 1.5 kg/s, air 20 → 28 °C, `C_cf` = 0.1993E−3,
  `n_cf` = 0.5, `n_r` = 0.8, `C_r_sh` = 0.03384E−3 for the desuperheating zone,
  `C_r_tp` = 0.00744E−3 for the condensing zone, `alpha` = 0.2 and 0.5), the
  same family of correlations the laboratory file belongs to.
- **`three_zone_hx_procedures.initials`**: `p_ev2 = 1.263E6 Pa`, the evaporating
  pressure stored in `Evaporator epsilon-NTU SQ080311.EES`. Without it the
  solver converges to a second solution with a negative vapour-zone UA (see
  *How to run*).
- **Level**: equations 139 → 1 point (50–300); largest algebraic block 6 → 1
  point (6–30); functions/procedures present → 1; multi-zone (three zones per
  procedure, two coupled fluids) → 1; semi-empirical calibration (fitted
  coefficients scaled with the mass flow rates) → 1; curated guesses required →
  1. Score 6 → **level 3**.

## Limitations and CoolSolve gaps

- **No gap blocks this model**; it is plain EES (`PROCEDURE`, `CALL`,
  `IF/THEN/ELSE`, `LOOKUP`, property calls) and it solves in CoolSolve v0.3.0.
  `missing_features` is empty.
- `CS-FEAT-IMPORT`: CoolSolve cannot yet import the procedures of a library
  file with `$INCLUDE library:…`; a model that uses them copies the
  definitions (workflow §4.5).
- **`CS-BUG-LOOKUP-WRITE`** (reported while doing this card, CoolSolve
  `docs/model_library_support.md` §5): a *statement* that writes a lookup-table
  cell, `lookup('ev', 1, 1) = M_dot_r*h_r_su_l`, is counted by CoolSolve as an
  **equation** in the main program, so a valid EES file becomes "not square"
  and refuses to run; inside a `PROCEDURE` body the same statement is silently
  dropped (no error, no warning). The three write blocks of
  `hx_ev_three_zones` are therefore dead code in CoolSolve. They are kept
  (the laboratory reads them from the external table `ev`, TM-0567/TM-0568);
  nothing in this model depends on them.
- A procedure body shares the variable namespace of the calling program: two
  procedures of the same file cannot have a local variable of the same name,
  and a local name may not collide with a variable of the calling program.
  This is why `P_ev`, `P_cd` and `P_crit` had to be renamed (see *Conversion
  log*). EES scopes them per procedure. Reported as an unverified suggestion,
  not registered.
- **Property calls on the saturation line are not usable** for R245fa in
  CoolProp: `enthalpy(R245fa, p = 343220, t = T_sat(R245fa, p = 343220))` and
  `enthalpy(R245fa, p = 343220, t = 49.906)` return NaN, and CoolSolve reports
  *"CoolProp returned invalid result (NaN or Inf) for H(R245fa) with inputs:
  P=343220 Pa, T=323.056 K"*. This is a CoolProp backend limitation, not a
  CoolSolve one, and the same file's `T_sat(R245fa, p = 343220)` = 49.906 °C
  and `pressure(R245fa, t = 50, x = 0)` = 344 208.8 Pa are consistent with
  each other. **Unverified suggestion** (no EES manual reference gathered, and
  the EES behaviour on a state exactly on the saturation line was not checked
  on the EES side), not registered.
- The correlation constants of every procedure are fitted for the fluid, the
  geometry and the mass flow rates of their source file. The procedures cannot
  size another exchanger.
- `hx_ev_three_zones` writes its zone enthalpies and temperatures into the
  external table `ev` of the laboratory (`ev.lkt`, `evaporator 1 2 & 3 zones
  SQ080603.lkt`); no companion table is shipped, since CoolSolve ignores the
  statements.

## Related models

- `CSL-0008` *condenser_three_zones*: the same three-zone condenser procedure
  family, written by Cristian Cuevas (Universidad de Concepción) — its
  `single_phase_HX` is the ancestor of `single_phase_HX_eps_ntu`, with the
  crossflow ε-NTU relation, the correct cold-fluid heat capacity and the
  refrigerant pressure drops. It also contains a `two_phase_CD`, the reduced
  sibling of `CD_eps_ntu` (`related` back-link).
- `CSL-0090` *hx_effectiveness_ntu*: the ε-NTU relations of this file written
  as pure `FUNCTION`s, with the flow arrangements and the closed forms; the
  counterflow relation used by `single_phase_HX_eps_ntu` and the
  `ε = 1 − exp(−NTU)` latent-heat relation are the counterflow and
  boiler/condenser cases of that model (`related` back-link).
- `CSL-0096` *plate_hx_heat_transfer*, `CSL-0097`
  *two_phase_nonboiling_in_tube*, `CSL-0098` *flow_boiling_in_tubes*:
  the heat-transfer coefficients a plate rating model combines with the
  effectiveness relations.
- `models/components/heat_exchangers/condenser_three_zones` variants
  (`CSL-0008:counterflow`, `CSL-0008:crossflow`) are the models that would
  consume these procedures.
- `CSL-0114` *evaporator_3_zones_plate_correlations*: the correlation-based three-zone plate evaporator of the same lab file family (Thonon/Hsieh), which rate a real plate geometry instead of the parametric UA/effectiveness relations of this library.
- CSL-0138 (hx_moving_boundary_bell): moving-boundary (Bell 2015) translation of the same zone-delimited heat-exchanger family (TESPy TSP-014).

# Cooling coil parameter identification model (PARAMID reference, wet regime)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0163`

Parameter-identification (PARAMID) reference model of a cooling and
dehumidifying coil from the ULiège model bank (Laborelec toolkit lineage):
**one measured wet-regime point** determines the coil model parameters. The
coil is a **one-zone counter-flow heat exchanger**; only the wet regime is
described. The conductance `AU` is the series combination of the air-side
convective resistance, the metal conduction resistance and the refrigerant
(brine)-side convective resistance; the air is replaced by a **fictitious
perfect gas** whose enthalpy is fixed by the wet-bulb temperature (Lebrun et
al. 1990) and the exhaust air state follows from a **fictitious
semi-isothermal exchanger** at the contact temperature (ASHRAE classical
procedure). The nominal flows are set equal to the measured ones and the
resistance ratios `ratio_R_a_r`, `ratio_R_m_a` are imposed, so the measured
capacity fixes the resistances; the computed exhaust air state is compared
with the measurement.

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (humid air); secondary refrigerant (ethylene glycol solution) through the BrineProp correlations |
| **Size** | 82 equations (largest block: 24), system square |
| **Source** | ULiège model bank — *Cooling coil PARAMID reference model*, 21 March 2008 (EES file inside `COOLINGCOIL_PARAMID_REFERENCE_MODEL_VL080321.zip`) |
| **Authors** | Vincent Lemort, Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** by `CS-GAP-NAME-PIPE`, `CS-GAP-INCLUDE`, `CS-GAP-CALL-EXPR-OUT`; the variant `cooling_coil_paramid_coolsolve.eescode` runs and is verified against the EES stored solution |

## Problem statement

A performance test of a cooling coil in the wet regime gives: atmospheric
pressure 101 300 Pa; supply air 27.8 °C dry bulb, 19.2 °C wet bulb; exhaust
air 12.5 °C dry bulb, 12.2 °C wet bulb; a 35 % ethylene glycol solution enters
at 6.7 °C and leaves at 12.1 °C with a mass flow of 1.86 kg/s. With the
ratio `ratio_R_a_r` = 1.1 (nominal air-side to refrigerant-side resistance)
and `ratio_R_m_a` = 0.05 (metal to nominal air-side resistance) imposed,
identify the coil parameters (nominal resistances `R_a_coil_n`, `R_r_coil_n`,
`R_m_coil`; nominal flows; `K|star_r_n`), i.e. compute the operating point
that the one-zone wet-coil model must reproduce: the cooling capacity, the
exhaust air state, the condensate flow and the sensible heat ratio, and
compare them with the measurements.

## Model

- **Measurement reduction** (§4.1 of the original): the brine density and
  specific heat come from the `BRINEPROP` procedure at the measured supply
  state; the measured capacity is read on the refrigerant side,
  `Q_dot_coil_meas = M_dot_r_coil_meas·c_p_r_coil_meas·(t_r_ex_coil_meas − t_r_su_coil_meas)`,
  and the unknown air flow follows from the moist-air enthalpy balance
  `Q_dot_coil_meas = M_dot_a_coil_meas·(h_a_su_coil − h_a_ex_coil_meas)` with
  the exhaust enthalpy at the measured `(T_db, T_wb)` pair. The measured
  sensible capacity, latent capacity and `SHR_meas` follow.
- **Resistances** (§4.3): `R_a_coil = R_a_coil_n·(M_dot_a_coil_n/M_dot_a_coil)^0.6`
  (laminar flow between flat plates), `R_r_coil = R_r_coil_n·(K|star_r_n/K|star_r)·(M_dot_r_coil_n/M_dot_r_coil)^m`
  (turbulent flow in circular tube) with `K|star_r = mu_r_coil^(n−m)·k_r_coil^(1−n)·c_p_r_coil^n`
  (Dittus-Boelter exponents m = 0.8, n = 0.3, Incropera and DeWitt 2002); the
  nominal flows are the measured ones (`M_dot_a_coil_n = M_dot_a_coil`,
  `M_dot_r_coil_n = M_dot_r_coil`) and `K|star_r_n = K|star_r`, so
  `R_a_coil = R_a_coil_n`, `R_r_coil = R_r_coil_n`; the two imposed ratios
  close the system once the capacity fixes their absolute level.
- **Wet coil** (§4.4–4.5): fictitious air (`R_af_coil = R_a_coil·c_p_a_coil/c_p_af_coil`,
  `C_dot_af_coil = M_dot_a_coil·c_p_af_coil`, Lewis = 1 as in the original),
  `1/AU_coil = R_af_coil + R_m_coil + R_r_coil`, counter-flow effectiveness
  `epsilon_coil_wet = (1 − exp(−NTU(1−ω)))/(1 − ω·exp(−NTU(1−ω)))`,
  `Q_dot_coil = epsilon_coil_wet·C_dot_min_coil_wet·(t_wb_su_coil − t_r_su_coil)`.
- **Air side** (§4.6): moist-air enthalpy balance with the condensate term,
  fictitious-air balance `Q_dot_coil = C_dot_af_coil·(t_wb_su_coil − t_wb_ex_coil)`;
  the exhaust state comes from the fictitious semi-isothermal contact surface,
  `epsilon_c_coil = 1 − exp(−NTU_c_coil)` with `NTU_c_coil = 1/(R_a_coil·C_dot_a_coil)`;
  `RH_su_coil` is solved from the measured `(T_db, T_wb)` supply pair through
  the implicit `wetbulb` call. The supply humidity ratio is
  `W_su_coil` = 0.0104 kg/kg and the contact temperature `t_c_coil` = 12.0 °C.
- **Outputs**: `R_a_coil_n` = 1.3144·10⁻⁴ K/W, `R_r_coil_n` = 1.1949·10⁻⁴ K/W,
  `R_m_coil` = 6.572·10⁻⁶ K/W (their ratios reproduce the two imposed values
  exactly: 1.100, 0.0500); `Q_dot_coil` = 35 944 W; exhaust air
  `t_a_ex_coil` = 12.29 °C, `t_wb_ex_coil` = 12.17 °C, `W_ex_coil` = 0.0088 kg/kg,
  `RH_ex_coil` = 0.986; condensate `M_dot_w_coil` = 2.9 g/s; `SHR` = 0.80.

| Inputs (measured point) | Value | Parameters | Value |
|---|---|---|---|
| `P_atm_meas` atmospheric pressure | 101 300 Pa | `ratio_R_a_r` resistance ratio | 1.1 |
| `t_a_su_coil_meas` / `t_wb_su_coil_meas` supply air | 27.8 / 19.2 °C | `ratio_R_m_a` resistance ratio | 0.05 |
| `t_a_ex_coil_meas` / `t_wb_ex_coil_meas` exhaust air | 12.5 / 12.2 °C | `refrigerant$` secondary refrigerant | `'EG'` |
| `t_r_su_coil_meas` / `t_r_ex_coil_meas` brine | 6.7 / 12.1 °C | `conc_r` glycol concentration | 35 % |
| `M_dot_r_coil_meas` brine flow | 1.86 kg/s | | |

In the original these twelve variables are entered in the Diagram window, so
the extraction is not square: each of them is given its **stored** value as an
equation. The stored run is the file's default operating point and is kept as
the regression case (workflow §3 / ees_import.md §8). With them the model is
exactly square (82 equations, 82 variables). The air flow
`M_dot_a_coil_meas` = 1.8093 kg/s is an **output** of the identification (not
measured): the stored value re-derives as
35 944.01/(54 474.4 − 34 608.5) = 1.8093 kg/s.

## How to run

The native file `cooling_coil_paramid.eescode` keeps the native EES syntax and
does **not** run in CoolSolve v0.3.0 (see *Limitations and CoolSolve gaps*).
The runnable variant `cooling_coil_paramid_coolsolve.eescode` changes only
what the gaps force (every change is logged in the conversion log and in the
header of the variant):

```bash
coolsolve ./cooling_coil_paramid_coolsolve.eescode
```

A `.initials` file is needed: without it the coupled block (24 equations:
effectiveness, contact surface, exhaust state) fails with *SingularJacobian*;
with the EES stored solution as initial values the model converges in 10
iterations (`System square: Yes`, 82 equations, 82 variables). To identify
another coil, replace the twelve measured/imposed values; to study the
sensitivity of the identified resistances to the imposed ratios, sweep
`ratio_R_a_r` or `ratio_R_m_a` (see the figure placeholder below).

## Results (default run of the variant)

| Quantity | CoolSolve | EES (stored) | rel. diff |
|---|---:|---:|---:|
| `R_a_coil_n` identified air-side resistance [K/W] | 1.31523·10⁻⁴ | 1.31444·10⁻⁴ | 6.0e-04 |
| `R_r_coil_n` identified refrigerant-side resistance [K/W] | 1.19567·10⁻⁴ | 1.19495·10⁻⁴ | 6.0e-04 |
| `R_m_coil` identified metal resistance [K/W] | 6.5762·10⁻⁶ | 6.5722·10⁻⁶ | 6.0e-04 |
| `AU_coil` global conductance [W/K] | 5753.4 | 5753.2 | 3.2e-05 |
| `Q_dot_coil` total cooling power [W] | 35 944.0 | 35 944.0 | < 1e-06 |
| `Q_dot_coil_meas` measured cooling power [W] | 35 944.0 | 35 944.0 | < 1e-06 |
| `M_dot_a_coil_meas` identified air flow [kg/s] | 1.8050 | 1.8093 | 2.4e-03 |
| `t_a_ex_coil` computed exhaust air dry bulb [°C] | 12.2923 | 12.2936 | 1.1e-04 |
| `t_wb_ex_coil` computed exhaust air wet bulb [°C] | 12.16611 | 12.16647 | 3.0e-05 |
| `W_ex_coil` exhaust humidity ratio [kg/kg] | 0.0088155 | 0.0087788 | 4.2e-03 |
| `RH_ex_coil` exhaust relative humidity [-] | 0.98596 | 0.98584 | 1.2e-04 |
| `M_dot_w_coil` condensate flow [kg/s] | 2.925·10⁻³ | 2.895·10⁻³ | 1.05e-02 |
| `SHR` sensible heat ratio [-] | 0.79906 | 0.80089 | 2.3e-03 |
| `epsilon_coil_wet` [-] | 0.56271 | 0.56268 | 5.1e-05 |
| `t_c_coil` contact temperature [°C] | 12.0315 | 12.0309 | 4.8e-05 |

The measured capacity (35.94 kW, read on the brine side) is reproduced
exactly by the identified coil (it is the equation that fixes the
resistances); the model exhaust air state differs from the measurement by
−0.21 K dry bulb and −0.03 K wet bulb (identification residual, the same in
EES and CoolSolve up to the property backend), and 2.9 g/s of condensate is
removed, i.e. the wet identification is consistent with the measured point.
The physical words check against the numbers: the brine leaves 5.4 K warmer
(12.1 − 6.7 °C, as a coil load must), the air is **cooled and dehumidified**
(27.8 → 12.3 °C, 10.4 → 8.8 g/kg), and the fictitious-air capacity rate
(5110 W/K) is the minimum of the two, so `omega` = 0.768 < 1.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. the identified R_a_coil_n (with R_r_coil_n and R_m_coil) or the residual
     t_a_ex_coil - t_a_ex_coil_meas vs ratio_R_a_r (no psychrometric chart in CoolSolve,
     CS-FEAT-PSYCHRO: decision D7, sweep plot), figures/cooling_coil_paramid_sweep.png -->

## Verification

The **native file cannot be solved** by CoolSolve v0.3.0 (`CS-GAP-NAME-PIPE`,
`CS-GAP-INCLUDE`, `CS-GAP-CALL-EXPR-OUT`), so the comparison concerns the
runnable variant `cooling_coil_paramid_coolsolve.eescode`, which differs from
the native file by the two changes of the conversion log. Compared with
`compare_solution.py` against the stored solution of the source EES file
(93 records, 80 of them with a value; the tool decodes 92, see below): **79 common variables, 23
differ above rtol = 0.001, maximum relative difference 1.05e-02**
(`M_dot_w_coil`, 2.925·10⁻³ against 2.895·10⁻³ kg/s).

- Property backend. All 23 deviations (1.45e-03 … 1.05e-02) have a single
  cause, the EES and CoolProp humid-air formulations: the humidity ratios
  `W_su_coil` 5.52e-03, `W_ex_coil`/`W_c_coil` 4.17e-03, the enthalpies
  `h_a_su_coil` 2.22e-03, `h_a_ex_coil` 2.11e-03, `h_c_coil` 2.18e-03,
  `c_p_af_coil` 2.32e-03, `t_dp_su_coil` 1.45e-03 — the same 0.1–0.5 % spread
  as the other humid-air models of the library (`CSL-0074` 4.8e-03,
  `CSL-0073` 2.7e-02, `CSL-0070` 4.4e-03).
- Amplified differences: `M_dot_w_coil` 1.05e-02 is proportional to
  `W_su_coil − W_ex_coil`, a difference of two humidity ratios
  (1.6206·10⁻³ against 1.5998·10⁻³ kg/kg, +1.30 % on the difference);
  `Q_dot_lat_coil` 9.09e-03 and `Q_dot_lat_coil_meas` 8.82e-03 are the
  differences of two large numbers; the `M_dot_a_coil` family (2.37e-03,
  with it `C_dot_a_coil`, `Q_dot_sens_coil`, `SHR`) follows from the enthalpy
  balance against the exact brine-side capacity.
- Purely algebraic results are reproduced exactly (< 1e-06): the brine-side
  capacity `Q_dot_coil` (it closes on the measured flow and temperatures),
  `m`, `n`, the two imposed ratios, the brine properties and
  `V_dot_r_coil_meas` (= 1.86/1051.096 = 0.00176958 m³/s). The identified
  resistances agree to 6.0e-04: their absolute level follows from the
  effectiveness equation, whose `C_dot_min_coil_wet` carries the fictitious-air
  specific heat (2.3e-03), and `AU_coil` itself agrees to 3.2e-05.

One variable of the source file (`v_a_ex_coil` = 0.8202139 m³/kg) is missing
from the extraction reference and was **decoded by hand** from the binary
(record skipped by `ees_extract.py`, already-registered tool bug `CS-BUG-EXTRACT-FMT-BYTE`, found with `CSL-0070`; this model adds extra evidence);
CoolSolve gives 0.819883 m³/kg (4.0e-04, same humid-air backend family). The
stored solution was cross-checked against the equations before use, as
required by `CS-BUG-EXTRACT-STALE`: `C_dot_r_coil_meas = 1.86·3578.655 =
6656.30 W/K`, `Q_dot_coil_meas = 6656.30·5.4 = 35 944.01 W`,
`M_dot_a_coil_meas = 35 944.01/(54 474.4 − 34 608.5) = 1.8093 kg/s`,
`epsilon_c_coil = 1 − exp(−4.0980) = 0.9834`,
`AU_coil = 1/(4.7750e-5 + 6.5722e-6 + 1.1949e-4) = 5753.2 W/K` re-derive the
stored values, so the panel is self-consistent. The parametric "Table 2"
(3335 × 2) decoded from the file is a **leftover artifact**, not measured
data: its `R_a_coil` column sweeps smoothly by ~1.6·10⁻⁶ per row (the stored
`R_a_coil` = 1.31444·10⁻⁴ is not in it) and its `k` column holds 791 stray
entries (574 zeros, a few 1/0.2 and absurd values like −1.6·10⁺⁹²), so it is
not used as a reference. The 11 records cleared to −9999 (`C_dot`, `c_p`,
`AU`, `R`, `P`, `t[1..3]`, `W[1..3]`) and the leftovers `LAT` (guess 13),
`a` (guess 1), `t` (0.00041 m) are not variables of the model (Diagram-window
remains) and are dropped.

## Source and attribution

ULiège model bank (Laborelec toolkit lineage), *cooling coil parameters
identification model* (PARAMID reference), dated 16 January 2008 (file name
suffix `VL080321`), by **Vincent Lemort** and **Jean Lebrun** (University of
Liège, Thermodynamics Laboratory; the EES licence tag
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}`
confirms the laboratory). The same theory (fictitious wet-bulb gas,
semi-isothermal contact surface, three resistances in series) is published in
Lemort, V., C. Cuevas, J. Lebrun, I.V. Teodorese, *Development of simple
cooling coil models for simulation of HVAC systems*, ASHRAE Transactions
114(1), 2008, and in the references cited by the file itself (Lebrun et al.
1990; ASHRAE 2000; Incropera and DeWitt 2002). The zip carries the laboratory
disclaimer (freely distributed, may not be sold or distributed for commercial
purposes, cite the origin).

Source file (EES 7.888, equations stored as RTF), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Cooling_Coil/COOLINGCOIL_PARAMID_REFERENCE_MODEL_VL080321.zip!/COOLINGCOIL_PARAMID_REFERENCE_EES_MODEL_VL080321.EES`
(inventory candidate `TM-0470`). The zip also contains a compiled `.EXE`
version of the model, not imported. The model calls the laboratory's
`Brineprop` library procedure, which is **not** in this zip: it is library
model `CSL-0079` *brineprop_secondary_refrigerants* (inventory `TM-0479`,
with its two binary `.lkt` tables), extracted from
`.../AHU_Components/Recovery_Systems/GLYCOLRECOVERYLOOP_REFSIM_EES_MODEL_SB080116.zip!/UserLib/BrineProp/Brineprop.lib`.

**Triage of the sibling files.** The three cooling-coil files of the folder
are **different levels of detail and are kept as separate, linked models**
(workflow §2; decision of card C-137, confirmed by an equation review): the
parameter-identification model of this card (`TM-0470` → `CSL-0163`), the
RefSim simulation model `TM-0471` (→ `CSL-0074`), which describes the dry and
wet regimes simultaneously and selects the regime of largest capacity, and
the simplified model with control `TM-0472` (→ `CSL-0073`), which drops the
refrigerant side. They have no `duplicate_group`.

## Conversion log

- **2026-10-09 — import** (`tools/ees_extract.py`): equations stored as
  **RTF** (trailing NUL byte stripped, `CS-BUG-EXTRACT-NUL`); unit system
  already `SI MASS DEG PA C J`, so **no unit conversion**; one embedded
  parametric table decoded (see *Verification*: leftover artifact, not used);
  licence tag removed; the header was replaced by the standard one and the
  comments of the original were kept (typos of the original corrected:
  `efficieny` → *efficiency*, `Sensinble` → *sensible*, `threats` → *treats*).
  Every equation and every value of the original is unchanged.
- **Variables of the Diagram window restored as equations.** The eight
  measured inputs, the two imposed ratios, `conc_r` and `refrigerant$` are
  only referenced, never assigned, in the equations window; each of the
  twelve variables is given its **stored** value as an equation — the stored
  solution is the file's default operating point and is kept as the
  regression case. With them the model is exactly square (82 equations, 82
  variables). The extracted variable records also contain stale Diagram-window
  leftovers (`LAT`, `a`, `t`, and eleven −9999 records), dropped.
- **`refrigerant$ = 'EG'` documented decision.** The string value is not
  exported by the extractor (the stored run used the Diagram window); `'EG'`
  is taken from the RefSim sibling `CSL-0074` (same coil family, same 35 %
  concentration) and is consistent with the stored brine density
  (1051.096 kg/m³ at 6.7 °C for EG 35 %; `CSL-0079` gives 1051.355 kg/m³ at
  6 °C, PG 35 % would be ≈ 1044 kg/m³).
- **Units in comments.** Temperatures, powers, resistances, conductances,
  viscosities, conductivities and heat capacities carry their SI unit;
  `K|star`, `NTU`, `omega`, `epsilon`, `RH`, `SHR` and the two ratios are
  dimensionless `[-]`.
- **Observable `V_dot_r_coil_meas` is an output.** The original computes the
  refrigerant mass flow from a measured volume flow
  (`M_dot_r_coil_meas = V_dot_r_coil_meas·rho_r_coil_meas`); the stored run
  (mass flow 1.86 kg/s exactly, volume flow 0.00176958 m³/s recomputed from
  it) shows the mass flow was the Diagram input, so `M_dot_r_coil_meas` is
  given the stored value and `V_dot_r_coil_meas` stays an output.
- **`v_a_ex_coil` reference value hand-decoded.** The extraction reference
  misses the record of `v_a_ex_coil` although the equation
  `v_a_ex_coil = volume(AIRH2O,T=t_a_ex_coil,P=P_atm,w=W_ex_coil)` is in the
  file: `ees_extract.py` skips the record because its format byte (@+74) is 1,
  not 3 (already registered as `CS-BUG-EXTRACT-FMT-BYTE` with `CSL-0070`,
  **not re-reported here**; this model is cited as extra evidence). The record decodes
  cleanly by hand (value 0.8202139 m³/kg, units m³/kg) and is consistent with
  the CoolSolve result (4.0e-04).
- **`t_a_ex_coil` (not `t_a_ex_coil_meas`) in the exhaust volume call.** The
  original writes
  `v_a_ex_coil_meas = volume(AIRH2O,T=t_a_ex_coil,...)` (model state, not the
  measurement) and `h_a_ex_coil_meas = enthalpy(...,t=t_a_ex_coil_meas,...)`
  with the measurement; kept as in the original (both variables exist and are
  verified).
- **Runnable variant** `cooling_coil_paramid_coolsolve.eescode`, two changes,
  each forced by a CoolSolve gap (all logged in its header too):
  1. `K|star_r_n` → `Kstar_r_n` and `K|star_r` → `Kstar_r`: CoolSolve cannot
     parse the `|` character in a variable name (`CS-GAP-NAME-PIPE`; the
     register row cites this very file). The equations are unchanged.
  2. The six `CALL BRINEPROP(...)` calls are replaced by the six brine
     properties **stored by EES** for the default operating point
     (`rho_r_coil_meas` = `rho_r_coil` = 1051.096386 kg/m³,
     `c_p_r_coil_meas` = `c_p_r_coil` = 3578.654952 J/(kg·K),
     `mu_r_coil` = 3.850610191·10⁻³ Pa·s, `k_r_coil` = 0.4332900778 W/(m·K)),
     because the `Brineprop` procedure is a `USERLIB` library procedure
     (`CS-GAP-INCLUDE`, procedure of library model `CSL-0079`, reading two
     binary `.lkt` tables) and its calls return expressions
     (`c_p/1000`, `mu*1000`: `CS-GAP-CALL-EXPR-OUT`). Consequence: in the
     variant the brine properties do not vary with `conc_r` or
     `t_r_su_coil_meas`, so the identified refrigerant-side resistance is
     constant — the variant is the regression case, not a parametric brine
     model. The unit factors of the original calls are absorbed in the stored
     values (as for `CSL-0074`). The BrineProp procedure itself is available
     as library model `CSL-0079` for models that can include it.
- **No figure-ready state arrays.** This is a humid-air (`AirH2O`) component
  model, for which CoolSolve has no psychrometric diagram (`CS-FEAT-PSYCHRO`,
  decision D7): its figure is a parametric sweep plot, as for `CSL-0074`.
- **Level.** Score (taxonomy.md §3): equations 82 (50–300 → 1), largest block
  24 (6–30 → 1), no function or array defined in the file (0), single zone
  and single component (0), semi-empirical calibration — parameter
  identification from one measured point (1), needs curated guesses — the EES
  stored solution is needed or the 24-equation block fails
  (*SingularJacobian*) (1) → 4 → **level 3**, moved by −1 to **level 2**
  (card value) because the model is a single one-zone coil with explicit
  equations apart from the effectiveness/contact-surface loop, as for its
  sibling `CSL-0074`.

## Limitations and CoolSolve gaps

- **`CS-GAP-NAME-PIPE` — the native file does not parse.** The variable names
  `K|star_r_n` / `K|star_r` contain the pipe character; CoolSolve refuses
  every line that names them: *"Parse failed: Line 101: Could not parse
  line, Line 104: Could not parse line"* (the `K|star` definition and the
  `K|star_r_n = K|star_r` assignment). Already registered (found with
  `CSL-0074`, whose register row cites this file), **not re-reported here**;
  the runnable variant renames the two variables.
- **`CS-GAP-INCLUDE` (with `CS-GAP-LKT`) — the native file cannot be solved.**
  The six `CALL BRINEPROP('Density'|'SpecHeat'|'Dynvisc'|'thermalc', …)` calls
  resolve to the laboratory library procedure `Brineprop.lib` (and its two
  binary `.lkt` lookup tables), which CoolSolve neither loads nor can read.
  Already registered (found with `CSL-0011`), **not re-reported here**; the
  runnable variant uses the stored brine properties.
- **`CS-GAP-CALL-EXPR-OUT` — the native file cannot be solved.** Two of the
  calls return an expression, `CALL BRINEPROP('SpecHeat',…:c_p_r_coil_meas/1000)`
  and `CALL BRINEPROP('Dynvisc',…:mu_r_coil*1000)` (the procedure returns
  kJ/(kg·K) and mPa·s). Already registered (found with `CSL-0072`),
  **not re-reported here**; the runnable variant absorbs the factors in the
  stored values.
- Physical limitations of the model itself: one zone, wet regime only (the
  measured point must be wet — the card's dry-regime counterpart is the
  RefSim sibling `CSL-0074`); the two ratios `ratio_R_a_r`, `ratio_R_m_a` are
  imposed inputs of the identification, so the three resistances are
  determined only up to these assumptions; `Q_dot_coil_meas` is read on the
  brine side only (no independent air-side measurement of the capacity); the
  condensate is assumed at the contact temperature; `t_w_coil = t_c_coil`.
- Tool bug met with this model: **`CS-BUG-EXTRACT-FMT-BYTE`** (already
  registered with `CSL-0070`, extra evidence added to the row, not a new
  registration) —
  `tools/ees_extract.py` skips a well-formed variable record whose format
  byte (@+74) is not 3 (here `v_a_ex_coil`, format byte 1, decoded by hand);
  see *Verification*; the row exists, this model only adds evidence.

## Related models

- `CSL-0074` *cooling_coil_refsim*: the RefSim sibling of the same model bank
  and authors — the simulation counterpart (dry + wet regimes, regime of
  largest capacity) of the identification model of this card; same
  fictitious-gas and contact-surface theory, same `Brineprop` calls.
- `CSL-0073` *cooling_coil_with_control_simplified*: the simplified model of
  the same component of the same model bank, with a control law and no
  refrigerant side.
- `CSL-0079` *brineprop_secondary_refrigerants*: the BrineProp library whose
  `BRINEPROP` procedure the original calls (ethylene-glycol properties of the
  coil).
- `CSL-0017` *chilled_water_cooling_coil*: chilled-water cooling coil of the
  same air-handling family, dry and wet regimes resolved in several zones.
- `CSL-0162` *glycol_runaround_recovery_loop*: the same Braun wet-coil
  formulation applied to the two coils of a run-around heat-recovery loop
  (import of the same model bank, card C-154).

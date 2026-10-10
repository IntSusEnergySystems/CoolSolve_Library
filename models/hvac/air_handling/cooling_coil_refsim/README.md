# Cooling coil RefSim model (dry and wet regimes)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0074`

Reference simulation model (RefSim) of a cooling and dehumidifying coil from
the ULiège model bank (Laborelec toolkit lineage). The coil is a **one-zone
counter-flow heat exchanger** in which the fully dry and the fully wet regimes
are described simultaneously; the regime kept is the one giving the **largest
coil capacity** (Braun hypothesis, Braun et al. 1989). The global heat-transfer
conductance `AU` is the series combination of the air-side convective
resistance, the metal conduction resistance and the refrigerant-side
convective resistance; the latter scales with the brine properties through the
`K|star` coefficient. In the wet regime the air is replaced by a **fictitious
perfect gas** whose enthalpy is fixed by the actual wet-bulb temperature
(Lebrun et al. 1990) and the outlet air state is obtained with a **fictitious
semi-isothermal exchanger** (contact temperature, ASHRAE classical procedure).
The model computes both regimes, the selected regime, the coil capacity, the
exhaust air and refrigerant states and the condensate flow rate.

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (humid air); secondary refrigerant (ethylene glycol solution) through the BrineProp correlations |
| **Size** | 77 equations, 59 blocks (largest block: 19) |
| **Source** | ULiège model bank — *Cooling coil RefSim model*, 18 March 2008 (EES file inside `COOLINGCOIL_REFSIM_MODEL_VL080318.zip`) |
| **Authors** | Vincent Lemort, Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0, re-checked with 0.3.0@57b22d3 — native file **blocked** by `CS-GAP-NAME-PIPE`, `CS-GAP-INCLUDE`, `CS-GAP-IFSTR` (`CS-GAP-IF5` and `CS-GAP-CALL-EXPR-OUT` are closed in CoolSolve `fix/library-gaps-2`, @59b2862 and @57b22d3); the variant `cooling_coil_refsim_coolsolve.eescode` runs and is verified against the EES stored solution |

## Problem statement

Air at 30 °C and 50 % relative humidity (101 325 Pa in the diagram window of
the original, **98 000 Pa in the stored run**) enters a cooling coil at
1.8 kg/s of dry air; a 35 % ethylene glycol solution enters the other side at
1.7 kg/s and 6 °C. The coil is a one-zone counter-flow exchanger with an
air-side thermal resistance `R_a_coil_n` = 1.319·10⁻⁴ K/W, a refrigerant-side
resistance `R_r_coil_n` = 1.199·10⁻⁴ K/W and a metal resistance
`R_m_coil` = 6.596·10⁻⁶ K/W, rated at nominal flows of 1.803 kg/s of air and
1.866 kg/s of brine. Determine the dry and the wet capacity, the regime that
governs, the exhaust air temperature, humidity ratio and relative humidity,
the exhaust refrigerant temperature, the condensate flow rate and the sensible
heat ratio of the coil.

## Model

- Air side (both regimes): `c_p_a_coil`, `h_a_su_coil`, `W_su_coil`,
  `t_wb_su_coil` from the humid-air property calls; the air capacity rate is
  `C_dot_a_coil = M_dot_a_coil·c_p_a_coil` and, in the dry regime, the air is
  not dehumidified (`W_ex_coil_dry = W_su_coil`).
- Resistances: `R_a_coil = R_a_coil_n·(M_dot_a_coil_n/M_dot_a_coil)^0.6`
  (laminar flow between flat plates) and
  `R_r_coil = R_r_coil_n·(K|star_r_n/K|star_r)·(M_dot_r_coil_n/M_dot_r_coil)^0.8`
  (turbulent flow in circular tube), with
  `K|star_r = mu_r_coil^(n−m)·k_r_coil^(1−n)·c_p_r_coil^n` and `m` = 0.8,
  `n` = 0.3 (Dittus-Boelter exponents, Incropera and DeWitt 2002);
  `1/AU = R_a + R_m + R_r`.
- Dry regime: counter-flow effectiveness of Braun's hypothesis (one
  equation), `NTU = AU/C_dot_min`, `Q_dot_coil_dry = epsilon·C_dot_min·(t_a_su − t_r_su)`,
  and the same heat rate read on the air side
  `Q_dot_coil_dry = C_dot_a·(t_a_su − t_a_ex_coil_dry)`; the contact
  temperature `t_c_ex_coil_dry` follows from the ratio of the refrigerant-side
  and total resistances, and `DELTA_t_cond = t_dp_ex_coil_dry − t_c_ex_coil_dry`
  is positive when condensation can occur.
- Wet regime: the air side is replaced by the fictitious air
  (`R_af_coil = R_a_coil·c_p_a_coil/c_p_af_coil`, `C_dot_af_coil = M_dot_a_coil·c_p_af_coil`,
  Lewis = 1 as in the original), the capacity is
  `Q_dot_coil_wet = epsilon_coil_wet·C_dot_min_coil_wet·(t_wb_su − t_r_su)` and is
  also written on the moist-air enthalpy balance and on the fictitious-air
  balance; the exhaust state comes from the fictitious semi-isothermal contact
  surface, `epsilon_c_coil_wet = 1 − exp(−NTU_c_coil_wet)` with
  `NTU_c_coil_wet = 1/(R_a_coil·C_dot_a_coil)`.
- Regime selection and outputs: five EES **5-argument `IF(A,B,X,Y,Z)`** calls
  select the wet branch (`X`, when `Q_dot_coil_wet > Q_dot_coil_dry`) or the
  dry branch (`Z`), i.e. the branch of maximal capacity, for `Q_dot_coil`,
  `AU_coil`, `M_dot_w_coil`, `t_a_ex_coil` and `W_ex_coil`; the string
  `WetHumide$` is written the same way with `IF$`.
- Outputs: `Q_dot_sens_coil = C_dot_a·(t_a_su − t_a_ex_coil)`,
  `Q_dot_lat_coil = Q_dot_coil − Q_dot_sens_coil`,
  `RH_ex_coil = relhum(...)`, `v_a_ex_coil = volume(...)`,
  `t_r_ex_coil = t_r_su_coil + Q_dot_coil/C_dot_r_coil` and
  `SHR = Q_dot_sens_coil/Q_dot_coil`.

| Inputs (default run) | Value | Parameters | Value |
|---|---|---|---|
| `t_a_su_coil` supply air temperature | 30 °C | `refrigerant$` secondary refrigerant | `'EG'` |
| `RH_su_coil` supply relative humidity | 0.5 | `conc_r` glycol concentration | 35 % |
| `P_atm` atmospheric pressure | 98 000 Pa | `K|star_r_n` nominal properties coefficient | 106 |
| `M_dot_a_coil` air flow | 1.8 kg/s | `R_a_coil_n` nominal air-side resistance | 1.319·10⁻⁴ K/W |
| `M_dot_r_coil` brine flow | 1.7 kg/s | `R_r_coil_n` nominal refrigerant-side resistance | 1.199·10⁻⁴ K/W |
| `t_r_su_coil` brine supply temperature | 6 °C | `R_m_coil` metal resistance | 6.596·10⁻⁶ K/W |
| | | `M_dot_a_coil_n`, `M_dot_r_coil_n` nominal flows | 1.803, 1.866 kg/s |

In the original these thirteen variables are entered in the Diagram window
(`"! in diagram"`) or only exist there, so the extraction is not square: each of
them is given its **stored** value as an equation. The stored run is the
file's default operating point and is kept as the regression case
(workflow §3, step 4 / ees_import.md §8). Note that the stored run used
`P_atm` = 98 000 Pa, not the 101 325 Pa written in the comment of the
equations window: with 101 325 Pa the supply humidity ratio would be
0.013311 kg/kg against the stored 0.013771 kg/kg.

`c_p_a_coil = 1032.41 J/(kg·K)`, `W_su_coil = 0.013771 kg/kg` and
`h_a_su_coil = 65 405 J/kg` stored by EES are reproduced by the conversion
below: `0.622·0.5·4246/(98000 − 0.5·4246) = 0.013771 kg/kg` at
`p_ws(30 °C) = 4246 Pa` (the steam partial pressure is `0.5·4246` = 2123 Pa).

## How to run

The native file `cooling_coil_refsim.eescode` keeps the native EES syntax and
does **not** run in CoolSolve v0.3.0 (see *Limitations and CoolSolve gaps*). The
runnable variant `cooling_coil_refsim_coolsolve.eescode` changes only what the
gaps force (every change is logged in the conversion log and in the header of
the variant):

```bash
coolsolve ./cooling_coil_refsim_coolsolve.eescode
```

A `.initials` file is needed: without it the wet block (19 equations) reaches
*MaxIterations*; with the EES stored solution as initial values the model
converges in 13 iterations (`System square: Yes`, 77 equations, 77 variables).
To study another operating point, change the supply state or the coil
parameters; a sweep of `t_r_su_coil` (or of `M_dot_a_coil`) shows how the
selected regime switches and how the capacity and the sensible heat ratio
follow (see the figure placeholder below).

## Results (default run of the variant)

| Quantity | CoolSolve | EES (stored) | rel. diff |
|---|---:|---:|---:|
| `Q_dot_coil` total cooling power [W] | 45 165.7 | 45 135.2 | 6.8e-04 |
| `Q_dot_coil_dry` dry-regime capacity [W] | 36 126.4 | 36 123.6 | 7.8e-05 |
| `Q_dot_coil_wet` wet-regime capacity [W] | 45 165.7 | 45 135.2 | 6.8e-04 |
| `AU_coil` global conductance [W/K] | 5478.07 | 5474.89 | 5.8e-04 |
| `AU_coil_dry` / `AU_coil_wet` [W/K] | 3682.75 / 5478.07 | 3682.75 / 5474.89 | < 1e-06 / 5.8e-04 |
| `t_a_ex_coil` exhaust air temperature [°C] | 14.1169 | 14.1059 | 7.7e-04 |
| `t_wb_ex_coil_wet` exhaust wet-bulb [°C] | 14.0009 | 13.9902 | 7.7e-04 |
| `t_c_coil_wet` contact temperature [°C] | 13.8405 | 13.8296 | 7.9e-04 |
| `epsilon_c_coil_wet` contact effectiveness [-] | 0.98301 | 0.98302 | 9.4e-06 |
| `W_ex_coil` exhaust humidity ratio [kg/kg] | 0.0103100 | 0.0102606 | 4.8e-03 |
| `RH_ex_coil` exhaust relative humidity [-] | 0.98796 | 0.98796 | 6.8e-06 |
| `Q_dot_sens_coil` sensible power [W] | 29 520.2 | 29 536.5 | 5.5e-04 |
| `Q_dot_lat_coil` latent power [W] | 15 645.5 | 15 598.6 | 3.0e-03 |
| `M_dot_w_coil` condensate flow [kg/s] | 6.345·10⁻³ | 6.318·10⁻³ | 4.2e-03 |
| `t_r_ex_coil` exhaust refrigerant temperature [°C] | 13.4293 | 13.4243 | 3.7e-04 |
| `SHR` sensible heat ratio [-] | 0.65360 | 0.65440 | 1.2e-03 |
| `t_a_ex_coil_dry` dry-regime exhaust temperature [°C] | 10.5625 | 10.5614 | 1.0e-04 |
| `R_a_coil`, `R_r_coil` resistances [K/W] | 1.3203·10⁻⁴, 1.3291·10⁻⁴ | 1.3203·10⁻⁴, 1.3291·10⁻⁴ | < 1e-06 |

The **wet regime governs**: 45.2 kW against 36.1 kW in the dry regime, i.e. the
same 1.8 kg/s of air leaves at 14.12 °C with 10.31 g of water per kg of dry air
(relative humidity 0.988), and 6.35 g/s of condensate is removed. The latent
part is 15.6 kW of the 45.2 kW, hence SHR = 0.654. The brine leaves 7.43 K
warmer (`13.429 − 6` °C), i.e. 45 166 W through 6079 W/K. The physical words
check against the numbers: the *compression* is on the refrigerant side (a
7.43 K temperature **rise** across the coil, as a cooling coil must do), the air
is **cooled and dehumidified** (30 → 14.12 °C, 13.84 → 10.31 g/kg).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. Q_dot_coil (with Q_dot_coil_dry and Q_dot_coil_wet) and SHR vs t_r_su_coil, or
     Q_dot_coil vs M_dot_a_coil (no psychrometric chart in CoolSolve, CS-FEAT-PSYCHRO:
     decision D7, sweep plot), figures/cooling_coil_refsim_sweep.png -->

## Verification

The **native file cannot be solved** by CoolSolve (`CS-GAP-NAME-PIPE`,
`CS-GAP-INCLUDE`, `CS-GAP-IFSTR`; `CS-GAP-IF5` was a fourth one in v0.3.0), so the comparison concerns the runnable variant
`cooling_coil_refsim_coolsolve.eescode`, which differs from the native file by
the four changes of the conversion log. Compared with
`compare_solution.py` against the 87 variables decoded from the source EES
file: **74 common variables, 21 differ above rtol = 0.001, maximum relative
difference 7.81e-01** (`DELTA_t_cond`, 10.107 K against 2.218 K). One EES
variable (`LAT`) is not a variable of the model (leftover of the Diagram
window), and three variables of the variant (`K|star_r_n` → `Kstar_r_n`,
`Kstar_r`, `refrigerant$`) have no counterpart in the reference.

The maximum is **not** a model error: it is the stale stored value discussed
below, and the two variables concerned (`t_dp_ex_coil_dry`, 4.28e-01, and
`DELTA_t_cond`, its only user) are the only ones above 1e-02.

- Stale reference value. The equation `t_dp_ex_coil_dry =
  dewpoint(AIRH2O,T=t_a_ex_coil_dry,P=P_atm,w=W_ex_coil_dry)` is evaluated with
  `W_ex_coil_dry = W_su_coil = 0.0137708 kg/kg` at 98 000 Pa, whose dew-point
  temperature is 18.4 °C — the value the same file stores for the identical
  supply call, `t_dp_su_coil` = 18.442 °C. The stored `t_dp_ex_coil_dry`
  equals `t_a_ex_coil_dry` = 10.5614 °C exactly, i.e. it is not the dew point
  of the humidity ratio stored next to it: the decoded solution is stale for
  that variable (`CS-BUG-EXTRACT-STALE`), and `DELTA_t_cond` follows it.
  CoolSolve gives 18.4509 °C, consistent with `W_ex_coil_dry = W_su_coil`.
- Property backend. The remaining 19 deviations (1.2e-03 … 4.8e-03) have a
  single cause, the EES and CoolProp humid-air formulations: the supply
  humidity ratio `W_su_coil` 4.64e-03, the supply enthalpy `h_a_su_coil`
  2.14e-03, `c_p_a_coil` 1.3e-04, the saturated-water humidity ratios
  `W_c_coil_wet` / `W_ex_coil` 4.79e-03 and the exhaust enthalpies 3.0e-03.
  The same 0.1–0.5 % spread as the other humid-air models of the library
  (`CSL-0073` 2.7e-02, `CSL-0070` 4.4e-03, `CSL-0016` 5.1e-03).
- Purely algebraic results are reproduced to ≤ 7.9e-04: the resistances
  `R_a_coil`, `R_r_coil`, `R_af_coil` (< 1e-06 … 2.5e-03), `NTU` and
  `epsilon` of both regimes (1.6e-03 … 2.0e-03), `C_dot_a_coil` and
  `c_p_a_coil`, the contact effectiveness `epsilon_c_coil_wet` 9.4e-06, the
  dry-regime exhaust temperature `t_a_ex_coil_dry` 1.0e-04, the relative
  humidity `RH_ex_coil` 6.8e-06, the total and sensible powers 6.8e-04 and
  5.5e-04.
- Amplified differences: `Q_dot_lat_coil` 3.0e-03 (the difference of two large
  numbers, 45 165.7 − 29 520.2 W), `M_dot_w_coil` 4.2e-03 (proportional to
  `W_su_coil − W_ex_coil`, a difference of two humidity ratios) and
  `SHR` 1.2e-03.

No variable is excluded from the comparison; the three variables that only the
variant has are the renamed `K|star` coefficients and the string input
`refrigerant$`.

The stored EES solution was cross-checked against the equations before use, as
required by `CS-BUG-EXTRACT-STALE`: `C_dot_r_coil = 1.7·3576.117 = 6079.4 W/K`,
`omega_coil_dry = 1858.34/6079.40 = 0.30568`,
`Q_dot_coil_dry = 1858.34·(30 − 10.5614) = 36 123.6 W` and
`epsilon_c_coil_wet = 1 − exp(−4.0756) = 0.98302` re-derive the stored
values, so the panel is self-consistent (one operating point, not a stale mix)
for everything except the dew point of the dry exhaust air.

## Source and attribution

ULiège model bank (Laborelec toolkit lineage), *cooling coil RefSim model*, dated
16 January 2008 (file name suffix `VL080318`), by **Vincent Lemort** and
**Jean Lebrun** (University of Liège, Faculty of Applied Sciences,
Thermodynamics Laboratory; the EES licence tag
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}`
confirms the laboratory). Published in Lemort, V., C. Cuevas, J. Lebrun,
I.V. Teodorese, *Development of simple cooling coil models for simulation of
HVAC systems*, ASHRAE Transactions 114(1), 2008. The zip carries the laboratory
disclaimer (freely distributed, may not be sold or distributed for commercial
purposes, cite the origin).

Source file (EES 7.888), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Cooling_Coil/COOLINGCOIL_REFSIM_MODEL_VL080318.zip!/CoolingCoil_RefSim_EES_Model_VL080318.EES`
(inventory candidate `TM-0471`). The zip also contains a compiled `.EXE`
version of the model, not imported. The model calls the laboratory's
`Brineprop` library procedure, which is **not** in this zip and not yet in the
library: it is in another zip of the same collection,
`.../AHU_Components/Recovery_Systems/GLYCOLRECOVERYLOOP_REFSIM_EES_MODEL_SB080116.zip!/UserLib/BrineProp/Brineprop.lib`
with its two binary lookup tables `Brine1.lkt` and `Brine2.lkt` (inventory
`TM-0479`/`TM-0480`, function-library card `C-84`, roadmap `P1.9`).

**Triage of the sibling files.** The three cooling-coil files of the folder are
**different levels of detail and are kept as separate, linked models**
(workflow §2): the RefSim model of this card (`TM-0471` → `CSL-0074`), the
parameter-identification model `TM-0470` (identifies `R_a_coil_n`,
`R_r_coil_n`, `R_m_coil` and the nominal flows from one measured wet-regime
point) and the simplified model with control `TM-0472` (→ `CSL-0073`), which
drops the refrigerant side entirely. They have no `duplicate_group`.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): equations stored as **RTF**
  (trailing NUL byte stripped, `CS-BUG-EXTRACT-NUL`); unit system already
  `SI MASS DEG PA C J`, so **no unit conversion**; no lookup or parametric
  table; licence tag removed; the header was replaced by the standard one and
  the comments of the original were kept (typos of the original corrected:
  `threats` → *treats*, `Fuly` → *fully*, `regim` → *regime*, `Merckel` →
  *Merkel*, `pour calculer W_ex_coil_wet` → *to calculate W_ex_coil_wet*).
  Every equation and every value of the original is unchanged.
- **Variables of the Diagram window restored as equations.** The six inputs
  carry the comment `"! in diagram"` in the equations window, and the six
  parameters (`K|star_r_n`, `conc_r`, `R_a_coil_n`, `R_r_coil_n`, `R_m_coil`,
  `M_dot_a_coil_n`, `M_dot_r_coil_n`) plus `refrigerant$` are only referenced,
  never assigned: the equations window of the original is not square. Each of
  the thirteen variables is given its **stored** value as an equation — the
  stored solution is the file's default operating point and is kept as the
  regression case. With them the model is square (77 equations, 77 variables).
  `LAT` (13) and `a` (1) of the variable records are unused leftovers of the
  Diagram window and are dropped.
- **`P_atm` = 98 000 Pa, not 101 325 Pa.** The comment of the original says
  101 325 Pa, but the stored run used 98 000 Pa; the stored humidity ratio
  0.013771 kg/kg only follows from 98 000 Pa (0.013311 kg/kg from
  101 325 Pa). The stored value was kept, as the regression case.
- **Units in comments.** Temperatures, powers, resistances, conductances,
  conductivities, viscosities and heat capacities carry their SI unit;
  `K|star`, `NTU`, `omega`, `epsilon`, `RH` and `SHR` are dimensionless `[-]`.
- **Observable `t_wb_ex_coil` has no equation.** It is announced in the output
  list of the original (and in the header) but is never computed there; the
  model delivers `t_wb_ex_coil_wet` (and `t_wb_ex_coil_dry` = `t_a_ex_coil_dry`
  in the dry regime, since the dry exhaust air is not dehumidified). The list
  is kept as it is, as a comment.
- **Runnable variant** `cooling_coil_refsim_coolsolve.eescode`, four changes,
  each forced by a CoolSolve gap (all logged in its header too):
  1. `K|star_r_n` → `Kstar_r_n` and `K|star_r` → `Kstar_r`: CoolSolve cannot
     parse the `|` character in a variable name (`CS-GAP-NAME-PIPE`). The
     equations are unchanged.
  2. The four `CALL BRINEPROP(...)` calls are replaced by the four brine
     properties **stored by EES** for the default operating point
     (`rho_r_coil` = 1051.354719 kg/m³, `c_p_r_coil` = 3576.11699 J/(kg·K),
     `mu_r_coil` = 3.951911085·10⁻³ Pa·s, `k_r_coil` = 0.4326901231 W/(m·K)),
     because the `Brineprop` procedure is a `USERLIB` library procedure
     (`CS-GAP-INCLUDE`) that reads two binary `.lkt` files (`CS-GAP-LKT`); a
     library function model will provide them (card `C-84`). Consequence: in
     the variant the brine properties do not vary with `conc_r` or
     `t_r_su_coil`, so the refrigerant-side resistance `R_r_coil` is constant
     — the variant is the regression case, not a parametric brine model. The
     unit factors of the original calls (`c_p_r_coil/1000` because `Brineprop`
     returns kJ/(kg·K), `mu_r_coil*1000` because it returns milliPa·s) are
     absorbed in the stored values, which are the values of `c_p_r_coil` and
     `mu_r_coil` themselves.
  3. The five EES 5-argument `IF(A,B,X,Y,Z)` calls are replaced by the
     3-argument `IF` of CoolSolve, `if(Q_dot_coil_wet-Q_dot_coil_dry, X, Z)`:
     `CS-GAP-IF5`. The three-argument form is valid EES as well, but the two
     forms are not equivalent outside the regression point: the EES form
     returns `Y` when the two capacities are equal, the CoolSolve form returns
     `Z` (the dry branch).
  4. `WetHumide$ = IF$(Q_dot_coil_dry, Q_dot_coil_wet,'Wet','Wet','Dry')` is
     **removed**: CoolSolve does not implement the string intrinsic `IF$` at
     any arity (`ees_vs_coolsolve.csv` line 35 lists it as *No*; a 3-argument
     reproducer raises *"Unknown or unsupported function: if$ with 3
     arguments"*), and the string feeds no equation. The regime is still
     readable from `Q_dot_coil` and from the two capacities. **Unverified
     suggestion for the maintainer:** register the string form of the inline
     conditional (`CS-GAP-IFSTR`).
- **No figure-ready state arrays.** This is a humid-air (`AirH2O`) component
  model, for which CoolSolve has no psychrometric diagram
  (`CS-FEAT-PSYCHRO`, decision D7): its figure is a parametric sweep plot, as
  for `CSL-0070` and `CSL-0073`.
- **Level.** Score (taxonomy.md §3): equations 77 (50–300 → 1), largest block 19
  (6–30 → 1), no function or array defined in the file (0), single zone and
  single component (0), semi-empirical correlations and an operating-point
  regime switch (1), needs curated guesses — the EES stored solution is needed
  or the wet block reaches *MaxIterations* (1) → 4 → **level 3**, moved by −1
  to **level 2** (card value) because the model is a single one-zone coil with
  explicit equations apart from the effectiveness loop.
- **2026-10-10 — re-check with CoolSolve `fix/library-gaps-2` @59b2862 (T-RECHECK, `CS-GAP-IF5` closed).** The five-argument `IF` of the native file is now implemented; the native file is still blocked, the first error now comes from another gap (the parse stops at the `K|star_r_n` names, `CS-GAP-NAME-PIPE`). The variant is kept.
- **2026-10-10 — re-check with CoolSolve `fix/library-gaps-2` @57b22d3 (T-RECHECK, `CS-GAP-CALL-EXPR-OUT` closed).** The two `CALL BRINEPROP` calls with an expression output (lines 113 and 114) now parse. The native file is still blocked: the parse stops at the `K|star_r_n` names (lines 78 and 111, `CS-GAP-NAME-PIPE`) and the `BRINEPROP` library procedure is unknown (`CS-GAP-INCLUDE`), `IF$` is unknown (`CS-GAP-IFSTR`, line 188). Evidence, in a scratch copy with only `K|star_r_n`/`K|star_r` renamed `Kstar_r_n`/`Kstar_r`: the file is square (80 equations, 80 unknowns), the expression outputs become the auxiliary variables `__out1_BRINEPROP_L113` (`c_p_r_coil/1000`) and its twin of line 114, and the solve stops with *"Unknown procedure: BRINEPROP"* (`CS-GAP-INCLUDE`). The variant is kept: its change 2 (stored brine properties instead of the `CALL BRINEPROP`) is still forced by `CS-GAP-INCLUDE`/`CS-GAP-LKT`, not by the expression outputs.

## Limitations and CoolSolve gaps

- **`CS-GAP-NAME-PIPE` — the native file does not parse.** A variable name
  containing the `|` character, `K|star_r_n` and `K|star_r` in the original, is
  refused: *"Could not parse line"*, and on the line that uses them
  *"Unknown function 'K|star_r_n/K|star_r*'"* (the `/`…`*` run is read as a call).
  Reproducer (valid EES, 2 lines): `K|star_a = 106` ⏎ `K|star_b = 2*K|star_a` →
  *"Parse failed: Line 1 … Line 2: Could not parse line"*; the same file with
  `Kstar_a`/`Kstar_b` solves. Evidence that the syntax is valid EES: the two
  cooling-coil model-bank files use it, the source of this model
  (`CoolingCoil_RefSim_EES_Model_VL080318.EES`, whose lines 112 and 115 of the
  extracted equations are `K|star_r_n` and `K|star_r`) and
  `COOLINGCOIL_PARAMID_REFERENCE_MODEL_VL080321.EES` (inventory `TM-0470`),
  where it appears even in an equation, `K|star_r_n=K|star_r`; both files store
  a complete solution. Registered with this evidence; the family of the
  already-registered `CS-GAP-NAME-SYMBOL` (`C%`).
- **`CS-GAP-INCLUDE` (with `CS-GAP-LKT`) — the native file cannot be solved.**
  The four `CALL BRINEPROP('Density'|'SpecHeat'|'Dynvisc'|'thermalc', …)` calls
  resolve to the laboratory library procedure `Brineprop.lib` (and its two
  binary lookup tables `Brine1.lkt`, `Brine2.lkt`), which CoolSolve neither
  loads nor can read: the warning *"Unknown function 'BRINEPROP'"* is emitted
  and the blocks that call it cannot be evaluated. Already registered
  (found with `CSL-0011`), **not re-reported here**. The proper fix is the
  function model of card `C-84`; the runnable variant uses the stored brine
  properties.
- **`CS-GAP-CALL-EXPR-OUT` — closed in CoolSolve `fix/library-gaps-2` @57b22d3.** Two of the four
  `CALL BRINEPROP` calls use an expression as output
  (`CALL BRINEPROP('SpecHeat',…:c_p_r_coil/1000)`, line 113, and
  `CALL BRINEPROP('Dynvisc',…:mu_r_coil*1000)`, line 114); CoolSolve v0.3.0
  refused them (*"Output 1 of 'BRINEPROP' must be a variable, not the expression
  'c_p_r_coil/1000': …"*) and now accepts them (auxiliary variable
  `__out<k>_BRINEPROP_L<line>`; see the conversion log). Removed from
  `missing_features`. The variant removes the calls altogether (change 2, still
  forced by `CS-GAP-INCLUDE`).
- **`CS-GAP-IF5` — closed in CoolSolve `fix/library-gaps-2` @59b2862.** The EES intrinsic
  `IF(A,B,X,Y,Z)` raised *"Unknown or unsupported function: if
  with 5 arguments"* in CoolSolve v0.3.0 and now evaluates; it is used five times here (regime selection of
  `Q_dot_coil`, `AU_coil`, `M_dot_w_coil`, `t_a_ex_coil`, `W_ex_coil`).
  Already registered (found with `CSL-0009`, blocked `CSL-0073`),
  **not re-reported here**; the runnable variant uses `if(cond,a,b)`.
- **`CS-GAP-IFSTR` — the native file cannot be solved.** The EES string
  conditional `IF$(cond,true$,false$)` raises *"Unknown or unsupported
  function: if$ with 3 arguments"* at every arity; it is used once here, for
  the output `WetHumide$`. Reproducer (valid EES, 3 lines): `a = 1` ⏎ `b = 2` ⏎
  `s$ = IF$(a-b,'Wet','Dry')` → *"Block 2 (size 1, vars: s$) failed:
  EvaluationError - Unknown or unsupported function: if$ with 3 arguments"*.
  Newly registered with this model; the runnable variant drops `WetHumide$`
  (it feeds no equation).
- Physical limitations of the model itself: one zone (no air-side or
  temperature distribution along the coil, no frost formation, no condensate
  flow/bypass effect); the refrigerant side is a **secondary fluid** modelled
  with constant properties and no phase change, so the capacity is the largest
  of the two regimes rather than a rating; `DELTA_t_cond` is a diagnostic
  (positive means condensation is possible in the dry regime), it does not
  drive the regime switch, which compares the two capacities; `c_p_af_coil`,
  `epsilon_coil_wet` and the wet-branch resistances are outputs of the wet
  model, computed whatever the selected regime.

## Related models

- `CSL-0017` *chilled_water_cooling_coil*: chilled-water cooling coil of the
  same air-handling family, dry and wet regimes, resolved in several zones.
- `CSL-0073` *cooling_coil_with_control_simplified*: the simplified model of
  the same component of the same model bank, with a control law and no
  refrigerant side.
- `CSL-0062` *cooling_coil_condensate_ratio*: condensate ratio and dry-air flow
  at a cooling coil.
- `CSL-0070` *adiabatic_humidifier_simplified*: the simplified model of another
  air-handling component of the same ULiège model bank and author group.
- `CSL-0076` *cooling_tower_direct_contact_refsim*: the cooling tower of the
  same model bank, built on the same fictitious-fluid (wet-bulb) theory.
- `CSL-0077` *aircooled_chiller_refsim*: another model of the same ULiège model
  bank (IEA A43 PR2 A15), an air-cooled water chiller whose condenser and
  evaporator use the same three-resistances-in-series description.
- `CSL-0079` *brineprop_secondary_refrigerants*: the BrineProp library this
  model copies its `BRINEPROP` procedure from (brine properties of the
  ethylene-glycol solution of the coil).
- `CSL-0162` *glycol_runaround_recovery_loop*: the same Braun wet-coil
  formulation applied to the two coils of a run-around heat-recovery loop
  (import of the same model bank, card C-154).
- `CSL-0163` *cooling_coil_paramid*: the parameter-identification sibling of
  the same model bank and authors (card C-155): one measured wet-regime point
  identifies the resistances of the same one-zone wet-coil model.

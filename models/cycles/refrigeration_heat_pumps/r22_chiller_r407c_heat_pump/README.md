# R22 chiller with an R407C heat pump upgrading its condenser heat

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0319`

A water chiller working with R22 (0 °C evaporation, 45 °C condensation, 900 kW of cooling at full load)
rejects its condenser heat to a water circuit at 30 → 35 °C. A second machine, a heat pump working with
R407C (20 °C evaporation, 80 °C condensation), takes that heat at its evaporator and delivers it to a water
circuit heated from 60 to 70 °C. The compressor-motor groups have constant global isentropic efficiencies,
the four water-side exchangers are rated by their effectivenesses (outputs of the model). The model gives the
COP of each machine, the global COP of the installation and the part-load factors ELF (electrical power)
and CLF (cooling capacity) used to discuss part-load operation.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R22, R407C (CoolProp properties); Water (secondary circuits) |
| **Size** | 108 equations, largest block: 1 (75 equations of the original plus 33 diagram state-point equations) |
| **Source** | ULiège *Machines et systèmes thermiques*, répétition 10, exercise 4 — original EES file `MSTH-SB-R10-EX4.EES` (`thermo_models` TM-0157) |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory; initials SB of the file name) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — verified: R22 side agrees with the stored EES solution (< 0.9 %); the R407C side departs from EES 7.458 by up to 16 % because of the old EES R407C property model, while two independent CoolProp formulations agree to 2·10⁻⁴ (see Verification) |

## Problem statement

The original file has no written statement, only the equations and short comments (translated here).
It is the fourth question of the R10 chiller exercise: the R22 chiller of the previous questions
(evaporator duty 900 kW at full load, water 8 → 4 °C at the evaporator, 30 → 35 °C at the condenser,
`T_ev = 0 °C`, `T_cd = 45 °C`, 3 K of subcooling, `epsilon_s = 0.67`, motor efficiency 0.9) is completed by
a heat pump ("Ajout d'une PAC") on R407C that recovers its condenser heat. The water flow rates and the
effectivenesses of all exchangers follow from the imposed temperatures. The last comment of the
file notes that the COPs can be increased by reducing the temperature differences between evaporation and
condensation, within the limits set by the effectivenesses of the exchangers.

## Model

R22 chiller (states 1 evaporator outlet, 2 compressor outlet, 3 condenser outlet, 4 evaporator inlet):

- saturated vapour at `T_ev` at the compressor inlet, liquid subcooled by `DELTAT_sc` at the condenser outlet,
  isenthalpic expansion `h_4 = h_3`; `P_cd = PRESSURE(R22, T=T_cd, x=0.5)`;
- `W_dot_el = W_dot_cp_s/epsilon_s = W_dot_cp/eta_m`, with `W_dot_cp = M_dot_r*(h_2 - h_1)` and the isentropic
  work from `ENTHALPY(R22, S=S_1, P=P_cd)`;
- energy balance `Q_dot_cd = Q_dot_ev + W_dot_cp`;
- water circuits: `Q_dot = M_dot_w*cp_w*ΔT_w` on the water side and `Q_dot = epsilon*C_dot_min*(T_w,su − T_ref)`
  with an isothermal refrigerant side; the water flow rates and the effectivenesses are results
  (`epsilon_ev = 0.5`, `epsilon_cd = 1/3`); `cp_w` is evaluated at the mean water temperature.

R407C heat pump (same numbering, suffix `_pac`):

- evaporator heat `Q_dot_ev_pac = Q_dot_cd` taken from the water leaving the chiller condenser (35 → 30 °C,
  same flow rate); `epsilon_ev_pac` from the water temperatures and `T_ev_pac = 20 °C`;
- condenser: water 60 → 70 °C (`cp = 4187 J/kg-K` as in the original), `T_cd_pac = 80 °C`; the water flow rate
  follows from the heat balance and `epsilon_cd_pac = 0.5` is a result;
- `epsilon_c_pac_s = 0.6` global isentropic efficiency, `eta_m_pac = 0.9`;
- saturated vapour at the evaporator outlet, liquid at the bubble point of `T_cd_pac − 3 K` at the condenser outlet.

Global quantities: `COP_global = (Q_dot_ev + Q_dot_cd_pac)/(W_dot_el + W_dot_el_pac)` (cooling and heating are both
useful), `COP_pac`, `COP_chiller`, `ELF = W_dot_el/W_dot_el_max` with `W_dot_el_max = 276350 W`,
`CLF = Q_dot_ev/Q_dot_ev_max` with `Q_dot_ev_max = 900 kW`. The load is set by `CLF`
(`CLF = 1`, see the conversion log).

Part load: with `CLF = 0.5` (CoolSolve run of this file with `CLF=0.5`, not shipped) the solver gives
`ELF = 0.4958` and unchanged COPs (3.284, 2.407, 2.639): all efficiencies and effectivenesses are
constant, so `ELF = CLF*0.9916` is linear (the plot comment of the original EES file says the evolution is linear
because the efficiency degradation at part load is not taken into account).

## How to run

```bash
coolsolve ./r22_chiller_r407c_heat_pump.eescode
```

No `.initials` or `coolsolve.conf` is needed (141 iterations from default guesses). Change `CLF` (0 < CLF ≤ 1) to
study part load.

## Results

| Quantity | R22 chiller | R407C heat pump | Installation |
|---|---|---|---|
| Evaporator duty | `Q_dot_ev` = 900.0 kW | `Q_dot_ev_pac` = 1146.6 kW | |
| Condenser duty | `Q_dot_cd` = 1146.6 kW | `Q_dot_cd_pac` = 1831.4 kW | |
| Electrical power | `W_dot_el` = 274.04 kW | `W_dot_el_pac` = 760.87 kW | 1034.9 kW |
| Refrigerant flow rate | 5.893 kg/s | 13.213 kg/s | |
| Pressures (evaporator → condenser) | 497.99 kPa → 1729.2 kPa (ratio 3.47) | 957.6 kPa → 3834.7 kPa (ratio 4.00) | |
| Discharge temperature | 76.8 °C | 106.2 °C | |
| COP | `COP_chiller` = 3.284 | `COP_pac` = 2.407 | `COP_global` = 2.639 |
| Part-load factors | `ELF` = 0.9916, `CLF` = 1 | | |

Water flow rates: 53.54 kg/s (chiller evaporator), 54.87 kg/s (chiller condenser = heat-pump evaporator),
43.74 kg/s (heat-pump condenser). The heat pump delivers 1831.4 kW (= 43.74 kg/s × 4187 J/kg-K × 10 K)
at 60 → 70 °C, 1.6 times the cooling capacity.
The evaporating pressure of the R22 chiller (497.99 kPa) is computed in the diagram block
(`P_ev_r22`), it is not a variable of the original.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7):
     ![P-h diagram of the two cycles](figures/r22_chiller_r407c_heat_pump_ph.png)
     P-h diagrams of the R22 chiller (`h[i]`/`P[i]`) and of the R407C heat pump (`h_pac[i]`/`P_pac[i]`) -->

## Verification

Reference: the solution stored in the EES original `MSTH-SB-R10-EX4.EES` (EES 7.458, 74 stored variables,
`CLF = 1`), compared with `tools/compare_solution.py` (rtol = 0.001), which prints:

> 74 common variables, 31 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 34

(the 34 variables only in CoolSolve are the 33 diagram state-point equations and the unused string `fluid$`).
The largest printed relative difference is 4.31e-01 (`s_1_pac`).

| Quantity | EES stored | CoolSolve | rel. diff as printed |
|---|---:|---:|---:|
| `W_dot_el` | 276350 W | 274035 W | 8.37e-03 |
| `M_dot_r` | 5.93633 kg/s | 5.89266 kg/s | 7.36e-03 |
| `COP_chiller` | 3.25674 | 3.28425 | 8.37e-03 |
| `h_3` | 253596 J/kg | 252315 J/kg | 5.05e-03 |
| `P_cd` | 1.72982e+06 Pa | 1.72921e+06 Pa | 3.53e-04 (within rtol) |
| `P_ev_pac` | 948538 Pa | 957649 Pa | 9.51e-03 |
| `P_cd_pac` | 3.79743e+06 Pa | 3.83472e+06 Pa | 9.73e-03 |
| `M_dot_r_pac` | 14.9968 kg/s | 13.2126 kg/s | 1.19e-01 |
| `W_dot_el_pac` | 903495 W | 760867 W | 1.58e-01 |
| `COP_pac` | 2.17141 | 2.40701 | 9.79e-02 |
| `COP_global` | 2.42563 | 2.63929 | 8.10e-02 |

Reading of the deviations:

- **R22 chiller (< 0.9 %)**: `h_1`, `h_2`, `h_2_s` and `P_cd` agree within rtol. The refrigerating effect
  `h_1 − h_4` is 151.61 kJ/kg in EES and 152.73 kJ/kg in CoolSolve (`h_3`, liquid at 42 °C, 1.3 kJ/kg lower in
  CoolProp), which gives 0.74 % on `M_dot_r` and 0.84 % on all the powers; the same R22 deviation
  (EES 7.458 against CoolProp, `h_3` ≈ 1.2 kJ/kg) is documented for `CSL-0033`. The water `cp` differ by
  1.5e-03 (`cp_w_ev`, 4196.3 vs 4202.8 J/kg-K) and 8.4e-04 (`cp_w_cd`, within rtol); the stored EES values were not
  investigated further (the stored `M_dot_w_ev` is consistent with the stored `cp_w_ev`).
- **R407C heat pump: the EES 7.458 R407C properties are the outlier (resolved 2026-11-01).** A third property
  model was used: CoolProp's multi-fluid **mixture** model of R32/R125/R134a at the R407C composition
  (23/25/52 % by mass, mole fractions 0.3811/0.1796/0.4393; the mixture formulation REFPROP uses by default for
  R407C), evaluated in CoolSolve with the fluid string `R32[0.3811]&R125[0.1796]&R134a[0.4393]`. It is independent
  of the pseudo-pure R407C equation of CoolProp (Lemmon 2003) used by the model, yet the two agree:

  | Quantity | pseudo-pure R407C (model) | R32/R125/R134a mixture | EES 7.458 (stored) |
  |---|---:|---:|---:|
  | refrigerating effect `h(20 °C, x=1) − h(77 °C, x=0)` | 86.783 kJ/kg | 86.796 kJ/kg | 76.597 kJ/kg |
  | isentropic work to 3834.7 kPa from the dew point at 20 °C | 34.55 kJ/kg | 34.56 kJ/kg | 36.15 kJ/kg (to 3797 kPa) |
  | bubble / dew pressure at 20 °C | 1037.55 / 880.29 kPa | 1037.62 / 880.36 kPa | — |
  | bubble / dew pressure at 77 °C | 3937.13 / 3722.43 kPa | 3936.29 / 3722.69 kPa | — |

  The two CoolProp formulations agree within 1.5·10⁻⁴ on the quantities that drive `M_dot_r_pac` and
  `W_dot_el_pac`, and within 2·10⁻⁴ on the saturation pressures, while EES 7.458 (2005) is 12 % lower on the
  refrigerating effect, mainly through the bubble-point liquid enthalpy at 77 °C, 9 K below the critical point
  (86.2 °C), where the EES − CoolProp enthalpy offset drops from 141.3 to 131.1 kJ/kg. The R407C model of that
  EES release is therefore the cause of the deviation, not the equations of the model; the same EES-side R407C
  deviation appears in `CSL-0078` (EES 7.888: suction vapour `c_p` −10 %, dew temperature +0.3 K against both
  CoolProp formulations) and in `CSL-0260`. The CoolSolve results are kept as the reference of this model.
  Earlier analysis (2026-10-31), kept for the record:
  1. *First variable above 1 %, in circuit order* (offsets of absolute `h`/`s` excluded): `P_ev_pac` 9.51e-03 and
     `P_cd_pac` 9.73e-03 (just below), then `w_cp_pac_s` 4.41e-02 (isentropic work 36.15 kJ/kg in EES, 34.55 in
     CoolSolve), then the refrigerating effect `h_1_pac − h_4_pac` (76.60 kJ/kg in EES, 86.78 in CoolSolve, +13 %
     in CoolSolve, after the reference-state offset is removed), hence `M_dot_r_pac` 1.19e-01 and
     `W_dot_el_pac` 1.58e-01. The absolute offsets are 141.29 kJ/kg at the dew point of 20 °C and 131.11 kJ/kg
     at the bubble point of 77 °C (EES − CoolProp, in the sense CoolProp = EES + offset), 756.4 J/kg-K on `s_1_pac`.
  2. *The (P, x = 0.5) rewrite is not the cause.* `h_1_pac` (`T=20, x=1`), `h_3_pac` (`T=77, x=0`) and `s_1_pac`
     are untouched calls whose (CoolProp − EES) difference carries the +13 % on `h_1_pac − h_4_pac`, and
     `M_dot_r_pac` (13.213 vs 14.997 kg/s, −11.9 %) does not depend on any pressure at all. The pressure only enters
     `w_cp_pac_s`: with the pressure convention changed (CoolSolve runs of variants of the file, not shipped),
     `W_dot_el_pac` stays between 745.9 kW (dew/dew), 755.9 kW (EES stored `P_ev_pac`, `P_cd_pac` imposed
     directly), 760.9 kW (this model, mid-quality) and 774.1 kW (bubble/bubble), against 903.5 kW in EES.
     The mid-quality pressures themselves differ from the stored ones by 0.95 % and 0.97 % (see the rows above).
     The implicit form `T_x = TEMPERATURE(R407C, P, x=0.5)` is the direct inversion of the EES call in CoolProp.
  3. *The stored solution corresponds to `CLF = 1`*: `Q_dot_ev = 900000 = Q_dot_ev_max`, `M_dot_w_ev = Q/(cp·4)` and
     `COP_global = 2.4256` recompute from the stored values. The CLF-independent ratios deviate as well
     (`COP_pac` 9.79e-02; specific refrigerant flow `M_dot_r_pac/Q_dot_ev_pac` 1.3055e-5 vs 1.1522e-5 kg/J,
     −11.7 % in CoolSolve), so the load is not the cause.
  The remaining suspects are the R407C equations of state (EES vs the CoolProp mixture) in the high-temperature
  state `T = 77 °C` (close to the critical region of the mixture, not checked), and the way EES treats the glide
  of R407C; the same kind of deviation (offset spreading over 138.9–142.9 kJ/kg, `c_p` 10–13 %) is reported in `CSL-0260`.
  The 2026-11-01 check above supplies the third property source that was missing.
- The consistency of the stored EES solution itself was checked on the global COP:
  (900000 + 1961859.7)/(276349.5 + 903494.6) = 2.4256, as stored.
- **Balances and second law of the CoolSolve solution** (2026-11-01): the condenser duties close the two energy
  balances (`Q_dot_cd = Q_dot_ev + W_dot_cp`, `Q_dot_cd_pac = Q_dot_ev_pac + W_dot_cp_pac`) and the water-side
  balances; every effectiveness is below 1 (0.5, 1/3, 1/3, 0.5); each refrigerant temperature lies on the correct
  side of its water stream (0 °C < 4 °C, 45 °C > 35 °C, 20 °C < 30 °C, 80 °C > 70 °C); the COPs stay below the
  Carnot values at the refrigerant temperatures (chiller 3.28 < 273.15/45 = 6.07, heat pump 2.41 < 353.15/60 = 5.89);
  the discharge enthalpies exceed the isentropic ones (`epsilon_s` = 0.67, `epsilon_c_pac_s` = 0.6 on the electrical
  power with `eta_m` = 0.9). The heat pump mixes a mid-quality pressure with dew/bubble enthalpies as the original
  does (state 3 at the bubble point of 77 °C lies 102 kPa above `P_cd_pac`): a teaching simplification of a
  zeotropic blend, kept.

## Source and attribution

Original model: Stéphane Bertagnolio (initials SB of the file name), ULiège Thermodynamics Laboratory, course
*Machines et systèmes thermiques* (J. Lebrun, V. Lemort, S. Bertagnolio), exercise session 10, exercise 4, EES
file `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 10/MSTH-SB-R10-EX4.EES`
(EES X7.458). The R22 chiller part also appears in the files of exercise 3 of the same session
(`MSTh R10 Ex 3.EES`, `MSTH-SB-R10-EX3.EES`, `MSTH-SB-R10-EX3-2.EES`, `thermo_models` TM-0153, TM-0156, TM-0155):
chiller sizing and identification of the same R22 machine, without the R407C heat pump (not imported, see Niche).

## Conversion log

- **2026-10-31 — import**: extraction with `ees_extract.py` (74 variables, no table decoded, no warning); the
  unit system is already SI-°C-Pa-J (no conversion); comments translated to English with SI units; standard
  header added; equations kept in the original order and with the original names.
- **Operating point (CLF)**: the equations window of the original contains no equation for the load (`Q_dot_ev=450000`
  is commented out) and the stored `CLF = 1` is not set by any equation: `CLF` is most likely a column of a
  parametric table (the binary file contains the column names `CLF` and `ELF`, but the extractor decodes no table and
  the contents were not decoded). As for any table input (ees_import.md §8), the default run `CLF = 1` (the stored
  solution, `Q_dot_ev = 900 kW`) is added as an equation, which makes the system square (75 equations, 75 unknowns
  before the diagram block; the unmodified extraction has 74 equations and 75 unknowns).
- **R407C (T, x = 0.5) calls**: `P_ev_pac = PRESSURE(R407C, T=T_ev_pac, x=0.5)` and
  `P_cd_pac = PRESSURE(R407C, T=T_cd_pac-DELTAT_sc_pac, x=0.5)` fail in CoolProp (NaN for the mid-quality (T, x) pair on
  the zeotropic R407C; solver stops with "CoolProp evaluation failed in final solution"). Rewritten with the supported
  (P, x = 0.5) pair, implicitly in the pressure (`T_ev_pac = TEMPERATURE(R407C, P=P_ev_pac, x=0.5)`,
  `T_cd_pac − DELTAT_sc_pac = TEMPERATURE(R407C, P=P_cd_pac, x=0.5)`): registered as `CS-GAP-PROP-TQ-PSEUDOPURE`
  (maintainer decision: not a gap, rewrite in the native file; same rewrite as `CSL-0260`).
  The (T, x = 1) and (T, x = 0) calls run unchanged. The EES file mixes a mid-quality saturation pressure with
  dew/bubble enthalpies (`h_1_pac` at `x=1`, `h_3_pac` at `x=0`): kept as in the original, hence the heat-pump
  state temperatures of the diagram block (from (P, h)) are 22.8 °C and 75.8 °C instead of 20 °C and 77 °C
  (zeotropic glide).
- **Kept as in the original**: the string `fluid$='R22'` is declared but not used (the calls write `R22`);
  `DELTAT_oh` and `DELTAT_oh_pac` are not used by any equation; `T_cd_pac-3` in `h_3_pac` is written with the literal 3
  (equal to `DELTAT_sc_pac`); `W_dot_el_max = 276350` is the rounded value of `W_dot_el` at full load found by EES,
  hence `ELF = 0.999998` in EES and 0.9916 in CoolSolve (property backends).
- **Diagram block**: added at the end (no effect on the results, checked: the 75 variables of the original have the same printed .sol
  values before and after adding it), arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (R22) and `P_pac[i]`, `h_pac[i]`, `T_pac[i]`,
  `s_pac[i]` (R407C), `i = 1..4`; the discharge enthalpy of the heat pump is
  `h_1_pac + W_dot_cp_pac/M_dot_r_pac`; the R22 evaporating pressure `P_ev_r22` is added for the chiller (it is not
  a variable of the original).
- **Level**: 108 equations (1), largest block 1 (0), arrays (1: diagram block only; the original has no
  functions or arrays), several coupled components (two machines, four water exchangers: 1), part load as
  indicators only (0), default guesses sufficient (0) → score 3 → level 2 (score 2–3).

## Niche

Nearest models and what this one adds:

- `CSL-0033` (*heat_pump_r22_semihermetic_compressor*, same repetition, exercise 1): R22 machine with a detailed
  semi-hermetic compressor model and eps-NTU exchangers with imposed `AU`; one machine, no cascade.
  Here the compressors have constant efficiencies and the exchangers are rated by effectivenesses (outputs).
- `CSL-0001` (*refrigeration_cycle_simple_compressor*) and `CSL-0025` (*heat_pump_cycle_r22_30kw*): a single R22
  (or R134a) cycle without secondary circuits (CSL-0001) or with a prescribed heating capacity (CSL-0025).
- `CSL-0250` (*cascade_heat_pump_geothermal_dh*): cascade heat pump with pinch-imposed exchangers and no part-load
  indicators.

New here: **two machines coupled by a water circuit** (an R22 chiller whose condenser heat feeds the evaporator of an
R407C heat pump, heat *upgrading* 35 → 70 °C), the **global COP** of the installation counting cooling and heating,
the **ELF/CLF part-load factors**, and an **R407C zeotropic fluid** with mid-quality saturation conditions in a
teaching exercise. The R22 chiller alone (TM-0153/0155/0156, exercise 3) is covered by this model.

## Limitations and CoolSolve gaps

- R407C is a pseudo-pure fluid with temperature glide in CoolProp (bubble and dew lines): the heat-pump states are
  only as consistent as the original's mixing of mid-quality pressure and dew/bubble enthalpies.
- The R407C heat-pump results differ from the EES 7.458 stored values by up to 16 % on the electrical power: the
  deviation comes from the R407C property model of that EES release (two independent CoolProp formulations agree
  with each other, see Verification). The model is `verified` on the CoolProp properties.
- Constant efficiencies: part load is linear (`ELF = CLF*0.9916`) by construction.
- `CS-GAP-PROP-TQ-PSEUDOPURE` (registered as "not a gap"): worked around in the native file (see conversion log); it
  does not block the model (`missing_features` empty). `CS-GAP-PARAMETRIC` (parametric-table inputs) is only
  relevant for the `CLF` column of the original file, replaced by the default run.

## Related models

- `CSL-0033` *heat_pump_r22_semihermetic_compressor*: exercise 1 of the same repetition (R22, detailed compressor).
- `CSL-0001` *refrigeration_cycle_simple_compressor*: R22 refrigeration cycle of the same ULiège series.
- `CSL-0068` *heat_pump_scroll_compressor_data_check*: R407C scroll-compressor data check; documents R407C
  saturation pressures in CoolProp (dew/bubble vs mid-quality).
- `CSL-0260` *scroll_compressor_reed_valve*: R407C mid-quality pressure calls rewritten with the same (P, x) inversion.

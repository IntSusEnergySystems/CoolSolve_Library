# Cascade heat pump, geothermal water to district heating

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0250`

Two refrigerant loops (LT, HT) coupled in a cascade between a geothermal
water source and a district-heating (DH) network. The four source/load heat
exchangers are *sectioned* exchangers with an imposed pinch (5 K): one energy
balance per refrigerant zone (two-phase, superheat/desuperheat, subcool) and
the pinch condition at the zone boundary where the minimum occurs replace the
imposed saturation pressures of a classic design model. The main file
(translated from TESPy notebook `variant_2_series_IHX.ipynb`) adds an internal
heat exchanger (IHX) in each loop; the variant file
(`cascade_heat_pump_geothermal_dh_ammonia_desuperheater.eescode`, from
`variant_4_ammonia_desuperheater.ipynb`) runs ammonia without IHX but with a
desuperheater ahead of each condenser.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R1233zd(E), Water (main file); Ammonia, Water (variant) |
| **Size** | 148 equations (largest block: 38); variant: 151 equations (largest block: 44) |
| **Source** | TESPy notebooks `variant_2_series_IHX.ipynb` and `variant_4_ammonia_desuperheater.ipynb` (solution drafts of a KCORC summer-school exercise) |
| **Authors** | Francesco Witte and Amalia Steinhauer (KCORC summer school, parent exercise; draft notebooks supplied by S. Quoilin) |
| **Original** | [https://github.com/fwitte/KCORC_summer_school/](https://github.com/fwitte/KCORC_summer_school/) — parent exercise [`tespy/HP_design/LT_HeatPump_R1233zdE_GroupA.ipynb`](https://github.com/fwitte/KCORC_summer_school/blob/85a2362/tespy/HP_design/LT_HeatPump_R1233zdE_GroupA.ipynb) (commit `85a2362`) |
| **License** | The KCORC repository states "shared for educational use" and has no LICENSE file; TESPy is MIT. Published here with full credit and a link to the original; to be removed or relicensed on the authors' request |
| **CoolSolve** | 0.4.0 — verified against a re-run of the notebooks (see *Verification*) |

## Problem statement

A geothermal production well delivers 100 kg/s of water at 60 °C (5 bar). The
water is cooled in series through the HT then LT evaporator to 50 °C between
the two and 40 °C at injection. DH return water at 60 °C is heated to 90 °C —
through the LT then HT condenser (main file), additionally through the LT then
HT desuperheater (variant); the DH mass flow is a **result**, not an input.
Each refrigerant loop runs a classic vapour-compression cycle: isenthalpic
expansion valve, compressor with isentropic efficiency 0.75, no pressure
drops. In the main file an IHX per loop superheats the suction by 10 K beyond
the 5 K leaving the evaporator and subcools the liquid accordingly. Instead of
fixing evaporation/condensation pressures, each of the four exchangers imposes
a minimum approach of 5 K between the streams; the saturation temperatures are
results.

## Model

The TESPy plumbing (Network, Connection objects, CycleCloser, the Newton
solver) becomes plain simultaneous equations; the notebook's variable meanings
and connection labels (LT 1…4/1a, HT 1…4/1a) are kept as name suffixes.

- **States** (per loop): suction superheat `td_dew` = 5 K (+10 K through the
  IHX, main file), condenser-outlet subcooling `td_bubble` = 3 K (LT) / 5 K
  (HT) → `T_1 = T_dew(P_ev) + SH`, `T_3 = T_bub(P_cond) − SC`; isentropic
  compression `h_2 = h_1 + (h_2s − h_1)/eta_s`; isenthalpic valve `h_4 = h_3b`.
- **IHX** (main file): energy balance `h_3b = h_3 − (h_1 − h_1a)`; the TESPy
  CycleCloser enforces the enthalpy equality `h_1b = h_1` (verified in the
  TESPy source, `cycle_closer.py`), which closes the cycle.
- **Sectioned exchangers**: the refrigerant zones (evaporator: two-phase +
  superheat; condenser: desuperheat + two-phase + subcool) each get an energy
  balance on both streams, giving the zone-boundary temperatures of the water
  (`T_w_ev_*`, `T_w_sub_*`, `T_w_cond_*`). The pinch is imposed at the boundary
  where the minimum occurs — the **cold end** (water outlet / two-phase inlet)
  for the evaporators, the **dew-point boundary** for the condensers — and the
  `PPTD_MIN_*` variables check afterwards that the minimum zone-boundary
  difference equals the imposed 5 K (TESPy's own `pinch()` helper does the
  same check on its section profiles). An earlier formulation with
  `PPTD = MIN(...) = pinch` as the closing equation (the pattern of
  `CSL-0133`) is mathematically identical but does not converge in CoolSolve
  0.4.0 (non-smooth nested `MIN` inside a 77-variable block); the split form
  below is used instead.

Unknowns: the four saturation pressures, the two refrigerant mass flows
(closed by the geothermal energy balances), the DH mass flow and the
intermediate DH enthalpies (closed by the DH energy balances, DH supply at
90 °C). Inputs: the 17 design values of the header (pinches, SH/SC, eta_s,
IHX duty split, water states, geothermal flow).

| Inputs | Value | Outputs (main file, LT / HT) | Value |
|---|---|---|---|
| `TD_PINCH_*` (4 exchangers) | 5 K | `T_ev_LT` / `T_ev_HT` | 35.00 / 45.00 °C |
| `SH_LT`, `SH_HT` | 5 K | `T_cond_LT` / `T_cond_HT` | 78.49 / 93.59 °C |
| `SC_LT`, `SC_HT` | 3 / 5 K | `m_LT` / `m_HT` | 28.35 / 30.50 kg/s |
| `ETA_S` | 0.75 | `W_LT` / `W_HT` | 927.0 / 1031.8 kW |
| `DT_IHX` | 10 K | DH water between condensers `T_d2` | 74.86 °C |
| `T_GEO_IN/MID/OUT` | 60/50/40 °C | `m_dh` | 82.04 kg/s |
| `M_GEO` | 100 kg/s | `Q_dh` / `Q_geo` | 10 320 / 8 361 kW |
| `T_DH_IN/OUT` | 60/90 °C | `W_tot` / `COP` | 1 958.7 kW / 5.269 |

## How to run

```bash
coolsolve ./cascade_heat_pump_geothermal_dh.eescode                       # main file (variant 2)
coolsolve ./cascade_heat_pump_geothermal_dh_ammonia_desuperheater.eescode # variant 4
```

Both files need the guess values of their `.initials` (saturation pressures,
mass flows, DH enthalpies). Units are the library convention SI-°C-Pa-J; the
notebooks work in the same unit values (their display units bar/°C/kW only
affect printing). The arrays `P_LT[i], h_LT[i], T_LT[i], s_LT[i]` and
`P_HT[i], …` (i = 1 suction, 2 discharge, 3 condenser outlet, 4 evaporator
inlet) give each loop on the CoolSolve Diagram tab (*Overlay array path*,
*Close cycle*).

## Results

| Quantity | Variant 2 (R1233zd(E), IHX) | Variant 4 (NH3, desuperheaters) |
|---|---:|---:|
| LT loop: `T_ev_LT` / `T_cond_LT` [°C] | 35.00 / 78.49 | 35.00 / 76.89 |
| HT loop: `T_ev_HT` / `T_cond_HT` [°C] | 45.00 / 93.59 | 45.00 / 89.32 |
| LT loop: `P_ev` / `P_cond` [bar] | 1.84 / 6.35 | 13.50 / 38.68 |
| HT loop: `P_ev` / `P_cond` [bar] | 2.53 / 9.06 | 17.82 / 50.45 |
| LT loop: `m_LT` [kg/s], `W_LT` [kW] | 28.35, 927.0 | 4.45, 927.9 |
| HT loop: `m_HT` [kg/s], `W_HT` [kW] | 30.50, 1031.8 | 4.73, 972.7 |
| discharge `T_2_LT` / `T_2_HT` [°C] | 95.75 / 109.21 | 141.43 / 151.96 |
| `Q_geo` [kW] | 8 361.4 | 8 361.4 |
| `Q_dh` [kW] | 10 320.1 | 10 262.0 |
| `m_dh` [kg/s] | 82.04 | 81.58 |
| `W_tot` [kW] | 1 958.7 | 1 900.6 |
| system `COP` [-] | 5.269 | 5.399 |

DH water: 60 → 74.86 → 90 °C (variant 2); 60 → 72.77 → 85.40 → 87.58 → 90 °C
(variant 4, after LT cond., HT cond., LT dsh., HT dsh.). Ammonia reaches a
slightly better COP (smaller compressor power at the same lift) but needs a
5–15 bar pressure level and a 40 K higher discharge temperature.

T-Q composite-curve data (variant 2, cumulative duty from the cold end of each
water stream, as in the notebook's `chained_TQ` plot; water side / refrigerant
side):

| cumulative Q [kW] | geo water [°C] | LT refrig. [°C] | DH water [°C] | LT refrig. [°C] |
|---:|---:|---:|---:|---:|
| 0 | 40.00 | 35.00 | 60.00 | 75.49 |
| 112.2 | – | – | 60.33 | 78.49 (bubble) |
| 4 060.8 | 49.72 | 35.00 (dew) | – | – |
| 4 179.3 | 50.00 | 40.00 | – | – |
| 4 633.7 | – | – | 73.49 | 78.49 (dew) |
| 5 106.2 | – | – | 74.86 | 95.75 |
| 5 315.0 | – | – | 75.47 | 88.59 (bubble) |
| 8 229.9 | 59.69 | 45.00 (dew) | – | – |
| 8 361.4 | 60.00 | 50.00 | – | – |
| 9 832.3 | – | – | 88.59 | 93.59 (dew) |
| 10 320.1 | – | – | 90.00 | 109.21 |

(the HT refrigerant temperatures of the geothermal side sit in the HT columns
at the same duties: 45.00 at 8 229.9 kW etc.; zone duties — LT evaporator
4 060.8 + 118.5 kW, HT 4 050.6 + 131.5 kW; LT condenser 472.5 + 4 521.5 +
112.2 kW, HT 487.8 + 4 517.3 + 208.8 kW.)

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-Q composite curves of the
     geothermal and DH sides, or a P-h overlay of the two loops,
     figures/cascade_heat_pump_geothermal_dh_*.png -->

## Verification

The original notebooks were **re-run in a throw-away virtual environment**
(`work/venv`, Python 3.12, `pip install tespy matplotlib`; TESPy 0.11.3,
CoolProp as shipped with it; run headless with `MPLBACKEND=Agg` after
`jupyter nbconvert --to script` — the script `work/ref_values.py` of the card
re-builds both networks and prints the values below, full precision). The
CoolSolve `.sol` of both files was then compared with those values (28 and 30
common variables; interface conversions: notebook display bar/kW/kJ read as
Pa/W/J).

`compare_solution.py <file>.sol <reference>.csv`: **28 common variables, 0
differ (rtol=0.001)** (variant 2) and **30 common variables, 0 differ
(rtol=0.001)** (variant 4); the maximum relative deviation over the common
variables is **3.2e-06** (on `T_2_HT`, variant 2) and **3.0e-06** (on `Q_dh`,
variant 4) — far below the 0.1 % expected from CoolProp version differences
alone (the venv CoolProp and the CoolSolve-pinned CoolProp are different
commits).

| Quantity | Variant 2: TESPy / CoolSolve | Variant 4: TESPy / CoolSolve |
|---|---:|---:|
| `P_ev_LT` [Pa] | 183 734.1 / 183 734.1 | 1 349 991.7 / 1 349 991.7 |
| `P_cond_LT` [Pa] | 634 571.3 / 634 571.3 | 3 868 218.5 / 3 868 218.5 |
| `P_ev_HT` [Pa] | 252 700.1 / 252 700.1 | 1 781 674.5 / 1 781 674.5 |
| `P_cond_HT` [Pa] | 905 774.4 / 905 774.4 | 5 044 992.9 / 5 044 992.9 |
| `T_cond_LT` / `T_cond_HT` [°C] | 78.4875 / 93.5856 | 76.8853 / 89.3187 |
| `m_LT` / `m_HT` [kg/s] | 28.3533 / 30.5043 | 4.4509 / 4.7275 |
| `W_LT` / `W_HT` [kW] | 926.96 / 1031.77 | 927.89 / 972.75 |
| `m_dh` [kg/s] | 82.0435 | 81.5816 |
| `Q_dh` [kW] | 10 320.1 | 10 262.0 |
| `COP` [-] | 5.2688 | 5.3993 |

The pinch checks `PPTD_MIN_EV_LT`, `PPTD_MIN_EV_HT`, `PPTD_MIN_COND_LT`,
`PPTD_MIN_COND_HT` all evaluate to exactly 5 K in both `.sol` files, as in the
notebook's `pinch()` helper. Overall energy balance: `Q_dh − Q_geo` =
1 958 735.64 W = `W_tot` (variant 2, closes to 1e-5 W).

## Source and attribution

Solution drafts of an exercise of the **KCORC summer school**. Parent exercise:
[`fwitte/KCORC_summer_school`](https://github.com/fwitte/KCORC_summer_school),
`tespy/HP_design/LT_HeatPump_R1233zdE_GroupA.ipynb` (commit `85a2362`), by
Francesco Witte and Amalia Steinhauer (authors of that notebook according to the repository history).
The draft notebooks translated here were supplied by S. Quoilin and are not in
the repository; their individual authors are not recorded, so the credit goes to the exercise. The
KCORC repository has no LICENSE file ("shared for educational use"). Source notebooks (maintainer's collection):
`~/Nextcloud/thermo_models/variant_2_series_IHX.ipynb` and
`~/Nextcloud/thermo_models/variant_4_ammonia_desuperheater.ipynb` (inventory
candidates `LDS-001` and `LDS-002` of `sources/ext_leads`).

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of two TESPy notebooks (TESPy 0.11.3).
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff /
version control history). TESPy is released under the MIT License; the two notebooks
(summer-school exercise drafts) carry no licence statement.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in
Python", J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.

## Conversion log

- **2026-10-21 — translation** (`T-TRANSLATE`, workflow §5): the physics of
  the two notebooks was translated into EES-language simultaneous equations;
  Python/TESPy plumbing removed (Network/solver → the CoolSolve solver,
  CycleCloser → the enthalpy equality `h_1b = h_1` it enforces,
  `pr1 = pr2 = 1` → no pressure-drop equations, `td_dew`/`td_bubble`
  specifications → superheat/subcooling relative to the saturation temperature
  at the connection pressure). SI-°C-Pa-J inside the equations; the notebooks
  already compute in these unit values (their bar/°C/kW are display units
  only), so no value conversion was needed (water-side 5 bar → `P_WATER =
  5E5` Pa written explicitly). Variable names keep the notebook's connection
  labels (`_LT`/`_HT` suffix, states 1, 2, 3, 3b, 4, 1a, `h_g*`/`h_d*` water
  enthalpies, `PPTD_*` pinches, `m_dh`, `W_`, `Q_`, `COP`).
- **Sectioned exchangers**: TESPy `SectionedHeatExchanger` with `td_pinch`
  splits the exchanger at the refrigerant phase boundaries and imposes the
  minimum approach over its (grid-discretised) section profile
  (`td_pinch_func`: `td_pinch − min(T_hot − T_cold)`). The translation writes
  one energy balance per zone and the zone-boundary temperatures, imposes the
  pinch at the boundary where the minimum occurs (cold end for the
  evaporators, dew-point boundary for the condensers) and checks afterwards
  `PPTD_MIN_* = MIN(boundaries) = 5 K` — the same check as the notebook's
  `pinch()` helper. The first attempt used the single closing equation
  `PPTD = MIN(...) = pinch` (pattern of `CSL-0133`): mathematically
  identical, but CoolSolve 0.4.0 does not converge on the resulting
  77-variable block (non-smooth nested `MIN`); the model is not blocked (the
  adopted form is equivalent and verified against the notebook).
- **Variant split** (one card, one library model): the main file is the
  R1233zd(E)/IHX notebook (LDS-001, inventory row `added`); the
  ammonia/desuperheater notebook (LDS-002, row `merged`) ships as the variant
  file `cascade_heat_pump_geothermal_dh_ammonia_desuperheater.eescode` with
  its own `.initials` and `.sol`. Differences: no IHX (`h_1 = h_1a`, suction
  superheat 5 K only), desuperheaters `T_2b = T_cond + 15` ahead of the
  condensers (whose desuperheating zone shrinks accordingly), DH water passes
  LT cond. → HT cond. → LT dsh. → HT dsh., fluid `Ammonia`.
- **Level**: score = equations 148 (2, 50–300) + largest block 38 (2, > 30) +
  arrays present (1) + cascade, ≥ 3 coupled components (1) + physics 0 +
  curated guesses needed (1) = 7 → level 4, **moved down to 3**: design-point
  teaching model whose large block comes from property-call chains, not from
  demanding numerics (converges in 17 iterations from round-number guesses),
  as the inventory's `level_guess` 3 anticipated.
- Comments paraphrase the notebooks'; the `.initials` files hold round-number
  guesses, not stored values of another tool.

## Limitations and CoolSolve gaps

- No blocking CoolSolve gap: both files run natively in CoolSolve 0.4.0.
- The nested-`MIN` closing equation of `CSL-0133`'s pattern does not converge
  inside the large implicit block of this model (see conversion log); the
  equivalent split formulation is used. No register row: not a missing EES
  feature, a solver-robustness observation on a non-smooth formulation.
- The desuperheaters of variant 4 are `SectionedHeatExchanger` in TESPy but
  stay single-phase (no section boundary); they are translated as plain energy
  balances and their terminal differences are results (LT 6.48 K, HT 16.74 K,
  no temperature cross, as in the notebook output).
- The TESPy `UA`/`kA` outputs of the sectioned exchangers are not translated
  (UA is a design *result* of the notebook's discretised profile, not part of
  the equation system).

## Related models

- `CSL-0133` *heat_pump_propane_pinch*: single-loop heat pump sized by imposed
  pinches with the same `MIN(zone-boundary differences) = pinch` pattern (its
  closing-equation form does not converge here; see conversion log).
- `CSL-0014` *hx_constant_pinch*: the pinch-imposed three-zone condenser
  component (LaboThapPy `HexCstPinch`) reused idea-wise for the zone
  balances of this model.
- `CSL-0039` *high_temp_heat_pump_pcm_storage*: high-temperature heat pump on
  a geothermal case study (Zorlu), same category of source-to-DH heat pumps.
- `CSL-0145` *refrigeration_co2_transcritical_booster*: two-stage cascade
  refrigeration system (CO2 booster), the cascade/sectioned-exchanger
  counterpart on the refrigeration side.
- `CSL-0138` *hx_moving_boundary_bell*: moving-boundary evaporator model
  (Bell 2015), another discretised-evaporator view of the same two-zone
  physics.
- `CSL-0013` *heat_pump_basic_tespy*: basic TESPy heat-pump translation
  (same source library, simplest cycle).

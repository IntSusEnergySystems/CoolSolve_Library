# ext_leads - leads and notebooks added by the maintainer

Candidates that do not belong to one of the swept collections: files dropped at the root of
`~/Nextcloud/thermo_models/` (2026-10-21) and the repositories of the maintainer's `lisf of repositories`
note. Machine-readable backlog: [`inventory.csv`](inventory.csv) (same columns as `sources/tespy`, ids `LDS-nnn`).

| ids | content |
|---|---|
| LDS-001, LDS-002 | `variant_2_series_IHX.ipynb` and `variant_4_ammonia_desuperheater.ipynb`: TESPy cascade heat pump, geothermal source to district heating (exercise drafts of the KCORC summer school). One library model, two variants. Authors to be confirmed by the maintainer |
| LDS-003 … LDS-010 | repository leads, not yet triaged (SEGS and sCO2 of F. Witte probably duplicate library models; ORC off-design, ExerPy CCPP, DTU recuperated Brayton HTHP, own `NextGenerationHeatPumps`) |

The original list, kept for the record:

```
Based on literature data and/or validated with other simulation software:
  fwitte/SEGS_exergy SEGS.py · fwitte/sCO2_exergy sCO2.py ·
  fwitte/KCORC_summer_school tespy/ORC_offdesign/complete_ORC.ipynb ·
  oemof/exerpy examples/exergy_analysis/ccpp
Exercise for PhD students at the summer school: figure 4 and figure 5 models of
  fwitte/KCORC_summer_school tespy/HP_design/LT_HeatPump_R1233zdE_GroupA.ipynb (solution drafts = LDS-001/002)
DTU, in progress and not tested by the maintainer: SamueleGrandinDTU/recuperated_Brayton_HTHP examples
Own: squoilin/NextGenerationHeatPumps
```

## 2026-10-21 triage

Card C-276 (`T-TRIAGE`): rows `LDS-003` … `LDS-010` were cloned shallowly under `work/triage/`
(deleted when the card closed), their code, READMEs and licence files read, and compared with
`library.json` and the other inventories on the equations/specifications, not only on names.
Rows `LDS-001`/`LDS-002` belong to card C-275 and were not touched. No lead contained several
distinct models — the folder leads `LDS-006` (`ccpp`) and `LDS-008` (`examples`) each describe one
plant model with reference/variant files — so no rows `LDS-011`+ were appended.

| lead | decision | reason |
|---|---|---|
| LDS-003 fwitte/SEGS_exergy `SEGS.py` | duplicate | Same TESPy SEGS network as `CSL-0147` (`TSP-051`): 159/162 specification lines identical (the tespy test only adds `state="l"` hints); `SEGS.py` adds the exerpy exergy analysis, the EBSILON `.ebs` flowsheet and README result tables |
| LDS-004 fwitte/sCO2_exergy `sCO2.py` | duplicate | Same sCO2 network as `CSL-0144` (`TSP-042`): all 38 specification lines contained in `tespy/docs/model_library/sco2.ipynb` (which adds the staged split-ratio spec and NSGA-II); script adds exergy + Penkuhn & Tsatsaronis validation CSVs |
| LDS-005 KCORC `ORC_offdesign/complete_ORC.ipynb` | todo | Two-stage (HT+LT) series ORC on geothermal brine — absent from the library (all `orc_*` models are single-loop) and from the other inventories; design point validated against Table 3/Figure 6 of Heberle et al. 2015 inside the notebook; **the KCORC repo has no LICENSE file** (README: educational use) → confirm before translating. Card C-279 |
| LDS-006 exerpy `examples/exergy_analysis/ccpp` | duplicate | Same CCPP (300 MW grid + 100 MW district heat, drum HRSG, HP/LP turbines) as `TSP-043` (still `todo`): 66/80 specification lines identical, and the `TSP-043` note already says it originates from this example; differs by unit defaults, a few HRSG pressure drops and staged solving. Keep the folder as verification reference for the `TSP-043` card (`ccpp_ebs.json`, `ccpp_aspen.json`, `validation.ipynb`) |
| LDS-007 KCORC `HP_design/LT_HeatPump_R1233zdE_GroupA.ipynb` | duplicate | Source exercise of `LDS-001`/`LDS-002` (card C-275, one library model, roadmap pre-assigns `CSL-0250`): same case study; the exercise imposes saturation temperatures 35/45/80/95 °C on plain HXs, the drafts impose a 5 K pinch on sectioned HXs (IHX/desuperheater variants). Its design tables belong in the C-275 README; `library_id` left empty until C-275 lands |
| LDS-008 `recuperated_Brayton_HTHP` examples | todo | One plant model in two layouts (standalone / TES-integrated), not several models: the steady design-point model `main/standalone_base_recup_hthp.py` is the translation target; the examples are week-long transient simulations with electricity-price lookups and strategy optimisation → difficulty=hard, `CS-GAP-OPTIM`. **No LICENSE file** and untested WIP → priority low. Card C-281 |
| LDS-009 `nghp/simple HTHP model.py` | todo | R245fa HTHP at T_ev 80 °C / T_cd 145 °C with recomputed water profiles — no library model of this system (`CSL-0133` propane low-level pinch HP, `CSL-0039` Zorlu cyclopentane+PCM: other fluid, levels, topology); explicit forward script, MIT, re-run for verification. Card C-278 |
| LDS-010 `nghp/advanced HTHP model.py` | todo | Zeotropic/transcritical HTHP — absent (`TSP-049` is another system); mixtures are supported since `CS-GAP-FLUIDS-MIXTURE` was closed, the REFPROP back end is replaced by CoolProp/EES fluid names (decision D12, not a gap) → difficulty=hard, no registered blocking gap. Card C-280 |

Counts: 4 `duplicate`, 4 `todo` (`LDS-001`/`LDS-002` untouched, still `todo`, card C-275).

Proposed cards (roadmap §6):

```text
[ ] C-278  T-TRANSLATE  LDS-009  → cycles/refrigeration_heat_pumps/high_temp_heat_pump_r245fa  — simple R245fa high-temperature heat pump (T_ev 80 C / T_cd 145 C) with recomputed water-side profiles and pinch check; verification: re-run nghp/simple HTHP model.py in a venv and compare the printed state tables and water mass flows
[ ] C-279  T-TRANSLATE  LDS-005  → cycles/organic_rankine/orc_double_stage_kirchstockach  — two-stage (HT+LT) series ORC on geothermal brine, air-cooled condensers, design point; verification: re-run complete_ORC.ipynb in a venv and compare with the Heberle et al. 2015 Table 3 values asserted in the notebook
[ ] C-280  T-TRANSLATE  LDS-010  → cycles/refrigeration_heat_pumps/high_temp_heat_pump_zeotropic_transcritical  — advanced HTHP: zeotropic mixtures and transcritical cycles (R1336mzz(Z) default, REFPROP replaced by CoolProp per decision D12); verification: re-run nghp/advanced HTHP model.py in a venv and compare the state tables and T-s plot data
[ ] C-281  T-TRANSLATE  LDS-008  → cycles/refrigeration_heat_pumps/recuperated_brayton_hthp  — air recuperated Brayton high-temperature heat pump, steady design point, standalone + TES-integrated layouts; verification: re-run main/standalone_base_recup_hthp.py in a venv and compare the design results (confirm the repository licence first)
```

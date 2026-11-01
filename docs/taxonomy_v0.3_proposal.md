# C-139 taxonomy review at M2: proposal for v0.3 (299 models)

Read-only review. Counts come from `library.json`. All IDs below were checked to exist and to be assigned exactly once.

## 1. Counts per category (v0.2)

| Category | Subcategory: models (flag) |
|---|---|
| fundamentals | properties 8, **processes 21 (>15)**, combustion 7 |
| heat_transfer | conduction 1 (near-empty), **convection 20 (>15)**, radiation 1 (near-empty), pressure_drop 6 |
| components | **heat_exchangers 27**, **compressors 28**, expanders_turbines 14, pumps_fans 10, valves_nozzles_piping 9, boilers_burners 6, storage 2 (near-empty), instrumentation 2 (near-empty) |
| cycles | steam_power 10, organic_rankine 11, **gas_turbines 16**, **engines 24**, **refrigeration_heat_pumps 32**, absorption_sorption 2 (near-empty) |
| hvac | psychrometrics 6, air_handling 11, cooling_towers 7 |
| renewables | solar_thermal 5, photovoltaics 1 (near-empty), geothermal_biomass **0 (empty)** |
| buildings | 6 |
| energy_systems | cogeneration 3, district_heating 1 (near-empty), economics 2 (near-empty) |

Two points about the rules:
- The ~40-model rule in `docs/taxonomy.md` is too high for browsing. Proposed new rule: split above ~20 models, or above ~15 when a physical-system split is obvious.
- Categories are limited to two levels. The M1 note of `roadmap.md` (P6.2) suggested `compressors/positive_displacement`, which would be a third level. I use flat sibling subcategories under `components/` and `cycles/` instead.

## 2. Proposed splits (every model of the old subcategory is assigned)

**components/compressors (28) becomes 3 + 1 misfiled move.** Split by machine type, as in the M1 recommendation.
- `compressors_positive_displacement` (16): CSL-0007, 0020, 0021, 0022, 0067, 0123, 0136, 0156, 0157, 0167, 0202, 0217, 0245, 0260, 0268, 0269 (piston, scroll, screw, Roots, catalogue and identification models).
- `compressors_turbo` (8): CSL-0023, 0035, 0069, 0177, 0181, 0213, 0235, 0328 (centrifugal/radial, similarity, maps, loss models).
- Moved out (see §3): CSL-0010, 0169, 0270 go to `fundamentals/processes` (ideal compression, no machine model); CSL-0152 (turbocharger) goes to `cycles/engines`.

**components/heat_exchangers (27) becomes 2 + 2 moves.** Split by physical system: phase-change exchangers against single-phase and generic ones.
- `condensers_evaporators` (11): CSL-0008, 0014, 0031, 0032, 0112, 0113, 0114, 0115, 0124, 0138, 0173.
- `heat_exchangers` stays (15): CSL-0002, 0026, 0027, 0090, 0096, 0102, 0105, 0110, 0111, 0126, 0127, 0128, 0137, 0161, 0315.
- Moved out: CSL-0081 to `renewables/geothermal_biomass`, CSL-0286 to `hvac/cooling_towers`. CSL-0124 comes in from `pressure_drop`.

**cycles/refrigeration_heat_pumps (32) becomes 3 + 2 moves.** This matches the M1 `heat_pumps` / `refrigeration` recommendation, plus a third group for industrial and high-temperature machines.
- `refrigeration` (10): CSL-0001, 0015, 0061, 0077, 0145, 0148, 0209, 0212, 0216, 0222.
- `heat_pumps` (14): CSL-0013, 0025, 0033, 0054, 0068, 0078, 0116, 0133, 0155, 0171, 0228, 0246, 0319, 0324.
- `high_temperature_heat_pumps` (6): CSL-0039, 0250, 0251, 0253, 0254, 0313 (sink at about 80 C and above, cascade and industrial).
- Moved out: CSL-0186 (Carnot engine + refrigerator) to `fundamentals/processes`; CSL-0303 (evaporative condenser) to `hvac/cooling_towers`.

**cycles/engines (24) becomes 3 + 1 incoming.** Three separate kinds of content are mixed today.
- `air_standard_cycles` (5): CSL-0049, 0059, 0192, 0201, 0280 (Otto, Diesel, Stirling).
- `engine_models` (5): CSL-0024, 0034, 0149, 0152, 0272 (crank-angle, gas-engine and turbocharger operating-point models).
- `engines` stays (15): CSL-0151, 0178, 0185, 0188, 0206, 0221, 0223, 0244, 0273, 0274, 0275, 0276, 0277, 0278, 0279 (sizing, air and fuel flow, data-sheet coherence and ISO 3046 derating, emissions).

**fundamentals/processes (21) becomes 2.** Split by system type.
- `closed_systems` (14): CSL-0003, 0048, 0172, 0176, 0210, 0214, 0225, 0230, 0237, 0241, 0243, 0283, 0285, 0320 (tanks, piston-cylinders, uniform-state tank discharge). CSL-0003 comes from `properties`.
- `processes` stays (12): CSL-0010, 0045, 0056, 0057, 0169, 0186, 0193, 0197, 0242, 0247, 0270, 0323. New description: steady-flow devices, mixing, exergy and second law.

**heat_transfer/convection (20) becomes 2 + 1 move.**
- `two_phase_heat_transfer` (4): CSL-0088, 0089, 0097, 0098 (boiling, condensation, two-phase in tube).
- `convection` stays (15): CSL-0086, 0087, 0091, 0092, 0093, 0094, 0095, 0099, 0100, 0101, 0104, 0108, 0109, 0321, 0322.
- Moved out: CSL-0131 (void fraction) to `pressure_drop`, as its taxonomy description says.

**cycles/gas_turbines (16): no split.** It is a coherent family. The only candidate is the 3 turbojets, which is too small a group.

## 3. Misfiled models

| Model | Better category | Reason |
|---|---|---|
| CSL-0081 vertical_ghes_refsim | renewables/geothermal_biomass | Borefield, the folder `docs/taxonomy.md` reserves for it; also fills the empty subcategory. |
| CSL-0286 indirect_contact_tower_identification | hvac/cooling_towers | Fluid cooler, not a plain exchanger. |
| CSL-0227 evaporative_condenser_effectiveness | hvac/cooling_towers | Evaporative equipment sitting in `air_handling`. |
| CSL-0303 evaporative_condenser_catalogue | hvac/cooling_towers | Same physics as CSL-0227. |
| CSL-0131 void_fraction_correlations | heat_transfer/pressure_drop | `pressure_drop` is declared to hold void-fraction correlations. |
| CSL-0152 turbocharger_combustion_products | cycles/engine_models | Main object is the engine boost system, like CSL-0221 and 0223. |
| CSL-0186 carnot_engine_refrigerator | fundamentals/processes | Second-law exercise, not a refrigeration cycle. |
| CSL-0010, 0169, 0270 | fundamentals/processes | Ideal compression exercises with no compressor model. |
| CSL-0003 methane_tank_evaporation | fundamentals/closed_systems | Tank energy balance, not a property model. |
| CSL-0124 plate_hx_pressure_drop_identification | components/condensers_evaporators | Steady plate-HX model, not a correlation library. |
| CSL-0158 gas_pipe_insulated_pressure_drop | components/valves_nozzles_piping | A pipe model, like CSL-0196. |

## 4. Near-empty subcategories

- Merge `renewables/photovoltaics` (1) into `solar_thermal`, renamed `solar` (6 models). `geothermal_biomass` is kept and gets CSL-0081.
- Keep `conduction` 1, `radiation` 1, `storage` 2, `instrumentation` 2, `absorption_sorption` 2, `district_heating` 1 and `economics` 2. The backlog and the M1 note fill them, and merging unrelated physics would hurt browsing.

## 5. Version bump and file changes (described, not applied)

Version goes from 0.2 to **0.3**.

- `taxonomy.json`:
  - set `version` to "0.3";
  - add keys `compressors_positive_displacement`, `compressors_turbo`, `condensers_evaporators` (under `components`);
  - add `refrigeration`, `heat_pumps`, `high_temperature_heat_pumps`, `air_standard_cycles`, `engine_models` (under `cycles`; remove `refrigeration_heat_pumps` and `compressors`);
  - add `closed_systems` (under `fundamentals`) and `two_phase_heat_transfer` (under `heat_transfer`);
  - rename `solar_thermal` to `solar`;
  - rewrite the descriptions of `heat_exchangers`, `engines`, `processes`, `convection`, `pressure_drop` and `cooling_towers`.
- `docs/taxonomy.md`:
  - section 1 title and tree to v0.3;
  - the split rule changed to ~20 models;
  - a rule that sibling names carry the family prefix (`compressors_...`);
  - the `category_guess` mapping table updated (compressors, heat_exchangers, engines, refrigeration_heat_pumps, fundamentals, solar_renewables);
  - the M1 clarification that ideal-gas cycles go to `engines` or `gas_turbines`, not `processes`.
- Other files: `README.md` (version and tree), the roadmap P6.2 log, and `library.json` and `library.html` (regenerated). Each moved model needs `git mv`, `previous_paths` and a rebuild.
- Check that `redirects.csv` stays unique when the old `compressors` and `refrigeration_heat_pumps` keys disappear.

**CoolSolve GUI Library menu.** It follows the taxonomy folders. After the split, `components` has 10 entries and `cycles` 9. These entries must have a short `title` in `taxonomy.json`, because the menu shows titles rather than keys. The menu's sort order must be checked, since flat siblings such as `compressors_*` need to stay adjacent. Library models are resolved by ID through `library.json` and `redirects.csv`, so `$INCLUDE 'library:CSL-xxxx'` keeps working. The GUI should be tested once against the regenerated `library.json`, and the library tag should be bumped at the next release (P6.3).

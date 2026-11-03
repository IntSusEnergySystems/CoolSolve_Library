# Taxonomy v0.3 — plan (applied 2026-11-03)

Single plan of the v0.3 taxonomy (2026-11-03). It replaces the C-139 proposal, the C-491 move CSV and the C-491 category drafts,
and it is the input of `tools/move_model.py`. Applied on 2026-11-03 with `tools/move_model.py --plan docs/taxonomy_v0.3.md` (not committed yet): `taxonomy.json` is v0.3 and the folders have moved; the file is kept as the rationale and the record of the moves.

## 1. Rules

The goal is smooth browsing of the library in `library.html` and in the **Library** button of the CoolSolve GUI. The GUI menu
(`CoolSolve/src/library_store.cpp`, `LibraryStore::menu`) has exactly two levels (top category → subcategory → models). It lists
the categories in `taxonomy.json` order, shows only `verified` models (sorted by title) and hides empty categories. Hence:

- **Two levels at most.** A third level would need a GUI change. Long lists are split into sibling subcategories instead.
- **3 to 7 models per subcategory** (a few exceptions of 2, stated in section 2). Above 7, split by physical system or machine type;
  below 3, merge with the nearest sibling, unless the subject is distinct and the backlog will fill it.
- **At most about 9 subcategories per top category**, so that each GUI submenu stays short. A top category with 7 models or fewer
  holds its models directly, without subcategories (`buildings` already does).
- **Browse by object.** A textbook exercise on a machine sits with that machine (steam-turbine exercises under steam turbines). An
  exercise on a principle with no machine model (ideal or staged compression, tank energy balance, Carnot) sits in `fundamentals`.
- Keys are lower-case `snake_case`, unique among siblings; folder names of the models are unchanged (no renames).

## 2. Tree and counts

302 models (277 verified, shown in the GUI), 12 top categories, 57 leaf categories; leaf size 2–7, median 5.
Counts are *all models / verified models (GUI)*.

- **Fundamentals** `fundamentals` — 39 / 35, 7 subcategories
  - Properties `fundamentals/properties` — 5 / 5
  - Property libraries `fundamentals/property_libraries` — 4 / 4
  - Tanks and vessels `fundamentals/tanks_vessels` — 7 / 7
  - Piston-cylinder devices `fundamentals/piston_cylinders` — 5 / 5
  - Steady-flow processes `fundamentals/steady_flow` — 5 / 5
  - Second law and exergy `fundamentals/second_law` — 6 / 6
  - Combustion `fundamentals/combustion` — 7 / 3
- **Heat transfer** `heat_transfer` — 27 / 27, 6 subcategories
  - Conduction, fins and radiation `heat_transfer/conduction_radiation` — 3 / 3
  - Internal convection `heat_transfer/internal_convection` — 6 / 6
  - External convection `heat_transfer/external_convection` — 6 / 6
  - Natural convection `heat_transfer/natural_convection` — 3 / 3
  - Boiling and condensation `heat_transfer/two_phase` — 5 / 5
  - Pressure drop `heat_transfer/pressure_drop` — 4 / 4
- **Heat exchangers** `heat_exchangers` — 27 / 27, 5 subcategories
  - Rating and sizing methods `heat_exchangers/methods` — 6 / 6
  - Single-phase exchangers `heat_exchangers/effectiveness_lmtd` — 5 / 5
  - Plate heat exchangers `heat_exchangers/plate` — 6 / 6
  - Zoned and discretised models `heat_exchangers/zoned_discretised` — 5 / 5
  - Condensers and evaporators `heat_exchangers/condensers_evaporators` — 5 / 5
- **Compressors, turbines and pumps** `machines` — 48 / 48, 9 subcategories
  - Reciprocating compressors `machines/reciprocating_compressors` — 6 / 6
  - Scroll, screw and Roots compressors `machines/rotary_compressors` — 5 / 5
  - Compressor catalogues and maps `machines/compressor_maps` — 5 / 5
  - Turbocompressors `machines/turbocompressors` — 5 / 5
  - Turbomachine design `machines/turbomachine_design` — 5 / 5
  - Steam turbines `machines/steam_turbines` — 6 / 6
  - Expanders and turbo-expanders `machines/expanders` — 7 / 7
  - Pumps `machines/pumps` — 5 / 5
  - Fans `machines/fans` — 4 / 4
- **Other components** `components` — 20 / 18, 4 subcategories
  - Boilers and burners `components/boilers_burners` — 6 / 5
  - Nozzles, diffusers and ejectors `components/nozzles_ejectors` — 5 / 5
  - Pipes, valves and flow meters `components/piping_valves` — 7 / 7
  - Thermal storage `components/storage` — 2 / 1
- **Power cycles** `power_cycles` — 37 / 35, 8 subcategories
  - Steam power plants `power_cycles/steam_basic` — 5 / 5
  - Reheat and regenerative steam cycles `power_cycles/steam_advanced` — 5 / 5
  - Organic Rankine cycles `power_cycles/orc_design` — 6 / 6
  - ORC off-design and applications `power_cycles/orc_applications` — 4 / 3
  - Gas turbine cycles `power_cycles/gas_turbine_design` — 6 / 6
  - Gas turbines off design `power_cycles/gas_turbine_offdesign` — 5 / 4
  - Jet propulsion `power_cycles/jet_propulsion` — 3 / 3
  - Supercritical and combined cycles `power_cycles/supercritical_combined` — 3 / 3
- **Engines** `engines` — 26 / 21, 4 subcategories
  - Air-standard cycles `engines/air_standard_cycles` — 5 / 4
  - Engine and boost models `engines/engine_models` — 7 / 5
  - Engine sizing `engines/sizing` — 7 / 6
  - Performance and emissions `engines/performance` — 7 / 6
- **Refrigeration and heat pumps** `refrigeration_heat_pumps` — 32 / 29, 6 subcategories
  - Refrigeration cycles `refrigeration_heat_pumps/refrigeration_cycles` — 6 / 6
  - Refrigeration systems and chillers `refrigeration_heat_pumps/refrigeration_systems` — 5 / 5
  - Absorption chillers `refrigeration_heat_pumps/absorption` — 2 / 2
  - Heat pump cycles `refrigeration_heat_pumps/heat_pump_cycles` — 6 / 6
  - Heat pump systems `refrigeration_heat_pumps/heat_pump_systems` — 7 / 5
  - High-temperature heat pumps `refrigeration_heat_pumps/high_temperature` — 6 / 5
- **HVAC** `hvac` — 26 / 20, 5 subcategories
  - Psychrometrics `hvac/psychrometrics` — 5 / 5
  - Cooling coils `hvac/cooling_coils` — 7 / 4
  - Air handling `hvac/air_handling` — 4 / 2
  - Cooling towers `hvac/cooling_towers` — 7 / 7
  - Evaporative condensers and fluid coolers `hvac/evaporative_coolers` — 3 / 2
- **Buildings** `buildings` — 6 / 6 (no subcategories)
- **Renewables** `renewables` — 7 / 5 (no subcategories)
- **Energy systems** `energy_systems` — 7 / 6 (no subcategories)

**Exceptions and GUI notes.**
- `components/storage` (2, one verified) and `refrigeration_heat_pumps/absorption` (2) are kept as exceptions: distinct objects
  (dynamic storage tanks; absorption cycles) that the backlog will fill, and merging them into an unrelated sibling would hide them.
  `hvac/air_handling` and `hvac/evaporative_coolers` hold blocked models that the GUI hides until their CoolSolve gaps close.
- Emissions are not a subcategory of their own: the two exhaust-gas analyses (CSL-0058, CSL-0266, blocked) are combustion
  stoichiometry and stay in `fundamentals/combustion`; fuel and CO2 figures join `engines/performance`, so no GUI submenu shows one model.
- `machines` has 9 subcategories, the maximum; `power_cycles` 8.

**Judgement calls to confirm.** CSL-0326 thermosyphon in `heat_exchangers/zoned_discretised` (row-by-row model) rather than
condensers; CSL-0147 SEGS stays a steam cycle (`power_cycles/steam_advanced`) rather than `renewables`; CSL-0058/0266 (excess air
from exhaust-gas analysis of engines) stay in `fundamentals/combustion`; CSL-0323 electrolyser and fuel cell goes to
`energy_systems`; CSL-0186 Carnot engine + refrigerator to `fundamentals/second_law`; CSL-0010/0169/0270 (compression with no
machine model) to `fundamentals/steady_flow`. The borderline pairs of the library audit (CSL-0226/0295 turbojets, CSL-0032/0227
condensers, CSL-0310 vs CSL-0199/0207/0234 nozzles) end up as neighbours or in sibling categories, which makes them easy to compare.

## 3. `taxonomy.json` v0.3

The complete file. `tools/move_model.py --plan docs/taxonomy_v0.3.md` writes it to `taxonomy.json` before moving the models.
Top categories `cycles` and the old subcategories `compressors`, `refrigeration_heat_pumps`, `solar_thermal`, `photovoltaics`, … disappear;
the old paths keep working through `previous_paths` and `redirects.csv` (`$INCLUDE 'library:CSL-xxxx'` resolves by ID).

```json
{
  "version": "0.3",
  "description": "Folder taxonomy of the CoolSolve Library. A model's category is its parent folder under models/. Kind, level and status are facets stored in model.json (see docs/taxonomy.md). Change this file together with the folders (docs/taxonomy.md, section 'Changing the taxonomy').",
  "categories": [
    {
      "key": "fundamentals",
      "title": "Fundamentals",
      "description": "Thermodynamic basics: properties, closed and open systems, first and second law, combustion chemistry.",
      "children": [
        {
          "key": "properties",
          "title": "Properties",
          "description": "Exercises on fluid states and property functions: real versus ideal gas, constant cp versus property calls, two-phase states, densities."
        },
        {
          "key": "property_libraries",
          "title": "Property libraries",
          "description": "Function libraries of thermophysical properties not built into CoolSolve: brines, heat-transfer fluids, single-fluid correlations, pseudo-critical properties."
        },
        {
          "key": "tanks_vessels",
          "title": "Tanks and vessels",
          "description": "Rigid tanks and vessels: constant-volume heating and cooling, connected tanks, charge and discharge of a tank (uniform-state open systems)."
        },
        {
          "key": "piston_cylinders",
          "title": "Piston-cylinder devices",
          "description": "Closed systems with boundary work: piston-cylinders with springs or stops, isothermal, adiabatic and polytropic compression and expansion."
        },
        {
          "key": "steady_flow",
          "title": "Steady-flow processes",
          "description": "First-law exercises on steady-flow processes: ideal and staged compression, mixing of streams, hydraulic power."
        },
        {
          "key": "second_law",
          "title": "Second law and exergy",
          "description": "Entropy generation, exergy destruction, reversible work, Carnot engines and refrigerators."
        },
        {
          "key": "combustion",
          "title": "Combustion",
          "description": "Stoichiometry, excess air and exhaust-gas analysis, mean specific heat of the products (cpbar), combustion chamber, adiabatic flame temperature, dissociation."
        }
      ]
    },
    {
      "key": "heat_transfer",
      "title": "Heat transfer",
      "description": "Heat-transfer mechanisms and correlations, independent of a specific component (mostly function libraries).",
      "children": [
        {
          "key": "conduction_radiation",
          "title": "Conduction, fins and radiation",
          "description": "Thermal resistances and shape factors, fin efficiency, radiative exchange between surfaces."
        },
        {
          "key": "internal_convection",
          "title": "Internal convection",
          "description": "Single-phase convection inside pipes, curved and printed-circuit channels, near-critical fluids and engine cylinders."
        },
        {
          "key": "external_convection",
          "title": "External convection",
          "description": "Forced convection over plates, cylinders, tube banks, finned bundles, shell sides and packed beds."
        },
        {
          "key": "natural_convection",
          "title": "Natural convection",
          "description": "Free convection from plates, spheres and cylinders, in enclosures and jacketed vessels."
        },
        {
          "key": "two_phase",
          "title": "Boiling and condensation",
          "description": "Pool and flow boiling, critical heat flux, film condensation, two-phase non-boiling flow, void fraction."
        },
        {
          "key": "pressure_drop",
          "title": "Pressure drop",
          "description": "Friction factors, straight-pipe and two-phase pressure drop, bends, tube banks and shell sides."
        }
      ]
    },
    {
      "key": "heat_exchangers",
      "title": "Heat exchangers",
      "description": "Heat-exchanger models and the methods to rate and size them.",
      "children": [
        {
          "key": "methods",
          "title": "Rating and sizing methods",
          "description": "Function libraries: effectiveness-NTU, P-NTU, LMTD and correction factors, zone procedures, shell-and-tube sizing, part-load UA scaling."
        },
        {
          "key": "effectiveness_lmtd",
          "title": "Single-phase exchangers",
          "description": "Single-phase counterflow, crossflow and generic exchangers rated by effectiveness-NTU, a constant effectiveness or UA-LMTD."
        },
        {
          "key": "plate",
          "title": "Plate heat exchangers",
          "description": "Plate heat exchangers: heat-transfer and pressure-drop correlations, thermal-resistance and three-zone condenser/evaporator models."
        },
        {
          "key": "zoned_discretised",
          "title": "Zoned and discretised models",
          "description": "Multi-zone (pinch-based), finite-volume, moving-boundary and row-by-row discretised exchangers."
        },
        {
          "key": "condensers_evaporators",
          "title": "Condensers and evaporators",
          "description": "Air-cooled, water-cooled and shell-and-tube condensers, wet-coil evaporators."
        }
      ]
    },
    {
      "key": "machines",
      "title": "Compressors, turbines and pumps",
      "description": "Models of rotating and reciprocating machines: compressors, expanders, turbines, pumps and fans.",
      "children": [
        {
          "key": "reciprocating_compressors",
          "title": "Reciprocating compressors",
          "description": "Piston compressors: parameter identification, suction pressure drop, leakage, speed laws."
        },
        {
          "key": "rotary_compressors",
          "title": "Scroll, screw and Roots compressors",
          "description": "Rotary positive-displacement compressors: semi-empirical scroll, screw and Roots models."
        },
        {
          "key": "compressor_maps",
          "title": "Compressor catalogues and maps",
          "description": "Compressors described by catalogue data and polynomials (ARI, EN 12900, manufacturer tables)."
        },
        {
          "key": "turbocompressors",
          "title": "Turbocompressors",
          "description": "Centrifugal compressors: performance, power, performance maps and design similarity."
        },
        {
          "key": "turbomachine_design",
          "title": "Turbomachine design",
          "description": "Similarity laws, specific speed and diameter (Cordier), axial and radial loss models."
        },
        {
          "key": "steam_turbines",
          "title": "Steam turbines",
          "description": "Steam turbines: isentropic efficiency, heat loss, wet expansion (Baumann), off-design (Stodola cone law)."
        },
        {
          "key": "expanders",
          "title": "Expanders and turbo-expanders",
          "description": "Scroll and volumetric expanders, empirical ORC expander maps, turbo-expanders and small gas or vapour turbines."
        },
        {
          "key": "pumps",
          "title": "Pumps",
          "description": "Centrifugal pumps: manufacturer curves, similarity laws, dimensionless polynomials, variable speed."
        },
        {
          "key": "fans",
          "title": "Fans",
          "description": "Centrifugal and variable-speed fans: reference models and dimensionless polynomials."
        }
      ]
    },
    {
      "key": "components",
      "title": "Other components",
      "description": "Boilers, nozzles and ejectors, pipes, ducts, valves and flow meters, thermal storage.",
      "children": [
        {
          "key": "boilers_burners",
          "title": "Boilers and burners",
          "description": "Fuel-oil, gas and condensing boilers, modulating and on/off burners, parameter identification."
        },
        {
          "key": "nozzles_ejectors",
          "title": "Nozzles, diffusers and ejectors",
          "description": "Isentropic and steam nozzles, critical flow, diffusers, single- and two-phase ejectors."
        },
        {
          "key": "piping_valves",
          "title": "Pipes, valves and flow meters",
          "description": "Pipe and duct models, valve authority, orifice plates and nozzle flow measurement."
        },
        {
          "key": "storage",
          "title": "Thermal storage",
          "description": "Hot-water and ice storage tanks (dynamic)."
        }
      ]
    },
    {
      "key": "power_cycles",
      "title": "Power cycles",
      "description": "Thermodynamic power cycles: steam Rankine, organic Rankine, gas turbines, jet propulsion, supercritical CO2 and combined cycles.",
      "children": [
        {
          "key": "steam_basic",
          "title": "Steam power plants",
          "description": "Simple steam Rankine cycles and plants: component balances, cooling by a river, part load."
        },
        {
          "key": "steam_advanced",
          "title": "Reheat and regenerative steam cycles",
          "description": "Steam cycles with reheat, extractions and feedwater heaters, solar steam plant."
        },
        {
          "key": "orc_design",
          "title": "Organic Rankine cycles",
          "description": "ORC design points: simple, recuperated, with extraction, double-stage plants, power ratios."
        },
        {
          "key": "orc_applications",
          "title": "ORC off-design and applications",
          "description": "ORC off-design and charge, waste-heat recovery and biomass CHP."
        },
        {
          "key": "gas_turbine_design",
          "title": "Gas turbine cycles",
          "description": "Brayton cycles and gas turbines at design: open cycle, intercooling, reheat, regeneration, inlet cooling."
        },
        {
          "key": "gas_turbine_offdesign",
          "title": "Gas turbines off design",
          "description": "Gas turbines at part load and any regime: reduced quantities, compressor and expander maps."
        },
        {
          "key": "jet_propulsion",
          "title": "Jet propulsion",
          "description": "Turbojets: ideal, with component efficiencies, with afterburner."
        },
        {
          "key": "supercritical_combined",
          "title": "Supercritical and combined cycles",
          "description": "Supercritical CO2 cycles and combined gas-steam cycles."
        }
      ]
    },
    {
      "key": "engines",
      "title": "Engines",
      "description": "Reciprocating internal-combustion engines: ideal cycles, engine and boost models, sizing, performance and emissions.",
      "children": [
        {
          "key": "air_standard_cycles",
          "title": "Air-standard cycles",
          "description": "Ideal-gas Otto, Diesel and Stirling cycles."
        },
        {
          "key": "engine_models",
          "title": "Engine and boost models",
          "description": "Crank-angle and operating-point models of gas engines; supercharged and turbocharged engines (air flow, compressor and turbine matching)."
        },
        {
          "key": "sizing",
          "title": "Engine sizing",
          "description": "Cylinder count and geometry, intake valves, valve timing, fuel injection."
        },
        {
          "key": "performance",
          "title": "Performance and emissions",
          "description": "Dynamometer tests, data-sheet coherence, bsfc, ISO 3046 derating, fuel consumption, exhaust emissions and CO2 per km."
        }
      ]
    },
    {
      "key": "refrigeration_heat_pumps",
      "title": "Refrigeration and heat pumps",
      "description": "Vapour-compression, gas and absorption refrigeration cycles and heat pumps.",
      "children": [
        {
          "key": "refrigeration_cycles",
          "title": "Refrigeration cycles",
          "description": "Basic vapour-compression refrigeration cycles: compressor models, volume ratio, losses, unloaded cylinders."
        },
        {
          "key": "refrigeration_systems",
          "title": "Refrigeration systems and chillers",
          "description": "Chillers, domestic refrigerators, CO2 booster systems, reverse Brayton air cycles."
        },
        {
          "key": "absorption",
          "title": "Absorption chillers",
          "description": "LiBr-water and ammonia-water absorption cycles."
        },
        {
          "key": "heat_pump_cycles",
          "title": "Heat pump cycles",
          "description": "Basic heat pump cycles: COP, second-law efficiency, pinch-sized exchangers."
        },
        {
          "key": "heat_pump_systems",
          "title": "Heat pump systems",
          "description": "Air-source, brine-to-water and inverter heat pumps from component and catalogue models, zeotropic mixtures."
        },
        {
          "key": "high_temperature",
          "title": "High-temperature heat pumps",
          "description": "Industrial heat pumps with a sink at about 80 °C and above: cascade, two-stage NH3, R245fa, R1336mzz(Z), Brayton."
        }
      ]
    },
    {
      "key": "hvac",
      "title": "HVAC",
      "description": "Heating, ventilation and air conditioning: moist air, coils, air handling, cooling towers.",
      "children": [
        {
          "key": "psychrometrics",
          "title": "Psychrometrics",
          "description": "Moist-air states, adiabatic mixing, saturation, wet bulb, steam injection."
        },
        {
          "key": "cooling_coils",
          "title": "Cooling coils",
          "description": "Air cooling and dehumidifying coils: contact factor, dry and wet regimes, control, reheat."
        },
        {
          "key": "air_handling",
          "title": "Air handling",
          "description": "Air handling units, humidifiers, heating coils and heat-recovery loops."
        },
        {
          "key": "cooling_towers",
          "title": "Cooling towers",
          "description": "Wet cooling towers: direct contact, catalogue data, fan speed and air-flow control."
        },
        {
          "key": "evaporative_coolers",
          "title": "Evaporative condensers and fluid coolers",
          "description": "Evaporative condensers and indirect-contact cooling towers (fluid coolers)."
        }
      ]
    },
    {
      "key": "buildings",
      "title": "Buildings",
      "description": "Building thermal models, terminal units and comfort."
    },
    {
      "key": "renewables",
      "title": "Renewables",
      "description": "Solar collectors and geometry, photovoltaic modules, solar ORC, ground-source boreholes."
    },
    {
      "key": "energy_systems",
      "title": "Energy systems",
      "description": "Cogeneration, district heating, hydrogen and the economics of energy investments."
    }
  ]
}
```

## 4. Moves

259 of 302 models change category (no folder renames); 43 stay where they are (`heat_transfer/pressure_drop`, `components/boilers_burners`,
`buildings`, … kept their path). `tools/move_model.py` reads the rows of this table (first column the ID, last column the target).

| ID | Model | From | To |
|---|---|---|---|
| CSL-0118 | air_nozzle_ejector | components/valves_nozzles_piping | components/nozzles_ejectors |
| CSL-0180 | aircraft_engine_diffuser | components/valves_nozzles_piping | components/nozzles_ejectors |
| CSL-0190 | steam_nozzle_exit | components/valves_nozzles_piping | components/nozzles_ejectors |
| CSL-0310 | isentropic_nozzle_critical | components/valves_nozzles_piping | components/nozzles_ejectors |
| CSL-0325 | ejector_two_phase_co2 | components/valves_nozzles_piping | components/nozzles_ejectors |
| CSL-0075 | iso5167_orifice_plate_flow_rate | components/instrumentation | components/piping_valves |
| CSL-0120 | ball_valve_authority | components/valves_nozzles_piping | components/piping_valves |
| CSL-0122 | nozzle_discharge_coefficients | components/instrumentation | components/piping_valves |
| CSL-0158 | gas_pipe_insulated_pressure_drop | heat_transfer/pressure_drop | components/piping_valves |
| CSL-0170 | return_duct_simplified | components/valves_nozzles_piping | components/piping_valves |
| CSL-0196 | reference_pipe | components/valves_nozzles_piping | components/piping_valves |
| CSL-0311 | return_duct_paramid | components/valves_nozzles_piping | components/piping_valves |
| CSL-0142 | district_heating_loop | energy_systems/district_heating | energy_systems |
| CSL-0146 | cgam_cogeneration | energy_systems/cogeneration | energy_systems |
| CSL-0154 | investment_npv_payback | energy_systems/economics | energy_systems |
| CSL-0233 | cogeneration_monthly_demand | energy_systems/cogeneration | energy_systems |
| CSL-0261 | gas_engine_rankine_bottoming | energy_systems/cogeneration | energy_systems |
| CSL-0262 | investment_npv_irr | energy_systems/economics | energy_systems |
| CSL-0323 | h2_electrolyzer_fuel_cell | fundamentals/processes | energy_systems |
| CSL-0049 | otto_cycle_air_standard | cycles/engines | engines/air_standard_cycles |
| CSL-0059 | stirling_cycle_ideal_regenerator | cycles/engines | engines/air_standard_cycles |
| CSL-0192 | otto_cycle_cengel | cycles/engines | engines/air_standard_cycles |
| CSL-0201 | stirling_cycle_r4bis | cycles/engines | engines/air_standard_cycles |
| CSL-0280 | diesel_cycle_air_standard | cycles/engines | engines/air_standard_cycles |
| CSL-0024 | single_cylinder_engine_weibe | cycles/engines | engines/engine_models |
| CSL-0034 | gas_engine_full_power_cpbar | cycles/engines | engines/engine_models |
| CSL-0149 | gas_engine_complete_model | cycles/engines | engines/engine_models |
| CSL-0152 | turbocharger_combustion_products | components/compressors | engines/engine_models |
| CSL-0221 | supercharged_engine_air_flow | cycles/engines | engines/engine_models |
| CSL-0223 | turbocharged_engine_expander | cycles/engines | engines/engine_models |
| CSL-0272 | gas_engine_identified_nominal_point | cycles/engines | engines/engine_models |
| CSL-0151 | engine_derating_iso3046 | cycles/engines | engines/performance |
| CSL-0188 | fuel_co2_per_km | cycles/engines | engines/performance |
| CSL-0244 | engine_dynamometer_test | cycles/engines | engines/performance |
| CSL-0273 | engine_data_coherence_derating | cycles/engines | engines/performance |
| CSL-0274 | scania_marine_diesel_handbook | cycles/engines | engines/performance |
| CSL-0278 | vehicle_exhaust_emissions | cycles/engines | engines/performance |
| CSL-0279 | engine_bsfc_bore_stroke_afr | cycles/engines | engines/performance |
| CSL-0178 | intake_valve_sizing | cycles/engines | engines/sizing |
| CSL-0185 | diesel_injection_sizing | cycles/engines | engines/sizing |
| CSL-0206 | gasoline_double_injection | cycles/engines | engines/sizing |
| CSL-0275 | square_v6_engine_exercise | cycles/engines | engines/sizing |
| CSL-0276 | valve_overlap_timing | cycles/engines | engines/sizing |
| CSL-0277 | fuel_injection_ci_engine | cycles/engines | engines/sizing |
| CSL-0331 | engine_cylinder_count | cycles/engines | engines/sizing |
| CSL-0047 | nonideal_gas_isothermal_work | fundamentals/properties | fundamentals/piston_cylinders |
| CSL-0176 | piston_cylinder_water_constant_pressure | fundamentals/processes | fundamentals/piston_cylinders |
| CSL-0210 | piston_cylinder_spring_water | fundamentals/processes | fundamentals/piston_cylinders |
| CSL-0214 | piston_cylinder_stops_air | fundamentals/processes | fundamentals/piston_cylinders |
| CSL-0285 | argon_piston_compression | fundamentals/processes | fundamentals/piston_cylinders |
| CSL-0225 | co2_tank_ideal_gas | fundamentals/processes | fundamentals/properties |
| CSL-0237 | air_isentropic_compression_cp | fundamentals/processes | fundamentals/properties |
| CSL-0241 | helium_balloon_buoyancy | fundamentals/processes | fundamentals/properties |
| CSL-0079 | brineprop_secondary_refrigerants | fundamentals/properties | fundamentals/property_libraries |
| CSL-0121 | heat_transfer_fluid_properties | fundamentals/properties | fundamentals/property_libraries |
| CSL-0132 | r1233zd_thermal_conductivity | fundamentals/properties | fundamentals/property_libraries |
| CSL-0317 | pseudo_critical_properties | fundamentals/properties | fundamentals/property_libraries |
| CSL-0045 | steam_turbine_exergy_balance | fundamentals/processes | fundamentals/second_law |
| CSL-0056 | iron_block_quench_water_tank | fundamentals/processes | fundamentals/second_law |
| CSL-0057 | two_tanks_max_work_air | fundamentals/processes | fundamentals/second_law |
| CSL-0186 | carnot_engine_refrigerator | cycles/refrigeration_heat_pumps | fundamentals/second_law |
| CSL-0193 | mixing_chamber_exergy | fundamentals/processes | fundamentals/second_law |
| CSL-0197 | rigid_tank_compressor_exergy | fundamentals/processes | fundamentals/second_law |
| CSL-0010 | two_stage_steam_compressor_intercooling | components/compressors | fundamentals/steady_flow |
| CSL-0169 | r134a_compressor_minimum_power | components/compressors | fundamentals/steady_flow |
| CSL-0242 | hydroelectric_head_power | fundamentals/processes | fundamentals/steady_flow |
| CSL-0247 | water_stream_adiabatic_mixing | fundamentals/processes | fundamentals/steady_flow |
| CSL-0270 | air_compressor_staging_comparison | components/compressors | fundamentals/steady_flow |
| CSL-0003 | methane_tank_evaporation | fundamentals/properties | fundamentals/tanks_vessels |
| CSL-0048 | two_tanks_connected_valve_r12 | fundamentals/processes | fundamentals/tanks_vessels |
| CSL-0172 | rigid_tank_two_compartments_water | fundamentals/processes | fundamentals/tanks_vessels |
| CSL-0230 | rigid_vessel_water_heat_removal | fundamentals/processes | fundamentals/tanks_vessels |
| CSL-0243 | water_tank_entropy_change | fundamentals/processes | fundamentals/tanks_vessels |
| CSL-0283 | helium_bottle_lox_displacement | fundamentals/processes | fundamentals/tanks_vessels |
| CSL-0320 | r12_tank_discharge_heat_supply | fundamentals/processes | fundamentals/tanks_vessels |
| CSL-0008 | condenser_three_zones | components/heat_exchangers | heat_exchangers/condensers_evaporators |
| CSL-0027 | shell_and_tube_steam_condenser | components/heat_exchangers | heat_exchangers/condensers_evaporators |
| CSL-0031 | refrigeration_evaporator_wet_coil | components/heat_exchangers | heat_exchangers/condensers_evaporators |
| CSL-0032 | wet_air_cooled_condenser | components/heat_exchangers | heat_exchangers/condensers_evaporators |
| CSL-0173 | r134a_condenser_water_circuit | components/heat_exchangers | heat_exchangers/condensers_evaporators |
| CSL-0002 | counterflow_hx_oil_water | components/heat_exchangers | heat_exchangers/effectiveness_lmtd |
| CSL-0026 | crossflow_hx_hot_gas_water | components/heat_exchangers | heat_exchangers/effectiveness_lmtd |
| CSL-0126 | hx_constant_effectiveness | components/heat_exchangers | heat_exchangers/effectiveness_lmtd |
| CSL-0128 | hx_eps_ntu_plate_pipe | components/heat_exchangers | heat_exchangers/effectiveness_lmtd |
| CSL-0137 | hx_lmtd_ua | components/heat_exchangers | heat_exchangers/effectiveness_lmtd |
| CSL-0090 | hx_effectiveness_ntu | components/heat_exchangers | heat_exchangers/methods |
| CSL-0102 | hx_temperature_effectiveness_pntu | components/heat_exchangers | heat_exchangers/methods |
| CSL-0105 | lmtd_and_f_correction | components/heat_exchangers | heat_exchangers/methods |
| CSL-0110 | shell_and_tube_sizing | components/heat_exchangers | heat_exchangers/methods |
| CSL-0112 | three_zone_hx_procedures | components/heat_exchangers | heat_exchangers/methods |
| CSL-0315 | ua_cecchinato_partload | components/heat_exchangers | heat_exchangers/methods |
| CSL-0096 | plate_hx_heat_transfer | components/heat_exchangers | heat_exchangers/plate |
| CSL-0111 | plate_hx_correlations | components/heat_exchangers | heat_exchangers/plate |
| CSL-0113 | condenser_3_zones_plate_correlations | components/heat_exchangers | heat_exchangers/plate |
| CSL-0114 | evaporator_3_zones_plate_correlations | components/heat_exchangers | heat_exchangers/plate |
| CSL-0124 | plate_hx_pressure_drop_identification | heat_transfer/pressure_drop | heat_exchangers/plate |
| CSL-0161 | plate_hx_thermal_resistances | components/heat_exchangers | heat_exchangers/plate |
| CSL-0014 | hx_constant_pinch | components/heat_exchangers | heat_exchangers/zoned_discretised |
| CSL-0115 | hx_fem_evaporator_discretised | components/heat_exchangers | heat_exchangers/zoned_discretised |
| CSL-0127 | hx_constant_effectiveness_discretised | components/heat_exchangers | heat_exchangers/zoned_discretised |
| CSL-0138 | hx_moving_boundary_bell | components/heat_exchangers | heat_exchangers/zoned_discretised |
| CSL-0326 | thermosyphon_hx | components/heat_exchangers | heat_exchangers/zoned_discretised |
| CSL-0106 | conduction_resistances_and_shapes | heat_transfer/conduction | heat_transfer/conduction_radiation |
| CSL-0107 | radiation_heat_flux | heat_transfer/radiation | heat_transfer/conduction_radiation |
| CSL-0109 | fin_efficiency_and_wall_factors | heat_transfer/convection | heat_transfer/conduction_radiation |
| CSL-0094 | external_crossflow_cylinder | heat_transfer/convection | heat_transfer/external_convection |
| CSL-0095 | tube_bank_nusselt | heat_transfer/convection | heat_transfer/external_convection |
| CSL-0099 | air_cooler_air_side | heat_transfer/convection | heat_transfer/external_convection |
| CSL-0101 | external_forced_conv_plates | heat_transfer/convection | heat_transfer/external_convection |
| CSL-0108 | packed_bed_nusselt | heat_transfer/convection | heat_transfer/external_convection |
| CSL-0321 | shell_side_htc | heat_transfer/convection | heat_transfer/external_convection |
| CSL-0086 | in_cylinder_htc_correlations | heat_transfer/convection | heat_transfer/internal_convection |
| CSL-0087 | internal_turbulent_nusselt | heat_transfer/convection | heat_transfer/internal_convection |
| CSL-0091 | internal_laminar_and_curved_nu | heat_transfer/convection | heat_transfer/internal_convection |
| CSL-0104 | supercritical_internal_nu | heat_transfer/convection | heat_transfer/internal_convection |
| CSL-0322 | pche_htc | heat_transfer/convection | heat_transfer/internal_convection |
| CSL-0330 | curved_duct_htc | heat_transfer/convection | heat_transfer/internal_convection |
| CSL-0092 | free_conv_cylinders | heat_transfer/convection | heat_transfer/natural_convection |
| CSL-0093 | free_conv_plates_and_sphere | heat_transfer/convection | heat_transfer/natural_convection |
| CSL-0100 | free_conv_enclosed_and_jackets | heat_transfer/convection | heat_transfer/natural_convection |
| CSL-0088 | nucleate_boiling_and_chf | heat_transfer/convection | heat_transfer/two_phase |
| CSL-0089 | condensation_film | heat_transfer/convection | heat_transfer/two_phase |
| CSL-0097 | two_phase_nonboiling_in_tube | heat_transfer/convection | heat_transfer/two_phase |
| CSL-0098 | flow_boiling_in_tubes | heat_transfer/convection | heat_transfer/two_phase |
| CSL-0131 | void_fraction_correlations | heat_transfer/convection | heat_transfer/two_phase |
| CSL-0016 | moist_air_cooling_coil_contact_factor | hvac/psychrometrics | hvac/cooling_coils |
| CSL-0017 | chilled_water_cooling_coil | hvac/air_handling | hvac/cooling_coils |
| CSL-0062 | cooling_coil_condensate_ratio | hvac/air_handling | hvac/cooling_coils |
| CSL-0073 | cooling_coil_with_control_simplified | hvac/air_handling | hvac/cooling_coils |
| CSL-0074 | cooling_coil_refsim | hvac/air_handling | hvac/cooling_coils |
| CSL-0163 | cooling_coil_paramid | hvac/air_handling | hvac/cooling_coils |
| CSL-0292 | room_air_conditioning_coil_reheat | hvac/air_handling | hvac/cooling_coils |
| CSL-0227 | evaporative_condenser_effectiveness | hvac/air_handling | hvac/evaporative_coolers |
| CSL-0286 | indirect_contact_tower_identification | components/heat_exchangers | hvac/evaporative_coolers |
| CSL-0303 | evaporative_condenser_catalogue | cycles/refrigeration_heat_pumps | hvac/evaporative_coolers |
| CSL-0123 | copeland_catalogue_correlation | components/compressors | machines/compressor_maps |
| CSL-0136 | polynomial_compressor_en12900 | components/compressors | machines/compressor_maps |
| CSL-0157 | reciprocating_catalogue_r717 | components/compressors | machines/compressor_maps |
| CSL-0245 | grasso_screw_rpm_efficiencies | components/compressors | machines/compressor_maps |
| CSL-0269 | grasso_screw_catalogue_r717 | components/compressors | machines/compressor_maps |
| CSL-0037 | scroll_expander_semi_empirical | components/expanders_turbines | machines/expanders |
| CSL-0084 | orc_expander_pump_empirical_maps | components/expanders_turbines | machines/expanders |
| CSL-0117 | double_stage_scroll_expander | components/expanders_turbines | machines/expanders |
| CSL-0189 | r134a_turbine_power | components/expanders_turbines | machines/expanders |
| CSL-0199 | turboexpander_laval_wheel | components/expanders_turbines | machines/expanders |
| CSL-0207 | turboexpander_parameter_identification | components/expanders_turbines | machines/expanders |
| CSL-0234 | turboexpander_ideal_nozzle_laval | components/expanders_turbines | machines/expanders |
| CSL-0071 | centrifugal_fan_reference_model | components/pumps_fans | machines/fans |
| CSL-0165 | centrifugal_fan_paramid | components/pumps_fans | machines/fans |
| CSL-0187 | fan_polynomial_identification | components/pumps_fans | machines/fans |
| CSL-0205 | vav_fan_simulation | components/pumps_fans | machines/fans |
| CSL-0072 | centrifugal_brine_pump_refsim | components/pumps_fans | machines/pumps |
| CSL-0125 | pump_curve_similarity | components/pumps_fans | machines/pumps |
| CSL-0183 | pump_polynomial_identification | components/pumps_fans | machines/pumps |
| CSL-0203 | variable_speed_pump_simulation | components/pumps_fans | machines/pumps |
| CSL-0240 | sihi_pump_simulation | components/pumps_fans | machines/pumps |
| CSL-0021 | piston_compressor_identification | components/compressors | machines/reciprocating_compressors |
| CSL-0022 | refrigeration_compressor_identification | components/compressors | machines/reciprocating_compressors |
| CSL-0067 | piston_compressor_suction_drop_leakage | components/compressors | machines/reciprocating_compressors |
| CSL-0167 | reciprocating_polynomial_r22 | components/compressors | machines/reciprocating_compressors |
| CSL-0217 | compressor_inlet_drop_speed_leakage | components/compressors | machines/reciprocating_compressors |
| CSL-0268 | reciprocating_compressor_exponent_m | components/compressors | machines/reciprocating_compressors |
| CSL-0007 | scroll_compressor_semi_empirical | components/compressors | machines/rotary_compressors |
| CSL-0020 | dry_air_screw_compressor_leakage | components/compressors | machines/rotary_compressors |
| CSL-0156 | refrigeration_screw_compressor_r22 | components/compressors | machines/rotary_compressors |
| CSL-0202 | roots_compressor_10l | components/compressors | machines/rotary_compressors |
| CSL-0260 | scroll_compressor_reed_valve | components/compressors | machines/rotary_compressors |
| CSL-0135 | turbine_stodola_offdesign | components/expanders_turbines | machines/steam_turbines |
| CSL-0174 | steam_turbine_isentropic_efficiency | components/expanders_turbines | machines/steam_turbines |
| CSL-0182 | geothermal_steam_turbine | components/expanders_turbines | machines/steam_turbines |
| CSL-0224 | steam_turbine_heat_loss | components/expanders_turbines | machines/steam_turbines |
| CSL-0282 | steam_turbine_n2_compressor | components/expanders_turbines | machines/steam_turbines |
| CSL-0314 | steam_turbine_baumann | components/expanders_turbines | machines/steam_turbines |
| CSL-0023 | centrifugal_turbocompressor_performance | components/compressors | machines/turbocompressors |
| CSL-0035 | centrifugal_compressor_lookup_map | components/compressors | machines/turbocompressors |
| CSL-0069 | centrifugal_compressor_design_similarity | components/compressors | machines/turbocompressors |
| CSL-0181 | centrifugal_air_compressor_power | components/compressors | machines/turbocompressors |
| CSL-0213 | centrifugal_air_compressor_ke | components/compressors | machines/turbocompressors |
| CSL-0177 | turbocompressor_similarity_laws | components/compressors | machines/turbomachine_design |
| CSL-0235 | turbomachine_optimal_diameter | components/compressors | machines/turbomachine_design |
| CSL-0318 | cordier_specific_speed | components/pumps_fans | machines/turbomachine_design |
| CSL-0327 | axial_turbine_loss_models | components/expanders_turbines | machines/turbomachine_design |
| CSL-0328 | radial_machine_loss_models | components/compressors | machines/turbomachine_design |
| CSL-0050 | gas_turbine_two_shaft_intercooled_regenerative | cycles/gas_turbines | power_cycles/gas_turbine_design |
| CSL-0060 | gas_turbine_reheat | cycles/gas_turbines | power_cycles/gas_turbine_design |
| CSL-0141 | gas_turbine_open_cycle | cycles/gas_turbines | power_cycles/gas_turbine_design |
| CSL-0204 | brayton_cycle_cengel_9_76 | cycles/gas_turbines | power_cycles/gas_turbine_design |
| CSL-0294 | gas_turbine_inlet_air_chiller | cycles/gas_turbines | power_cycles/gas_turbine_design |
| CSL-0296 | regenerative_two_shaft_gas_turbine | cycles/gas_turbines | power_cycles/gas_turbine_design |
| CSL-0011 | two_shaft_gas_turbine_compressor_map | cycles/gas_turbines | power_cycles/gas_turbine_offdesign |
| CSL-0200 | gas_turbine_reduced_quantities | cycles/gas_turbines | power_cycles/gas_turbine_offdesign |
| CSL-0218 | gas_turbine_part_load | cycles/gas_turbines | power_cycles/gas_turbine_offdesign |
| CSL-0220 | gas_turbine_any_regime | cycles/gas_turbines | power_cycles/gas_turbine_offdesign |
| CSL-0293 | two_shaft_gas_turbine_expander_map | cycles/gas_turbines | power_cycles/gas_turbine_offdesign |
| CSL-0051 | turbojet_ideal_260ms | cycles/gas_turbines | power_cycles/jet_propulsion |
| CSL-0226 | turbojet_component_efficiencies | cycles/gas_turbines | power_cycles/jet_propulsion |
| CSL-0295 | turbojet_afterburner | cycles/gas_turbines | power_cycles/jet_propulsion |
| CSL-0040 | orc_biomass_chp | cycles/organic_rankine | power_cycles/orc_applications |
| CSL-0153 | orc_whr_refprop_cost | cycles/organic_rankine | power_cycles/orc_applications |
| CSL-0159 | orc_void_fraction_charge | cycles/organic_rankine | power_cycles/orc_applications |
| CSL-0312 | orc_offdesign_scroll_expander | cycles/organic_rankine | power_cycles/orc_applications |
| CSL-0019 | orc_simple_r245fa | cycles/organic_rankine | power_cycles/orc_design |
| CSL-0036 | orc_extraction_r134a | cycles/organic_rankine | power_cycles/orc_design |
| CSL-0134 | orc_preheated_recuperated_cyclopentane | cycles/organic_rankine | power_cycles/orc_design |
| CSL-0229 | orc_r113_power_to_power_ratio | cycles/organic_rankine | power_cycles/orc_design |
| CSL-0248 | orc_r113_turbine_outlet_temperature | cycles/organic_rankine | power_cycles/orc_design |
| CSL-0252 | orc_double_stage_kirchstockach | cycles/organic_rankine | power_cycles/orc_design |
| CSL-0029 | rankine_cycle_regenerative_extraction | cycles/steam_power | power_cycles/steam_advanced |
| CSL-0143 | rankine_cycle_two_extractions | cycles/steam_power | power_cycles/steam_advanced |
| CSL-0147 | segs_solar_power_plant | cycles/steam_power | power_cycles/steam_advanced |
| CSL-0191 | steam_reheat_power_plant | cycles/steam_power | power_cycles/steam_advanced |
| CSL-0208 | steam_reheat_power_plant_arrays | cycles/steam_power | power_cycles/steam_advanced |
| CSL-0004 | rankine_cycle_60mw | cycles/steam_power | power_cycles/steam_basic |
| CSL-0053 | steam_power_plant_elementary | cycles/steam_power | power_cycles/steam_basic |
| CSL-0140 | rankine_cycle_part_load | cycles/steam_power | power_cycles/steam_basic |
| CSL-0195 | power_plant_cooling_river | cycles/steam_power | power_cycles/steam_basic |
| CSL-0236 | power_plant_river_carnot | cycles/steam_power | power_cycles/steam_basic |
| CSL-0038 | orc_co2_polynomial_maps | cycles/organic_rankine | power_cycles/supercritical_combined |
| CSL-0052 | combined_gas_steam_cycle | cycles/gas_turbines | power_cycles/supercritical_combined |
| CSL-0144 | sco2_recompression_brayton | cycles/gas_turbines | power_cycles/supercritical_combined |
| CSL-0043 | libr_water_absorption_chiller | cycles/absorption_sorption | refrigeration_heat_pumps/absorption |
| CSL-0249 | nh3h2o_absorption_chiller | cycles/absorption_sorption | refrigeration_heat_pumps/absorption |
| CSL-0013 | heat_pump_basic_tespy | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_cycles |
| CSL-0025 | heat_pump_cycle_r22_30kw | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_cycles |
| CSL-0133 | heat_pump_propane_pinch | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_cycles |
| CSL-0171 | r134a_condenser_heat_rejection | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_cycles |
| CSL-0228 | r113_heat_pump_second_law | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_cycles |
| CSL-0246 | heat_pump_room_cop | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_cycles |
| CSL-0033 | heat_pump_r22_semihermetic_compressor | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_systems |
| CSL-0054 | heat_pump_r410a_air_evaporator | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_systems |
| CSL-0068 | heat_pump_scroll_compressor_data_check | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_systems |
| CSL-0078 | brine_to_water_heat_pump_refsim | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_systems |
| CSL-0116 | heat_pump_vitocal_300g | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_systems |
| CSL-0155 | inverter_air_water_heat_pump | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_systems |
| CSL-0324 | zeotropic_hp_propane_isobutane | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/heat_pump_systems |
| CSL-0039 | high_temp_heat_pump_pcm_storage | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/high_temperature |
| CSL-0250 | cascade_heat_pump_geothermal_dh | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/high_temperature |
| CSL-0251 | high_temp_heat_pump_r245fa | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/high_temperature |
| CSL-0253 | high_temp_heat_pump_zeotropic_transcritical | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/high_temperature |
| CSL-0254 | recuperated_brayton_hthp | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/high_temperature |
| CSL-0313 | heat_pump_nh3_two_stage_flooded | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/high_temperature |
| CSL-0001 | refrigeration_cycle_simple_compressor | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_cycles |
| CSL-0015 | refrigeration_cycle_basic_r134a | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_cycles |
| CSL-0148 | scroll_volume_ratio_cycle_r134a | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_cycles |
| CSL-0209 | r134a_water_cooled_condenser | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_cycles |
| CSL-0216 | refrigeration_compressor_r22_r134a | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_cycles |
| CSL-0222 | r22_unloaded_cylinders | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_cycles |
| CSL-0061 | refrigerator_freezer_r134a | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_systems |
| CSL-0077 | aircooled_chiller_refsim | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_systems |
| CSL-0145 | refrigeration_co2_transcritical_booster | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_systems |
| CSL-0212 | reverse_brayton_intercooling | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_systems |
| CSL-0319 | r22_chiller_r407c_heat_pump | cycles/refrigeration_heat_pumps | refrigeration_heat_pumps/refrigeration_systems |
| CSL-0081 | vertical_ghes_refsim | components/heat_exchangers | renewables |
| CSL-0082 | parabolic_trough_receiver_forristal | renewables/solar_thermal | renewables |
| CSL-0083 | parabolic_trough_loss_correlations | renewables/solar_thermal | renewables |
| CSL-0119 | solar_geometry_sun_path | renewables/solar_thermal | renewables |
| CSL-0129 | parabolic_trough_collector_discretised | renewables/solar_thermal | renewables |
| CSL-0160 | pv_module_single_diode | renewables/photovoltaics | renewables |
| CSL-0329 | orc_solar_complex | renewables/solar_thermal | renewables |

## 5. How it was applied

1. Decide on sections 1–3 (edit this file: the JSON block and the table are the plan).
2. `python3 tools/move_model.py --plan docs/taxonomy_v0.3.md --dry-run` — checks that every model ends in a declared category,
   lists the moves and the link rewrites, changes nothing.
3. Same without `--dry-run`: writes `taxonomy.json`, `git mv` of the folders, `previous_paths`, link rewrites, `build_index.py`.
4. Then: `docs/taxonomy.md` §1 (tree, rules of section 1 above, `category_guess` table), the tree of the library `README.md`,
   full `tools/test_models.py` regression, one look at the GUI Library menu with the regenerated `library.json`, the P6.2 log line in
   `roadmap.md`, and the library tag at the next CoolSolve release (P6.3).

## 6. History

- 2026-10-31, C-139 (review at M2, 299 models): first proposal — split rule ~40 → ~20 models, six flat splits under the 8 v0.2 top
  categories, ~15 misfiled models, photovoltaics merged into solar.
- 2026-11-02, C-490/C-491: `tools/move_model.py`, a 110-row CSV plan and the drafted category entries; dry run clean.
- 2026-11-03 (maintainer): one file only; at most 6–7 models per category and no near-empty categories, for browsing in
  `library.html` and in the GUI. The v0.2 top categories `components` and `cycles` (99 and 96 models) are split into
  `heat_exchangers`, `machines`, `components`, `power_cycles`, `engines` and `refrigeration_heat_pumps`; this plan. Applied on a scratch copy of the library: `build_index.py` 0 errors, 259 redirects,
  `test_models.py` 314 targets (277 main files + 37 variants), 0 failure (CoolSolve 0.4.0 build of 2026-11-01).
- 2026-11-03: applied. `move_model.py` moved 259 folders (`git mv`, staged), rewrote 29 links in 12 files, wrote `taxonomy.json`; `build_index.py` 0 errors; `docs/taxonomy.md` §1 and the README tree updated.

# Crossflow heat exchanger — hot gas heating water (effectiveness–NTU)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0026`

A crossflow heat exchanger uses hot gas of constant specific heat to heat
pressurised water. The model applies the classical effectiveness–NTU method
for crossflow arrangement: capacity rates, capacity rate ratio, NTU,
effectiveness, then the gas flow rate, the transferred power, the overall
conductance and the required exchange area through the energy balances. It is
the companion exercise of `CSL-0002` for the crossflow arrangement.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water (CoolProp properties); hot gas with constant c = 1000 J/(kg·K) |
| **Size** | 29 equations (largest block: 4) |
| **Source** | ULiège exercise session (répétition 12, exercise 3) — CoolSolve example `exchangers2` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise, 2005); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the solution stored in the original EES file |

## Problem statement

Hot gas (c = 1000 J/(kg·K)) at 300 °C is used to heat water at 35 °C and
2 bar in a crossflow heat exchanger. The water flow rate is 1 kg/s. The gas
and the water leave the exchanger at 100 °C and 125 °C respectively. The
convective heat transfer coefficient on the gas side is estimated at
100 W/(m²·K). Determine the heat exchanger area. No pressure drops are
assumed.

## Model

Effectiveness–NTU method for a crossflow exchanger:

- capacity rates $\dot C = \dot m c$, with the water specific heat evaluated
  by CoolProp at the mean inlet/outlet temperature and a constant gas c;
- capacity rate ratio $\omega = \dot C_{min}/\dot C_{max}$ (the gas is the
  minimum-capacity fluid);
- $NTU = AU/\dot C_{min}$ with $AU$ the overall conductance;
- crossflow effectiveness (one fluid mixed, as in the original)
  $\varepsilon = 1-\exp\left(\frac{1}{\omega}\,NTU^{0.22}\,
  \left(\exp(-\omega\,NTU^{0.78})-1\right)\right)$;
- transferred power $\dot Q = \varepsilon \dot C_{min} (T_{gaz,su}-T_{w,su})$,
  closed by the energy balance on each side, which fixes the gas flow rate.

Two extra blocks are kept from the original for the record: an alternative
conductance $AU_{bis} = \dot Q/\Delta T_{LM}$ from the logarithmic mean
temperature difference (reference IX.24 of the original), and a wall
calculation (gas/water convection around a wall temperature, overall
coefficient $U$ in series). Both are inconsistent with the NTU sizing (see
*Limitations*); the sizing result is the area $A = 7.38$ m².

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `c_gaz` gas specific heat | 1000 J/(kg·K) | `Q_dot` transferred power | 377.7 kW |
| `T_gaz_su` / `T_gaz_ex` | 300 / 100 °C | `M_dot_gaz` gas flow | 1.888 kg/s |
| `T_w_su` / `T_w_ex` | 35 / 125 °C | `epsilon` effectiveness | 0.755 |
| `P_w` / `M_dot_w` | 2 bar / 1 kg/s | `NTU` / `AU` | 2.024 / 3822 W/K |
| `h_gaz` gas-side coefficient | 100 W/(m²·K) | `A` exchange area | 7.38 m² |
| | | `omega` / `C_dot_min` | 0.450 / 1888 W/K |

## How to run

Open `crossflow_hx_hot_gas_water.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./crossflow_hx_hot_gas_water.eescode
```

The shipped `.initials` (values stored in the original EES file) select the
intended solution: without guess values the solver may converge to a
degenerate root of the wall block (very large area, near-zero overall
coefficient).

## Results

| ε [-] | NTU [-] | ω [-] | Q̇ [kW] | ṁ_gaz [kg/s] | A [m²] |
|---:|---:|---:|---:|---:|---:|
| 0.755 | 2.024 | 0.450 | 377.7 | 1.888 | 7.38 |

The gas, being the minimum-capacity fluid, cools by 200 K (75 % of the
inlet-temperature difference of 265 K, the effectiveness), while the water
heats by 90 K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. A and epsilon vs M_dot_w (Parametric tab) -->

## Verification

Reference: the solution stored in the original EES file `exchangers2.EES`
(EES 9.920, `misc/EES_ok.zip` of the CoolSolve repository), compared with
`tools/compare_solution.py` (tolerances quoted as printed: `rtol=0.001`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `c_w` | 4193.884 J/(kg·K) | 4196.537 J/(kg·K) | 0.063 % |
| `Q_dot` | 377 449.5 W | 377 688.3 W | 0.063 % |
| `M_dot_gaz` | 1.8872 kg/s | 1.8884 kg/s | 0.063 % |
| `NTU` | 2.02387 | 2.02387 | < 0.001 % |
| `AU` / `AU_bis` | 3819.5 / 3712.9 W/K | 3822.0 / 3715.3 W/K | 0.064 % |
| `A` | 7.37757 m² | 7.37756 m² | < 0.001 % |
| `U` | 426.35 W/(m²·K) | 426.62 W/(m²·K) | 0.063 % |
| `T_wall` | −311.62 °C | −311.94 °C | 0.10 % |

28 of 29 variables agree within 0.1 %; `T_wall`, at 1.04e-03 relative, is
marginally above the printed `rtol=0.001` but well within the property
tolerance of CoolSolve `docs/ees_import.md` §11. All deviations trace back
to the difference between the water cp of EES 9.920 and CoolProp at
(2 bar, 80 °C) (0.063 %); `T_wall = T_{gaz,bar} − Q̇/(A·h_{gaz})` amplifies
it by subtraction (0.10 % on −312 °C, i.e. 0.3 K).

## Source and attribution

Original exercise (in French) by **Vincent Lemort** (ULiège Thermodynamics
Laboratory), header `VL050517` — exercise session (*répétition*) 12,
exercise 3, 2005 (the header `VL050517` reads 2005-05-17); the exact course could not be identified from the file.
The model was rewritten in English as the CoolSolve example
`examples/exchangers2.eescode` by S. Quoilin; this library model is the
curated version of that example, which remains in the CoolSolve repository
as a test case.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/exchangers2.eescode`
  (inventory candidate `CSX-017`);
- original EES file with its stored solution:
  `~/git/CoolSolve/misc/EES_ok.zip` → `EES_ok/exchangers2.EES` (EES 9.920).

No matching exercise was found in the ULiège collection inventory
(`sources/thermo_models/inventory.csv` searched for crossflow / gas-water
exchanger titles): only the `CSX-017` row is decided on by this card.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `exchangers2.EES`): unit system already SI-°C-Pa-J (no conversion needed);
  EES licence tag (`Jean Lebrun`, the lab licence, not the author) and `{$PX$}`
  display tag removed; no tables, no external functions (only `cp`, `exp`,
  `ln`, `min`, `max`, all CoolSolve built-ins); full stored solution available
  (29 variables, none cleared).
- **2026-10-05 — example vs original**: the CoolSolve example
  `exchangers2.eescode` transcribes the EES original faithfully — the 22
  equations are identical up to the English translation of the header, the
  section titles and one comment; only the stored-solution rounding differs
  (`exchangers2.initials` holds the EES values to 4 significant digits).
  The library model follows the EES original; nothing had to be reconciled.
- **2026-10-05 — curation**: standard header added, comments translated from
  French to English, SI units added to every dimensional comment. No change
  to any equation or value. The `$UnitSystem` line written by the extractor
  was deleted (library convention: CoolSolve has a single unit system).
  The `{AU=A*U}` line stays commented out, as in the original.
- **2026-10-05 — level**: 29 equations, largest block 4, no functions, arrays
  or calibrated physics → score 0 → level 1.
- **Decision — no diagram state arrays**: the workflow asks for `P[i]`, `h[i]`,
  `T[i]`, `s[i]` arrays on real-fluid models; here the hot fluid has no
  CoolProp properties and the model uses a single water cp call, so a
  thermodynamic-diagram overlay is not meaningful. The figure will be a
  parametric sweep (see placeholder above).

## Limitations and CoolSolve gaps

- The wall-temperature block of the original is kept faithfully but is not
  physical: it gives `T_wall = −311.6 °C` and `h_w = −130.6 W/(m²·K)`
  (negative), hence `U = 426 W/(m²·K)`, larger than `h_gaz = 100 W/(m²·K)`,
  which a series resistance cannot exceed with positive coefficients. These
  values are in the EES stored solution itself, so they are faithfully
  imported, not a CoolSolve artifact; the sizing (NTU → `A = 7.38` m²) is
  unaffected.
- The LMTD check uses a counterflow logarithmic mean difference
  (`AU_bis = 3715 W/K`, 2.8 % below the NTU conductance `AU = 3822 W/K`),
  expected for a crossflow exchanger; the library result is the NTU one.
- Constant gas specific heat and water cp evaluated once at the mean
  temperature.
- CoolSolve prints a `CP(): t=80 looks like Fahrenheit` hint on this model
  (80 °C mean water temperature); the value is in Celsius and the result is
  correct — known heuristic behaviour (`CS-BUG-HINT-FAHRENHEIT`, already
  registered, not blocking).
- No other CoolSolve gaps encountered during the import.

## Related models

- `CSL-0002` *counterflow_hx_oil_water*: same exercise session (répétition 12)
  for the counterflow arrangement (oil cooled by water).
- `CSL-0008` *condenser_three_zones*: three-zone ε-NTU model of an air-cooled
  condenser, each zone with its own effectiveness law.
- `CSL-0027` *shell_and_tube_steam_condenser*: the next exercise of the same
  session (1-2 shell-and-tube steam condenser, ε-NTU rating).
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations
  (Cmin, Cmax, Cr, NTU<->UA, eps and NTU for the counterflow, parallel,
  crossflow and boiler/condenser arrangements) as EES functions, to be copied
  in a model that rates a crossflow exchanger.
- `CSL-0105` *lmtd_and_f_correction*: the LMTD relations (`LMTD`,
  `F_LMTD_Fakheri`, `Ft_aircooler`) as EES functions, the alternative rating
  method of a crossflow exchanger.

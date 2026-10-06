# 1-2 shell-and-tube steam condenser (effectiveness–NTU)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0027`

A 1-2 shell-and-tube condenser (1 shell pass, 2 tube passes) condenses steam
at 50 °C on 30 000 water-cooled tubes. Treated as a semi-isothermal
exchanger, the model applies the effectiveness–NTU method
($\varepsilon = 1-\exp(-NTU)$): water energy balance, capacity rate,
effectiveness, overall conductance, then the water-side heat transfer
coefficient from the Colburn j-factor analogy, the overall coefficient in
series and the tube length from the required exchange area. It is the third
exercise of the same session as `CSL-0002` (counterflow) and `CSL-0026`
(crossflow).

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water (CoolProp properties); condensing steam at imposed temperature |
| **Size** | 35 equations (largest block: 3) |
| **Source** | ULiège exercise session (répétition 12, exercise 4) — CoolSolve example `exchangers3` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise, 2005); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the solution stored in the original EES file |

## Problem statement

The condenser of a steam power plant is a 1-2 shell-and-tube exchanger
(1 shell-side pass, 2 tube-side passes) with 30 000 thin tubes of 25 mm
outer diameter. The steam-side convective coefficient is 11 000 W/(m²·K),
the exchanger duty is 2000 MW, water flows at 1 kg/s per tube and enters
at 20 °C while the steam condenses at 50 °C. Determine the water
temperature rise and the tube length.

## Model

Semi-isothermal exchanger (one fluid condensing at constant temperature):

- water energy balance $\dot Q = N_{tubes}\,\dot m_{1tube}\,c_{p,w}\,(T_{w,ex}-T_{w,su})$,
  with $c_{p,w}$ evaluated by CoolProp at the mean bulk temperature;
- effectiveness $\dot Q = \varepsilon\,\dot Q_{max}$,
  $\dot Q_{max} = N_{tubes}\,\dot m_{1tube}\,c_{p,w}\,(T_{vap}-T_{w,su})$;
- $NTU = AU/\dot C_w$ with $\varepsilon = 1-\exp(-NTU)$;
- water-side coefficient from the Colburn analogy $j = St\,Pr^{2/3}$ with
  $j = 0.023\,Re^{-0.2}$, properties at the mean bulk temperature and 1 bar;
- overall coefficient $U = 1/(1/h_w+1/h_{vap})$ (tube wall neglected,
  $D_{in} = D_{ext}$, as in the original);
- exchange area $A = N_{tubes}\,L_{tube}\,\pi\,D_{ext}$, i.e. the full tube
  length; $L_{tube,bis} = L_{tube}/2$ is one of the two water-side passes.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `D_ext` tube diameter | 0.025 m | `DELTAT_w` water temperature rise | 15.95 K |
| `N_tubes` number of tubes | 30 000 | `T_w_ex` water outlet temperature | 35.95 °C |
| `h_vap` steam-side coefficient | 11 000 W/(m²·K) | `epsilon` effectiveness | 0.532 |
| `Q_dot` duty | 2000 MW | `NTU` / `AU` | 0.758 / 95.1 MW/K |
| `M_dot_1tube` water flow per tube | 1 kg/s | `h_w` water-side coefficient | 6776 W/(m²·K) |
| `T_w_su` / `T_vap` | 20 / 50 °C | `U` overall coefficient | 4193 W/(m²·K) |
| | | `A` exchange area | 22 683 m² |
| | | `L_tube` tube length | 9.63 m |

## How to run

Open `shell_and_tube_steam_condenser.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./shell_and_tube_steam_condenser.eescode
```

No guess file is needed: the model converges from the default guesses
(105 iterations).

## Results

| ε [-] | NTU [-] | ΔT_w [K] | h_w [W/(m²·K)] | U [W/(m²·K)] | A [m²] | L_tube [m] |
|---:|---:|---:|---:|---:|---:|---:|
| 0.532 | 0.758 | 15.95 | 6776 | 4193 | 22 683 | 9.63 |

The 2000 MW duty heats the 30 000 kg/s of cooling water by 15.95 K
(53 % of the 30 K inlet-temperature difference, the effectiveness); each
9.63 m tube carries two 4.81 m water-side passes.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. L_tube and DELTAT_w vs M_dot_1tube (Parametric tab) -->

## Verification

Reference: the solution stored in the original EES file `exchangers3.EES`
(EES 9.920, `misc/EES_ok.zip` of the CoolSolve repository), compared with
`tools/compare_solution.py` (tolerances quoted as printed: `rtol=0.001`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_w_ex` | 35.937 °C | 35.948 °C | 0.03 % |
| `DELTAT_w` | 15.937 K | 15.948 K | 0.07 % |
| `cp_w` | 4183.125 J/(kg·K) | 4180.302 J/(kg·K) | 0.07 % |
| `epsilon` | 0.53123 | 0.53159 | 0.07 % |
| `NTU` | 0.75765 | 0.75842 | 0.10 % |
| `Nu` | 278.88 | 277.14 | 0.62 % |
| `A` / `L_tube` | 22 856.6 m² / 9.7006 m | 22 682.7 m² / 9.6269 m | 0.76 % |
| `U` | 4159.89 W/(m²·K) | 4193.17 W/(m²·K) | 0.79 % |
| `h_w` | 6689.78 W/(m²·K) | 6776.27 W/(m²·K) | 1.28 % |
| `k_w` / `Pr` / `alpha_w` | 0.59970 W/(m·K) / 5.8136 / 1.4390e-07 m²/s | 0.61127 W/(m·K) / 5.6956 / 1.4678e-07 m²/s | 1.9–2.0 % |

24 of 35 variables agree within 0.1 %; all 11 deviations trace back to a
single property difference — the liquid-water thermal conductivity of
EES 9.920 vs CoolProp at (1 bar, 28 °C) (1.9 %, densities, viscosities and
specific heats agreeing within 0.1 %) — propagated through `alpha_w`,
`Pr`, `Nu`, `h_w`, `U` and the sizing (`A`, `L_tube`, 0.76 %). This is
within the property tolerance of CoolSolve `docs/ees_import.md` §11
(up to a few % with an explained cause; same pattern as `CSL-0018`).

## Source and attribution

Original exercise (in French) by **Vincent Lemort** (ULiège Thermodynamics
Laboratory), header `VL050517` — exercise session (*répétition*) 12,
exercise 4 (the header `VL050517` reads 2005-05-17); the exact course could not be identified from the file.
The model was rewritten in English as the CoolSolve example
`examples/exchangers3.eescode` by S. Quoilin; this library model is the
curated version of that example, which remains in the CoolSolve repository
as a test case.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/exchangers3.eescode`
  (inventory candidate `CSX-018`);
- original EES file with its stored solution:
  `~/git/CoolSolve/misc/EES_ok.zip` → `EES_ok/exchangers3.EES` (EES 9.920).

No matching exercise was found in the ULiège collection inventory
(`sources/thermo_models/inventory.csv` searched for shell-and-tube /
steam-condenser titles and values): only the `CSX-018` row is decided on
by this card. The closest candidate, `TM-0410` (R134a condenser into a
water circuit), is a different system (counterflow energy balance, no NTU
rating, different fluids and values) and is left at `todo`.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `exchangers3.EES`): unit system already SI-°C-Pa-J (no conversion needed);
  EES licence tag (`Jean Lebrun`, the lab licence, not the author) and `{$PX$}`
  display tag removed; no tables, no external functions (`conductivity`,
  `cp`, `density`, `exp`, `viscosity` are all CoolSolve built-ins); full
  stored solution available (35 variables, none cleared).
- **2026-10-05 — example vs original**: the CoolSolve example
  `exchangers3.eescode` transcribes the EES original faithfully — the 27
  equations are identical up to the English translation of the header and
  comments (one section title, "longueur d'un tube", was left in French in
  the example and is translated here). The library model follows the EES
  original; nothing had to be reconciled.
- **2026-10-05 — curation**: standard header added, comments translated from
  French to English, SI units added to every dimensional comment (including
  `M_dot_1tube = 1 [kg/s]`, `T_w_su = 20 [C]`). No change to any equation
  or value. The `$UnitSystem` line written by the extractor was deleted
  (library convention: CoolSolve has a single unit system). The
  `{cp_w = 4186}` line stays commented out, as in the original.
- **2026-10-05 — level**: 35 equations, largest block 3, no functions, arrays
  or calibrated physics → score 0 → level 1.
- **Decision — no diagram state arrays**: the workflow asks for `P[i]`, `h[i]`,
  `T[i]`, `s[i]` arrays on real-fluid models; here the steam side is an
  imposed condensation temperature (no steam property call) and the water
  is nearly incompressible, so a thermodynamic-diagram overlay is not
  meaningful. The figure will be a parametric sweep (see placeholder above).

## Limitations and CoolSolve gaps

- Constant steam-side coefficient and constant condensation temperature
  (no steam-side pressure drop or subcooling).
- Tube wall thermal resistance neglected (`D_in = D_ext`); water properties
  evaluated once at the mean bulk temperature and 1 bar.
- No CoolSolve gaps encountered during the import.

## Related models

- `CSL-0096` *plate_hx_heat_transfer*: the plate-heat-exchanger correlations
  (single-phase Nu and flow boiling) a shell-and-tube condenser rating would
  use for its two-phase side, in place of the `h_` functions of `CSL-0089`.
- `CSL-0002` *counterflow_hx_oil_water*: same exercise session (répétition 12)
  for the counterflow arrangement (oil cooled by water).
- `CSL-0026` *crossflow_hx_hot_gas_water*: same exercise session
  (répétition 12, exercise 3) for the crossflow arrangement.
- `CSL-0008` *condenser_three_zones*: three-zone ε-NTU model of an air-cooled
  condenser, each zone with its own effectiveness law.
- `CSL-0089` *condensation_film*: the in-tube film-condensation correlations
  (Boyko-Kruzhilin, Akers-Deans-Crosser, Cavallini-Smith-Zecchin, Shah) that a
  condenser design can use for the condensing-side coefficient.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations
  (Cmin, Cmax, Cr, NTU<->UA, eps and NTU for the counterflow, parallel,
  crossflow and boiler/condenser arrangements) as EES functions, to be copied
  in a model that rates a shell-and-tube condenser.
- `CSL-0097` *two_phase_nonboiling_in_tube*: the two-phase non-boiling
  in-tube heat-transfer coefficients of the `ht` family (Davis-David,
  Groothuis-Hendal, Hughmark, Knott, Aggour, 9 functions), which a condenser
  or evaporator design can use for a tube carrying a condensing mixture.

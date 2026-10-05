# Thermal comfort: Fanger PMV-PPD model

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0012`

Thermal comfort of a person in a room, after the Fanger model (1970) as
taught by J. Lebrun (ULiège, course *Climatisation*, 2006-2007): the full
body heat balance (breathing, skin perspiration, sweat, conduction through
the clothing, radiation to the walls, convection to the air) gives the
thermal load `L_dot`, hence the Predicted Mean Vote `PMV` and the Predicted
Percentage of Dissatisfied `PPD`. The metabolic rate and the clothing
insulation are either given directly or picked from two lookup tables
(7 activities, 6 clothing ensembles).

| | |
|---|---|
| **Category** | Buildings |
| **Fluids** | Humid air (`AirH2O`), water |
| **Size** | native file: 61 equations for 59 unknowns (CoolSolve keeps both `$if` branches); runnable variant: 57 equations (largest block: 7) |
| **Source** | ULiège Thermodynamics Laboratory — thermal comfort model (EES file `thermal_confort_PMV_PPD SQSB080131.EES`) |
| **Authors** | S. Quoilin, J. Lebrun, S. Bertagnolio (ULiège Thermodynamics Laboratory, 2008-01-30) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** by `CS-GAP-IF-DIRECTIVE`, `CS-GAP-LOOKUPROW` (and then `CS-BUG-LOOKUP-STRING`, because its tables have string keys); the variant `thermal_comfort_pmv_ppd_coolsolve.eescode` runs and is verified against the EES stored solution (46/57 within 1e-3, 51/57 within 0.5 %, rest explained) |

## Problem statement

For a person of given mass, height (Dubois skin area), activity and
clothing, placed in air at `T_a` with relative humidity `RH_a` and air
speed `U`, facing walls at the mean radiant temperature `T_w` under
atmospheric pressure `P_a`, compute the heat fluxes the body can dissipate
without thermoregulation (`Q_dot_a`), the residual thermal load
(`L_dot = Q_dot_m − Q_dot_a`), and the comfort indices `PMV` and `PPD`.
Default run: standing person at rest in summer clothing, air at 14 °C,
walls at 20 °C, 50 % RH, still air (PMV ≈ −2.69, PPD ≈ 77 % — too cold).

## Model

- Skin area (Dubois): `A_sk = 0.203·M_i^0.425·H_i^0.725`.
- Metabolic heat `Q_dot_m = E_dot_m` (no external work); `E_dot_m` is either
  given (`E_dot_m_in`) or read from table `activite` (W/m², times `A_sk`).
- Dissipable flux `Q_dot_a`: breathing (CO₂-based ventilation rate,
  `M_dot_CO2 = 1.05E-7·E_dot_m`), skin perspiration (mass-transfer
  coefficient `K_D = 1.3E-9`), sweat (rectified: no negative sweat),
  conduction through clothing (`R_cl = 0.155·I_cl`), grey-body radiation
  (`ε = 0.95`, `F = 0.71`), convection (`max` of natural and forced parts).
- `PMV = C·L_dot/A_sk` with
  `C = 0.303·exp(−0.037·Q_dot_m/A_sk) + 0.0275`; `PPD` is a quartic fit of
  `|PMV|` used by the source model (valid near neutrality; it leaves the
  0–100 % range for large |PMV|).
- Clothing insulation `I_cl` is either given (`I_cl_in`, in clo) or read
  from table `veture` (clo).

| Inputs (default) | Value | Main outputs (default run) | Value |
|---|---|---|---|
| `row` (activity) | 3 (`Repos_debout`, 70 W/m²) | `E_dot_m` metabolic rate | 127.0 W |
| `row2` (clothing) | 2 (`Eté`, 0.5 clo) | `PMV` / `PPD` | −2.691 / 76.97 % |
| `M_i` / `H_i` | 70 kg / 1.7 m | `Q_dot_a` dissipable | 224.2 W |
| `T_a` / `T_w` | 14 / 20 °C | `Q_dot_cl` through clothing | 169.3 W |
| `RH_a` / `U` / `P_a` | 0.5 / 0.05 m/s / 1 bar | `T_cl` clothing temperature | 26.51 °C |

Lookup tables shipped with the model (keys decoded from the source binary).
The native file reads `thermal_comfort_pmv_ppd-activite.csv` / `-veture.csv`, whose first
column holds these keys (ASCII-folded: `Ete`, `Interieur (legere)`, …); the runnable variant
reads `thermal_comfort_pmv_ppd_coolsolve-*.csv`, whose first column is the row number
(see *Conversion log*):

| `activite` (`alpha_E` [W/m²]) | | `veture` (`clo`) | |
|---|---|---|---|
| 1 `Sommeil` | 41 | 1 `Tropicale` | 0.35 |
| 2 `Repos_assis` | 60 | 2 `Eté` | 0.5 |
| 3 `Repos_debout` | 70 | 3 `Intérieur (légère)` | 0.7 |
| 4 `Marche_5km/h` | 160 | 4 `Normale (intérieur hiver)` | 1.0 |
| 5 `Travail_leger` | 120 | 5 `Hiver` | 1.5 |
| 6 `Travail_lourd` | 250 | 6 `Polaire` | 3.5 |
| 7 `Sport` | 350 | | |

## How to run

The original file `thermal_comfort_pmv_ppd.eescode` keeps the native EES
syntax (`$if` string selections `activite$` / `Veture$`, `LOOKUP$ROW`) and
does **not** run in CoolSolve v0.3.0 (see *Limitations and CoolSolve gaps*). The runnable
variant fixes the EES selections of the default run (activity row 3,
clothing row 2 — positional `lookup()`, same column numbering as EES):

```bash
coolsolve ./thermal_comfort_pmv_ppd_coolsolve.eescode    # seconds, needs the *-coolsolve-*.csv tables next to it
```

To study another activity or garment, change `row`/`row2` (keys above);
to give the metabolism or the clothing resistance directly, replace
`E_dot_m = alpha_E_dot*A_sk` by `E_dot_m = E_dot_m_in` (default 100 W) or
`I_cl = lookup('veture',row2,2)` by `I_cl = I_cl_in` (default 1 clo) —
the two `$if` branches of the native file.

## Results

Default run (activity row 3, clothing row 2 — the EES selections):

| Quantity | CoolSolve | EES stored | Agreement |
|---|---:|---:|---|
| `PMV` | −2.6910 | −2.6888 | 0.08 % |
| `PPD` [%] | 76.974 | 77.083 | 0.14 % |
| `C` | 0.0502311 | 0.0502311 | exact |
| `L_dot` [W] | −97.203 | −97.125 | 0.08 % |
| `M_dot_R` [kg/s] | 1.75544e-4 | 1.75552e-4 | 0.005 % |
| `Q_dot_a` [W] | 224.21 | 224.134 | 0.04 % |
| `Q_dot_c` / `Q_dot_R` / `Q_dot_cl` [W] | 117.37 / 51.94 / 169.31 | same | ≤ 0.05 % |
| `T_cl` [°C] | 26.508 | 26.508 | 0.001 % |

Sensitivity of the comfort indices to the air temperature, for three clothing levels (runnable variant,
activity row 3 = 127 W, `T_w` = 20 °C, `RH_a` = 0.5, `U` = 0.05 m/s; clothing = `row2` 2, 4 or 5; PMV / PPD in each cell):

| `T_a` [°C] | 0.5 clo (`row2` = 2) | 1.0 clo (`row2` = 4) | 1.5 clo (`row2` = 5) |
|---|---:|---:|---:|
| 16 | −2.31 / 83.6 % | −1.01 / 26.9 % | −0.32 / 7.1 % |
| 18 | −1.93 / 72.9 % | −0.74 / 16.7 % | −0.11 / 5.3 % |
| 20 | −1.56 / 54.5 % | −0.48 / 9.7 % | +0.10 / 5.2 % |
| 22 | −1.20 / 35.5 % | −0.22 / 6.0 % | +0.31 / 6.9 % |
| 24 | −0.84 / 20.1 % | **+0.03 / 5.0 %** | +0.50 / 10.2 % |
| 26 | −0.50 / 10.2 % | +0.27 / 6.5 % | +0.68 / 14.7 % |

With 1.0 clo the neutral point lies at 24 °C of air temperature (sedentary activity, 20 °C radiant temperature);
thin clothing (0.5 clo) still gives 10 % dissatisfied at 26 °C, thick clothing (1.5 clo) becomes too warm above 20 °C.
(Sweep computed with the CoolSolve variant by changing `T_a` and `row2`, not stored in the EES file.)

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot, e.g. PMV vs air temperature (decision D7: humid-air models get a parametric sweep figure until CS-FEAT-PSYCHRO exists) -->

## Verification

`compare_solution.py` of the runnable variant against the 57 variables
stored in the source EES file (rtol 1e-3): **46/57 agree** (51/57 within
0.5 %); most of them are exact or ≤ 0.05 %: the whole
radiation/convection/clothing cluster, the breathing stoichiometry, `C`,
`L_dot`, `PMV`, `Q_dot_a`. The 11 others are 5 stale cells of a second run
(below) and 6 property-driven deviations ≤ 0.52 % (`h_R_ex`, `h_R_su`,
`w_R_ex`, `H_dot_R`, `PPD`, `PPD[1]`).

- Property-driven deviations (EES 7.9 vs CoolProp formulations):
  humid-air enthalpies and humidity ratio 0.16–0.52 %
  (`h_R_ex`, `h_R_su`, `w_R_ex`, hence `H_dot_R` 0.34 % and `PPD` 0.14 %).
- 5 stored cells belong to a *second* operating point mixed into the EES
  panel and cannot match any single run (proofs): `M_dot_R` violates its
  own equation with the stored companions
  (1.05e-5·28.9669/(0.05·44.01) = 1.3822e-4 ≠ 1.75552e-4 stored);
  `C = 0.0502` requires `Q_dot_m/A_sk = 70.0`, i.e. `Q_dot_m = 127 W`
  ≠ 100 W stored; `Q_dot_a = 224.134` equals the sum of its components
  only with `H_dot_sweat ≈ 9.14 W` ≠ 0 stored. They are leftovers of a
  100 W direct-metabolism run (`E_dot_m`/`Q_dot_m` = 100,
  `M_dot_CO2` = 1.05e-5, `T_sk` = 34.16 °C, `H_dot_sweat` = 0), while the
  rest of the panel — including `PMV`/`PPD` — is the 127 W lookup run
  (`Repos_debout`, row 3) that the variant reproduces. CoolSolve values
  for these 5 cells are the correct solutions of the equations
  (e.g. `M_dot_R` = 1.75544e-4 by direct arithmetic).

## Source and attribution

Thermal comfort model by **S. Quoilin, J. Lebrun and S. Bertagnolio**
(ULiège Thermodynamics Laboratory, 2008-01-30), after Fanger, P.O.,
*Thermal Comfort – Analysis and Applications in Environmental
Engineering* (Danish Technical Press, 1970) and J. Lebrun's course notes
*Climatisation: le confort thermique* (ULiège, 2006-2007). The header of
the source file is a copy-paste of the laboratory boiler template (also
noted in the inventory); the lab disclaimer asks users to cite the origin
(done here). EES licence stamp: J. Lebrun laboratory licence (ULiège).

Source file (EES 7.991, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/Thermal confort PMV-PPD SQSB080131/thermal_confort_PMV_PPD SQSB080131.EES`
(inventory candidate `TM-0326`, representative of duplicate group
`DG-0061`; `TM-0263` is a byte-identical copy in the model bank,
recorded as `duplicate`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve
  repository): unit system already SI-C-Pa-J; EES licence tag removed;
  no parametric table; 57/57 variables with stored values; one embedded
  lookup table `activite` reported as 74×2 (see below). Comments
  translated to English, standard header added, default inputs added
  from the stored values (the source had them commented out, with
  `T_a = 20 °C`; the stored run used `T_a = 14 °C`). The string variables
  `activite$` and `Veture$` of the `$if` directives are never defined in the
  source file: restored as inputs of the native file (default
  `Repos_debout` / `Ete`, the stored run).
- **2026-10-05 — lookup tables reconstructed by hand.** The extractor
  merges the numeric columns of the two adjacent tables into one
  spurious 74-row CSV, drops the string key columns and misparses the
  second column (reported `CS-BUG-EXTRACT-LOOKUP-STRING`): the shipped
  `thermal_comfort_pmv_ppd-activite.csv` (7 rows) and
  `-veture.csv` (6 rows) were decoded from the binary instead —
  `activite`: Sommeil/Repos_assis/Repos_debout/Marche_5km/h/
  Travail_leger/Travail_lourd/Sport → 41/60/70/160/120/250/350 W/m²;
  `veture`: Tropicale/Eté/Intérieur (légère)/Normale (intérieur hiver)/
  Hiver/Polaire → 0.35/0.5/0.7/1.0/1.5/3.5 clo. Column numbering kept
  (values in column 2, as in EES); the first column carries the EES row
  numbers in the variant tables (CoolSolve `lookup()` returns NaN on
  tables with string cells — `CS-BUG-LOOKUP-STRING`); the native file keeps
  string-keyed CSVs (ASCII-folded keys, `activite,alpha_E` and
  `veture,I_cl`) so that it can run unchanged once the gaps are closed.
  The missing-`veture` warning of the extraction report is explained: both
  tables were always in the file.
- **2026-10-05 — runnable variant**
  `thermal_comfort_pmv_ppd_coolsolve.eescode`: the two `$if` blocks
  resolved to the lookup branches with the EES selections (`row = 3`,
  `row2 = 2`; positional `lookup()`, same columns as EES), physics
  unchanged; companion tables and initials duplicated under the
  variant stem (CoolSolve resolves them per file name).
- **Level 2** (score 3: 57 equations in the variant, largest block 7, array
  assignments `PPD[1]`/`PMV_abs[1]`; explicit empirical model, solves
  from default guesses).
- No `$UnitSystem` directive (library convention; already SI-C-Pa-J).

## Limitations and CoolSolve gaps

- The native file is **blocked** by (see CoolSolve
  `docs/model_library_support.md`):
  `CS-GAP-IF-DIRECTIVE` (`$if`/`$else`/`$endif` on string variables is
  parsed but ignored — both branches compile),
  `CS-GAP-LOOKUPROW` (`LOOKUP$ROW('table','col',value)` is unsupported).
- Extraction bugs found on the way: `CS-BUG-EXTRACT-LOOKUP-STRING`
  (string key columns dropped, adjacent tables merged into a spurious
  74×2 CSV), `CS-BUG-LOOKUP-STRING` (every lookup function is NaN on a
  table with a string column — hence numeric-only CSVs for the variant, and
  a third blocker of the native file once the two gaps are closed).
- Physics notes: the source `PPD` quartic is not Fanger's exponential
  law and leaves [0, 100] outside its fit range (e.g. −449 % at
  PMV = −4.29 for the 100 W direct-metabolism branch); the Stefan–
  Boltzmann constant is rounded to 5.7E-8; water saturation properties come
  from CoolProp (IAPWS) rather than the EES 7.9 formulation (the `p_s_sk`
  cells still agree within 0.1 %, with the temperature and formulation
  differences compensating each other on the default run).
- Figure: parametric sweep placeholder (humid-air model, decision D7,
  pending `CS-FEAT-PSYCHRO`).

## Related models

- `CSL-0042` *3R2C building thermal network with weather lookup*: the other
  `buildings/` model, from the same CLIM course; also a blocked native file
  with a verified runnable `_coolsolve` variant.

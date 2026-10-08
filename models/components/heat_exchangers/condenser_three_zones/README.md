# Air-cooled condenser, three-zone parametric model

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0008`

A semi-empirical model of an air-cooled R134a condenser (typical of car
air-conditioning), where the exchanger is cut in three zones —
de-superheating, two-phase condensation, subcooling — each described by an
ε-NTU law. The heat-transfer conductance of each zone is fitted as power laws
of the mass flow rates (`AU = alpha/(R_cf + R_r)` with
`R = C·M_dot^-n`), which makes the model valid in off-design conditions. The
refrigerant supply pressure (hence the condensing temperature) and the
repartition between zones are the implicit unknowns, solved from the thermal
balances. Three flow arrangements are shipped as three files: the main model
(combined crossflow/counterflow) and two variants.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R134a, Air (`Air_ha`, treated as real dry air) |
| **Size** | 124 equations (largest block: 63) + variant files |
| **Source** | C. Cuevas (Universidad de Concepción), 2008, via the ULiège collection — 3 configuration files (duplicate group DG-0060, 6 files) |
| **Authors** | Cristian Cuevas (Universidad de Concepción) |
| **License** | MIT (original: free distribution, cite the origin) |
| **CoolSolve** | v0.3.0 — runs and verified against the EES stored solutions of the three originals (see *Verification*) |

## Problem statement

Predict the performance of a finned-tube air-cooled condenser from the
refrigerant mass flow rate and supply state, the air mass flow rate and
supply temperature, and parameters fitted on one operating point: total
heat rejection, condensing pressure and temperature, zone effectiveness,
air-side pressure drop. Typical use: component model of a refrigeration or
heat-pump cycle model (car A/C condenser, [1][2][3]).

## Model

Three refrigerant zones in series (supply → saturated vapour → saturated
liquid → subcooled outlet), each with:

- conductance `AU = alpha/(C_cf·M_dot_cf^(-n_cf) + C_r·M_dot_r^(-n_r))`
  (alpha = surface fraction of the zone in the series arrangements,
  air-flow fraction in the purely crossflow arrangement);
- ε-NTU relation: counterflow (variants), crossflow both-unmixed
  approximation `ε = 1-exp((exp(-ω·NTU^0.78)-1)/(ω·NTU^0.22))` (main
  model), `ε = 1-exp(-NTU)` for the constant-temperature two-phase zone;
- air- and refrigerant-side pressure drops of the form
  `ΔP = K_1·M_dot²/ρ + K_2·M_dot^(2+n)/(ρ·μ^n)` (all refrigerant-side
  coefficients are 0 in the shipped data).

The three flow arrangements differ only in the air-side connections and the
ε relation (files otherwise identical to the originals):

| File | Arrangement (air side) | Inputs of the original file |
|---|---|---|
| `condenser_three_zones.eescode` | air in series sc → tp → sh, overall counterflow, crossflow ε per single-phase zone | ṁ_r = 0.5 kg/s, ṁ_a = 1.5 kg/s, ΔT_oh = 10 K, ΔT_sc = 8 K |
| `condenser_three_zones_counterflow.eescode` | same series arrangement, counterflow ε | same inputs |
| `condenser_three_zones_crossflow.eescode` | three parallel air streams, one per zone, mixed outlets | ṁ_r = 0.1 kg/s, ṁ_a = 1.6 kg/s, ΔT_oh = 50 K, ΔT_sc = 16 K |

Common inputs: air at 20 °C, 101 325 Pa; R134a. Outputs: `P_r_su_cd`,
`t_r_cd`, zone duties `Q_dot_r_cd_sh/tp/sc`, ε and NTU per zone, alphas,
`DELTAP_cf_cd`. The state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (1 supply,
2 saturated vapour, 3 saturated liquid, 4 subcooled outlet) give the
refrigerant path on the P-h or T-s diagram (CoolSolve *Diagram* tab,
*Overlay array path*).

## How to run

```bash
coolsolve ./condenser_three_zones.eescode
```

**The 63-equation implicit block requires the shipped `.initials` file**
(each variant has its own): without it all solver configurations fail
(see CoolSolve `docs/debugging_models.md`, §*Example: condenser_3zones*).
The shipped guesses are the verified solutions; they were first obtained
from physical estimates derived from the EES stored solution (enthalpy
differences transposed to the CoolProp reference states, t_r_cd estimated
from h_fg). Update them with `coolsolve -g <file>.eescode` after a
successful solve.

## Results

| Configuration | P_r_su [MPa] | t_r_cd [°C] | Q̇_sh [W] | Q̇_tp [W] | Q̇_sc [W] | Q̇_tot [W] | alpha sh/tp/sc [-] |
|---|---:|---:|---:|---:|---:|---:|---|
| combined crossflow/counterflow | 2.105 | 69.8 | 7 295 | 62 383 | 6 892 | 76 569 | 0.298 / 0.654 / 0.049 |
| purely counterflow | 2.096 | 69.6 | 7 276 | 62 537 | 6 881 | 76 694 | 0.279 / 0.673 / 0.048 |
| purely crossflow (other inputs) | 0.949 | 37.4 | 5 249 | 16 569 | 2 308 | 24 126 | 0.086 / 0.620 / 0.294 |

With the same high-load inputs, the three arrangements give similar total
duties (the surface repartition adapts); the crossflow file is solved at the
low-load inputs of its original.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the
     R134a path through the condenser, figures/condenser_three_zones_ph.png -->

## Verification

Each file was solved unchanged (after unit-system curation, see *Conversion
log*) and compared with the solution stored by EES in the corresponding
original file (`compare_solution.py`, reference `ees_variables.csv`):

| Quantity | combined | counterflow | crossflow |
|---|---:|---:|---:|
| zone duties / total duty | ≤ 0.23 % | ≤ 0.13 % | ≤ 0.09 % |
| AU, NTU per zone | ≤ 0.41 % | ≤ 0.48 % | ≤ 0.1 % |
| air pressure drop | 0.87 % | 0.87 % | 0.9 % |

Deviations explained:

- **Enthalpy reference states**: all absolute enthalpies differ by a
  constant offset (R134a +148.15 kJ/kg, air +125.99 kJ/kg) between EES 7.8
  and CoolProp; enthalpy *differences* (the duties) agree within 5·10⁻⁵.
- **Viscosities**: EES `Air_ha`/R134a vapour viscosities differ from
  CoolProp by 1.1–1.7 %, which explains the air pressure drop deviation
  (ΔP ∝ μ^-0.5).
- R134a saturated states agree within 0.02 % (h_fg) → same condensing
  temperatures.

## Source and attribution

Model by **Cristian Cuevas** (Departamento de Ingeniería Mecánica,
Universidad de Concepción, Chile; crcuevas@udec.cl), written 2008-01-08
during a stay at the ULiège Thermodynamics Laboratory (EES licence of
J. Lebrun). The original header asks users to cite the origin and forbids
commercial redistribution; the model is republished here under the library
MIT license as part of the published ULiège collection.

Scientific references:

1. Cuevas C. & Winandy E., 2002. *Simplified 3 zones modelling of a car
   air-conditioning condenser*, IIR Zero Leakage – Minimum Charge
   Conference, Stockholm.
2. Cuevas C., Winandy E. & Lebrun J., 2003. *Modelling of an air condenser
   working in critical zone for engine cooling by refrigeration loop*, VTMS
   6, Brighton.
3. Cuevas C., 2006. *Contribution to the modelling of refrigeration
   systems*, PhD thesis.

Source files (EES X7.793, English, group DG-0060 of six near-duplicates —
three configurations × two copies each; collection of S. Quoilin):

- main: `~/Nextcloud/thermo_models/modeles/Condenser_3_zones/Condenser three zones parametric model model (combined crossflow-counterflow) - CC080108-1.EES` (TM-0266)
- variants: same folder, `…(purely counterflow)…` (TM-0264) and `…(purely crossflow)…` (TM-0265); identical copies in `~/Nextcloud/thermo_models/Model data bank/Heat_Exchangers/Two_Phases_HEX/3_zones_Condenser/` (TM-0258/59/60)

The CoolSolve example `examples/condenser_3zones.eescode` (CSX-008) is the
crossflow configuration converted to SI-C-Pa-J; it stays in the CoolSolve
repository as a test case and is superseded by this native-EES library
model (its `.initials` were used to start the crossflow variant).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): decimal comma converted
  to dot by the tool; unit system of the originals `SI MASS RAD PA C J` —
  no trigonometric function is used anywhere in the model, so the RAD → DEG
  setting has no numerical effect (the `$UnitSystem` line was then removed, as in all library models); pressures,
  temperatures and energies were already Pa / °C / J, no other conversion
  needed. EES licence tag removed. Standard header added, comments kept in
  English, phone/fax/postal address of the original header dropped (kept:
  name, affiliation, e-mail, website, references, disclaimer).
- **2026-10-05 — dead code removed**: `P_cd = pressure(R$,x=0,T=t_cd)` and
  `P_crit = p_crit(R$)` in `two_phase_CD` (combined and counterflow
  originals; assigned, never used). No effect on the results (checked:
  solutions identical).
- **2026-10-05 — curated initials**: the EES stored solutions only cover
  half of the variables (no pressures, alphas, duties), so guesses were
  hand-built from the EES stored enthalpy differences transposed to the
  CoolProp reference states and physical estimates (t_r_cd ≈ 60-70 °C from
  h_fg); the main model then converges in 5 Newton iterations. Variants
  started from the solved main model (counterflow, same inputs) and from
  the CoolSolve example initials (crossflow).
- **2026-10-05 — diagram support**: block of 16 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) added at the end of the
  three files; results unchanged (checked).
- **2026-10-05 — merge of the duplicate group**: TM-0264 (counterflow) and
  TM-0265 (crossflow) kept as variant files; TM-0258/59/60 (second copies
  in the model data bank) not imported; CSX-008 superseded.

## Limitations and CoolSolve gaps

- The air cp in the two-phase zone is evaluated at P = 1 Pa in the
  originals (kept; effect < 0.05 % on the duties — the CoolSolve example
  uses 101 325 Pa, the EES references used 1 Pa).
- `Air_ha` is treated as real dry air by both EES (no humidity data given)
  and CoolSolve; no psychrometric effect.
- All refrigerant-side pressure-drop coefficients are zero in the shipped
  data, so the refrigerant pressure profile is flat; the correlation terms
  stay available for fitted data.
- The effectiveness relation of the single-phase zones changes with the
  arrangement (see *Model*); the fitted parameters C, K, n are only valid
  for one physical condenser.
- No CoolSolve gap found: procedures, string variables and the large block
  (63 equations) all run; convergence just needs the `.initials` file.

## Related models

- `CSL-0112` *three_zone_hx_procedures*: the procedure set of the J. Lebrun
  laboratory files this model descends from (`single_phase_HX` ->
  `single_phase_HX_eps_ntu`, `two_phase_CD` -> `CD_eps_ntu`), with the
  counterflow eps-NTU relation, no pressure drops and the three-zone
  condenser and evaporator of the same family.

- `CSL-0002` *counterflow_hx_oil_water*: single-zone ε-NTU exchanger
  (introductory level).
- `CSL-0014` *hx_constant_pinch*: three-zone condenser (desuperheating,
  condensation, subcooling) closed by an imposed pinch instead of fitted
  conductances.
- See also the CoolSolve example `condenser_3zones.eescode`.
- `CSL-0113` *condenser_3_zones_plate_correlations*: three-zone plate
  condenser sized with plate heat-transfer correlations (Thonon/Kuo) instead
  of fitted epsilon-NTU conductances; water-cooled R123.

- `CSL-0115` *hx_fem_evaporator_discretised*: the same two-phase heat
  exchanger treated fully discretised (N finite-volume cells, cell-by-cell U
  switching smoothed over a quality window) instead of three lumped zones.

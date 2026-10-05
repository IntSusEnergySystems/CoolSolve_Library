# Adiabatic humidifier, simplified model (effectiveness-NTU)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0070`

Simplified model of an adiabatic (evaporative) humidifier from the ULiège
model bank (reference-simulation component model, Laborelec toolkit
lineage): the air leaves close to its wet-bulb temperature, described by a
heat and moisture transfer effectiveness computed from an NTU whose
conductance `AU` follows power laws in the air and water flow rates
(identified on laboratory tests). The model computes the exit air
temperature and humidity, the exit relative humidity and the fraction of
the supplied water that is actually evaporated ("humidifier efficiency").

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (humid air) |
| **Size** | 25 equations, all explicit (largest block: 1): 15 for the model, 10 for the control-panel inputs and parameters |
| **Source** | ULiège model bank — *Simplified model for adiabatic humidification*, 3 January 2008 (EES file inside `Adiabatic_Humidifier_RefSim_Model_NFJL080103.zip`) |
| **Authors** | Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; verified against the EES stored solution (see *Verification*) |

## Problem statement

Air at 25 °C, relative humidity 30 %, flows at 2.2 kg/s through an adiabatic
humidifier at 99 600 Pa; 0.015 kg/s of water is supplied to it. The
humidifier conductance is `AU_n = 1500 W/K` at the nominal flow rates
(2.5 kg/s air, 0.013 kg/s water), with exponents `n = 0.4` (air) and
`m = 0.7` (water). Determine the transfer effectiveness, the exit air state
and the humidifier efficiency.

## Model

- Supply state (*su*): humidity ratio `w_su_hum` from `RH_su_hum`, wet-bulb
  temperature `t_wb_su_hum`, enthalpy `h_a_su_hum` and specific heat
  `cp_a_hum`, all on `AirH2O` at `(t_a_su_hum, P_atm)`.
- Conductance correlation: `AU_hum = AU_hum_n·(M_dot_a_hum/M_dot_a_hum_n)^n_hum·(M_dot_w_su_hum/M_dot_w_su_hum_n)^m_hum`.
- Effectiveness: `epsilon_hum = 1 − exp(−NTU_hum)` with
  `NTU_hum = AU_hum/C_dot_min_hum` and `C_dot_min_hum = C_dot_a_hum =
  M_dot_a_hum·cp_a_hum` (air side, as in the original).
- Exit state (*ex*): `t_a_ex_hum = t_a_su_hum + epsilon_hum·(t_wb_su_hum −
  t_a_su_hum)`; the exit air is saturated at the supply wet-bulb temperature
  (`w_ex_hum = humrat(…, b = t_wb_su_hum)`), giving `RH_ex_hum` and
  `h_a_ex_hum`.
- Water balance: `M_dot_w_ex_hum = M_dot_w_su_hum − M_dot_a_hum·(w_ex_hum −
  w_su_hum)`; humidifier efficiency `eta_hum = (M_dot_w_su_hum −
  M_dot_w_ex_hum)/M_dot_w_su_hum` (as in the original: the ratio of the
  water actually vaporized to the water supplied; not to be confused with
  the transfer effectiveness).

| Inputs (default run) | Value | Parameters | Value |
|---|---|---|---|
| `M_dot_a_hum` air flow | 2.2 kg/s | `AU_hum_n` conductance | 1500 W/K |
| `t_a_su_hum` supply air temperature | 25 °C | `n_hum` / `m_hum` exponents | 0.4 / 0.7 |
| `RH_su_hum` supply relative humidity | 0.3 | `M_dot_a_hum_n` nominal air flow | 2.5 kg/s |
| `P_atm` atmospheric pressure | 99 600 Pa | `M_dot_w_su_hum_n` nominal water flow | 0.013 kg/s |
| `M_dot_w_su_hum` supplied water flow | 0.015 kg/s | | |

In the original the inputs and parameters are entered in the control panel
(Diagram window); the library model gives them their stored (default-run)
values as equations.

## How to run

```bash
coolsolve ./adiabatic_humidifier_simplified.eescode
```

Change the input and parameter values to study other operating points; the
comment block at the end of the file reproduces the characteristic values
identified for two laboratory humidifiers (centrifugal atomizing: `AU_n =
1500`, `n = 0.771`, `m = 0.4718`; wetted wires: `AU_n = 7646`, `n = 0.5`,
`m = 0`).

## Results (default run)

| Quantity | CoolSolve | EES (stored) | rel. diff |
|---|---:|---:|---:|
| `epsilon_hum` transfer effectiveness [-] | 0.50526 | 0.50516 | 1.9e-04 |
| `t_wb_su_hum` supply wet-bulb [°C] | 14.340 | 14.353 | 9e-04 |
| `t_a_ex_hum` exit air temperature [°C] | 19.614 | 19.622 | 4e-04 |
| `w_ex_hum` exit humidity ratio [kg/kg] | 0.0082345 | 0.0082040 | 3.7e-03 |
| `RH_ex_hum` exit relative humidity [-] | 0.56752 | 0.56756 | 7e-05 |
| `eta_hum` humidifier efficiency [-] | 0.32467 | 0.32411 | 1.7e-03 |
| `M_dot_w_ex_hum` exhaust water flow [kg/s] | 0.010130 | 0.010138 | 8e-04 |

About 32 % of the supplied water is evaporated; the air leaves at 56.8 %
relative humidity, 5.3 K above its wet-bulb temperature (effectiveness
0.505).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. epsilon_hum and eta_hum vs M_dot_a_hum (no psychrometric chart in CoolSolve, CS-FEAT-PSYCHRO),
     figures/adiabatic_humidifier_simplified_sweep.png -->

## Verification

Solved with CoolSolve and compared with the EES stored solution
(`compare_solution.py`): **25 common variables, 5 differ above rtol = 0.001,
maximum relative difference 4.42e-03** (`w_su_hum`, the property-call
results: `w_su_hum` 4.4e-03, `w_ex_hum` 3.7e-03, `h_a_su_hum`/`h_a_ex_hum`
1.3e-03, `eta_hum` 1.7e-03). This is within the 0.5 % expected between the
EES and CoolProp humid-air property formulations (CoolSolve
`docs/ees_import.md` §11). Temperatures, pressures, flow rates,
effectiveness and NTU agree to ≤ 9.4e-04.

Nine variables stored in the EES file are not part of the comparison:
`M_dot_a, R, cp, su, AU_n, M_dot_a_n, M_dot_w_n, n, m` — control-panel
display variables that no equation of the file uses (values of the
identified-parameter examples).

Five of the 25 reference values (`t_a_su_hum, t_wb_su_hum, t_a_ex_hum,
RH_ex_hum, M_dot_w_ex_hum`) were recovered by hand-decoding the binary
variable records that `tools/ees_extract.py` skips (bug
`CS-BUG-EXTRACT-FMT`); they were cross-checked against the equations (the
hand-decoded `t_a_ex_hum`, `RH_ex_hum` and `M_dot_w_ex_hum` re-derive from
the stored `epsilon_hum`, `t_wb_su_hum` and flow rates exactly).

## Source and attribution

ULiège model bank (Laborelec toolkit lineage), *Simplified model for
adiabatic humidification*, dated 3 January 2008, author **Jean Lebrun**
(header and EES licence tag). The zip also carries the laboratory
disclaimer (freely distributed, may not be sold, cite origin) and the
companion file is listed as an IEA ECBCS Annexe 43 PR2 A10 reference model
(see `IEA A43 PR2 A10 Reference humidifier EES model NFJL PhAJL080108.pdf`
in the same folder).

Source file (EES 7.793), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Humidifiers/Adiabatic_Humidifier_RefSim_Model_NFJL080103.zip!/Adiabatic_Humidifier_SimRef_EES_Model_NFJL080103.EES`
(inventory candidate `TM-0475`). The zip also contains a compiled `.EXE`
version of the model (not imported). No sibling ParamID file of this
component is in the collection.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): unit system already
  SI-°C-Pa-J; no lookup or parametric table; licence tag removed; comments
  translated (typos of the original corrected); standard header added.
  Inputs and parameters (control panel of the original) given their stored
  values as equations — the stored values are the file's default operating
  point and are kept as the regression case. The equations of the original
  are unchanged.
- **Stored run vs identified values.** The stored run used `n_hum = 0.4`,
  `m_hum = 0.7`, while the comment block lists the identified values
  `n = 0.771`, `m = 0.4718` for the centrifugal atomizing humidifier
  (`AU_n = 1500`, `M_dot_a_n = 2.5`, `M_dot_w_n = 0.013` agree). The stored
  operating point is kept (decision: the regression case is the file's last
  run); edit `n_hum`, `m_hum` to reproduce the identified parameters.
- **Unit annotation.** The original stores `AU_hum`, `AU_hum_n` with the
  unit `W/(K*m^2)`; `NTU_hum = AU_hum/C_dot_min_hum` requires W/K, which is
  used here.
- **Level.** Score (taxonomy.md §3): equations 25 (< 50 → 0), largest block
  1 (≤ 5 → 0), no functions/arrays (0), single component (0), identified
  `AU` correlation (semi-empirical: 1), no curated guesses (0) → 1 →
  **level 1** (card value confirmed).
- **Extraction issue** (bug `CS-BUG-EXTRACT-FMT`, reported in the CoolSolve
  register): `ees_extract.py` skipped 5 of the file's variable records
  because their format byte differs from the expected value; the records
  were decoded by hand with the documented layout and cross-checked (see
  *Verification*).

## Limitations

- Simplified model: the exit air is assumed saturated at the supply
  wet-bulb temperature; no carry-over of unevaporated droplets is modelled
  (the exhaust water flow is a balance residual).
- The effectiveness-NTU form with `C_dot_min` = air side is kept as in the
  original; `AU` is correlated with the air **and** water flow rates.
- The control-panel outputs of the original list `W_a_ex_hum`, which no
  equation of the file defines (only `w_ex_hum` is computed).

## Related models

- `CSL-0066` *adiabatic_saturation_wet_bulb*: the same adiabatic-saturation
  physics (constant wet-bulb temperature) from the psychrometrics side,
  with the thermodynamic wet-bulb vs wet-bulb comparison.
- `CSL-0016` *moist_air_cooling_coil_contact_factor*: the same
  effectiveness-type closure (contact factor) for the opposite process
  (cooling and dehumidifying coil) in air handling.
- `CSL-0028` *air_handling_unit_moist_air*: full air handling unit on
  `AirH2O`.

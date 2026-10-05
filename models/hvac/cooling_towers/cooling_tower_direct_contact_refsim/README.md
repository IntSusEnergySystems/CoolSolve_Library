# Direct-contact cooling tower, reference simulation model

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0076`

Reference simulation model of an open (direct-contact) cooling tower of the
ULiège model bank: the tower is a counter-flow heat exchanger between the
cooling water and the ambient air, the air leaving the tower saturated. The air
side is described by a *fictitious fluid* whose enthalpy is set by the wet-bulb
temperature (the theory of the wet cooling coil), and the dry heat transfer
coefficient, the air-side pressure drop and the fan over-pressure are all
referred to the nominal conditions of the tower, so that the water flow rate,
the air flow rate and the fan speed can be changed independently.

| | |
|---|---|
| **Category** | HVAC › Cooling towers |
| **Fluids** | AirH2O (humid air), water (constant `c_w` = 4187 J/kg·K, `v_w` = 0.001 m³/kg) |
| **Size** | 54 equations, largest block: 12 (the counter-flow exchanger loop) |
| **Source** | ULiège model bank (Laborelec toolkit lineage), direct contact cooling tower reference simulation model, 4 January 2008 (`CoolingTower_RefSim_EES_model_CASJL080104.EES`, EES 7.793); IEA A43 PR2 A16 reference cooling tower model |
| **Authors** | Cleide Da Silva, Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

A counter-flow cooling tower with a nominal dry heat transfer coefficient
AU_dry,n = 10 000 W/K, nominal air and water flow rates of 8.5 and 12 kg/s, a
nominal air-side pressure drop of 400 Pa produced by the fan at 2000 min⁻¹, a
constant water fall speed of 0.5 m/s and a fan efficiency of 0.65 cools
13 kg/s of water entering at 35 °C with ambient air at 25.13 °C, 50 % relative
humidity and 101 325 Pa. Determine the outlet water temperature, the range and
approach, the cooling power, the electrical power of the fan, the water
consumption, and the air flow rate the tower draws.

The air flow rate is not an input: the air velocity needed in the free area to
produce the fan over-pressure fixes it through the geometry of the tower
(the free area is what is left of the total area once the falling water is
accounted for).

## Model

- **Air side energy balance** (the exhaust air is saturated):
  `Q_dot_ct = M_dot_a_ct·(h_a_ex_ct − h_a_su_ct)`, with the exhaust state
  `(P_atm, h_a_ex_ct, R=1)`; the same power is written on the fictitious
  capacity flow rate, `C_dot_af_ct = M_dot_a_ct·c_p_af_ct`, whose specific heat
  `c_p_af_ct` is defined by the fictitious fluid,
  `c_p_af_ct = (h_a_ex_ct − h_a_su_ct)/(t_wb_ex_ct − t_wb_su_ct)`, and
  `t_wb_ex_ct = t_a_ex_ct`.
- **Water side energy balance**: `Q_dot_ct = C_dot_w_ct·(t_w_su_ct − t_w_ex_ct)`
  with `C_dot_w_ct = M_dot_w_ct·c_w`.
- **Effectiveness** (counter-flow, fictitious capacity flow rates on both
  sides): `Q_dot_ct = epsilon_f_ct·C_dot_min_f_ct·(t_w_su_ct − t_wb_su_ct)`,
  `C_dot_min/max = min/max(C_dot_w_ct, C_dot_af_ct)`,
  `NTU_f_ct = AU_f_ct/C_dot_min_f_ct`, `omega_f_ct = C_dot_min_f_ct/C_dot_max_f_ct`.
- **Merckel**: `AU_f_ct = AU_dry_ct·c_p_af_ct/c_p_a_ct`; the dry coefficient
  follows both flow rates with respect to the nominal conditions:
  `AU_dry_ct = AU_dry_n_ct·(M_dot_w_ct/M_dot_w_n_ct)^m_ct·(M_dot_a_ct/M_dot_a_n_ct)^n_ct`.
- **Air-side pressure drop and free area**: `DELTAp_ct = C_a_ct²/(2·v_a_ct)`,
  `C_a_ct = M_dot_a_ct·v_a_ct/A_a_ct`, `A_a_ct = A_a_0_ct − A_w_ct`,
  `A_w_ct = M_dot_w_ct·v_w/C_w_ct`; the same relations at the nominal point
  (`v_a_n_ct` = 0.83 m³/kg, `DELTAp_n_ct` = 400 Pa) fix the total free area
  `A_a_0_ct`, and the fan characteristic
  `DELTAp_ct = DELTAp_n_ct·(rpm_FAN_ct/rpm_FAN_n_ct)²` fixes the pressure drop
  of the current operating point, hence the air velocity and the air flow rate.
- **Fan power** `W_dot_FAN_ct = V_dot_a_ct·DELTAp_ct/eta_FAN_ct`, **water
  consumption** `M_dot_w_ct_consumed = M_dot_a_ct·(W_ex_ct − W_su_ct)/eta_ct`,
  and the reference variables `range = t_w_su_ct − t_w_ex_ct`,
  `approach = t_w_ex_ct − t_wb_su_ct`.

| Inputs | Value | Parameters | Value |
|---|---|---|---|
| `M_dot_w_ct` water flow | 13 kg/s | `AU_dry_n_ct` | 10 000 W/K |
| `t_w_su_ct` water supply | 35 °C | `C_w_ct` water fall speed | 0.5 m/s |
| `t_a_su_ct` air supply | 25.13 °C | `DELTAp_n_ct` | 400 Pa |
| `RH_su_ct` air supply humidity | 0.5 | `eta_ct` / `eta_FAN_ct` | 0.95 / 0.65 |
| `P_atm` | 101 325 Pa | `m_ct` / `n_ct` | 0.1 / 0.6 |
| `rpm_FAN_ct` fan speed | 2000 min⁻¹ | `M_dot_a_n_ct` / `M_dot_w_n_ct` | 8.5 / 12 kg/s |

## How to run

Open `cooling_tower_direct_contact_refsim.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./cooling_tower_direct_contact_refsim.eescode
```

The shipped `.initials` holds the solution stored by EES for this operating
point; without it the air-side geometry block is singular (CoolSolve guesses 1
for the areas and the air velocity), see *Limitations*.

## Results

Default operating point (13 kg/s of water from 35 °C, air 25.13 °C / 50 % RH):

| Variable | Value | | Variable | Value |
|---|---:|---|---|---:|
| `t_w_ex_ct` outlet water | 28.90 °C | | `M_dot_a_ct` air flow rate | 8.298 kg/s |
| `range` | 6.10 K | | `V_dot_a_ct` air volume flow | 7.12 m³/s |
| `approach` | 10.91 K | | `C_a_ct` air velocity (free area) | 26.20 m/s |
| `Q_dot_ct` cooling power | 332.1 kW | | `A_a_0_ct` total free area | 0.2978 m² |
| `W_dot_FAN_ct` fan power | 4.383 kW | | `DELTAp_ct` | 400 Pa |
| `M_dot_w_ct_consumed` | 0.1264 kg/s | | `AU_dry_ct` / `AU_f_ct` | 9936 / 38 121 W/K |
| `t_a_ex_ct` exhaust air | 28.17 °C (saturated) | | `NTU_f_ct` / `epsilon_f_ct` | 1.168 / 0.598 |

The water leaves 6.10 K below its inlet temperature and 10.91 K above the
supply wet-bulb temperature (18.0 °C); the exhaust air is saturated at
28.17 °C, as the model assumes. The evaporation rate (0.126 kg/s) is 0.97 % of
the water flow rate, the usual order of magnitude for a direct-contact tower.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the figure is a
     parametric sweep (e.g. Q_dot_ct and approach vs the water flow rate) — the
     model runs on humid air, for which CoolSolve has no diagram yet
     (CS-FEAT-PSYCHRO), so there is no state-point array to overlay -->

## Verification

The equations were transcribed from the equations window of the source file (see
*Conversion log*) and solved as they stand — the extraction is **square** as it
stands (`coolsolve -d`: *System square: Yes*, 54 equations, 54 variables) and no
equation of the file was replaced by a stored value; the result was compared with
the solution stored by EES in the source file
(`compare_solution.py cooling_tower_direct_contact_refsim.sol reference/ees_variables.csv`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Q_dot_ct` [W] | 331 163 | 332 128 | 2.90e-03 |
| `W_dot_FAN_ct` [W] | 4383.17 | 4382.60 | 1.3e-04 |
| `M_dot_w_ct_consumed` [kg/s] | 0.125850 | 0.126395 | 4.31e-03 |
| `t_w_ex_ct` [°C] | 28.9159 | 28.8982 | 6.1e-04 |
| `M_dot_a_ct` [kg/s] | 8.29671 | 8.29778 | 1.3e-04 |
| `C_a_ct` [m/s] | 26.2067 | 26.2034 | 1.3e-04 |
| `A_a_0_ct` [m²] | 0.2977872 | 0.2977871 | 3.8e-07 |
| `NTU_f_ct` | 1.16797 | 1.16802 | 4.0e-05 |
| `h_a_su_ct` [J/kg] | 50 666.3 | 50 756.4 | 1.78e-03 |
| `W_su_ct` [kg/kg] | 0.00995912 | 0.0100042 | 4.51e-03 |

**54 common variables, 13 above rtol = 0.001, maximum relative difference
4.51e-03** (`W_su_ct`). Every difference is a humid-air property: the humidity
ratio and the enthalpy of the supply and exhaust air are computed by the ASHRAE
formulation of EES 7.793 and by CoolProp, which differ by 0.18–0.45 % at these
states (the same deviations as in `CSL-0016`, `CSL-0070` and `CSL-0074`). The
41 algebraic results of the model (flow rates, areas, air velocity, pressure
drop, NTU, effectiveness, powers, consumption) agree to better than 1e-3, 23 of
them exactly (bit-identical). No variable was excluded from the comparison.

Ten decoded EES variables are not variables of the model: `Q_dot_n_ct`,
`M_dot_a_n_ct_default`, `M_dot_w_n_ct_default` and `AU_dry_n_ct_default` (the
ASHRAE primary toolkit relations that size the nominal conditions from a nominal
cooling power; display strings in the source, quoted in the comment block of
section 6), `a_ct`, `b_ct`, `c_ct`, `d_ct` (executable lines of the source that
feed no equation, removed as dead code) and `m`, `E`, two records that EES does
not list among its own *Variables in Main*.

## Source and attribution

Reference simulation model by **Cleide Da Silva** and **Jean Lebrun** (ULiège
Thermodynamics Laboratory), part of the ULiège model bank (Laborelec toolkit
lineage), dated 4 January 2008 in the file header
(`"Authors: Cleide Da Silva, J. Lebrun"`; the `{$ID$…}` tag names the EES
licence of J. Lebrun's laboratory). The same folder ships the printed
documentation of the model, *"IEA A43 PR2 A16 Reference cooling tower EES model
CASJL PhAJL080108.pdf"*.

Source file (EES 7.793, English), collection of S. Quoilin, **inside a zip
archive that is not extracted by the collection**:
`~/Nextcloud/thermo_models/Model data bank/Heat_and_Cool_Production_Systems/Cooling_Towers/CoolingTower_RefSim_model_CASJL080104.zip!/CoolingTower_RefSim_EES_model_CASJL080104.EES`
(inventory candidate `TM-0489`).

The archive also holds an EXE version of the model (`…RefSim_EXE_model….EXE`),
not imported. **No ParamID (parameter-identification) or simplified version of
the cooling tower exists in the model bank** — the three `RefSim`/`ParamID`/
simplified triples of the bank concern the cooling coil, the adiabatic
humidifier and the centrifugal pump, not the cooling tower — so nothing was
merged into or split from this model. The Laborelec 2002 direct-contact tower
files of the collection (`TM-0292` experimental, `TM-0293` identification,
`TM-0294` simulation, kPa/kJ unit system, Merkel model without the air-side
pressure-drop and fan relations) are a different, earlier model and were left
for their own triage.

## Conversion log

- **2026-10-05 — extraction** (`CoolSolve/tools/ees_extract.py`): EES 7.793, unit
  system already `SI MASS DEG PA C J` (no conversion needed, no
  `$UnitSystem` directive in the library file), no lookup and no parametric
  table, licence tag removed, 64 variable records decoded. The report lists the
  functions `enthalpy`, `exp`, `humrat`, `max`, `min`, `specheat`, `temperature`,
  `volume`, `wetbulb`, all built into CoolSolve.
- **2026-10-05 — the raw extraction cannot be parsed by CoolSolve
  (`CS-BUG-MULTILINE-COMMENT-START`).** `ees_extract.py` does return the
  equations (they are in the equations window, alternating with the display
  strings), but the file it writes uses display strings whose opening `"` is
  the **last character of a line** (the text starts on the next line, e.g.
  `"` ⏎ `Water side energy balance:"`). CoolSolve then warns *"The comment
  opened by a '"' at line N is never closed: everything after it is ignored"*
  and fails with *"Could not parse line"*. The form is valid EES — the source
  file is a working model of the model bank (EES stores the full solution of its
  56 variables) and the print-out of its equations window shipped with the model
  (the PDF named above) shows the same text. The library file therefore keeps
  **one comment string per line**, which is the same text with the quotes moved.
- **2026-10-05 — transcription of the equations** from the extracted equations
  window, variable by variable, with the following points:
  - the 6 inputs and the 10 parameters are **not** equations of the file: the
    window says *"The 6 outputs, 6 inputs and 10 parameters are given in the
    control panel"* and the parameters block is itself inside a display string.
    They are written as input assignments in the `.eescode` file with the values
    of the control panel (i.e. the values EES stored for this operating point);
  - the window gives the air-side balance twice, as alternatives ("or"):
    `Q_dot_ct = M_dot_a_ct*(h_a_ex_ct − h_a_su_ct)` **or**
    `Q_dot_ct = C_dot_af_ct*(t_wb_ex_ct − t_wb_su_ct)`. Only the first is kept as
    an equation and the fictitious specific heat gets the closing relation the
    window implies,
    `c_p_af_ct = (h_a_ex_ct − h_a_su_ct)/(t_wb_ex_ct − t_wb_su_ct)`, which
    reproduces the stored value exactly (3922.23 J/kg·K =
    (90581.3 − 50666.3)/(28.1736 − 17.9970)) and leaves the system square;
  - `a_ct = 27.5E-3`, `b_ct = 2.6`, `c_ct = 70E-3`, `d_ct = -61E3` are
    executable lines of the file, but they feed no other equation (the relations
    that use them, `M_dot_a_n_ct_default = a_ct*Q_dot_n_ct + b_ct` and the two
    other default relations, are display strings): kept as dead code in the
    comment block of section 6 instead of as four equations with no user;
  - nothing else was changed: the remaining equations are the ones of the file,
    with the same variables, functions and constants.
- **2026-10-05 — curation**: standard header, comments in English (paraphrasing
  the comments of the original), the six inputs and the ten parameters of the
  control panel of the original written as input assignments, the outputs listed
  as they are in the original, `c_w`, `v_w` and `v_a_n_ct` as constants. No
  equation was added, removed or re-arranged; no variable was renamed. The system
  is square as it stands (`coolsolve -d`: *System square: Yes*, 54 equations,
  54 variables, largest block 12).
- **2026-10-05 — `.initials`**: the stored EES solution, curated to the 54
  variables of the model (the ten variables listed in *Verification* are
  dropped). Needed: without guesses the 12-variable air-side block is singular
  (`SingularJacobian`), since CoolSolve guesses 1 for the areas and the air
  velocity.
- **Level**: score 4 with [taxonomy.md §3](../docs/taxonomy.md) (54 equations → 1,
  largest block 12 → 1, no function/procedure/array → 0, single zone → 0,
  semi-empirical calibration → 1, curated guesses needed → 1) = level 3 by the
  table; lowered by one to **level 2** because the model is a single-zone
  component with one small implicit loop and no off-design or multi-zone
  treatment — the same profile as `CSL-0074`, also rated level 2.

## Limitations and CoolSolve gaps

- The model needs the shipped `.initials` (see above); without them the air-side
  geometry block is singular. The model is not *blocked*: it solves in 17
  iterations.
- The exhaust air is assumed saturated (`R = 1` at the exhaust), so the model
  cannot describe a tower whose exhaust air is not wetted out.
- The tower is described by a single zone: no axial variation of the water flow
  rate (constant `M_dot_w_ct` along the tower), and no dependence of the heat
  transfer coefficient on the local water-to-air temperature ratio.
- The humid-air differences against EES (up to 0.45 %, see *Verification*) are
  property-backend differences, not modelling differences.
- Variable bounds are not supported by CoolSolve (`CS-GAP-BOUNDS`): EES bounded
  `epsilon_f_ct` to [0, 1], `omega_f_ct` to [0, 0.999] and `RH_su_ct` to
  [0, 1.01]; the equations keep the results in range by themselves.

## Related models

- `CSL-0074` *cooling_coil_refsim*: same model bank and same theory (fictitious
  fluid defined by the wet-bulb temperature, dry and wet regimes) for a cooling
  coil.
- `CSL-0030` *two_speed_cooling_tower*: same category; cooling tower with a
  nominal and a half-speed fan regime, two equations blocks with an index.
- `CSL-0065` *cooling_tower_condenser_water*: same category; cooling tower
  sized from a power-plant condenser duty.- `CSL-0077` *aircooled_chiller_refsim*: another model of the same ULiège
  model bank (IEA A43 PR2 A15), the air-cooled condenser air side of a water
  chiller.

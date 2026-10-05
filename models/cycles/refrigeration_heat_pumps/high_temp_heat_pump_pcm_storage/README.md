# High-temperature heat pump with PCM storage (Zorlu geothermal plant case study)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0039`

High-temperature vapour-compression heat pump (cyclopentane) in a case study for
the Zorlu geothermal plant: a geothermal brine (water, 113 °C supply, pumped
over 0.5 bar) evaporates the working fluid, an internal heat exchanger
(recuperator) transfers heat from the condenser outlet to the compressor
suction, and the condenser delivers heat to a water loop that charges a
phase-change-material (PCM) storage. The evaporating and condensing pressures
are not imposed: they follow from pinch constraints (10 K at the condenser,
3 K at the evaporator) evaluated zone by zone — superheat, two-phase and
subcooling zones selected by nested IF-THEN-ELSE in two PROCEDUREs.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | CycloPentane (working fluid), Water (brine and heat distribution) |
| **Size** | 151 equations, largest block: 63 (126 for the model, 1 energy-balance check, 24 for the diagram state points) |
| **Source** | CoolSolve example `zorlu_heat_pump.eescode` (CSX-047), after an untranslated EES model of the Zorlu plant; no EES original is available |
| **Authors** | TBD (author of the original EES model, not identified); S. Quoilin (CoolSolve translation) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs (with the shipped `.initials`); no independent reference available, see *Verification* |

## Problem statement

The plant requirements are a condenser duty of 7 MW and a 2 MW ORC expander
(the ORC itself is not modelled here). The heat pump lifts the geothermal
brine from 113 °C to a 141 °C water loop; the PCM storage is charged at
`T_PCM` = 141 °C for 4 h and discharged for 2 h, with 5 % losses. Determine
the cycle pressures that satisfy the pinch constraints, the compressor power
and the COP, and the PCM storage volume and discharge power.

## Model

- **Evaporator**: brine cooled from `T_sf_su_ev` ≈ 113.11 °C to ≈ 110.28 °C;
  refrigerant evaporates at `p_su_ev` ≈ 4.932 bar (T<sub>sat</sub> 107.28 °C)
  and leaves superheated by `DELTAT_sh` = 1 K. The pinch is evaluated per zone
  by `q_dot_pinch_fun_ev` (here the superheat and two-phase zones are active).
- **Internal heat exchanger**: effectiveness `epsilon_ihx_hp` = 0.8 applied to
  the smaller of the two maximum heat rates.
- **Compressor**: isentropic efficiency `epsilon_s_cp` = 0.8, suction at the
  recuperator cold outlet, discharge at `p_su_cd` ≈ 12.59 bar (T ≈ 180 °C).
- **Condenser**: desuperheating, condensation at 154 °C, subcooling by
  `DELTAT_sc` = 3 K; the water side heats from 141 °C to ≈ 141.34 °C at
  10 000 kg/s. The pinch is evaluated per zone by `q_dot_pinch_fun_cd`
  (all three zones active).
- **Brine production pump**: `eta_is_sf_pp` = 0.7, pressure lift 0.5 bar,
  58 % of the available flow (497.6 kg/s), power included in the COP.
- **PCM sizing**: `Q_PCM = Q_dot_cd_HP`, `E_PCM = Q_PCM·t_charge`, 5 % losses,
  `Vol_PCM = E_PCM/E_density_PCM`, discharge power `E_PCM_f/t_discharge`.
  `t_charge` = 4 and `t_discharge` = 2 are **hours in the original** (the
  example feeds the bare values into the SI equations, so the storage results
  carry the original time convention: `E_PCM` = 2.8·10⁷ reads J but is
  2.8·10⁷ W·h = 28 MWh, `Vol_PCM` = 311 m³ for `E_density_PCM` = 9·10⁴ J·h/m³
  ≡ 90 kWh/m³). The heat-pump results are unaffected.

| Inputs | Value | Outputs | Value |
|---|---:|---|---:|
| `Q_dot_cd_HP` condenser duty | 7 MW | `Q_dot_cd` condenser duty (pinch zones) | 7.010 MW |
| `epsilon_s_cp` compressor isentropic eff. | 0.8 | `W_dot_cp` compressor power | 1.055 MW |
| `epsilon_ihx_hp` recuperator effectiveness | 0.8 | `W_dot_sf_pp` brine pump power | 37.5 kW |
| `DELTAT_pp_cd` / `DELTAT_pp_ev` | 10 / 3 K | `COP_HP` (pump power included) | 6.417 |
| `m_dot` refrigerant flow | 19.99 kg/s | `p_su_ev` / `p_su_cd` | 4.93 / 12.59 bar |
| `m_dot_sf_su_ev` brine flow | 497.6 kg/s | `T_out_cp` compressor outlet | 180.0 °C |
| `m_dot_sf_su_cd` water flow | 10 000 kg/s | `T_sf_ex_cd` water outlet | 141.3 °C |
| `t_charge` / `t_discharge` | 4 / 2 h | `Vol_PCM` storage volume | 311 m³ |
| `E_density_PCM` storage density | 90 kWh/m³ | `Q_dis_PCM` discharge power | 13.3 MW |
| `PCM_cap` capacity requirement | 29 MWh | `Q_dot_rec` recuperator duty | 1.223 MW |

## How to run

Open `high_temp_heat_pump_pcm_storage.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./high_temp_heat_pump_pcm_storage.eescode
```

The shipped `.initials` (converged solution of the pinch formulation) is
required: the CoolSolve solver-robustness report shows that most solver
configurations fail without it, because the pinch procedures make the
63-variable block strongly conditional. No `coolsolve.conf` is needed.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 evaporator outlet, 2
compressor suction, 3 condenser inlet, 4 condenser outlet, 5 valve inlet,
6 evaporator inlet) give the cycle on the P-h or T-s diagram (CoolSolve
*Diagram* tab, *Overlay array path*, *Close loop*; with zero pressure drops
points 1–2 and 3–5 merge on the diagram).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cyclopentane cycle,
     figures/high_temp_heat_pump_pcm_storage_ph.png -->

## Verification

No independent reference exists: the model is a translation of an EES file
that is not available (not in CoolSolve `misc/EES_ok.zip`, and the ULiège
collection has no Zorlu/PCM exercise — searched `zorlu`, `PCM`,
`cyclopentane`; see *Source and attribution*). The verification therefore
reproduces the converged solution distributed with the CoolSolve example
(`zorlu_heat_pump.initials`):

> `114 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
> CoolSolve: 37` — the 37 extra variables are the state-point arrays
> `P[i]`/`h[i]`/`T[i]`/`s[i]`, the balance check and the string variables of
> the library model.
> With `--rtol 1e-12` the largest relative deviation is **1.85e-10** on
> `W_dot_sf_pp` (round-off of the stored values).

Sanity checks: cycle energy balance `balance` = 0 W (to machine precision) on
7.010 MW; both pinch constraints are active (`DT_min_cd` = 10 K,
`DT_min_ev` = 3 K); `Q_dot_sc_ev` ≈ 0 (the evaporator has no subcooling zone,
as expected for a valve inlet in the two-phase region).

Status is `runs` (no independent reference), not `verified`.

## Source and attribution

The CoolSolve example `zorlu_heat_pump.eescode` (CSX-047) states that it is
"translated from EES"; neither the example, the CoolSolve repository
(`misc/EES_ok.zip`, searched in full) nor the ULiège collection
(`~/Nextcloud/thermo_models`, searched for `zorlu`, `PCM`, `cyclopentane`)
contains that original. The author of the original EES model is unknown
(`TBD`); the CoolSolve translation is by S. Quoilin.

Source file: `~/git/CoolSolve/examples/zorlu_heat_pump.eescode` with its
`zorlu_heat_pump.initials` (the example stays in the CoolSolve repository as
a test case; inventory candidate `CSX-047`). No `thermo_models` row describes
the same exercise, so no cross-source triage was needed.

## Conversion log

- **2026-10-05 — import** (from the CoolSolve example): the example was
  already in SI-°C-Pa-J; the equations were kept unchanged. The example's
  "translated from EES" banner and its solver note were replaced by the
  standard library header; units were added to the comments; the PCM time
  convention (`t_charge`/`t_discharge` in hours) is documented in *Model*
  instead of being silently assumed in seconds.
- **2026-10-05 — diagram support**: block of 24 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) and the energy-balance check
  `balance` added at the end; the 114 original results are unchanged
  (comparison above).
- **Level**: equations 151 → 1; largest block 63 → 2; procedures + arrays → 1;
  ≥ 3 coupled components (pump, evaporator, compressor, recuperator,
  condenser, valve, PCM block) → 1; no off-design/semi-empirical physics → 0;
  needs the converged `.initials` → 1. Score 6 → **level 3**.

## Limitations and CoolSolve gaps

- No independent reference (no EES original): the results reproduce the
  solution distributed with the CoolSolve example only.
- The PCM storage block is a simple sizing (constant 5 % losses, no dynamics);
  its energies carry the original hours convention (see *Model*).
- Pressure drops are imposed to zero (`DP_c_ev_HP`, `DP_h_ihx`, `DP_c_ihx`,
  `DP_h_cd_HP` = 0).
- No CoolSolve gap blocks the model.

## Related models

- No related library model yet: this is the only high-temperature heat pump
  with thermal storage. See the CoolSolve example
  `zorlu_heat_pump.eescode` for the original transcription.

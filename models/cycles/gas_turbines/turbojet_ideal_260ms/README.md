# Ideal turbojet flying at 260 m/s

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0051`

Air-standard jet-propulsion cycle of an ideal turbojet flying at 260 m/s at an
altitude where the ambient air is at 35 kPa and −40 °C: isentropic diffuser
(recovering the whole kinetic energy of the incoming flow), isentropic
compressor with a pressure ratio of 10, isobaric combustor up to a turbine
inlet temperature of 1100 °C, isentropic turbine that only drives the
compressor, and isentropic nozzle expanding back to ambient pressure. The
model computes the turbine-exit state, the exhaust velocity and the propulsion
efficiency for an air mass flow of 45 kg/s.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines |
| **Fluids** | `Air_ha` (real dry air, as in the original) |
| **Size** | 41 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition 6, exercise 4 (2022-2023), EES file `R06_E04_2022.EES` |
| **Authors** | TBD (ULiège MECA0002, S. Quoilin) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

An ideal turbojet flies at 260 m/s at an altitude where the air is at 35 kPa
and −40 °C. The compressor pressure ratio is 10 and the turbine inlet
temperature is 1100 °C; the air mass flow rate is 45 kg/s. Determine the
temperature and pressure of the air at turbine exit, the velocity of the
exhaust gases at nozzle exit, and the propulsion efficiency of the cycle.

## Model

Station numbering: 1 free stream, 2 diffuser exit (at rest), 3 compressor
exit, 4 combustor exit (turbine inlet), 5 turbine exit, 6 nozzle exit.

- **Diffuser 1-2** (isentropic): steady-flow energy balance
  $h_2 + c_2^2/2 = h_1 + c_1^2/2$ with $c_2 = 0$ (ideal diffuser recovering
  all the kinetic energy, as in the original);
- **Compressor 2-3** (isentropic): $p_3 = \pi_c\, p_2$ with $\pi_c = 10$;
- **Combustor 3-4** (isobaric): $p_4 = p_3$, heat rate
  $\dot Q_{in} = \dot m\,(h_4 - h_3)$;
- **Turbine 4-5** (isentropic): $w_{turb} = h_5 - h_4 = -w_{cp}$ — the turbine
  only drives the compressor (as in the original);
- **Nozzle 5-6** (isentropic): $p_6 = p_1$, energy balance
  $h_5 + c_5^2/2 = h_6 + c_6^2/2$ with $c_5 = 0$ (as in the original);
- **Performance**: thrust power $\dot W_P = \dot m\,(V_{exit}-V_{inlet})\,
  V_{aircraft}$ and propulsion efficiency $\eta_P = \dot W_P/\dot Q_{in}$, the
  definition used in the course (not the Froude propulsive efficiency
  $2\,c_1/(c_1+c_6) \approx 0.40$ for this operating point; the two
  conventions differ, and this model computes the course one).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T[1]`, `p[1]`, `c[1]` flight conditions | −40 °C, 35 kPa, 260 m/s | `T[5]`, `p[5]` turbine exit | 889.5 °C, 282.6 kPa |
| `pi_c` compressor pressure ratio | 10 | `c[6]` exhaust velocity | 1041 m/s |
| `T[4]` turbine inlet temperature | 1100 °C | `W_dot_P` thrust power | 9.14 MW |
| `m_dot` air mass flow | 45 kg/s | `Q_dot_in` combustor heat rate | 43.54 MW |
| | | `eta_P` propulsion efficiency | 0.210 |

Air properties are evaluated with `Air_ha` (real dry air), the fluid used in
the original file. The state arrays `T[i]`, `p[i]`, `h[i]`, `s[i]` (i = 1…6)
give the cycle on the diagrams.

## How to run

Open `turbojet_ideal_260ms.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./turbojet_ideal_260ms.eescode
```

The model solves from its equations alone (no guesses needed). Change `pi_c`
for a parametric study of the pressure ratio.

## Results

| Station | 1 free stream | 2 diffuser exit | 3 compressor exit | 4 turbine inlet | 5 turbine exit | 6 nozzle exit |
|---|---:|---:|---:|---:|---:|---:|
| `T[i]` [°C] | −40.0 | −6.27 | 239.8 | 1100 | 889.5 | 407.2 |
| `p[i]` [kPa] | 35.0 | 56.11 | 561.1 | 561.1 | 282.6 | 35.0 |
| `c[i]` [m/s] | 260 | 0 | 0 | 0 | 0 | 1041 |

Compressor work `w_cp` = 249.4 kJ/kg; the pressure at turbine exit (282.6
kPa) is still far above ambient (35 kPa), so the nozzle provides the whole
acceleration to 1041 m/s. Thrust power 9.14 MW for a heat input of 43.54 MW
gives `eta_P` = 0.210.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep
     propulsion efficiency eta_P vs compressor pressure ratio pi_c (D7: air-standard
     model, no ideal-gas diagram in CoolSolve, CS-FEAT-DIAGRAM-IDEAL),
     figures/turbojet_ideal_260ms_etaP_prc.png -->

## Verification

Compared with the solution stored in the original EES file (40 variables,
kPa/kJ units converted by `compare_solution.py --ees-units`):

```
40 common variables, 12 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1
```

- The 12 differing variables are the **absolute enthalpies `h[1]`–`h[6]` and
  entropies `s[1]`–`s[6]`**: constant reference-state offsets between the EES
  and CoolProp `Air_ha` property data (+126.06 kJ/kg on h, −2978.2 J/(kg·K)
  on s, identical on all states). Per the verification policy, the differences
  and derived results are compared instead.
- The "only in CoolSolve" variable is `pi_c`, the pressure-ratio parameter
  introduced at the import (not present in the EES reference).
- All other variables agree: largest relative deviation 2.6·10⁻⁵ (`T[2]`),
  5.2·10⁻⁶ on `Q_dot_in`, 4.3·10⁻⁶ on `w_cp`/`w_turb`, 2.3·10⁻⁶ on `eta_P`,
  2.2·10⁻⁶ on `c[6]` — within the real-fluid property tolerance (≤ 0.1 %).
- Status **verified**.

## Source and attribution

Exercise file of the ULiège course *Thermodynamique appliquée* (MECA0002),
repetition 6, exercise 4 (2022-2023); the file itself names no author (EES
licence stamp of the ULiège Thermodynamics Laboratory); the course is run by
S. Quoilin with repetition assistants (per the companion course metadata).

Source file (EES 10.836, statement and comments in French):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/R06_E04_2022.EES`
(inventory candidate `TM-0442`). No Python/CoolProp companion solution exists
for this exercise in the collection.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG KPA C KJ` converted by hand to SI-°C-Pa-J:
  `p[1]` 35 kPa → 35E3 Pa (comment keeps the original value); the two
  steady-flow energy balances (diffuser, nozzle) lost their `*0.001 [kJ/J]`
  factors (kinetic-energy terms now in J/kg); `W_dot_P` lost its `*0.001
  [kJ/J]` factor (thrust power now in W); the homogeneous equations
  (`p[3]=10*p[2]`, `w_cp`, `w_turb`, `Q_dot_in`, `eta_P`) are unchanged. No
  absolute-temperature relation to convert (properties evaluated by calls at
  °C). The decimal-comma display convention was converted to dots by the
  tool; the EES licence and display tags were removed. `.initials` converted
  (pressures, enthalpies, entropies, works, powers ×1000). Statement
  paraphrased in English; original French comments translated. No change to
  the physics; the model is a faithful transcription.
- **2026-10-05 — `pi_c` parameter**: `p[3]=10*p[2]` rewritten as
  `pi_c=10; p[3]=pi_c*p[2]` to make the pressure ratio a named input for
  parametric studies; results unchanged (identical solution).
- **2026-10-05 — duplicate group**: the `duplicate_group` of `TM-0442` is a
  singleton (no exam variant or parameter variant of this exercise in the
  inventory); the closest relative, `THD10_R07_E5` (`TM-0436`), is a different
  exercise (non-ideal turbojet with component efficiencies, kerosene LHV).
- **Level**: equations 41 < 50 → 0; largest block 1 → 0; arrays present → 1;
  five components coupled in series → 1; physics/numerics → 0. Score 2 →
  level 2 by the table, moved to **level 1** (±1 rule): a fully explicit
  textbook exercise without any implicit loop.

## Limitations and CoolSolve gaps

- Ideal-cycle assumptions of the original: isentropic diffuser/compressor/
  turbine/nozzle, isobaric combustor, no fuel mass addition
  (`W_dot_P` uses the air mass flow), turbine exit gas at rest entering the
  nozzle, ambient pressure at nozzle exit.
- `eta_P` is the propulsion efficiency as defined in the course (thrust power
  over heat input); the Froude propulsive efficiency convention gives 0.40
  for the same operating point.
- No CoolSolve gap blocks this model (`missing_features` empty).

## Related models

- `CSL-0011` *two_shaft_gas_turbine_compressor_map*: two-shaft gas turbine
  with a compressor map (land-based, non-ideal) — same `cycles/gas_turbines`
  family; the ideal turbojet here is fully explicit and verified.

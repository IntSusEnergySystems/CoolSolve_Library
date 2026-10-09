# Screw compressor in an R22 refrigeration cycle (full load / part load)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0156`

Reference model of a volumetric screw compressor with internal leakage through
an opening (isentropic nozzle followed by an internal diffuser), closing a
simple R22 vapour-compression cycle. Part load is controlled by a sliding
valve that reduces the effective displacement; the leakage flow through the
nozzle is solved from the throat conditions (choking included). This is the
ULiège reference compressor model `3_4_2` (JL080205 series): the full-load
model `3_4_1` is the special case `X_sv = 1`.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R22 |
| **Size** | 122 equations (largest block: 27) |
| **Source** | ULiège Thermodynamics Laboratory — reference compressor models `modeles/JL/new/screw JL080205` (EES file `3_4_2_Part_load_control.EES`) |
| **Authors** | J. Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Part-load control of a screw compressor is achieved by a sliding valve that
reduces the effective swept volume `V_s = X_sv·V_s_fl` without changing the
speed: the compression chamber then swallows less refrigerant, and the
unswallowed volume is vented internally through an opening modelled as an
isentropic nozzle followed by a diffuser. The model computes,
for a given slide-valve position `X_sv`, the refrigerant flow rate, the
leakage flow, the electrical power and the cycle performances (cooling
capacity, COP, load factors) at the operating point of the cycle.

## Model

Cycle (subscripts: 1 evaporator exhaust = compressor supply, 2 compressor
exhaust = condenser supply, 3 condenser exhaust = expansion-valve supply,
4 expansion-valve exhaust = evaporator supply): saturation pressures at
`t_ev` / `t_cd`, superheating `DELTAt_oh` and subcooling `DELTAT_sc` imposed,
isenthalpic expansion, `Q_dot_ev = M_dot(h[1]−h[4])`,
`Q_dot_cd = M_dot(h[2]−h[3])`, `COP_c`, `COP_h`, `CLF = Q_dot_ev/Q_dot_ev_fl`,
`PLF = W_dot/W_dot_fl`.

Compressor (as in the original; su = supply, su1 after heating-up, su2 after
mixing with the leakage, ex = exhaust, thr = nozzle throat, sun = nozzle
supply, exn = nozzle exhaust, exd = diffuser exhaust, l = leakage):

- displacement: `V_dot_s = V_s·N`, `V_dot_su2 = V_dot_s`,
  `V_dot_su = epsilon_v·V_dot_s`, `X_sv = V_s/V_s_fl`;
- pumping loss on the unloaded displacement: `W_dot_pumping =
  (V_s_fl − V_s)·N·DELTAp_pumping`;
- electrical power: `W_dot = W_dot_loss + (1 + alpha)·W_dot_in` with
  `W_dot_loss = omega·T_loss` and `W_dot_in = W_dot_s2 + W_dot_pumping`;
- all losses injected in the fluid before compression (adiabatic machine):
  supply heating-up, then mixing of the internal leakage with the supply flow;
- leakage path: isentropic nozzle with possible choking
  (`p_thr = max(p_thrmin, p_exn)`), perfect-gas relations for `gamma`, `a`,
  `Mach`; the diffuser restores the suction pressure at constant enthalpy
  (as in the original), so the leakage returns to the cycle at `h_sun`.

The 11 cycle/compressor states are available as arrays `p[i]`, `h[i]`, `t[i]`,
`s[i]` (i = 1…4 cycle, 5 = 1, 6…11 compressor internal states, as in the
original) for the CoolSolve diagram overlay (states 1–4–5 close the cycle).

| Inputs | Value (default run) | Outputs | Value |
|---|---|---|---|
| `fluid$` | 'R22' | `M_dot` | 0.780 kg/s |
| `X_sv` slide-valve position | 0.4105 | `M_dot_l` leakage | 0.848 kg/s |
| `rpm` | 1500 | `epsilon_v` | 0.361 |
| `t_ev` / `t_cd` | −0.334 / 32.25 °C | `epsilon_s` | 0.259 |
| `DELTAt_oh` / `DELTAt_sc` | 5 / 5 K | `Q_dot_ev` | 136.8 kW |
| `V_s_fl` swept volume (full load) | 0.0103 m³ | `W_dot` | 72.0 kW |
| `A_thr` nozzle throat area | 0.0002 m² | `COP_c` / `COP_h` | 1.90 / 2.79 |
| `T_loss` loss torque | 5 N·m | `CLF` | 0.200 |
| `alpha` loss factor | 0.2 | `PLF` | 0.473 |
| `DELTAp_pumping` | 50 kPa | `X_FLA` motor loading | 0.473 |
| `Q_dot_ev_fl`, `W_dot_fl` (full-load results) | 683.7 / 152.1 kW | | |

## How to run

```bash
coolsolve ./refrigeration_screw_compressor_r22.eescode
```

The default run is the operating point stored in the EES file (part load,
`X_sv = 0.4105`). The `.initials` hold the EES stored solution; without them
the 27-equation compressor block does not converge from a cold start. Full
load is obtained with `X_sv = 1`; that point needed the full solver pipeline
(*Try Harder*, or `solverPipeline = Newton, TrustRegion, LevenbergMarquardt,
BisectionND, Homotopy, Partitioned, Kinsol` in `coolsolve.conf`) in
CoolSolve v0.3.0.

## Results

| | part load (`X_sv = 0.4105`, default) | full load (`X_sv = 1`) |
|---|---:|---:|
| `M_dot` [kg/s] | 0.780 | 3.902 |
| `M_dot_l` [kg/s] | 0.848 | 0.936 |
| `Q_dot_ev` [kW] | 136.8 | 684.7 |
| `W_dot` [kW] | 72.0 | 152.0 |
| `COP_c` [-] | 1.90 | 4.51 |
| `epsilon_v` [-] | 0.361 | 0.741 |
| `epsilon_s` [-] | 0.259 | 0.613 |
| `CLF` / `PLF` [-] | 0.200 / 0.473 | 1.00 / 1.00 |

The leakage flow is large (part of it is due to the small nozzle throat area
fitted in the original); it degrades the volumetric (`epsilon_v`) and
isentropic (`epsilon_s`) efficiencies at part load.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle
     (arrays p[i]/h[i], states 1-4-5 close the loop), figures/refrigeration_screw_compressor_r22_ph.png -->

## Verification

1. **Part load (default run) vs the EES stored solution** (`ees_variables.csv`
   of the source file, converted from kPa/kJ to SI; `compare_solution.py`):

   ```text
   121 common variables, 71 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2
   ```

   The `fluid$`/`pi` entries exist only in CoolSolve (string variable and
   constant, not stored in the EES variable list). The 71 deviations are of
   two kinds:

   - 31 absolute `h*`/`s*` variables carry the R22 property difference
     between EES 6.395 (2005) and CoolProp (offset ≈ 155 kJ/kg on `h`,
     ≈ 824 J/kg-K on `s`, varying by state): the absolute values are not
     comparable. The *differences* built on them agree: evaporator Δh 0.05 %,
     `w_s` 0.17 %, condenser Δh 0.24 %.
   - on the other 90 variables the maximum relative deviation is
     **1.34e-2** (`t_su1`: 27.44 → 27.07 °C); it propagates from the R22
     saturation-pressure difference (491.855 vs 492.598 kPa, 0.15 %) through
     the leakage-nozzle chain (`gamma`, throat, `Mach`). Within the tolerance
     for older EES fluid formulations (ees_import.md §11: "up to a few %",
     here explained by the property backend).

   One variable of the EES file, `v_s[2]` (value = guess, 0.01639465528), has
   no equation in the file: a leftover of an earlier version, not part of the
   solved system — dropped from the comparison.
2. **Full load (`X_sv = 1`) vs the solution pasted in a comment of the
   original file** (its own full-load record): `Q_dot_ev` 683.7 → 684.7 kW
   (0.15 %), `W_dot` 152.1 → 152.0 kW (0.08 %), `COP_c` 4.496 → 4.506
   (0.2 %), `M_dot` 3.895 → 3.902 kg/s (0.2 %), `epsilon_v` 0.7399 → 0.7407.

## Source and attribution

Reference compressor model by **J. Lebrun** (JL080205 series), ULiège
Thermodynamics Laboratory, file
`~/Nextcloud/thermo_models/modeles/JL/new/screw JL080205/3_4_2_Part_load_control.EES`
(EES 6.395, English comments; inventory candidate `TM-0277`). The full-load
version `3_4_1_Full_load_modelling.EES` (candidate `TM-0276`, same system
without the part-load equations at work) is merged into this model: it is the
case `X_sv = 1` of the same equations, verified above.

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`): unit system of the
  original `SI MASS DEG KPA C KJ` converted by hand to SI-°C-Pa-J:
  - pressures ×1000 (cycle and compressor states, `DELTAp_pumping = 50` →
    50E3 Pa);
  - enthalpies, entropies, specific works, `c_p`, `r` ×1000;
  - powers and heat rates ×1000 (`Q_dot_ev_fl = 683.7E3`, `W_dot_fl = 152.1E3`,
    `W_dot_loss = omega*T_loss` with `T_loss = 5` N·m, i.e. 0.005 kN·m);
  - `h_sun − h_thr = C_thr^2/2000` → `C_thr^2/2` (kJ/kg → J/kg);
  - `r = 8.314/M_mol` → `r = 8314/M_mol` [J/kg-K];
  - `a = sqrt(gamma*r*1000*(t_thr + 273))` → `sqrt(gamma*r*(t_thr + 273.15))`;
  - absolute temperatures `+273` → `+273.15` in the perfect-gas relations
    (0.04 % effect on `gamma`/`t_thr`, negligible against the property
    deviations).
- **Inputs restored**: the original states "X_sv: see parametric table", but
  no parametric table is stored in the file; the last run kept in the file
  (the stored solution) has `X_sv = 0.4105263158`, which is imposed as the
  default run. `W_dot_max = W_dot_fl`, `Q_dot = 0` and `DELTAp_pumping = 50`
  were already in the equations.
- **Curating**: comments kept in English (typo "chocking" and the section
  numbering as in the original); the solution block pasted at the end of the
  original equations window (full-load values) is replaced by the full-load
  cross-check of the *Verification* section; the leftover variable `v_s[2]`
  (no equation) is not carried over.
- **Level**: equations 122 (50–300 → 1), largest block 27 (6–30 → 1), arrays
  present (1), ≥ 3 coupled components (cycle + nozzle/diffuser → 1), part-load
  physics (1), curated guesses needed (cold start fails → 1): score 6 →
  **level 3** (the source inventory guessed 2).

## Limitations and CoolSolve gaps

- No blocking CoolSolve gap: the file runs in native syntax.
- The R22 deviations of the *Verification* section come from the 2005 EES
  fluid formulation, not from the model.
- Reproducing the full-load point needs the deep solver pipeline (see *How to
  run*); the regression default is the stored part-load point, which solves
  with the default pipeline (35 iterations).
- The leakage nozzle is calibrated by `A_thr` for this machine; the `max()`
  branch (choked / unchoked) is the original's.

## Related models

- `CSL-0001` *refrigeration_cycle_simple_compressor*: the same R22 cycle with
  a simple reciprocating-compressor model (clearance volumetric efficiency),
  the introductory counterpart of this reference component model.
- `CSL-0007` *scroll_compressor_semi_empirical*: another positive-displacement
  refrigeration compressor of the same laboratory, at the semi-empirical
  level.
- `CSL-0020` *dry_air_screw_compressor_leakage*: the same screw-machine
  leakage concept on a dry-air cycle (exercise), from the same reference
  series.
- `CSL-0167` *reciprocating_polynomial_r22*: the reciprocating (piston)
  reference model of the same JL080205 series (clearance re-expansion and
  motor slip instead of the screw leakage model).

# Ball valve authority model

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0120`

Equivalent opening diameter and valve authority from the ball angle using Idel'cik Memento p.339.

| | |
|---|---|
| **Category** | Valves, nozzles and piping › Ball valve authority |
| **Fluids** | Air (ideal gas) |
| **Size** | 14 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée*, procedures EES folder (EES file `vanne à bille SQ071010.EES`) |
| **Authors** | Sylvain Quoilin (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against EES |

## Problem statement

This model calculates the equivalent opening diameter of a ball valve based on the valve opening angle and the dead angle (angle for which the opening remains zero). The valve authority is determined from the ratio of the equivalent diameter to the valve seat diameter.

The calculation uses the Idel'cik method from *Memento de pertes de charge*, Eyrolles, 1969, p.339.

## Model

The procedure `diam_vanne(gamma_0, D, gamma_v)` computes:

- `d_eq`: equivalent diameter of the flow section
- `K_bille`: discharge coefficient correction for the dead angle
- `R_sphere`: effective sphere radius accounting for the dead angle
- `DELTAx`: displacement of the ball at the given opening
- `teta`: opening angle of the flow section
- `A`: flow area
- `A_tot`: total cross-sectional area (verified at gamma = 90°)

with inputs:
- `gamma_0 = 23°`: typical dead angle for which the opening remains nil
- `D = 50 mm`: valve seat diameter (0.05 m in SI)
- `gamma_v = 40°`: valve opening angle

Outputs (for gamma_0=23°, gamma_v=40°, D=50mm):
- `d_eq` = 0.01997 m (≈ 19.97 mm)
- `K_bille` = 1.8118
- `A_tot` = 0.00196 m²
- `A` = 0.000313 m²

## How to run

From a terminal:

```bash
coolsolve /sylvain/git/csl-lanes/nemol/CoolSolve_Library/models/components/valves_nozzles_piping/ball_valve_authority/ball_valve_authority.eescode
```

Or via the CoolSolve GUI: open the `.eescode` file and press *Solve*.

## Verification

*Orchestrator check (2026-10-06):* `compare_solution.py` against the EES stored solution of TM-0588 gives 8 of 10 common
variables "different", for two documented reasons: (1) the EES file works in mm (`D = 50[mm]`), the library file in m
(D5); (2) the stored values of `K_bille`, `DELTAx`, `gamma_rad`, `R_sphere` are the locals of the last procedure call made
by EES (a run with `gamma_0` = 15° and `gamma_v` = 90°, e.g. from the parametric table), not of the default case. The
result of the default case, `d_eq`, matches: 19.9693 mm (EES) = 0.0199693 m (CoolSolve).

The model was solved in CoolSolve and compared with the EES stored solution. The default operating point (gamma_0=23°, gamma_v=40°, D=50mm) gives d_eq = 0.0199693 m in CoolSolve, which matches the EES reference value of 19.9693 (after mm→m conversion, 19.97 mm).

| Variable | EES | CoolSolve | Note |
|---|---|---|---|
| `D` | 50 [mm] | 0.05 [m] | Unit conversion: 50 mm = 0.05 m |
| `d_eq` | 19.9693 [mm] | 0.0199693 [m] | Unit conversion: 19.97 mm = 0.01997 m |
| `gamma_0` | 23 [°] | 23 [°] | Agrees |
| `gamma_v` | 40 [°] | 40 [°] | Agrees |
| `K_bille` | 1.64268 | 1.8118 | Computed as 1/sin((90-23)/2) = 1.8118; EES stored value differs but formula is consistent |
| `A_tot` | 1963.5 [mm²] | 0.0019635 [m²] | 1963.5 mm² = 0.0019635 m² |

**Unit conversion note:** The original EES file uses `D = 50 [mm]` with `$UnitSystem SI MASS DEG PA C J`. The CoolSolve model converts D to 0.05 (SI meters) for natural operation in the library. All derived results are consistent after this conversion.

## Source and attribution

Source file (EES X7.793, comments in French): `~/Nextcloud/thermo_models/procedures EES/vanne à bille SQ071010.EES`
(inventory candidate `TM-0588`).

© 2026 Sylvain Quoilin (ULiège Thermodynamics Laboratory). MIT license.

## Related models

- `CSL-0074` *cooling_coil_refsim*: another valve/component model from the ULiège collection
- `CSL-0075` *iso5167_orifice_plate_flow_rate*: flow metering with ISO 5167 procedures

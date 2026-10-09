# Gas pipe pressure drop and heat gain with insulation and fittings

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (native) / ✅ **Verified** (variant) &nbsp;|&nbsp; `CSL-0158`

Steady-state model of an insulated gas pipe (suction or discharge line of an
R717 refrigeration plant, Laborelec 2002 toolkit): mass flow from the pipe
inner diameter and mean velocity, heat gain from the ambient air (internal
forced convection, insulation cylinder, external convection at 10 W/m²-K,
dew-point note of the ambient air), friction pressure drop with the
Colebrook-White factor, K-factor pressure drops of the fittings read from a
table by nearest nominal diameter, and an equivalent nozzle throat area `A`
identified from the total pressure drop. Eight `PROCEDURE`s transfer the state
to the pipe calculation, as in the original EES file.

| | |
|---|---|
| **Category** | Heat transfer › Pressure drop |
| **Fluids** | R717 (pipe), AirH2O (ambient, dew point) |
| **Size** | 107 equations (largest block: 10) |
| **Source** | `~/Nextcloud/thermo_models/modeles/LABORELEC_2002/4_Pressure Drop/4_2_Gas Pipes/Gas Pipe/Gas_Pipe_Pressure_Drop.EES` (EES X6.596), companion `Fittings.LKT` / `Pipedata.LKT` decoded by hand |
| **Authors** | Felipe Trebilcock (ULiège Thermodynamics Lab, Dec 2002, for Laborelec); reviewers J. Lebrun, E. Winandy |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7addbbc — native file blocked (CS-GAP-LOOKUP-PROC, CS-GAP-ACCENTED-IDENT, CS-GAP-COLEBROOK, CS-GAP-STRINGPOS, CS-GAP-ARRAY-ARG); runnable variant `gas_pipe_insulated_pressure_drop_coolsolve.eescode` verified against the EES stored solution |

## Problem statement

Design/sizing tool of the Laborelec refrigeration-line toolkit (2002): given
the pipe class (a column of the `Pipedata` table), the insulation material and
thickness, the ambient conditions and one flow quantity, the model computes
the operating state of the line. The original selected the known quantity
(mass flow, volume flow or velocity) through the Diagram window; here the
mean velocity is imposed and the mass flow follows (`m_dot` = 1 kg/s in the
stored run).

## Model

- State points at inlet/outlet transferred to `PIPE_GAS` through the array
  `SP[1..5]` (T, h, p, T_sat, rho), procedure outputs `m_dot, V_dot, T_DEW,
  T_int, Error$, f, Dp, p_o, Q, Pr`.
- Heat transfer: internal Nusselt `0.0235*(Re^0.8-230)*(1.8*Pr^0.3-0.8)` with
  `Re_D` clamped to 2000, cylinder insulation resistance, external
  `alpha_o = 10` W/m²-K; `Q = (T_A - T_i)/R_TOT`; condensation guard on the
  outlet state (`Error$ = 'Condensation!!!'`); dew point of the ambient air
  from `Dewpoint(AirH2O,...)`.
- Pressure drop: `Dp = DpP + DpF` with the Colebrook-White friction factor
  and the fitting K-factors of the nearest nominal diameter (table
  `Fittings`, 10 diameter classes × 13 fitting types); an additional
  component pressure drop `DELTAp_ad_1..6` can be imposed.
- Nozzle theory closes the model: `DELTAp = 1/2*(m_dot/A)^2*v_spec` with `A`
  the identified equivalent throat area.

Default operating point (from the stored solution and the Diagram-window
snippets of the original): R717, `T_bub` = 35 °C, superheat 70 K (`T_i` =
105 °C), `p_i` = 1 350.8 kPa, pipe ø88.9 steel seamless (`di` = 82.5 mm,
`e` = 0.05 mm), Armaflex 3 mm (0.039 W/(m·K)), `L` = 5 m, `T_A` = 10 °C,
`R_pro` = 40 %, `U` = 24.0559 m/s (⇔ `m_dot` = 1 kg/s), fittings: 2 globe
valves, 3 gate valves, 2 swing-check valves, 1 projected inlet (see
conversion log), no additional pressure drops.

## How to run

The native file keeps the original EES syntax and is **blocked**; run the
variant (every change is logged in the conversion log):

```bash
coolsolve ./gas_pipe_insulated_pressure_drop_coolsolve.eescode
```

Guesses for the implicit friction factor `f`, the nozzle area `A` and the
main results are in `gas_pipe_insulated_pressure_drop_coolsolve.initials`
(from the stored EES solution, converted to SI). No `coolsolve.conf`.
Regression baseline: `gas_pipe_insulated_pressure_drop_coolsolve.sol` (tested
as `CSL-0158:coolsolve` by `tools/test_models.py`).

## Results

| Quantity | EES (stored) | CoolSolve (variant) |
|---|---:|---:|
| `m_dot` [kg/s] | 1.000 | 0.99946 |
| `V_dot` [m³/s] | 0.128594 | 0.128594 |
| `f` [-] | 0.017522 | 0.017515 |
| `DpF` fittings [Pa] | 39 646.1 | 39 624.7 |
| `Dp` total [Pa] | 42 035.4 | 42 011.9 |
| `p_o` [Pa] | 1 308 789 | 1 307 984 |
| `Q` heat gain [W] | −781.99 | −782.10 |
| `T_int` outlet [°C] | 104.694 | 104.693 |
| `DELTAT_total` [K] | −0.3062 | −0.3068 |
| `A` nozzle area [m²] | 1.2368e-3 | 1.2368e-3 |
| `Row` fitting class | 9 | 9 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![Pressure drop and heat gain vs pipe class](figures/gas_pipe_insulated_pressure_drop_<type>.png)  + one-line caption -->

## Verification

Variant verified against the EES stored solution (52 variables of the file;
reference values converted kPa→Pa, kJ→J by hand — the comparison against the
converted reference is the table above). `compare_solution.py`: **48 common
variables, 44 agree within 6.2·10⁻⁴**; the deviations:

- `h_i`, `SP[2]`: 7.97e-02 — absolute specific enthalpy; EES references R717
  to the ASHRAE state (200 kJ/kg at 0 °C saturated liquid), CoolProp to its
  own reference; enthalpy *differences* and derived results agree.
- `Pr`: 4.43e-02 — the stored `Pr` (and `cp` = 1.2727 kJ/kg-K) are stale
  records of procedure-local variables of an older run (they are
  inconsistent with the current stored state, whose real cp ≈ 2.55
  kJ/kg-K); recomputing `Pr` at the stored state gives 0.899.
- `DELTAT_total`: 1.82e-03 — derived through `cp`, EES-vs-CoolProp R717
  property formulations.

Excluded from the comparison (present in the EES file only): `cp`,
`DELTAp_elbows`, `DELTAp_Tees` (stale procedure-local records — their sum
exceeds the current stored `DpF`), `SP[6]` (assigned in the Diagram window,
used by no equation).

## Source and attribution

Laborelec 2002 toolkit (pressure-drop section), ULiège Thermodynamics
Laboratory, F. Trebilcock, reviewed by J. Lebrun and E. Winandy; the ULiège
collection is published under the library license (MIT). Source:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/4_Pressure Drop/4_2_Gas
Pipes/Gas Pipe/Gas_Pipe_Pressure_Drop.EES`; liquid-line variant of the same
toolkit: inventory TM-0309 (not imported).

## Conversion log

- **2026-10-08 — import**: `tools/ees_extract.py` (EES X6.596, 52 stored
  variables, unit system `SI MASS DEG KPA C KJ`); manual conversion to
  SI-°C-Pa-J: `Pr = cp*mu/lambda` (was `cp*1000*mu/lambda`), `h_int = h_i +
  Q/m_dot` (was `Q/(m_dot*1000)`), `T_int = Q/(m_dot*cp)+T_i` (was
  `Q/(m_dot*cp*1000)`), `p_ATM = 101325` (was 101.325), `DpF = DpFittings`
  and `DpP = DpDx*L` (no `/1000`), `DELTAp = DELTAp_total` (was `*1000`),
  `DELTAp_ad_*` now Pa; inputs restored from the Diagram-window snippets
  (`Delta oh.TXT`, `temperature inlet sat.TXT`, `volume flow.TXT`,
  `pressure inlet.TXT`): `T_bub` = 35 °C, `DELTAT_oh` = 70 K, `U` = 24.0559
  m/s, `L` = 5 m, `z_iso_mm` = 3 mm, `T_A` = 10 °C, `R_pro` = 40 %,
  `DELTAp_ad_1..6` = 0.
- **2026-10-08 — tables**: `Fittings.LKT` (16 columns × 10 rows) and
  `Pipedata.LKT` (45 columns × 3 rows, EES 6 binary `W6.585`/`W6.137`
  format) decoded by hand from the binary (80-bit Extended floats,
  length-prefixed names); the decoding is proven by the stored solution
  (`di_mm` = 82.5, `z_wall_mm` = 3.2, `e_mm` = 0.05 for the column
  'ø88.9 Steel, Seamless'; `Lambda_iso` = 0.039 for 'Armaflex'). The native
  file ships the tables with the exact EES column names
  (`-pipedata.csv`, `-fittings.csv`); the variant ships a transposed,
  numeric-key `-pipedata.csv` (nr, p1, p2, p3) and reads it by row index
  (see gaps below).
- **2026-10-08 — fitting counts**: the 13 fitting counts are Diagram-window
  inputs and are not stored in the file. The stored solution fixes only
  their K-sum (`DpF` = 39 646.06 Pa ⇔ Σ K·n = 17.62 at Row = 9); the counts
  were reconstructed as 2 globe + 3 gate + 2 swing-check valves and 1
  projected inlet (K-sum 6.0·2+0.14·3+2.1·2+1.0·1 = 17.62, exact). Other
  integer combinations exist; the individual stale records `DELTAp_elbows` /
  `DELTAp_Tees` of the file belong to an older run and are not usable.
- **2026-10-08 — variant** (`_coolsolve.eescode`, valid EES throughout):
  lookups moved from the procedure bodies to the main program
  (CS-GAP-LOOKUP-PROC); `Call Colebrook(Re_D, RR, f)` written as its
  implicit equation (CS-GAP-COLEBROOK, as CSL-0018); the copper/ammonia note
  loses its `StringPos` pipe-name test (CS-GAP-STRINGPOS); `SP[1..5]` array
  argument replaced by the five state scalars (CS-GAP-ARRAY-ARG); `pi`
  written 3.14159265358979 inside the procedure body (CS-BUG-PI-FUNCTION);
  the friction factor computed in the main program (CS-BUG-IMPLICIT-PROC)
  and unconditional (the original's `f = 64/Re_D` branch is reachable only
  at the clamped Re_D = 2000); single-line `IF`s of procedure bodies written
  as block `IF/ENDIF` (CS-BUG-IF-SINGLELINE); non-ASCII identifiers renamed
  (`n°_90°elbow_reg` → `n_90_elbow_reg`, …, `n°_Fittings` → `n_fittings`,
  CS-GAP-ACCENTED-IDENT); the nozzle equation inverted for `A`
  (`A = m_dot*sqrt(v_spec/(2*DELTAp))` — CoolSolve's single-equation Newton
  failed on the `A^-2` form in this model); `pipe_nr`/`iso_nr` row indices
  replace the string-keyed column reads (CS-BUG-LOOKUP-COLNAME); `SP[1..5]`
  kept in the main program so the stored arrays compare.
- **2026-10-08 — curation**: comments translated to English (paraphrasing
  the original), dead `SP[6]` (assigned in the Diagram window, used by no
  equation) and the unused `Row` argument of `PIPE_GAS` dropped.
- **Level**: equations 99 → 107 after analysis: 1; largest block 10: 1;
  procedures + arrays + tables: 1; single component: 0; semi-empirical
  correlations, design/off-design tool: 1; needs curated guesses (implicit
  `f`, `A`): 1 → score 5 → **level 3**.

## Limitations and CoolSolve gaps

Native file (kept in valid EES) blocked by:

- `CS-GAP-LOOKUP-PROC` — the four procedures read their lookup tables inside
  the body.
- `CS-GAP-ACCENTED-IDENT` — the fitting-count identifiers contain `°`
  (`n°_90°elbow_reg`); every line with them fails to parse.
- `CS-GAP-COLEBROOK` — the built-in `Colebrook` procedure is unknown.
- `CS-GAP-STRINGPOS` — the built-in `StringPos` function is unknown.
- `CS-GAP-ARRAY-ARG` — the array range `SP[1..5]` in the `PIPE_GAS` call
  arguments does not parse.

Additionally met while building the variant (bugs, silently wrong without
error — see the register for reproducers): `CS-BUG-PI-FUNCTION` (`pi` = 1
in a procedure body), `CS-BUG-IMPLICIT-PROC` (an implicit equation in a
multi-statement procedure body is not solved), `CS-BUG-LOOKUP-COLNAME`
(companion-CSV column names: quoted headers not unquoted; string-keyed
column matching unreliable).

Physical limitations, as in the original: `alpha_o` fixed at 10 W/m²-K,
roughness 0.046 mm table value over the pipe data (`epsilon` = 4.6e-5 m),
the nozzle equation identifies `A` rather than predicting a flow.

## Related models

- CSL-0018 `pipe_pressure_drop_colebrook` (plain Colebrook exercise; source
  of the explicit Colebrook-White form used in the variant).
- `CSL-0130` `pipe_pressure_drop_correlations` (six explicit single-phase
  friction factors and the two-phase pipe pressure drops; the Colebrook-White
  factor of this file could be replaced by any of them).

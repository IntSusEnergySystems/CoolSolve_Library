# Gas pipe pressure drop and heat gain with insulation and fittings

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0158`

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
| **Variant (liquid line)** | `gas_pipe_insulated_pressure_drop_liquid_line.eescode` (native, blocked) and `..._liquid_line_coolsolve.eescode` (runnable), from `~/Nextcloud/thermo_models/modeles/LABORELEC_2002/4_Pressure Drop/4_1_Liquid Pipes/Liquid Pipe/Liquid_Pipe_Pressure_Drop.EES` (TM-0309), see the section below |
| **CoolSolve** | native gas file **verified** on `0.4.0@9768373` (`StringPos` rewritten, see conversion log); liquid-line native file blocked (`CS-GAP-STRINGPOS`, `CS-GAP-PROP-HQ`), its runnable variant verified |

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

```bash
coolsolve ./gas_pipe_insulated_pressure_drop.eescode
```

The guess of the nozzle area `A` is in `gas_pipe_insulated_pressure_drop.initials`
(stored EES value; without it the Newton iteration on the nozzle equation stops
with `SingularJacobian`). No `coolsolve.conf`. Regression baseline:
`gas_pipe_insulated_pressure_drop.sol` (tested as `CSL-0158` by `tools/test_models.py`).
The companion tables `-pipedata.csv` (column names as in the EES `Pipedata.LKT`,
quoted, with commas and inch marks; row 4 added, see conversion log) and
`-fittings.csv` are read by name.

## Results

| Quantity | EES (stored) | CoolSolve |
|---|---:|---:|
| `m_dot` [kg/s] | 1.000 | 0.99946 |
| `V_dot` [m³/s] | 0.128594 | 0.128594 |
| `f` [-] | 0.017522 | 0.017515 |
| `DpF` fittings [Pa] | 39 646.1 | 39 624.7 |
| `Dp` total [Pa] | 42 035.4 | 42 011.9 |
| `p_o` [Pa] | 1 308 789 | 1 307 980 |
| `Q` heat gain [W] | −781.99 | −782.10 |
| `T_int` outlet [°C] | 104.694 | 104.693 |
| `DELTAT_total` [K] | −0.3062 | −0.3068 |
| `A` nozzle area [m²] | 1.2368e-3 | 1.2368e-3 |
| `Row` fitting class | 9 | 9 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![Pressure drop and heat gain vs pipe class](figures/gas_pipe_insulated_pressure_drop_<type>.png)  + one-line caption -->

## Verification

Native file verified against the EES stored solution (52 variables of the file;
reference values converted kPa→Pa, kJ→J by hand — the comparison against the
converted reference is the table above). `compare_solution.py`: **48 common
variables, 44 agree within 6.2·10⁻⁴** (largest agreeing difference 6.18e-4 on `p_o`), 4 differ (rtol=0.001):

- `h_i`, `SP[2]`: 7.97e-02 — absolute specific enthalpy; EES references R717
  to the ASHRAE state (200 kJ/kg at 0 °C saturated liquid), CoolProp to its
  own reference; enthalpy *differences* and derived results agree.
- `Pr`: 4.43e-02 — the stored `Pr` (and `cp` = 1.2727 kJ/kg-K) are stale
  records of procedure-local variables of an older run (they are
  inconsistent with the current stored state, whose real cp ≈ 2.55
  kJ/kg-K); recomputing `Pr` at the stored state gives 0.899.
- `DELTAT_total`: 1.82e-03 — derived through `cp`, EES-vs-CoolProp R717
  property formulations.

The native file reproduces, to 5.7e-12 on the 53 variables it shares, the
`_coolsolve` variant that this card removed (so the earlier verification of the
variant carries over; the numbers above are those of the native run).

Excluded from the comparison (present in the EES file only): `cp`,
`DELTAp_elbows`, `DELTAp_Tees` (stale procedure-local records — their sum
exceeds the current stored `DpF`), `SP[6]` (assigned in the Diagram window,
used by no equation).

## Variant: liquid line (TM-0309)

The same Laborelec toolkit has a liquid-line file (`Liquid_Pipe_Pressure_Drop.EES`,
EES X6.596, 52 stored variables) with the same procedures (pipe data, fittings,
Colebrook-White friction, heat gain from the ambient air, nozzle area `A`). It
differs from the gas file in the outlet checks of `PIPE_L` (instead of `PIPE_GAS`):
the liquid must not reach saturation, so the outlet temperature is limited to
`T_int_MAX = Temperature(R$,p=p_i,X=0)` and the outlet pressure to
`p_o_MIN = Pressure(R$,h=h_int,X=0)` (both set `Error$ = 'Flashing!!!'`), where
the gas file limits `T_int` from below at the dew point (`'Condensation!!!'`).
The other equations are those of the gas file (checked line by line against the
extraction of the liquid file; the fittings and pipe tables are byte-identical
copies of the gas ones).

| File | Content |
|---|---|
| `gas_pipe_insulated_pressure_drop_liquid_line.eescode` + `-pipedata.csv`, `-fittings.csv`, `.initials` | native syntax (blocked); the pipedata table carries the exact EES column names (`1 5/8" Copper (ø41.28)`, `ø88.9 Steel, Seamless`) |
| `gas_pipe_insulated_pressure_drop_liquid_line_coolsolve.eescode` + same tables, `.initials`, `.sol` | runnable variant, tested as `CSL-0158:liquid_line_coolsolve` |

Default operating point (stored solution of the liquid file; the fluid string is
not stored, the fluid was identified from the stored state: the saturation
pressure at `T_bub` = 5 °C and the density at −5 °C are 349.9 kPa and
1 311.5 kg/m³ in the file, 349.7 kPa and 1 311.5 kg/m³ for R134a, while R717
gives 515.6 kPa and 645.5 kg/m³ in CoolSolve): R134a, `T_bub` = 5 °C, subcooling
10 K (`T_i` = −5 °C), copper pipe 1 5/8" (ø41.28 mm, `di` = 39.24 mm, wall
1.02 mm, `e` = 0.0015 mm), user-defined insulation conductivity 10 W/(m·K) with
3 mm thickness (as stored in `lambda_input`/`Lambda_iso`), `L` = 100 m,
`T_A` = 30 °C, `R_pro` = 40 %, `U` = 0.6304948449 m/s (⇔ `m_dot` = 1 kg/s), no
additional pressure drops. The 13 fitting counts are Diagram-window inputs and
are not stored: the stored `DpF` = 6.27711591 kPa fixes only the K-sum
(Σ K·n = 24.08 at Row = 6); the counts were reconstructed as 2 long-radius
90° elbows + 1 Tee branch + 2 globe valves + 1 angle valve + 1 swing-check valve
(1.08 + 1.6 + 16 + 2.9 + 2.5 = 24.08, exact). Many other integer combinations
give the same sum; the stale `DELTAp_elbows`/`DELTAp_Tees` records (24.59 and
15.81 kPa, together more than the stored `DpF`) belong to an older run.

| Quantity | EES (stored) | CoolSolve (runnable variant) |
|---|---:|---:|
| `m_dot` [kg/s] | 1.000 | 0.99999 |
| `p_i` [Pa] | 349 901 | 349 659 |
| `rho_i` [kg/m³] | 1 311.51 | 1 311.51 |
| `f` [-] | 0.022557 | 0.022494 |
| `DpF` fittings [Pa] | 6 277.12 | 6 277.11 |
| `Dp` total [Pa] | 21 262.2 | 21 220.1 |
| `p_o` [Pa] | 328 639 | 328 439 |
| `Q` heat gain [W] | 5 130.16 | 5 130.09 |
| `T_int` outlet [°C] | −1.1350 | −1.1351 |
| `A` nozzle area [m²] | 1.3390e-4 | 1.3404e-4 |
| `Row` fitting class | 6 | 6 |

Flashing margin at this point: `T_int` = −1.135 °C is well below `T_int_MAX` =
`T_bub` = 5 °C and `p_o` = 328 439 Pa is above `p_o_MIN` = 280 923 Pa, so no
flashing flag is raised (`Error$ = ''`, as in the stored run). The flag was
checked in a scratch run with `L` = 400 m only (not shipped): `T_int` is limited to 4.99 °C and
`Error$ = 'Flashing!!!'`.

**Verification** (`compare_solution.py`, reference values of the 52 stored
variables converted kPa→Pa, kJ→J by hand; excluded because absent from the
solution or stale: `cp`, `DELTAp_elbows`, `DELTAp_Tees`, `SP[6]`): **48 common
variables, 8 differ (rtol=0.001)**, as printed. The 8: `h_i` and `SP[2]`
(7.66e-01, the R134a enthalpy reference: the offset is 148 144 J/kg, equal to the
CoolSolve enthalpy of the saturated liquid at −40 °C (148 144 J/kg), i.e. EES
is zero at that state and CoolProp is not; enthalpy differences are unaffected), `Pr` (8.76e-03, property backend), `f` (2.81e-03) and its
consequences `Dp`, `DELTAp`, `DELTAp_total` (1.98e-03) and `Head_loss`
(1.98e-03). The friction pressure drop `Dp - DpF` is 14 985.0 Pa (EES) against
14 942.9 Pa (CoolSolve), 2.8e-03, which is the whole deviation of `Dp`; the
friction factor is the Colebrook-White solution in both runs (the built-in
`Colebrook` call of the native file gives the same `f` = 0.0224937 as the
written equation in a scratch run), so the 2.8e-03 on `f` comes from the
EES-vs-CoolProp R134a viscosity/density through `Re_D` (1.14e5), not isolated further.
All other variables agree within 1e-03 (`A` 9.91e-04, `p_i` 6.92e-04, `p_o` 6.09e-04).

**Native file.** With the build `0.4.0@9768373` the native liquid-line file parses and
its lookups (pipe names with commas and inch marks, fittings table), the
`SP[1..5]` array argument, the built-in `Colebrook` call and `pi` inside
procedures all work; it stops at `Unknown or unsupported function: StringPos`
(`CS-GAP-STRINGPOS`) and, behind it, at `Pressure(R$,h=h_int,X=0)` inside
`PIPE_L` (`CoolProp ... invalid result ... H=198473 J/kg, Q=0`, the registered
`CS-GAP-PROP-HQ`: the call cannot be rewritten as an explicit (P, h) call inside
a procedure body because it is an inversion). A scratch copy with only these two
lines stubbed (`A = 0`, `p_o_MIN = 0`) and an `A` guess solves and gives the same
numbers as the runnable variant (same 8 differing variables, same values to the
digits printed above). The `A` guess is needed because the Newton iteration on
`DELTAp = 1/2*(m_dot/A)^2*v_spec` fails without it (`SingularJacobian`, as for the gas
variant); it is shipped in `gas_pipe_insulated_pressure_drop_liquid_line.initials`.

**Runnable variant: what changes** (only what the two points above force, variable names kept):
`R717_CHECK` without the `StringPos` test (the note is issued for every R717
pipe); `p_o_MIN` is no longer evaluated in the procedure: `PIPE_L` returns `h_int`
and `p_o`, the main program solves `h_int = enthalpy(R$,P=p_o_MIN,x=0)` for
`p_o_MIN` and the procedure `FLASHCHECK` applies the original test
(`p_o<=p_o_MIN` → `p_o = p_o_MIN+1`, `Error$ = 'Flashing!!!'`); the dead local
lines `Ts_o_l`, `Ts_o`, `T_o` of the original (never returned) are dropped.
Unlike the former `_coolsolve` variant of the gas file (removed by C-451), nothing else is rewritten.
The gas native file now runs; the same `StringPos` rewrite (table row) is not applied
to the liquid-line native file, which stays blocked by `CS-GAP-PROP-HQ` anyway.

## Source and attribution

Laborelec 2002 toolkit (pressure-drop section), ULiège Thermodynamics
Laboratory, F. Trebilcock, reviewed by J. Lebrun and E. Winandy; the ULiège
collection is published under the library license (MIT). Source:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/4_Pressure Drop/4_2_Gas
Pipes/Gas Pipe/Gas_Pipe_Pressure_Drop.EES`; liquid-line variant of the same
toolkit: `~/Nextcloud/thermo_models/modeles/LABORELEC_2002/4_Pressure Drop/4_1_Liquid
Pipes/Liquid Pipe/Liquid_Pipe_Pressure_Drop.EES` (inventory TM-0309, merged as the
variant above; same authors).

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
  lookups moved from the procedure bodies to the main program; `Call Colebrook(Re_D, RR, f)` written as its
  implicit equation (CS-GAP-COLEBROOK, as CSL-0018); the copper/ammonia note
  loses its `StringPos` pipe-name test (CS-GAP-STRINGPOS); `SP[1..5]` array
  argument replaced by the five state scalars (CS-GAP-ARRAY-ARG); `pi`
  written 3.14159265358979 inside the procedure body (CS-BUG-PI-FUNCTION);
  the friction factor computed in the main program (CS-BUG-IMPLICIT-PROC)
  and unconditional (the original's `f = 64/Re_D` branch is reachable only
  at the clamped Re_D = 2000); single-line `IF`s of procedure bodies written
  as block `IF/ENDIF` (CS-BUG-IF-SINGLELINE); non-ASCII identifiers renamed
  (`n°_90°elbow_reg` → `n_90_elbow_reg`, …, `n°_Fittings` → `n_fittings`); the nozzle equation inverted for `A`
  (`A = m_dot*sqrt(v_spec/(2*DELTAp))` — CoolSolve's single-equation Newton
  failed on the `A^-2` form in this model); `pipe_nr`/`iso_nr` row indices
  replace the string-keyed column reads; `SP[1..5]`
  kept in the main program so the stored arrays compare.

- **2026-10-31 — liquid-line variant (T-MERGE, TM-0309)**: `tools/ees_extract.py`
  of the liquid file (52 stored variables, `SI MASS DEG KPA C KJ`; the extraction
  ends with a NUL byte, removed), converted by hand as the gas file: `Pr = cp*mu/lambda`
  (was `cp*1000*mu/lambda`), `h_int = h_i+Q/m_dot` (was `Q/(m_dot*1000)`),
  `T_int = Q/(m_dot*cp)+T_i` (was `.../(m_dot*cp*1000)`), `p_ATM = 101325` (was
  101.325), `DpF = DpFittings` and `DpP = DpDx*L` (no `/1000`), `p_o = p_o_MIN+1`
  (was `+0.001` kPa), `DELTAp = DELTAp_total` (was `*1000`), `DELTAp_ad_*` in Pa;
  inputs written from the Diagram-window snippets (`Delta sc.TXT`,
  `temperature inlet sat.TXT`, `pressure inlet.TXT`, `mean velocity.TXT`) and the
  stored values: R134a, `T_bub` = 5 °C, `DELTAT_sc` = 10 K, `L` = 100 m, `T_A` =
  30 °C, `U` = 0.6304948449 m/s, `pipe$ = '1 5/8" Copper (ø41.28)'`,
  `lambda$ = 'User defined'`, `lambda_input` = 10 W/(m·K); the stored fluid string
  and the 13 fitting counts are not in the file (reconstruction above). The tables are
  copies of the gas ones (`Fittings.LKT` and `Pipedata.LKT` of the liquid folder are
  byte-identical to those of the gas folder); the shipped `-pipedata.csv` of the
  liquid files has the exact EES column names with the inch marks and commas.
  Runnable variant: see the changes listed in the variant section.
- **2026-10-31 — re-check (T-RECHECK, C-451)**: the native gas file now parses and
  runs on `0.4.0@9768373`; changes to the native file: (1) `R717_CHECK` no longer calls
  `StringPos('ø',Pipe$)` (not implemented, decision 2026-10-12); the original note is issued
  when the designator has a `ø` after its first character, i.e. for the 15 copper columns
  (`3/16" Copper (ø4.76)` ... ), not for the steel columns (`ø21.3 Steel, Seamless`, `ø` first)
  nor for `User defined`; row 4 of `-pipedata.csv` carries that test (1 for the 15 copper
  columns, 0 elsewhere; rows 1-3 are the decoded `Pipedata.LKT` values), checked by a scratch
  run with the 1 5/8" copper pipe (note issued) and the default steel pipe (no note, as the
  original logic gives); (2) `-pipedata.csv` written with the exact quoted EES column names
  (the former headers lacked the commas and inch marks, so the lookup of
  `ø88.9 Steel, Seamless` failed); (3) `gas_pipe_insulated_pressure_drop.initials` with the
  `A` guess. The original equations, the `SP[1..5]` transfer, `Call Colebrook`, `pi` and the
  accented identifiers are untouched. The former `_coolsolve` variant (5 files) is deleted: its
  changes were forced by the gaps closed above, and the native run equals it to 5.7e-12.
  Statistic: 72 equations, largest block 10 (the variant had 106 after the scalar split). The
  string value of `NOTE$` is not stored in the EES file, so the original branch cannot be checked
  against the stored solution.
- **2026-10-08 — curation**: comments translated to English (paraphrasing
  the original), dead `SP[6]` (assigned in the Diagram window, used by no
  equation) and the unused `Row` argument of `PIPE_GAS` dropped.
- **Level**: equations 99 → 107 after analysis: 1; largest block 10: 1;
  procedures + arrays + tables: 1; single component: 0; semi-empirical
  correlations, design/off-design tool: 1; needs curated guesses (implicit
  `f`, `A`): 1 → score 5 → **level 3**.

## Limitations and CoolSolve gaps

Re-check C-451 (CoolSolve `0.4.0@9768373`), gaps of the gas native file, each with a
minimal run on this build:

- `CS-GAP-COLEBROOK` closed: `Re = 1e5` ⏎ `RR = 0.0005` ⏎ `CALL Colebrook(Re, RR, f)` gives `f` = 2.0327e-02.
- `CS-GAP-ARRAY-ARG` closed: a `PROCEDURE S3(R$,SP[1..3]:y)` called with `SP[1..3]` gives `y` = 6.
- `CS-BUG-PI-FUNCTION` closed: `A = pi/4*d^2` in a `PROCEDURE` body gives 3.14159 for `d` = 2.
- `CS-BUG-IMPLICIT-PROC` closed (no implicit statement remains in the native bodies; one in a
  body is now a parse error naming the line).
- `CS-GAP-ACCENTED-IDENT` closed (the `°` identifiers of the native file parse).
- `CS-GAP-STRINGPOS` still not implemented (`i = StringPos('ø', s$)` gives *Unknown or
  unsupported function: stringpos with 2 arguments*); maintainer decision 2026-10-12: the model is
  rewritten (see conversion log), so it is not listed in `missing_features`.

The liquid-line native file (variant above) is still blocked by `CS-GAP-STRINGPOS` and by the
registered `CS-GAP-PROP-HQ` (`Pressure(R134a,h=h,X=0)` inside a `PROCEDURE`: *CoolProp returned
invalid result ... H=200013 J/kg, Q=0*, reproduced with a 6-line model); its runnable variant is
verified. Both are evidence rows in the register.

Physical limitations, as in the original: `alpha_o` fixed at 10 W/m²-K,
roughness 0.046 mm table value over the pipe data (`epsilon` = 4.6e-5 m),
the nozzle equation identifies `A` rather than predicting a flow.

## Related models

- CSL-0018 `pipe_pressure_drop_colebrook` (plain Colebrook exercise; source
  of the explicit Colebrook-White form formerly used in the gas variant).
- `CSL-0130` `pipe_pressure_drop_correlations` (six explicit single-phase
  friction factors and the two-phase pipe pressure drops; the Colebrook-White
  factor of this file could be replaced by any of them).
- `CSL-0316` *local_losses_idelchik_elbows* (function library): Reynolds- and
  geometry-dependent loss coefficient of a bend, instead of the fixed `K` of the
  fittings table used here.

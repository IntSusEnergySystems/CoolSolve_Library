# Reciprocating compressor from catalogue data (R717)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0157`

Catalogue-data model of an R717 (ammonia) reciprocating compressor, from the
2002 Laborelec compressor toolkit of the ULiège Thermodynamics Laboratory: the
manufacturer rows (condensing/evaporating temperature, capacity, electrical
power, mass flow, 17 operating points) are read from a lookup table and turned
into the global isentropic and volumetric effectiveness versus pressure ratio,
with a power-law extrapolation of the isentropic effectiveness to 1000 and
750 rpm.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R717 (ammonia) |
| **Size** | 399 equations (largest block: 1; 1 `DUPLICATE` loop over the 17 catalogue rows) |
| **Source** | ULiège — Laborelec compressor toolkit 2002 (`Catalogue_data_model-RPM_simulation-Part_speed-Full_load.EES`, EES 6.596) |
| **Authors** | Felipe Trebilcock (ULiège Thermodynamics Laboratory); reviewers J. Lebrun, E. Winandy |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file blocked (`CS-BUG-DUPLICATE-VAR-BOUND`, `CS-GAP-LOOKUP-NONAME`); the runnable variant is verified against the EES stored solution |

## Problem statement

The catalogue (compressor selection software) gives, for 17 operating points
(condensing 30/40/50 °C × evaporating +15…−15 °C), the capacity (36–146 kW),
the electrical power (11–21 kW) and the mass flow rate (0.033–0.127 kg/s) of
an R717 reciprocating compressor at 1450 rpm with 5.001 K of superheating.
Given the swept volume (0.0009712 m³), the model computes, for each point:

- the isentropic effectiveness $\varepsilon_s = w_s / w_{mes}$ with
  $w_s = h_{exs} - h_{su}$ the isentropic specific work and
  $w_{mes} = \dot W_{el}/\dot m$ the measured specific work;
- the volumetric effectiveness
  $\varepsilon_v = \dot V_{su}/\dot V_{sw}$ with $\dot V_{su} = \dot m\,v_{su}$
  and $\dot V_{sw} = V_s\,N$ the displaced flow;
- the pressure ratio $r_p = p_{cd}/p_{ev}$ (saturation pressures);
- the isentropic effectiveness extrapolated to 1000 and 750 rpm with the
  power law $\varepsilon_s(N) = \varepsilon_s \cdot (1450/N)^{0.18}$.

## Model

The 17 catalogue rows are read with `lookup` (columns: `T_cd`, `T_ev`,
`Q_dot_ev`, `W_dot_el`, `M_dot_man`); every equation is an explicit assignment
inside one `DUPLICATE` loop, so the system is a square block of 399 explicit
equations. Fluid states are evaluated on real-fluid R717 properties
(`enthalpy`, `entropy`, `volume`, saturation `pressure` at the catalogue
temperatures). This is the *simulation* member (RPM/part-load maps) of a
5-file family (RPM simulation, full-load and part-load identification,
Copeland scroll big/small — inventory group DG-0066): the effectiveness
polynomials they identify are fitted with the expression noted in the file,
`epsilon_s_cp_mes[i] = a0 + a1*(R_p_cp[i]-7)^2 + a2/(R_p_cp[i]-a3)` (the
coefficients are not defined in this file).

## How to run

The native file keeps the original EES syntax and is **blocked**; run the
variant (valid EES as well, no CoolSolve-only syntax):

```bash
coolsolve ./reciprocating_catalogue_r717_coolsolve.eescode
```

Both files are accompanied by their lookup table (`reciprocating_catalogue_r717-lookup_1.csv`
for the native file, `reciprocating_catalogue_r717_coolsolve-lookup_1.csv`
for the variant; identical SI values). The variant is regression-tested as
`CSL-0157:coolsolve`.

## Results

Effectiveness map computed by the variant (extract of its `.sol` baseline;
all values agree with the EES stored solution to the tolerances of
*Verification*):

| Row | T_cd [°C] | T_ev [°C] | r_p [-] | ε_s [-] | ε_v [-] | ε_s @1000 rpm [-] | ε_s @750 rpm [-] |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 30 | 15 | 1.602 | 0.7454 | 0.9693 | 0.7970 | 0.8393 |
| 6 | 30 | −10 | 4.014 | 0.7472 | 0.7994 | 0.7989 | 0.8413 |
| 8 | 40 | 15 | 2.135 | 0.8388 | 0.9459 | 0.8968 | 0.9445 |
| 14 | 50 | 15 | 2.792 | 0.8552 | 0.9184 | 0.9144 | 0.9630 |

The volumetric effectiveness decreases with pressure ratio (0.969 at r_p 1.60
down to 0.799 at r_p 4.01 within the T_cd = 30 °C family); the isentropic
effectiveness spans 0.713 (r_p 4.94, the 30 °C / −15 °C point) to 0.855
(50 °C / 15 °C). The speed correction raises ε_s by 6.9 % at 1000 rpm and
12.6 % at 750 rpm ((1450/1000)^0.18 = 1.069, (1450/750)^0.18 = 1.126); the
two extrapolated curves are outputs of the file's own law — no measured
1000/750 rpm data are present in this file.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): epsilon_s and
     epsilon_v versus pressure ratio (parametric plot over the 17 catalogue points),
     figures/reciprocating_catalogue_r717_effectiveness.png -->

## Verification

The variant is verified against the **EES stored solution** of the source file
(645 variables stored, all valid; 381 are variables of the active model — the
string `fluid$`, the loop index and 261 stale records of commented-out
equations are not part of it). Unit conversion of the reference: the file is
in kPa/kJ, so pressures and specific energies are compared ×1000 (pressures
and enthalpies; the 42 stored unit tags, all `kW`, are stale — the one on
`M_dot_cp_mes` contradicts its values and was corrected, see conversion log).

`python3 tools/compare_solution.py … : 381 common variables, 51 differ
(rtol=0.001); only in EES: 0; only in CoolSolve: 18` — max. rel. diff. 9.07e-02
(on `h_su_cp[7]`).

- The 51 differing variables are exactly the **absolute enthalpies and
  entropies** (`h_exs_cp`, `h_su_cp`, `s_su_cp`): a pure reference-state
  offset EES vs CoolProp for R717 (h: +145.1…+145.5 kJ/kg; s:
  +482.2…+482.9 J/kg-K), as allowed by the CoolSolve verification policy —
  differences and derived results are compared instead.
- All 330 derived results (effectiveness, specific works, pressure ratios,
  volumes, saturation pressures/temperatures, speeds) pass the tolerance
  (worst 9.96·10⁻⁴ on `V_dot_su_cp_mes[1]`), within the 0.1 % real-fluid
  property tolerance (EES 6.596 vs CoolProp ammonia).
- `t_su_cp[i]` has no stored EES value; checked by hand (20.001 °C =
  T_ev + 5.001 K).

The native file cannot be verified: CoolSolve drops its `DUPLICATE` loop
(silently reducing it to the 8 constant assignments, *SUCCESS*) and rejects
its nameless `lookup` calls.

## Source and attribution

Laborelec compressor toolkit, December 2002, by **Felipe Trebilcock**
(ULiège Thermodynamics Laboratory), reviewed by J. Lebrun and E. Winandy
(authors from the collection inventory; the file header carries no name).
Source file (EES 6.596), collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/1_Compressors/1_1_Reciprocating Compressors/Catalogue_data_model-RPM_simulation-Part_speed-Full_load.EES`
(inventory candidate `TM-0282`, duplicate group DG-0066).

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`): unit system
  `$UnitSystem SI MASS DEG KPA C KJ` → converted by hand to SI-°C-Pa-J. The
  only quantities carrying the kPa/kJ units are the catalogue table (powers
  and capacity kW → W; mass flows kg/s, temperatures °C unchanged), the
  saturation pressures and the specific energies/entropies returned by the
  property calls — the equations are homogeneous and stay unchanged; the
  pressure ratio, effectiveness, speeds and `DELTAT_oh = 5.001 [K]` are
  unchanged. Input values kept: `V_s_cp = 0.0009712 [m^3]`, `rpm_cp = 1450`,
  `rpm2 = 1000`, `rpm3 = 750`, `m = 0.18`.
- **2026-10-08 — recovery of the lookup table.** `ees_extract.py` decoded
  **no** embedded table although the equations call `lookup(i, 1…5)` with
  `n = 17` rows. The table was decoded by hand from the binary (80-bit
  Extended floats, `docs/ees_import.md` §13): the file contains **three
  copies** of a 5-column table (`T_cd`, `T_ev`, `Q_dot_ev`, `W_dot_el`,
  `M_dot_man` — the model reads columns 1, 2, 4, 5; column 3 belongs to the
  commented-out `Q_dot_ev[i]=lookup(i,3)`). The first copy matches the EES
  stored solution on all 85 cells (max. rel. diff. < 10⁻⁷ after kW → W); the
  two other copies disagree on `Q_dot_ev`/`W_dot_el`/`M_dot_man` and are
  stale (earlier data), so the first copy was shipped. The original table
  name is not recoverable from the binary; the EES default-name convention
  `lookup 1` → `lookup_1` is used.
- **2026-10-08 — comment corrections** (comments only): the original unit
  tag `[kW]` on `M_dot_cp_mes` (and the stale EES unit record `kW`) is wrong —
  the values are kg/s (w_mes = 86.9 kJ/kg matches the R717 isentropic work at
  r_p 1.6); the comment now says [kg/s]. The commented-out condenser/evaporator
  block (an alternative `Q_dot_ev` from the cycle with `DELTAT_sc = 0.001`)
  is summarised in a note at the end of the file: under the EES rule that
  brace comments do not nest, the `{` at its second line is comment text and
  the `}` of `Q_dot_cd[i]=…}` closes the whole block — CoolSolve parses it the
  same way, so none of its equations is active, and the stored `DELTAT_sc`/
  `T_ex_cd`/`Q_dot_ev` values are stale records of an earlier version of the
  file. Comments translated to English; standard header added.
- **2026-10-08 — runnable variant** `reciprocating_catalogue_r717_coolsolve.eescode`:
  only the two gap-forced changes — `DUPLICATE i = 1, n` → `DUPLICATE i = 1, 17`
  (`n = 17` kept, unused) and nameless `lookup(i, col)` →
  `lookup('lookup_1', i, col)`; both original forms are valid EES. No
  CoolSolve-only syntax. Verified against the same EES reference (above).
- **Level** (taxonomy §3): equations 399 → 2; largest block 1 → 0;
  functions/arrays/`DUPLICATE` present → 1; multi-zone/≥3 components no → 0;
  semi-empirical/part-load (catalogue maps, speed extrapolation) → 1;
  curated guesses no → 0. Score 4 → **level 3**.

## Limitations and CoolSolve gaps

- `CS-BUG-DUPLICATE-VAR-BOUND`: a `DUPLICATE` loop whose bounds are variables
  (`duplicate i = 1, n`, valid EES, used here) is **silently dropped** — the
  native file *solves* with only its 8 constant equations and *SUCCESS*,
  computing nothing. Blocks the native file.
- `CS-GAP-LOOKUP-NONAME`: the nameless catalogue form `lookup(row, col)`
  (valid EES; EES reads its default "Lookup Table #1" — the stored solution of
  this file proves it) is rejected with *"Expression is not a string literal
  or variable"*. Blocks the native file.
- The catalogue rows and `V_s_cp` come from the original file; the compressor
  model/displacement they refer to is not documented further in the source.
- Physical: the speed extrapolation is the file's own power law (no measured
  1000/750 rpm data in this file); the effectiveness is a *global*
  (electrical → isentropic) effectiveness, as in the original.

## Related models

- `CSL-0123` *copeland_catalogue_correlation*: the ARI/Copeland catalogue
  polynomial correlation — same catalogue-data approach for the Copeland
  scroll members of this 5-file family (TM-0288/TM-0289).
- `CSL-0035` *centrifugal_compressor_lookup_map*: compressor performance read
  from a lookup table (the native `INTERPOLATE` map form, also blocked by its
  lookup gap, with a runnable variant).

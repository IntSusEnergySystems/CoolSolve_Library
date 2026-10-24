# Screw compressor from catalogue data (Grasso C-52, R717)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0269`

Catalogue-data model of an R717 (ammonia) Grasso C-52 screw compressor, from
the 2002 Laborelec compressor toolkit of the ULiège Thermodynamics Laboratory:
the manufacturer rows (condensing/evaporating temperature, evaporator
capacity, electrical power — 24 operating points at 2940 rpm) are read from a
lookup table and turned into the global isentropic and volumetric
effectiveness versus pressure ratio, with a part-load correction at
PLF = 0.42. The manufacturer mass flow is an *output*: it follows from the
catalogue capacity and the evaporator energy balance.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R717 (ammonia) |
| **Size** | 681 equations (largest block: 1; 1 `DUPLICATE` loop over the 24 catalogue rows) |
| **Source** | ULiège — Laborelec compressor toolkit 2002 (`Catalogue_data_model-Grasso C-52 - 2490rpm.EES`, EES 6.596) |
| **Authors** | Felipe Trebilcock (ULiège Thermodynamics Laboratory); reviewers J. Lebrun, E. Winandy |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see *Verification*) |

## Problem statement

This file is a manufacturer catalogue model, not an examination problem. The
catalogue (compressor selection software) gives, for 24 operating points
(condensing 20/25/30/35/40 °C × evaporating −20…+5 °C), the evaporator
capacity (91.6–252.8 kW) and the electrical power (24.6–45.1 kW) of a Grasso
C-52 screw compressor at 2940 rpm with 5.001 K of superheating. Given the
swept volume (0.0013095 m³), the model computes, for each point:

- the isentropic effectiveness $\varepsilon_s = w_s / w_{mes}$ with
  $w_s = h_{exs} - h_{su}$ the isentropic specific work and
  $w_{mes} = \dot W_{el}/\dot m$ the measured specific work;
- the volumetric effectiveness
  $\varepsilon_v = \dot V_{su}/\dot V_{sw}$ with $\dot V_{su} = \dot m\,v_{su}$
  and $\dot V_{sw} = V_s\,N$ the displaced flow;
- the pressure ratio $r_p = p_{cd}/p_{ev}$ (saturation pressures);
- the part-load effectivenesses $\varepsilon_{s,pl}$ and
  $\varepsilon_{v,pl}$ at the part-load factor PLF = 0.42, as in the original:
  $\varepsilon_{s,pl} = \varepsilon_s(0.463 + 1.5255\,\mathrm{PLF} -
  1.607\,\mathrm{PLF}^2 + 0.62\,\mathrm{PLF}^3)$ and
  $\varepsilon_{v,pl} = \varepsilon_v\,\mathrm{PLF}^{mm}$ with $mm = 1$.

The file name says *2490 rpm*; the equation window (and the stored solution)
use `rpm_cp = 2940`, which is kept as in the original.

## Model

The 24 catalogue rows are read with the nameless `lookup(row, col)` form
(columns: `T_cd`, `T_ev`, `Q_dot_ev`, `W_dot_el`, `M_dot_man`); every
equation is an explicit assignment inside one `DUPLICATE` loop, so the system
is a square block of 681 explicit equations (CoolSolve reports *System
square: Yes*). Fluid states are evaluated on real-fluid R717 properties
(`enthalpy`, `entropy`, `volume`, saturation `pressure` at the catalogue
temperatures). This is the *screw compressor* member of the Laborelec
catalogue family, a sibling of the reciprocating model `CSL-0157`: the
structure is the same, but here the condenser/evaporator states of the cycle
are active (`T_ex_cd = T_cd - DELTAT_sc`), the catalogue mass-flow read is
commented out and `M_dot_cp[i]` is *computed* from the catalogue capacity via
the evaporator balance $Q_{ev} = \dot m (h_{su,cp} - h_{ex,cd})$. The commented
block at the end of the file notes the effectiveness polynomials the original
lists for this machine at 100 % down to 10 % of the load (a fit of the same
catalogue; the active model reads the rows themselves):

```
100% - epsilon_s_cp_mes[i] = 0.908801447+0.0162294137*(R_p_cp[i]-6.57616267)^2-0.949659513/(R_p_cp[i]-0.317276836)
 90% - epsilon_s_cp_mes[i] = 1.11854216+0.0293495143*(R_p_cp[i]-6.5)^2-2.45637349/(R_p_cp[i]+0.332172541)
 80% - epsilon_s_cp_mes[i] = 0.953178285+0.0210993042*(R_p_cp[i]-6.5)^2-1.39259111/(R_p_cp[i]-0.0704693372)
 70% - epsilon_s_cp_mes[i] = 0.759746868+0.0128014614*(R_p_cp[i]-5.5)^2-0.221619404/(R_p_cp[i]-1.179485)
 60% - epsilon_s_cp_mes[i] = 0.741861794+0.0170065482*(R_p_cp[i]-5.5)^2-0.27915589/(R_p_cp[i]-1.12540103)
 50% - epsilon_s_cp_mes[i] = 0.686952869+0.0176116612*(R_p_cp[i]-5.5)^2-0.241899372/(R_p_cp[i]-1.16016232)
 40% - epsilon_s_cp_mes[i] = 0.498952067+0.00323*(R_p_cp[i]-10.2053)^2-0.091282/(R_p_cp[i]-1.35176498)
 30% - epsilon_s_cp_mes[i] = 0.621613235+0.0199924143*(R_p_cp[i]-6.5)^2-0.937602889/(R_p_cp[i]-0.198193895)
 20% - epsilon_s_cp_mes[i] = 0.620480251+0.0248703698*(R_p_cp[i]-6.5)^2-1.84383447/(R_p_cp[i]+0.622866984)
 10% - epsilon_s_cp_mes[i] = 0.348275018+0.0140081228*(R_p_cp[i]-6.5)^2-1.11250311/(R_p_cp[i]+1.07942061)
100 % - EPSILON_S_CP_MES[I] = 0.77+0.00670689929*(R_p_cp[i]-7)^2-0.225766017/(R_p_cp[i]-1.11750968)
100% - epsilon_v_cp_mes[i] = 0.865229152 - 0.011508488*R_p_cp[i]
 90% - epsilon_v_cp_mes[i] = 0.77862087 - 0.0103469939*R_p_cp[i]
 80% - epsilon_v_cp_mes[i] = 0.692175833 - 0.00919468881*R_p_cp[i]
 70% - epsilon_v_cp_mes[i] = 0.605775096 - 0.0080909136*R_p_cp[i]
 60% - epsilon_v_cp_mes[i] = 0.519068091 - 0.00687731255*R_p_cp[i]
 50% - epsilon_v_cp_mes[i] = 0.43268267 - 0.00573832804*R_p_cp[i]
 40% - epsilon_v_cp_mes[i] = 0.346161061 - 0.00463117546*R_p_cp[i]
 30% - epsilon_v_cp_mes[i] = 0.259393613 - 0.00338794169*R_p_cp[i]
 20% - epsilon_v_cp_mes[i] = 0.173053318 - 0.0023137992*R_p_cp[i]
 10% - epsilon_v_cp_mes[i] = 0.0865478394 - 0.00113186141*R_p_cp[i]
```

## How to run

```bash
coolsolve ./grasso_screw_catalogue_r717.eescode
```

The catalogue rows are read from the lookup table
`grasso_screw_catalogue_r717-lookup_1.csv` (nameless `lookup(row, col)` form:
EES's default *Lookup Table #1*); the loop bound `n = 24` is a variable, as in
the original. No `.initials` file is needed: all equations are explicit and
the default guesses converge in 48 iterations.

## Results

Effectiveness map computed by the model (extract of its `.sol` baseline; all
values agree with the EES stored solution to the tolerances of *Verification*):

| Row | T_cd [°C] | T_ev [°C] | r_p [-] | ε_s [-] | ε_v [-] | M_dot [kg/s] | Q_dot_ev [kW] | W_dot_el [kW] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 20 | −20 | 4.510 | 0.7235 | 0.8117 | 0.0816 | 94.3 | 24.6 |
| 6 | 25 | −20 | 5.277 | 0.7194 | 0.8051 | 0.0809 | 91.6 | 27.6 |
| 8 | 25 | −10 | 3.450 | 0.7599 | 0.8269 | 0.1239 | 141.9 | 29.0 |
| 11 | 25 | +5 | 1.945 | 0.6715 | 0.8439 | 0.2173 | 252.8 | 29.8 |
| 16 | 30 | +5 | 2.263 | 0.7173 | 0.8382 | 0.2159 | 245.9 | 34.6 |
| 21 | 40 | −10 | 5.349 | 0.7408 | 0.8060 | 0.1208 | 129.5 | 41.3 |
| 24 | 40 | +5 | 3.015 | 0.7580 | 0.8270 | 0.2130 | 232.2 | 45.1 |

Across the 24 points the pressure ratio spans 1.94–5.35, the isentropic
effectiveness 0.672 (row 11, the mildest pressure ratio and highest
condensing temperature) to 0.766 (row 23) and the volumetric effectiveness
0.805 (row 6) to 0.847 (row 5). The part-load factor PLF = 0.42 multiplies
ε_s by 0.463 + 1.5255·0.42 − 1.607·0.42² + 0.62·0.42³ = 0.8662 and ε_v by
PLF^mm = 0.42 (mm = 1).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): effectiveness
     versus pressure ratio over the 24 catalogue points (parametric plot),
     figures/grasso_screw_catalogue_r717_effectiveness.png -->

## Verification

The model is verified against the **EES stored solution** of the source file
(701 variables stored; 656 are variables of the active model). Unit
conversion of the reference: the file is in kPa/kJ, so pressures
(`P_cd`, `P_ev`, `p_su_cp`, `p_ex_cp`), specific energies and entropies
(`h_*`, `w_*`, `s_su_cp`) and the two power columns of the catalogue table
(kW → W) are compared ×1000; temperatures, volume flows, effectiveness and
speeds are unchanged. The comparison was made with a reference CSV converted
by hand from `reference/ees_variables.csv` (the stored unit tags, all `kW`,
cover only `Q_dot_ev` and the stale `M_dot_cp_mes`).

`python3 tools/compare_solution.py … : 656 common variables, 144 differ
(rtol=0.001); only in EES: 45; only in CoolSolve: 25` — max. rel. diff. 0.331
(on `h_ex_cd[1]`).

- The 144 differing variables are exactly the **absolute enthalpies and
  entropies** (`h_ex_cd`, `h_ex_ev`, `h_exs_cp`, `h_su_cp`, `h_su_ev`,
  `s_su_cp`): a pure reference-state offset CoolProp − EES for R717
  (h: +145.12…+145.53 kJ/kg; s: +482.2…+482.5 J/kg-K), as allowed by the
  CoolSolve verification policy — differences and derived results are
  compared instead.
- All 512 derived results (effectiveness, specific works, pressure ratios,
  volume flows, saturation pressures, mass flows, capacities, part-load
  effectivenesses) pass the tolerance (worst 9.51·10⁻⁴ on
  `epsilon_v_cp_mes[11]`), within the 0.1 % real-fluid property tolerance
  (EES 6.596 vs CoolProp ammonia).
- Only in EES: the stale records `M_dot_cp_mes[1..25]` (the commented-out
  `M_dot_cp_mes[i]=lookup(i,5)`), the index-25 records of 16 array variables
  (the file once had `n = 25`) and the loop index `i`.
- Only in CoolSolve: `fluid$` (a string, absent from the numeric reference)
  and `t_su_cp[1..24]`, which the EES stored solution does not contain;
  checked by hand (t_su_cp = T_ev + 5.001 K, e.g. row 1: −20 + 5.001 =
  −14.999 °C).

## Source and attribution

Laborelec compressor toolkit, December 2002, by **Felipe Trebilcock**
(ULiège Thermodynamics Laboratory), reviewed by J. Lebrun and E. Winandy
(authors from the collection inventory; the file header carries no name).
Source file (EES 6.596), collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/1_Compressors/1_2_Screw Compressors/Catalogue_data_model-Grasso C-52 - 2490rpm.EES`
(inventory candidate `TM-0284`, duplicate group DG-0067 with the Grasso N-5
and S-51 files, which differ only in the machine data).

## Conversion log

- **2026-10-22 — import** (`tools/ees_extract.py`): unit system
  `$UnitSystem SI MASS DEG KPA C KJ` → converted by hand to SI-°C-Pa-J. The
  only quantities carrying the kPa/kJ units are the catalogue table (capacity
  and electrical power kW → W; temperatures °C unchanged), the saturation
  pressures and the specific energies/entropies returned by the property
  calls — the equations are homogeneous and stay unchanged; the pressure
  ratio, effectiveness, speeds, `DELTAT_oh = 5.001 [K]`,
  `DELTAT_sc = 0.001 [K]` and `PLF = 0.42` are unchanged. Input values kept:
  `V_s_cp = 0.0013095 [m^3]`, `rpm_cp = 2940`, `nn = 0.15` (unused in the
  active equations, as in the original), `mm = 1`.
- **2026-10-22 — recovery of the lookup table.** `ees_extract.py` decoded
  **no** embedded table although the equations call `lookup(i, 1…4)` with
  `n = 24` rows. The table was decoded by hand from the binary (80-bit
  Extended floats, `docs/ees_import.md` §13): the file contains one
  consistent 5-column table (`T_cd`, `T_ev`, `Q_dot_ev`, `W_dot_el`,
  `M_dot_man`; the model reads columns 1–4, column 5 belongs to the
  commented-out `M_dot_cp_mes[i]=lookup(i,5)`); later byte patterns that
  start like the first column are not decodable copies (stale fragments).
  The first copy matches the EES stored solution **exactly** on all 120
  cells of the four read columns (max. rel. diff. 0 before the kW → W
  conversion). The original table name is not recoverable from the binary;
  the EES default-name convention `lookup 1` → `lookup_1` is used.
- **2026-10-22 — comment curation** (comments only): the original's
  multi-line `"` comment holding the effectiveness polynomials is reproduced
  as a note at the end of the file (each line its own comment; the full list
  is above and in the original); the brace comments (`{M_dot_cp_mes[i]=…}`,
  the condenser block `{h_su_cd[i]=h_ex_cp[i]; …}` referring to the undefined
  `h_ex_cp`) are summarised in the same note — under the EES rule that brace
  comments do not nest, none of their equations is active, and the stored
  `M_dot_cp_mes` values are stale records of that earlier version. Comments
  translated to English; standard header added; units annotated in SI.
- **Level** (taxonomy §3): equations 681 → 2; largest block 1 → 0;
  functions/arrays/`DUPLICATE` present → 1; multi-zone/≥3 coupled components
  no → 0; semi-empirical/part-load (catalogue map, PLF correction) → 1;
  curated guesses no → 0. Score 4 → **level 3**.

## Limitations and CoolSolve gaps

- The catalogue rows and `V_s_cp` refer to a Grasso C-52 whose model and
  displacement are not documented further in the source; the file name
  (2490 rpm) disagrees with the equation window (2940 rpm) — the latter is
  used, as in the original.
- Physical: the part-load correction is the original's empirical polynomial
  in PLF (no part-load measurement in this file); the effectiveness is a
  *global* (electrical → isentropic) effectiveness, as in the original; the
  100 %–10 % polynomials in the end note are the file's own fits of the same
  catalogue and are not evaluated by the model.
- No CoolSolve gap blocks the model (`ees_extract.py` not finding the
  embedded table is `CS-BUG-EXTRACT-LOOKUP-STRING`-family tooling behaviour;
  the table is shipped decoded, no model gap).

## Related models

- `CSL-0157` *reciprocating_catalogue_r717*: same toolkit and structure for
  the R717 reciprocating family (DG-0066) — there the catalogue mass flow is
  read from the table and the evaporator balance is commented out; here the
  two are swapped and a part-load correction is added.
- `CSL-0245` *grasso_screw_rpm_efficiencies*: the toolkit example that
  evaluates the polynomial isentropic efficiencies of the same four Grasso
  screw machines (including C-52) and scales them from 2940 to 1500 rpm.

# Turbocharger matching with combustion-product composition

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0152`

Steady-state matching of a turbocharger on a supercharged engine (simplified
formulation of P. Ngendakumana): ambient air drawn through the filter is
compressed (given pressure ratio and isentropic efficiency), cooled in an
intercooler (epsilon-NTU on a glycol-water loop), and the engine burns fuel at
the given air-fuel ratio; a fraction `k` of the fuel energy is carried by the
exhaust gas, whose enthalpy and entropy are computed from the molar
composition of the complete-combustion products (excess air, simplified dry
air 79 % N2 / 21 % O2, ideal-gas CO2/H2O/O2/N2 with formation enthalpies).
The turbine is matched on the compressor through the shaft power balance, and
the model computes the equivalent exhaust-orifice diameter and the heat
recovered as a percentage of the fuel energy.

| | |
|---|---|
| **Category** | Components › Compressors (turbocharger compressor–turbine matching) |
| **Fluids** | Air (compressor–intercooler–engine), EG 40 % (glycol-water loop), ideal-gas CO2, H2O, O2, N2 (exhaust products) |
| **Size** | 219 equations, largest block 10 (runnable variant; the native file does not parse in CoolSolve, see *Limitations*) |
| **Source** | ULiège — MCI course, TP4 exercise 1 (EES file `SURALIMENTATION_FORMULATION SIMPLE_V2017-1.EES`, "formulation simplifiée", PNG 24/03/2019) |
| **Authors** | P. Ngendakumana (ULiège Thermodynamics Laboratory); R. Dickes (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@7addbbc — native file **blocked** (4 gaps, see below); runnable variant `turbocharger_combustion_products_coolsolve.eescode` verified against the EES stored solution |

## Model

One operating point, all default values of the original:

| Input | Value | Input | Value |
|---|---|---|---|
| `r_p_c` compressor pressure ratio | 2.16 | `AFR` air-fuel ratio | 20 |
| `epsilon_s_c` compressor isentropic eff. | 0.70 | `k` fraction of fuel energy to exhaust | 1/3 |
| `Filtre` filter pressure drop | 50 mm H2O | `C_pc` mass fraction of C in the fuel | 86.9 % |
| `epsilon_hex` intercooler effectiveness | 0.80 | `LHV_f` fuel LHV | 43 MJ/kg |
| `M_dot_a` / `M_dot_w` air / glycol-water flow | 0.045 / 0.025 kg/s | `epsilon_s_e` turbine isentropic eff. | 0.70 |
| `Conc` glycol concentration | 40 % | `eta_m_e` turbine mechanical eff. | 0.85 |

The combustion-products properties (enthalpy, entropy, molar mass) come from
the subprogram `HSCmHnPRODCOMB_PNG030110` of the original, flattened into the
main program (decision D10), and from `FUNCTION mm_p`. The turbine is sized by
the power balance `w_c = -w_e*(1+f)*eta_m_e`, the intake state follows from the
isentropic relation `s_p_su_e = s_p_ex_e_s`, and the exhaust line is
represented by an equivalent orifice (`M_dot_p = A_eq_e*rho_ex_e*C_ex_e` with
`C_ex_e^2/2 = -w_e`).

## How to run

```bash
coolsolve ./turbocharger_combustion_products_coolsolve.eescode
```

The native file `turbocharger_combustion_products.eescode` is the faithful
transcription (valid EES, SUBPROGRAM flattened); it does not parse in
CoolSolve (see *Limitations*).

## Results (runnable variant, default operating point)

| Quantity | Value | Quantity | Value |
|---|---:|---|---:|
| `p_a_ex_c` compressor outlet | 2.149 bar | `T_p_su_e` exhaust at turbine inlet | 636.3 °C |
| `w_c` / `w_c_s` compressor work | 103.8 / 72.6 kJ/kg | `T_p_ex_e` exhaust at turbine outlet | 539.3 °C |
| `T_a_ex_c` compressor outlet temp. | 123.0 °C | `w_e` / `w_e_s` turbine work | -116.3 / -166.1 kJ/kg |
| `T_a_ex_hex` air after intercooler | 44.6 °C | `p_su_e` / `r_p_e` turbine intake | 2.00 bar / 1.99 |
| `T_w_ex_hex` glycol-water outlet | 64.4 °C | `phi_e` equivalent-orifice diameter | 17.04 mm |
| `e` excess air of the combustion | 0.385 (-) | `C_ex_e` / `C_a` gas velocity / sonic speed | 482 / 554 m/s (subsonic, as in the original) |
| `MM_p` exhaust molar mass | 28.94 kg/kmol | `HR` / `HR_0` heat recovery | 5.63 % of `Q_dot` / 16.9 % of `Q_dot_p` |

Sanity checks of the original verified: `HR_bis = HR` (independent route),
`C_a > C_ex_e` (subsonic), `epsilon_s_c = epsilon_s_e = 0.7` by construction.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep
     suggested by the blocked status (e.g. HR and phi_e vs k), figures/…png -->

## Verification

Against the EES stored solution of the source file (`compare_solution.py`,
runnable variant; the native file does not parse). The EES variable table
holds 111 records, 109 with values (`AU` and `C` are dead variables without
values; the subprogram-internal records `x[i]`, `h[i]`, `s[i]`, `MM[i]`,
`pp[i]`, `temp`, `pres`, `f_st`, `e`, `ntkmol`, `h_p`, `s_p` are the state of
the last subprogram execution, i.e. the `ref` call at 25 °C / 1 bar).

- 82 common variables (`compare_solution.py`, rtol = 0.001): the 50 passing
  include `T_p_su_e` 636.14 / 636.27 °C, `p_a_ex_c` 214 941 Pa (1.8e-7),
  `Q_dot_p` 32 544.5 / 32 545.9 W, `HR` 5.612 / 5.627 %, `phi_e`
  17.054 / 17.040 mm, `MM_p` 28.9364 / 28.9367 kg/kmol, `rho_ex_e`, `c_w`,
  `c_p_a_c`, `gamma_a_c`… 12 further physical results sit at 1.1e-3 – 4.5e-3
  (maximum `Q_dot_2` = 4.51e-3, an air-enthalpy difference over 19.6 K; also
  `w_c`/`w_c_s`/`w_e`/`w_e_s` at 2.79e-3, `Q_dot_hex`, `C_dot_h`/`C_dot_min`,
  `C_ex_e`, `c_p_a_hex`, `c_p_p_e`, `c_v_p_e`) — property-backend
  differences (EES 10.589 vs CoolProp) within the ≤ 0.5 % tolerance.
- Absolute enthalpies/entropies of `Air` (`h_a_*`, `s_a_*`) and of the
  products (`s_m_su_e`, `s_p_ex_e`, `s_p_ref`, `s_ref[i]`) differ by the
  reference-state offsets of the two backends; all differences agree (e.g.
  compressor Δh 103 487 / 103 776 J/kg). `CS-GAP-AIR-ENTHALPY-REF` documents
  the Air offset; it does not block this model (differences only).
- **8 stored values are stale** (a mix of older EES sessions, cf.
  `CS-BUG-EXTRACT-STALE`) and cannot be reproduced by the file's own
  equations: `h_p_ref`, `h_p_su_e`, `h_p_ex_e`, `h_p_ex_e_s` carry a constant
  offset of -82.87 MJ/kg w.r.t. the file's own subprogram evaluated with the
  species enthalpies stored in the same file (`h[1]` = -8 940 832 J/kg at
  25 °C gives `h_p` = -2 104 110 J/kg at 25 °C, the value CoolSolve finds;
  all four stored differences are correct and match CoolSolve within 4e-5);
  `s_p_ex_e_s` and `s_p_su_e` (65 073.58 J/kg-K) are off the scale of the
  same file's `s_p_ex_e` (8 055.08) for nearly identical states; `p_su_e`
  (1.027 bar) and `r_p_e` (1.024) contradict the stored `w_e_s`
  (-165 645 J/kg needs ≈ 2 bar). CoolSolve computes the physically consistent
  values (`p_su_e` = 2.00 bar, `r_p_e` = 1.99, `T_pp_su_e` = 636.3 °C — no
  stored value).
- The stored subprogram state (ref call) is reproduced under the flattened
  names: `x_ref[i]` / `MM_ref[i]` / `pp_ref[i]` / `h_ref[i]` / `f_st_ref` /
  `e_ref` / `ntkmol_ref` / `MM_p_ref` match the stored `x[i]`… within 3e-3
  (composition and partial pressures exact; the small composition deviation
  comes from the element molar masses substituted in the variant).

## Source and attribution

Exercise model of the ULiège **MCI** course (TP4, exercise 1,
supercharging), "formulation simplifiée" dated 24/03/2019 (PNG =
P. Ngendakumana), from the collection shared by R. Dickes (EES licence stamp
of the ULiège Thermodynamics Laboratory). The combustion-products subprogram
is the PNG `HSCmHnPRODCOMB` library routine, embedded in the file (cf.
`CSL-0005` for the same library's cpbar/gamma/mmprod routines).

Source file (EES X10.589, comments in French):
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP4_Ex_1/SURALIMENTATION_FORMULATION SIMPLE_V2017-1.EES`
(inventory candidate `TM-0240`).

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`): unit system already
  SI-°C-Pa-J (no unit conversion). The extractor wrongly reported a decimal-
  comma format and rewrote the ranges `i=1,4` of the five `sum(...)` lines and
  of the `Duplicate` as `i=1.4` (`CS-BUG-EXTRACT-DECIMAL-RANGE`); the ranges
  were restored to `i=1,4` (the raw file is in dot format: `2.16`, `86.9`).
  The dead `$INCLUDE D:\…HSCmHnPRODCOMB_SI_PNG030110.LIB` line was removed:
  the subprogram it points to is embedded in the file itself, and the
  external library is not in the collection. `$TABSTOPS` (GUI setting)
  dropped; EES licence/display tags removed by the extractor; comments
  translated to English; standard header added.
- **Decision D10 — SUBPROGRAM flattened.** `HSCmHnPRODCOMB_PNG030110
  (m,n,f,temp,pres:h_p,s_p)` (molar composition, enthalpy and entropy of the
  products) had five calls, each replaced by a copy of its equations with the
  formal arguments substituted and the internal variables tagged per call:
  `MM→MM_<tag>[i]`, `f_st→f_st_<tag>`, `e→e_<tag>`, `ntkmol→ntkmol_<tag>`,
  `x→x_<tag>[i]`, `MM_p→MM_p_<tag>`, `h→h_<tag>[i]`, `pp→pp_<tag>[i]`,
  `s→s_<tag>[i]`, with

  | Call | Site | Tag | temp → | pres → | h_p → | s_p → |
  |---|---|---|---|---|---|---|
  | 1 | Engine | `_su_e` | `T_p_su_e` | `pres_su_e` | `h_p_su_e` | `s_m_su_e` |
  | 2 | Expander | `_ex_e` | `T_p_ex_e` | `p_ex_e` | `h_p_ex_e` | `s_p_ex_e` |
  | 3 | Expander (isentropic) | `_ex_e_s` | `T_p_ex_e_s` | `p_ex_e` | `h_p_ex_e_s` | `s_p_ex_e_s` |
  | 4 | Expander (intake state) | `_su_e2` | `T_pp_su_e` | `p_su_e` | `h_p_su_e` | `s_p_su_e` |
  | 5 | Heat recovery | `_ref` | `T_ref` | `pres_ref` | `h_p_ref` | `s_p_ref` |

  No name collision with the main program. `FUNCTION mm_p` kept as is.
- **Dead variables** `AU` and `C` of the EES variable table (both without
  stored value) do not appear in the equations; they are not carried over.
- **Level justification** (taxonomy §3): 219 equations (1), largest block 10
  (1), functions + arrays (1), ≥ 3 coupled components (1), off-design
  matching physics (1), curated guesses needed (1) → score 6 → level 3.
- **2026-10-08 — runnable variant** `turbocharger_combustion_products_coolsolve.eescode`
  (only what the four gaps force; still valid EES):
  1. `C%` → `C_pc`, `Q_dot_2_%` → `Q_dot_2_pc` (`CS-GAP-NAME-SYMBOL`);
  2. `molarmass(C)`/`molarmass(H)` → 12.0107 / 1.00794 kg/kmol, the values EES
     returns (recomputed from the stored `m`, `n`) (`CS-GAP-MOLARMASS-ELEMENT`), in
     `FUNCTION mm_p`, in `m`, `n` and in the five `f_st_<tag>` lines;
  3. the 16 indexed sums `sum(expr,i=1,4)` expanded as explicit 4-term sums,
     the terms of `h_p`/`s_p` parenthesised before the `/MM_p_<tag>` division
     (`CS-GAP-SUM-INDEXED`);
  4. `Cp(EG,T=T_bar_w_hex,C=Conc)` → `Cp(EG,T=T_bar_w_hex,P=p_atm,C=Conc)`
     (`CS-GAP-INCOMPRESSIBLE`); no physical effect for an incompressible
     solution (CoolSolve EG 40 % at 44.6 °C: 3615.4 vs EES 3615.1 J/kg-K).
  Verified against the same EES reference (see *Verification*).

## Limitations and CoolSolve gaps

The native file is **blocked** by four registered gaps (`missing_features`):

- `CS-GAP-NAME-SYMBOL` — parse error on `C% = 86.9` and `Q_dot_2_% = …`
  ("Line 76/141: Could not parse line");
- `CS-GAP-SUM-INDEXED` — the 16 indexed `sum(expr,i=1,4)` make the system
  not-square (219 equations / 240 unknowns, no error on the sum lines);
- `CS-GAP-MOLARMASS-ELEMENT` — `molarmass(C)`, `molarmass(H)` ("Unknown
  fluid: 'C'"), registered with this card;
- `CS-GAP-INCOMPRESSIBLE` — `Cp(EG,T=…,C=40)` ("cp requires exactly 2 input
  properties …, got 1"; adding `P=` unblocks the call, CoolSolve has the EG
  solution fluid and agrees with EES within 1e-4).

The stored EES solution mixes stale values from older sessions
(`CS-BUG-EXTRACT-STALE`); the verification above separates the consistent
last run from the 8 stale values. `tools/ees_extract.py` also mangled the
`i=1,4` ranges of this dot-format file (`CS-BUG-EXTRACT-DECIMAL-RANGE`).

## Related models

- `CSL-0005` *cpbar_combustion_products*: the cpbar/gamma/mmprod routines of
  the same ULiège combustion library (the products properties here come from
  the HSCmHnPRODCOMB routine of the same library, embedded in the file).
- `CSL-0150` *adiabatic_flame_dissociation*: same MCI TP collection
  (TP1), combustion products with the EES built-in equilibrium/NASA routines.

# Gas turbine with a chiller on the compressor inlet air

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0294`

Open-cycle Brayton plant (compressor, adiabatic combustion chamber, expander
burning methane in air) whose inlet air at 30 °C is cooled to 20 °C by an R134a
refrigeration machine — a suction chiller on the compressor intake. The
refrigeration cycle (evaporator on the air line, condenser at 45 °C, isentropic
compressor efficiency 0.65, isenthalpic expansion) is coupled to the gas turbine
through the air mass flow: the compressor reduced mass flow is kept at its
nominal value by the inlet cooling, and the model sizes the evaporator UA and
the chiller compressor displacement that achieve it.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines |
| **Fluids** | Air, CH4, R134a (+ N2, O2, CO2, H2O in the copied combustion-product routines) |
| **Size** | 104 equations (largest block: 9; ~78 in the main program, the rest in the copied `cpbar`/`gamma` routines) |
| **Source** | ULiège MSTh repetition R12, exercise 7 (`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 12/MSTH-SB-R12-EX7.EES`) |
| **Authors** | Stéphane Bertagnolio (from the file name `MSTH-SB-R12-EX7`, the ULiège Thermodynamics Lab EES stamp and the inventory authors cell) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified (see verification field) |

## Problem statement

MSTh (MECA0006 *Machines et systèmes thermiques*, ULiège) repetition R12,
exercise 7 (course material, published as an example per the maintainer
decision of `sources/thermo_models/README.md`): a gas turbine takes in air at
30 °C; a refrigeration machine cools the intake to 20 °C. With the nominal
reduced quantities of the machine without chiller
(MR_c_n = 17.41, MR_e_n = 3.625, NR_n = 9.575), compute the plant and size the
chiller. The original's own comments state the follow-up study: vary the
displacement (or speed) of the chiller compressor and observe how the gas
turbine efficiency varies with its inlet temperature.

## Model

Single steady regime, no pressure loss in the combustor, constant isentropic
efficiencies (compressor and expander of the Brayton cycle 0.85, chiller
compressor 0.65), isenthalpic expansion in the chiller, methane LHV
50 MJ/kg, fuel at 20 °C.

- **Chiller (R134a)**: saturation pressures from (T, x) at T_ev = 10 °C and
  T_cd = 45 °C; evaporator duty from the refrigerant side
  `Q_dot_ev = M_dot_r*(h_1-h_4)` and from the air side
  `Q_dot_ev = M_dot_a*cp_a_chiller*(T_chiller_su-T_c_su)`; the ε-NTU relation
  of the evaporator (`epsilon_ev = 1-exp(-NTU_ev)`, equal heat capacities) with
  `NTU_ev = AU_ev/(M_dot_a*cp_a_chiller)` closes the sizing: with the 10 K air
  temperature drop it fixes ε_ev = 0.5, NTU_ev = ln 2 and hence
  `AU_ev = M_dot_a*cp*ln 2`. The chiller compressor displacement follows from
  the inlet volume flow `V_dot_1 = M_dot_r*v_1 = N*V_s` at N = 50 rev/s.
- **Brayton cycle**: air compression and product expansion with the isentropic
  relation written on absolute temperatures (`+273` as in the original),
  `gamma` and the mean specific heats `cpbar` of the ULiège combustion library
  (CmHn fuel, simplified air), combustor energy balance `q_1..q_5` at reference
  25 °C, shaft power `W_dot_sh`, electrical power via η_em = 0.9, efficiencies
  `eta` and `eta_global` (including the chiller power).
- **Reduced quantities**: `NR = N_rot/sqrt(T_c_su+273)`,
  `MR_c = M_dot_a*sqrt(T_c_su+273)/(P_c_su/1e5)`,
  `MR_e = M_dot_p*sqrt(T_e_su+273)/(P_e_su/1e5)`; the equation
  `MR_c = MR_c_n*NR/NR_n` (original comment: the compressor stays choked and
  the turbine speed is not varied) determines the air mass flow of the cooled
  regime.

As in the original, the expander work is `W_dot_e = M_dot_a*w_e` (w_e per kg of
products) and the compressor work `W_dot_c = M_dot_p*w_c` (w_c per kg of air);
the two mass flows differ by the fuel flow f ≈ 0.0165. Kept unchanged.

Inputs: `T_chiller_su`, `T_c_su`, `P_c_su`, `P_c_ex`, `T_e_su`,
`epsilon_c_s`, `epsilon_e_s`, `eta_em`, `T_cd`, `T_ev`,
`epsilon_chiller_s`, `N`, `N_rot`, `LHV_f`, `MR_c_n`, `MR_e_n`, `NR_n`.
Outputs: `W_dot_sh`, `W_dot_el`, `eta`, `eta_global`, `COP_chiller`,
`AU_ev`, `V_s`, `M_dot_a`, `M_dot_r`, `MR_c`, `MR_e`, `NR`.

## How to run

```
coolsolve models/cycles/gas_turbines/gas_turbine_inlet_air_chiller/gas_turbine_inlet_air_chiller.eescode
```

The shipped `.initials` (EES stored solution, R134a h/s shifted to the
CoolProp reference) is convenient but not required: the model converges from
the default guesses (61 iterations). No variants, no `coolsolve.conf`.

## Results

Default operating point (with chiller), CoolSolve vs the EES stored solution:

| Quantity | EES | CoolSolve | Unit |
|---|---:|---:|---|
| `M_dot_a` (air) | 1.03429 | 1.03429 | kg/s |
| `Q_dot_ev` (evaporator / intake cooling) | 10 412 | 10 408 | W |
| `W_dot_cp_chiller` | 2 432.4 | 2 432.0 | W |
| `COP_chiller` | 4.2806 | 4.2796 | – |
| `AU_ev` (sized) | 721.70 | 721.44 | W/K |
| `V_s` (sized displacement) | 7.337e-05 | 7.332e-05 | m3/rev |
| `W_dot_sh` | 242 729 | 242 238 | W |
| `W_dot_el` | 218 457 | 218 014 | W |
| `eta` | 0.28526 | 0.28500 | – |
| `eta_global` (incl. chiller) | 0.28445 | 0.28418 | – |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7) -->
<!-- ![...](figures/gas_turbine_inlet_air_chiller_<type>.png) -->

## Verification

Reference: the EES stored solution of `MSTH-SB-R12-EX7.EES` (78 numeric values,
EES X7.458), compared with `tools/compare_solution.py`:

```
78 common variables, 20 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 26
```

- **Reference-state offsets (excluded from the deviation figure)**: `h_1`,
  `h_2`, `h_2_s`, `h_3`, `h_4` (CoolProp − EES = +148.1 kJ/kg for R134a) and
  `s_1` (+0.796 kJ/kg·K); all R134a uses in the model are differences, so no
  result is affected.
- **Property-backend differences** (CoolProp vs EES Air/CH4): the largest is
  `cp_f` = 8.77e-3 (cp(CH4), same ~1 % as in CSL-0220/CSL-0293), then
  `q_2` 9.84e-3, `cp_a` 2.45e-3, `W_dot_sh`/`W_dot_el` 2.02e-3, `w_c` 1.27e-3,
  `T_c_ex` 1.11e-3, `f`/`M_dot_f`/`Q_dot_c`/`q_3` 1.08e-3.
- **Everything else within 1e-3**, including the sizing outputs: `AU_ev`
  3.67e-4, `V_s` 6.80e-4 (the (P,h) rewrite of `v_1`), `COP_chiller` 2.33e-4,
  `eta` 9.43e-4, `eta_global` 9.45e-4; `M_dot_a` and `NR`/`MR_c` agree to
  9e-11 (fixed by the reduced-quantity equations with data inputs).
- **The 26 names only in CoolSolve**: the 8 unused outputs of the two `cpbar`
  CALLs and the 18 post-processing state-point variables (`T_2`, `T_4`,
  `P_ch[i]`, `h_ch[i]`, `T_ch[i]`, `s_ch[i]`).

Checks: `ees-stored-solution`, `order-of-magnitude`.

## Niche

Nearest library models, by equations:

1. `CSL-0200` *gas_turbine_reduced_quantities* — same single-shaft Brayton core
   (cpbar/gamma, `q_1..q_5` balance, MR/NR relations) but no chiller; this model
   adds the coupled R134a refrigeration cycle and the sizing of the evaporator
   UA and compressor displacement (new topology: two coupled cycles).
2. `CSL-0218`/`CSL-0220` (part-load / any-regime single-shaft gas turbines) —
   same family, no refrigeration and map-based regimes instead of one design
   point.
3. `CSL-0293` *two_shaft_gas_turbine_expander_map* (same MSTh collection,
   imported by card C-333) — two shafts and lookup maps, no chiller.

What this model adds: the gas-turbine intake-cooling topology (chiller sized
against the reduced-quantity constraint), which no library model has.

## Source and attribution

- Authors: Stéphane Bertagnolio (initials `SB` in the file name, MSTh course
  ULiège; the file carries the `Laboratoire de Thermodynamique, U. de Liege`
  EES stamp). Course material of MECA0006 *Machines et systèmes thermiques*
  (ULiège), repetition R12, exercise 7 — published as an example per the
  maintainer decision of `sources/thermo_models/README.md`.
- Source file: `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 12/MSTH-SB-R12-EX7.EES`
  (inventory row TM-0171, EES X7.458). Never copied into the library.
- The `cpbar`/`gamma` routines come from the ULiège combustion library
  (P. Ngendakumana, 2003), published in this library as `CSL-0005`
  *cpbar_combustion_products*; copied here as in `CSL-0200`/`CSL-0293`.

## Conversion log

- **2026-10-24 — import**: extracted with `ees_extract.py` (EES X7.458,
  `$UnitSystem SI MASS DEG PA C J` — already the CoolSolve unit system, the
  directive removed). Comments translated to English (paraphrase); provisional
  values and the commented alternative `T_c_su=T_chiller_su` ("without
  chiller") kept as comments. The equation-window calls of `cpbar` and `gamma`
  are undefined in the file (implicit EES user library): the routines of
  `CSL-0005` are copied in a library block (`CS-GAP-INCLUDE`, workaround of
  the workflow §4). The two `cpbar(...)` calls in function position are
  transcribed as `CALL` (multi-output procedure; valid EES, no equation
  change, as in `CSL-0034`/`CSL-0293`). `v_1=VOLUME(R134a,h=h_1,x=1)` rewritten
  as `v_1=VOLUME(R134a,P=P_ev,h=h_1)` — same state, the (h,x) pair returns
  NaN in CoolProp (decision D12; register row `CS-GAP-PROP-HQ`). State-point
  arrays of the R134a chiller added for the diagrams (`P_ch[i]`, `h_ch[i]`,
  `T_ch[i]`, `s_ch[i]`; results unchanged). `.initials` from the EES stored
  solution, R134a h/s shifted by the CoolProp−EES offsets; the model also
  converges without them.
- **Level**: score 3 = equations 1 (104, 50–300) + block 0 (largest 9 ≤ 5) +
  structure 1 (copied procedures/functions) + coupled components 1 (gas
  turbine + chiller) + off-design 0 + numerics 0 → level 2.

## Limitations and CoolSolve gaps

- Design point only (one regime); the parametric study suggested by the
  original (vary the chiller displacement) is not part of the model.
- `CS-GAP-PROP-HQ` ((h, x) property pair returns NaN): worked around in the
  native file by the D12 rewrite above; not blocking, not in
  `missing_features`.
- The expander/compressor work uses the mass flows as written in the original
  (`M_dot_a*w_e`, `M_dot_p*w_c`); kept unchanged (see *Model*).

## Related models

- `CSL-0200` (gas_turbine_reduced_quantities): same Brayton core and reduced
  quantities, no chiller.
- `CSL-0293` (two_shaft_gas_turbine_expander_map): same MSTh R9 family and the
  same copied combustion routines; two shafts and maps instead.
- `CSL-0005` (cpbar_combustion_products): source of the copied `cpbar`/`gamma`.

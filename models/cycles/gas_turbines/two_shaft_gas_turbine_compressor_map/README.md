# Two-shaft gas turbine with a compressor map and two expanders

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0011`

Steady-state model of a two-shaft gas turbine on air: a single-spool compressor
and combustion chamber, and two mechanically independent expanders, the first
driving the compressor and the second the generator. The compressor is
described by a **performance map** — reduced mass flow, pressure ratio and
isentropic efficiency versus reduced speed — read from an embedded lookup
table; the combustor is closed by an energy balance in which the mean specific
heats of the air and of the combustion products come from the `cpbar` routine of
the ULiège combustion library (CSL-0005); the power balance of expander 1 gives
its isentropic efficiency, and expander 2 expands down to the (unknown) ambient
pressure. The model is the library's example of a **turbo-machine map** and of a
gas turbine whose combustion side is described by mean specific heats.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air (compressor, expanders); N₂, O₂, CO₂, H₂O (combustion products, inside `cpbar`) |
| **Size** | 44 equations in the main file (largest block: 7), 38 blocks; the runnable variant has 52 equations (largest block: 11) once the two copied library routines are inlined |
| **Source** | ULiège — course *Machines et systèmes thermiques* (MECA0006), revision exercises of 2005-12-23 (EES file `Revision JL051223-02.EES`) |
| **Authors** | Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0+`fix/library-gaps` — the main file is **blocked** by `CS-GAP-INTERP-EES` and `CS-GAP-INCLUDE`; the runnable variants are verified against the EES stored solutions of the three revision files |

## Problem statement

A two-shaft gas turbine (compressor + combustor on one shaft, high-pressure
turbine driving the compressor and low-pressure turbine driving the generator on
a second shaft) runs on air at **p₁ = 1 bar and t₁ = 15 °C**. The compressor
design speed is 10 000 rpm at t₁,design = 15 °C, and its map is known at three
reduced speeds:

| `N_rN` | `M_r_cp` | `r_p` | `epsilon_s_cp` |
|---:|---:|---:|---:|
| 1.00 | 454 | 4.60 | 0.860 |
| 0.95 | 420 | 4.00 | 0.865 |
| 0.90 | 370 | 3.60 | 0.860 |

Determine, at **nominal speed** (N = N_design): the air mass flow, the
compressor power, the flame temperature, the air–fuel ratio needed to reach it,
the isentropic efficiency of expander 1, its exhaust temperature and the
pressure after expander 2 (the natural gas is methane, LHV = 50 MJ/kg, arriving
at 25 °C, which is also the reference temperature of the sensible enthalpies of
the air and of the combustion products in the combustor balance).

The original exercise is a **revision in three parts**, all describing this one
machine and available as three EES files (`Revision JL051223-01/02/03.EES`):
part 1 runs the machine at 95 % of its nominal speed and gives the flame
temperature (802 °C) and the isentropic efficiency of expander 1 (0.85); part 2
(*this model*) brings it back to nominal speed and asks for those two
quantities; part 3 repeats the question with colder, less dense ambient
conditions (0.76 bar, 0 °C).

## Model

Reduced properties (revolutions per second, Pa, °C):

$$\dot m_r=\dot m\,\frac{\sqrt{T+273}}{p/10^5},\qquad N_r=\frac{N}{\sqrt{T+273}},\qquad N_{rN}=\frac{N_r}{N_{r,design}}$$

Compressor (map + balance):

$$w_{cp}=\frac{h_{2s}-h_1}{\epsilon_{s,cp}},\quad h_{2s}=h(p_2,s_1),\quad p_2=p_1\,r_p$$

the three map quantities `M_r_cp`, `r_p`, `epsilon_s_cp` being read from the
lookup table at `N_rN`; the air flow follows from the map, $\dot m_a=\dot m_{r,cp}(p_1/10^5)/\sqrt{t_1+273}$.

Combustion chamber (no pressure loss, no heat loss; the flame temperature
`t_ex_burner` is defined by an energy balance in which the sensible enthalpies of
the air and of the products are counted from a 25 °C reference, in J/kg):

$$\underbrace{c̄_{p,a}(25-t_2)}_{q_1}+\underbrace{0}_{q_2}+\underbrace{(-f\,\mathrm{LHV})}_{q_3}+\underbrace{0}_{q_4}+\underbrace{c̄_{p,p}(t_{ex}-25)}_{q_5}=0$$

The mean specific heats `c̄_p,a` and `c̄_p,p` are those of the ULiège combustion
library: `cpbar(1,4,0,25,t_2)` for the air and `cpbar(1,4,f,25,t_ex_burner)`
for the products of CH₄ in simplified air (CSL-0005, copied in the runnable
variant); the ratio of specific heats of the products comes from its `gamma`
routine. `q_1` and `q_5` are the sensible enthalpies of the compressed air and of
the combustion products relative to the 25 °C reference (`q_1` is negative because
the air is hotter than 25 °C), and `q_3` is the heat released by the combustion;
they are terms of the balance, not heat losses to the ambient. `q_2 = 0` states
that the combustor is adiabatic (no heat loss) and `q_4 = 0` that the combustion
is complete (no unburned CO).

Expander 1 drives the compressor (no mechanical loss):

$$\dot m_p\,w_{exp1}=\dot m_a\,w_{cp},\qquad \epsilon_{s,exp1}=\frac{w_{exp1}}{w_{s,exp1}},\qquad w_{exp1}=c̄_{p,p}(t_3-t_4)$$

with $\dot m_p=\dot m_a(1+f)$ and $t_3=t_{ex}$; its isentropic end state uses
the products' ratio of specific heats, $(t_{4s}+273)/(t_3+273)=(p_4/p_3)^{(\gamma-1)/\gamma}$.
Since expander 2 has no load, its exhaust pressure `p_4` is **not** given: it is
the pressure at which the isentropic expansion from `p_3` reaches the exhaust
temperature `t_4` fixed by expander 1.

| Inputs | Value | Outputs (nominal speed) | Value |
|---|---|---|---|
| `p_1`, `t_1` | 1 bar, 15 °C | `M_dot_1` air flow | 24.75 kg/s |
| `N_design` | 10 000 rpm | `r_p`, `epsilon_s_cp` (from the map) | 4.00, 0.865 |
| `N` | `N_design` | `w_cp` compressor specific work | 162.6 kJ/kg |
| `LHV` | 50 MJ/kg | `t_ex_burner` flame temperature | 802.4 °C |
| `t_1_design` | 15 °C | `f` air–fuel ratio | 0.0143 (e = 3.07) |
| `M_r_exp1`, `M_r_exp2` | 205.8, 385.3 (given) | `epsilon_s_exp1` | 0.850 |
| map `lookup_1` | 3 × 4 | `t_4`, `p_4` | 658.9 °C, 198.9 kPa |

## How to run

The main file `two_shaft_gas_turbine_compressor_map.eescode` keeps the native
EES syntax and **does not run** in CoolSolve v0.3.0 (see *Limitations and CoolSolve
gaps*). The runnable transcription, written for CoolSolve, is:

```bash
coolsolve ./two_shaft_gas_turbine_compressor_map_coolsolve.eescode
```

Keep `two_shaft_gas_turbine_compressor_map_coolsolve.initials` (the solution
stored by EES): **without it the solver converges to a nonphysical branch**
(`f` = −0.85, `t_ex_burner` = 51 000 °C) and reports SUCCESS. Three edits
separate the two files: the three `INTERPOLATE` calls use CoolSolve's positional
form (CoolSolve-only syntax, **not valid EES**: the `_coolsolve` and `_ambient`
files are not meant to be run in EES), the two `cpbar` calls become `CALL`
statements (the `CALL cpbar(...)` form is valid EES), and the `cpbar`/`gamma`
routines of CSL-0005 are copied in (details in *Conversion log*). No equation of
the machine was changed.

Two cases are shipped as files:

| File | Case |
|---|---|
| `two_shaft_gas_turbine_compressor_map_coolsolve.eescode` | nominal speed, 1 bar, 15 °C (the main operating point, revision part 2) |
| `two_shaft_gas_turbine_compressor_map_ambient.eescode` | 95 % of nominal speed, 0.76 bar, 0 °C (revision part 3, inventory `TM-0151`) |

Each `.eescode` file needs its own copy of the map
(`two_shaft_gas_turbine_compressor_map*-lookup_1.csv`), since a CoolSolve model
only reads the tables named after its own file name.

## Results

Nominal speed, 1 bar, 15 °C (`two_shaft_gas_turbine_compressor_map_coolsolve.sol`):

| Quantity | Value | Quantity | Value |
|---|---:|---|---:|
| `M_dot_1` air flow | 24.75 kg/s | `q_1` air enthalpy at `t_2` relative to 25 °C, sign reversed | −153.6 kJ/kg |
| `r_p` | 4.00 | `q_5` products enthalpy at `t_ex_burner` relative to 25 °C | 868.6 kJ/kg |
| `epsilon_s_cp` | 0.865 | `t_ex_burner` | 802.4 °C |
| `t_2` compressor outlet | 175.8 °C | `f` air–fuel ratio | 0.01430 |
| `w_cp` | 162.6 kJ/kg | `M_dot_p` products | 25.10 kg/s |
| `w_s_cp` isentropic | 140.7 kJ/kg | `w_exp1` | 160.3 kJ/kg |
| `gamma` products | 1.323 | `epsilon_s_exp1` | 0.8504 |
| `p_2` = `p_3` | 400 kPa | `t_4` / `t_4s` | 658.9 / 633.6 °C |
| | | `p_4` | 198.9 kPa |

The machine burns 1.4 % of its air mass in fuel (307 % excess air) to reach
802 °C at 4:1 compression; expander 1 delivers 160.3 kJ per kg of product gas
against the 162.6 kJ per kg of air needed by the compressor (4.02 MW on both
sides once multiplied by the mass flows 25.10 and 24.75 kg/s), so its isentropic
efficiency is 0.850.

The three parts of the revision exercise, computed with this model:

| Quantity | 95 % speed, 1 bar, 15 °C (`TM-0149`) | nominal speed, 1 bar, 15 °C (`TM-0150`) | 95 % speed, 0.76 bar, 0 °C (`TM-0151`) |
|---|---:|---:|---:|
| `N_rN` computed | 0.9500 | 1.0000 | 0.9757 |
| `M_r_cp`, `r_p`, `epsilon_s_cp` (read at 0.95) | 420, 4.00, 0.865 | 420, 4.00, 0.865 | 420, 4.00, 0.865 |
| `M_dot_1` [kg/s] | 24.75 | 24.75 | 19.32 |
| `w_cp` [kJ/kg] | 162.6 | 162.6 | 154.3 |
| compressor power `M_dot_1`·`w_cp` [MW] | 4.02 | 4.02 | 2.98 |
| `t_2` [°C] | 175.8 | 175.8 | 152.7 |
| `t_ex_burner` [°C] | 802 (given) | 802.4 | 748.1 |
| `f` | 0.01429 | 0.01430 | 0.01344 |
| `w_exp1` [kJ/kg] | 160.3 | 160.3 | 152.2 |
| `epsilon_s_exp1` | 0.850 (given) | 0.8504 | 0.8475 |
| `t_4` [°C] | 658.5 | 658.9 | 610.9 |
| `p_4` [kPa] | 198.8 | 198.9 | 151.1 |

The colder, lighter ambient (part 3) removes 22 % of the air flow, 5 % of
the compressor specific work and 26 % of the compressor power (4.02 to 2.98 MW);
the flame temperature drops by 54 K and the excess air
rises to 333 %.

The map is read at the **literal** `N_rN = 0.95` in all three parts of the
exercise, so `N_rN` is only a diagnostic of the running point. Reading the map
at the actual reduced speed instead (what the phrase *"retour à la vitesse
nominale"* of part 2 invites the student to do) gives, at `N_rN` = 1,
`M_r_cp` = 454, `r_p` = 4.6 and `epsilon_s_cp` = 0.86 (and, by linear
interpolation between the two nodes, `M_r_cp` = 437.5, `r_p` = 4.31,
`epsilon_s_cp` = 0.8624 at `N_rN` = 0.9757, part 3) — but then the two reduced
flows given in the revision files, `M_r_exp1` = 205.8 and `M_r_exp2` = 385.3, no
longer agree with the rest of the machine, so that reading is not shipped here.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the model runs on
     Air, so CoolSolve has no T-s/P-h diagram for it (CS-FEAT-DIAGRAM-IDEAL): a
     parametric-sweep plot is expected, e.g. w_cp / t_ex_burner / epsilon_s_exp1
     versus p_1 (ambient pressure) or versus N/N_design, or the compressor map
     r_p and epsilon_s_cp versus the reduced speed N_rN -->

## Verification

The three EES files of the revision store the solution of their last run, all
consistent with their own equations. Each of them was reproduced with this
model (runnable transcription; `tools/compare_solution.py`, CoolSolve
v0.3.0+`fix/library-gaps`):

| Run | Variables compared | Max. rel. deviation | Largest deviation |
|---|---:|---:|---|
| `TM-0150` nominal speed (main file) | 44 (40 without reference offsets) | 1.6·10⁻³ | `c_p_a` 1017.17 → 1018.80 |
| `TM-0151` ambient variant | 44 (40) | 1.4·10⁻³ | `c_p_a` 1016.05 → 1017.50 |
| `TM-0149` 95 % speed | 44 (40) | 1.6·10⁻³ | `c_p_a` 1017.17 → 1018.80 |

Explanations, in the order of the deviations of the main run:

1. **Reference state of air** — `h_1`, `h_2`, `h_2s` and `s_1` differ by 20–30 %
   because CoolProp and EES use different reference states for `Air`
   (`ees_import.md` §11: compare differences, not absolute values). The
   enthalpy difference of the compressor, `h_2 − h_1`, agrees to 6·10⁻⁴
   (162 634 vs 162 537 J/kg), and so does `w_s_cp = h_2s − h_1` (140 679 vs
   140 595).
2. **Ideal-gas enthalpies of the combustion products** — `c_p_a` and
   `c̄_p,p` differ by 0.1–0.2 % (the same deviation as the verified model
   CSL-0005), which propagates to the fuel–air ratio `f` and `q_3` (1.0·10⁻³)
   and, through `t_2`, to `q_1`. All derived results — specific works, temperatures,
   `epsilon_s_exp1`, `p_4`, mass flows — agree within 1.1·10⁻³, inside the
   0.5 % tolerance of `ees_import.md` §11 for a different equation of state.
3. The model reads the map at a table node (`N_rN` = 0.95), so the linear
   interpolation of CoolSolve and the cubic interpolation of EES
   (`CS-GAP-INTERP-CUBIC`) give the same value. The two reduced flows of the
   exercise are given *and* computed (`M_r_exp1` = 205.8, `M_r_exp2` = 385.3):
   the equations reproduce those values to 10⁻¹¹ at this operating point, so
   the redundancy is consistent, as in EES. Where the exercise does not give
   them (part 1) the model computes 205.759 and 385.446 against the 205.762 and
   385.283 stored by EES (4.2·10⁻⁴ at most, from the deviations above).

## Source and attribution

Revision exercise of the ULiège course *Machines et systèmes thermiques*
(MECA0006), series of 2005-12-23 by **Jean Lebrun** (ULiège Thermodynamics
Laboratory), in three parts (`Revision JL051223-01/02/03.EES`; the same three
files also appear, byte for byte, in the folder *TP 13 Révisions* of the same
course). The author is identified from the file prefix `JL` and the EES
licence stamp of the file (`{$ID$ #1206: Jean Lebrun, Laboratoire de
Thermodynamique, Univ. Liege}`); the model was translated for the library by
editing its comments, never its equations. The combustion routines `cpbar` and
`gamma` are those of the ULiège combustion library (P. Ngendakumana, 2003),
published as the library model CSL-0005.

Source file (EES X7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 09/Revision JL051223-02.EES`
(inventory candidate `TM-0150`, duplicate group `DG-0032`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): unit
  system already `SI MASS DEG PA C J`, no conversion needed (the `$UnitSystem`
  line is dropped, as in every library model); the EES licence tag was removed;
  the embedded table `Lookup 1` was renamed `lookup_1` (file-name safety) and
  the three references in the equations updated by the tool; the block *Solution:
  Variables in Main* that the file carries in its equations window was dropped
  (it is the stored solution, kept as reference in `ees_variables.csv`).
  Comments translated to English, standard header added; **the 44 equations are
  unchanged** (checked equation by equation against the extraction). The
  textbook approximations of the original were kept: `273` instead of
  `273.15` in the reduced properties and in the isentropic relation, the
  commented-out `c_p_p = 1100` and `gamma = 1.35` left as documentation of the
  constants they replace.
- **2026-10-05 — runnable variant**
  `two_shaft_gas_turbine_compressor_map_coolsolve.eescode`: three
  transcriptions leaving the physics untouched —
  (i) the three `INTERPOLATE('lookup_1', <y>, 'N_rN', N_rN=0.95)` calls written
  in CoolSolve's positional form `INTERPOLATE('lookup_1','N_rN',<y>,0.95)`
  (`CS-GAP-INTERP-EES`); this positional form is **CoolSolve-only syntax and
  not valid EES**, so the `_coolsolve` and `_ambient` files are not meant to be
  run in EES; (ii) the two calls of the `cpbar` PROCEDURE written as
  `CALL cpbar(... : c_p_a, Q_4_a, x_a, e_min_a, e_a)`, the form that runs in
  CoolSolve for a 5-output procedure (where the function-call form of the main
  file is rejected) and that is valid EES; only the first output, the mean
  specific heat, is used by the model; (iii) the `cpbar` PROCEDURE and the
  `gamma` FUNCTION copied from CSL-0005 in a marked block, until
  `CS-FEAT-IMPORT` provides `$INCLUDE library:cpbar_combustion_products`
  (`CS-GAP-INCLUDE`). Verified against the EES stored solution (see
  *Verification*).
- **2026-10-05 — variant `two_shaft_gas_turbine_compressor_map_ambient.eescode`**
  (revision part 3, inventory `TM-0151`): only three inputs of the runnable
  variant were edited (`p_1` = 76 000 Pa, `t_1` = 0 °C, `N` = 0.95 `N_design`);
  verified against the EES stored solution of `TM-0151`.
- **2026-10-05 — merge of the duplicate group `DG-0032`** (roadmap decision D4:
  one exam in several files describing one system → one example model). Part 1
  (`TM-0149`, the same machine at 95 % speed with `t_ex_burner` = 802 °C and
  `epsilon_s_exp1` = 0.85 given) is the same operating point as the main file
  and adds no equation: it is reported in the *Results* table and was used as a
  third verification reference. Part 3 (`TM-0151`) differs by the ambient
  conditions and is shipped as the `_ambient` variant. The three files of *TP 13
  Révisions* (`TM-0175`, `TM-0176`, `TM-0177`) are byte-identical copies of the
  three files of *TP 09* and are recorded as duplicates.
- **Level 2** — score 4 on the `taxonomy.md` §3 grid (largest block 7, four
  coupled components, semi-empirical combustion, guesses required), lowered by
  one point: the difficulty is pedagogical, not numerical — the implicit loop is
  a single block of 11 variables and the model is an exercise, as in the
  inventory guess and in CSL-0006, which uses the same combustion library.

## Limitations and CoolSolve gaps

Physical simplifications of the exercise: air and combustion products are ideal
gases with mean specific heats (no dissociation, no pressure dependence, no
temperature dependence of `c̄_p` inside a stage), the combustor has no pressure
loss and no heat loss (`q_2` = 0; `q_1` and `q_5` are the sensible enthalpies of
the air and of the products relative to a 25 °C reference, not losses),
the mechanical losses of the turbine are neglected (`M_dot_p·w_exp1 =
M_dot_a·w_cp`), expander 2 has no load, and expander 1 is described by a single
isentropic efficiency.

The main file is **blocked** by two CoolSolve gaps (see CoolSolve
`docs/model_library_support.md`), both worked around in the runnable variants:

- `CS-GAP-INTERP-EES` — the native EES call
  `INTERPOLATE('lookup_1','M_r_cp','N_rN',N_rN=0.95)` (a named argument selects
  the *input* column) is parsed as a property call and fails with *"Unknown
  fluid: 'lookup_1'"*; the runnable variants use CoolSolve's positional form,
  which is not valid EES;
- `CS-GAP-INCLUDE` / `CS-FEAT-IMPORT` — `cpbar` and `gamma` come from an EES
  `.LIB` loaded implicitly, which CoolSolve does not support; the two routines
  are therefore copied from CSL-0005 in the runnable variants and should become
  `$INCLUDE library:<name>` lines.

Open question for the maintainer (to be checked in EES): the main file calls
`cpbar(1,4,0,25,T_2)` and `cpbar(1,4,f,25,T_ex_burner)` as functions, whereas
the `cpbar` of CSL-0005 is a PROCEDURE with five outputs, which CoolSolve
refuses in an expression (*"Procedure cpbar has 5 outputs and cannot be called
as a function"*); the runnable variants therefore use `CALL cpbar(...)`. It has
not been verified whether EES accepts such a function-call form for a
multi-output procedure, nor which output it would return; the 2005 exercise
most likely used an older version of `cpbar` with a single output. This is not
a registered CoolSolve gap.

Also worth knowing: the file emits the harmless hint *"Did you mean 'CO2'?"* on
every ideal-gas `CO2` property call inside the copied library routines
(`CS-BUG-FLUID-HINT-CO2`), and a `.initials` file is required (see *How to
run*).

## Related models

- `CSL-0005` (*cpbar_combustion_products*): the `cpbar` procedure and the
  `gamma` function used by this model, copied into the runnable variant.
- `CSL-0006` (*boiler_mean_specific_heat*): another user of the same combustion
  library, on a heating boiler.
- `CSL-0035` (*centrifugal_compressor_lookup_map*): another map-based
  compressor model blocked by the same native `INTERPOLATE` gap.
- `CSL-0050` (*gas_turbine_two_shaft_intercooled_regenerative*): the same
  machine concept (two independent shafts, the HP turbine driving the
  compressors) with a constant compressor pressure ratio, intercooling,
  regeneration and a reheat combustion chamber.
- `CSL-0051` (*turbojet_ideal_260ms*): ideal turbojet of the same course
  (repetition 6), fully explicit and verified — the non-ideal counterpart of
  this gas-turbine family.

- `CSL-0052` (*combined_gas_steam_cycle*): the same gas cycle on ideal-gas
  air with a constant compressor pressure ratio, but topping a Rankine
  bottoming cycle heated by the exhaust gases.
- `CSL-0060` (*gas_turbine_reheat*): the same intercooled + regenerative
  architecture on ideal-gas air, with the reheat combustion chamber between the
  turbine stages and the LP expansion to ambient pressure.

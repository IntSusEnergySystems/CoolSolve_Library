# Simple ORC with imposed component performance (R245fa)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0019`

A subcritical Organic Rankine Cycle for a quick evaluation of the cycle
performance (the *screening method* of Chapter 5.3 of Quoilin, 2011):
R245fa heated by hot Therminol-66 oil in the evaporator, condensed against
cooling water, with a recuperator. Expander and pump are described by
imposed isentropic effectivenesses (0.8) and both heat exchangers by
imposed pinch constraints (10 K). For the default inputs
($T_{ev}$ = 130 °C, $T_{cd}$ = 30 °C) the model determines the evaporation
and condensation pressures, all state points, the heat-source/sink outlet
states, the net power (14.8 kW) and the cycle efficiency (15.7 %).

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R245fa, Water (heat sink), Therminol-66 oil (heat source, `therminol66` procedure) |
| **Size** | 182 equations in 152 blocks (largest block: 12), incl. arrays `s[i]`, `t[i]`, `p[i]`, `h[i]` for the diagrams |
| **Source** | S. Quoilin, PhD thesis, University of Liège (2011) — CoolSolve example `orc_r245fa` + original EES file |
| **Authors** | S. Quoilin (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs from the shipped `.initials`; import verified against the solution stored in the original EES file |

## Problem statement

A subcritical ORC with R245fa operates between an evaporation
temperature of 130 °C and a condensation temperature of 30 °C, with
5 K of superheat at the evaporator outlet and 7.5 K of subcooling at the
condenser outlet. The heat source is 3 kg/s of Therminol-66 oil, the heat
sink 4 kg/s of water; the pinch in each heat exchanger is 10 K and the
pressure drops are neglected. The expander and the pump have an isentropic
effectiveness of 0.8 each and the recuperator an effectiveness of 0.8.
For a working-fluid flow rate of 0.4 kg/s, determine the evaporation and
condensation pressures, the expander and pump powers, the net power and
the cycle efficiency.

## Model

- Saturation pressures at $T_{ev}$ and $T_{cd}$ (phase-change plateaus);
  zero pressure drops, so $p_{su,ev} = p_{su,exp}$ and
  $p_{ex,exp} = p_{ex,cd}$;
- expander: imposed isentropic effectiveness
  $\varepsilon_{exp} = (h_{su} - h_{ex})/(h_{su} - h_{ex,s})$;
- condenser/evaporator: three-point energy balances (subcooled / two-phase
  / superheated regions) against the secondary fluids with pinch
  constraints $pinch_{ev}$, $pinch_{cd}$ evaluated at the region boundaries;
- pump: $h_{ex,pp} = h_{su,pp} + v_{su,pp}(p_{su,ev} - p_{ex,cd})/\varepsilon_{pp}$;
- recuperator: $\dot Q_{rec} = \varepsilon_{rec}\,\dot C_{min}(T_{su,vap} - T_{su,liq})$
  with capacity rates from $c_p$ calls on each side;
- heat source: Therminol-66 properties from the `therminol66` procedure
  (density, heat capacity, conductivity, kinematic viscosity as functions
  of the oil temperature in °C); heat sink: water property calls;
- performance: $w_{exp}$, $w_{pp}$, $w_{net}$, $q_{ev}$,
  $\eta_{cycle} = w_{net}/q_{ev}$, pressure and volume ratios $r_p$, $r_v$.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `fluid$` working fluid | R245fa | `p_su_ev` evaporation pressure | 23.50 bar |
| `M_dot` working-fluid flow | 0.4 kg/s | `p_ex_cd` condensation pressure | 1.781 bar |
| `T_ev` / `T_cd` | 130 / 30 °C | `W_dot_exp` expander power | 15.61 kW |
| `M_dot_hf` oil / `M_dot_cf` water | 3 / 4 kg/s | `W_dot_pp` pump power | 0.807 kW |
| `pinch_ev` / `pinch_cd` | 10 / 10 K | `W_dot_net` net power | 14.80 kW |
| `DELTAT_ex_ev` / `DELTAT_ex_cd` | 5 / 7.5 K | `eta_cycle` cycle efficiency | 0.1569 |
| `epsilon_exp` / `epsilon_pp` / `epsilon_rec` | 0.8 / 0.8 / 0.8 | `r_p` / `r_v` | 13.19 / 16.24 |

## How to run

Open `orc_simple_r245fa.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./orc_simple_r245fa.eescode
```

The model needs the shipped `.initials` file (EES stored values): from
default guesses the oil-property block is singular (see *Limitations*).
It then converges in 50 iterations.

Change `fluid$` to another subcritical azeotropic fluid to reproduce the
screening study; set `epsilon_rec = 0` to remove the recuperator.

## Results

| Quantity | Value |
|---|---:|
| `p_su_ev` evaporation pressure | 23.50 bar |
| `p_ex_cd` condensation pressure | 1.781 bar |
| `T_hf_su_ev` oil inlet (computed from the evaporator balance) | 147.1 °C |
| `T_hf_ex_ev` oil outlet | 131.4 °C |
| `T_cf_su_cd` water inlet | 12.5 °C |
| `T_cf_ex_cd` water outlet | 17.2 °C |
| `T_su_exp` expander inlet | 135.0 °C |
| `T_ex_exp` expander outlet | 62.2 °C |
| `Q_dot_rec` recuperator duty | 11.87 kW |
| `q_ev` specific heat input | 235.8 kJ/kg |
| `W_dot_net` net power | 14.80 kW |
| `eta_cycle` cycle efficiency | 0.1569 |

The arrays `s[i]`, `t[i]`, `p[i]`, `h[i]` (1 pump outlet … 11 loop
closure) give the cycle on the T-s or P-h diagram (CoolSolve *Diagram*
tab, *Overlay array path*, *Close cycle*); `T_hf[i]`/`T_cf[i]` give the
secondary-fluid temperature profiles in the heat exchangers.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle,
     figures/orc_simple_r245fa_ts.png -->

## Verification

Faithful import vs the solution stored in the original EES file
(`EES_ok/orc_r245fa.EES`, EES 9.920, 186 stored variables). Of the 177
variables common with the CoolSolve solution:

- 88 agree within 0.1 % (all imposed inputs, temperatures, pinches,
  flow rates, $T_{ev}$/$T_{cd}$ exactly);
- the rest deviate systematically by 0.1–2.1 % (thermodynamic quantities)
  and up to 5.2 % (vapour conductivity `k[6]`), plus the diagnostic `x`
  (100 in EES, 0 in CoolSolve: see *Limitations*); all traced to the R245fa
  property formulation (the original uses `$REFERENCE r245fa IIR`,
  i.e. the REFPROP-based IIR reference; CoolSolve uses CoolProp):
  saturation pressures +0.4–0.5 % at the imposed $T_{ev}$/$T_{cd}$,
  propagating to enthalpies/entropies (~0.2 %), `cp_vap_rec` −1.75 %,
  `Q_dot_rec` −2.06 %, vapour conductivity `k[6]` −5.2 % (transport
  properties, as in `CSL-0018`);

| Quantity | EES | CoolSolve | rel. diff. |
|---|---:|---:|---:|
| `p_su_ev` [Pa] | 2.33933e6 | 2.34952e6 | +4.3e-03 |
| `p_ex_cd` [Pa] | 177175 | 178079 | +5.1e-03 |
| `W_dot_net` [W] | 14816.5 | 14801.8 | −1.0e-03 |
| `W_dot_exp` [W] | 15620.0 | 15608.8 | −7.2e-04 |
| `q_ev` [J/kg] | 235388 | 235801 | +1.8e-03 |
| `eta_cycle` [-] | 0.157363 | 0.156930 | −2.7e-03 |
| `T_hf_su_ev` [°C] | 147.088 | 147.060 | −1.9e-04 |
| `r_p` / `r_v` [-] | 13.20 / 16.15 | 13.19 / 16.24 | −0.07 % / +0.57 % |

(EES also stores 9 stale variables with no counterpart in the equations:
the commented-out second-law block `E_dot_hf`, `eta_II`, `h_hf_0`,
`s_hf_0`, `s_hf_su_ev` and the scalars `s`, `T_cf[5]`, `T_cf[6]`,
`T_hf[1]` — values from an earlier revision of the file, ignored.)

## Source and attribution

Screening ORC model of the PhD thesis of **S. Quoilin** (ULiège
Thermodynamics Laboratory): *Sustainable energy conversion through the
use of Organic Rankine Cycles for waste heat recovery and solar
applications* (2011, Chapter 5.3). The file carries the author's name
and date (18 September 2011) and a permissive-use statement (free use
and reproduction with credit to the thesis). The `{$ID$ … Jean Lebrun …}`
tag is the EES licence of the laboratory, not the author. The CoolSolve
example `orc_r245fa.eescode` (S. Quoilin) has byte-identical equations
(see *Conversion log*).

Source files: CoolSolve `examples/orc_r245fa.eescode` (inventory
candidate `CSX-031`) and its EES original `misc/EES_ok.zip`:
`EES_ok/orc_r245fa.EES` (EES 9.920, comments in English, full stored
solution of 186 variables, no tables).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `orc_r245fa.EES`): unit system already SI-°C-Pa-J (no conversion
  needed); EES licence tag (Jean Lebrun, the lab licence, not the author)
  and `{$PX$}` display tag removed; one `PROCEDURE` (`therminol66`),
  `$REFERENCE r245fa IIR` and `$ifnot parametrictable` directives kept
  (CoolSolve accepts them; the model solves); no tables, no external
  functions (all calls are CoolSolve built-ins). The raw extraction solves
  from the stored values and matches EES (see above).
- **2026-10-05 — library model follows the EES original.** The CoolSolve
  example `orc_r245fa.eescode` has byte-identical equations to the EES
  original (only the `$UnitSystem` line added by the extractor and
  trailing blank lines differ); it stays in CoolSolve as a test case and
  is superseded here by this curated model. No physics changed by the
  curation (re-solved: identical `.sol`).
- **2026-10-05 — curation**: standard header added; SI units added to the
  input comments; the nomenclature unit of `h` corrected to J/kg (was
  J/(kg·K) in the original); the `MM = molarmass(toluene)` line kept with
  an explanatory comment (unused leftover of the thesis template).
  Already diagram-ready: the state arrays `s[i]`, `t[i]`, `p[i]`, `h[i]`
  and the profiles `T_hf[i]`/`T_cf[i]` are in the original.
- The air-source sibling `orc_simple` (CoolSolve example `CSX-032`,
  EES original `simple_ORC_model SQ120220.EES`, candidate `TM-0324`) is the
  same thesis screening model with air as heat source and sink
  (`hf$ = cf$ = 'air_ha'`), `M_dot = 1` kg/s, 5 K of subcooling, no
  recuperator (`epsilon_rec = 0`), EES property calls for the secondary
  fluids instead of `therminol66`, and the second-law block active; it is
  recorded as merged into this model for documentation only: the inputs
  block alone does not reproduce it (the secondary-fluid equations of the
  heat source and sink, `therminol66` here, and the second-law block also
  differ), and no variant file is shipped. Its earlier copy with a
  diagram window (`TM-0322`) is recorded as a duplicate.

## Limitations and CoolSolve gaps

- EES `quality()` at the superheated expander exhaust stores 100 (percent
  convention outside the saturation dome); CoolSolve returns 0 for the
  same call. Diagnostic output only — the physics is unaffected. (Not
  registered in the CoolSolve gap register: unverified suggestion — the
  value 100 is the one stored in the solution of `orc_r245fa.EES`; to be
  confirmed with a minimal reproducer in valid EES before registering.)
- `$REFERENCE r245fa IIR` is kept verbatim; CoolSolve solves the model
  with its own (CoolProp) R245fa properties — hence the ~0.5 % systematic
  deviations above, not a gap.
- From default guesses the 12-variable oil-property block is singular;
  the shipped `.initials` (EES stored values) are required. Level score:
  1 (182 equations) + 1 (block of 12) + 1 (procedure, arrays) + 1 (five
  coupled components) + 0 (design-point model) + 1 (curated guesses) = 5
  → level 3.
- No other CoolSolve gap: the model uses only built-in property functions
  (incl. `molarmass(toluene)`, unquoted lowercase, which CoolSolve
  resolves to 92.14 kg/kmol).

## Related models

- CoolSolve example `orc_simple.eescode` (same thesis screening model with
  air source/sink and no recuperator — merged here, kept in CoolSolve as
  a test case).
- `CSL-0004` (Rankine cycle of a 60 MW steam plant): same category, water
  instead of an organic fluid.
- `CSL-0015` (Basic R134a refrigeration cycle): same category family
  (vapour-compression/vapour-power cycles with imposed performance).
- `CSL-0084` *orc_expander_pump_empirical_maps*: same fluid (R245fa) and a
  small closed ORC demo, with the expander and pump performance from maps.

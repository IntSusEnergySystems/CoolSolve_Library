# Steam turbine driving a nitrogen compressor (exercise 5.54)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0282`

A steam turbine drives a nitrogen compressor; the remaining power goes to an
electric generator. Steam (0.25 kg/s) expands from 4 MPa, 350 °C to 20 kPa,
x = 0.95 in an adiabatic turbine; 42 kW drive a nitrogen compressor
(0.04 kg/s from 100 kPa, 20 °C to 10 MPa, 35 °C at the cooler outlet). The
model applies the first law for steady open systems on two control volumes
and computes (a) the power left for the generator and (b) the heat given up
by the nitrogen through compressor + cooler. A bonus section redoes the
nitrogen balance with the ideal-gas substance `N2` and quantifies the error
of the perfect-gas model (about 1.7 %).

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Water, Nitrogen, N2 (ideal gas) |
| **Size** | 38 equations (largest block: 1) |
| **Source** | thermo_models, ULiège THD 2017-2018, file `THD10_R03_E2.EES` |
| **Authors** | TBD (ULiège THD) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise 5.54 (course exercise, paraphrased from the original French
comments): a steam turbine drives a nitrogen compressor, as illustrated on
figure 5.33 of the course notes. The steam and nitrogen states are given on
the scheme; the mass flows are 0.25 kg/s in the turbine and 0.04 kg/s in the
compressor. The heat losses of the turbine are small and taken as zero. The
turbine delivers 42 kW to the compressor and the rest of its power goes to
an electric generator. (a) Determine the turbine power available to drive
the generator. (b) Determine the rate at which heat is lost by the nitrogen
as it passes through the compressor and the outlet cooler.

Sign convention of the original: every power is accounted **from the steam
side** of the turbine, so `W_dot_turb`, `W_dot_cmp` and `W_dot_gen` are all
negative (powers given up by the steam control volume). For the nitrogen
balance the exchanges are counted from the nitrogen side, hence
`abs(W_dot_cmp)` as the compression power received by the fluid.

## Model

Both machines are open systems in steady flow with one inlet and one outlet,
so the mass flow is the same at inlet and outlet and the first law reduces
to \(\dot Q + \dot W = \dot m\,(h_{out} - h_{in})\) (kinetic- and
potential-energy changes neglected against the enthalpy changes, as in the
original):

- \(a)\ \dot W_{turb} = \dot m_{vap}(h_{out,tv} - h_{in,tv}) =
  \dot W_{cmp} + \dot W_{gen}\), the turbine taken as adiabatic.
- \(b)\ \dot Q_{N2} + |\dot W_{cmp}| = \dot m_{N2}(h_{out,rfd} - h_{in,c})\)
  for the compressor + cooler control volume, for lack of data at the
  compressor outlet.

Steam states use Water (two-phase exit with (P, x), superheated inlet with
(T, P)); the nitrogen states use the real fluid `Nitrogen`. The bonus
section repeats the nitrogen balance with `N2`, the ideal-gas substance
(chemical formula = ideal gas in EES/CoolSolve), and computes
`err_Q = 100*abs(1 - Q_dot_N2_gp/Q_dot_N2)`.

## How to run

```bash
coolsolve ./steam_turbine_n2_compressor.eescode
```

Every block is explicit (largest block: 1); CoolSolve solves in a few
iterations with the shipped `.initials` and without them. No
`coolsolve.conf`, no variant.

## Results (default operating point)

| Quantity | EES (stored) | CoolSolve |
|---|---:|---:|
| W_dot_turb | −150.21 kW | −150.57 kW |
| W_dot_gen | −108.21 kW | −108.57 kW |
| Q_dot_N2 | −42.097 kW | −42.097 kW |
| Q_dot_N2_gp | −41.375 kW | −41.375 kW |
| err_Q | 1.7159 % | 1.7157 % |

The generator receives about 108 kW, and almost all the compression power
(42 kW) is rejected as heat by the compressor + cooler group: the balance
works out so because the nitrogen leaves the cooler near its inlet
temperature (35 °C against 20 °C).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![T-s diagram of the steam expansion](figures/steam_turbine_n2_compressor_ts.png)  + one-line caption -->

## Verification

Against the stored solution of `THD10_R03_E2.EES` (EES X8.423),
`compare_solution.py --ees-units`: 22 common variables, 2 differ
(rtol=0.001); only in EES: 1; only in CoolSolve: 16. Maximum relative
difference 3.25e-03 on W_dot_gen. The 16 CoolSolve-only variables are the
state-point arrays; the EES-only variable `P` (stored value 1, no unit) does
not appear anywhere in the equations of the original: it is a leftover of
the EES session, not part of the model.

The two variables above rtol=0.001 are `W_dot_turb` (2.35e-03) and
`W_dot_gen` (3.26e-03), which follows from `W_dot_turb − W_dot_cmp`. Both
come from the steam inlet enthalpy: CoolSolve 3 093 322 J/kg against EES
3 091 841 J/kg (rel. diff 4.8e-04), while `h_out_tv` agrees within 2.7e-05;
the small property deviation between the EES 8.4 water tables and CoolProp's
Helmholtz formulation is amplified by the difference of two large
enthalpies. This stays within the ≤ 0.5 % typical agreement for real-fluid
properties (ees_import.md §11). All other variables agree within 2.8e-04:
the real `Nitrogen` enthalpies match within 3e-06 (no reference-state
offset), and the ideal-gas `N2` enthalpies differ by up to 4.1e-04 (EES
ideal-gas data vs CoolProp), which leaves the derived heat `Q_dot_N2_gp`
within 2.7e-06 (only enthalpy *differences* enter the balance).

## Source and attribution

Source file: `~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R03/THD10_R03_E2.EES`
(EES X8.423, `SI MASS DEG KPA C KJ`, decimal comma). ULiège THD course
(repetition 3, exercise 2, 2017-2018), teachers S. Bertagnolio and
S. Borguet; no author name in the file, hence `TBD (ULiège THD)`. Exercise
5.54 of the course notes. Published under the library licence (MIT).

## Conversion log

- **2026-10-23 — import**: `ees_extract.py` (decimal comma converted to dot,
  EES licence tag removed); unit system `SI MASS DEG KPA C KJ` converted by
  hand to SI-°C-Pa-J: all pressures ×1000 (`p_in_c` 100 kPa → 100e3 Pa,
  `p_out_rfd` 10 000 kPa → 10e6 Pa, `p_in_tv` 4000 kPa → 4e6 Pa, `p_out_tv`
  20 kPa → 20e3 Pa), `W_dot_cmp` −42 kW → −42e3 W; enthalpies and powers are
  equation results (kJ/kg, kW → J/kg, W). No absolute-temperature relation
  and no hidden unit factor in the equations; temperatures already in °C.
  Guesses converted likewise in `.initials`. Comments translated from
  French (paraphrases); the exercise statement moved to the README.
- **2026-10-23 — post-processing**: state-point arrays `P[i]`, `h[i]`,
  `T[i]`, `s[i]` added (1–2: steam on Water; 3–4: nitrogen on Nitrogen);
  the results of the original variables are unchanged (their values in the
  `.sol` match the EES reference).
- **Level**: equations 38 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0 (the
  turbine, compressor and cooler are lumped control volumes coupled only by
  the given power −42 kW); no off-design/part-load → 0; no curated guesses
  → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

None: the model uses only standard property calls on Water, Nitrogen and
N2. Physical scope: the given states fix one operating point; the perfect
gas comparison is valid at these moderate temperatures only (as the
original notes).

## Related models

- `CSL-0189` (*r134a_turbine_power*): a turbine driving a compressor on a
  single fluid (R134a), with isentropic efficiencies and
  mechanical/alternator links.
- `CSL-0224` (*steam_turbine_heat_loss*): the same course, the same first
  law on one steam turbine, with kinetic- and potential-energy terms kept.

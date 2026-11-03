# Two-phase CO2 ejector (constant-efficiency sections, HEM-choked motive flow)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0325`

Transcritical CO2 ejector of the Liu & Groll type: the motive flow (gas-cooler
outlet) expands through a nozzle, entrains the suction flow (evaporator
outlet) expanded in a second nozzle, both streams mix at constant area with a
mixing efficiency, and a diffuser recovers part of the kinetic energy. The
ejector is the two-phase expansion work-recovery device of transcritical CO2
refrigeration/heat-pump cycles; this model computes the section pressures
(choking, suction, mixing), the exhaust state and the section areas from the
two inlet states, the two mass flow rates (entrainment ratio) and five
constant efficiencies.

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | R744 (CO2) |
| **Size** | 76 equations (largest block: 11) |
| **Source** | LaboThapPy `component/expander/ejector_csteff.py` (commit `f03f7f47`) |
| **Authors** | Basile Chaudoir (ULiège Thermodynamics Laboratory) |
| **License** | Apache-2.0/MIT (original); this translation published under the library license (MIT) |
| **CoolSolve** | 0.4.0@eb797fe — verified (source re-run compared, see *Verification*) |

## Problem statement

Given the motive inlet (T_su_1 = 40 °C, P_su_1 = 100 bar, M_dot_su_1 = 0.18 kg/s)
and the suction inlet (T_su_2 = 15 °C, P_su_2 = 39 bar, M_dot_su_2 = 0.07 kg/s)
of a transcritical CO2 cycle, and the constant efficiencies of the four
ejector sections, compute the ejector exhaust state and section areas. This is
the example `ejector_csteff_example.py` of the source; the model is
intended for on-design calculations of ejector-expansion transcritical CO2
cycles (Liu & Groll 2008).

## Model

Four sections, solved as one set of simultaneous equations (the Python class
solves them by three nested `brentq` root finds; every root find becomes an
equation of the square system):

1. **Motive nozzle** — constant isentropic efficiency eta_m:
   h_mb = h_su_1 − eta_m·(h_su_1 − h_mb_is), v_mb = √(2·(h_su_1 − h_mb)),
   A_mb = M_dot_su_1/(rho_mb·v_mb). The exit pressure P_b_sonic is closed by
   the condition h_mb = h_f(P_b_sonic), i.e. the exit state sits exactly on the
   saturated-liquid boundary. This reproduces what the source's solver actually
   computes: its `brentq` residual v_mb − a_mb jumps from +11.7 m/s (two-phase
   Kornhauser branch) to −78 m/s (single-phase CoolProp sound speed) exactly at
   that boundary, and the bracketing root find converges onto the jump (at the
   stored solution v_mb − a_mb = 89.96 − 78.28 = +11.7 m/s, so the exit flow is
   *not* sonic there despite the "choked" intent; see *Limitations*).
2. **Suction nozzle** — eta_s, same relations, exit pressure P_b_suction.
3. **Suction chamber / mixing section** — constant-pressure mixing of the two
   streams at their respective exit pressures, with a momentum-based mixed
   velocity V_mix = (v_mb + w·v_sb)/(1 + w) and mixing efficiency eta_mix. Two
   closures: the area balance A_mix_mom(P_b_suction) = A_mb + A_sb (the source's
   `suction_chamber` residual) closes P_b_suction, and the mass/momentum/energy
   system of the mixing section (rho_mix = M_dot_t/(A_mix·v_mix), the momentum
   balance for P_mix, h_mix = h0_mix − v_mix²/2, rho_mix = rho(h_mix, P_mix))
   closes v_mix.
4. **Diffuser** — pressure recovery P_ex = P_mix + C_t·½·rho_mix·v_mix² with
   the two-phase C_t correlation of Owen, Abdul-Ghani & Amini (Rouhani-type,
   homogeneous void fraction eps):
   C_t = 2·(A_mix/A_d)·rho_mix·(1 − A_mix/A_d)/(rho_l·(1 − eps)²),
   which closes the diffuser exit area A_d; h_ex = h_mix + (h_ex_is − h_mix)/eta_d
   with h_ex_is = h_mix + ½·v_mix² (definition as in the source).

The Kornhauser (1990) homogeneous-equilibrium speed of sound of the two-phase
mixture, a_mb = ν·√((h_g − h_f)/((v_g − v_f)·(∂h/∂P)_s − (∂v/∂P)_s·(h_g − h_f))),
is computed as post-processing at the nozzle exit state (the (∂/∂P)|_sat
derivatives by central differences with DELTA_P_sat = 500 Pa; agreement with
the CoolProp analytic partials of the source: 78.281 vs 78.281 m/s).

Inputs: T_su_1, P_su_1, M_dot_su_1, T_su_2, P_su_2, M_dot_su_2 (or w),
eta_m, eta_s, eta_mix, eta_d, C_t. Outputs: P_b_sonic, P_b_suction, P_mix,
P_ex, h_ex, T_ex, x_ex, v_ex, and the areas A_mb, A_sb, A_mix, A_d.

## How to run

```bash
coolsolve ./ejector_two_phase_co2.eescode
```

`.initials` provides guesses for the implicit variables (physical values, from
the source solution); they are needed mainly for the near-critical saturation
block (with default guesses the Kornhauser denominator is negative at the
start, which a Newton solver cannot recover from). `coolsolve.conf` disables
the CoolProp analytic partial derivatives (unreliable on two-phase saturation
calls) and enables tearing (the choking block reduces to a 1-D Newton).

## Results (default point)

| Variable | Value | | Variable | Value |
|---|---:|---|---|---:|
| P_b_sonic | 72.759 bar | | P_mix | 43.422 bar |
| v_mb | 90.00 m/s | | v_mix | 64.95 m/s |
| a_sound_mb (Kornhauser) | 78.30 m/s | | h_mix | 348.47 kJ/kg |
| P_b_suction | 37.864 bar | | x_mix | 0.6254 |
| v_sb | 43.21 m/s | | P_ex | 46.215 bar |
| A_mb | 3.487e-6 m² | | T_ex | 11.06 °C |
| A_sb | 1.686e-5 m² | | x_ex | 0.6335 |
| A_mix | 2.035e-5 m² | | v_ex | 60.18 m/s |
| A_d | 2.057e-5 m² | | w | 0.3889 |

Energy balance: M_dot_t·h_ex = 87.76 kW vs M_dot_p·h_su_1 + M_dot_s·h_su_2 =
87.66 kW (+0.11 %): the diffuser definition of the source,
h_ex = h_mix + (h_ex_is − h_mix)/eta_d, multiplies the *whole* kinetic energy
by 1/eta_d instead of the recovered fraction and therefore creates
(1/eta_d − 1)·½·v_mix² ≈ 0.37 kJ/kg of enthalpy; kept as in the original.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7) -->

## Verification

The source example was re-run in a throw-away virtual environment (LaboThapPy
`f03f7f47`, CoolProp 8.0.0, `work/ejector_two_phase_co2/`, since deleted): a
copy of `ejector_csteff.py` with the broken `void_fraction` import fixed (see
*Conversion log*) was driven by the example inputs and every internal result
dumped to `reference.csv`. `compare_solution.py ejector_two_phase_co2.sol
reference.csv`: **33 common variables, 1 differ (rtol=0.001)** — x_mb, which is
exactly 0 in this model (the closing condition h_mb = h_f) while the source's
`brentq` leaves the numerical residue 5.82e-06 of its branch-jump search;
all other variables agree, maximum relative difference **4.48e-04** (v_mb),
 pressures ≤ 1.2e-04. The residual ≤ 5e-4 scatter (h_su_1 2.4e-04, s_su_1
1.7e-04) is the property-backend difference (CoolSolve CoolProp 8.1.0dev vs
the source venv's 8.0.0): it shifts the saturation boundary h_mb = h_f and
with it P_b_sonic by +872 Pa (+1.2e-04).

The A_d of the reference (2.05731e-05 m²) is the tight-tolerance root of the
C_t correlation; the source's own stored A_d equals A_mix (2.03511e-05 m²)
because its `brentq` uses xtol=1e-5, larger than the distance between the root
and the lower bracket end A_mix — the returned area does not satisfy its own
correlation (C_t_comp = 0 there for C_t = 0.7). The model solves the
correlation exactly.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of `EjectorCstEff` from LaboThapPy, file
`labothappy/component/expander/ejector_csteff.py`, commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy
Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université de
Liège (ULiège), Université de Mons (UMONS). Original author of the file (git
history): B. Chaudoir. Changes: translated from Python to CoolSolve; the three
nested `brentq` root finds replaced by simultaneous equations; Kornhauser
sound-speed partial derivatives computed by central differences; CoolProp
fluid name `CO2` mapped to the EES real-fluid name `R744`.

Scientific basis: F. Liu, E. A. Groll, "Analysis of a two phase flow ejector
for transcritical CO2 cycle", (2008); two-phase sound speed: Kornhauser (1990);
diffuser C_t correlation: Owen, Abdul-Ghani & Amini (Rouhani 1969 void
fraction), as cited in the source.

## Conversion log

- **2026-10-31 — translation**: LaboThapPy `EjectorCstEff.solve()` translated
  to simultaneous equations; SI-K-Pa-J → SI-°C-Pa-J (temperatures only:
  velocities and specific energies are unchanged); `brentq` root finds →
  equations (P_b_sonic: h_mb = h_f, P_b_suction: area balance, v_mix:
  property consistency, A_d: C_t correlation); `brentq` retry loop of the
  mixing section (`v_min += 1`) dropped — the equation system has the same
  root; the phase-dependent branch of the sound speed (two-phase Kornhauser vs
  single-phase CoolProp `speed_sound`) written in its two-phase form, the only
  one applicable at the solution (x_mb = 0 boundary; single-phase sound speed
  kept as comment in the README only); source guards (`np.clip` of x, den ≤ 0,
  dh ≤ 0, try/except around the exhaust area) never active at the solution and
  not written.
- **2026-10-31 — import fix (in a work copy)**: the source imports
  `labothappy.correlations.properties.void_fraction` (module does not exist;
  it lives in `labothappy/correlations/void_fraction/`) and calls
  `void_fraction(x, rho_g, rho_l)[0]` (no such function; the dispatcher is
  `compute_void_fraction(AS, params)` and the models take
  `(rho_l, rho_v, x)` and return a float). Fixed in the copy as the
  **homogeneous** model `void_fraction_homogeneous(rho_l, rho_g, x)` — the
  dispatcher's default — used for the C_t correlation of the diffuser; the
  translation writes the same homogeneous formula.
- **2026-10-31 — source bug not transcribed**: `A_mb = 1/(rho_mb·v_mb·M_dot)`
  in `solve()` (wrong dimensions; overwritten by the correct
  `m_dot/(rho·v)` inside `suction_chamber()` before any use) — only the
  correct definition is written.
- **2026-10-31 — naming**: the sound-speed variable `a_mb` of the source is
  renamed `a_sound_mb` (EES names are case-insensitive: `a_mb` would collide
  with the area `A_mb`); the motive-nozzle closure is h_mb = h_f(P_b_sonic) —
  the exact point its solver converges to — not v_mb = a_mb (no root; see
  *Model*).
- **Level**: equations 76 (< 50? no: 50–300 → 1); largest block 11 (> 30? no:
  6–30 → 2); functions/arrays none → 0; multi-zone/≥ 3 coupled components
  (nozzle + nozzle + mixing + diffuser) → 1; semi-empirical constant
  efficiencies → 1; curated guesses (`.initials`) → 1. Score 6 → **level 3**.

## Limitations and CoolSolve gaps

- Constant-efficiency semi-empirical model: the "choking" pressure is in
  practice the saturated-liquid boundary of the motive-nozzle exit state (the
  source's own root), and the exit flow is subsonic there (v_mb − a_mb =
  +11.7 m/s at the solution); the diffuser enthalpy definition is not
  energy-conserving (+0.11 %, see *Results*). Both behaviours are faithful to
  the source; use with care outside its calibration envelope.
- No CoolSolve gap blocks the model (`missing_features` empty). No new gap
  registered; solver steering needed `.initials` and `coolsolve.conf`
  (documented under *How to run*), which is solver usage, not a language gap.

## Related models

- CSL-0118 (air nozzle ejector): ideal-gas air ejector (subsonic orifice-type
  nozzle, momentum mixing, diffuser efficiency) — nearest library model; this
  model adds the two-phase real-fluid physics (HEM sound speed, saturation
  boundary, quality and void fraction at mixing and exhaust).
- CSL-0014 (hx_constant_pinch): other LaboThapPy translation on R744
  (transcritical CO2 gas-cooler side component).

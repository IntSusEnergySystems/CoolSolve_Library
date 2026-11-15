#!/usr/bin/env python3
"""Build sources/ees_library/{curation.csv,inventory.csv} for the F-Chart EES
example library (~/Nextcloud/thermo_models/EES_library).

Runs sources/thermo_models/sweep.py on the EES_library folder (read-only),
applies the curation table below (one row per file, keyed by path), renumbers
the candidate ids to EEL-nnnn and sets source=ees_library, and merges the
decision/library_id workflow columns from an existing inventory.csv.

The DECISION dict is the triage of 2026-11-11 (maintainer to review):
  decision in {todo, discarded, duplicate, merged}
"""
import csv, subprocess, sys, tempfile
from pathlib import Path

LIB = Path('/sylvain/mount/git/CoolSolve_Library')
SWEEP = LIB / 'sources/thermo_models/sweep.py'
ROOT = Path('/sylvain/Nextcloud/thermo_models/EES_library')
OUT = LIB / 'sources/ees_library'

# path -> (title, description, category, kind, level, priority, decision, notes)
# decision: todo / discarded / duplicate / merged  (library_id left empty)
C = {}

def add(path, title, desc, cat, kind, lvl, pri, dec, notes=''):
    C[path] = dict(title=title, description=desc, category_guess=cat, kind_guess=kind,
                   level_guess=lvl, priority=pri, decision=dec, notes=notes)

# ---------------- language / solver / units feature demos (discarded) ----------------
add('$export_import.ees', '$IMPORT/$EXPORT directive demo', 'Feature demo of the $IMPORT and $EXPORT directives and clipboard exchange; no model.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'EES feature not planned for CoolSolve')
add('$IF StringVariable.EES', '$IF on string variables demo', 'Conditional compilation with $IF on string variables set in the Equations window or Parametric table.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('$IF StringVariable2.EES', '$IF string directive demo 2', 'Second demo of conditional compilation with $IF on strings.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('$IFNOT directive.EES', '$IFNOT directive demo', 'Trivial equation set demonstrating the $IFNOT directive.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('$reference.ees', '$REFERENCE directive demo', 'Changing the default enthalpy/entropy reference state of a fluid with $REFERENCE.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'CoolSolve has its own reference-state handling')
add('$savetable.ees', '$SAVETABLE demo', 'Feature demo of $SAVETABLE with the CONCAT$ and EESFILEDIR$ string functions.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('$Warning.EES', '$Warnings directive demo', 'Turning solver warnings on/off with $Warnings.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('ArrayRange_Notation.EES', 'Array range notation demo', 'Demonstration of the array range notation.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('AvoidLogProblem.EES', 'Solver behaviour demo', 'How EES handles a zero logarithm during iteration; no model.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('BasicEqn.EES', 'Basic equation demo', 'Trivial equation set used to introduce the Equations window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Complex_withSubprograms.EES', 'Complex-mode subprogram demo', 'Calling a Subprogram configured in complex mode from a real main program.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('complexroots.EES', 'Complex roots demo', 'Roots of a polynomial with EES complex mode.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Convert.EES', 'Convert function demo', 'Unit conversion with the CONVERT function.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('DOLAST directive.EES', '$DOLAST directive demo', 'Controlling the order of equation evaluation with $DOLAST.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('FindingtheLimit.EES', 'Integral limit demo', 'Using the Integral command to determine an integration limit (pure math).', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('globalConstant.EES', '$Constant directive demo', 'Global constants with $Constant used in array declarations and loops.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'CS-GAP-CONSTANT closed on the CoolSolve side')
add('iftest.ees', 'User function demo', 'IF-THEN-ELSE logic in user-written functions; no physical model.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Matrix.ees', 'Matrix product demo', '3x3 matrix product with DUPLICATE and SUM; pure linear algebra.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Matrix2.ees', 'Matrix operations demo (manual ch. 7)', 'Matrix operations example of the EES manual; pure linear algebra.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Modules.EES', 'Module demo', 'Demonstration of MODULES solving implicit equation sets.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Modules&Subprograms.EES', 'Modules and subprograms demo', 'Differences between MODULES and SUBPROGRAMS.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Singularity.EES', 'Singular equation set demo', 'How EES handles singular equation sets; no physical model.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('TabStops.EES', '$TabStops demo', 'Tab spacing control in the Equations window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Trace.EES', '$Trace directive demo', 'Displaying intermediate solver results with $Trace.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('UnitConversion F=ma.EES', 'Unit checking demo (F=ma)', 'Unit conversion and checking with Newton law in English units ($CheckUnits).', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Dinner.ees', 'Word problem (restaurant bill)', 'Algebraic word problem used to introduce equation solving; no engineering content.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Ch1ex.ees', 'R134a throttle (chapter-1 exercise)', 'Determination of the outlet state of an R134a throttle; used to introduce property calls and plots.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'duplicate physics of Throttle.EES; kPa/kJ; trivial')
add('Dbl_intg.ees', 'Double integral demo', 'Two-variable integration of an analytic function; pure math.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('DFQ_1.ees', 'Three integral-method demo', 'Three ways of writing the same ODE with the Integral function (pure math).', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Substeps.ees', '$IntegralTable step demo', 'Second-order ODE with small integration steps reported at larger intervals; pure math.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('ShootingMethod_DFQ.EES', 'Shooting method demo', 'Shooting method for a 2nd-order BVP with the Integral function; pure math.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('drag.ees', 'Projectile with drag (ODE demo)', 'Second-order ODE (ballistics with drag) used to demonstrate the Integral function; no substance properties.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Rk4_test.ees', 'Runge-Kutta library function demo', 'Using the EES RK4 library function on a test ODE; pure math.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('periodic_steady_state.EES', 'Macro REPEAT/UNTIL demo', 'Professional-version macro that iterates a transient to periodic steady state; macro feature discarded.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'macro; diagram-window: yes')
add('testmacrocycle.EES', 'Macro cycle demo', 'Macro command file cycling calculations; Professional feature.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'macro')
add('testinclude.EES', '$INCLUDE demo', 'Purpose of the file is explained only in the Diagram window; $INCLUDE demonstration.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('Excel_ees.ees', 'EES-Excel DDE demo', 'Calling EES from Excel with DDE and macros; Professional feature.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'DDE/macro')
add('testexcelmacro.EES', 'Excel macro demo', 'EES macro exchanging data with Excel.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'macro')
add('curvefit.ees', 'CurveFit1D demo', 'Polynomial fits of order 1-6 with the CURVEFIT1D procedure; regression feature demo.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('LinearRegression.EES', 'Linear regression demo', 'Polynomial fit of compressor map data with the Linear Regression command (menu feature).', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Nlinrg.ees', 'Non-linear regression demo', 'Regression of lookup-table data by minimising the RMS error with Min/Max.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('genetic_test1.EES', 'Genetic optimisation demo', 'Test of the genetic optimisation method on a toy problem.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Uncertainty.EES', 'Uncertainty propagation demo', 'Flat-plate convection with uncertainty estimates (uncertainty analysis feature).', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'uncertainty propagation not planned in CoolSolve')
add('errorbars.EES', 'Uncertainty table and error bars demo', 'Relative-humidity uncertainty from T/wet-bulb uncertainties; plotting feature.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Degreedays.EES', 'Degree-days parametric demo', 'Computes heating degree-days to demonstrate variable start/stop rows in the Parametric table (Professional feature).', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes (mentioned); degree-day concept itself is trivial')
add('Copper.ees', 'Lookup table interpolation demo (copper)', 'INTERPOLATE/Differentiate and curve-fit of copper property data in a Lookup table; feature demo.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Tungsten.EES', '2-D matrix interpolation demo (tungsten)', 'INTERPOLATE2DM on spectral emittance of tungsten; feature demo on tabulated data.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Prop2.EES', 'Parametric table / property demo', 'Property evaluations in a Parametric table; feature demo.', 'feature-demo', 'demo', 1, 'skip', 'discarded', '')
add('Prop3.ees', 'Steam property demo (SI/English)', 'Steam properties in SI and English units; feature demo.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes (mentioned)')

# ---------------- diagram / GUI / plotting / animation demos (discarded) ----------------
add('Diagram_FormattedText.EES', 'Diagram formatted-text demo (Otto)', 'Otto-cycle air-standard equations used to demonstrate formatted text in the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes; the Otto model itself is covered by the library air_standard_cycles')
add('Diagram_graphics_control.EES', 'Diagram graphics control demo', 'Controlling Diagram-window graphics (boxes, lines, circles) from equations.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('Diagram_IN_OUT.EES', 'Diagram input/output demo', 'Making Diagram-window variables either inputs or outputs.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('Diagram_window_sliders.EES', 'Diagram slider demo (Wiebe engine)', 'SI engine heat release (Wiebe) with slider inputs in the Diagram window; the model substance duplicates CSL-0024.', 'feature-demo', 'demo', 2, 'skip', 'discarded', 'diagram-window: yes (sliders); duplicate-likely CSL-0024 (crank-angle Wiebe)')
add('ChildDiagramWindows.EES', 'Child diagram windows demo', 'Several levels of child diagram windows (Professional feature).', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('DiagrmW.ees', 'Diagram window demo (throttle)', 'R134a throttle used to demonstrate the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('Input-Output.EES', 'Diagram input-output demo', 'Two equations demonstrating input/output flexibility of Diagram-window variables.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('guesses.EES', 'Guess values diagram demo', 'Diagram window illustrating how guess values affect the solution of one non-linear equation.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('Moveable_Figures.EES', 'Moveable figures demo', 'Graphics that can be dragged in the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('Links.EES', 'Diagram link demo', 'Links between diagram windows.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('Link_Return.EES', 'Diagram return-link demo', 'Return links between diagram windows.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('checkboxexample.EES', 'Check-box demo', 'Check-box control of the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('radiogroupexample.EES', 'Radio-group demo', 'Radio-button group control of the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes')
add('MakePlot.EES', 'Plot-window demo', 'Creating a plot window from equation data.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'plot demo')
add('3-d plot.ees', '3-D plot demo', 'Demonstration of 3-D plotting.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'plot demo')
add('3D Points Plot.EES', '3-D points plot demo', '3-D scatter plotting demo.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'plot demo')
add('PolarPlots.EES', 'Polar plot demo', 'Polar plotting of wind data (Professional feature).', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'plot demo')
add('Plot_strings.EES', 'Plot strings demo', 'String labels in plot windows.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'plot demo')
add('Plot_in_Diagram.EES', 'Plot in diagram demo (throttle)', 'R134a throttle with plots embedded in the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'diagram-window: yes; plot demo')
add('Indicated power.EES', 'Plot smoothing demo', 'Smoothing option of the plot window on indicated-power data (equations absent).', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'plot demo; data only')
add('Indicated power (1).EES', 'Plot smoothing demo (copy)', 'Exact copy of Indicated power.EES.', 'feature-demo', 'demo', 1, 'skip', 'duplicate', 'intra-collection exact copy')
add('Animation.EES', 'Animation demo', 'Diagram-window animation demo (no equations).', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'animation; diagram-window: yes')
add('avi_test.EES', 'AVI animation demo', 'Video animation test (no equations).', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'animation')
add('ball.EES', 'Bouncing ball animation', 'Ballistic animation driven from equations.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'animation; diagram-window: yes')
add('Beer.EES', 'Beer bubbles animation', 'CO2 bubble rise in beer (Stokes drag) animated in the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'animation; diagram-window: yes; RTF equations text')
add('projectile.EES', 'Projectile game animation', 'Projectile with wind and drag hitting a target in the Diagram window.', 'feature-demo', 'demo', 1, 'skip', 'discarded', 'animation/game; diagram-window: yes')
add('air compressor.EES', 'Air compressor animation', 'Reciprocating air compressor animated in the Diagram window (S.A. Klein 2004).', 'feature-demo', 'demo', 2, 'skip', 'discarded', 'animation; diagram-window: yes; physics covered by machines/ compressors')
add('2-stroke engine.EES', 'Two-stroke engine animation', 'Crank-angle scavenged Otto cycle (procedure with TableValue lookups) animated in the Diagram window.', 'feature-demo', 'demo', 2, 'skip', 'discarded', 'animation; diagram-window: yes; RTF; air-standard cycles covered')
add('4-stroke engine.EES', 'Four-stroke engine animation', 'Crank-angle four-stroke Otto cycle animated in the Diagram window.', 'feature-demo', 'demo', 2, 'skip', 'discarded', 'animation; diagram-window: yes; air-standard cycles covered')
add('Diesel engine.EES', 'Diesel engine animation', 'Crank-angle four-stroke Diesel cycle animated in the Diagram window.', 'feature-demo', 'demo', 2, 'skip', 'discarded', 'animation; diagram-window: yes; air-standard cycles covered')
add('Water change in phase.EES', 'Water phase change animation', 'Piston-cylinder water heated through saturation, animated in the Diagram window; also uses the rho_() solid-property function.', 'feature-demo', 'demo', 2, 'skip', 'discarded', 'animation; diagram-window: yes; physics covered by CSL-0176 piston-cylinder')

# ---------------- intra-collection duplicates ----------------
add('2-D Conduction (1).EES', '2-D conduction (copy)', 'Exact copy of 2-D Conduction.EES.', 'heat_transfer/conduction_radiation', 'steady', 2, 'skip', 'duplicate', 'intra-collection exact copy of EEL 2-D Conduction.EES')
add('Regen_minmax (1).EES', 'Regenerative Rankine Min/Max (copy)', 'Exact copy of Regen_minmax.EES.', 'power_cycles/steam_advanced', 'optimization', 2, 'skip', 'duplicate', 'intra-collection exact copy of EEL Regen_minmax.EES')
add('Difeqn2.ees', 'Lumped capacitance (method 2)', 'Same lumped-capacitance cooling problem as Difeqn1.ees, solved with a different integral formulation.', 'fundamentals/tanks_vessels', 'dynamic', 1, 'skip', 'duplicate', 'same physical model as Difeqn1.ees')

# ---------------- import candidates (todo) ----------------
add('2-D Conduction.EES', 'Two-dimensional steady conduction in a square plate',
    'Finite-difference 2-D steady temperature field in a square plate with two edges at 100 C, one at 0 C and one insulated; 2-D arrays, contour/3-D plots.',
    'heat_transfer/conduction_radiation', 'steady', 2, 'medium', 'todo',
    'no library counterpart (CSL-0106 is resistances/shape factors only); no diagram window detected')
add('Transient Conduction through a Plane Wall.EES', 'Transient conduction in a plane wall with convection',
    '1-D transient conduction (wall initially uniform, convective boundary at t=0): separation-of-variables series solution compared with the numerical integral solution.',
    'heat_transfer/conduction_radiation', 'dynamic', 2, 'medium', 'todo',
    'dynamic kind; complements CSL-0106 (steady resistances)')
add('Blasius.EES', 'Blasius flat-plate boundary-layer solution',
    'Classic Blasius problem: laminar flow over a flat plate solved as a 2nd-order BVP with the Integral function and guess values (shooting); gives the skin-friction and delta growth.',
    'heat_transfer/external_convection', 'dynamic', 2, 'high', 'todo',
    'no library counterpart; the library has external-convection correlations (functions) but not the ODE solution; classic validation case (f"(0)=0.332)')
add('von Karman.EES', 'von Karman viscous pump',
    "von Karman's viscous pump (White, Viscous Fluid Flow, 2005, p.162): three coupled ODEs f, g, h solved with the Integral function; famous rotating-disk BVP.",
    'heat_transfer/external_convection', 'dynamic', 3, 'high', 'todo',
    'no library counterpart; rotating disk / viscous pump; reference values in White')
add('Convect.ees', 'Flat-plate convection exercise',
    'Heat transfer between air and a flat plate with convection formulae relying on transport properties (Pr from built-in function); EES teaching exercise.',
    'heat_transfer/external_convection', 'steady', 1, 'low', 'todo',
    'duplicate-likely: the library already has external-convection function libraries (ht source, CSL correlations); kPa/kJ units')
add('moody.ees', 'Churchill friction factor (user function)',
    'User-written function computing the pipe friction factor with the Churchill (1977) correlation spanning all flow regimes.',
    'heat_transfer/pressure_drop', 'function', 1, 'low', 'todo',
    'duplicate-likely CSL-0018 (Colebrook-White) and CSL-0130 (friction factors); check whether Churchill is already covered before importing')
add('Blackbody.EES', 'Blackbody band-fraction calculator',
    'Fraction f_1_2 of blackbody emissive power between two wavelengths (Planck law integral); inputs entered on the Diagram window.',
    'heat_transfer/conduction_radiation', 'function', 1, 'low', 'todo',
    'diagram-window: yes (inputs; not imported, gap CS-GAP-DIAGRAM-WINDOW to register); duplicate-likely CSL-0107 (radiation function library) - check band fraction coverage')
add('Heatex.ees', 'Counterflow heat exchanger effectiveness',
    'Counterflow HX: effectiveness and outlet temperatures from known LMTD, inlet temperature and capacity rates.',
    'heat_exchangers/methods', 'steady', 1, 'low', 'todo',
    'duplicate-likely CSL-0002 / CSL-0090 (eps-NTU); textbook exercise, kPa/kJ units')
add('runaround_HX.EES', 'Run-around heat-recovery loop (convergence lesson)',
    "Run-around loop between a hot and a cold stream: overall effectiveness with known capacity rates and HX effectivenesses; demonstrates guess values and block-wise convergence.",
    'heat_exchangers/methods', 'steady', 2, 'low', 'todo',
    'duplicate-likely CSL-0162 (glycol run-around loop); keep only for the convergence-teaching angle; diagram-window: yes (schematic; not imported)')
add('Rankine.ees', 'Regenerative Rankine cycle with optimum extraction pressure',
    'Regenerative Rankine cycle (one open feedwater heater); find the extraction pressure maximising the thermal efficiency with Min/Max; pumps and turbine ideal.',
    'power_cycles/steam_advanced', 'optimization', 2, 'medium', 'todo',
    'English units (psia) - convert by hand; Min/Max not in CoolSolve (optimisation kind, blocked-likely); diagram-window: yes (not imported); analytic optimum as verification')
add('Regen.ees', 'Regenerative Rankine cycle with two feedwater heaters',
    'Rankine cycle with two closed feedwater heaters; effect of the FWH pressures on efficiency (parametric study, unit steam flow).',
    'power_cycles/steam_advanced', 'steady', 2, 'low', 'todo',
    'English units; duplicate-likely the library steam_advanced models; check before importing')
add('Regen_minmax.EES', 'Regenerative Rankine with two FWHs (Min/Max)',
    'Same cycle as Regen.ees with the two FWH pressures optimised with Min/Max.',
    'power_cycles/steam_advanced', 'optimization', 2, 'low', 'todo',
    'English units; Min/Max gap (optimisation kind); near-duplicate of Regen.ees')
add('SteamCyc.ees', 'Reheat Rankine cycle (Cengel & Boles 9.26)',
    'Ideal reheat Rankine cycle (8 MPa/500 C, reheat at 3 MPa to 500 C, condenser 20 kPa); textbook exercise.',
    'power_cycles/steam_basic', 'steady', 1, 'low', 'todo',
    'statement from Cengel & Boles (paraphrase + credit; needs-permission like thermo_kuleuven); duplicate-likely the library steam_basic family; diagram-window: yes (mentioned)')
add('Gas Turbine System.EES', 'Simple gas turbine (English units)',
    'Simple gas turbine cycle: compressor pressure ratio 14, isentropic efficiencies 83/87 %, turbine inlet 2500 R; net power and efficiency.',
    'power_cycles/gas_turbine_design', 'steady', 1, 'low', 'todo',
    'English units (R/psia) - convert by hand; duplicate-likely CSL-0204/CSL-0141/CSL-0050 family; diagram-window: yes (schematic; not imported)')
add('Refrig.ees', 'Vapour-compression refrigeration cycle (R134a)',
    'Simple R134a vapour-compression cycle with built-in property tables; COP vs evaporator temperature; P-h plot overlay.',
    'refrigeration_heat_pumps/refrigeration_cycles', 'steady', 1, 'low', 'todo',
    'duplicate-likely CSL-0001; RTF equations text; kPa/kJ units')
add('Refrig_pro.EES', 'Vapour-compression refrigeration cycle (R134a, diagram)',
    'Same simple R134a cycle as Refrig.ees with inputs in the Diagram window.',
    'refrigeration_heat_pumps/refrigeration_cycles', 'steady', 1, 'low', 'todo',
    'diagram-window: yes (not imported); duplicate-likely CSL-0001')
add('capvst.ees', 'Heat pump with effectiveness heat exchangers',
    'R134a heat pump cycle with effectiveness-based evaporator/condenser (alpha/beta kW/K), isentropic compressor with volumetric flow; COP vs outdoor temperature.',
    'refrigeration_heat_pumps/heat_pump_cycles', 'steady', 2, 'medium', 'todo',
    'decimal-comma file (European locale) and kPa/kJ units - convert; classic effectiveness-cycle teaching model')
add('Absorp.ees', 'Ammonia-water absorption cycle (external DLL)',
    'Single-effect NH3/H2O absorption refrigeration cycle using an external EES DLL procedure for the mixture properties.',
    'refrigeration_heat_pumps/absorption', 'steady', 3, 'low', 'todo',
    'external-procedure call (CoolSolve gap) but the built-in nh3h2o module may replace it (see CSL-0249 which is duplicate-likely); check before importing')
add('Supermkt.ees', 'Supermarket cooling system with bypass',
    'Supermarket refrigeration/HVAC system with bypass and psychrometric functions; one of two examples of Klein & Al-Habdan, CAEE vol 1(3) 1993, 265-275.',
    'refrigeration_heat_pumps/refrigeration_systems', 'steady', 2, 'high', 'todo',
    'unique integrated system model, no library counterpart; credit the CAEE paper (needs-permission for the statement); diagram-window: yes (problem statement shown there; not imported)')
add('Maxpower.ees', 'Carnot engine at maximum power (Curzon-Ahlborn)',
    'Efficiency of an endoreversible Carnot engine with finite heat-transfer rate limits, optimised for maximum power with EES Min/Max.',
    'fundamentals/second_law', 'optimization', 2, 'medium', 'todo',
    'Min/Max gap (optimisation kind); diagram-window: yes (not imported); analytic Curzon-Ahlborn value as verification')
add('nozzle.EES', 'Converging-diverging nozzle with guess-value chaining',
    'Isentropic flow of air through a converging-diverging nozzle: area-Mach relation solved by setting guess values of one variable to another (choking).',
    'components/nozzles_ejectors', 'steady', 2, 'low', 'todo',
    'duplicate-likely CSL-0310 (isentropic nozzle, choked/unchoked); the guess-value lesson is CoolSolve-relevant (initials file)')
add('Throttle.EES', 'R134a throttle with kinetic energy',
    'Outlet state of a refrigerant throttle including kinetic energy; inputs normally set in the Diagram window ($IFNOT DiagramWindow).',
    'components/piping_valves', 'steady', 1, 'low', 'todo',
    'diagram-window: yes (inputs; not imported); kPa/kJ; duplicate-likely the library valve exercises')
add('psych.EES', 'Psychrometric property calculator',
    'Atmospheric-air properties from pressure and any two of relative humidity, dry-bulb, wet-bulb, humidity ratio, dew-point (238 equations); inputs and substance selection on the Diagram window.',
    'hvac/psychrometrics', 'function', 2, 'medium', 'todo',
    'diagram-window: yes (not imported); string $IF selection likely hits CS-GAP-IF-NO-CONSTANT - expect a _coolsolve variant per property pair; valuable as a psychrometrics function library')
add('Property_Calculator.EES', 'Multi-fluid property calculator',
    'Properties of water, ammonia, R12, R134a, R22... from any two independent intensive properties (Procedure Find, 162 equations); substance selected on the Diagram window.',
    'fundamentals/property_libraries', 'function', 2, 'low', 'todo',
    'diagram-window: yes (not imported); $IF string selection - CS-GAP-IF-NO-CONSTANT; overlaps the CoolSolve GUI property calculator; import only as a function library if at all')
add('sonic_v.EES', 'Speed of sound by entropy perturbation (function)',
    'User function V_sonic computing the speed of sound from an isentropic density perturbation, unit-system aware (UnitSystem function).',
    'fundamentals/property_libraries', 'function', 1, 'low', 'todo',
    'UnitSystem() built-in function - check CoolSolve support (CS-GAP-UNITSYSTEM is about the directive; the function may need a new gap/row); small function-library candidate')
add('Solid-Liquid_Props.EES', 'Solid-property library demo',
    'Demonstrates the EES Solid-Liquid property library functions (k_, rho_, c_, mu_, beta_, E_, alpha_, nu_) for metals and other solids.',
    'fundamentals/properties', 'function', 1, 'medium', 'todo',
    'blocked: EES solid-property functions not in CoolSolve - register new gap (ties into the CoolSolve solid-phase design study, docs/solid_phase_properties.md); interesting anchor model for a materials/mechanics domain')
add('Steam_flow vectors.EES', 'Impulse-turbine velocity triangles (complex numbers)',
    'Single-stage impulse turbine: minimum steam flow, blade and stage efficiency from velocity triangles represented as complex numbers ($Complex On).',
    'machines/turbomachine_design', 'steady', 3, 'medium', 'todo',
    'blocked: $Complex complex-number mode not in CoolSolve - register new gap; steam_nbs fluid name; velocity-triangle models absent from the library otherwise; diagram-window: yes (notation)')
add('spring.EES', 'Spring-loaded piston-cylinder dynamics (helium)',
    'Latched piston released against a compressed spring in an insulated cylinder: damped oscillation of the helium until rest (friction), energy balance and entropy generation.',
    'fundamentals/piston_cylinders', 'dynamic', 2, 'medium', 'todo',
    'dynamic kind; animation output (not imported, gap); Cengel-type statement; complements CSL-0210 (quasi-static spring-loaded piston)')
add('gas spring.EES', 'Gas-spring oscillator (ball on a gas column)',
    'Steel ball oscillating on an air column in a glass tube: real-gas spring with damping, solved with the Integral function.',
    'fundamentals/piston_cylinders', 'dynamic', 2, 'medium', 'todo',
    'dynamic kind; animation output (not imported, gap); mmHg/atmosphere units; no library counterpart')
add('Difeqn1.ees', 'Lumped-capacitance cooling',
    'Single lump at 400 C cooling in a 20 C medium: ODE solved with the Integral function and a Parametric table.',
    'fundamentals/tanks_vessels', 'dynamic', 1, 'low', 'todo',
    'dynamic kind; simplest transient; check overlap with the library dynamic models before importing')
add('adiabatic_combustion.EES', 'Adiabatic flame temperature with guess values',
    'Octane burned with 30 % excess air: complete, adiabatic combustion exit temperature; illustrates the importance of guess values.',
    'fundamentals/combustion', 'steady', 1, 'low', 'todo',
    'ideal-gas combustion species (enthalpy(O2),...) - CS-GAP-FLUIDS-NASA-SPECIES (blocked-likely); duplicate-likely CSL-0046 (octane, 400 % air)')
add('Flamet.ees', 'Adiabatic flame temperature of methane (JANAF)',
    'CH4 with 0-200 % excess air: adiabatic flame temperature without dissociation using the built-in JANAF species properties; parametric study.',
    'fundamentals/combustion', 'steady', 1, 'low', 'todo',
    'JANAF species - CS-GAP-FLUIDS-NASA-SPECIES (blocked-likely); duplicate-likely CSL-0150/CSL-0046')
add('ChemEq.EES', 'Chemical equilibrium by the law of mass action',
    'Octane with 120 % theoretical air at 1850 K, 1 bar: equilibrium mole fractions of CO2, CO, H2O, N2, O2, NO from equilibrium-constant equations (law of mass action).',
    'fundamentals/combustion', 'steady', 2, 'high', 'todo',
    'ideal-gas species properties (CS-GAP-FLUIDS-NASA-SPECIES, blocked-likely); note the g|o_CO2 variable-name syntax (| in names); anchor model for the chemical-reaction domain; self-contained once species data exist')
add('ChemEq_converge.EES', 'Chemical equilibrium, 11 species (robust convergence)',
    'Same combustion equilibrium extended to 11 species (incl. H2, OH, H, O, N) with a staged initialisation for robust convergence.',
    'fundamentals/combustion', 'steady', 3, 'medium', 'todo',
    'same NASA-species gap; the staged-guess strategy is a valuable convergence showcase')
add('janaf.ees', 'Chemical equilibrium with JANAF/NASA data',
    'Octane with 120 % theoretical air: equilibrium using the NASA external procedure and JANAF table data for species enthalpies and Gibbs energies.',
    'fundamentals/combustion', 'steady', 2, 'medium', 'todo',
    'NASA external procedure + JANAF species - CS-GAP-FLUIDS-NASA-SPECIES and external-procedure gap (the NASA call is redundant in EES >= 8, per the file comments)')
add('LaGrange.EES', 'Chemical equilibrium by Lagrange multipliers',
    'Same octane/120 % air equilibrium solved with the Lagrange method of undetermined multipliers (no optimisation command needed).',
    'fundamentals/combustion', 'steady', 3, 'high', 'todo',
    'ideal-gas species properties (CS-GAP-FLUIDS-NASA-SPECIES, blocked-likely); elegant fully-equation-based method; pairs with ChemEq.EES and min_G.EES as a three-method set')
add('min_G.EES', 'Chemical equilibrium by Gibbs minimisation',
    'Same equilibrium found by directly minimising the total Gibbs function with Min/Max (two degrees of freedom).',
    'fundamentals/combustion', 'optimization', 3, 'medium', 'todo',
    'NASA-species gap + Min/Max gap (optimisation kind); third of the three-method set')
add('compressorMap.EES', 'Compressor map 2-D interpolation',
    'Compressor power and mass flow from a 2-D map (evaporator/condenser saturation temperatures) with INTERPOLATE2D on the companion lookup table.',
    'machines/compressor_maps', 'function', 2, 'low', 'todo',
    'blocked: CS-GAP-INTERP2D (scattered 2-D interpolation); companion compressorMap.lkt (EEL row below) must be converted to CSV; English-unit map (degF); duplicate-likely CSL-0035 (lookup-table map)')
add('compressorMap.lkt', 'Compressor map lookup table',
    'Lookup table of compressor power and mass flow vs saturation temperatures; companion of compressorMap.EES.',
    'machines/compressor_maps', 'function', 2, 'skip', 'merged',
    'merged with compressorMap.EES (EEL row above)')

COLUMNS = ['candidate_id','source','path','companion_files','title','description','category_guess','kind_guess',
           'level_guess','language','format','ees_version','n_lines','n_equations','features','unit_hints','fluids',
           'doc_quality','duplicate_group','is_representative','priority','license_status','authors','notes',
           'ees_units','stored_solution','tables','decision','library_id']
CUR_COLS = ['key','scope','title','description','category_guess','kind_guess','level_guess','priority',
            'license_status','authors','notes','doc_quality','language']

# ---- run sweep into a temp dir with our curation ----
tmp = Path(tempfile.mkdtemp(prefix='eeslib_'))
with open(tmp/'c.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=CUR_COLS)
    w.writeheader()
    for path, c in sorted(C.items()):
        w.writerow(dict(key=path, scope='file', title=c['title'], description=c['description'],
                        category_guess=c['category_guess'], kind_guess=c['kind_guess'],
                        level_guess=c['level_guess'], priority=c['priority'], license_status='fchart-mit',
                        authors='S.A. Klein / F-Chart Software', notes=c['notes'], doc_quality='', language='en'))
r = subprocess.run([sys.executable, str(SWEEP), '--root', str(ROOT), '--out', str(tmp),
                    '--curation', str(tmp/'c.csv')], capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
rows = list(csv.DictReader(open(tmp/'inventory.csv', newline='', encoding='utf-8')))
print('sweep rows:', len(rows))

# ---- renumber EEL-, set source, attach decisions ----
prev = {}
if (OUT/'inventory.csv').exists():
    for p in csv.DictReader(open(OUT/'inventory.csv', newline='', encoding='utf-8')):
        prev[' '.join(p['path'].split())] = p
rows.sort(key=lambda r: r['path'].lower())
missing = []
for i, row in enumerate(rows, 1):
    cid = 'EEL-%03d' % i
    key = ' '.join(row['path'].split())
    c = C.get(key)
    if c is None:
        missing.append(key)
        decision, notes = 'todo', 'TRIAGE MISSING - review'
    else:
        decision, notes = c['decision'], c['notes']
    if key in prev and prev[key].get('decision') not in ('', 'todo', None):
        decision = prev[key]['decision']           # workflow column preserved (added/merged/duplicate/discard decisions)
        if prev[key].get('library_id'):
            row['library_id'] = prev[key]['library_id']
    row['candidate_id'] = cid
    row['source'] = 'ees_library'
    row['decision'] = decision
    # sweep.py forces license_status='own' (maintainer decision 2026-10-04 for the ULiege
    # collection); this source is F-Chart content -> restore the curation value
    if c is not None:
        row['license_status'] = 'fchart-mit'
        row['authors'] = 'S.A. Klein / F-Chart Software'
    # append our triage note to the sweep notes (keep both)
    sw = row.get('notes', '')
    row['notes'] = (sw + ('; ' if sw and notes else '') + notes) if notes else sw
    row['companion_files'] = 'compressorMap.lkt' if key == 'compressorMap.EES' else row.get('companion_files','')

if missing:
    print('MISSING CURATION:', missing)

OUT.mkdir(exist_ok=True)
with open(OUT/'inventory.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS)
    w.writeheader(); w.writerows(rows)

# also write the curation.csv next to the script (stable, re-runnable)
with open(OUT/'curation.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=CUR_COLS)
    w.writeheader()
    for path, c in sorted(C.items()):
        w.writerow(dict(key=path, scope='file', title=c['title'], description=c['description'],
                        category_guess=c['category_guess'], kind_guess=c['kind_guess'],
                        level_guess=c['level_guess'], priority=c['priority'], license_status='fchart-mit',
                        authors='S.A. Klein / F-Chart Software', notes=c['notes'], doc_quality='', language='en'))

import collections
cnt = collections.Counter(r['decision'] for r in rows)
cnt2 = collections.Counter(r['priority'] for r in rows if r['decision'] == 'todo')
print('decisions:', dict(cnt))
print('todo priorities:', dict(cnt2))
print('wrote', OUT/'inventory.csv', len(rows), 'rows and curation.csv', len(C), 'rows')

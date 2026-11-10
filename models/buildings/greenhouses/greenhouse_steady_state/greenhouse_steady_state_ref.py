#!/usr/bin/env python3
"""Reference solve of CSL-0333 (scipy). Same equations as the .eescode.

    python3 greenhouse_steady_state_ref.py

Needs numpy and scipy. Prints the design-point solution, its wall time, and
the max relative difference against greenhouse_steady_state.sol when that
file is present.
"""
import math
import time
from pathlib import Path

from scipy.optimize import root

sigma = 5.67e-8
g = 9.81
R = 8314.0
M_H2O = 18.0
dh = 2.45e6
phi = 25.0
h_air = 3.8
l_pip = 2.232
d_pip = 0.051
eps_cov, eps_can, eps_flr, eps_pip = 0.84, 1.0, 0.89, 0.88
tau_covPAR = tau_covNIR = 0.85
rho_covPAR = rho_covNIR = 0.13
U_leaf = 5.0
LAI = 1.06
rho_canPAR, rho_canNIR = 0.07, 0.35
K1_PAR = K2_PAR = 0.7
K_NIR = 0.27
rho_flrPAR = rho_flrNIR = 0.07
lam_so, e_flr, lam_flr = 0.85, 0.02, 1.7
e_so = [0.02, 0.04, 0.08, 0.16, 0.32]
T_so_deep = 3.0
eta_RfFlr, Cd, Cw, h_ven, c_leak = 0.1, 0.75, 0.09, 0.68, 1.5e-4
c_pipFF = 0.49
rho_air, cp_air, rho_can = 1.2, 1005.0, 1.23
gamma, rb, rmin = 65.8, 275.0, 82.0
C1, C2 = 4.3, 0.54
s_sw = 11.0
eta_PAR = eta_NIR = 0.5
eta_air_G = 0.1
A_pip = math.pi * d_pip * l_pip
FF_pip = A_pip * c_pipFF
FF_can = 1 - math.exp(-0.94 * LAI)
U_flr_so1 = 2 / (e_flr / lam_flr + e_so[0] / lam_so)
U_so = [2 * lam_so / (e_so[i] + e_so[i + 1]) for i in range(4)]
U_so5 = lam_so / (e_so[4] / 2)
R_so = 1 / U_flr_so1 + sum(1 / u for u in U_so) + 1 / U_so5


def vp_sat(T):
    return -274.36 + 877.52 * math.exp(0.0545 * T)


def solar(I):
    a_par = 1 - tau_covPAR - rho_covPAR
    a_nir = 1 - tau_covNIR - rho_covNIR
    q_swr_cov = (a_par * eta_PAR + a_nir * eta_NIR) * I
    Rt = I * eta_PAR * tau_covPAR * (1 - eta_air_G)
    q_can_par = (Rt * (1 - rho_canPAR) * (1 - math.exp(-K1_PAR * LAI))
                 + Rt * math.exp(-K1_PAR * LAI) * rho_flrPAR * (1 - rho_canPAR)
                 * (1 - math.exp(-K2_PAR * LAI)))
    q_flr_par = Rt * math.exp(-K1_PAR * LAI) * (1 - rho_flrPAR)
    tau_cf = math.exp(-K_NIR * LAI) * (1 - rho_flrNIR) / (
        1 - rho_canNIR * (1 - math.exp(-K_NIR * LAI)) * rho_flrNIR)
    rho_cf = (rho_canNIR * (1 - math.exp(-K_NIR * LAI))
              + math.exp(-2 * K_NIR * LAI) * (1 - rho_flrNIR) * rho_flrNIR
              / (1 - rho_canNIR * (1 - math.exp(-K_NIR * LAI)) * rho_flrNIR))
    tau_ccf = tau_covNIR * tau_cf / (1 - rho_covNIR * rho_cf)
    rho_ccf = rho_covNIR + tau_covNIR ** 2 * rho_cf / (1 - rho_covNIR * rho_cf)
    a_can = 1 - tau_ccf - rho_ccf
    a_flr = tau_ccf
    R_nir = I * eta_NIR * (1 - eta_air_G)
    q_can = q_can_par + R_nir * a_can
    q_flr = q_flr_par + R_nir * a_flr
    q_air = eta_air_G * I * (tau_covPAR * eta_PAR + (a_can + a_flr) * eta_NIR)
    Rcan = I * (1 - eta_air_G) * (eta_PAR * tau_covPAR + eta_NIR * (a_can + a_flr))
    return q_swr_cov, q_can, q_flr, q_air, Rcan


def fluxes(T_air, T_can, T_cov, T_flr, T_pip, VP_air, T_out, RH_out, u_wind, I, T_sky, CO2, u_ven):
    q_swr_cov, q_can, q_flr, q_air, Rcan = solar(I)
    T_air_K = T_air + 273.15
    T_out_K = T_out + 273.15
    VP_out = RH_out / 100 * vp_sat(T_out)
    U_ac = 1.7 * max(1e-9, abs(T_air - T_cov)) ** 0.33 / math.cos(math.radians(phi)) ** 0.66
    q_pip = 1.99 * max(1e-9, abs(T_pip - T_air)) ** 0.32 * math.pi * d_pip * l_pip * (T_pip - T_air)
    U_ca = 2 * LAI * U_leaf
    dtf = T_air - T_flr
    U_af = (1 / (1 + math.exp(-s_sw * dtf)) * 1.7 * abs(dtf) ** 0.33
            + 1 / (1 + math.exp(s_sw * dtf)) * 1.3 * abs(dtf) ** 0.25)
    du = 4 - u_wind
    alpha = ((1 / (1 + math.exp(-s_sw * du)) * (2.8 + 1.2 * u_wind)
              + 1 / (1 + math.exp(s_sw * du)) * 2.5 * u_wind ** 0.8) / math.cos(math.radians(phi)))
    q_ac = U_ac * (T_air - T_cov)
    q_ca = U_ca * (T_can - T_air)
    q_af = U_af * (T_air - T_flr)
    q_co = alpha * (T_cov - T_out)
    q_cnd = (T_flr - T_so_deep) / R_so
    Tk = lambda T: T + 273.15
    q_cs = eps_cov * sigma * (Tk(T_cov) ** 4 - Tk(T_sky) ** 4)
    q_cc = eps_can * eps_cov * FF_can * sigma * (Tk(T_can) ** 4 - Tk(T_cov) ** 4)
    q_cf = eps_can * eps_flr * FF_can * (1 - FF_pip) * sigma * (Tk(T_can) ** 4 - Tk(T_flr) ** 4)
    q_fc = eps_flr * eps_cov * (1 - FF_pip) * (1 - FF_can) * sigma * (Tk(T_flr) ** 4 - Tk(T_cov) ** 4)
    q_pc = eps_pip * eps_can * FF_pip * FF_can * sigma * (Tk(T_pip) ** 4 - Tk(T_can) ** 4)
    q_pf = eps_pip * eps_flr * FF_pip * (1 - FF_can) * sigma * (Tk(T_pip) ** 4 - Tk(T_flr) ** 4)
    q_pv = eps_pip * eps_cov * FF_pip * (1 - FF_can) * sigma * (Tk(T_pip) ** 4 - Tk(T_cov) ** 4)
    Tm = (T_air_K + T_out_K) / 2
    f_ven = u_ven * eta_RfFlr * Cd / 2 * math.sqrt(abs(g * h_ven / 2 * abs(T_air - T_out) / Tm + Cw * u_wind ** 2))
    f_leak = max(0.25, u_wind) * c_leak
    f = f_ven + f_leak
    h_sens = rho_air * cp_air * f * (T_air - T_out)
    mv_out = M_H2O * f / R * (VP_air / T_air_K - VP_out / T_out_K)
    S = 1 / (1 + math.exp(-(Rcan - 5)))
    rI = (Rcan / (2 * LAI) + C1) / (Rcan / (2 * LAI) + C2)
    C3 = 0.5e-2 * (1 - S) + 2.3e-2 * S
    Tmin = 33.6 * (1 - S) + 24.5 * S
    C4 = 1.1e-11 * (1 - S) + 6.1e-7 * S
    C5 = 5.2e-6 * (1 - S) + 4.3e-6 * S
    rCO2 = min(1.5, 1 + C4 * (CO2 - 200) ** 2)
    rVP = min(3.8, 1 + C5 * (vp_sat(T_can) - VP_air) ** 2)
    rT = 1 + C3 * (T_can - Tmin) ** 2
    rs = rmin * rI * rCO2 * rVP * rT
    q_lat_can = 2 * rho_can * cp_air * LAI / (gamma * (rb + rs)) * (vp_sat(T_can) - VP_air)
    mv_can = q_lat_can / dh
    q_lat_cov = dh * max(0.0, 6.4e-9 * U_ac * (VP_air - vp_sat(T_cov)))
    mv_cov = q_lat_cov / dh
    return dict(q_air=q_air, q_can=q_can, q_flr=q_flr, q_cov=q_swr_cov, q_pip=q_pip,
                q_ac=q_ac, q_ca=q_ca, q_af=q_af, q_co=q_co, q_cnd=q_cnd, q_cs=q_cs,
                q_cc=q_cc, q_cf=q_cf, q_fc=q_fc, q_pc=q_pc, q_pf=q_pf, q_pv=q_pv,
                h_sens=h_sens, mv_out=mv_out, q_lat_can=q_lat_can, mv_can=mv_can,
                q_lat_cov=q_lat_cov, mv_cov=mv_cov)


def solve(I=0.0):
    """Night design point. Returns the solution dict. smooth=False, as the .eescode."""
    T_out, RH_out, u_wind, T_sky, T_air, CO2, u_ven = -10.0, 80.0, 3.0, -25.0, 18.0, 400.0, 0.0

    def residual(x):
        T_pip, T_can, T_cov, T_flr, VP = x
        q = fluxes(T_air, T_can, T_cov, T_flr, T_pip, VP, T_out, RH_out, u_wind, I, T_sky, CO2, u_ven)
        air = q["q_air"] + q["q_pip"] + q["q_ca"] - q["q_af"] - q["q_ac"] - q["h_sens"]
        can = q["q_can"] + q["q_pc"] - q["q_ca"] - q["q_lat_can"] - q["q_cc"] - q["q_cf"]
        cov = q["q_cov"] + q["q_ac"] + q["q_lat_cov"] + q["q_cc"] + q["q_fc"] + q["q_pv"] - q["q_co"] - q["q_cs"]
        flr = q["q_flr"] + q["q_pf"] + q["q_cf"] + q["q_af"] - q["q_fc"] - q["q_cnd"]
        moi = q["mv_can"] - q["mv_cov"] - q["mv_out"]
        return [air, can, cov, flr, moi]

    sol = root(residual, [60.0, 16.0, 1.0, 16.0, 700.0], method="hybr")
    if not sol.success:
        raise RuntimeError(sol.message)
    T_pip, T_can, T_cov, T_flr, VP = sol.x
    q = fluxes(T_air, T_can, T_cov, T_flr, T_pip, VP, T_out, RH_out, u_wind, I, T_sky, CO2, u_ven)
    Q = q["q_pip"] + q["q_pc"] + q["q_pf"] + q["q_pv"]
    out = dict(T_pip=T_pip, T_can=T_can, T_cov=T_cov, T_flr=T_flr, VP_air=VP, Q_pip=Q,
               K_glob=Q / (T_air - T_out), RH_air=100 * VP / vp_sat(T_air),
               q_cnv_cov_out=q["q_co"], q_rad_cov_sky=q["q_cs"], h_sens_air_out=q["h_sens"],
               q_cnd_flr_soil=q["q_cnd"], MV_can_air=q["mv_can"], MV_air_cov=q["mv_cov"],
               q_rad_flr_cov=q["q_fc"], q_lat_can_air=q["q_lat_can"], q_cnv_pip_air=q["q_pip"],
               q_rad_pip_can=q["q_pc"], q_rad_pip_flr=q["q_pf"], q_rad_pip_cov=q["q_pv"],
               q_rad_can_cov=q["q_cc"], q_rad_can_flr=q["q_cf"], q_cnv_air_cov=q["q_ac"],
               q_cnv_can_air=q["q_ca"], q_cnv_air_flr=q["q_af"], MV_air_out=q["mv_out"],
               nfev=sol.nfev)
    return out


def load_sol(path):
    values = {}
    for line in Path(path).read_text().splitlines():
        if " = " not in line:
            continue
        key, raw = line.split(" = ", 1)
        try:
            values[key.strip()] = float(raw)
        except ValueError:
            pass
    return values


if __name__ == "__main__":
    t0 = time.perf_counter()
    sol = solve(0.0)
    dt = time.perf_counter() - t0
    print(f"solve {dt:.4f} s  ({sol['nfev']} evaluations)")
    print(f"Q_pip {sol['Q_pip']:.6f} W/m2   T_pip {sol['T_pip']:.6f} C   "
          f"T_can {sol['T_can']:.6f}   T_cov {sol['T_cov']:.6f}   T_flr {sol['T_flr']:.6f}")
    print(f"VP_air {sol['VP_air']:.6f} Pa   RH_air {sol['RH_air']:.4f} %   K_glob {sol['K_glob']:.6f}")
    sol_path = Path(__file__).with_name("greenhouse_steady_state.sol")
    if sol_path.is_file():
        cs = load_sol(sol_path)
        worst = (0.0, "")
        for key, value in sol.items():
            if key == "nfev" or key not in cs:
                continue
            rel = abs(value - cs[key]) / max(abs(value), abs(cs[key]), 1e-30)
            if rel > worst[0]:
                worst = (rel, key)
        print(f"vs {sol_path.name}: max relative difference {worst[0]:.3e} on {worst[1]}")

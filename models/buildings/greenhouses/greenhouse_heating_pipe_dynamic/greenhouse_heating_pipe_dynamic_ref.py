#!/usr/bin/env python3
"""Reference integration of CSL-0335 (classical RK4, step 30 s).

    python3 greenhouse_heating_pipe_dynamic_ref.py

Needs numpy. Same equations as the .eescode: the climate fluxes of CSL-0334
with the pipe split into five water cells. Prints the wall time and the max
difference against greenhouse_heating_pipe_dynamic-integral.csv (CoolSolve,
step 60 s).
"""
import math
import time
from pathlib import Path

import numpy as np

sigma = 5.67e-8
g = 9.81
R = 8314.0
M_H2O = 18.0
R_v = 8314.0 / 18.0
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
C_air = rho_air * cp_air * h_air
C_can = 1200.0 * LAI
C_cov = 2600.0 * 840.0 * 4e-3 / math.cos(math.radians(phi))
C_flr = 2e4
C_so = [1.73e6 * e for e in e_so]
T_bar = 291.0
U12, U23, U34, U45 = U_so
N = 5
rho_w, cp_w, d_int = 1000.0, 4187.0, 0.047
V_pip = math.pi * d_int ** 2 / 4 * l_pip
C_water = rho_w * cp_w * V_pip / N


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


def fluxes(T_air, T_can, T_cov, T_flr, VP_air, T_out, RH_out, u_wind, I, T_sky, CO2, u_ven):
    """Climate fluxes with a dummy pipe temperature (the cells replace the pipe terms)."""
    q_swr_cov, q_can, q_flr, q_air, Rcan = solar(I)
    T_air_K = T_air + 273.15
    T_out_K = T_out + 273.15
    VP_out = RH_out / 100 * vp_sat(T_out)
    U_ac = 1.7 * ((T_air - T_cov) ** 2 + 1e-8) ** 0.165 / math.cos(math.radians(phi)) ** 0.66
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
    Tk = lambda T: T + 273.15
    q_cs = eps_cov * sigma * (Tk(T_cov) ** 4 - Tk(T_sky) ** 4)
    q_cc = eps_can * eps_cov * FF_can * sigma * (Tk(T_can) ** 4 - Tk(T_cov) ** 4)
    q_cf = eps_can * eps_flr * FF_can * (1 - FF_pip) * sigma * (Tk(T_can) ** 4 - Tk(T_flr) ** 4)
    q_fc = eps_flr * eps_cov * (1 - FF_pip) * (1 - FF_can) * sigma * (Tk(T_flr) ** 4 - Tk(T_cov) ** 4)
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
    q_lat_cov = dh * max(0.0, 6.4e-9 * U_ac * (VP_air - vp_sat(T_cov)))
    return dict(q_air=q_air, q_can=q_can, q_flr=q_flr, q_cov=q_swr_cov,
                q_ac=q_ac, q_ca=q_ca, q_af=q_af, q_co=q_co, q_cs=q_cs,
                q_cc=q_cc, q_cf=q_cf, q_fc=q_fc, h_sens=h_sens, mv_out=mv_out,
                q_lat_can=q_lat_can, mv_can=q_lat_can / dh, mv_cov=q_lat_cov / dh,
                q_lat_cov=q_lat_cov)


def cell_fluxes(Tw, T_air, T_can, T_cov, T_flr):
    out = []
    area = math.pi * d_pip * l_pip / N
    for T in Tw:
        qc = 1.99 * ((T - T_air) ** 2 + 1e-8) ** 0.16 * area * (T - T_air)
        Tk = T + 273.15
        rc = eps_pip * eps_can * FF_pip * FF_can * sigma * (Tk ** 4 - (T_can + 273.15) ** 4) / N
        rf = eps_pip * eps_flr * FF_pip * (1 - FF_can) * sigma * (Tk ** 4 - (T_flr + 273.15) ** 4) / N
        rv = eps_pip * eps_cov * FF_pip * (1 - FF_can) * sigma * (Tk ** 4 - (T_cov + 273.15) ** 4) / N
        out.append((qc, rc, rf, rv, qc + rc + rf + rv))
    return out


def rhs(y, tau, tab):
    T_air, T_can, T_cov, T_flr, s1, s2, s3, s4, s5, VP = y[:10]
    Tw = y[10:]
    T_out = float(np.interp(tau, tab["tau"], tab["T_out"]))
    RH = float(np.interp(tau, tab["tau"], tab["RH_out"]))
    I = float(np.interp(tau, tab["tau"], tab["I_glob"]))
    uw = float(np.interp(tau, tab["tau"], tab["u_wind"]))
    Tsky = float(np.interp(tau, tab["tau"], tab["T_sky"]))
    Tsp = float(np.interp(tau, tab["tau"], tab["T_air_sp"]))
    CO2 = float(np.interp(tau, tab["tau"], tab["CO2_air_sp"]))
    Tsu = float(np.interp(tau, tab["tau"], tab["T_su_pip"]))
    Mdot = float(np.interp(tau, tab["tau"], tab["M_dot_pip"]))
    u_ven = min(max(0.2 * (T_air - Tsp - 2.0), 0.0), 1.0)
    q = fluxes(T_air, T_can, T_cov, T_flr, VP, T_out, RH, uw, I, Tsky, CO2, u_ven)
    cells = cell_fluxes(Tw, T_air, T_can, T_cov, T_flr)
    qpip = sum(c[0] for c in cells)
    qpc = sum(c[1] for c in cells)
    qpf = sum(c[2] for c in cells)
    qpv = sum(c[3] for c in cells)
    qf = U_flr_so1 * (T_flr - s1)
    q12 = U12 * (s1 - s2)
    q23 = U23 * (s2 - s3)
    q34 = U34 * (s3 - s4)
    q45 = U45 * (s4 - s5)
    q5 = U_so5 * (s5 - T_so_deep)
    Qa = q["q_air"] + qpip + q["q_ca"] - q["q_af"] - q["q_ac"] - q["h_sens"]
    Qc = q["q_can"] + qpc - q["q_ca"] - q["q_lat_can"] - q["q_cc"] - q["q_cf"]
    Qv = q["q_cov"] + q["q_ac"] + q["q_lat_cov"] + q["q_cc"] + q["q_fc"] + qpv - q["q_co"] - q["q_cs"]
    Qf = q["q_flr"] + qpf + q["q_cf"] + q["q_af"] - q["q_fc"] - qf
    MV = q["mv_can"] - q["mv_cov"] - q["mv_out"]
    dy = [Qa / C_air, Qc / C_can, Qv / C_cov, Qf / C_flr,
          (qf - q12) / C_so[0], (q12 - q23) / C_so[1], (q23 - q34) / C_so[2],
          (q34 - q45) / C_so[3], (q45 - q5) / C_so[4],
          R_v * T_bar / h_air * MV]
    Tin = Tsu
    for i in range(N):
        dy.append((Mdot * cp_w * (Tin - Tw[i]) - cells[i][4]) / C_water)
        Tin = Tw[i]
    return dy


def rk4(tab, h=30.0, t_end=518400.0, save_every=3600.0):
    y = np.array([19, 19, 8, 16, 14, 12, 10, 8, 5, 0.8 * vp_sat(19), 40, 40, 40, 40, 40], dtype=float)
    rows = [y.copy()]
    n = int(round(t_end / h))
    every = int(round(save_every / h))
    for i in range(1, n + 1):
        t = (i - 1) * h
        k1 = np.array(rhs(y, t, tab))
        k2 = np.array(rhs(y + 0.5 * h * k1, t + 0.5 * h, tab))
        k3 = np.array(rhs(y + 0.5 * h * k2, t + 0.5 * h, tab))
        k4 = np.array(rhs(y + h * k3, t + h, tab))
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if i % every == 0:
            rows.append(y.copy())
    return np.array(rows)


COLUMNS = ["T_air", "T_can", "T_cov", "T_flr", "T_so1", "T_so2", "T_so3", "T_so4", "T_so5",
           "VP_air", "T_w1", "T_w2", "T_w3", "T_w4", "T_w5"]


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    tab = np.genfromtxt(here / "greenhouse_heating_pipe_dynamic-heating.csv", delimiter=",", names=True)
    t0 = time.perf_counter()
    rows = rk4(tab)
    dt = time.perf_counter() - t0
    print(f"RK4 h=30 s  {dt:.2f} s  ({len(rows)} hourly rows)")
    print(f"end T_air {rows[-1, 0]:.4f} C   T_w1 {rows[-1, 10]:.4f}   T_w5 {rows[-1, 14]:.4f}   "
          f"VP_air {rows[-1, 9]:.2f} Pa")
    csv_path = here / "greenhouse_heating_pipe_dynamic-integral.csv"
    if csv_path.is_file():
        cs = np.genfromtxt(csv_path, delimiter=",", names=True)
        print(f"vs {csv_path.name} (CoolSolve, h=60 s):")
        for i, name in enumerate(COLUMNS):
            d = np.max(np.abs(cs[name] - rows[:, i]))
            print(f"  {name:8} max |difference| {d:.5g}")

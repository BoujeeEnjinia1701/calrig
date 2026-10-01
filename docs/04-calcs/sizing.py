"""CalRig sizing calculations, CLR-CAL-001 v0.4 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Imports PARAMS and derived dimensions from cad/src/model.py, reads bom/bom.csv and
project.yaml, and prints every number that CLR-CAL-001 quotes. Tags in brackets, for
example [B3], match the section and line in the note. First-principles estimates only.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, fsolve

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
RESULTS = {}
K0 = 273.15


def out(tag, text):
    print(f"[{tag}] {text}")


def psat(t_c):
    """Saturation vapor pressure over water, Pa (Magnus form, Alduchov and Eskridge 1996)."""
    return 610.94 * math.exp(17.625 * t_c / (t_c + 243.04))


def rho_v(t_c, rh=100.0):
    """Water vapor density, g/m3."""
    return rh / 100 * psat(t_c) / (461.5 * (t_c + K0)) * 1000


def dew_point(t_c, rh):
    g = math.log(rh / 100) + 17.625 * t_c / (t_c + 243.04)
    return 243.04 * g / (17.625 - g)


# ---------------------------------------------------------------- assumptions
H_IN, H_OUT = 10.0, 8.0          # W/(m2 K), inside (fan-stirred) and outside (still room) films
K_ACR, K_XPS, K_FOAM = 0.19, 0.034, 0.035
RHO_ACR, RHO_XPS, RHO_PLY = 1190.0, 35.0, 550.0
CP_ACR = 1470.0
BRIDGE = 1.20                    # edges, gasket, cable gland and fixings add 20 % to the jacketed UA
LOOP_FLOW = 3.0                  # L/min conditioning flow, closed loop from and back to the chamber
HEPA_FULL, HEPA_SLOW = 20.0, 5.0  # L/min
LEAK_ACH = 0.1                   # air changes per hour through the gasket and gland
# internal gains, W: mixing fan, inner Peltier fan, six heads at up to 0.4 W, references
GAINS = {"mixing fan 120 mm": 2.4, "inner Peltier fan": 1.5, "six sensor heads": 6 * 0.4, "references": 0.4}
G = sum(GAINS.values())
# thermoelectric module, 12706 class (typical datasheet values, to confirm for the chosen part)
TEC = {"Vmax": 15.2, "Imax": 6.0, "dTmax": 66.0, "Th": 300.0}
R_SINK_OUT = 0.25                    # K/W, outer sink with 92 mm fan
R_SINK_IN = P["sink_in_r"]           # K/W, enlarged inner fin block with fan (DDR-002); was 0.45
R_SINK_IN_OLD = 0.45
V_SUPPLY = 12.0

a = TEC["Vmax"] / TEC["Th"]
R = (TEC["Th"] - TEC["dTmax"]) * TEC["Vmax"] / (TEC["Th"] * TEC["Imax"])
K = (TEC["Th"] - TEC["dTmax"]) * TEC["Vmax"] * TEC["Imax"] / (2 * TEC["Th"] * TEC["dTmax"])

print("CalRig CLR-CAL-001 sizing (all values are estimates)")
out("A0", f"TEC model: Seebeck {a * 1000:.1f} mV/K, resistance {R:.2f} ohm, conductance {K:.2f} W/K")

# ---------------------------------------------------------------- A. geometry, capacity, size, mass
ix, iy, iz = P["inner"]
out("A1", f"inside {ix:.0f} x {iy:.0f} x {iz:.0f} mm = {D['volume_l']:.1f} L; outside shell "
    f"{D['outer'][0]:.0f} x {D['outer'][1]:.0f} x {D['outer'][2]:.0f} mm")
bw, bd, bh = P["bay"]
out("A2", f"tray {D['tray_len']:.0f} x {D['tray_dep']:.0f} mm, {P['bays'][0] * P['bays'][1]} bays of "
    f"{bw:.0f} x {bd:.0f} mm; head clearance above tray {D['head_clear']:.0f} mm (bay height {bh:.0f} mm)")
RESULTS["R10"] = ("6 heads, 90 x 70 x 50 mm, sealed gland",
                  f"{P['bays'][0] * P['bays'][1]} bays {bw:.0f} x {bd:.0f} mm, {D['head_clear']:.0f} mm clear",
                  "met" if P["bays"][0] * P["bays"][1] >= 6 and D["head_clear"] >= 50 else "not met")

sys.path.insert(0, str(ROOT / ".kit"))
from model import build_parts, build_components  # noqa: E402
parts = build_parts()
vol = {k: s.volume / 1e9 for k, s in parts.items()}      # m3
COMP = build_components()
cvol = {k: c.shape.volume / 1e9 for k, c in COMP.items()}   # m3, one component each
# acrylic: shell with its welded front frame, drip tray and fan spacers (CLR-DDR-003); door alone
acr_shell = cvol["shell"] + cvol["frame"] + cvol["drip"] + cvol["spacers"]
mass = {
    "chamber shell, frame, drip tray (acrylic)": acr_shell * RHO_ACR,
    "door (acrylic)": cvol["door"] * RHO_ACR,
    "jacket and door panel (XPS)": (vol["jacket"] + vol["door_panel"]) * RHO_XPS,
    "base plate (plywood)": vol["base"] * RHO_PLY,
    "Peltier assembly": 1.1, "mixing fan": 0.15, "sensor tray and hub": 0.5, "reference cluster": 0.15,
    "bubbler with 0.3 L water": 0.8, "dryer with 0.5 kg gel": 0.85, "HEPA loop": 0.4, "aerosol port": 0.1,
    "controller": 0.25, "power supply": 0.6, "salt jars": 0.6, "wiring, gasket, four latches": 0.55,
    # added for construction (CLR-DDR-003): bulkheads, glands, drain line and empty bottle; printed parts
    "bulkheads, glands, drain line and bottle": 0.2, "printed dryer socket and jar rack": 0.1,
}
m_total = sum(mass.values())
fx, fy = D["footprint"]
out("A3", f"overall {fx:.0f} x {fy:.0f} mm footprint, {D['height']:.0f} mm high; mass {m_total:.2f} kg "
    f"(acrylic {mass['chamber shell, frame, drip tray (acrylic)'] + mass['door (acrylic)']:.1f} kg, XPS "
    f"{mass['jacket and door panel (XPS)']:.2f} kg, base {mass['base plate (plywood)']:.1f} kg)")
RESULTS["R13"] = ("600 x 500 mm, 400 mm high, 14 kg", f"{fx:.0f} x {fy:.0f} x {D['height']:.0f} mm, {m_total:.1f} kg",
                  "met" if fx <= 600 and fy <= 500 and D["height"] <= 400 and m_total <= 14 else "not met")

# ---------------------------------------------------------------- B. heat balance
u_jk = 1 / (1 / H_IN + P["wall"] / 1000 / K_ACR + P["ins"] / 1000 / K_XPS + 1 / H_OUT)
u_door = 1 / (1 / H_IN + P["door_t"] / 1000 / K_ACR + 1 / H_OUT)
u_door_p = 1 / (1 / H_IN + P["door_t"] / 1000 / K_ACR + P["ins"] / 1000 / K_XPS + 1 / H_OUT)
a_jk = D["area_jacketed"] - D["pelt_open_area"]
ua_loop = LOOP_FLOW / 60000 * 1.2 * 1005
ua_leak = LEAK_ACH / 3600 * D["volume_l"] / 1000 * 1.2 * 1005
UA = BRIDGE * u_jk * a_jk + u_door_p * D["area_door"] + ua_loop + ua_leak
UA_open = BRIDGE * u_jk * a_jk + u_door * D["area_door"] + ua_loop + ua_leak
out("B1", f"U jacketed wall {u_jk:.2f}, clear door {u_door:.2f}, door with panel {u_door_p:.2f} W/(m2 K)")
out("B2", f"UA with door panel {UA:.2f} W/K (walls {BRIDGE * u_jk * a_jk:.2f}, door {u_door_p * D['area_door']:.2f}, "
    f"loop {ua_loop:.3f}, leak {ua_leak:.3f}); door panel off {UA_open:.2f} W/K")
out("B3", "internal gains " + ", ".join(f"{k} {v:.1f} W" for k, v in GAINS.items()) + f"; total {G:.1f} W")


def cool_state(I, t_room, t_ch):
    """Cooling mode at current I with the chamber at t_ch: returns Qc into module (W), P (W), V, Th sink."""
    def eqs(x):
        tc, th = x
        qc = a * I * tc - 0.5 * I * I * R - K * (th - tc)
        qh = a * I * th + 0.5 * I * I * R - K * (th - tc)
        return [tc - ((t_ch + K0) - qc * R_SINK_IN), th - ((t_room + K0) + qh * R_SINK_OUT)]
    tc, th = fsolve(eqs, [t_ch + K0 - 5, t_room + K0 + 10])
    qc = a * I * tc - 0.5 * I * I * R - K * (th - tc)
    v = a * (th - tc) + I * R
    return qc, v * I, v, th - K0


def heat_state(I, t_room, t_ch):
    """Heating mode: returns heat into the chamber (W), P (W), V, inner junction temperature."""
    def eqs(x):
        th, tc = x                      # th inside (hot), tc outside (cold)
        qin = a * I * th + 0.5 * I * I * R - K * (th - tc)
        qout = a * I * tc - 0.5 * I * I * R - K * (th - tc)
        return [th - ((t_ch + K0) + qin * R_SINK_IN), tc - ((t_room + K0) - qout * R_SINK_OUT)]
    th, tc = fsolve(eqs, [t_ch + K0 + 10, t_room + K0 - 3])
    qin = a * I * th + 0.5 * I * I * R - K * (th - tc)
    v = a * (th - tc) + I * R
    return qin, v * I, v, th - K0


def i_at_supply(state, t_room, t_ch):
    """Largest current at which the module voltage stays within the 12 V supply."""
    f = lambda I: state(I, t_room, t_ch)[2] - V_SUPPLY
    return brentq(f, 0.1, TEC["Imax"]) if f(TEC["Imax"]) > 0 else TEC["Imax"]


def net_cooling(t_room, t_ch, ua=UA):
    I = i_at_supply(cool_state, t_room, t_ch)
    qc = cool_state(I, t_room, t_ch)[0]
    return qc - (ua * (t_room - t_ch) + G)


def lowest(t_room, ua=UA):
    """Lowest chamber temperature holdable at full 12 V drive (net cooling = 0)."""
    return brentq(lambda t: net_cooling(t_room, t, ua), t_room - 40, t_room + 5)


lows = {tr: lowest(tr) for tr in (15.0, 22.0, 25.0, 30.0)}
for tr, tl in lows.items():
    I = i_at_supply(cool_state, tr, tl)
    qc, pw, v, th = cool_state(I, tr, tl)
    out("B4", f"room {tr:.0f} C: lowest chamber {tl:.1f} C at full drive ({I:.2f} A, {v:.1f} V, {pw:.0f} W, "
        f"outer sink {th:.0f} C)")
# duty at 10 C in a 25 C room and at 20 C in a 22 C room
for tr, tch in ((25.0, 10.0), (22.0, 20.0)):
    need = UA * (tr - tch) + G
    I = brentq(lambda i: cool_state(i, tr, tch)[0] - need, 0.05, TEC["Imax"]) if lows[tr] < tch else float("nan")
    qc, pw, v, th = cool_state(I, tr, tch)
    t_fin = tch - need * R_SINK_IN
    out("B5", f"hold {tch:.0f} C in a {tr:.0f} C room: load {need:.1f} W, {I:.2f} A, {v:.1f} V, {pw:.0f} W; "
        f"inner sink about {t_fin:.1f} C")
    if tch == 20.0:
        FIN_20 = t_fin
    else:
        P_COLD, TH_COLD = pw, th
# heating
for tr, tch in ((22.0, 40.0), (15.0, 40.0)):
    need = UA * (tch - tr) - G
    I = brentq(lambda i: heat_state(i, tr, tch)[0] - need, 0.01, TEC["Imax"])
    q, pw, v, tin = heat_state(I, tr, tch)
    Imax_h = i_at_supply(heat_state, tr, tch)
    qmax = heat_state(Imax_h, tr, tch)[0]
    out("B6", f"hold {tch:.0f} C in a {tr:.0f} C room: load {need:.1f} W, {I:.2f} A, {pw:.1f} W, inner sink "
        f"{tin:.0f} C; heating capacity at 12 V {qmax:.0f} W")
    if tr == 15.0:
        T_IN_HOT = tin
tl30 = lows[30.0]
r1_ok = lows[25.0] <= 10.0 and lows[15.0] <= 10.0
RESULTS["R1"] = ("10 to 40 C in a room at 15 to 25 C; lowest point stated for rooms up to 30 C",
                 f"lowest {lows[25.0]:.1f} C in a 25 C room, {tl30:.1f} C in a 30 C room; 40 C held with margin",
                 "met" if r1_ok else "not met")

# transient: lumped heat capacity
C_TH = (cvol["shell"] + cvol["drip"] + cvol["door"]) * RHO_ACR * CP_ACR + D["volume_l"] / 1000 * 1.2 * 1005 + 0.5 * 900 + 0.9 * 1000
out("B7", f"lumped heat capacity {C_TH / 1000:.1f} kJ/K (acrylic shell and door, air, tray, heads); "
    f"passive time constant {C_TH / UA / 3600:.1f} h")


def ramp(t_room, t0, t1, band=0.3, dt=5.0):
    """Minutes to go from t0 to within band of t1 at full drive."""
    t, s = t0, 0.0
    while abs(t - t1) > band and s < 6 * 3600:
        if t1 < t:
            q = net_cooling(t_room, t)
        else:
            I = i_at_supply(heat_state, t_room, t)
            q = heat_state(I, t_room, t)[0] - UA * (t - t_room) + G
            q = -q
        t -= q / C_TH * dt
        s += dt
    return s / 60


RAMPS = {"22 to 20 C": ramp(22, 22, 20), "20 to 40 C": ramp(22, 20, 40), "40 to 20 C": ramp(22, 40, 20),
         "25 to 10 C (25 C room)": ramp(25, 25, 10.5) if lows[25.0] < 10 else float("nan")}
out("B8", "full-drive ramps (22 C room unless stated): " + ", ".join(f"{k} {v:.0f} min" for k, v in RAMPS.items()))

# ---------------------------------------------------------------- C. moisture
w_air = (0.85 - 0.20) * rho_v(40) * D["volume_l"] / 1000
# sorption into the acrylic surface: D_w about 1e-12 m2/s, uptake 2 % by mass at 100 % RH (linear)
Dw, uptake = 1e-12, 0.02
depth = 2 * math.sqrt(Dw * 45 * 60 / math.pi)
w_wall = D["area_shell_in"] * 1.2 * depth * RHO_ACR * uptake * 0.65 * 1000
out("C1", f"water for 20 to 85 % RH at 40 C: air {w_air:.2f} g, acrylic surface uptake in 45 min about {w_wall:.2f} g "
    f"(penetration {depth * 1e6:.0f} um); total {w_air + w_wall:.1f} g")
tau_loop = D["volume_l"] / LOOP_FLOW
f_sorb = (w_air + w_wall) / w_air
eff = 0.9
rho_in = eff * rho_v(43.0)
r_start, r_tgt = rho_v(40, 20), rho_v(40, 85)
t_hum = tau_loop * f_sorb * math.log((rho_in - r_start) / (rho_in - r_tgt))
out("C2", f"humidify 20 to 85 % RH at 40 C: loop time constant {tau_loop:.0f} min, bubbler 43 C at 90 % saturation "
    f"gives {rho_in:.1f} g/m3; about {t_hum:.0f} min with wall uptake")
rho_dry = rho_v(20, 5)
t_dry = tau_loop * f_sorb * math.log((rho_v(22, 50) - rho_dry) / (rho_v(20, 20) - rho_dry))
out("C3", f"dry to 20 % RH at 20 C from room air (22 C, 50 %): gel outlet about 5 % RH, about {t_dry:.0f} min")
gel_cap = 500 * 0.05
per_sweep = (rho_v(40, 85) - rho_v(20, 20)) * D["volume_l"] / 1000 + w_wall
out("C4", f"silica gel: {gel_cap:.0f} g usable at low RH (5 % by mass); about {per_sweep:.1f} g removed per sweep; "
    f"about {gel_cap / per_sweep:.0f} sweeps between regenerations")
# bubbler heater
a_jar = 2 * math.pi * (P["bubbler"][0] + P["sleeve"]) / 1000 * P["bubbler"][1] / 1000 + math.pi * (P["bubbler"][0] / 1000) ** 2
u_sleeve = 1 / (1 / H_OUT + P["sleeve"] / 1000 / K_FOAM)
loss_bare = 10.0 * (2 * math.pi * P["bubbler"][0] / 1000 * P["bubbler"][1] / 1000 + math.pi * (P["bubbler"][0] / 1000) ** 2) * 21
loss_sl = u_sleeve * a_jar * 21
evap = (w_air + w_wall) * 2400 / (t_hum * 60)
warm = 0.3 * 4186 * 21 / (10.0 - loss_sl / 2) / 60
out("C5", f"bubbler at 43 C in a 22 C room: loss bare jar {loss_bare:.1f} W, with 10 mm foam sleeve {loss_sl:.1f} W; "
    f"evaporation {evap:.1f} W; 10 W pad warms 0.3 L in {warm:.0f} min (preheat during the 20 C points)")
# wet line: condensation without trace heat
mcp = LOOP_FLOW / 2 / 60000 * 1.2 * 1005
ua_line = 2 * math.pi * K_FOAM / math.log(12 / 4) * 0.2
t_exit = 22 + (43 - 22) * math.exp(-ua_line / mcp)
out("C6", f"wet line 200 mm, foam-lagged, 1.5 L/min: air leaves at {t_exit:.0f} C, below the {dew_point(43, 90):.0f} C "
    f"dew point of the bubbler air, so the line needs trace heat (about {ua_line * 25 + mcp * 2:.1f} W to hold 45 C)")
# door and fin condensation
dp = dew_point(40, 85)
for tr in (22.0, 15.0):
    f_open = 40 - (40 - tr) * u_door / H_IN
    f_pan = 40 - (40 - tr) * u_door_p / H_IN
    f_wall = 40 - (40 - tr) * u_jk / H_IN
    out("C7", f"40 C, 85 % RH (dew point {dp:.1f} C), room {tr:.0f} C: inner door face {f_open:.1f} C clear, "
        f"{f_pan:.1f} C with panel (margin {f_pan - dp:.1f} K); jacketed wall {f_wall:.1f} C")
    if tr == 15.0:
        DOOR_MARGIN_15 = f_pan - dp
    else:
        DOOR_MARGIN_22 = f_pan - dp
dp20 = dew_point(20, 85)
out("C8", f"20 C, 85 % RH (dew point {dp20:.1f} C): inner Peltier sink about {FIN_20:.1f} C in a 22 C room, "
    f"margin {FIN_20 - dp20:+.1f} K; the sink condenses and dehumidifies in rooms warmer than about "
    f"{20 + (20 - dp20 - (G) * R_SINK_IN) / (UA * R_SINK_IN):.0f} C")
ROOM_FIN = 20 + (20 - dp20 - G * R_SINK_IN) / (UA * R_SINK_IN)
ROOM_FIN_OLD = 20 + (20 - dp20 - G * R_SINK_IN_OLD) / (UA * R_SINK_IN_OLD)
# condensation on the inner sink versus what the bubbler can supply at 20 C, 85 %
A_FIN, H_FIN = 0.10, 30.0                       # m2 fin area, W/(m2 K) with the inner fan (TRL 3 sink)
hm = H_FIN / (1.2 * 1005)                       # m/s, Lewis analogy
fin_old = 20 - (UA * 2 + G) * R_SINK_IN_OLD
cond_old = hm * A_FIN * (rho_v(20, 85) - rho_v(fin_old)) * 3600 if fin_old < dp20 else 0.0
cond = hm * A_FIN * (rho_v(20, 85) - rho_v(FIN_20)) * 3600 if FIN_20 < dp20 else 0.0
supply = LOOP_FLOW / 60000 * (eff * rho_v(23.0) - rho_v(20, 85)) * 3600
out("C9", f"inner sink {R_SINK_IN:.2f} K/W: condenses {cond:.1f} g/h at 20 C, 85 % in a 22 C room (bubbler supplies "
    f"{supply:.1f} g/h) and stays dry in rooms up to {ROOM_FIN:.0f} C; the former {R_SINK_IN_OLD:.2f} K/W sink ran at "
    f"{fin_old:.1f} C, condensed {cond_old:.1f} g/h and stayed dry only below {ROOM_FIN_OLD:.0f} C")
r2_ok = ROOM_FIN >= 25.0 and cond <= supply
RESULTS["R2"] = ("20 to 85 % RH at 20 to 40 C", f"reached in {max(t_hum, t_dry):.0f} min; 20 C, 85 % RH held in rooms up to "
                 f"{ROOM_FIN:.0f} C (inner sink dry)",
                 "met" if r2_ok else ("at risk" if cond <= supply else "not met"))

# ---------------------------------------------------------------- D. stability (R3), PI simulation
def simulate(t_set=40.0, t_room=22.0, hours=1.0, dt=1.0, lag=4.0, dead=20.0, swing=1.0):
    n = int(hours * 3600 / dt)
    t = t_set
    meas = t_set
    kp, ki = 40.0, 40.0 / 600
    integ = (UA * (t_set - t_room) - G) / ki          # bumpless start at the steady-state drive
    buf = [t_set] * int(dead / dt)
    hist = []
    for k in range(n):
        tr = t_room + swing * math.sin(2 * math.pi * k * dt / 1800)
        buf.append(t)
        seen = buf.pop(0)
        meas += (seen - meas) * dt / lag
        m = round(meas / 0.01) * 0.01
        e = t_set - m
        integ += e * dt
        q = kp * e + ki * integ                     # W into the chamber
        qmax = 60.0
        q = max(-qmax, min(qmax, q))
        q = round(q / qmax * 255) / 255 * qmax      # 8-bit PWM
        t += (q + UA * (tr - t) + G) / C_TH * dt
        if k * dt > 900:
            hist.append(t)
    return max(abs(np.array(hist) - t_set))


dev = max(simulate(40.0), simulate(20.0))
rh_from_t = 85 * (math.log(psat(40.3) / psat(40.0)))
out("D1", f"PI control, 20 s transport delay, 4 s sensor lag, 8-bit drive, room swinging 1 K over 30 min: "
    f"peak deviation {dev:.2f} K")
rh_budget = math.hypot(85 * (psat(40 + dev) / psat(40) - 1), 0.5 * 2)
out("D2", f"RH stability at 40 C, 85 %: temperature term {85 * (psat(40 + dev) / psat(40) - 1):.2f} % RH, mixing "
    f"control +/-1 % RH (assumed); combined {rh_budget:.1f} % RH")
RESULTS["R3"] = ("+/-0.3 C, +/-2 % RH over 30 min", f"+/-{dev:.2f} C, +/-{rh_budget:.1f} % RH (idealized model)",
                 "met" if dev <= 0.3 and rh_budget <= 2 else "at risk")

# ---------------------------------------------------------------- E. uniformity (R4)
FREE = {"80 mm": 50.0, "120 mm": 85.0}     # m3/h free air, typical 12 V fans
EFF, F_TRAY = 0.4, 0.5
cases = {"40 C, 22 C room": UA * 18 - G, "20 C, 22 C room": UA * 2 + G, "10 C, 25 C room": UA * 15 + G}
spans = {}
for fan, q in FREE.items():
    mcp_mix = q * EFF / 3600 * 1.2 * 1005
    spans[fan] = {c: F_TRAY * load / mcp_mix for c, load in cases.items()}
    out("E1", f"{fan} mixing fan ({q * EFF:.0f} m3/h effective): bay-to-bay span " +
        ", ".join(f"{c} {s:.2f} K" for c, s in spans[fan].items()))
sp = spans["120 mm"]
rh_u = 85 * (psat(40 + sp["40 C, 22 C room"] / 2) / psat(40) - 1)
out("E2", f"RH spread from temperature at 40 C, 85 %: +/-{rh_u:.1f} % RH")
epa_ok = max(sp["40 C, 22 C room"], sp["20 C, 22 C room"]) / 2 <= 0.3
RESULTS["R4"] = ("+/-0.3 C, +/-2 % RH between bays",
                 f"+/-{sp['40 C, 22 C room'] / 2:.2f} C at 40 C, +/-{sp['10 C, 25 C room'] / 2:.2f} C at 10 C; +/-{rh_u:.1f} % RH",
                 "at risk")

# ---------------------------------------------------------------- F. reference uncertainty (R5, R6)
u_t = {"ice point realization": 0.02, "SHT45 tolerance after offset, 0 to 40 C (0.1 C, rectangular)": 0.1 / math.sqrt(3),
       "drift between checks (0.03 C, rectangular)": 0.03 / math.sqrt(3), "resolution and noise": 0.01,
       "reference to bay gradient at the mast (0.05 C, rectangular)": 0.05 / math.sqrt(3)}
U_t = 2 * math.sqrt(sum(v * v for v in u_t.values()))
u_t_max = dict(u_t)
u_t_max["SHT45 tolerance after offset, 0 to 40 C (0.1 C, rectangular)"] = 0.2 / math.sqrt(3)
U_t_max = 2 * math.sqrt(sum(v * v for v in u_t_max.values()))
out("F1", f"reference temperature U (k = 2): {U_t:.2f} C with a 0.1 C tolerance after the ice point; "
    f"{U_t_max:.2f} C if the tolerance is 0.2 C")
RESULTS["R5"] = ("0.2 C or better, k = 2", f"{U_t:.2f} C (0.1 C tolerance), {U_t_max:.2f} C (0.2 C)",
                 "at risk" if U_t <= 0.2 < U_t_max else ("met" if U_t_max <= 0.2 else "not met"))
u_h = {"salt fixed point (Greenspan, largest 0.27 % RH, k = 2)": 0.27 / 2,
       "jar gradient 0.2 K at 85 % RH (rectangular)": 85 * (psat(25.2) / psat(25) - 1) / math.sqrt(3),
       "hysteresis (0.8 % RH, rectangular)": 0.8 / math.sqrt(3),
       "interpolation between fixed points (0.5 % RH, rectangular)": 0.5 / math.sqrt(3),
       "temperature away from 25 C (1.0 % RH, rectangular)": 1.0 / math.sqrt(3)}
U_h = 2 * math.sqrt(sum(v * v for v in u_h.values()))
out("F2", "reference humidity components: " + "; ".join(f"{k} {v:.2f}" for k, v in u_h.items()))
out("F3", f"reference humidity U (k = 2): {U_h:.1f} % RH")
RESULTS["R6"] = ("2 % RH or better, k = 2, four salt points", f"{U_h:.1f} % RH",
                 "met" if U_h <= 1.8 else ("at risk" if U_h <= 2.2 else "not met"))

# ---------------------------------------------------------------- G. particles (R7, R8)
V = D["volume_l"] / 1000
k_dep = 0.2 / 60                      # 1/min, smoke deposition in a stirred chamber (0.2 per hour)
k_leak = LEAK_ACH / 60
k_full = HEPA_FULL / 1000 / V * 0.9995 + k_dep + k_leak
k_slow = HEPA_SLOW / 1000 / V * 0.9995 + k_dep + k_leak
t_clean = math.log(35 / 2) / k_full
floor = 15 * k_leak / k_slow
t_decay = math.log(300 / 5) / k_slow
t_decay_nodep = math.log(300 / 5) / (HEPA_SLOW / 1000 / V)
m_smoke = 300 * V
out("G1", f"clean-down 35 to 2 ug/m3 at {HEPA_FULL:.0f} L/min: {t_clean:.1f} min; leak floor with a 15 ug/m3 room "
    f"{floor:.2f} ug/m3")
out("G2", f"decay 300 to 5 ug/m3 at {HEPA_SLOW:.0f} L/min: {t_decay:.0f} min with deposition 0.2 per hour "
    f"({t_decay_nodep:.0f} min without); smoke mass {m_smoke:.1f} ug, a 60 mL syringe needs plume above "
    f"{m_smoke / 0.06 / 1000:.2f} mg/m3")
RESULTS["R7"] = ("zero below 2 ug/m3; 300 to 5 ug/m3 in 45 min or less",
                 f"clean-down {t_clean:.0f} min, floor {floor:.2f}; decay {t_decay:.0f} min",
                 "met" if t_decay <= 45 and floor < 2 else "not met")
RESULTS["R8"] = ("transfer PM sensor collocated 30 days, meeting EPA targets", "no collocation site named (open item)",
                 "not met")

# ---------------------------------------------------------------- H. CO2 (R9)
k_scrub = LOOP_FLOW / 1000 / V
co2_floor = 420 * k_leak / (k_scrub + k_leak)
t_zero = math.log(420 / 50) / (k_scrub + k_leak)
span = 40000 * 1.0 / (D["volume_l"] + 1.0)
out("H1", f"soda lime zero: {t_zero:.0f} min to 50 ppm, floor {co2_floor:.0f} ppm; 1 L of breath at 4 % adds "
    f"{span:.0f} ppm; SCD30 reference +/-{30 + 0.03 * 1000:.0f} ppm at 1,000 ppm")
RESULTS["R9"] = ("zero below 50 ppm; span 400 to 2000 ppm", f"floor {co2_floor:.0f} ppm; span to about {420 + span:.0f} ppm",
                 "met" if co2_floor < 50 else "not met")

# ---------------------------------------------------------------- I. throughput (R11)
settle_h = max(t_hum, t_dry)
EQ = 15.0                             # min for heads and references to equilibrate after the chamber is in band
HOLD = 30.0
points = [("20 C, 40 %", RAMPS["22 to 20 C"], t_dry), ("20 C, 85 %", 0, t_hum), ("40 C, 85 %", RAMPS["20 to 40 C"], t_hum * 0.3),
          ("40 C, 40 %", 0, t_dry)]
t_sweep = sum(max(r, h) + EQ + HOLD for _, r, h in points)
t_part = t_clean + 5 + t_decay + 10
t_total = (t_sweep + t_part) / 60
out("I1", "sweep: " + "; ".join(f"{n} settle {max(r, h):.0f} + {EQ:.0f} + hold {HOLD:.0f} min" for n, r, h in points))
out("I2", f"sweep {t_sweep / 60:.1f} h + particle run {t_part:.0f} min = {t_total:.1f} h")
RESULTS["R11"] = ("sweep plus particle run in 8 h or less", f"{t_total:.1f} h", "met" if t_total <= 8 else "not met")

# ---------------------------------------------------------------- J. power and thermal safety (R15, R16)
I_hot = i_at_supply(heat_state, 15.0, 40.0)
p_pelt_max = max(cool_state(i_at_supply(cool_state, 30, tl30), 30, tl30)[1], heat_state(I_hot, 15, 40)[1])
loads = {"Peltier at 12 V": p_pelt_max, "bubbler heater": 10.0, "wet-line trace": 3.0, "pumps 2 x 2 W": 4.0,
         "fans (mixing, 2 on the Peltier)": 2.4 + 1.5 + 2.0, "HEPA blower": 3.0, "controller": 1.5, "sensors": 2.8}
p_peak = sum(loads.values())
out("J1", "peak loads " + ", ".join(f"{k} {v:.0f} W" for k, v in loads.items()) + f": {p_peak:.0f} W, "
    f"{p_peak / 12:.1f} A at 12 V (supply 10 A, fuse 10 A)")
RESULTS["R15"] = ("no mains, fused 12 V, 100 W peak", f"{p_peak:.0f} W peak, {p_peak / 12:.1f} A", "met" if p_peak <= 100 else "not met")
th_worst = cool_state(i_at_supply(cool_state, 30, tl30), 30, tl30)[3]
out("J2", f"outer sink at full cooling in a 30 C room: {th_worst:.0f} C (cut-off 70 C); inner sink heating to 40 C "
    f"in a 15 C room: {T_IN_HOT:.0f} C; air cut-off 50 C is {50 - 40:.0f} K above the top set point")
RESULTS["R16"] = ("hardware cut-off 50 C air, 70 C hot side", f"outer sink {th_worst:.0f} C max in normal use",
                  "met" if th_worst < 70 else "at risk")

# ---------------------------------------------------------------- K. cost (R12)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows)
budget = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd"):
        budget = float(line.split(":")[1].split("#")[0])
core = total - sum(float(r["unit_cost_usd"]) for r in rows if r["item"].startswith(("16 ",)))
core -= 59.0                         # SCD30 share of line 8
out("K1", f"BOM {len(rows)} lines, total ${total:.0f}; budget_usd ${budget:.0f} "
    f"({'over' if total > budget else 'within'} by ${abs(total - budget):.0f}; set to $412 by Amish on 2026-09-26, DDR-002; "
    f"was $400, and $300 before that); core without CO2 ${core:.0f}")
RESULTS["R12"] = (f"${budget:.0f} in parts", f"${total:.0f} (${total - budget:+.0f} vs ${budget:.0f})",
                  "not met" if total > budget else "met")

RESULTS["R14"] = ("CSV and per-sensor report", "software not written (beyond TRL 3)", "not verifiable at TRL 3")
RESULTS["R17"] = ("no toxic gases; smoke cleared through HEPA", "by design; clean-down time above", "met")
RESULTS["R18"] = ("saw or laser cutter, drill, soldering iron", "by design; model has no machined parts", "met")

# ---------------------------------------------------------------- L. results
print("\n[L] Results against every requirement")
order = [f"R{i}" for i in range(1, 19)]
for r in order:
    tgt, val, st = RESULTS[r]
    print(f"  {r:<4} {st:<24} {val}   (target: {tgt})")
counts = {}
for r in order:
    counts[RESULTS[r][2]] = counts.get(RESULTS[r][2], 0) + 1
print("[L1] counts: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))

"""CalRig product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a filleted insulation jacket in five panels with
seams, the clear acrylic chamber and front door with a printed border, draw latches and a lead
gland; inside, the perforated six-bay sensor tray with example sensor heads, the reference
cluster on its mast, the guarded 120 mm mixing fan and the finned inner Peltier sink; outside,
the outer Peltier sink and guarded fan, the foam-sleeved bubbler, the dryer column, the aerosol
port and ball valve, the HEPA loop, controller and power supply behind the chamber, the four
salt fixed-point jars and the removable door panel. Context is a compact lab bench top.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS, derived() and build_parts() in
model.py (same axes: X across the bench, conditioning column at +X; Y front, -Y is the door,
to back; Z up; base plate on the bench at z = 0). Differences from model.py are listed in
docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived, build_parts

TITLE = "CalRig: benchtop calibration chamber for low-cost air sensors"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -60,
     "note": "Product render from the front right and above (about 30 deg elevation); the sensor tray and "
             "reference cluster show through the clear door, with the Peltier fan, bubbler and dryer at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): jacket panels, acrylic "
             "chamber and door, sensor tray and heads, reference cluster, mixing fan, Peltier heat pump, "
             "bubbler, dryer, HEPA loop, controller, power supply, salt jars and door panel"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 16, "az": -76,
     "note": "Detail from the front, slightly right and above (about 16 deg elevation): six sensor heads on "
             "the tray and the reference cluster behind the clear door, without the bench"},
]

# Colours (restrained product palette; kit accent)
C_JACKET = "#ECEDEE"
C_JACKET_IN = "#DADDE1"
C_BASE = "#2B2F36"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_CLEAR = "#DCEBF5"
C_METAL = "#B8BEC6"
C_ALU = "#C7CCD2"
C_FAN = "#24282E"
C_ROTOR = "#3A3F47"
C_HEAD_W = "#F1F1EF"
C_HEAD_G = "#8A9099"
C_HEAD_D = "#3A3F47"
C_LABEL = "#F4F4F2"
C_LED_G = "#22C55E"
C_LED_T = "#5EEAD4"
C_FOAM = "#33373D"
C_TUBE = "#EDEDEA"
C_GEL = "#E8B04A"
C_BRASS = "#C9A227"
C_BENCH = "#D8D5CF"
C_SALT = "#F7F7F5"
LID_COLS = ["#9A3B3B", "#3B5B9A", "#C9C3B6", "#4D7A57"]


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _front(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_y(x, y, z, af, h):
    """Hex prism along Y centred at (x, y, z)."""
    return Pos(x, y + h / 2, z) * extrude(Plane.XZ * RegularPolygon(af / 1.732, 6), amount=h)


def _rrect(cx, cy, z0, z1, sx, sy, r):
    """Rounded-rectangle prism (vertical edges filleted)."""
    b = _bx(cx - sx / 2, cx + sx / 2, cy - sy / 2, cy + sy / 2, z0, z1)
    return _fillet_try(b, _par(b, Axis.Z), [r, r * 0.7])


def _fan(size, thick, blades=7):
    """Axial fan on the Z axis, front (guard) face at +Z. Returns frame, rotor, guard."""
    frame = Box(size, size, thick)
    frame = _fillet_try(frame, _par(frame, Axis.Z), [size * 0.08, size * 0.05])
    ro = size * 0.46
    frame -= Cylinder(ro, thick + 2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame -= Pos(sx * size * 0.41, sy * size * 0.41, 0) * Cylinder(size * 0.025, thick + 2)
    struts = (Rot(0, 0, 45) * Box(size * 1.3, 3.0, 3.0)) + (Rot(0, 0, -45) * Box(size * 1.3, 3.0, 3.0))
    struts = Pos(0, 0, -thick / 2 + 1.5) * struts
    frame += struts & Box(size - 1, size - 1, thick)
    hub = Pos(0, 0, 0) * Cylinder(size * 0.17, thick * 0.7)
    hub = _fillet_try(hub, _top(hub), [size * 0.03, 1.0])
    rotor = hub
    for k in range(blades):
        b = Pos(size * 0.29, 0, 0) * Rot(28, 0, 0) * Box(size * 0.26, size * 0.14, 1.6)
        rotor += Rot(0, 0, k * 360.0 / blades) * b
    rotor &= Cylinder(ro - 1.5, thick)
    zg = thick / 2 - 0.6
    guard = None
    for f in (0.12, 0.22, 0.32, 0.42):
        ring = Pos(0, 0, zg) * (Cylinder(size * f + 0.7, 1.2) - Cylinder(size * f - 0.7, 2.0))
        guard = ring if guard is None else guard + ring
    bars = Pos(0, 0, zg) * (Box(size * 0.92, 1.6, 1.2) + Box(1.6, size * 0.92, 1.2))
    guard += bars & Pos(0, 0, zg) * Cylinder(ro + 0.5, 1.2)
    return frame, rotor, guard


def product_parts(P=PARAMS):
    D = derived(P)
    M = build_parts(P, door_panel=True)
    t, ins = P["wall"], P["ins"]
    cx0, cx1, cy0, cy1, cz0, cz1 = D["cx0"], D["cx1"], D["cy0"], D["cy1"], D["cz0"], D["cz1"]
    floor = D["floor"]
    bx, by, bt = P["base"]
    pz = floor + P["pelt_z"]
    oy, oz = P["pelt_open"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ 4 base plate (plinth)
    EB = (0, 0, -200)
    base = _bx(-bx / 2, bx / 2, -by / 2, by / 2, 0, bt)
    base = _fillet_try(base, _par(base, Axis.Z), [22.0, 16.0, 10.0])
    base = _fillet_try(base, _top(base), [3.0, 2.0, 1.0])
    add("Base plate (HDPE)", base, C_BASE, "plastic", 4, "shell", EB)
    bscr = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = _zcyl(sx * (bx / 2 - 22), sy * (by / 2 - 22), bt + 0.6, 4.0, 1.2)
            s = _fillet_try(s, _top(s), [0.6, 0.3])
            s -= _box(sx * (bx / 2 - 22), sy * (by / 2 - 22), bt + 1.2, 5.0, 1.0, 1.0)
            bscr = s if bscr is None else bscr + s
    add("Base plate screws", bscr, C_METAL, "metal", 17, "shell", EB)

    # ------------------------------------------------------------ 3 insulation jacket (five panels)
    ox0, ox1 = cx0 - ins, cx1 + ins
    oy0, oy1 = cy0, cy1 + ins
    oz0, oz1 = bt, cz1 + ins
    jo = _bx(ox0, ox1, oy0, oy1, oz0, oz1)
    jo = _fillet_try(jo, _par(jo, Axis.Z), [12.0, 8.0, 5.0])
    jo = _fillet_try(jo, [e for e in _top(jo)], [10.0, 6.0, 4.0])
    jo = _fillet_try(jo, _front(jo), [2.5, 1.5, 1.0])
    jk = jo - _bx(cx0, cx1, cy0 - 1, cy1, cz0, cz1)
    jk -= _bx(cx1 - 1, cx1 + ins + 1, -oy / 2, oy / 2, pz - oz / 2, pz + oz / 2)
    jk -= _xcyl(cx0 - ins / 2, 0, floor + P["aero_z"], P["aero_d"] / 2 + 6, ins + 2)
    for y in P["port_ys"]:
        jk -= _xcyl(cx1 + ins / 2, y, floor + P["port_z"], P["port_d"] / 2 + 4, ins + 2)
    # seams where the panels meet (parting lines)
    W, Dp = ox1 - ox0, oy1 - oy0
    ccx, ccy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
    for zs in (cz0, cz1):
        ring = _rrect(ccx, ccy, zs - 0.6, zs + 0.6, W + 2, Dp + 2, 13.0) \
            - _rrect(ccx, ccy, zs - 1, zs + 1, W - 2.0, Dp - 2.0, 11.0)
        jk -= ring
    for xs in (cx0, cx1):
        jk -= _bx(xs - 0.6, xs + 0.6, oy1 - 1.0, oy1 + 1, cz0, cz1)
    regions = [
        ("Insulation jacket, bottom panel", _bx(-900, 900, -900, 900, -50, cz0), (0, 0, -110)),
        ("Insulation jacket, top panel", _bx(-900, 900, -900, 900, cz1, 900), (0, 0, 300)),
        ("Insulation jacket, left panel", _bx(-900, cx0, -900, 900, cz0, cz1), (-230, 0, 0)),
        ("Insulation jacket, right panel", _bx(cx1, 900, -900, 900, cz0, cz1), (190, 0, 0)),
        ("Insulation jacket, back panel", _bx(cx0, cx1, -900, 900, cz0, cz1), (0, 250, 0)),
    ]
    for nm, reg, ex in regions:
        add(nm, jk & reg, C_JACKET, "plastic", 3, "shell", ex)

    # name plate and front status light on the top band of the jacket
    fy = oy0
    plate = _box(ccx - 60, fy - 0.2, (cz1 + oz1) / 2, 92, 0.4, 11)
    add("CalRig name plate", plate, C_ACCENT, "painted", 17, "shell", (0, 0, 300))
    ink = _box(ccx - 88, fy - 0.5, (cz1 + oz1) / 2, 26, 0.3, 4) + _box(ccx - 50, fy - 0.5, (cz1 + oz1) / 2 + 1.5, 40, 0.3, 2.0) \
        + _box(ccx - 50, fy - 0.5, (cz1 + oz1) / 2 - 2.0, 30, 0.3, 1.2)
    add("Name plate print", ink, C_LABEL, "paper", 17, "shell", (0, 0, 300))
    lx, lz = ox1 - 40, (cz1 + oz1) / 2
    ring = _ycyl(lx, fy - 0.8, lz, 5.0, 1.6) - _ycyl(lx, fy - 0.8, lz, 3.4, 3)
    add("Status light bezel", ring, C_DARK, "plastic", 13, "shell", (0, 0, 300))
    dome = (_ycyl(lx, fy - 0.8, lz, 3.3, 1.6) + Pos(lx, fy - 1.2, lz) * Sphere(2.8)) & _box(lx, fy - 1.5, lz, 8, 3.0, 8)
    add("Status light, green (lit)", dome, C_LED_G, "emissive", 13, "shell", (0, 0, 300))

    # ------------------------------------------------------------ 1 chamber shell (clear acrylic)
    add("Chamber shell, 6 mm clear acrylic", M["shell"], C_CLEAR, "clear", 1, "shell", (0, 0, 0))

    # ------------------------------------------------------------ 2 front door
    ED = (0, -520, 0)
    dy0, dy1 = D["door_y0"], cy0
    door = _bx(cx0, cx1, dy0, dy1, cz0, cz1)
    door = _fillet_try(door, _par(door, Axis.Y), [4.0, 2.0])
    add("Front door, clear acrylic", door, "#E6F0F5", "clear", 2, "shell", ED)
    bw_ = 22.0
    border = _bx(cx0 + 0.5, cx1 - 0.5, dy0 - 0.3, dy0, cz0 + 0.5, cz1 - 0.5)
    border = _fillet_try(border, _par(border, Axis.Y), [3.5, 2.0])
    win = _bx(cx0 + bw_, cx1 - bw_, dy0 - 1, dy0 + 1, cz0 + bw_, cz1 - bw_)
    win = _fillet_try(win, _par(win, Axis.Y), [8.0, 5.0])
    add("Door border print", border - win, C_DARK, "painted", 2, "shell", ED)
    gask = _bx(cx0 + 2, cx1 - 2, dy1 - 0.2, dy1 + 0.0, cz0 + 2, cz1 - 2) \
        - _bx(cx0 + 8, cx1 - 8, dy1 - 1, dy1 + 1, cz0 + 8, cz1 - 8)
    add("Door gasket (silicone)", gask, C_BLACK, "rubber", 2, "shell", ED)

    lw, ld, lh = P["latch"]
    zc = (cz0 + cz1) / 2
    for k, xl in enumerate((cx0 + 30 + lw / 2, cx1 - 30 - lw / 2)):
        body = _box(xl, dy0 - 5, zc, lw, 10, lh)
        body = _fillet_try(body, body.edges(), [2.0, 1.2, 0.6])
        add(f"Draw latch {k + 1}", body, C_METAL, "metal", 2, "shell", ED)
        lev = _box(xl, dy0 - 11, zc + 2, lw - 8, 2.4, lh - 10)
        lev = _fillet_try(lev, _par(lev, Axis.Y), [4.0, 2.0])
        lev = _fillet_try(lev, _front(lev), [0.8, 0.4])
        add(f"Draw latch lever {k + 1}", lev, C_DARK, "plastic", 2, "shell", ED)
        riv = _fuse(_ycyl(xl + sx * (lw / 2 - 4), dy0 - 10.4, zc + sz * (lh / 2 - 4), 1.6, 0.8)
                    for sx in (-1, 1) for sz in (-1, 1))
        add(f"Draw latch rivets {k + 1}", riv, C_METAL, "metal", 2, "shell", ED)

    gx, gz = cx1 - 60, cz0 + 45
    gl = _hex_y(gx, dy0 - 2.5, gz, 20.0, 5.0) + _ycyl(gx, dy0 - 8.0, gz, 8.0, 6.0)
    gl += (Pos(gx, dy0 - 11.0, gz) * Sphere(7.0)) & _box(gx, dy0 - 14, gz, 20, 6, 20)
    add("Sensor lead gland", gl, C_DARK, "plastic", 2, "shell", ED)

    # ------------------------------------------------------------ 5 Peltier heat pump
    EP = (380, 0, 0)
    sxi, syi, szi = P["sink_in"]
    fins = _bx(cx1 - t - 5, cx1 - t, -syi / 2, syi / 2, pz - szi / 2, pz + szi / 2)
    n = 17
    pitch = (syi - 1.6) / (n - 1)
    for k in range(n):
        y = -syi / 2 + 0.8 + k * pitch
        fins += _bx(cx1 - t - sxi, cx1 - t - 5, y - 0.8, y + 0.8, pz - szi / 2, pz + szi / 2)
    add("Inner Peltier fin block (aluminium)", fins, C_ALU, "metal", 5, "internal", (300, 0, 0))
    mod = _bx(cx1 - t, cx1 + ins, -40, 40, pz - 40, pz + 40)
    add("Peltier module and cold block", mod, C_ALU, "metal", 5, "internal", (340, 0, 0))
    sxo, syo, szo = P["sink_out"]
    x0 = cx1 + ins
    osk = _bx(x0, x0 + 5, -syo / 2, syo / 2, pz - szo / 2, pz + szo / 2)
    n = 15
    pitch = (syo - 1.6) / (n - 1)
    for k in range(n):
        y = -syo / 2 + 0.8 + k * pitch
        osk += _bx(x0 + 5, x0 + sxo, y - 0.8, y + 0.8, pz - szo / 2, pz + szo / 2)
    add("Outer Peltier heat sink (aluminium)", osk, C_ALU, "metal", 5, "shell", EP)
    fx, fyy, fz = P["fan_out"]
    fr, ro, gd = _fan(fyy, fx)
    place = Pos(x0 + sxo + fx / 2, 0, pz) * Rot(0, 90, 0)
    add("Outer fan frame, 92 mm", place * fr, C_FAN, "plastic", 5, "shell", (EP[0] + 60, 0, 0))
    add("Outer fan rotor", place * ro, C_ROTOR, "plastic", 5, "shell", (EP[0] + 60, 0, 0))
    add("Outer fan finger guard", place * gd, C_METAL, "metal", 5, "shell", (EP[0] + 60, 0, 0))

    # ------------------------------------------------------------ 6 internal mixing fan
    f, ft = P["mix_fan"], P["mix_fan_t"]
    mx = cx0 + t + 20 + f / 2
    my = cy1 - t - 5 - ft / 2
    mz = cz1 - t - 10 - f / 2
    fr, ro, gd = _fan(f, ft)
    place = Pos(mx, my, mz) * Rot(90, 0, 0)
    EM = (0, -60, 230)
    add("Mixing fan frame, 120 mm", place * fr, C_FAN, "plastic", 6, "internal", EM)
    add("Mixing fan rotor", place * ro, C_ROTOR, "plastic", 6, "internal", EM)
    add("Mixing fan guard", place * gd, C_METAL, "metal", 6, "internal", EM)

    # ------------------------------------------------------------ 7 sensor tray and example heads
    ET = (0, -250, 0)
    tz0 = floor + P["tray_z"]
    tx0 = cx0 + t + 10
    ty0 = cy0 + t + 10
    TL, TD = D["tray_len"], D["tray_dep"]
    tray = _bx(tx0, tx0 + TL, ty0, ty0 + TD, tz0, tz0 + P["tray_t"])
    tray = _fillet_try(tray, _par(tray, Axis.Z), [6.0, 4.0])
    holes = []
    for i in range(13):
        for j in range(7):
            holes.append(_zcyl(tx0 + 15 + i * (TL - 30) / 12, ty0 + 14 + j * (TD - 28) / 6, tz0 + 3, 4.0, 10))
    tray -= _fuse(holes)
    for x in (tx0 + 10, tx0 + TL - 15):
        for y in (ty0 + 10, ty0 + TD - 15):
            tray += _zcyl(x + 2.5, y + 2.5, (floor + tz0) / 2, 3.0, tz0 - floor)
    add("Sensor tray, perforated aluminium", tray, C_ALU, "metal", 7, "internal", ET)
    rail = _bx(tx0, tx0 + TL, ty0 + TD, ty0 + TD + 12, tz0, tz0 + 25)
    rail = _fillet_try(rail, _top(rail), [2.0, 1.0])
    add("Cable rail and USB, I2C hub", rail, C_DARK, "plastic", 7, "internal", ET)
    ports = None
    for i in range(6):
        px = tx0 + 30 + i * (TL - 60) / 5
        c = _box(px, ty0 + TD - 1.0, tz0 + 16, 12, 2.0, 6)
        ports = c if ports is None else ports + c
    add("Hub connectors", ports, C_METAL, "metal", 7, "internal", ET)

    bw, bd, bh = P["bay"]
    g = P["bay_gap"]
    ztop = D["tray_top"]
    k = 0
    for j in range(P["bays"][1]):
        for i in range(P["bays"][0]):
            x = tx0 + g + i * (bw + g)
            y = ty0 + g + j * (bd + g)
            hx, hy = x + bw / 2, y + bd / 2
            sx_, sy_, sz_ = bw - 10, bd - 10, bh - 5
            style = (i + j) % 3
            col = [C_HEAD_W, C_HEAD_D, C_HEAD_G][style]
            head = _bx(hx - sx_ / 2, hx + sx_ / 2, hy - sy_ / 2, hy + sy_ / 2, ztop, ztop + sz_)
            head = _fillet_try(head, _par(head, Axis.Z), [10.0 if style == 0 else 5.0, 3.0])
            head = _fillet_try(head, _top(head), [4.0, 2.0, 1.0])
            fyh = hy - sy_ / 2
            if style == 0:       # louvred housing
                for q in range(4):
                    head -= _box(hx, fyh, ztop + 10 + q * 7, sx_ - 30, 4.0, 2.6)
            elif style == 1:     # top grille
                for a in (-1, 0, 1):
                    for b in (-1, 0, 1):
                        head -= _zcyl(hx + a * 11, hy + b * 11, ztop + sz_, 3.0, 4.0)
            else:                # side slots
                for q in range(5):
                    head -= _box(hx - sx_ / 2 + 14 + q * 11, fyh, ztop + sz_ / 2, 3.0, 4.0, sz_ - 20)
            add(f"Sensor head under test {k + 1} (example)", head, col, "plastic", None, "internal", ET)
            lab = _box(hx + sx_ / 2 - 16, fyh - 0.2, ztop + sz_ - 10, 18, 0.4, 7)
            add(f"Sensor head {k + 1} serial label", lab, C_LABEL, "paper", None, "internal", ET)
            led = _ycyl(hx - sx_ / 2 + 10, fyh - 0.4, ztop + sz_ - 10, 2.0, 1.2)
            add(f"Sensor head {k + 1} status light (lit)", led, C_LED_G if k % 2 == 0 else C_LED_T,
                "emissive", None, "internal", ET)
            k += 1

    # ------------------------------------------------------------ 8 reference cluster on its mast
    ER = (0, -150, 170)
    rx, ry, rz = P["ref"]
    rcx = tx0 + TL / 2
    rcy = ty0 + TD + 30
    mast = _bx(rcx - 5, rcx + 5, rcy - 5, rcy + 5, ztop, ztop + P["ref_z"])
    mast = _fillet_try(mast, _par(mast, Axis.Z), [2.0, 1.0])
    mast += _rrect(rcx, rcy, ztop, ztop + 4, 30, 24, 4.0)
    add("Reference mast (printed)", mast, C_DARK, "plastic", 8, "internal", ER)
    rz0 = ztop + P["ref_z"]
    rh = _bx(rcx - rx / 2, rcx + rx / 2, rcy - ry / 2, rcy + ry / 2, rz0, rz0 + rz)
    rh = _fillet_try(rh, _par(rh, Axis.Y), [8.0, 5.0])
    rh = _fillet_try(rh, _par(rh, Axis.Z), [3.0, 2.0])
    for q in range(5):
        rh -= _box(rcx - 22 + q * 6, rcy + ry / 2, rz0 + rz / 2, 2.6, 4.0, rz - 22)
    add("Reference cluster housing", rh, C_HEAD_W, "plastic", 8, "internal", ER)
    face = _bx(rcx - rx / 2 + 6, rcx + rx / 2 - 6, rcy - ry / 2 - 0.4, rcy - ry / 2, rz0 + 6, rz0 + rz - 6)
    face = _fillet_try(face, _par(face, Axis.Y), [4.0, 2.0])
    for q in range(6):
        face -= _box(rcx - 25 + q * 7, rcy - ry / 2, rz0 + rz / 2 + 4, 3.0, 2.0, 24)
    add("Reference cluster front plate", face, C_ACCENT, "painted", 8, "internal", ER)
    rlab = _box(rcx + 18, rcy - ry / 2 - 0.5, rz0 + 12, 22, 0.3, 6)
    add("Reference cluster label", rlab, C_LABEL, "paper", 8, "internal", ER)
    rled = _ycyl(rcx + 30, rcy - ry / 2 - 0.6, rz0 + rz - 12, 2.0, 1.2)
    add("Reference cluster status light (lit)", rled, C_LED_T, "emissive", 8, "internal", ER)

    # ------------------------------------------------------------ 9 humidifier bubbler
    EBu = (110, -210, 0)
    br, bh2 = P["bubbler"]
    bxp, byp = P["bubbler_xy"]
    sl = P["sleeve"]
    sleeve = _zcyl(bxp, byp, bt + (bh2 - 16) / 2, br + sl, bh2 - 16)
    sleeve = _fillet_try(sleeve, _top(sleeve), [3.0, 2.0])
    sleeve = _fillet_try(sleeve, _bottom(sleeve), [2.0, 1.0])
    for q in range(3):
        sleeve -= _zcyl(bxp, byp, bt + 30 + q * 40, br + sl + 2, 1.2) - _zcyl(bxp, byp, bt + 30 + q * 40, br + sl - 0.8, 2)
    add("Bubbler foam sleeve", sleeve, C_FOAM, "fabric", 9, "shell", EBu)
    jar = _zcyl(bxp, byp, bt + bh2 - 16 + 6, br, 12)
    add("Bubbler glass jar (clear)", jar, C_CLEAR, "clear", 9, "shell", EBu)
    lid = _zcyl(bxp, byp, bt + bh2 - 3, br + 2, 6)
    lid = _fillet_try(lid, _top(lid), [1.5, 1.0])
    knurl = _fuse(Pos(bxp, byp, bt + bh2 - 3) * Rot(0, 0, q * 360 / 28) * Pos(br + 2, 0, 0) * Box(1.6, 1.6, 5)
                  for q in range(28))
    add("Bubbler lid (knurled)", lid + knurl, C_METAL, "metal", 9, "shell", EBu)
    fit = _zcyl(bxp, byp, bt + bh2 + 7.5, 12, 15)
    fit = _fillet_try(fit, _top(fit), [2.0, 1.0])
    fit += _hex_z(bxp, byp, bt + bh2 + 3, 26, 6)
    add("Bubbler air fitting", fit, C_DARK, "plastic", 9, "shell", EBu)
    pzp = floor + P["port_z"]
    yp = P["port_ys"][0]
    line = _pipe([(cx1 + ins - 2, yp, pzp), (bxp, yp, pzp), (bxp, byp + br + sl - 4, pzp)], 6.0)
    add("Heated wet-air line, sleeved", line, C_FOAM, "fabric", 9, "shell", EBu)
    col = _xcyl(cx1 + ins + 4, yp, pzp, 9.0, 8.0)
    add("Wet-air port collar", col, C_DARK, "plastic", 9, "shell", (EP[0] - 200, 0, 0))

    # ------------------------------------------------------------ 10 dryer column
    EDr = (220, 240, 0)
    dr, dh = P["dryer"]
    dxp, dyp = P["dryer_xy"]
    tube = _zcyl(dxp, dyp, bt + dh / 2, dr, dh)
    add("Dryer column tube (clear acrylic)", tube, C_CLEAR, "clear", 10, "shell", EDr)
    gel = _zcyl(dxp, dyp, bt + 12 + (dh - 40) / 2, dr - 2.5, dh - 40)
    add("Indicating silica gel", gel, C_GEL, "plastic", 10, "shell", EDr)
    caps = _zcyl(dxp, dyp, bt + 6, dr + 1.5, 12) + _zcyl(dxp, dyp, bt + dh - 6, dr + 1.5, 12)
    caps = _fillet_try(caps, caps.edges(), [1.0, 0.5])
    add("Dryer end caps", caps, C_DARK, "plastic", 10, "shell", EDr)
    dfit = _zcyl(dxp, dyp, bt + dh + 6, 10, 12)
    dfit = _fillet_try(dfit, _top(dfit), [2.0, 1.0])
    add("Dryer air fitting", dfit, C_DARK, "plastic", 10, "shell", EDr)
    yp2 = P["port_ys"][1]
    dline = _pipe([(cx1 + ins - 2, yp2, pzp), (dxp, yp2, pzp), (dxp, dyp - dr + 3, pzp)], 4.5)
    add("Dry-air line (silicone)", dline, C_TUBE, "plastic", 10, "shell", EDr)

    # ------------------------------------------------------------ 11 HEPA scrubber loop
    EH = (-60, 380, 0)
    hx_, hy_, hz_ = P["hepa"]
    y0 = cy1 + ins + 5
    hb = _bx(P["hepa_x"] - hx_ / 2, P["hepa_x"] + hx_ / 2, y0, y0 + hy_, bt, bt + hz_)
    hb = _fillet_try(hb, _par(hb, Axis.Z), [8.0, 5.0])
    hb = _fillet_try(hb, _top(hb), [3.0, 2.0])
    for q in range(9):
        hb -= _box(P["hepa_x"] - 48 + q * 12, y0 + hy_ / 2, bt + hz_, 4.0, hy_ - 20, 3.0)
    add("HEPA scrubber housing", hb, C_JACKET, "plastic", 11, "shell", EH)
    hl = _box(P["hepa_x"], y0 + hy_ + 0.2, bt + hz_ / 2, 60, 0.4, 24)
    add("HEPA filter label", hl, C_ACCENT, "painted", 11, "shell", EH)

    # ------------------------------------------------------------ 12 aerosol injection port
    EA = (-380, 0, 0)
    az = floor + P["aero_z"]
    stub = _xcyl(cx0 - ins - 15, 0, az, P["aero_d"] / 2 - 2, 30 + 2 * t)
    stub += _xcyl(cx0 - ins - 2, 0, az, P["aero_d"] / 2 + 4, 4)
    add("Aerosol port stub and flange", stub, C_METAL, "metal", 12, "shell", EA)
    vb = _bx(cx0 - ins - 46, cx0 - ins - 30, -14, 14, az - 14, az + 14)
    vb = _fillet_try(vb, vb.edges(), [3.0, 2.0, 1.0])
    add("Aerosol ball valve body (brass)", vb, C_BRASS, "metal", 12, "shell", EA)
    lev = _box(cx0 - ins - 38, 0, az + 17, 8, 44, 4) + _zcyl(cx0 - ins - 38, 0, az + 15, 4, 4)
    lev = _fillet_try(lev, lev.edges().filter_by(Axis.Z), [1.5, 0.8])
    add("Aerosol valve lever", lev, C_ACCENT, "plastic", 12, "shell", EA)
    luer = _xcyl(cx0 - ins - 46 - 5, 0, az, 5.0, 10)
    add("Luer syringe port", luer, C_TUBE, "plastic", 12, "shell", EA)

    # ------------------------------------------------------------ 13 controller, 14 power supply
    EC = (150, 380, 0)
    cxx, cyy, czz = P["ctrl"]
    cb = _bx(P["ctrl_x"] - cxx / 2, P["ctrl_x"] + cxx / 2, y0 + 3, y0 + 3 + cyy, bt, bt + czz)
    cb = _fillet_try(cb, _par(cb, Axis.Z), [6.0, 4.0])
    cb = _fillet_try(cb, _top(cb), [2.5, 1.5])
    for q in range(8):
        cb -= _box(P["ctrl_x"] - 60 + q * 8, y0 + 3 + cyy / 2, bt + czz, 3.0, cyy - 22, 2.0)
    add("Controller enclosure", cb, C_DARK, "plastic", 13, "shell", EC)
    cl = _box(P["ctrl_x"] + 45, y0 + 3 + cyy / 2, bt + czz + 0.2, 40, 22, 0.4)
    add("Controller label", cl, C_ACCENT, "painted", 13, "shell", EC)
    cled = _zcyl(P["ctrl_x"] + 70, y0 + 3 + 12, bt + czz + 0.5, 2.2, 1.2)
    add("Controller status light (lit)", cled, C_LED_G, "emissive", 13, "shell", EC)
    px_, py_, pz_ = P["psu"]
    ps = _bx(P["psu_x"] - px_ / 2, P["psu_x"] + px_ / 2, y0 + 3, y0 + 3 + py_, bt, bt + pz_)
    ps = _fillet_try(ps, ps.edges(), [4.0, 2.5, 1.5])
    add("12 V power supply (external)", ps, C_BLACK, "plastic", 14, "shell", (0, 380, 0))
    pl = _box(P["psu_x"], y0 + 3 + py_ / 2, bt + pz_ + 0.2, 70, 34, 0.4)
    add("Power supply rating label", pl, C_LABEL, "paper", 14, "shell", (0, 380, 0))
    dc = _pipe([(P["psu_x"] + px_ / 2 - 1, y0 + 3 + py_ / 2, bt + 15), (P["ctrl_x"] - cxx / 2 + 1, y0 + 3 + py_ / 2, bt + 15)], 3.0)
    add("DC lead", dc, C_BLACK, "rubber", 14, "shell", (0, 380, 0))

    # ------------------------------------------------------------ 15 salt fixed-point jars
    EJ = (-40, -170, 0)
    jr, jh = P["jar"]
    for k, x in enumerate(P["jar_xs"]):
        gj = _zcyl(x, P["jar_y"], bt + (jh - 8) / 2, jr, jh - 8)
        gj = _fillet_try(gj, _bottom(gj), [2.0, 1.0])
        add(f"Salt jar {k + 1} (glass)", gj, C_CLEAR, "clear", 15, "shell", EJ)
        salt = _zcyl(x, P["jar_y"], bt + 1.5 + 9, jr - 1.5, 18)
        add(f"Salt jar {k + 1} slurry", salt, C_SALT, "plastic", 15, "shell", EJ)
        cap = _zcyl(x, P["jar_y"], bt + jh - 4, jr + 0.8, 8)
        cap = _fillet_try(cap, _top(cap), [1.5, 1.0])
        add(f"Salt jar {k + 1} lid", cap, LID_COLS[k], "plastic", 15, "shell", EJ)
        band = _zcyl(x, P["jar_y"], bt + 20, jr + 0.3, 12) - _zcyl(x, P["jar_y"], bt + 20, jr - 0.2, 14)
        band &= _box(x, P["jar_y"] - jr, bt + 20, 2 * jr, 2 * jr, 14)
        add(f"Salt jar {k + 1} label", band, C_LABEL, "paper", 15, "shell", EJ)

    # ------------------------------------------------------------ 3 removable door panel (accessory)
    lw, ld, lh = P["latch"]
    dp = _bx(cx0 - ins, cx1 + ins, D["door_y0"] - ld - ins, D["door_y0"] - ld, bt, cz1 + ins)
    dp = _fillet_try(dp, _par(dp, Axis.Y), [12.0, 8.0])
    dp = _fillet_try(dp, _front(dp), [2.5, 1.5])
    add("Removable door panel (XPS, faced)", dp, C_JACKET, "plastic", 3, "accessory", (-640, -520, 0))
    hnd = _box((cx0 + cx1) / 2, D["door_y0"] - ld - ins - 6, cz1 - 20, 120, 12, 18)
    hnd = _fillet_try(hnd, hnd.edges(), [4.0, 2.0])
    hnd -= _box((cx0 + cx1) / 2, D["door_y0"] - ld - ins - 6, cz1 - 24, 96, 20, 10)
    add("Door panel pull handle", hnd, C_DARK, "plastic", 3, "accessory", (-640, -520, 0))

    # ------------------------------------------------------------ context (not in the BOM)
    bench = _bx(-400, 400, -300, 300, -32, 0)
    bench = _fillet_try(bench, _top(bench), [3.0, 2.0])
    add("Lab bench top (laminate)", bench, C_BENCH, "plastic", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")

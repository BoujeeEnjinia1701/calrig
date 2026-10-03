"""CalRig product appearance model (build123d), TRL 3, constructable design (CLR-DDR-003).

Finished-product look for photoreal renders of the design as it will be built: a 9 mm sealed
birch plywood base; the insulation jacket in five faced panels with seams (facing in renders
only, CLR-DEC-001); the front badge on the jacket top with the name plate and lit status light
and its lead to the controller; the clear acrylic shell with its welded front frame, drip tray and
fan spacers; the clear door with its printed border, gasket, four draw latches and keepers (no
gland in the door); inside, the perforated six-bay sensor tray with example heads, the reference
cluster on its printed mast, the guarded 120 mm mixing fan on its spacers and the finned inner
Peltier sink; outside, the clamped outer sink and guarded fan, the bulkhead fittings, the two
cable glands and the HEPA bulkheads in the back wall, the drain line and bottle, the two air
pumps, the foam-sleeved bubbler, the dryer column in its socket, the aerosol port and ball valve,
the HEPA unit, controller and power supply, the salt jars in their rack and the removable door
panel with its pull handle (accessory). Context is a compact lab bench top.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS, derived() and build_components()
in model.py (same axes: X across the bench, conditioning column at +X; Y front, -Y is the door,
to back; Z up; base plate on the bench at z = 0); most parts are the model.py solids themselves.
Differences from model.py are listed in docs/REVIEW.md (sessions 2026-09-26 and 2026-10-02).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived, build_components, fuse

TITLE = "CalRig: benchtop calibration chamber for low-cost air sensors"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -60,
     "note": "Product render from the front right and above (about 30 deg elevation); the sensor tray and "
             "reference cluster show through the clear door with its printed border and four latches; the "
             "front badge and status light sit on the jacket top, with the Peltier fan, bubbler and dryer at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): plywood base, jacket "
             "panels, front badge, acrylic chamber with front frame, door and latches, sensor tray and heads, "
             "reference cluster, mixing fan, Peltier heat pump, bulkheads, bubbler, dryer, pumps, HEPA unit, "
             "controller, power supply, salt jars and the door panel with its pull handle"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 16, "az": -76,
     "note": "Detail from the front, slightly right and above (about 16 deg elevation): six sensor heads on "
             "the tray and the reference cluster behind the clear door, without the bench"},
]

# Colours (restrained product palette; kit accent)
C_JACKET = "#ECEDEE"
C_JACKET_IN = "#DADDE1"
C_BASE = "#D8B98A"          # sealed birch plywood (CLR-DEC-001, 2026-10-02)
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
C_BENCH = "#C9CCD1"
C_FIT = "#F1F1EE"
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
    C = build_components(P, door_panel=True)
    M = lambda k: C[k].shape  # noqa: E731
    t, ins = P["wall"], P["ins"]
    cx0, cx1, cy0, cy1, cz0, cz1 = D["cx0"], D["cx1"], D["cy0"], D["cy1"], D["cz0"], D["cz1"]
    floor, ceil = D["floor"], D["ceil"]
    bx, by, bt = P["base"]
    pz = D["pz"]
    xin, xo = cx1 - t, cx1 + ins
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ 4 base plate: sealed birch plywood
    EB = (0, 0, -200)
    base = _fillet_try(M("base"), _par(M("base"), Axis.Z), [4.0, 2.0])
    base = _fillet_try(base, _top(base), [1.0, 0.5])
    add("Base plate (9 mm sealed birch plywood)", base, C_BASE, "wood", 4, "shell", EB)

    # ------------------------------------------------------------ 3 insulation jacket, faced (renders only)
    ox0, ox1, oy0, oy1, oz0, oz1 = cx0 - ins, cx1 + ins, cy0, cy1 + ins, bt, cz1 + ins
    jo = _bx(ox0, ox1, oy0, oy1, oz0, oz1)
    jo = _fillet_try(jo, _par(jo, Axis.Z), [12.0, 8.0, 5.0])
    jo = _fillet_try(jo, list(_top(jo)), [10.0, 6.0, 4.0])
    jk = jo & fuse(M(f"jacket_{k}") for k in ("bottom", "top", "back", "left", "right"))   # the model's holes
    W, Dp = ox1 - ox0, oy1 - oy0
    ccx, ccy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
    for zs in (cz0, cz1):                      # parting lines where the panels meet
        jk -= _rrect(ccx, ccy, zs - 0.6, zs + 0.6, W + 2, Dp + 2, 13.0) - _rrect(ccx, ccy, zs - 1, zs + 1, W - 2.0, Dp - 2.0, 11.0)
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

    # ------------------------------------------------------------ 20 front badge, name plate, status light, lead
    EBg = (0, -60, 360)
    badge = _fillet_try(M("badge"), _par(M("badge"), Axis.Y), [1.5, 0.8])
    add("Front badge (printed)", badge, C_DARK, "plastic", 20, "shell", EBg)
    add("Name plate", M("name_plate"), C_ACCENT, "painted", 20, "shell", EBg)
    nb = M("name_plate").bounding_box()
    ink_y, zc_ = nb.min.Y - 0.2, (nb.min.Z + nb.max.Z) / 2
    ink = _box(nb.min.X + 22, ink_y, zc_, 30, 0.4, 4.2) + _box(nb.min.X + 70, ink_y, zc_ + 1.2, 52, 0.4, 2.0) \
        + _box(nb.min.X + 64, ink_y, zc_ - 2.0, 40, 0.4, 1.2)
    add("Name plate print", ink, C_LABEL, "paper", 20, "shell", EBg)
    sb = M("status_light").bounding_box()
    lx, lz, fy = (sb.min.X + sb.max.X) / 2, (sb.min.Z + sb.max.Z) / 2, sb.min.Y
    add("Status light bezel", M("status_light") - _ycyl(lx, fy, lz, 3.2, 6), C_METAL, "metal", 20, "shell", EBg)
    lens = (_ycyl(lx, fy + 1.0, lz, 3.2, 2.0) + Pos(lx, fy + 0.4, lz) * Sphere(2.9)) & _box(lx, fy + 1.0, lz, 8, 2.0 + 1.4, 8)
    add("Status light, green (lit)", lens, C_LED_G, "emissive", 20, "shell", EBg)
    add("Status light lead", M("light_lead"), C_BLACK, "rubber", 20, "shell", (0, 120, 300))

    # ------------------------------------------------------------ 1 chamber shell with frame, drip tray, spacers
    add("Chamber shell, 6 mm clear acrylic", M("shell"), C_CLEAR, "clear", 1, "shell", (0, 0, 0))
    add("Front frame, clear acrylic", M("frame"), C_CLEAR, "clear", 1, "shell", (0, -120, 0))
    add("Drip tray, clear acrylic", M("drip"), C_CLEAR, "clear", 1, "internal", (300, 0, 0))
    add("Fan spacers", M("spacers"), C_CLEAR, "clear", 1, "internal", (0, -60, 230))

    # ------------------------------------------------------------ 2 door, printed border, gasket, latches
    ED = (0, -520, 0)
    add("Front door, clear acrylic", M("door"), "#E6F0F5", "clear", 2, "shell", ED)
    add("Door border print", M("border"), C_DARK, "painted", 2, "shell", ED)
    add("Door gasket (silicone)", M("gasket"), C_BLACK, "rubber", 2, "shell", (0, -300, 0))
    add("Latch keepers (4)", M("keepers"), C_METAL, "metal", 2, "shell", ED)
    lat = _fillet_try(M("latches"), M("latches").edges().filter_by(Axis.Y), [1.5, 0.8])
    add("Draw latches (4)", lat, C_METAL, "metal", 2, "shell", (0, -260, 0))

    # ------------------------------------------------------------ 5 Peltier heat pump, clamped through the wall
    EP = (380, 0, 0)
    sxi, syi, szi = P["sink_in"]
    sb_ = P["sink_base"]
    fins = M("sink_in") & _bx(xin - sb_, xin, -900, 900, -900, 900)          # base plate with clamp holes
    n = 17
    pitch = (syi - 1.6) / (n - 1)
    for k in range(n):
        y = -syi / 2 + 0.8 + k * pitch
        fins += _bx(xin - sxi, xin - sb_, y - 0.8, y + 0.8, pz - szi / 2, pz + szi / 2)
    add("Inner Peltier fin block (aluminium)", fins, C_ALU, "metal", 5, "internal", (300, 0, 0))
    add("Peltier module and spacer block", M("pelt_block"), C_ALU, "metal", 5, "internal", (340, 0, 0))
    sxo, syo, szo = P["sink_out"]
    sbo = P["sink_base_out"]
    osk = M("sink_out") & _bx(xo, xo + sbo, -900, 900, -900, 900)
    n = 15
    pitch = (syo - 1.6) / (n - 1)
    for k in range(n):
        y = -syo / 2 + 0.8 + k * pitch
        osk += _bx(xo + sbo, xo + sxo, y - 0.8, y + 0.8, pz - szo / 2, pz + szo / 2)
    add("Outer Peltier heat sink (aluminium)", osk, C_ALU, "metal", 5, "shell", EP)
    add("Clamp screws and sleeves (4)", M("clamp"), C_METAL, "metal", 5, "shell", EP)
    fx, fyy, fz = P["fan_out"]
    fr, ro, gd = _fan(fyy, fx)
    place = Pos(xo + sxo + fx / 2, 0, pz) * Rot(0, 90, 0)
    add("Outer fan frame, 92 mm", place * fr, C_FAN, "plastic", 5, "shell", (EP[0] + 60, 0, 0))
    add("Outer fan rotor", place * ro, C_ROTOR, "plastic", 5, "shell", (EP[0] + 60, 0, 0))
    add("Outer fan finger guard", place * gd, C_METAL, "metal", 5, "shell", (EP[0] + 60, 0, 0))

    # ------------------------------------------------------------ 6 internal mixing fan on its spacers
    mb = M("mixfan").bounding_box()
    f, ft = P["mix_fan"], P["mix_fan_t"]
    fr, ro, gd = _fan(f, ft)
    place = Pos((mb.min.X + mb.max.X) / 2, (mb.min.Y + mb.max.Y) / 2, (mb.min.Z + mb.max.Z) / 2) * Rot(90, 0, 0)
    EM = (0, -60, 230)
    add("Mixing fan frame, 120 mm", place * fr, C_FAN, "plastic", 6, "internal", EM)
    add("Mixing fan rotor", place * ro, C_ROTOR, "plastic", 6, "internal", EM)
    add("Mixing fan guard", place * gd, C_METAL, "metal", 6, "internal", EM)

    # ------------------------------------------------------------ 7 sensor tray and example heads
    ET = (0, -250, 0)
    tx0, ty0 = D["tray_x0"], D["tray_y0"]
    TL, TD = D["tray_len"], D["tray_dep"]
    tz0 = floor + P["tray_z"]
    rail_r = _bx(tx0 - 1, tx0 + TL + 1, ty0 + TD, ty0 + TD + 13, tz0, tz0 + 26)
    add("Sensor tray, perforated acrylic", M("tray") - rail_r, "#EEF1F3", "plastic", 7, "internal", ET)
    add("Cable rail", M("tray") & rail_r, C_DARK, "plastic", 7, "internal", ET)
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

    # ------------------------------------------------------------ 8 reference cluster on its printed mast
    ER = (0, -150, 170)
    add("Reference mast (printed)", M("mast"), C_DARK, "plastic", 8, "internal", ER)
    rb = M("ref").bounding_box()
    rcx, rcy, rz0 = (rb.min.X + rb.max.X) / 2, (rb.min.Y + rb.max.Y) / 2, rb.min.Z
    rx, ry, rz = P["ref"]
    rh = M("ref")
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
    add("Reference cluster label", _box(rcx + 18, rcy - ry / 2 - 0.5, rz0 + 12, 22, 0.3, 6), C_LABEL, "paper", 8, "internal", ER)
    add("Reference cluster status light (lit)", _ycyl(rcx + 30, rcy - ry / 2 - 0.6, rz0 + rz - 12, 2.0, 1.2),
        C_LED_T, "emissive", 8, "internal", ER)

    # ------------------------------------------------------------ 19 bulkheads, glands, drain line and bottle
    EF = (300, 0, 0)
    add("Inlet and suction bulkheads (3)", M("fit_cond"), C_FIT, "plastic", 19, "shell", EF)
    add("Drain bulkhead", M("fit_drain"), C_FIT, "plastic", 19, "shell", EF)
    add("HEPA bulkheads (2)", M("fit_hepa"), C_FIT, "plastic", 19, "shell", (0, 300, 0))
    gl = M("glands")
    for x in P["glands"]:                                    # hex body on the outside part of each gland
        gl += _hex_y(x, cy1 + 4, floor + P["gland_z"], 24.0, 8.0)
    add("Cable glands (2), M20 nylon", gl, C_DARK, "plastic", 19, "shell", (0, 300, 0))
    bxb, byb = P["bottle_xy"]
    brr, bhh = P["bottle"]
    bot = _zcyl(bxb, byb, bt + (bhh - 8) / 2, brr, bhh - 8)
    bot = _fillet_try(bot, _top(bot), [3.0, 1.5])
    add("Drain bottle (HDPE)", bot, "#F3F1EA", "plastic", 19, "shell", (420, 0, 0))
    add("Drain bottle cap", _zcyl(bxb, byb, bt + bhh - 4, 6.0, 8), C_DARK, "plastic", 19, "shell", (420, 0, 0))
    dr_ = M("drain") - _zcyl(bxb, byb, bt + bhh / 2 - 1, brr + 0.5, bhh + 2)
    add("Drain line (silicone)", dr_, C_TUBE, "plastic", 19, "shell", (420, 0, 0))

    # ------------------------------------------------------------ 9 humidifier bubbler and 9, 10 air pumps
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
    add("Bubbler glass jar (clear)", _zcyl(bxp, byp, bt + bh2 - 16 + 6, br, 12), C_CLEAR, "clear", 9, "shell", EBu)
    lid = _zcyl(bxp, byp, bt + bh2 - 3, br + 2, 6)
    lid = _fillet_try(lid, _top(lid), [1.5, 1.0])
    knurl = _fuse(Pos(bxp, byp, bt + bh2 - 3) * Rot(0, 0, q * 360 / 28) * Pos(br + 2, 0, 0) * Box(1.6, 1.6, 5)
                  for q in range(28))
    add("Bubbler lid (knurled)", lid + knurl, C_METAL, "metal", 9, "shell", EBu)
    fit = _zcyl(bxp, byp, bt + bh2 + 7.5, 12, 15)
    fit = _fillet_try(fit, _top(fit), [2.0, 1.0])
    fit += _hex_z(bxp, byp, bt + bh2 + 3, 26, 6)
    add("Bubbler air fitting", fit, C_DARK, "plastic", 9, "shell", EBu)
    zp = floor + P["port_z"]
    yA, yB = P["port_ys"]
    xout = xo + 4.0
    line = _pipe([(xout, yA, zp), (bxp, yA, zp)], 6.0)
    add("Heated wet-air line, sleeved", line, C_FOAM, "fabric", 9, "shell", EBu)
    px, pyd, ph = P["pump"]
    pumps = None
    for x in P["pump_xs"]:
        pb = _bx(x - px / 2, x + px / 2, P["pump_y"] - pyd / 2, P["pump_y"] + pyd / 2, bt, bt + ph)
        pb = _fillet_try(pb, _par(pb, Axis.Z), [4.0, 2.0])
        pb = _fillet_try(pb, _top(pb), [2.0, 1.0])
        pumps = pb if pumps is None else pumps + pb
    add("Air pumps (2)", pumps, C_HEAD_D, "plastic", 9, "shell", (330, -60, 0))
    ys_, zs_ = P["suction"][0], floor + P["suction"][1]
    xa = P["pump_xs"][0]
    add("Suction line (silicone)", _pipe([(xout, ys_, zs_), (xa, ys_, zs_), (xa, ys_, bt + ph)], 4.0),
        C_TUBE, "plastic", 9, "shell", (330, -60, 0))

    # ------------------------------------------------------------ 10 dryer column in its printed socket
    EDr = (220, 240, 0)
    dr, dh = P["dryer"]
    dxp, dyp = P["dryer_xy"]
    add("Dryer socket (printed)", M("dryer_socket"), C_DARK, "plastic", 10, "shell", EDr)
    z0d = bt + 4
    add("Dryer column tube (clear acrylic)", _zcyl(dxp, dyp, z0d + dh / 2, dr, dh), C_CLEAR, "clear", 10, "shell", EDr)
    add("Indicating silica gel", _zcyl(dxp, dyp, z0d + 12 + (dh - 40) / 2, dr - 2.5, dh - 40), C_GEL, "plastic", 10, "shell", EDr)
    caps = _zcyl(dxp, dyp, z0d + dh - 6, dr + 1.5, 12)
    caps = _fillet_try(caps, caps.edges(), [1.0, 0.5])
    add("Dryer end cap", caps, C_DARK, "plastic", 10, "shell", EDr)
    dfit = _zcyl(dxp, dyp, z0d + dh + 6, 10, 12)
    dfit = _fillet_try(dfit, _top(dfit), [2.0, 1.0])
    add("Dryer air fitting", dfit, C_DARK, "plastic", 10, "shell", EDr)
    add("Dry-air line (silicone)", _pipe([(xout, yB, zp), (dxp - 20, yB, zp), (dxp - 20, dyp - 10, zp)], 4.5),
        C_TUBE, "plastic", 10, "shell", EDr)

    # ------------------------------------------------------------ 11 HEPA scrubber unit
    EH = (-60, 380, 0)
    hb = _fillet_try(M("hepa"), _par(M("hepa"), Axis.Z), [8.0, 5.0])
    hb = _fillet_try(hb, _top(hb), [3.0, 2.0])
    hbb = M("hepa").bounding_box()
    hx_, hy_, hz_ = P["hepa"]
    for q in range(9):
        hb -= _box(P["hepa_x"] - 48 + q * 12, (hbb.min.Y + hbb.max.Y) / 2, bt + hz_, 4.0, hy_ - 20, 3.0)
    add("HEPA scrubber housing", hb, C_JACKET, "plastic", 11, "shell", EH)
    add("HEPA filter label", _box(P["hepa_x"], hbb.max.Y + 0.2, bt + hz_ / 2, 60, 0.4, 24), C_ACCENT, "painted", 11, "shell", EH)

    # ------------------------------------------------------------ 12 aerosol injection port
    EA = (-380, 0, 0)
    az = floor + P["aero_z"]
    pt = M("port") - _bx(cx0 - ins - 47, cx0 - ins - 29, -15, 15, az - 15, az + 15)
    add("Aerosol port bulkhead and stub", pt, C_METAL, "metal", 12, "shell", EA)
    vb = _bx(cx0 - ins - 46, cx0 - ins - 30, -14, 14, az - 14, az + 14)
    vb = _fillet_try(vb, vb.edges(), [3.0, 2.0, 1.0])
    add("Aerosol ball valve body (brass)", vb, C_BRASS, "metal", 12, "shell", EA)
    lev = _box(cx0 - ins - 38, 0, az + 17, 8, 44, 4) + _zcyl(cx0 - ins - 38, 0, az + 15, 4, 4)
    lev = _fillet_try(lev, lev.edges().filter_by(Axis.Z), [1.5, 0.8])
    add("Aerosol valve lever", lev, C_ACCENT, "plastic", 12, "shell", EA)
    add("Luer syringe port", _xcyl(cx0 - ins - 46 - 5, 0, az, 5.0, 10), C_TUBE, "plastic", 12, "shell", EA)

    # ------------------------------------------------------------ 13 controller, 14 power supply
    EC = (150, 380, 0)
    cxx, cyy, czz = P["ctrl"]
    y0 = cy1 + ins + 5
    cb = _fillet_try(M("ctrl"), _par(M("ctrl"), Axis.Z), [6.0, 4.0])
    cb = _fillet_try(cb, _top(cb), [2.5, 1.5])
    for q in range(6):
        cb -= _box(P["ctrl_x"] - 60 + q * 8, y0 + 3 + cyy / 2 + 6, bt + czz, 3.0, cyy - 30, 2.0)
    add("Controller enclosure", cb, C_DARK, "plastic", 13, "shell", EC)
    add("Controller label", _box(P["ctrl_x"] + 45, y0 + 3 + cyy / 2 + 6, bt + czz + 0.2, 40, 22, 0.4), C_ACCENT, "painted", 13, "shell", EC)
    add("Controller status light (lit)", _zcyl(P["ctrl_x"] + 70, y0 + 3 + 40, bt + czz + 0.5, 2.2, 1.2), C_LED_G, "emissive", 13, "shell", EC)
    px_, py_, pz_ = P["psu"]
    ps = _fillet_try(M("psu"), M("psu").edges(), [4.0, 2.5, 1.5])
    add("12 V power supply (external)", ps, C_BLACK, "plastic", 14, "shell", (0, 380, 0))
    add("Power supply rating label", _box(P["psu_x"], y0 + 3 + py_ / 2, bt + pz_ + 0.2, 70, 34, 0.4), C_LABEL, "paper", 14, "shell", (0, 380, 0))
    dc = _pipe([(P["psu_x"] + px_ / 2 - 1, y0 + 3 + py_ / 2, bt + 15), (P["ctrl_x"] - cxx / 2 + 1, y0 + 3 + py_ / 2, bt + 15)], 3.0)
    add("DC lead", dc, C_BLACK, "rubber", 14, "shell", (0, 380, 0))

    # ------------------------------------------------------------ 15 salt fixed-point jars in their printed rack
    EJ = (-40, -170, 0)
    add("Jar rack (printed)", M("jar_rack"), C_DARK, "plastic", 15, "shell", EJ)
    jr, jh = P["jar"]
    for k, x in enumerate(P["jar_xs"]):
        gj = _zcyl(x, P["jar_y"], bt + (jh - 8) / 2, jr, jh - 8)
        gj = _fillet_try(gj, _bottom(gj), [2.0, 1.0])
        add(f"Salt jar {k + 1} (glass)", gj, C_CLEAR, "clear", 15, "shell", EJ)
        add(f"Salt jar {k + 1} slurry", _zcyl(x, P["jar_y"], bt + 1.5 + 9, jr - 1.5, 18), C_SALT, "plastic", 15, "shell", EJ)
        cap = _zcyl(x, P["jar_y"], bt + jh - 4, jr + 0.8, 8)
        cap = _fillet_try(cap, _top(cap), [1.5, 1.0])
        add(f"Salt jar {k + 1} lid", cap, LID_COLS[k], "plastic", 15, "shell", EJ)
        band = _zcyl(x, P["jar_y"], bt + 26, jr + 0.3, 8) - _zcyl(x, P["jar_y"], bt + 26, jr - 0.2, 10)
        band &= _box(x, P["jar_y"] - jr, bt + 26, 2 * jr, 2 * jr, 10)
        add(f"Salt jar {k + 1} label", band, C_LABEL, "paper", 15, "shell", EJ)

    # ------------------------------------------------------------ 3 removable door panel with pull handle (accessory)
    EDP = (-640, -520, 0)
    dp = _fillet_try(M("door_panel"), _front(M("door_panel")), [2.5, 1.5])
    add("Removable door panel (XPS, white vinyl face)", dp, C_JACKET, "plastic", 3, "accessory", EDP)
    hnd = _fillet_try(M("handle"), M("handle").edges().filter_by(Axis.X), [2.0, 1.0])
    add("Door panel pull handle (printed)", hnd, C_DARK, "plastic", 3, "accessory", EDP)

    # ------------------------------------------------------------ context (not in the BOM)
    bench = _bx(-400, 400, -300, 300, -32, 0)
    bench = _fillet_try(bench, _top(bench), [3.0, 2.0])
    add("Lab bench top (laminate)", bench, C_BENCH, "plastic", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")

"""CalRig parametric model (build123d), TRL 3, constructable design (CLR-DDR-003).

Run from the repo root:  python cad/src/model.py          (export STEP and STL, print the checks)
                         python cad/src/model.py --check  (constructability checks only)
Exports STEP and STL into cad/step and cad/stl:
    calrig-assembly.step / .stl     the whole rig on its base plate (door panel fitted)
    chamber.step / .stl             chamber shell with frame, door (printed border), gasket, latches, jacket,
                                    door panel with pull handle, front badge with name plate and status light
    conditioning.step / .stl        Peltier assembly, bubbler, dryer, pumps, HEPA loop, aerosol port,
                                    bulkhead fittings and drain

Axes: X across the bench (conditioning column at +X), Y front (-Y, door) to back (+Y), Z up.
Units mm. The base plate sits on the bench at z = 0 and is centred on the origin.

The design is constructable (STANDARDS section 18): every part is cut, laser cut, printed or bought,
and every part touches and is fixed to the parts next to it. build_components() returns each part
separately (for the build plan pictures and the checks); build_parts() fuses them into the BOM
groups that the calculation note, the drawing and the concept media use. checks() tests, with
build123d, that parts which must touch do touch and parts which must not touch are apart, and that
the R10 large heads of large_heads() fit the tray (decisions of 2026-10-02, CLR-DEC-001).
Not fabrication detail; drawings carry no tolerances before TRL 4.
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 4 base plate (bench footprint, R13); 9 mm birch plywood (CLR-DDR-003, mass)
    "base": (600.0, 500.0, 9.0),
    # 1 chamber: inside size (x, y, z), acrylic wall
    "inner": (400.0, 300.0, 300.0), "wall": 6.0,
    "chamber_x0": -229.0,             # outside left face of the chamber
    # 1 front frame welded to the shell's open front: margin beyond the opening, latch tabs
    "frame_m": 25.0, "frame_t": 6.0, "tab": (41.0, 40.0),
    # 3 insulation jacket: XPS thickness on all faces except the door; removable door panel
    "ins": 25.0, "panel_m": 3.0,      # door panel covers the opening plus 3 mm each side
    # 2 door: acrylic thickness, overlap past the opening, gasket (thickness, band from, band to)
    "door_t": 6.0, "door_ov": 15.0, "gasket": (3.0, 4.0, 12.0),
    # draw latches: body (x, y, z) on the frame tabs, heights from the opening's centre
    "latch": (32.0, 12.0, 30.0), "latch_dz": (-95.0, 95.0),
    # 5 Peltier assembly on the +X wall: opening, inner sink, outer sink, outer fan
    "pelt_open": (90.0, 100.0), "pelt_z": 200.0,  # opening (y, z) and its centre height above the chamber floor
    # inner sink enlarged to about 0.20 K/W (CLR-DDR-002, decided by Amish 2026-09-25) so the
    # 20 C, 85 % RH point stays above the dew point in rooms up to about 28 C
    "sink_in": (45.0, 120.0, 110.0), "sink_in_r": 0.20,
    "sink_out": (40.0, 110.0, 110.0), "fan_out": (25.0, 92.0, 92.0),
    "sink_base": 12.0, "sink_base_out": 10.0,       # base plate thickness of each sink
    "clamp": (57.0, 42.0),            # four clamp screws at y = +-57, z = pelt_z +- 42
    # 6 internal mixing fan, 120 mm class (CLR-CAL-001 section E), on four 15 mm spacers
    "mix_fan": 120.0, "mix_fan_t": 25.0, "fan_gap": 15.0,
    # 7 sensor tray: plate height above the chamber floor, bay size (largest head, R10), grid
    "tray_z": 50.0, "tray_t": 6.0, "bay": (90.0, 70.0, 50.0), "bays": (3, 2), "bay_gap": 12.0,
    "tray_hole": (8.0, 24.0),         # perforation: hole diameter, pitch
    # 8 reference cluster on a printed mast standing behind the tray rail
    "ref": (80.0, 40.0, 55.0), "ref_z": 120.0, "mast": 20.0,
    # 9, 10 conditioning column: bubbler jar with foam sleeve, dryer column in a printed socket
    "bubbler": (35.0, 150.0), "bubbler_xy": (255.0, -100.0), "sleeve": 10.0,
    "dryer": (25.0, 230.0), "dryer_xy": (270.0, 100.0),
    "port_d": 12.0, "port_ys": (-60.0, 60.0), "port_z": 40.0,   # conditioning inlets on the +X wall
    "suction": (-36.0, 20.0),         # suction port (y, height above the chamber floor) on the +X wall
    "pump": (30.0, 28.0, 30.0), "pump_xs": (233.0, 271.0), "pump_y": -36.0,
    # drip tray under the inner sink and its drain
    "drip": (50.0, 130.0, 14.0), "drain_y": 5.0, "bottle": (15.0, 80.0), "bottle_xy": (270.0, 5.0),
    # 11 HEPA scrubber loop behind the chamber, two ports in the back wall
    "hepa": (140.0, 60.0, 130.0), "hepa_x": -130.0, "hepa_ports": (-40.0, 40.0), "hepa_pz": 77.0,
    # cable glands in the back wall (x positions, height above the chamber floor, M20)
    "glands": (40.0, 100.0), "gland_z": 37.0, "gland_d": 20.0,
    # 12 aerosol port on the -X wall: 16 mm bulkhead stub; jacket clearance hole
    "aero_d": 20.0, "aero_stub": 16.0, "aero_z": 210.0,
    # 13, 14 controller and power supply behind the chamber
    "ctrl": (160.0, 55.0, 50.0), "ctrl_x": 205.0,
    "psu": (140.0, 55.0, 38.0), "psu_x": 30.0,
    # 15 salt fixed-point jars in a printed rack, front right
    "jar": (13.0, 40.0), "jar_y": -225.0, "jar_xs": (195.0, 223.0, 251.0, 279.0),
    # 20 front badge (CLR-DEC-001, 2026-10-02): printed strip on the front of the top jacket panel, its lip
    # resting on the front frame's top edge; carries the name plate and the status light. Width, depth
    # back from the frame's front face, height above the jacket top; light centre from the badge's right end
    "badge": (200.0, 30.0, 12.0), "led_in": 20.0, "led": (2.5, 5.0, 2.0),   # light body r, bezel r, bezel depth
    "plate": (120.0, 10.0),           # name plate label (width, height) on the badge's front face
    "lead": 3.0, "lead_x": 160.0,     # status light lead (square section) and where it runs down the back
    # 2 printed border on the door's front face (opaque, hides the frame edges); 3 door panel pull handle
    "border": 22.0, "handle": (120.0, 30.0, 4.0, 100.0, 12.0, 25.0),   # flange w, h, t; grip length, section, reach
    # R10 large item case (CLR-DEC-001, 2026-10-02): heads checked at the clear height less this gap
    "large_gap": 10.0,
}

FIT_OUT = 4.0      # bulkhead fittings stand 4 mm proud of the jacket's outer face


def derived(p=PARAMS):
    """Dimensions the calc note and drawings quote, computed from PARAMS."""
    ix, iy, iz = p["inner"]
    t, ins = p["wall"], p["ins"]
    bx, by, bt = p["base"]
    cx0 = p["chamber_x0"]
    cx1 = cx0 + ix + 2 * t
    cy0, cy1 = -(iy / 2 + t), iy / 2 + t
    cz0 = bt + ins                         # chamber sits on the bottom jacket panel
    cz1 = cz0 + iz + 2 * t
    floor = cz0 + t                        # inside floor
    ceil = cz1 - t
    n_x, n_y = p["bays"]
    bw, bd, bh = p["bay"]
    g = p["bay_gap"]
    tray_len = n_x * bw + (n_x + 1) * g
    tray_dep = n_y * bd + (n_y + 1) * g
    ft, (gt, _, _) = p["frame_t"], p["gasket"]
    door_y1 = cy0 - ft - gt                # back face of the door (on the gasket)
    door_y0 = door_y1 - p["door_t"]        # front face of the door
    sink_out_x1 = cx1 + ins + p["sink_out"][0]
    fan_out_x1 = sink_out_x1 + p["fan_out"][0]
    aero_x0 = cx0 - ins - 30.0 - 16.0      # stub 30 mm plus valve 16 mm
    overall = {
        "x0": min(-bx / 2, aero_x0), "x1": max(bx / 2, fan_out_x1,
                                              p["bubbler_xy"][0] + p["bubbler"][0] + p["sleeve"],
                                              p["dryer_xy"][0] + p["dryer"][0] + 4, max(p["jar_xs"]) + p["jar"][0]),
        "y0": -by / 2, "y1": by / 2, "z1": cz1 + ins + p["badge"][2],
    }
    return {
        "cx0": cx0, "cx1": cx1, "cy0": cy0, "cy1": cy1, "cz0": cz0, "cz1": cz1, "floor": floor, "ceil": ceil,
        "ox0": cx0 + t, "ox1": cx1 - t, "oxc": (cx0 + cx1) / 2, "ozc": (floor + ceil) / 2,
        "volume_l": ix * iy * iz / 1e6,
        "outer": (cx1 - cx0, cy1 - cy0, cz1 - cz0),
        "tray_len": tray_len, "tray_dep": tray_dep,
        "tray_x0": cx0 + t + 10, "tray_y0": cy0 + t + 10,
        "tray_top": floor + p["tray_z"] + p["tray_t"],
        "head_clear": (cz1 - t) - (floor + p["tray_z"] + p["tray_t"]),
        # R10 large item case: two bays side by side, and a 2 x 2 block of four bays (bays plus the gap)
        "pair": (2 * p["bay"][0] + p["bay_gap"], p["bay"][1]),
        "block": (2 * p["bay"][0] + p["bay_gap"], 2 * p["bay"][1] + p["bay_gap"]),
        "door_y0": door_y0, "door_y1": door_y1,
        "door_size": (ix + 2 * p["door_ov"], iz + 2 * p["door_ov"]),
        "frame_size": (ix + 2 * p["frame_m"], iz + 2 * p["frame_m"]),
        "pz": floor + p["pelt_z"],
        "overall": overall,
        "footprint": (overall["x1"] - overall["x0"], overall["y1"] - overall["y0"]),
        "height": overall["z1"],
        # inside wall areas (m2) for the heat balance: door face separately
        "area_door": ix * iz / 1e6,
        "area_jacketed": (2 * iy * iz + 2 * ix * iy + ix * iz) / 1e6,
        "area_shell_in": (2 * iy * iz + 2 * ix * iy + ix * iz) / 1e6,
        "pelt_open_area": p["pelt_open"][0] * p["pelt_open"][1] / 1e6,
    }


def _b():
    import build123d as b
    return b


def box(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def zcyl(x, y, z0, r, h):
    b = _b()
    return b.Pos(x, y, z0 + h / 2) * b.Cylinder(r, h)


def xcyl(x0, x1, y, z, r):
    b = _b()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, abs(x1 - x0))


def ycyl(y0, y1, x, z, r):
    b = _b()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(y1 - y0))


def fuse(shapes):
    out = None
    for s in shapes:
        if s is not None:
            out = s if out is None else out + s
    return out


Comp = namedtuple("Comp", "name shape bom kind")


def build_components(p=PARAMS, door_panel=True):
    """Every component as its own solid: {key: Comp(name, shape, bom line, make/buy)}."""
    D = derived(p)
    t, ins = p["wall"], p["ins"]
    cx0, cx1, cy0, cy1, cz0, cz1 = D["cx0"], D["cx1"], D["cy0"], D["cy1"], D["cz0"], D["cz1"]
    floor, ceil = D["floor"], D["ceil"]
    ox0, ox1, oxc = D["ox0"], D["ox1"], D["oxc"]
    ozc = D["ozc"]
    bx, by, bt = p["base"]
    pz = D["pz"]
    oy, oz = p["pelt_open"]
    C = {}

    def add(key, name, shape, bom, kind):
        C[key] = Comp(name, shape, bom, kind)

    mx = lambda x: 2 * oxc - x  # noqa: E731  mirror an x position about the opening's centre line

    # 4 base plate
    add("base", "Base plate", box(-bx / 2, bx / 2, -by / 2, by / 2, 0, bt), 4, "make")

    # ---- positions of everything that passes through a wall
    xin, xout = cx1 - t, cx1 + ins + FIT_OUT          # right wall inside face, fitting outer end
    ports = [(y, floor + p["port_z"]) for y in p["port_ys"]] + [(p["suction"][0], floor + p["suction"][1])]
    pin = p["drip"]
    drip_z0 = pz - p["sink_in"][2] / 2 - 4 - pin[2]   # drip tray floor underside, 4 mm below the inner sink
    drain = (p["drain_y"], drip_z0 + 8.0)
    clamps = [(sy * p["clamp"][0], pz + sz * p["clamp"][1]) for sy in (-1, 1) for sz in (-1, 1)]
    az = floor + p["aero_z"]
    hz = floor + p["hepa_pz"]
    hxs = [p["hepa_x"] + d for d in p["hepa_ports"]]
    gz = floor + p["gland_z"]

    # 1 chamber shell, five-sided, open at -Y for the door, with every hole it needs
    shell = box(cx0, cx1, cy0, cy1, cz0, cz1) - box(cx0 + t, cx1 - t, cy0 - 1, cy1 - t, cz0 + t, cz1 - t)
    shell -= box(xin - 1, cx1 + 1, -oy / 2, oy / 2, pz - oz / 2, pz + oz / 2)
    shell -= xcyl(cx0 - 1, cx0 + t + 1, 0, az, p["aero_stub"] / 2)
    for y, z in ports:
        shell -= xcyl(xin - 1, cx1 + 1, y, z, p["port_d"] / 2)
    shell -= xcyl(xin - 1, cx1 + 1, drain[0], drain[1], 3.0)
    for y, z in clamps:
        shell -= xcyl(xin - 1, cx1 + 1, y, z, 2.0)
    for x in hxs:
        shell -= ycyl(cy1 - t - 1, cy1 + 1, x, hz, p["port_d"] / 2)
    for x in p["glands"]:
        shell -= ycyl(cy1 - t - 1, cy1 + 1, x, gz, p["gland_d"] / 2)
    add("shell", "Chamber shell", shell, 1, "make")

    # 1 front frame, welded to the shell's front edges; tabs carry the latches
    fm, ftk = p["frame_m"], p["frame_t"]
    tw, th = p["tab"]
    frame = box(ox0 - fm, ox1 + fm, cy0 - ftk, cy0, floor - fm, ceil + fm)
    for dz in p["latch_dz"]:
        zl = ozc + dz
        frame += box(ox1 + fm - 1, ox1 + fm + tw, cy0 - ftk, cy0, zl - th / 2, zl + th / 2)
        frame += box(mx(ox1 + fm + tw), mx(ox1 + fm - 1), cy0 - ftk, cy0, zl - th / 2, zl + th / 2)
    frame -= box(ox0, ox1, cy0 - ftk - 1, cy0 + 1, floor, ceil)
    add("frame", "Front frame", frame, 1, "make")

    # 1 drip tray under the inner sink, welded to the right wall; open toward the wall
    dw, dl, dh = pin
    drip = box(xin - dw, xin, -dl / 2, dl / 2, drip_z0, drip_z0 + dh)
    drip -= box(xin - dw + 3, xin + 1, -dl / 2 + 3, dl / 2 - 3, drip_z0 + 3, drip_z0 + dh + 1)
    add("drip", "Drip tray", drip, 1, "make")

    # 6 mixing fan on four spacers welded to the back wall
    f, ft_, fg = p["mix_fan"], p["mix_fan_t"], p["fan_gap"]
    fx0, fz1 = cx0 + t + 20, cz1 - t - 10
    fy1 = cy1 - t - fg
    add("mixfan", "Mixing fan", box(fx0, fx0 + f, fy1 - ft_, fy1, fz1 - f, fz1), 6, "buy")
    sp = []
    for xc in (fx0 + 7.5, fx0 + f - 7.5):
        for zc in (fz1 - 7.5, fz1 - f + 7.5):
            sp.append(box(xc - 6, xc + 6, fy1, cy1 - t, zc - 6, zc + 6))
    add("spacers", "Fan spacers (4)", fuse(sp), 1, "make")

    # 2 door, gasket, latches and keepers
    ov = p["door_ov"]
    dy0, dy1 = D["door_y0"], D["door_y1"]
    door = box(ox0 - ov, ox1 + ov, dy0, dy1, floor - ov, ceil + ov)
    # printed border on the door's front face: an opaque band round the edge, cut round the four keepers.
    # The print is drawn 0.3 mm into the door's front face so the door, keepers and panel still bear on it.
    bwd = p["border"]
    border = (box(ox0 - ov, ox1 + ov, dy0, dy0 + 0.3, floor - ov, ceil + ov)
              - box(ox0 - ov + bwd, ox1 + ov - bwd, dy0 - 1, dy0 + 1, floor - ov + bwd, ceil + ov - bwd))
    for dz in p["latch_dz"]:
        zl = ozc + dz
        for x0_, x1_ in ((ox1 + ov - 8, ox1 + ov - 1), (mx(ox1 + ov - 1), mx(ox1 + ov - 8))):
            border -= box(x0_, x1_, dy0 - 1, dy0 + 1, zl - 8, zl + 8)
    add("door", "Door", door - border, 2, "make")
    add("border", "Door border (printed)", border, 2, "buy")
    gt, g0, g1 = p["gasket"]
    gas = (box(ox0 - g1, ox1 + g1, dy1, cy0 - ftk, floor - g1, ceil + g1)
           - box(ox0 - g0, ox1 + g0, dy1 - 1, cy0 - ftk + 1, floor - g0, ceil + g0))
    add("gasket", "Door gasket", gas, 2, "buy")
    lx, ly, lz = p["latch"]
    keep, lat = [], []
    for dz in p["latch_dz"]:
        zl = ozc + dz
        for m in (False, True):
            X = (lambda a, b_: (mx(b_), mx(a))) if m else (lambda a, b_: (a, b_))
            keep.append(box(*X(ox1 + ov - 8, ox1 + ov - 1), dy0 - 3, dy0, zl - 8, zl + 8))
            lat.append(box(*X(ox1 + fm + 4, ox1 + fm + 4 + lx), cy0 - ftk - ly, cy0 - ftk, zl - lz / 2, zl + lz / 2))
            lat.append(box(*X(ox1 + ov - 7, ox1 + fm + 18), dy0 - 6, dy0 - 3, zl - 5, zl + 5))
    add("keepers", "Latch keepers (4)", fuse(keep), 2, "buy")
    add("latches", "Draw latches (4)", fuse(lat), 2, "buy")

    # 3 insulation jacket: bottom, top, back, left, right, with clearance holes
    jk = {
        "bottom": box(cx0 - ins, cx1 + ins, cy0, cy1 + ins, bt, cz0),
        "top": box(cx0 - ins, cx1 + ins, cy0, cy1 + ins, cz1, cz1 + ins),
        "back": box(cx0, cx1, cy1, cy1 + ins, cz0, cz1),
        "left": box(cx0 - ins, cx0, cy0, cy1 + ins, cz0, cz1),
        "right": box(cx1, cx1 + ins, cy0, cy1 + ins, cz0, cz1),
    }
    r = jk["right"] - box(cx1 - 1, cx1 + ins + 1, -oy / 2, oy / 2, pz - oz / 2, pz + oz / 2)
    for y, z in ports:
        r -= xcyl(cx1 - 1, cx1 + ins + 1, y, z, p["port_d"] / 2 + 4)
    r -= xcyl(cx1 - 1, cx1 + ins + 1, drain[0], drain[1], 6.0)
    for y, z in clamps:
        r -= xcyl(cx1 - 1, cx1 + ins + 1, y, z, 4.0)
    jk["right"] = r
    jk["left"] = jk["left"] - xcyl(cx0 - ins - 1, cx0 + 1, 0, az, p["aero_d"] / 2 + 6)
    bk = jk["back"]
    for x in hxs:
        bk -= ycyl(cy1 - 1, cy1 + ins + 1, x, hz, p["port_d"] / 2 + 4)
    for x in p["glands"]:
        bk -= ycyl(cy1 - 1, cy1 + ins + 1, x, gz, p["gland_d"] / 2 + 6)
    jk["back"] = bk
    for k, s in jk.items():
        add(f"jacket_{k}", f"Jacket {k} panel", s, 3, "make")
    if door_panel:   # removable XPS door panel on the door, held by four hook-and-loop pads
        pm = p["panel_m"]
        add("door_panel", "Door panel", box(ox0 - pm, ox1 + pm, dy0 - ins, dy0, floor - ov, ceil + ov), 3, "make")
        # printed pull handle glued to the panel's front face, centred near its top edge
        hw, hh, htk, gl_, gs, hr = p["handle"]
        hy, hzc = dy0 - ins, ceil - 15.0
        hnd = box(oxc - hw / 2, oxc + hw / 2, hy - htk, hy, hzc - hh / 2, hzc + hh / 2)
        for sx in (-1, 1):                                   # two posts from the flange to the grip
            xp = oxc + sx * (gl_ / 2 - gs / 2)
            hnd += box(xp - gs / 2, xp + gs / 2, hy - hr + gs, hy - htk, hzc - gs / 2, hzc + gs / 2)
        hnd += box(oxc - gl_ / 2, oxc + gl_ / 2, hy - hr, hy - hr + gs, hzc - gs / 2, hzc + gs / 2)
        add("handle", "Door panel pull handle", hnd, 3, "make")

    # 20 front badge on the top jacket panel: lip down to the front frame's top edge; name plate and status light
    bw_, bd_, bh_ = p["badge"]
    jt = cz1 + ins                                   # top of the jacket
    fy = cy0 - p["frame_t"]                          # front face of the front frame
    fz1 = ceil + p["frame_m"]                        # top edge of the front frame
    bx0, bx1 = oxc - bw_ / 2, oxc + bw_ / 2
    badge = box(bx0, bx1, fy, fy + bd_, jt, jt + bh_) + box(bx0, bx1, fy, cy0, fz1, jt)
    lr, br_, bdp = p["led"]
    lx, lz = bx1 - p["led_in"], (fz1 + jt + bh_) / 2
    badge -= ycyl(fy - 1, fy + bd_ + 1, lx, lz, lr + 0.1)            # hole for the light and its lead
    add("badge", "Front badge", badge, 20, "make")
    add("status_light", "Status light", ycyl(fy - bdp, fy, lx, lz, br_) + ycyl(fy, fy + 10, lx, lz, lr), 20, "buy")
    pw, ph = p["plate"]
    add("name_plate", "Name plate", box(bx0 + 10, bx0 + 10 + pw, fy - 0.5, fy, lz - ph / 2, lz + ph / 2), 20, "buy")
    # status light lead: out of the badge, along the jacket top, down the back panel, onto the controller
    w2 = p["lead"] / 2
    yb, xl_ = cy1 + ins, p["lead_x"]
    ctop = bt + p["ctrl"][2]
    lead = (ycyl(fy + 10, fy + bd_ + 4, lx, lz, w2)
            + box(lx - w2, lx + w2, fy + bd_ + 4 - 2 * w2, fy + bd_ + 4, jt, lz)
            + box(lx - w2, lx + w2, fy + bd_ + 4 - 2 * w2, yb - 2 * w2, jt, jt + 2 * w2)
            + box(lx - w2, xl_ + w2, yb - 2 * w2, yb, jt, jt + 2 * w2)
            + box(xl_ - w2, xl_ + w2, yb, yb + 2 * w2, ctop, jt + 2 * w2)
            + box(xl_ - w2, xl_ + w2, yb, cy1 + ins + 5 + 3 + 10, ctop, ctop + 2 * w2))
    add("light_lead", "Status light lead", lead, 20, "buy")

    # 5 Peltier assembly: inner sink (base and fins), module block, outer sink, fan, clamp screws
    sxi, syi, szi = p["sink_in"]
    sxo, syo, szo = p["sink_out"]
    fx, fy, fz = p["fan_out"]
    sb, sbo = p["sink_base"], p["sink_base_out"]
    xo = cx1 + ins
    holes_in = fuse(xcyl(xin - sb - 1, xin + 1, y, z, 2.0) for y, z in clamps)
    holes_out = fuse(xcyl(xo - 1, xo + sbo + 1, y, z, 2.0) for y, z in clamps)
    add("sink_in", "Inner sink", box(xin - sb, xin, -syi / 2, syi / 2, pz - szi / 2, pz + szi / 2) - holes_in
        + box(xin - sxi, xin - sb, -50, 50, pz - 50, pz + 50), 5, "buy")
    add("pelt_block", "Peltier module and spacer block", box(xin, xo, -40, 40, pz - 40, pz + 40), 5, "buy")
    add("sink_out", "Outer sink", box(xo, xo + sbo, -syi / 2, syi / 2, pz - szi / 2, pz + szi / 2) - holes_out
        + box(xo + sbo, xo + sxo, -50, 50, pz - 50, pz + 50), 5, "buy")
    add("fan_out", "Outer fan", box(xo + sxo, xo + sxo + fx, -fy / 2, fy / 2, pz - fz / 2, pz + fz / 2), 5, "buy")
    cl = []
    for y, z in clamps:
        cl += [xcyl(xin - sb, xo + sbo + 4, y, z, 2.0), xcyl(xin - sb - 3, xin - sb, y, z, 3.5),
               xcyl(xo + sbo, xo + sbo + 4, y, z, 3.5), xcyl(cx1, xo, y, z, 4.0)]
    add("clamp", "Clamp screws and sleeves (4)", fuse(cl), 5, "buy")

    # 7 sensor tray: perforated plate, four legs and a cable rail
    tz0 = floor + p["tray_z"]
    tx0, ty0 = D["tray_x0"], D["tray_y0"]
    TL, TD = D["tray_len"], D["tray_dep"]
    plate = box(tx0, tx0 + TL, ty0, ty0 + TD, tz0, tz0 + p["tray_t"])
    hd, hp = p["tray_hole"]
    nxh, nyh = int(TL // hp), int(TD // hp)
    hx0 = tx0 + (TL - (nxh - 1) * hp) / 2
    hy0 = ty0 + (TD - (nyh - 1) * hp) / 2
    plate -= fuse(zcyl(hx0 + i * hp, hy0 + j * hp, tz0 - 1, hd / 2, p["tray_t"] + 2)
                  for i in range(nxh) for j in range(nyh)
                  if not (i in (0, nxh - 1) and j in (0, nyh - 1)))   # no hole over a leg
    tray = plate
    for x in (tx0 + 10, tx0 + TL - 20):
        for y in (ty0 + 10, ty0 + TD - 20):
            tray += box(x, x + 10, y, y + 10, floor, tz0)
    tray += box(tx0, tx0 + TL, ty0 + TD, ty0 + TD + 12, tz0, tz0 + 25)
    add("tray", "Sensor tray", tray, 7, "make")

    # sensors under test at the largest head size (R10): example payload, not in the BOM
    bw, bd, bh = p["bay"]
    g = p["bay_gap"]
    duts = []
    for i in range(p["bays"][0]):
        for j in range(p["bays"][1]):
            x = tx0 + g + i * (bw + g)
            y = ty0 + g + j * (bd + g)
            duts.append(box(x + 5, x + bw - 5, y + 5, y + bd - 5, D["tray_top"], D["tray_top"] + bh - 5))
    add("duts", "Sensors under test (example)", fuse(duts), None, "payload")

    # 8 reference cluster on a printed mast standing on the floor against the tray rail
    rx, ry, rz = p["ref"]
    ms = p["mast"]
    rcx = tx0 + TL / 2
    my0 = ty0 + TD + 12
    rz0 = D["tray_top"] + p["ref_z"]
    mast = box(rcx - ms / 2, rcx + ms / 2, my0, my0 + ms, floor, rz0)
    for zh in (56.0, 69.0):                       # two screw holes into the tray rail
        mast -= ycyl(my0 - 1, my0 + ms + 1, rcx, floor + zh, 2.25)
    mast -= zcyl(rcx, my0 + ms / 2, rz0 - 15, 2.25, 16)              # screw hole for the cluster carrier
    mast -= box(rcx + ms / 2 - 3, rcx + ms / 2 + 1, my0 + 7, my0 + 13, floor - 1, rz0 + 1)  # lead channel
    add("mast", "Reference mast", mast, 8, "make")
    rcy = my0 + ms / 2
    add("ref", "Reference cluster", box(rcx - rx / 2, rcx + rx / 2, rcy - ry / 2, rcy + ry / 2, rz0, rz0 + rz), 8, "buy")

    # bulkhead fittings through the right wall (inlets, suction, drain) and the back wall (HEPA)
    fit = []
    for y, z in ports:
        fit += [xcyl(xin - 6, xout, y, z, p["port_d"] / 2), xcyl(xin - 6, xin, y, z, 9.0)]
    add("fit_cond", "Conditioning bulkheads (3)", fuse(fit), 19, "buy")
    add("fit_drain", "Drain bulkhead", xcyl(xin - 6, xout, drain[0], drain[1], 3.0)
        + xcyl(xin - 6, xin, drain[0], drain[1], 4.0), 19, "buy")
    hy0_ = cy1 + ins + 5
    fh = []
    for x in hxs:
        fh += [ycyl(cy1 - t - 3, hy0_, x, hz, p["port_d"] / 2), ycyl(cy1 - t - 3, cy1 - t, x, hz, 9.0)]
    add("fit_hepa", "HEPA bulkheads (2)", fuse(fh), 19, "buy")
    gl = []
    for x in p["glands"]:
        gl += [ycyl(cy1 - t, cy1, x, gz, p["gland_d"] / 2), ycyl(cy1 - t - 4, cy1 - t, x, gz, 13.0),
               ycyl(cy1, cy1 + 20, x, gz, 12.0)]
    add("glands", "Cable glands (2)", fuse(gl), 19, "buy")

    # 9 bubbler with foam sleeve and heated outlet line to the front inlet
    br, bh2 = p["bubbler"]
    bxp, byp = p["bubbler_xy"]
    sl = p["sleeve"]
    zp = floor + p["port_z"]
    yA, yB = p["port_ys"]
    add("bubbler", "Bubbler", zcyl(bxp, byp, bt, br + sl, bh2) + zcyl(bxp, byp, bt + bh2, 12, 15)
        + box(xout, bxp, yA - 6, yA + 6, zp - 6, zp + 6), 9, "buy")
    # 10 dryer column in a printed socket, line to the back inlet
    dr, dh = p["dryer"]
    dxp, dyp = p["dryer_xy"]
    sock = zcyl(dxp, dyp, bt, dr + 4, 25) - zcyl(dxp, dyp, bt + 4, dr + 0.5, 30)
    sock -= fuse(zcyl(dxp + 15 * math.cos(math.radians(a)), dyp + 15 * math.sin(math.radians(a)), bt - 1, 2.0, 7)
                 for a in (90, 210, 330))                            # three screw holes in the floor
    add("dryer_socket", "Dryer socket", sock, 10, "make")
    add("dryer", "Dryer column", zcyl(dxp, dyp, bt + 4, dr, dh) + zcyl(dxp, dyp, bt + 4 + dh, 10, 12)
        + box(xout, dxp - 15, yB - 5, yB + 5, zp - 5, zp + 5) + box(dxp - 25, dxp - 15, yB - 5, dyp - 10, zp - 5, zp + 5), 10, "buy")
    # 9, 10 two diaphragm pumps on the base, fed from the suction port
    px, pyd, ph = p["pump"]
    pumps = [box(x - px / 2, x + px / 2, p["pump_y"] - pyd / 2, p["pump_y"] + pyd / 2, bt, bt + ph) for x in p["pump_xs"]]
    ys_, zs_ = ports[2]
    xa = p["pump_xs"][0]
    tube = box(xout, xa + 4, ys_ - 4, ys_ + 4, zs_ - 4, zs_ + 4) + box(xa - 4, xa + 4, ys_ - 4, ys_ + 4, bt + ph, zs_ + 4)
    add("pumps", "Air pumps (2) and suction line", fuse(pumps) + tube, 9, "buy")
    # drain line and catch bottle
    bxb, byb = p["bottle_xy"]
    brr, bhh = p["bottle"]
    dl_ = (box(xout, bxb + 4, drain[0] - 3, drain[0] + 3, drain[1] - 3, drain[1] + 3)
           + box(bxb - 4, bxb + 4, drain[0] - 3, drain[0] + 3, bt + bhh, drain[1] + 3))
    add("drain", "Drain line and bottle", dl_ + zcyl(bxb, byb, bt, brr, bhh), 19, "buy")

    # 11 HEPA scrubber unit behind the jacket
    hx, hy, hz_ = p["hepa"]
    add("hepa", "HEPA unit", box(p["hepa_x"] - hx / 2, p["hepa_x"] + hx / 2, hy0_, hy0_ + hy, bt, bt + hz_), 11, "buy")

    # 12 aerosol port: 16 mm bulkhead stub through the left wall, inside nut, ball valve outside
    st = p["aero_stub"] / 2
    add("port", "Aerosol port and valve", xcyl(cx0 - ins - 30, cx0 + t + 3, 0, az, st)
        + xcyl(cx0 + t, cx0 + t + 3, 0, az, 12.0)
        + box(cx0 - ins - 46, cx0 - ins - 30, -14, 14, az - 14, az + 14), 12, "buy")

    # 13 controller and 14 power supply behind the jacket
    y0 = cy1 + ins + 5
    cx, cy, cz = p["ctrl"]
    add("ctrl", "Controller", box(p["ctrl_x"] - cx / 2, p["ctrl_x"] + cx / 2, y0 + 3, y0 + 3 + cy, bt, bt + cz), 13, "buy")
    px_, py_, pz_ = p["psu"]
    add("psu", "Power supply", box(p["psu_x"] - px_ / 2, p["psu_x"] + px_ / 2, y0 + 3, y0 + 3 + py_, bt, bt + pz_), 14, "buy")

    # 15 salt fixed-point jars in a printed rack
    jr, jh = p["jar"]
    jy = p["jar_y"]
    xs = p["jar_xs"]
    rack = box(xs[0] - jr - 4, xs[-1] + jr + 4, jy - jr - 6, jy + jr + 6, bt, bt + 15)
    rack -= fuse(zcyl(x, jy, bt - 1, jr + 0.5, 20) for x in xs)
    rack -= fuse(zcyl(x, jy, bt - 1, 2.0, 20) for x in (xs[0] - jr - 4 + 8, xs[-1] + jr + 4 - 8))  # screw holes
    add("jar_rack", "Jar rack", rack, 15, "make")
    add("jars", "Salt jars (4)", fuse(zcyl(x, jy, bt, jr, jh) for x in xs), 15, "buy")
    return C


def large_heads(p=PARAMS):
    """R10 large item case (CLR-DEC-001, 2026-10-02): envelopes on the tray, for the checks only.

    A head up to 192 x 70 mm in plan takes two bays side by side; a head up to 192 x 152 mm takes a
    2 x 2 block of four bays. Each is drawn at the full block size and at the clear height above the
    tray less `large_gap`, in every position the six bays allow: {name: solid}.
    """
    D = derived(p)
    bw, bd, _ = p["bay"]
    g = p["bay_gap"]
    tx0, ty0, z0 = D["tray_x0"], D["tray_y0"], D["tray_top"]
    z1 = z0 + D["head_clear"] - p["large_gap"]
    (pw, pd), (kw, kd) = D["pair"], D["block"]
    out = {}
    for i in range(p["bays"][0] - 1):
        x = tx0 + g + i * (bw + g)
        out[f"block, bays {i + 1} and {i + 2}, both rows"] = box(x, x + kw, ty0 + g, ty0 + g + kd, z0, z1)
        for j in range(p["bays"][1]):
            y = ty0 + g + j * (bd + g)
            out[f"pair, bays {i + 1} and {i + 2}, row {j + 1}"] = box(x, x + pw, y, y + pd, z0, z1)
    return out


# BOM groups as the calculation note, the general arrangement and the concept media use them
GROUP_KEYS = {
    "base": ("base",),
    "shell": ("shell", "frame", "drip", "spacers"),
    "door": ("door", "border", "gasket", "keepers", "latches"),
    "jacket": ("jacket_bottom", "jacket_top", "jacket_back", "jacket_left", "jacket_right"),
    "door_panel": ("door_panel", "handle"),
    "badge": ("badge", "status_light", "name_plate", "light_lead"),
    "peltier": ("sink_in", "pelt_block", "sink_out", "fan_out", "clamp"),
    "mixfan": ("mixfan",),
    "tray": ("tray",),
    "duts": ("duts",),
    "ref": ("mast", "ref"),
    "bubbler": ("bubbler",),
    "dryer": ("dryer", "dryer_socket"),
    "pumps": ("pumps",),
    "hepa": ("hepa",),
    "port": ("port",),
    "fittings": ("fit_cond", "fit_drain", "fit_hepa", "glands", "drain"),
    "ctrl": ("ctrl",),
    "psu": ("psu",),
    "jars": ("jars", "jar_rack"),
}


def build_parts(p=PARAMS, door_panel=True):
    """Return {group: solid} for the BOM groups, plus example sensors under test ('duts')."""
    C = build_components(p, door_panel)
    return {g: fuse(C[k].shape for k in ks if k in C) for g, ks in GROUP_KEYS.items() if any(k in C for k in ks)}


GROUPS = {
    "chamber": ("shell", "door", "jacket", "door_panel", "badge"),
    "conditioning": ("peltier", "bubbler", "dryer", "pumps", "hepa", "port", "fittings"),
}


def assembly(p=PARAMS, door_panel=True):
    from build123d import Compound
    return Compound(children=list(build_parts(p, door_panel).values()))


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        i = a & b_
        return i.volume if i is not None else 0.0
    except Exception:
        return 0.0


def _gap(a, b_):
    return a.distance_to(b_)


def checks(p=PARAMS):
    """Pairs that must touch or stay apart: list of (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        """expect: 'touch' (no overlap, gap 0) or a minimum clearance in mm."""
        a = S(a) if isinstance(a, str) else a
        b_ = S(b_) if isinstance(b_, str) else b_
        v = _vol(a, b_)
        gp = _gap(a, b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    jk = fuse(S(k) for k in GROUP_KEYS["jacket"])
    chk("Jacket bottom panel on the base plate", "jacket_bottom", "base", "touch")
    chk("Shell on the jacket bottom panel", "shell", "jacket_bottom", "touch")
    for k in ("top", "back", "left", "right"):
        chk(f"Jacket {k} panel against the shell", f"jacket_{k}", "shell", "touch")
    chk("Front frame welded to the shell's front edges", "frame", "shell", "touch")
    chk("Front frame against the jacket's front edges", "frame", jk, "touch")
    chk("Front frame clear of the base plate", "frame", "base", 3.0)
    chk("Drip tray welded to the right wall", "drip", "shell", "touch")
    chk("Drip tray clear of the inner sink", "drip", "sink_in", 2.0)
    chk("Fan spacers welded to the back wall", "spacers", "shell", "touch")
    chk("Mixing fan on its spacers", "mixfan", "spacers", "touch")
    chk("Mixing fan clear of the shell", "mixfan", "shell", 5.0)
    chk("Gasket on the front frame", "gasket", "frame", "touch")
    chk("Door on the gasket", "door", "gasket", "touch")
    chk("Door clear of the front frame (gasket gap)", "door", "frame", 2.0)
    chk("Latches on the frame tabs", "latches", "frame", "touch")
    chk("Latch hooks on the keepers", "latches", "keepers", "touch")
    chk("Keepers on the door", "keepers", "door", "touch")
    chk("Door panel on the door", "door_panel", "door", "touch")
    chk("Door panel clear of the latches and keepers", "door_panel", S("latches") + S("keepers"), 3.0)
    # decisions of 2026-10-02 (CLR-DEC-001): door border, pull handle, front badge, status light and lead
    chk("Door border printed on the door's front face", "border", "door", "touch")
    chk("Door border clear of the gasket (front face only)", "border", "gasket", 5.0)
    chk("Keepers on the door through the border cut-outs", "keepers", "border", "touch")
    chk("Pull handle glued to the door panel", "handle", "door_panel", "touch")
    chk("Pull handle clear of the door, latches and keepers", "handle", S("door") + S("latches") + S("keepers"), 20.0)
    chk("Pull handle clear of the front badge", "handle", S("badge") + S("status_light"), 10.0)
    chk("Front badge on the jacket top panel", "badge", "jacket_top", "touch")
    chk("Front badge lip on the front frame's top edge", "badge", "frame", "touch")
    chk("Front badge clear of the door and door panel", "badge", S("door") + S("door_panel"), 5.0)
    chk("Front badge clear of the latches", "badge", S("latches") + S("keepers"), 20.0)
    chk("Status light bezel on the badge's front face", "status_light", "badge", "touch")
    chk("Name plate on the badge's front face", "name_plate", "badge", "touch")
    chk("Name plate clear of the status light", "name_plate", "status_light", 5.0)
    chk("Status light lead from the status light", "light_lead", "status_light", "touch")
    chk("Status light lead clear of the badge (in its hole)", "light_lead", "badge", 0.5)
    chk("Status light lead along the jacket top and back", "light_lead", jk, "touch")
    chk("Status light lead onto the controller", "light_lead", "ctrl", "touch")
    chk("Status light lead clear of the glands and HEPA bulkheads", "light_lead", S("glands") + S("fit_hepa"), 10.0)
    chk("Status light lead clear of the heat pump, dryer and supply", "light_lead",
        S("sink_out") + S("fan_out") + S("clamp") + S("dryer") + S("psu"), 10.0)
    # R10 large item case: every two-bay and four-bay envelope on the tray, clear of everything around it
    D = derived(p)
    tx0, ty0 = D["tray_x0"], D["tray_y0"]
    around = S("shell") + S("mixfan") + S("ref") + S("mast") + S("sink_in") + S("drip") + S("port") + S("spacers")
    for name, head in large_heads(p).items():
        chk(f"Large head ({name}) on the tray", head, "tray", "touch")
        chk(f"Large head ({name}) clear of walls, fan, sink, references", head, around, 5.0)
        hb = head.bounding_box()
        m = min(hb.min.X - tx0, tx0 + D["tray_len"] - hb.max.X, hb.min.Y - ty0, ty0 + D["tray_dep"] - hb.max.Y)
        rows.append((f"Large head ({name}) inside the tray outline", 0.0, m, 0.0, m >= 0))
    chk("Inner sink on the right wall", "sink_in", "shell", "touch")
    chk("Module block between the sinks (inner)", "pelt_block", "sink_in", "touch")
    chk("Module block between the sinks (outer)", "pelt_block", "sink_out", "touch")
    chk("Module block clear of the shell opening", "pelt_block", "shell", 4.0)
    chk("Outer sink on the jacket right panel", "sink_out", "jacket_right", "touch")
    chk("Outer fan on the outer sink", "fan_out", "sink_out", "touch")
    chk("Clamp screws through the shell", "clamp", "shell", "touch")
    chk("Clamp sleeves through the jacket", "clamp", "jacket_right", "touch")
    chk("Clamp screws through the inner sink", "clamp", "sink_in", "touch")
    chk("Clamp screws through the outer sink", "clamp", "sink_out", "touch")
    chk("Clamp screws clear of the outer fan", "clamp", "fan_out", 1.0)
    chk("Tray legs on the chamber floor", "tray", "shell", "touch")
    chk("Tray clear of the drip tray and inner sink", "tray", S("drip") + S("sink_in"), 10.0)
    chk("Mast on the chamber floor", "mast", "shell", "touch")
    chk("Mast against the tray rail", "mast", "tray", "touch")
    chk("Reference cluster on the mast", "ref", "mast", "touch")
    chk("Reference cluster clear of the mixing fan", "ref", "mixfan", 10.0)
    chk("Sensors under test on the tray", "duts", "tray", "touch")
    chk("Sensors under test clear of the reference cluster", "duts", S("ref") + S("mast"), 5.0)
    chk("Inlet and suction bulkheads in the right wall", "fit_cond", "shell", "touch")
    chk("Inlet and suction bulkheads clear of the jacket", "fit_cond", "jacket_right", 3.0)
    chk("Drain bulkhead in the right wall", "fit_drain", "shell", "touch")
    chk("Drain bulkhead clear of the jacket", "fit_drain", "jacket_right", 2.0)
    chk("Drain bulkhead clear of the drip tray floor", "fit_drain", "drip", 0.5)
    chk("HEPA bulkheads in the back wall", "fit_hepa", "shell", "touch")
    chk("HEPA bulkheads into the HEPA unit", "fit_hepa", "hepa", "touch")
    chk("HEPA bulkheads clear of the jacket", "fit_hepa", "jacket_back", 3.0)
    chk("Cable glands in the back wall", "glands", "shell", "touch")
    chk("Cable glands clear of the jacket", "glands", "jacket_back", 3.0)
    chk("Aerosol port in the left wall", "port", "shell", "touch")
    chk("Aerosol port clear of the jacket", "port", "jacket_left", 3.0)
    chk("Aerosol port clear of the mixing fan", "port", "mixfan", 5.0)
    chk("Bubbler line on its bulkhead", "bubbler", "fit_cond", "touch")
    chk("Bubbler on the base plate", "bubbler", "base", "touch")
    chk("Bubbler clear of the jacket", "bubbler", jk, 1.0)
    chk("Bubbler clear of the front frame and latches", "bubbler", S("frame") + S("latches"), 5.0)
    chk("Dryer socket on the base plate", "dryer_socket", "base", "touch")
    chk("Dryer column in its socket", "dryer", "dryer_socket", "touch")
    chk("Dryer line on its bulkhead", "dryer", "fit_cond", "touch")
    chk("Dryer clear of the outer sink and fan", "dryer", S("sink_out") + S("fan_out"), 5.0)
    chk("Pumps on the base plate", "pumps", "base", "touch")
    chk("Suction line on its bulkhead", "pumps", "fit_cond", "touch")
    chk("Pumps clear of the bubbler", "pumps", "bubbler", 3.0)
    chk("Pumps clear of the jacket", "pumps", jk, 5.0)
    chk("Drain line on its bulkhead", "drain", "fit_drain", "touch")
    chk("Drain bottle on the base plate", "drain", "base", "touch")
    chk("Drain line clear of the outer sink and fan", "drain", S("sink_out") + S("fan_out"), 3.0)
    chk("Drain line clear of the dryer line and pumps", "drain", S("dryer") + S("pumps"), 3.0)
    chk("HEPA unit on the base plate", "hepa", "base", "touch")
    chk("HEPA unit clear of the jacket", "hepa", jk, 3.0)
    chk("Controller on the base plate", "ctrl", "base", "touch")
    chk("Power supply on the base plate", "psu", "base", "touch")
    chk("Controller and supply clear of the jacket and glands", S("ctrl") + S("psu"), jk + S("glands"), 3.0)
    chk("Jar rack on the base plate", "jar_rack", "base", "touch")
    chk("Jars on the base plate, in the rack", "jars", "base", "touch")
    chk("Jars clear of the rack walls", "jars", "jar_rack", 0.3)
    chk("Jar rack clear of the door panel", "jar_rack", "door_panel", 5.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:58s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def main():
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    sets = {"calrig-assembly": list(parts.values())}
    for name, keys in GROUPS.items():
        sets[name] = [parts[k] for k in keys if k in parts]
    for name, shapes in sets.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
    D = derived()
    print(f"inside {PARAMS['inner']} mm, {D['volume_l']:.1f} L; footprint {D['footprint'][0]:.0f} x "
          f"{D['footprint'][1]:.0f} mm, height {D['height']:.0f} mm")
    for k, s in parts.items():
        print(f"  {k:<11} volume {s.volume / 1e6:7.3f} L")
    print("exported:", ", ".join(sets))


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    main()
    print_checks()

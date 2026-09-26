"""CalRig parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    calrig-assembly.step / .stl     the whole rig on its base plate (door panel fitted)
    chamber.step / .stl             chamber shell, front door and insulation jacket
    conditioning.step / .stl        Peltier assembly, bubbler, dryer, HEPA loop and aerosol port

Axes: X across the bench (conditioning column at +X), Y front (-Y, door) to back (+Y), Z up.
Units mm. The base plate sits on the bench at z = 0 and is centered on the origin.
Main dimensions and interfaces only: chamber envelope and wall, jacket, door, Peltier opening and
sinks, sensor bays at the largest head size in CLR-REQ-001 R10, conditioning ports, aerosol port,
the parts on the base and the overall footprint. Not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (CLR-CAL-001) and drawing CLR-DWG-001 (cad/src/sheets.py).
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 4 base plate (bench footprint, R13)
    "base": (600.0, 500.0, 12.0),
    # 1 chamber: inside size (x, y, z), acrylic wall
    "inner": (400.0, 300.0, 300.0), "wall": 6.0,
    "chamber_x0": -229.0,             # outside left face of the chamber
    # 3 insulation jacket: XPS thickness on all faces except the door; removable door panel
    "ins": 25.0,
    # 2 door: acrylic thickness, latch depth
    "door_t": 6.0, "latch": (30.0, 12.0, 40.0),
    # 5 Peltier assembly on the +X wall: opening, inner sink, outer sink, outer fan
    "pelt_open": (90.0, 100.0), "pelt_z": 200.0,  # opening (y, z) and its center height above the chamber floor
    "sink_in": (30.0, 80.0, 90.0), "sink_out": (40.0, 110.0, 110.0), "fan_out": (25.0, 92.0, 92.0),
    # 6 internal mixing fan, 120 mm class (CLR-CAL-001 section E)
    "mix_fan": 120.0, "mix_fan_t": 25.0,
    # 7 sensor tray: plate height above the chamber floor, bay size (largest head, R10), grid
    "tray_z": 50.0, "tray_t": 6.0, "bay": (90.0, 70.0, 50.0), "bays": (3, 2), "bay_gap": 12.0,
    # 8 reference cluster on a mast at the back of the tray
    "ref": (80.0, 40.0, 55.0), "ref_z": 120.0,
    # 9, 10 conditioning column: bubbler jar with foam sleeve, dryer column
    "bubbler": (35.0, 150.0), "bubbler_xy": (255.0, -110.0), "sleeve": 10.0,
    "dryer": (25.0, 230.0), "dryer_xy": (270.0, 100.0),
    "port_d": 12.0, "port_ys": (-60.0, 60.0), "port_z": 40.0,   # conditioning ports on the +X wall
    # 11 HEPA scrubber loop behind the chamber
    "hepa": (140.0, 60.0, 130.0), "hepa_x": -130.0,
    # 12 aerosol port on the -X wall
    "aero_d": 20.0, "aero_z": 210.0,
    # 13, 14 controller and power supply behind the chamber
    "ctrl": (160.0, 55.0, 50.0), "ctrl_x": 205.0,
    "psu": (140.0, 55.0, 38.0), "psu_x": 30.0,
    # 15 salt fixed-point jars, front right
    "jar": (13.0, 40.0), "jar_y": -225.0, "jar_xs": (195.0, 223.0, 251.0, 279.0),
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    ix, iy, iz = p["inner"]
    t, ins = p["wall"], p["ins"]
    bx, by, bt = p["base"]
    cx0 = p["chamber_x0"]
    cx1 = cx0 + ix + 2 * t
    cy0, cy1 = -(iy / 2 + t), iy / 2 + t
    cz0 = bt + ins                         # chamber sits on the bottom jacket panel
    cz1 = cz0 + iz + 2 * t
    floor = cz0 + t                        # inside floor
    n_x, n_y = p["bays"]
    bw, bd, bh = p["bay"]
    g = p["bay_gap"]
    tray_len = n_x * bw + (n_x + 1) * g
    tray_dep = n_y * bd + (n_y + 1) * g
    # outer (air-side) parts on +X
    sink_out_x1 = cx1 + ins + p["sink_out"][0]
    fan_out_x1 = sink_out_x1 + p["fan_out"][0]
    aero_x0 = cx0 - ins - 30.0 - 16.0      # stub 30 mm plus valve 16 mm
    overall = {
        "x0": min(-bx / 2, aero_x0), "x1": max(bx / 2, fan_out_x1,
                                              p["bubbler_xy"][0] + p["bubbler"][0] + p["sleeve"],
                                              p["dryer_xy"][0] + p["dryer"][0], max(p["jar_xs"]) + p["jar"][0]),
        "y0": -by / 2, "y1": by / 2, "z1": cz1 + ins,
    }
    return {
        "cx0": cx0, "cx1": cx1, "cy0": cy0, "cy1": cy1, "cz0": cz0, "cz1": cz1, "floor": floor,
        "volume_l": ix * iy * iz / 1e6,
        "outer": (cx1 - cx0, cy1 - cy0, cz1 - cz0),
        "tray_len": tray_len, "tray_dep": tray_dep,
        "tray_top": floor + p["tray_z"] + p["tray_t"],
        "head_clear": (cz1 - t) - (floor + p["tray_z"] + p["tray_t"]),
        "door_y0": cy0 - p["door_t"],
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


def fuse(shapes):
    out = None
    for s in shapes:
        if s is not None:
            out = s if out is None else out + s
    return out


def build_parts(p=PARAMS, door_panel=True):
    """Return {key: solid} for BOM items 1 to 15, plus example sensors under test ('duts')."""
    D = derived(p)
    t, ins = p["wall"], p["ins"]
    cx0, cx1, cy0, cy1, cz0, cz1 = D["cx0"], D["cx1"], D["cy0"], D["cy1"], D["cz0"], D["cz1"]
    floor = D["floor"]
    bx, by, bt = p["base"]
    pz = floor + p["pelt_z"]
    oy, oz = p["pelt_open"]
    parts = {}

    # 4 base plate
    parts["base"] = box(-bx / 2, bx / 2, -by / 2, by / 2, 0, bt)

    # 1 chamber shell, five-sided, open at -Y for the door
    shell = box(cx0, cx1, cy0, cy1, cz0, cz1) - box(cx0 + t, cx1 - t, cy0 - 1, cy1 - t, cz0 + t, cz1 - t)
    shell -= box(cx1 - t - 1, cx1 + 1, -oy / 2, oy / 2, pz - oz / 2, pz + oz / 2)
    shell -= xcyl(cx0 - 1, cx0 + t + 1, 0, floor + p["aero_z"], p["aero_d"] / 2)
    for y in p["port_ys"]:
        shell -= xcyl(cx1 - t - 1, cx1 + 1, y, floor + p["port_z"], p["port_d"] / 2)
    parts["shell"] = shell

    # 2 front door with latches
    lw, ld, lh = p["latch"]
    zc = (cz0 + cz1) / 2
    door = box(cx0, cx1, D["door_y0"], cy0, cz0, cz1)
    door += box(cx0 + 30, cx0 + 30 + lw, D["door_y0"] - ld, D["door_y0"], zc - lh / 2, zc + lh / 2)
    door += box(cx1 - 30 - lw, cx1 - 30, D["door_y0"] - ld, D["door_y0"], zc - lh / 2, zc + lh / 2)
    parts["door"] = door

    # 3 insulation jacket: bottom, top, back, left, right (with Peltier and port openings)
    jk = (box(cx0 - ins, cx1 + ins, cy0, cy1 + ins, bt, cz0)
          + box(cx0 - ins, cx1 + ins, cy0, cy1 + ins, cz1, cz1 + ins)
          + box(cx0, cx1, cy1, cy1 + ins, cz0, cz1)
          + box(cx0 - ins, cx0, cy0, cy1 + ins, cz0, cz1)
          + box(cx1, cx1 + ins, cy0, cy1 + ins, cz0, cz1))
    jk -= box(cx1 - 1, cx1 + ins + 1, -oy / 2, oy / 2, pz - oz / 2, pz + oz / 2)
    jk -= xcyl(cx0 - ins - 1, cx0 + 1, 0, floor + p["aero_z"], p["aero_d"] / 2 + 6)
    for y in p["port_ys"]:
        jk -= xcyl(cx1 - 1, cx1 + ins + 1, y, floor + p["port_z"], p["port_d"] / 2 + 4)
    parts["jacket"] = jk
    if door_panel:   # removable XPS door panel, fitted for hot, humid and cold set points
        parts["door_panel"] = box(cx0 - ins, cx1 + ins, D["door_y0"] - ld - ins, D["door_y0"] - ld, bt, cz1 + ins)

    # 5 Peltier assembly: inner sink, module through the wall and jacket, outer sink, outer fan
    sxi, syi, szi = p["sink_in"]
    sxo, syo, szo = p["sink_out"]
    fx, fy, fz = p["fan_out"]
    parts["peltier"] = (box(cx1 - t - sxi, cx1 - t, -syi / 2, syi / 2, pz - szi / 2, pz + szi / 2)
                        + box(cx1 - t, cx1 + ins, -40, 40, pz - 40, pz + 40)
                        + box(cx1 + ins, cx1 + ins + sxo, -syo / 2, syo / 2, pz - szo / 2, pz + szo / 2)
                        + box(cx1 + ins + sxo, cx1 + ins + sxo + fx, -fy / 2, fy / 2, pz - fz / 2, pz + fz / 2))

    # 6 internal mixing fan, back top corner, blowing toward the door
    f, ft = p["mix_fan"], p["mix_fan_t"]
    parts["mixfan"] = box(cx0 + t + 20, cx0 + t + 20 + f, cy1 - t - ft - 5, cy1 - t - 5, cz1 - t - 10 - f, cz1 - t - 10)

    # 7 sensor tray: plate, four standoffs and a harness rail
    tz0 = floor + p["tray_z"]
    tx0 = cx0 + t + 10
    ty0 = cy0 + t + 10
    tray = box(tx0, tx0 + D["tray_len"], ty0, ty0 + D["tray_dep"], tz0, tz0 + p["tray_t"])
    for x in (tx0 + 10, tx0 + D["tray_len"] - 15):
        for y in (ty0 + 10, ty0 + D["tray_dep"] - 15):
            tray += box(x, x + 5, y, y + 5, floor, tz0)
    tray += box(tx0, tx0 + D["tray_len"], ty0 + D["tray_dep"], ty0 + D["tray_dep"] + 12, tz0, tz0 + 25)
    parts["tray"] = tray

    # sensors under test at the largest head size (R10): example payload, not in the BOM
    bw, bd, bh = p["bay"]
    g = p["bay_gap"]
    duts = []
    for i in range(p["bays"][0]):
        for j in range(p["bays"][1]):
            x = tx0 + g + i * (bw + g)
            y = ty0 + g + j * (bd + g)
            duts.append(box(x + 5, x + bw - 5, y + 5, y + bd - 5, D["tray_top"], D["tray_top"] + bh - 5))
    parts["duts"] = fuse(duts)

    # 8 reference cluster on a mast behind the bays, above the heads
    rx, ry, rz = p["ref"]
    rcx = tx0 + D["tray_len"] / 2
    rcy = ty0 + D["tray_dep"] + 30
    parts["ref"] = (box(rcx - 5, rcx + 5, rcy - 5, rcy + 5, D["tray_top"], D["tray_top"] + p["ref_z"])
                    + box(rcx - rx / 2, rcx + rx / 2, rcy - ry / 2, rcy + ry / 2,
                          D["tray_top"] + p["ref_z"], D["tray_top"] + p["ref_z"] + rz))

    # 9 bubbler with foam sleeve and heated outlet line to the lower conditioning port
    br, bh2 = p["bubbler"]
    bxp, byp = p["bubbler_xy"]
    sl = p["sleeve"]
    parts["bubbler"] = (zcyl(bxp, byp, bt, br + sl, bh2)
                        + zcyl(bxp, byp, bt + bh2, 12, 15)
                        + box(cx1 + ins, bxp, p["port_ys"][0] - 6, p["port_ys"][0] + 6, floor + p["port_z"] - 6, floor + p["port_z"] + 6))
    # 10 dryer column and its line to the other conditioning port
    dr, dh = p["dryer"]
    dxp, dyp = p["dryer_xy"]
    parts["dryer"] = (zcyl(dxp, dyp, bt, dr, dh) + zcyl(dxp, dyp, bt + dh, 10, 12)
                      + box(cx1 + ins, dxp, p["port_ys"][1] - 5, p["port_ys"][1] + 5, floor + p["port_z"] - 5, floor + p["port_z"] + 5))

    # 11 HEPA scrubber loop behind the jacket
    hx, hy, hz = p["hepa"]
    y0 = cy1 + ins + 5
    parts["hepa"] = box(p["hepa_x"] - hx / 2, p["hepa_x"] + hx / 2, y0, y0 + hy, bt, bt + hz)

    # 12 aerosol port: stub through the jacket and a ball valve outside it
    az = floor + p["aero_z"]
    parts["port"] = (xcyl(cx0 - ins - 30, cx0 + t, 0, az, p["aero_d"] / 2 - 2)
                     + box(cx0 - ins - 46, cx0 - ins - 30, -14, 14, az - 14, az + 14))

    # 13 controller and 14 power supply behind the jacket
    cx, cy, cz = p["ctrl"]
    parts["ctrl"] = box(p["ctrl_x"] - cx / 2, p["ctrl_x"] + cx / 2, y0 + 3, y0 + 3 + cy, bt, bt + cz)
    px_, py_, pz_ = p["psu"]
    parts["psu"] = box(p["psu_x"] - px_ / 2, p["psu_x"] + px_ / 2, y0 + 3, y0 + 3 + py_, bt, bt + pz_)

    # 15 salt fixed-point jars
    jr, jh = p["jar"]
    parts["jars"] = fuse(zcyl(x, p["jar_y"], bt, jr, jh) for x in p["jar_xs"])
    return parts


GROUPS = {
    "chamber": ("shell", "door", "jacket", "door_panel"),
    "conditioning": ("peltier", "bubbler", "dryer", "hepa", "port"),
}


def assembly(p=PARAMS, door_panel=True):
    from build123d import Compound
    return Compound(children=list(build_parts(p, door_panel).values()))


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
        export_stl(c, str(out / "stl" / f"{name}.stl"))
    D = derived()
    print(f"inside {PARAMS['inner']} mm, {D['volume_l']:.1f} L; footprint {D['footprint'][0]:.0f} x "
          f"{D['footprint'][1]:.0f} mm, height {D['height']:.0f} mm")
    for k, s in parts.items():
        print(f"  {k:<11} volume {s.volume / 1e6:7.3f} L")
    print("exported:", ", ".join(sets))


if __name__ == "__main__":
    main()

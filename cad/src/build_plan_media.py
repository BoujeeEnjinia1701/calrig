"""CalRig prototype build plan pictures (CLR-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts|diagrams ...]
                         SHEETS=110,111 python cad/src/build_plan_media.py sheets   (only those making sketches)
With no argument it draws everything. Every 3D picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CLR-DWG-101 to 112        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wall-holes.png      hole positions in the shell walls and jacket panels
    docs/05-build-plan/base-layout.png     where each part stands on the base plate
    docs/05-build-plan/air-loops.png       the three air loops and the drain (matplotlib)
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, fuse, box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
DATE2 = "2026-10-02"     # front badge, door border and pull handle (CLR-DEC-001)
REPO = "github.com/BoujeeEnjinia1701/calrig"
D = derived(P)
C = build_components(P, door_panel=True)
S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"base": "#8B6F4E", "jacket": "#E3D3A0", "shell": "#8FB8CC", "frame": "#3F7F9F", "drip": "#2563EB",
       "spacers": "#1D4ED8", "fit": "#7C3AED", "glands": "#4C1D95", "port": "#991B1B", "sink": "#9CA3AF",
       "block": "#C2410C", "fan": "#374151", "clamp": "#111827", "mixfan": "#334155", "tray": "#6B7280",
       "mast": "#0F766E", "ref": "#14B8A6", "hepa": "#94A3B8", "ctrl": "#15803D", "psu": "#1F2937",
       "pumps": "#475569", "bubbler": "#0EA5E9", "dryer": "#D4A017", "socket": "#A16207", "drain": "#6D28D9",
       "rack": "#F59E0B", "jars": "#D1D5DB", "gasket": "#111827", "door": "#93C5FD", "keepers": "#374151",
       "latches": "#4B5563", "panel": "#FCD34D", "duts": "#9CA3AF", "bolt": "#111827",
       "badge": "#0F766E", "lead": "#B91C1C", "handle": "#7C2D12", "border": "#1F2937"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def made():
    """Named build-plan components, in build order."""
    return {
        "base": part("Base plate", C["base"].shape, COL["base"]),
        "jk_bottom": part("Jacket bottom panel", C["jacket_bottom"].shape, COL["jacket"]),
        "shell": part("Chamber shell", C["shell"].shape, COL["shell"]),
        "frame": part("Front frame", C["frame"].shape, COL["frame"]),
        "drip": part("Drip tray", C["drip"].shape, COL["drip"]),
        "spacers": part("Fan spacers (4)", C["spacers"].shape, COL["spacers"]),
        "fittings": part("Bulkheads and cable glands", S("fit_cond", "fit_drain", "fit_hepa", "glands"), COL["fit"]),
        "port": part("Aerosol port and valve", C["port"].shape, COL["port"]),
        "jk_rest": part("Jacket back, side and top panels", S("jacket_back", "jacket_left", "jacket_right", "jacket_top"), COL["jacket"]),
        "peltier": part("Peltier assembly", S("sink_in", "pelt_block", "sink_out", "fan_out", "clamp"), COL["block"]),
        "mixfan": part("Mixing fan", C["mixfan"].shape, COL["mixfan"]),
        "tray": part("Sensor tray", C["tray"].shape, COL["tray"]),
        "mast": part("Reference mast and cluster", S("mast", "ref"), COL["mast"]),
        "hepa": part("HEPA unit", C["hepa"].shape, COL["hepa"]),
        "elec": part("Controller and power supply", S("ctrl", "psu"), COL["ctrl"]),
        "pumps": part("Air pumps (2) and suction line", C["pumps"].shape, COL["pumps"]),
        "bubbler": part("Bubbler", C["bubbler"].shape, COL["bubbler"]),
        "dryer": part("Dryer socket and column", S("dryer_socket", "dryer"), COL["dryer"]),
        "drain": part("Drain line and bottle", C["drain"].shape, COL["drain"]),
        "jars": part("Jar rack and salt jars", S("jar_rack", "jars"), COL["rack"]),
        "badge": part("Front badge, name plate and status light", S("badge", "name_plate", "status_light"), COL["badge"]),
        "lead": part("Status light lead", C["light_lead"].shape, COL["lead"]),
        "gasket": part("Door gasket", C["gasket"].shape, COL["gasket"]),
        "door": part("Door with printed border and keepers", S("door", "border", "keepers"), COL["door"]),
        "latches": part("Draw latches (4)", C["latches"].shape, COL["latches"]),
        "panel": part("Door panel with pull handle", S("door_panel", "handle"), COL["panel"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"base": (0, 0, -330), "jk_bottom": (0, 0, -170), "shell": (0, 0, 0), "frame": (0, -200, 0),
           "drip": (60, -60, 250), "spacers": (-420, 0, 420), "fittings": (330, 330, 60), "port": (-380, 0, 0),
           "jk_rest": (0, 0, 470), "peltier": (360, 0, 160), "mixfan": (-420, 0, 260), "tray": (60, -280, -60),
           "mast": (220, -240, 300), "hepa": (300, 380, 480), "elec": (60, 380, -80), "pumps": (420, -60, -60),
           "bubbler": (330, -180, -40), "dryer": (470, 120, -40), "drain": (520, -10, 40), "jars": (220, -330, -150),
           "badge": (-60, -260, 700), "lead": (300, 120, 620),
           "gasket": (-160, -300, 300), "door": (-300, -450, 120), "latches": (-440, -540, 180), "panel": (-560, -640, -200)}
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CalRig prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above",
                       elev=20, azim=-60, size=(12, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    import os
    import build123d as b
    M = made()
    base = dict(project="CalRig", date=DATE)
    want = {w.strip() for w in os.environ.get("SHEETS", "").split(",") if w.strip()}
    out = []

    def sheet(*a, **kw):
        """Draw a making sketch only when it is wanted (all of them when SHEETS is not set)."""
        if want and kw["dwg_no"].split("-")[-1] not in want:
            return None
        if kw.get("rev", "P1") != "P1":     # revised sheets carry the date of their revision
            kw["date"] = kw["revisions"][-1][2]
        return bv.component_sheet(*a, **kw)
    shell_low = part("Chamber floor and lower walls", win(C["shell"].shape, -240, 200, -170, 170, 30, 130), COL["shell"])
    lift = lambda sh: b.Pos(0, 0, -sh.bounding_box().min.Z) * sh  # noqa: E731

    out.append(sheet(Part("Base plate", C["base"].shape, COL["base"]),
        [M["jk_bottom"], M["hepa"], M["elec"], M["bubbler"], M["dryer"], M["jars"], M["pumps"], M["drain"]],
        dwg_no="CLR-DWG-101", title="CalRig base plate: making sketch", material="Birch plywood 9 mm, sealed",
        notes=["Cut 600 x 500 mm from 9 mm birch plywood; sand the edges.",
               "Seal both faces and the edges with two coats of varnish:",
               "  the rig holds water, and bare plywood swells.",
               "Mark the outline of every part from the base layout picture:",
               "  measured from the left and front edges of the plate.",
               "Drill 3 mm pilot holes for the HEPA unit, controller,",
               "  dryer socket, jar rack and pump feet.",
               "Stick six rubber feet underneath: four at the corners,",
               "  40 mm in, and two at mid-length of the long edges.",
               "Fit: the jacket bottom panel sits on it, flush with the left",
               "  edge 46 mm in, glued with foam-safe adhesive.",
               "Check: the plate lies flat on the bench without rocking."],
        inset_view=(30, -60), **base))

    out.append(sheet(Part("Insulation jacket", S("jacket_bottom", "jacket_top", "jacket_back", "jacket_left", "jacket_right"), COL["jacket"]),
        [M["base"], M["shell"], M["frame"]],
        dwg_no="CLR-DWG-102", title="CalRig insulation jacket (five panels): making sketch",
        material="Extruded polystyrene (XPS) board 25 mm",
        notes=["Cut five panels from 25 mm XPS with a fine saw or hot wire:",
               "  bottom and top 462 x 337; back 412 x 312;",
               "  left and right 337 x 312 (337 front to back).",
               "Right panel: Peltier cut-out 90 wide x 100 tall; three 20 mm",
               "  port holes, a 12 mm drain hole and four 8 mm sleeve holes,",
               "  all lined up with the shell holes (wall holes picture).",
               "Left panel: 32 mm hole for the aerosol port.",
               "Back panel: two 20 mm HEPA holes and two 32 mm gland holes.",
               "Fit: each panel lies flat on the shell, glued with foam-safe",
               "  adhesive (never solvent cement, which melts XPS); tape",
               "  every seam with foil tape. Front edges flush with the shell.",
               "Check: no gap wider than 1 mm at any seam."],
        inset_view=(25, -55), **base))

    out.append(sheet(Part("Chamber shell", C["shell"].shape, COL["shell"]),
        [M["jk_bottom"], M["base"], M["frame"]],
        dwg_no="CLR-DWG-103", title="CalRig chamber shell: making sketch", material="Cast acrylic sheet 6 mm",
        notes=["Laser cut five panels from 6 mm cast acrylic: top and bottom",
               "  412 x 312; left and right 312 deep x 300 tall; back 400 x 300.",
               "Cut every hole with the panels (wall holes picture): right",
               "  wall Peltier opening 90 x 100, three 12 mm ports, 6 mm drain,",
               "  four 4 mm clamp holes; back wall two 12 mm HEPA holes, two",
               "  20 mm gland holes; left wall a 16 mm aerosol hole.",
               "Solvent weld: sides and back stand between top and bottom;",
               "  the front stays open. Clamp square; leave 24 h.",
               "Weld the four fan spacers to the back wall inside, the drip",
               "  tray to the right wall, and the front frame to the front edges.",
               "Inside 400 x 300 x 300 (36 L); outside 412 x 312 x 312.",
               "Check: fill 10 mm of water inside for an hour: no leaks."],
        inset_view=(25, -60), **base))

    out.append(sheet(Part("Front frame", C["frame"].shape, COL["frame"]), [M["shell"], M["jk_bottom"], M["jk_rest"], M["latches"]],
        dwg_no="CLR-DWG-104", title="CalRig front frame: making sketch", material="Cast acrylic sheet 6 mm",
        notes=["Laser cut from 6 mm acrylic: 450 x 350 outside with a",
               "  400 x 300 window in the middle (the chamber opening).",
               "Four latch tabs 41 wide x 40 tall stand out from the sides,",
               "  centred 95 above and 95 below the window's centre line.",
               "Mark each latch's screw holes through the latch; drill 3 mm.",
               "Fit: solvent weld the frame to the shell's front edges, window",
               "  lined up with the inside of the shell all round. The frame",
               "  overlaps the jacket's front edges by 19 mm and stands 6 mm",
               "  clear of the base plate.",
               "The door gasket sits on the frame's front face, 4 to 12 mm",
               "  outside the window.",
               "Check: the frame is flat; a straight edge shows no gap over 0.5 mm."],
        inset_view=(20, -60), **base))

    out.append(sheet(Part("Drip tray", C["drip"].shape, COL["drip"]), [part("Right wall", win(C["shell"].shape, 120, 190, -110, 110, 140, 330), COL["shell"]),
                                                          part("Inner sink", C["sink_in"].shape, COL["sink"])],
        dwg_no="CLR-DWG-105", title="CalRig drip tray: making sketch", material="Cast acrylic sheet 3 mm",
        view_shape=lift(C["drip"].shape), inset_view=(20, 200),
        notes=["Cut from 3 mm acrylic: a floor 50 x 130, a long side 130 x 11",
               "  and two ends 47 x 11.",
               "Weld the sides on top of the floor's edges, leaving the fourth",
               "  long edge open: that edge welds to the chamber wall.",
               "The tray is 50 deep, 130 long and 14 tall outside.",
               "Fit: weld the open edge to the inside of the right wall,",
               "  centred under the Peltier opening, floor 127 above the inside",
               "  floor. Its top is 4 below the inner sink.",
               "The 6 mm drain hole in the wall is 8 above the tray's",
               "  underside, just clear of the tray floor.",
               "Check: water poured into the tray runs out of the drain hole."],
        **base))

    out.append(sheet(Part("Sensor tray", C["tray"].shape, COL["tray"]), [shell_low, part("Example sensors", C["duts"].shape, COL["duts"]), M["mast"]],
        dwg_no="CLR-DWG-106", title="CalRig sensor tray: making sketch", material="Cast acrylic sheet 6 mm",
        view_shape=lift(C["tray"].shape), inset_view=(30, -60),
        notes=["Laser cut a 318 x 176 plate from 6 mm acrylic with 8 mm holes",
               "  on a 24 mm grid (13 x 7, none at the four corners over the legs).",
               "Engrave six bay outlines 90 x 70, 12 apart and 12 from the edges.",
               "Cut four legs 10 x 10 x 50 and a cable rail 318 x 25 x 12.",
               "Weld a leg under each corner, 10 in from both edges, and the",
               "  rail along the back edge, standing up from the plate.",
               "Drill and tap two M4 holes in the rail's back face, on its",
               "  middle, 6 and 19 up from its lower edge, for the mast.",
               "Fit: the legs stand loose on the chamber floor, so the tray",
               "  lifts out through the door. Plate top 56 above the floor.",
               "Check: the tray stands level and does not rock."],
        **base))

    out.append(sheet(Part("Reference mast", C["mast"].shape, COL["mast"]), [M["tray"], part("Reference cluster", C["ref"].shape, COL["ref"]), shell_low],
        dwg_no="CLR-DWG-107", title="CalRig reference mast: making sketch", material="PETG, 3D printed, 40 % infill",
        view_shape=lift(C["mast"].shape), inset_view=(25, -50),
        notes=["Print a square post 20 x 20 x 176 in PETG, standing up.",
               "Two 4.5 mm holes through it, front to back, 56 and 69 up",
               "  from the foot, matching the tapped holes in the tray rail.",
               "A 4.5 mm hole down the top end, 15 deep, and a 6 mm",
               "  channel down one face for the sensor leads.",
               "Fit: the foot stands on the chamber floor, one face flat",
               "  against the back of the tray rail, held by two M4 nylon",
               "  screws. The reference cluster's carrier (80 x 40) screws",
               "  onto the top with one M4 nylon screw.",
               "The references sit 120 above the tray, clear of the fan.",
               "Check: the mast stands upright against the rail."],
        **base))

    out.append(sheet(Part("Dryer socket", C["dryer_socket"].shape, COL["socket"]), [part("Base plate (corner)", win(C["base"].shape, 150, 300, 0, 250, 0, 9), COL["base"]), part("Dryer column", C["dryer"].shape, COL["dryer"])],
        dwg_no="CLR-DWG-108", title="CalRig dryer socket: making sketch", material="PETG, 3D printed",
        view_shape=lift(C["dryer_socket"].shape), inset_view=(25, -60),
        notes=["Print a cup 58 outside diameter and 25 tall, with a 51 bore",
               "  and a 4 mm floor.",
               "Three 4 mm holes in the floor, on a 30 mm circle, for wood",
               "  screws into the base plate.",
               "Fit: screw it to the base where the base layout shows. The",
               "  50 mm dryer column drops in with 0.5 clearance and stands",
               "  on the floor; it lifts out for the gel to be dried in an oven.",
               "Check: the column stands upright and lifts out by hand."],
        **base))

    out.append(sheet(Part("Jar rack", C["jar_rack"].shape, COL["rack"]), [part("Base plate (corner)", win(C["base"].shape, 120, 300, -250, -120, 0, 9), COL["base"]), part("Salt jars", C["jars"].shape, COL["jars"])],
        dwg_no="CLR-DWG-109", title="CalRig jar rack: making sketch", material="PETG, 3D printed",
        view_shape=lift(C["jar_rack"].shape), inset_view=(30, -60),
        notes=["Print a block 118 x 38 x 15 with four 27 mm through pockets,",
               "  28 apart, centred along it.",
               "Two 4 mm screw holes, one at each end, 8 from the end.",
               "Fit: screw it to the base in front of the bubbler (base",
               "  layout picture). The four 26 mm salt jars stand in the",
               "  pockets on the plywood, with 0.5 mm clearance.",
               "Label each pocket: LiCl, MgCl2, NaCl, KCl.",
               "Check: each jar drops in and lifts out freely."],
        **base))

    rv2 = lambda d: [("P1", "Making sketch for the prototype build plan", DATE, "AC"), ("P2", d, DATE2, "AC")]  # noqa: E731
    out.append(sheet(Part("Door", S("door", "border", "keepers"), COL["door"]), [M["frame"], M["gasket"], M["latches"], M["shell"]],
        dwg_no="CLR-DWG-110", title="CalRig door: making sketch", material="Clear cast acrylic sheet 6 mm; black printed vinyl",
        view_shape=C["door"].shape, inset_view=(15, -60), rev="P2", revisions=rv2("Printed border added (CLR-DEC-001)"),
        notes=["Cut 430 x 330 from 6 mm clear cast acrylic; flame or sand",
               "  the edges smooth and leave the film on until fitted.",
               "Border: a matt black printed vinyl frame 22 wide on the",
               "  front face, flush with the door's edges, with a 7 x 16",
               "  notch at each keeper. Peel the film, then apply it wet.",
               "Four latch keepers on the front face: centred 95 above and",
               "  95 below the door's centre line, 1 mm in from each side edge.",
               "Mark the keeper holes through the keeper; drill 3 mm,",
               "  M3 screws with nuts, a nylon washer under each.",
               "Fit: the door's back face presses on the gasket on the front",
               "  frame; it overlaps the 400 x 300 opening by 15 all round.",
               "Four draw latches on the frame tabs pull it on.",
               "Check: with the latches closed the gasket is squeezed evenly;",
               "  a strip of paper is held tight all round."],
        **base))

    out.append(sheet(Part("Door panel with pull handle", S("door_panel", "handle"), COL["panel"]), [M["door"], M["frame"], M["latches"]],
        dwg_no="CLR-DWG-111", title="CalRig door panel and pull handle: making sketch",
        material="Extruded polystyrene (XPS) board 25 mm; PETG handle, 3D printed",
        inset_view=(15, -60), rev="P2", revisions=rv2("Pull handle added (CLR-DEC-001)"),
        notes=["Cut 406 x 330 from 25 mm XPS. It covers the opening with",
               "  3 to spare each side and stays inside the latches.",
               "Face the front with white self-adhesive vinyl so it lasts.",
               "Handle: print in PETG a flange 120 x 30 x 4 with two",
               "  12 x 12 posts and a 100 long, 12 x 12 grip standing 25 out.",
               "  Glue the flange to the front with foam-safe adhesive,",
               "  centred left to right, its centre 30 below the top edge.",
               "Stick four hook-and-loop pads on its back, 30 in from each",
               "  corner, and their mates on the door.",
               "Fit: presses flat on the front of the door, 4 clear of the",
               "  keepers and latch hooks. Fitted for the 40 C, 85 % point and",
               "  for cold points; off for the others.",
               "Check: it stays on with the rig running and peels off by",
               "  hand with the pull handle; the handle does not move."],
        **base))

    lift_b = S("badge", "name_plate", "status_light")
    out.append(sheet(Part("Front badge", lift_b, COL["badge"]), [M["jk_rest"], M["frame"], M["door"], M["lead"]],
        dwg_no="CLR-DWG-112", title="CalRig front badge: making sketch", material="PETG, 3D printed, 40 % infill",
        view_shape=lift(C["badge"].shape), inset_view=(25, -60), date=DATE2,
        notes=["Print a strip 200 long: a top 30 deep x 12 tall and, under",
               "  its front edge, a lip 6 deep x 6 tall (front face 18 tall).",
               "A 5.2 mm hole through it front to back, 20 from the right",
               "  end and 9 up from the bottom of the lip, for the light.",
               "Push the 5 mm panel light in from the front: its 8 mm bezel",
               "  sits on the front face. Stick the 120 x 10 name plate on",
               "  the front face, 10 from the left end, level with the light.",
               "Fit: glue the top to the front of the jacket's top panel with",
               "  foam-safe adhesive, centred on the door, the lip resting on",
               "  the front frame's top edge and its front flush with the frame.",
               "Lead: out of the back, straight back along the top panel, right",
               "  along its back edge to 23 from the right end, down the back",
               "  panel to the controller's top; clips every 100 mm.",
               "Check: the light shows when the controller switches it on."],
        project="CalRig"))
    return out


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & box(x0, x1, y0, y1, z0, z1)


def joints():
    out = []
    fl, pz = D["floor"], D["pz"]
    # 01 shell on the jacket bottom on the base, front left corner, cut open at the front
    w = (-300, -205, -175, -60, 0, 110)
    out.append(bv.joint([
        part("Base plate", win(C["base"].shape, *w), COL["base"]),
        part("Jacket bottom panel (glued to the base)", win(C["jacket_bottom"].shape, *w), COL["jacket"]),
        part("Jacket left panel", win(C["jacket_left"].shape, *w), COL["jacket"]),
        part("Chamber shell (sits on the jacket)", win(C["shell"].shape, *w), COL["shell"]),
        part("Front frame (welded to the shell)", win(C["frame"].shape, *w), COL["frame"])],
        OUT / "joint-01.png", "Joint 1: shell, jacket, frame and base (front left corner)",
        subtitle="Cut open, seen from inside the chamber toward the left wall. The shell sits on the jacket; the frame covers their front edges",
        elev=18, azim=-20, size=(8, 6)))
    # 02 bulkhead fitting through the right wall and jacket, cut through the front inlet
    yA, zA = P["port_ys"][0], fl + P["port_z"]
    w = (160, 216, yA - 22, yA, zA - 22, zA + 22)
    out.append(bv.joint([
        part("Chamber shell, right wall", win(C["shell"].shape, *w), COL["shell"]),
        part("Jacket right panel (20 mm hole)", win(C["jacket_right"].shape, *w), COL["jacket"]),
        part("Bulkhead fitting: nut inside, barb outside for the line", win(C["fit_cond"].shape, *w), COL["fit"])],
        OUT / "joint-02.png", "Joint 2: a bulkhead fitting through the right wall (cut open)",
        subtitle="Seen from behind the cut. The fitting seals on the acrylic; the jacket hole is 4 mm clear and filled with foam",
        elev=20, azim=80, size=(8, 6)))
    # 03 Peltier assembly through the wall, cut through the upper clamp screws
    w = (125, 280, -75, 75, pz - 75, pz + P["clamp"][1])
    out.append(bv.joint([
        part("Chamber shell", win(C["shell"].shape, *w), COL["shell"]),
        part("Jacket right panel", win(C["jacket_right"].shape, *w), COL["jacket"]),
        part("Inner sink (inside)", win(C["sink_in"].shape, *w), COL["sink"]),
        part("Module and spacer block", win(C["pelt_block"].shape, *w), COL["block"]),
        part("Outer sink and fan", win(C["sink_out"].shape + C["fan_out"].shape, *w), "#6B7280"),
        part("Clamp screws in rigid sleeves", win(C["clamp"].shape, *w), COL["clamp"]),
        part("Drip tray", win(C["drip"].shape, *w), COL["drip"])],
        OUT / "joint-03.png", "Joint 3: the Peltier assembly through the right wall (cut level with the upper screws)",
        subtitle="Seen from above. Both sink bases clamp the wall; sleeves stop the screws crushing the foam",
        elev=55, azim=-70, size=(8, 6)))
    # 04 mixing fan on its spacers
    w = (-235, -195.5, 95, 160, 280, 348)
    out.append(bv.joint([
        part("Chamber shell, back wall and top", win(C["shell"].shape, *w), COL["shell"]),
        part("Fan spacer, welded to the back wall", win(C["spacers"].shape, *w), COL["spacers"]),
        part("Mixing fan (M4 nylon screw into the spacer)", win(C["mixfan"].shape, *w), COL["mixfan"])],
        OUT / "joint-04.png", "Joint 4: mixing fan on its spacers (cut through the upper left spacer)",
        subtitle="Seen from the right, inside the chamber. The fan stands 15 mm off the back wall so it can draw air",
        elev=12, azim=-15, size=(8, 6)))
    # 05 tray leg, rail and mast foot
    w = (-100, 110, -10, 80, 35, 140)
    out.append(bv.joint([
        part("Chamber floor", win(C["shell"].shape, *w), COL["shell"]),
        part("Sensor tray: plate, leg and rail", win(C["tray"].shape, *w), COL["tray"]),
        part("Mast foot, two M4 nylon screws into the rail", win(C["mast"].shape, *w), COL["mast"])],
        OUT / "joint-05.png", "Joint 5: tray rail and mast foot (behind the tray)",
        subtitle="Seen from behind and to the right. Mast and legs stand on the floor; nothing is screwed into the shell",
        elev=25, azim=40, size=(8, 6)))
    # 06 drip tray and drain, cut through the drain
    dy = P["drain_y"]
    w = (110, 290, -70, dy, 0, 200)
    out.append(bv.joint([
        part("Chamber shell", win(C["shell"].shape, *w), COL["shell"]),
        part("Jacket right panel", win(C["jacket_right"].shape, *w), COL["jacket"]),
        part("Drip tray (welded to the wall)", win(C["drip"].shape, *w), COL["drip"]),
        part("Drain bulkhead", win(C["fit_drain"].shape, *w), COL["fit"]),
        part("Drain line and bottle", win(C["drain"].shape, *w), COL["drain"]),
        part("Jacket bottom panel", win(C["jacket_bottom"].shape, *w), COL["jacket"]),
        part("Base plate", win(C["base"].shape, *w), COL["base"])],
        OUT / "joint-06.png", "Joint 6: drip tray and drain (cut through the drain)",
        subtitle="Seen from behind the cut. Water from the inner sink runs to the bottle on the base",
        elev=12, azim=75, size=(8, 6)))
    # 07 HEPA bulkheads into the HEPA unit, cut level with the fittings
    hz = fl + P["hepa_pz"]
    w = (-215, -45, 120, 255, 0, hz)
    out.append(bv.joint([
        part("Chamber shell, back wall", win(C["shell"].shape, *w), COL["shell"]),
        part("Jacket back panel", win(C["jacket_back"].shape, *w), COL["jacket"]),
        part("HEPA bulkheads (2)", win(C["fit_hepa"].shape, *w), COL["fit"]),
        part("HEPA unit", win(C["hepa"].shape, *w), COL["hepa"])],
        OUT / "joint-07.png", "Joint 7: HEPA bulkheads through the back wall (cut level with them)",
        subtitle="Seen from above, from inside the chamber. Each fitting runs from its nut inside to the HEPA unit's port",
        elev=50, azim=-115, size=(8, 6)))
    # 08 cable glands, cut level with them
    gz = fl + P["gland_z"]
    w = (15, 125, 125, 200, 0, gz)
    out.append(bv.joint([
        part("Chamber shell, back wall", win(C["shell"].shape, *w), COL["shell"]),
        part("Jacket back panel (32 mm hole)", win(C["jacket_back"].shape, *w), COL["jacket"]),
        part("Cable glands, locknut inside", win(C["glands"].shape, *w), COL["glands"])],
        OUT / "joint-08.png", "Joint 8: cable glands through the back wall (cut level with them)",
        subtitle="Seen from above, from inside the chamber. Sensor, reference and fan leads leave the chamber here",
        elev=50, azim=-115, size=(8, 6)))
    # 09 door, gasket, frame, latch, keeper and door panel, cut level with the upper right latch
    zl = D["ozc"] + P["latch_dz"][1]
    w = (140, 250, -205, -130, zl - 25, zl)
    out.append(bv.joint([
        part("Chamber shell", win(C["shell"].shape, *w), COL["shell"]),
        part("Jacket right panel", win(C["jacket_right"].shape, *w), COL["jacket"]),
        part("Front frame and latch tab", win(C["frame"].shape, *w), COL["frame"]),
        part("Gasket", win(C["gasket"].shape, *w), COL["gasket"]),
        part("Door", win(C["door"].shape, *w), COL["door"]),
        part("Keeper", win(C["keepers"].shape, *w), COL["keepers"]),
        part("Draw latch and hook", win(C["latches"].shape, *w), COL["latches"]),
        part("Door panel", win(C["door_panel"].shape, *w), COL["panel"])],
        OUT / "joint-09.png", "Joint 9: door, gasket and latch (cut level with the upper right latch)",
        subtitle="Seen from above. The latch on the frame tab hooks the keeper and squeezes the gasket",
        elev=82, azim=-90, size=(8, 6)))
    # 10 front badge on the jacket top and the frame edge, cut through the status light
    lx = D["oxc"] + P["badge"][0] / 2 - P["led_in"]
    jt = D["cz1"] + P["ins"]
    w = (lx - 40, lx, -175, -90, jt - 45, jt + 20)
    out.append(bv.joint([
        part("Jacket top panel", win(C["jacket_top"].shape, *w), COL["jacket"]),
        part("Front frame (top edge)", win(C["frame"].shape, *w), COL["frame"]),
        part("Chamber shell", win(C["shell"].shape, *w), COL["shell"]),
        part("Front badge (glued to the jacket)", win(C["badge"].shape, *w), COL["badge"]),
        part("Status light in its bezel", win(C["status_light"].shape, *w), "#22C55E"),
        part("Status light lead", win(C["light_lead"].shape, *w), COL["lead"]),
        part("Door (top edge)", win(C["door"].shape + C["border"].shape, *w), COL["door"])],
        OUT / "joint-10.png", "Joint 10: front badge and status light (cut through the light)",
        subtitle="Seen from the right, slightly in front, on the cut. The badge sits on the jacket's top panel, its lip on the frame's top edge",
        elev=15, azim=-20, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        kw.setdefault("elev", 20)
        kw.setdefault("azim", -60)
        kw.setdefault("label_done", False)
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    shell_set = [M["shell"], M["frame"], M["drip"], M["spacers"]]
    st(1, [M["base"]], [mv(M["jk_bottom"], (0, 0, 150))], "jacket bottom panel onto the base plate",
       "Foam-safe adhesive; left edge 46 mm and front edge 94 mm in from the base edges (base layout)",
       label_done=True)
    st(2, [M["base"], M["jk_bottom"]], [mv(part("Shell with frame, drip tray and spacers", S("shell", "frame", "drip", "spacers"), COL["shell"]), (0, 0, 220))],
       "chamber shell onto the jacket", "Lower it on, frame forward; foam-safe adhesive under the shell's bottom")
    done = [M["base"], M["jk_bottom"]] + shell_set
    st(3, done, [mv(part("Inlet, suction and drain bulkheads", S("fit_cond", "fit_drain"), COL["fit"]), (110, 0, 0)),
                 mv(part("HEPA bulkheads and cable glands", S("fit_hepa", "glands"), COL["glands"]), (0, 110, 0)),
                 mv(M["port"], (-110, 0, 0))],
       "bulkheads, glands and aerosol port into the walls",
       "Each from outside with its O-ring; locknut inside, reached through the open front. Seen from behind right",
       elev=22, azim=40)
    done += [M["fittings"], M["port"]]
    st(4, done, [mv(part("Jacket back panel", C["jacket_back"].shape, COL["jacket"]), (0, 150, 0)),
                 mv(part("Jacket left panel", C["jacket_left"].shape, COL["jacket"]), (-150, 0, 0)),
                 mv(part("Jacket right panel", C["jacket_right"].shape, COL["jacket"]), (150, 0, 0)),
                 mv(part("Jacket top panel", C["jacket_top"].shape, COL["jacket"]), (0, 0, 150))],
       "jacket back, side and top panels",
       "Slide each over the fittings; foam-safe adhesive on the shell; foil tape on every seam. Seen from behind right",
       elev=25, azim=40)
    done += [M["jk_rest"]]
    st(5, done, [mv(part("Inner sink (in through the open front)", C["sink_in"].shape, "#2F4A5F"), (0, -300, 0)),
                 mv(part("Module and spacer block", C["pelt_block"].shape, COL["block"]), (90, 0, 0)),
                 mv(part("Outer sink, fan and clamp screws", S("sink_out", "fan_out", "clamp"), "#6B7280"), (170, 0, 0))],
       "Peltier assembly through the right wall",
       "Thermal paste on the module; four clamp screws through the sleeves, tightened evenly in a cross pattern",
       elev=18, azim=-40)
    done += [M["peltier"]]
    st(6, done, [mv(M["mixfan"], (0, -150, 0))], "mixing fan onto its spacers",
       "Through the open front; four M4 nylon screws into the spacers, blowing toward the door", elev=12, azim=-70)
    done += [M["mixfan"]]
    st(7, done, [mv(M["tray"], (0, -260, 0))], "sensor tray in",
       "Slide it in through the open front, 10 mm from the left wall and 16 mm behind the front opening; legs on the floor",
       elev=12, azim=-70)
    done += [M["tray"]]
    st(8, done, [mv(part("Reference mast", C["mast"].shape, COL["mast"]), (0, -150, 0)),
                 mv(part("Reference cluster", C["ref"].shape, COL["ref"]), (0, -150, 70))],
       "reference mast and cluster",
       "Mast against the back of the rail on two M4 nylon screws; cluster on its top; leads down the mast to the glands",
       elev=12, azim=-70)
    done += [M["mast"]]
    st(9, done, [mv(M["hepa"], (0, 150, 0)), mv(part("Controller", C["ctrl"].shape, COL["ctrl"]), (0, 150, 0)),
                 mv(part("Power supply (strap)", C["psu"].shape, COL["psu"]), (0, 150, 0))],
       "HEPA unit, controller and power supply onto the base",
       "HEPA unit pushed onto its two bulkheads, then screwed down; supply held by a strap. Seen from behind right",
       elev=25, azim=40)
    done += [M["hepa"], M["elec"]]
    st(10, done, [mv(M["pumps"], (140, 0, 0)), mv(M["bubbler"], (140, -60, 0)), mv(M["dryer"], (140, 60, 0)),
                  mv(M["drain"], (180, 0, 0))],
       "pumps, bubbler, dryer and drain bottle",
       "Pumps screwed down; dryer socket screwed down; lines pushed onto the bulkheads and clamped", elev=20, azim=-30)
    done += [M["pumps"], M["bubbler"], M["dryer"], M["drain"]]
    st(11, done, [mv(M["jars"], (0, 0, 120))], "jar rack and salt jars",
       "Rack screwed to the base in front of the bubbler; jars stand in it, lids on", elev=25, azim=-50)
    done += [M["jars"]]
    st(12, done, [mv(M["badge"], (0, -120, 120)), mv(M["lead"], (0, 120, 120))], "front badge and status light lead",
       "Badge glued to the top panel, lip on the frame's top edge; lead back along the top and down to the controller",
       elev=30, azim=-40)
    done += [M["badge"], M["lead"]]
    st(13, done, [mv(M["gasket"], (0, -70, 0)), mv(M["door"], (0, -160, 0)), mv(M["latches"], (0, -260, 0))],
       "gasket, door and latches",
       "Gasket on the frame face; door on the gasket; four latches screwed to the tabs, then closed", elev=15, azim=-60)
    done += [M["gasket"], M["door"], M["latches"]]
    st(14, done, [mv(M["panel"], (0, -150, 0))], "door panel (hot, humid and cold points)",
       "Hold it by its pull handle and press it onto the four hook-and-loop pads on the door, between the latches",
       elev=15, azim=-60)
    return out


# ----------------------------------------------------------------- layouts (matplotlib)
INK, MUT, AC = "#111827", "#4B5563", "#0F766E"


def _foot(fig):
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")


def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    res = []
    fl = D["floor"]
    # ---- wall holes: three shell panels as cut (inside face up), with the jacket holes noted
    fig = plt.figure(figsize=(13, 8.6), dpi=150)
    fig.text(0.03, 0.975, "Chamber walls: hole positions (as cut, seen from outside the chamber)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.945, "Sizes in mm from the model. Solid outline: hole in the 6 mm acrylic wall. Dashed: the larger clearance hole in the 25 mm jacket panel "
             "in the same place.", fontsize=8.5, color=MUT, va="top")
    pz = D["pz"] - fl
    clamps = [(sy * P["clamp"][0], pz + sz * P["clamp"][1]) for sy in (-1, 1) for sz in (-1, 1)]
    drz = D["pz"] - P["sink_in"][2] / 2 - 4 - P["drip"][2] + 8 - fl
    # right wall, seen from outside (+X): front edge on the left of the picture
    ax = fig.add_axes([0.03, 0.08, 0.40, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    W, H = 312, 300
    ax.add_patch(Rectangle((0, 0), W, H, fc="#E0F2FE", ec=INK, lw=1.2))
    yy = lambda y: y + 156  # noqa: E731  from the front edge

    def hole(ax, x, z, d, dj=None, name=None, dy=0, ha="left"):
        ax.add_patch(Circle((x, z), d / 2, fc="white", ec=INK, lw=1))
        if dj:
            ax.add_patch(Circle((x, z), dj / 2, fc="none", ec=MUT, lw=0.6, ls="--"))
        ax.plot([x - d / 2 - 3, x + d / 2 + 3], [z, z], color=MUT, lw=0.4); ax.plot([x, x], [z - d / 2 - 3, z + d / 2 + 3], color=MUT, lw=0.4)
        if name:
            ax.text(x + (d / 2 + 4 if ha == "left" else -d / 2 - 4), z + dy, name, fontsize=7, color=INK, ha=ha, va="center",
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    oy, oz = P["pelt_open"]
    ax.add_patch(Rectangle((156 - oy / 2, pz - oz / 2), oy, oz, fc="white", ec=INK, lw=1))
    ax.text(156, pz, "Peltier opening\n90 x 100,\ncentre 156, 200", ha="center", va="center", fontsize=7, color=INK)
    for y, z in clamps:
        hole(ax, yy(y), z, 4, 8)
    ax.text(yy(57) + 8, pz + 42 + 10, "clamp holes 4 (jacket 8):\n99 and 213 along; 158 and 242 up", fontsize=7, color=INK, va="bottom")
    hole(ax, yy(P["port_ys"][0]), P["port_z"], 12, 20, "front inlet (wet)\n96 along, 40 up", dy=14, ha="left")
    hole(ax, yy(P["port_ys"][1]), P["port_z"], 12, 20, "back inlet (dry)\n216 along, 40 up", dy=14, ha="left")
    hole(ax, yy(P["suction"][0]), P["suction"][1], 12, 20, "suction 120 along, 20 up", dy=-2, ha="left")
    hole(ax, yy(P["drain_y"]), drz, 6, 12, "drain 6 (jacket 12):\n161 along, 135 up", dy=0, ha="left")
    ax.text(W / 2, -12, "Right wall, 312 x 300: along from the front edge (left), up from the bottom edge", ha="center", fontsize=8, color=AC)
    ax.text(-4, H / 2, "front edge (door side)", rotation=90, ha="right", va="center", fontsize=7.5, color=MUT)
    ax.set_xlim(-20, W + 10); ax.set_ylim(-22, H + 10)
    # back wall, seen from outside (from behind): the chamber's left wall is on the right of the picture
    ax = fig.add_axes([0.46, 0.38, 0.52, 0.52]); ax.set_aspect("equal"); ax.set_axis_off()
    W, H = 400, 300
    ax.add_patch(Rectangle((0, 0), W, H, fc="#E0F2FE", ec=INK, lw=1.2))
    xb = lambda x: W - (x - D["ox0"])  # noqa: E731  from the right-hand end seen from behind = chamber's left
    hz = P["hepa_pz"]
    for x in (P["hepa_x"] + d for d in P["hepa_ports"]):
        hole(ax, xb(x), hz, 12, 20)
    ax.text(xb(-130), hz + 16, "HEPA 12 (jacket 20): 53 and 133 from the\nleft-wall end, 77 up", fontsize=7, color=INK, ha="center", va="bottom")
    for x in P["glands"]:
        hole(ax, xb(x), P["gland_z"], 20, 32)
    ax.text(xb(70), P["gland_z"] + 22, "glands 20 (jacket 32): 263 and 323\nfrom the left-wall end, 37 up", fontsize=7, color=INK, ha="center", va="bottom")
    fx0 = D["cx0"] + P["wall"] + 20
    for xc in (fx0 + 7.5, fx0 + P["mix_fan"] - 7.5):
        for zc in (D["ceil"] - 10 - 7.5 - fl, D["ceil"] - 10 - P["mix_fan"] + 7.5 - fl):
            ax.add_patch(Rectangle((xb(xc) - 6, zc - 6), 12, 12, fc="#BFDBFE", ec=INK, lw=0.8, ls=":"))
    ax.text(xb(fx0 + 60), D["ceil"] - fl - 75, "fan spacers 12 x 12 (welded inside):\n27.5 and 132.5 from the left-wall end;\n177.5 and 282.5 up",
            fontsize=7, color=INK, ha="center", va="center")
    ax.text(W / 2, -12, "Back wall, 400 x 300, seen from behind: along from the end at the chamber's left wall (right), up from the bottom", ha="center", fontsize=8, color=AC)
    ax.set_xlim(-10, W + 10); ax.set_ylim(-22, H + 10)
    # left wall, seen from outside (-X): front edge on the right of the picture
    ax = fig.add_axes([0.62, 0.07, 0.25, 0.28]); ax.set_aspect("equal"); ax.set_axis_off()
    W, H = 312, 300
    ax.add_patch(Rectangle((0, 0), W, H, fc="#E0F2FE", ec=INK, lw=1.2))
    hole(ax, W - 156, P["aero_z"], 16, 32, "aerosol 16 (jacket 32):\n156 along, 210 up", dy=-30, ha="left")
    ax.text(W / 2, -16, "Left wall, 312 x 300: along from the front edge (right)", ha="center", fontsize=7.5, color=AC)
    ax.set_xlim(-10, W + 10); ax.set_ylim(-30, H + 10)
    fig.text(0.46, 0.33, "Jacket panels: the same positions, measured\nfrom the same edges of the panel; the jacket\n"
             "panels sit on the bottom panel and wrap the\nshell, so add 6 up for the side panels, and 6\nalong and 6 up for the back panel.",
             fontsize=7.8, color=MUT, va="top")
    _foot(fig)
    fig.savefig(OUT / "wall-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "wall-holes.png")

    # ---- base layout: footprints of everything on the base, from the model
    fig = plt.figure(figsize=(11, 9), dpi=150)
    ax = fig.add_axes([0.05, 0.08, 0.66, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    bx, by, _ = P["base"]
    X = lambda x: x + bx / 2  # noqa: E731
    Y = lambda y: y + by / 2  # noqa: E731
    ax.add_patch(Rectangle((0, 0), bx, by, fc="#E7D8C3", ec=INK, lw=1.2))
    items = [("jacket_bottom", "Jacket and chamber", "#E3D3A0"), ("hepa", "HEPA unit", COL["hepa"]), ("ctrl", "Controller", "#86EFAC"),
             ("psu", "Power supply", "#CBD5E1"), ("pumps", "Pumps", "#CBD5E1"), ("jar_rack", "Jar rack", "#FCD34D")]
    for k, name, col in items:
        sh = C[k].shape if k != "pumps" else fuse([box(x - P["pump"][0] / 2, x + P["pump"][0] / 2, P["pump_y"] - P["pump"][1] / 2,
                                                         P["pump_y"] + P["pump"][1] / 2, 0, 1) for x in P["pump_xs"]])
        bb = sh.bounding_box()
        ax.add_patch(Rectangle((X(bb.min.X), Y(bb.min.Y)), bb.size.X, bb.size.Y, fc=col, ec=INK, lw=0.8))
        ax.text(X(bb.center().X), Y(bb.center().Y), f"{name}\n{X(bb.min.X):.0f}, {Y(bb.min.Y):.0f}", ha="center", va="center", fontsize=7, color=INK)
    for (x, y), r, name in ((P["bubbler_xy"], P["bubbler"][0] + P["sleeve"], "Bubbler"), (P["dryer_xy"], P["dryer"][0] + 4, "Dryer\nsocket"),
                            (P["bottle_xy"], P["bottle"][0], "Bottle")):
        ax.add_patch(Circle((X(x), Y(y)), r, fc="#BAE6FD", ec=INK, lw=0.8))
        if r < 20:
            ax.text(X(x) - r - 4, Y(y), f"{name} {X(x):.0f}, {Y(y):.0f}", ha="right", va="center", fontsize=6.5, color=INK)
        else:
            ax.text(X(x), Y(y), f"{name}\n{X(x):.0f}, {Y(y):.0f}", ha="center", va="center", fontsize=6.5, color=INK)
    fb = C["frame"].shape.bounding_box()
    ax.add_patch(Rectangle((X(fb.min.X), Y(fb.min.Y)), fb.size.X, fb.size.Y, fc="#3F7F9F", ec=INK, lw=0.6))
    ax.text(X(fb.center().X), Y(fb.max.Y) + 4, "front frame (6 above the base)", ha="center", va="bottom", fontsize=7, color=INK)
    db = C["door_panel"].shape.bounding_box()
    ax.add_patch(Rectangle((X(db.min.X), Y(db.min.Y)), db.size.X, db.size.Y, fc="none", ec=MUT, lw=0.8, ls="--"))
    ax.text(X(db.center().X), Y(db.min.Y) - 3, "door and door panel above the base", ha="center", va="top", fontsize=7, color=MUT)
    ab = C["port"].shape.bounding_box()
    ax.add_patch(Rectangle((X(ab.min.X), Y(ab.min.Y)), ab.size.X, ab.size.Y, fc="#FCA5A5", ec=INK, lw=0.6))
    ax.annotate("aerosol valve\n(on the wall, 236 up)", xy=(X(ab.center().X), Y(ab.max.Y)), xytext=(25, 380), fontsize=7, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    ax.text(bx / 2, -14, "across from the left edge, mm", ha="center", fontsize=8, color=AC)
    ax.text(-14, by / 2, "back from the front edge, mm", rotation=90, ha="center", va="center", fontsize=8, color=AC)
    ax.text(bx / 2, by + 6, "back of the rig", ha="center", fontsize=7.5, color=MUT)
    ax.text(bx / 2, -30, "front (door side)", ha="center", fontsize=7.5, color=MUT)
    ax.set_xlim(-30, bx + 10); ax.set_ylim(-40, by + 18)
    fig.text(0.03, 0.97, "Base plate: where each part stands", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.94, "Seen from above, front at the bottom. Figures under each name: its left and front edges (rectangles) or its centre (circles), "
             "in mm from the base plate's left and front edges.", fontsize=8.2, color=MUT, va="top", wrap=True)
    notes = ["Fixings (3 mm pilot holes):", "", "Jacket bottom: foam-safe adhesive", "HEPA unit: four screws through its feet",
             "Controller: four screws through its", "  case flanges", "Power supply: a hook-and-loop strap", "  through two 25 mm slots",
             "Pumps: two screws each through their", "  rubber mounts", "Dryer socket: three screws", "Jar rack: two screws",
             "Bubbler: a hook-and-loop pad under", "  the jar; held also by its line", "Bottle: a hook-and-loop pad", "",
             "Six rubber feet underneath."]
    for i, t in enumerate(notes):
        fig.text(0.74, 0.86 - i * 0.026, t, fontsize=8, color=INK, va="top", fontweight="bold" if i == 0 else "normal")
    _foot(fig)
    fig.savefig(OUT / "base-layout.png", facecolor="white"); plt.close(fig); res.append(OUT / "base-layout.png")
    return res


# ----------------------------------------------------------------- diagrams (matplotlib)
def diagrams():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    res = []

    def setup(title, sub):
        fig = plt.figure(figsize=(12, 7.2), dpi=150)
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
        ax.text(2, 70, title, fontsize=13, fontweight="bold", color=INK, va="top")
        ax.text(2, 66.6, sub, fontsize=8.5, color=MUT, va="top")
        ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
        ax.text(118, 1.5, REPO, fontsize=7, color=AC, ha="right", family="monospace")
        return fig, ax

    def blk(ax, x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        if sub:
            ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(ax, pts, color, lw=2.0, arrow=False):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)
        if arrow:
            ax.annotate("", xy=pts[-1], xytext=pts[-2], arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12), zorder=2)

    def lab(ax, x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

    # ---- air loops
    fig, ax = setup("CalRig prototype: air loops and drain",
                    "Every loop starts and ends in the chamber, so the chamber stays sealed. Tube is 6 mm bore silicone, clamped on every barb.")
    ax.add_patch(FancyBboxPatch((40, 14), 40, 44, boxstyle="round,pad=0.4", fc="#F0F9FF", ec="#0EA5E9", lw=1.6))
    ax.text(60, 56.5, "Chamber, 36 L", ha="center", va="top", fontsize=9.5, fontweight="bold", color=INK)
    ax.text(60, 53.3, "mixing fan stirs it; sensors and\nreferences sit in the air", ha="center", va="top", fontsize=7.2, color=MUT)
    BL, GN, OR, PU, RD = "#0369A1", "#A16207", "#15803D", "#6D28D9", "#991B1B"
    blk(ax, 92, 46, 22, 10, "Bubbler", "heated jar, 0.3 L water", BL)
    blk(ax, 92, 32, 22, 10, "Dryer column", "500 g silica gel", GN)
    blk(ax, 92, 16, 22, 11, "Air pumps A and B", "about 3 L/min together,\nPWM sets the wet:dry ratio", "#475569")
    blk(ax, 6, 44, 22, 11, "HEPA unit", "H13 filter and blower,\n20 L/min clean, 5 L/min decay", OR)
    blk(ax, 6, 22, 22, 11, "Smoke syringe", "60 mL, drawn from an\nincense cup outside", RD)
    blk(ax, 92, 4, 22, 8, "Drain bottle", "250 mL, emptied by hand", PU)
    wire(ax, [(80, 20), (92, 20)], "#475569", arrow=True); lab(ax, 82, 22, "suction port (right wall)", "#475569")
    wire(ax, [(103, 27.3), (103, 31.7)], "#475569", arrow=True); lab(ax, 104, 29.5, "B", "#475569")
    wire(ax, [(114.3, 21), (117, 21), (117, 51), (114.3, 51)], "#475569", arrow=True); lab(ax, 117.3, 36, "A", "#475569")
    wire(ax, [(92, 51), (80, 51)], BL, arrow=True); lab(ax, 81, 53.3, "wet inlet, trace-heated line", BL)
    wire(ax, [(92, 37), (80, 37)], GN, arrow=True); lab(ax, 81, 39.3, "dry inlet", GN)
    wire(ax, [(40, 52), (28.3, 52)], OR, arrow=True); lab(ax, 29, 54.2, "HEPA out (back wall)", OR)
    wire(ax, [(28.3, 47), (40, 47)], OR, arrow=True); lab(ax, 29, 44.8, "HEPA return (back wall)", OR)
    wire(ax, [(28.3, 27), (40, 27)], RD, arrow=True); lab(ax, 29, 29.2, "aerosol port and valve", RD)
    wire(ax, [(76, 14), (76, 8), (92, 8)], PU, arrow=True); lab(ax, 77, 10, "drain from the drip tray", PU)
    ax.text(42, 17, "Soda lime cartridge (CO2 zero checks only) clips\ninline between pump B and the dryer.", fontsize=7, color=MUT, va="bottom")
    _ = res.append(OUT / "air-loops.png")
    fig.savefig(OUT / "air-loops.png", facecolor="white"); plt.close(fig)

    # ---- wiring
    fig, ax = setup("CalRig prototype: block-level wiring",
                    "Bought modules wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.")
    RED, BLU, GRY, BLK = "#B91C1C", "#1D4ED8", "#6B7280", "#111827"
    blk(ax, 3, 46, 16, 11, "Power supply", "certified 12 V, 10 A\nexternal brick", BLK)
    blk(ax, 26, 46, 20, 11, "Fuse and cut-offs", "10 A blade fuse; bimetal\n50 C (air), 70 C (hot side)\nand a cut-off relay", "#B45309")
    blk(ax, 54, 40, 26, 17, "Controller", "ESP32-class board, 15 A\nH-bridge, MOSFETs,\nmicroSD, USB and I2C hub", "#15803D")
    blk(ax, 88, 50, 28, 7, "Peltier module", "", "#C2410C")
    blk(ax, 88, 40, 28, 7, "Bubbler pad and line trace", "", "#0369A1")
    blk(ax, 88, 30, 28, 7, "Pumps A, B and HEPA blower", "", "#475569")
    blk(ax, 88, 20, 28, 7, "Fans and front status light", "", "#334155")
    blk(ax, 54, 16, 26, 12, "Cable glands (back wall)", "six sensor leads, reference\nleads, mixing fan lead", "#4C1D95")
    blk(ax, 10, 16, 32, 14, "Inside the chamber", "six sensors under test,\n2 x SHT45, SCD30, SPS30,\nmixing fan, 50 C air cut-off", "#0EA5E9")
    wire(ax, [(19.3, 51.5), (26, 51.5)], RED); lab(ax, 22.6, 59.2, "12 V, 1.5 mm²", RED, "center")
    wire(ax, [(46.3, 51.5), (54, 51.5)], RED); lab(ax, 50, 54, "1.5 mm²", RED, "center")
    wire(ax, [(80.3, 53.5), (88, 53.5)], RED); lab(ax, 84, 55.8, "1.5 mm²", RED, "center")
    wire(ax, [(80.3, 43.5), (88, 43.5)], RED); lab(ax, 84, 45.8, "0.75 mm²", RED, "center")
    wire(ax, [(80.3, 41), (84, 41), (84, 33.5), (88, 33.5)], RED); lab(ax, 83.6, 37, "0.5 mm²", RED, "right")
    wire(ax, [(84, 33.5), (84, 23.5), (88, 23.5)], RED); lab(ax, 83.6, 27, "0.5 mm²", RED, "right")
    wire(ax, [(67, 40), (67, 28.3)], BLU); lab(ax, 67.6, 34, "I2C, UART, USB\n0.25 mm²", BLU)
    wire(ax, [(54, 22), (42.3, 22)], BLU); lab(ax, 43, 24.4, "through the glands", BLU)
    wire(ax, [(36, 46), (36, 30.3)], GRY, 1.2); lab(ax, 36.6, 38, "cut-off loop,\n0.5 mm²", GRY)
    ax.text(3, 10.5, "Safety: the two bimetal cut-offs hold in the relay that feeds the Peltier and heater outputs; if either opens, those outputs "
            "lose power whatever the software does.", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 7, "Red: 12 V power. Blue: data. Grey: cut-off loop and thermistors (bubbler pad, line trace and outer sink each carry one). "
            "Everything is 12 V; no mains inside the rig.", fontsize=7.2, color=MUT)
    fig.savefig(OUT / "wiring.png", facecolor="white"); plt.close(fig); res.append(OUT / "wiring.png")
    return res


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "diagrams", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "layouts": layouts, "diagrams": diagrams}
    OUT.mkdir(parents=True, exist_ok=True)
    for w in what:
        r = fns[w]()
        print(w, "->", r)

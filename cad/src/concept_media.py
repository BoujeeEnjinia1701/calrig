"""CalRig concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X across the bench (conditioning column at +X), Y front (-Y, door) to back (+Y), Z up.
Units mm. The rig stands on a 12 mm base plate at z = 0; the bench top is at z = 0 in the hero.
Chamber: 6 mm acrylic, 400 x 300 x 300 mm inside (36 L).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all, human_figure


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cyl(x, y, z0, r, h):
    """Vertical cylinder standing on z0."""
    return Pos(x, y, z0 + h / 2) * Cylinder(r, h)


T = 6.0                                   # acrylic wall
CX0, CX1 = -290.0, 122.0                  # chamber outside, X (412 mm)
CY0, CY1 = -156.0, 156.0                  # chamber outside, Y (312 mm)
CZ0, CZ1 = 12.0, 324.0                    # chamber outside, Z (312 mm)
INS = 25.0                                # insulation jacket thickness

# 4 Base plate
base = box(-300, 310, -205, 265, 0, 12)

# 1 Chamber shell: five-sided acrylic box, open at the front (-Y) for the door
shell = box(CX0, CX1, CY0, CY1, CZ0, CZ1) - box(CX0 + T, CX1 - T, CY0 - 1, CY1 - T, CZ0 + T, CZ1 - T)
shell = shell - box(CX1 - T - 1, CX1 + 1, -45, 45, 150, 250)                    # Peltier opening, +X wall
shell = shell - Pos(CX0 - 1 + T / 2, 0, 230) * Rot(0, 90, 0) * Cylinder(10, T + 4)   # aerosol port, -X wall
for y in (-60, 60):                                                             # conditioning ports, +X wall
    shell = shell - Pos(CX1 - T / 2, y + 40, 70) * Rot(0, 90, 0) * Cylinder(6, T + 4)

# 2 Front door: clear acrylic plate with gasket frame and two latches
door = box(CX0, CX1, CY0 - 10, CY0, CZ0, CZ1)
door = door + box(CX0 + 30, CX0 + 60, CY0 - 22, CY0 - 10, 150, 190) + box(CX1 - 60, CX1 - 30, CY0 - 22, CY0 - 10, 150, 190)

# 3 Insulation jacket: removable XPS panels on the top, back and left side
jacket = (box(CX0, CX1, CY0, CY1 + INS, CZ1, CZ1 + INS)
          + box(CX0, CX1, CY1, CY1 + INS, CZ0, CZ1)
          + box(CX0 - INS, CX0, CY0, CY1 + INS, CZ0, CZ1 + INS))
jacket = jacket - Pos(CX0 - INS / 2, 0, 230) * Rot(0, 90, 0) * Cylinder(16, INS + 2)   # port clearance

# 5 Peltier heat pump: inner fin sink, module through the wall, outer sink and fan outside
peltier = (box(CX1 - T - 30, CX1 - T, -40, 40, 155, 245)
           + box(CX1 - T, CX1, -40, 40, 160, 240)
           + box(CX1, CX1 + 40, -55, 55, 145, 255)
           + box(CX1 + 40, CX1 + 65, -45, 45, 155, 245))

# 6 Internal mixing fan, top back corner
mixfan = box(-200, -120, 110, 140, 220, 300)

# 7 Sensor tray with six bays and a harness rail
tray = box(-270, 60, -130, 130, 60, 66) + box(-270, 60, 118, 130, 66, 90)
for y in (-110, 110):
    for x in (-265, 55):
        tray = tray + box(x, x + 5, y - 5, y + 5, CZ0 + T, 60)

# Sensors under test (example payload, not in the BOM): six boxes on the tray
duts = None
for i, x in enumerate((-240, -140, -40)):
    for y in (-70, 45):
        b = box(x, x + 70, y, y + 55, 66, 106)
        duts = b if duts is None else duts + b

# 8 Reference sensor cluster on a short mast in the middle of the tray, above the sensors
ref = (box(-150, -140, 5, 15, 66, 160)
       + box(-185, -105, -20, 40, 160, 200)
       + box(-175, -115, -10, 30, 200, 215))

# 9 Humidifier bubbler (distilled water, air pump) on the conditioning column
bubbler = cyl(245, -100, 12, 40, 150) + box(215, 275, -100 - 22, -100 + 22, 162, 180)
# 10 Dryer column (indicating silica gel, air pump)
dryer = cyl(245, 10, 12, 30, 230) + cyl(245, 10, 242, 14, 12)
# 11 HEPA scrubber loop behind the chamber (zero air and controlled aerosol decay)
hepa = box(-220, -60, CY1 + INS + 5, 255, 12, 150)
# 12 Aerosol injection port with valve, -X side
port = (Pos(CX0 - INS - 30, 0, 230) * Rot(0, 90, 0) * Cylinder(10, 60)
        + box(CX0 - INS - 50, CX0 - INS - 30, -14, 14, 244, 262))
# 13 Controller and power board with independent over-temperature cut-off
ctrl = box(180, 305, 120, 255, 12, 70)
# 14 Power supply, 12 V 10 A, certified external brick
psu = box(-30, 110, CY1 + INS + 10, 240, 12, 50)
# 15 Salt fixed-point jars (LiCl, MgCl2, NaCl, KCl), front right
jars = None
for i, x in enumerate((180, 212, 244, 276)):
    j = cyl(x, -178, 12, 13, 40)
    jars = j if jars is None else jars + j

parts = [
    Part("Chamber shell, 6 mm acrylic, 36 L", shell, "#B6D3DF", 1),
    Part("Front door with gasket and latches", door, "#D6E8EF", 2, (-60, -820, -120)),
    Part("Insulation jacket (XPS, removable)", jacket, "#F2E8C9", 3, (-160, 300, 520)),
    Part("Base plate", base, "#8B6F4E", 4, (0, 0, -200)),
    Part("Peltier heat pump, 60 W", peltier, "#C2410C", 5, (360, -90, 150)),
    Part("Internal mixing fan", mixfan, "#374151", 6, (0, -60, 230)),
    Part("Sensor tray, six bays", tray, "#6B7280", 7, (0, -300, -30)),
    Part("Sensors under test (example)", duts, "#9CA3AF", None, (0, -300, -30)),
    Part("Reference cluster (SHT45 x2, SCD30, SPS30)", ref, "#0F766E", 8, (0, -300, 250)),
    Part("Humidifier bubbler", bubbler, "#38BDF8", 9, (330, -200, 0)),
    Part("Dryer column (silica gel)", dryer, "#D4A017", 10, (430, 0, 40)),
    Part("HEPA scrubber loop", hepa, "#E5E7EB", 11, (0, 300, 0)),
    Part("Aerosol injection port and valve", port, "#991B1B", 12, (-170, 0, 60)),
    Part("Controller and power board", ctrl, "#15803D", 13, (330, 360, -40)),
    Part("12 V power supply (external)", psu, "#1F2937", 14, (60, 560, -40)),
    Part("Salt fixed-point jars", jars, "#FAFAFA", 15, (200, -260, 0)),
]

# Context for scale, hero and blueprint isometric only: a lab bench and a 1.75 m person
bench = box(-420, 460, -330, 330, -900, 0)
person = human_figure(1750.0, x=820, y=0, z=-900)
context = [Part("Lab bench", bench, "#C8CDD3"), Part("Person, 1.75 m", person.shape, "#9CA3AF")]

render_all(
    parts, project="CalRig", title="Sensor calibration chamber concept", dwg_no="CLR-DWG-010",
    key_figures=["Chamber 400 x 300 x 300 mm inside (36 L), 6 sensor bays",
                 "10 to 40 °C, 20 to 85 % RH (targets; cooling limited)",
                 "PM2.5 0 to 300 µg/m³ by smoke decay (estimate)",
                 "References: 2 x SHT45, SCD30, collocated SPS30",
                 "Salt fixed points 11, 33, 75, 84 % RH at 25 °C",
                 "About 610 x 470 x 350 mm, 12 V, 70 W peak (est.)",
                 "About $396 in parts (indicative); budget $300"],
    scale_figure=False, context=context, cut_exclude=("Front door with gasket and latches",),
    flow={"title": "calibration run, setpoint to record (durations are estimates)", "unit": "",
          "stages": [("Setpoint sweep", "4 T and RH points"), ("Chamber, 36 L", "settle 45 min (est.)"),
                     ("Log all sensors", "every 10 s, 6 bays"), ("Smoke decay run", "300 to 5 µg/m³ (est.)"),
                     ("Per-sensor fit", "slope, offset, RH term"), ("Calibration record", "CSV + PDF by serial")]},
)

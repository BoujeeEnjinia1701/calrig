"""CalRig concept media (TRL 3), generated from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Main parts and interfaces only; not for fabrication.

Axes: X across the bench (conditioning column at +X), Y front (-Y, door) to back (+Y), Z up.
Units mm. The rig stands on its 12 mm base plate at z = 0; the bench top is at z = 0 in the hero.
The removable door panel (part of BOM line 3) is left out of the media so the inside stays visible.
"""
import sys
from pathlib import Path
SRC = Path(__file__).resolve().parent
sys.path[:0] = [str(SRC.parents[1] / ".kit"), str(SRC)]
from concept import Part, render_all, human_figure  # noqa: E402
from model import PARAMS, build_parts, derived, box  # noqa: E402

p = build_parts(door_panel=False)
D = derived()

parts = [
    Part("Chamber shell, 6 mm acrylic, 36 L", p["shell"], "#B6D3DF", 1),
    Part("Front door with gasket and latches", p["door"], "#D6E8EF", 2, (-60, -820, -120)),
    Part("Insulation jacket (XPS, all faces but the door)", p["jacket"], "#F2E8C9", 3, (-160, 320, 560)),
    Part("Base plate, 600 x 500 mm", p["base"], "#8B6F4E", 4, (0, 0, -220)),
    Part("Peltier heat pump, 60 W", p["peltier"], "#C2410C", 5, (440, -200, 300)),
    Part("Internal mixing fan, 120 mm", p["mixfan"], "#374151", 6, (0, -60, 250)),
    Part("Sensor tray, six bays", p["tray"], "#6B7280", 7, (0, -320, -30)),
    Part("Sensors under test (example)", p["duts"], "#9CA3AF", None, (0, -320, -30)),
    Part("Reference cluster (SHT45 x2, SCD30, SPS30)", p["ref"], "#0F766E", 8, (0, -320, 260)),
    Part("Humidifier bubbler, sleeved, heated line", p["bubbler"], "#38BDF8", 9, (330, -220, 0)),
    Part("Dryer column (silica gel)", p["dryer"], "#D4A017", 10, (430, 60, 40)),
    Part("HEPA scrubber loop", p["hepa"], "#E5E7EB", 11, (0, 320, 0)),
    Part("Aerosol injection port and valve", p["port"], "#991B1B", 12, (-190, 0, 60)),
    Part("Controller and power board", p["ctrl"], "#15803D", 13, (420, 420, -200)),
    Part("12 V power supply (external)", p["psu"], "#1F2937", 14, (-420, -150, 480)),
    Part("Salt fixed-point jars", p["jars"], "#FAFAFA", 15, (200, -260, 0)),
]

# Context for scale, hero and blueprint isometric only: a lab bench and a 1.75 m person
bench = box(-440, 460, -330, 330, -900, 0)
person = human_figure(1750.0, x=820, y=0, z=-900)
context = [Part("Lab bench", bench, "#C8CDD3"), Part("Person, 1.75 m", person.shape, "#9CA3AF")]

fx, fy = D["footprint"]
render_all(
    parts, project="CalRig", title="Sensor calibration chamber concept", dwg_no="CLR-DWG-010",
    key_figures=["Chamber 400 x 300 x 300 mm inside (36 L), 6 sensor bays",
                 "10 to 40 °C in rooms to 25 °C; 11 °C lowest in a 30 °C room",
                 "20 to 85 % RH; 85 % at 20 °C in rooms up to 28 °C",
                 "PM2.5 decay 300 to 5 µg/m³ in about 28 min",
                 "References: 2 x SHT45, SCD30, collocated SPS30",
                 f"{fx:.0f} x {fy:.0f} x {D['height']:.0f} mm, 12 V, 90 W peak, 13.6 kg",
                 "About $412 in parts; budget $400 (CLR-CAL-001)"],
    scale_figure=False, context=context, cut_exclude=("Front door with gasket and latches",),
    flow={"title": "calibration run, setpoint to record (times from CLR-CAL-001, estimates)", "unit": "",
          "stages": [("Setpoint sweep", "4 points, cold to hot"), ("Chamber, 36 L", "22 to 31 min (est.)"),
                     ("Log all sensors", "every 10 s, 6 bays"), ("Smoke decay run", "28 min decay (est.)"),
                     ("Per-sensor fit", "slope, offset, RH term"), ("Calibration record", "CSV + PDF by serial")]},
)

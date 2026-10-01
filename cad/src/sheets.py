"""CalRig general arrangement sheet CLR-DWG-001, Rev P4 (TRL 3, constructable design, CLR-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CLR-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py. Dimensions come from PARAMS and derived(), so they follow any parameter
change. The concept blueprint in media/ is CLR-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-10-01"
DATE0 = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, edge by edge, skipping degenerate projected edges."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly(door_panel=False)
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="CalRig", title="General arrangement", dwg_no="CLR-DWG-001", rev="P4",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Cast acrylic, XPS, plywood; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE0, "AC"),
                         ("P2", "Larger inner Peltier sink; mass and power notes (DDR-002)", DATE0, "AC"),
                         ("P3", "Layout and labels tidied", DATE0, "AC"),
                         ("P4", "Constructable design: frame, door, fittings, drain (DDR-003)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    ix, iy, iz = P["inner"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    ci0, ci1 = D["cx0"] + P["wall"], D["cx1"] - P["wall"]
    yi = Z(D["cz1"] + P["ins"]) - 5
    L += [ext(X(ci0), Z(D["cz1"]), X(ci0), yi - 1), ext(X(ci1), Z(D["cz1"]), X(ci1), yi - 1)]
    L += dim_h(X(ci0), X(ci1), yi, f"{ix:.0f} inside")
    xr = X(bb.max.X) + 12
    L += dim_v(xr, Z(D["cz1"] - P["wall"]), Z(D["floor"]), f"{iz:.0f} inside", side=1)
    L += [ext(X(D["cx1"]), Z(D["cz1"] - P["wall"]), xr + 1, Z(D["cz1"] - P["wall"])),
          ext(X(D["cx1"]), Z(D["floor"]), xr + 1, Z(D["floor"]))]

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    Xt = lambda mx: x + (mx - bb.min.X) * k

    # right view (from +X)
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    yt = Zr(D["height"]) - 5
    L += [ext(Yr(D["cy0"] + P["wall"]), Zr(D["cz1"]), Yr(D["cy0"] + P["wall"]), yt - 1),
          ext(Yr(D["cy1"] - P["wall"]), Zr(D["cz1"]), Yr(D["cy1"] - P["wall"]), yt - 1)]
    L += dim_h(Yr(D["cy0"] + P["wall"]), Yr(D["cy1"] - P["wall"]), yt, f"{iy:.0f} inside")

    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 100, label="Isometric view", sublabel="Not to scale; door panel not shown")
    bw, bd, bh = P["bay"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Chamber {ix:.0f} x {iy:.0f} x {iz:.0f} inside ({D['volume_l']:.0f} L), {P['wall']:.0f} acrylic",
        f"XPS jacket {P['ins']:.0f} on all faces but the door; removable door panel",
        f"Six bays {bw:.0f} x {bd:.0f}, {D['head_clear']:.0f} clear above the tray (R10)",
        f"Peltier opening {P['pelt_open'][0]:.0f} x {P['pelt_open'][1]:.0f} in the +X wall; inner sink "
        f"{P['sink_in'][0]:.0f} x {P['sink_in'][1]:.0f} x {P['sink_in'][2]:.0f}",
        f"Door {D['door_size'][0]:.0f} x {D['door_size'][1]:.0f} on a welded front frame, gasket, four latches",
        f"Bulkheads: 3 x {P['port_d']:.0f} (+X), 2 x {P['port_d']:.0f} to HEPA, drain 6; aerosol {P['aero_stub']:.0f} (-X)",
        f"Base {P['base'][0]:.0f} x {P['base'][1]:.0f} x {P['base'][2]:.0f} plywood; overall height {D['height']:.0f}",
        "Mass about 13.8 kg; 12 V, 90 W peak (CLR-CAL-001)",
        "Third-angle; front view from -Y (door side)",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "CLR-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()

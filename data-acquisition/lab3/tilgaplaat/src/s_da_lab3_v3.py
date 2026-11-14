# DA Lab 3 drop plate V3 (14.11.2026): + shaped stops instead of square corner posts (glass slid along the 30.6 channels).
# Was: drop plate (4 x 4 Gridfinity, 5 x 5 drops, one 30 x 30 cover per drop)
# and AtomS3 screen-side mock-ups. Run: header = fusion-tutor/shared/tools/fusion-geometry/gf_std_foot.py + this file.
# Geometry sources: AtomS3 = official M5Stack STL (M5_Hardware C123_AtomS3), our caliper 24 x 24 x 12.9 (13.11.26);
# research note neliubov-memory/da-lab3-drop-plate-research.md. Claude for Dennel04, 13.11.2026.

def run(_context):
    app = adsk.core.Application.get()
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = d.rootComponent; up = d.userParameters; vi = adsk.core.ValueInput.createByString; P3 = adsk.core.Point3D.create
    FO = adsk.fusion.FeatureOperations
    P = {"gf_fit_adjust": ("0 mm", "Extra inward offset of the standard Gridfinity foot per side (0 = standard)"),
         # drop plate
         "dp_units": ("4", "Gridfinity units per side"),
         "dp_pitch": ("32.5 mm", "Drop / cover pitch: 30.6 cover pocket + 1.9 locating post"),
         "dp_plate": ("2.5 mm", "Plate thickness above the foot top"),
         "dp_cover": ("29.65 mm", "Cover glass, caliper 14.11.26: average 29.65 (V2 assumed 30)"),
         "dp_clear": ("0.3 mm", "Cover clearance per side (Lab 1: 0.4 moved freely, 0.2 jammed)"),
         "dp_gap": ("0.6 mm", "Spacer pad height = resin layer thickness (3 layers at 0.2); measure each plate"),
         "dp_pad_w": ("3 mm", "Spacer pad width"), "dp_pad_l": ("6 mm", "Spacer pad length"),
         "dp_pad_c": ("13.5 mm", "Spacer pad centre from the drop centre (pads under the cover edge midpoints)"),
         "dp_arm": ("6 mm", "Stop arm length from the grid crossing along the cell boundary (reaches into the glass path)"),
         "dp_post_h": ("2.4 mm", "Locating post height above the plate (cover top 1.8)"),
         "dp_mark": ("11 mm", "Scale crosses at +-this from the drop centre (22 mm apart, under the cover corners)"),
         "dp_mark_len": ("4 mm", "Scale cross arm length"),
         "groove_w": ("0.6 mm", "Engraved line width (fill with black marker)"), "groove_d": ("0.4 mm", "Engraved line depth"),
         # AtomS3 mock
         "at_size": ("24 mm", "AtomS3 outer size (caliper 13.11.26, M5Stack STL 24.0)"),
         "at_h": ("12.9 mm", "AtomS3 height (caliper 13.11.26, M5Stack 12.9)"),
         "at_r": ("3 mm", "AtomS3 plan corner radius (M5Stack STL)"),
         "at_wall": ("1.6 mm", "Mock wall; open bottom clears the battery pins"),
         "at_roof": ("3 mm", "Mock roof thickness at the top"),
         "at_win": ("17.8 mm", "Screen opening at the top face (M5Stack STL)"),
         "at_win_r": ("1.2 mm", "Screen opening corner radius (M5Stack STL)"),
         "at_win_in": ("16.2 mm", "Screen opening below the 45 deg chamfer (M5Stack STL)"),
         "at_chamfer": ("0.8 mm", "45 deg chamfer depth of the opening (M5Stack STL 0.79)"),
         "at_recess": ("1.2 mm", "Screen surface below the top face (frame thickness in the M5Stack STL; >= real recess)"),
         "at_active": ("15 mm", "Screen area mark: groove centre line (0.85 in 128 x 128 active area ~15.2)"),
         "at_tick": ("2 mm", "Scale tick pitch on the frame"),
         "at_count": ("6", "Number of mock-ups")}
    for n, (e, c) in P.items():
        if up.itemByName(n) is None: up.add(n, vi(e), "mm" if "mm" in e else "", c)
    v = lambda n: up.itemByName(n).value * (10 if "mm" in P[n][0] else 1)

    def new_comp(name):
        o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create()); o.component.name = name; return o.component
    def plane(C, z):
        pi = C.constructionPlanes.createInput(); pi.setByOffset(C.xYConstructionPlane, adsk.core.ValueInput.createByReal(z / 10))
        return C.constructionPlanes.add(pi)
    def rrect(sk, cx, cy, hx, hy, r):
        L = sk.sketchCurves.sketchLines.addTwoPointRectangle(P3((cx - hx) / 10, (cy - hy) / 10, 0), P3((cx + hx) / 10, (cy + hy) / 10, 0))
        if r > 0:
            for k in range(4):
                a, b = L.item(k), L.item((k + 1) % 4)
                sk.sketchCurves.sketchArcs.addFillet(a, a.endSketchPoint.geometry, b, b.startSketchPoint.geometry, r / 10)
    def rect(sk, x0, y0, x1, y1):
        sk.sketchCurves.sketchLines.addTwoPointRectangle(P3(x0 / 10, y0 / 10, 0), P3(x1 / 10, y1 / 10, 0))
    def extrude(C, sk, dist, op, body=None, taper=None, name="", pick=None):
        profs = adsk.core.ObjectCollection.create()
        for p in sk.profiles:
            if pick is None or pick(p): profs.add(p)
        ei = C.features.extrudeFeatures.createInput(profs, op)
        if taper is None:
            ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(dist / 10))
        else:
            ei.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(abs(dist) / 10)),
                                adsk.fusion.ExtentDirections.NegativeExtentDirection if dist < 0 else adsk.fusion.ExtentDirections.PositiveExtentDirection, vi(taper))
        if body is not None: ei.participantBodies = [body]
        f = C.features.extrudeFeatures.add(ei); f.name = name; return f

    # ---------------- drop plate ----------------
    C = new_comp("drop_plate")
    n = int(v("dp_units")); half = 21 * n - 0.25
    top = GF_HEIGHT; ptop = top + v("dp_plate")
    sk = C.sketches.add(plane(C, top)); sk.name = "plate"; rrect(sk, 0, 0, half, half, 3.75)
    extrude(C, sk, v("dp_plate"), FO.NewBodyFeatureOperation, name="plate")
    plate = C.bRepBodies.item(0); plate.name = "drop_plate"
    cells = [(-21 * (n - 1) + 42 * i, -21 * (n - 1) + 42 * j) for i in range(n) for j in range(n)]
    add_std_feet(C, cells, top)
    p, g = v("dp_pitch"), v("dp_cover") / 2 + v("dp_clear")
    drops = [((i - 2) * p, (j - 2) * p) for i in range(5) for j in range(5)]
    # spacer pads (inside each cover footprint, at the edge midpoints: air leaves through the corners)
    sk = C.sketches.add(plane(C, ptop)); sk.name = "spacer_pads"
    pw, pl, pc = v("dp_pad_w") / 2, v("dp_pad_l") / 2, v("dp_pad_c")
    for (x, y) in drops:
        rect(sk, x - pc - pw, y - pl, x - pc + pw, y + pl); rect(sk, x + pc - pw, y - pl, x + pc + pw, y + pl)
        rect(sk, x - pl, y - pc - pw, x + pl, y - pc + pw); rect(sk, x - pl, y + pc - pw, x + pl, y + pc + pw)
    extrude(C, sk, v("dp_gap"), FO.JoinFeatureOperation, plate, name="spacer_pads")
    # + shaped stops at every grid crossing: arms lie on the cell boundaries, so they overlap the glass edge span
    # and stop sliding along rows/columns (V2 square posts left 30.6 channels open)
    sk = C.sketches.add(plane(C, ptop)); sk.name = "locating_stops"
    s = (p - 2 * g) / 2; L = v("dp_arm"); lim = 2.5 * p + s
    for i in range(6):
        for j in range(6):
            x, y = (i - 2.5) * p, (j - 2.5) * p
            rect(sk, max(x - L, -lim), y - s, min(x + L, lim), y + s)
            rect(sk, x - s, max(y - L, -lim), x + s, min(y + L, lim))
    extrude(C, sk, v("dp_post_h"), FO.JoinFeatureOperation, plate, name="locating_stops")
    # orientation: the post at the corner of drop row 1 / column 1 is 3 mm taller
    sk = C.sketches.add(plane(C, ptop + v("dp_post_h"))); sk.name = "orientation_post"
    x = y = -2.5 * p; rect(sk, x - s, y - s, x + s, y + s)
    extrude(C, sk, 3, FO.JoinFeatureOperation, plate, name="orientation_post")
    # scale crosses (engraved, under the cover corners, outside the spot): 22 mm apart in x and y
    sk = C.sketches.add(plane(C, ptop)); sk.name = "scale_crosses"
    m, a, w = v("dp_mark"), v("dp_mark_len") / 2, v("groove_w") / 2
    for (x, y) in drops:
        for sx in (-1, 1):
            for sy in (-1, 1):
                cx, cy = x + sx * m, y + sy * m
                rect(sk, cx - a, cy - w, cx + a, cy + w); rect(sk, cx - w, cy - a, cx + w, cy + a)
    extrude(C, sk, -v("groove_d"), FO.CutFeatureOperation, plate, name="scale_crosses")

    def info(b):
        bb = b.boundingBox
        return "%s: %.2f x %.2f x %.2f mm, vol %.2f cm3" % (b.name, (bb.maxPoint.x-bb.minPoint.x)*10, (bb.maxPoint.y-bb.minPoint.y)*10, (bb.maxPoint.z-bb.minPoint.z)*10, b.volume)
    print(info(plate)); print("plate bodies %d" % C.bRepBodies.count)
    # check: glass 29.7 square in a pocket, can it leave? probe points just outside the pocket edge midpoints / corners
    z = (ptop + v("dp_gap") + 0.6) / 10
    for (px, py) in [(g + 0.1, 0), (g + 0.1, 12), (12, g + 0.1), (g + 0.1, g + 0.1)]:
        r = plate.pointContainment(P3(px / 10, py / 10, z))
        print("probe (%.2f, %.2f) at glass height: %s" % (px, py, "SOLID" if r == adsk.fusion.PointContainment.PointInsidePointContainment else "open"))

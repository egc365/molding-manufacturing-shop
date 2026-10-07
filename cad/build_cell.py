"""Original provisional FreeCAD layout; run in a FreeCAD Python runtime."""
from pathlib import Path
import json
import math
import hashlib

def load_spec(path):
    spec = json.loads(Path(path).read_text())
    if spec["units"] != "mm":
        raise ValueError("Expected millimetres")
    p = {name: row["value"] for name, row in spec["parameters"].items()}
    for name, value in p.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError("Invalid dimension: " + name)
    if p["build_width"] + 2*p["pallet_margin"] >= p["frame_width"] - 2*p["frame_member"]:
        raise ValueError("Pallet exceeds clear width")
    if p["build_depth"] + 2*p["pallet_margin"] >= p["frame_depth"] - 2*p["frame_member"]:
        raise ValueError("Pallet exceeds clear depth")
    if p["transfer_height"] + p["pallet_thickness"] + p["build_height"] >= p["frame_height"] - p["frame_member"]:
        raise ValueError("Envelope exceeds clear height")
    return spec, p

def build(spec_path, output_dir):
    import FreeCAD as App
    import Part
    spec, p = load_spec(spec_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise ValueError("Output directory must be empty")
    doc = App.newDocument("MoldingCellConcept")
    config = doc.addObject("App::FeaturePython", "CellParameters")
    config.addProperty("App::PropertyLength", "transfer_travel")
    config.transfer_travel = 0
    solids = []
    def box(name, size, origin, color, transparency=0, physical=True):
        obj = doc.addObject("Part::Box", name)
        obj.Length, obj.Width, obj.Height = size
        obj.Placement.Base = App.Vector(*origin)
        if App.GuiUp:
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.Transparency = transparency
        if physical:
            solids.append(obj)
        return obj
    w,d,h,m = (p[k] for k in ("frame_width","frame_depth","frame_height","frame_member"))
    for ix,x in enumerate((0,w-m)):
        for iy,y in enumerate((0,d-m)):
            box("Post%d%d" % (ix,iy),(m,m,h),(x,y,0),(.55,.55,.55))
    for iz,z in enumerate((0,h-m)):
        for iy,y in enumerate((0,d-m)):
            box("RailX%d%d" % (iz,iy),(w-2*m,m,m),(m,y,z),(.55,.55,.55))
        for ix,x in enumerate((0,w-m)):
            box("RailY%d%d" % (iz,ix),(m,d-2*m,m),(x,m,z),(.55,.55,.55))
    pw=p["build_width"]+2*p["pallet_margin"]
    pd=p["build_depth"]+2*p["pallet_margin"]
    x,y=(w-pw)/2,(d-pd)/2
    z,t=p["transfer_height"],p["pallet_thickness"]
    box("HeatedSupportPlaceholder",(pw,pd,10),(x,y,z-10),(.35,.35,.35))
    pallet=box("RemovablePallet",(pw,pd,t),(x,y,z),(.15,.45,.8))
    pallet.setExpression("Placement.Base.x",str(x)+" mm + CellParameters.transfer_travel")
    box("PrintEnvelopeReference",(p["build_width"],p["build_depth"],p["build_height"]),(x+p["pallet_margin"],y+p["pallet_margin"],z+t),(.2,.8,.4),85,False)
    bx=w+p["station_gap"]
    box("CoolingBufferSupportPlaceholder",(pw,pd,10),(bx,y,z-10),(.35,.35,.35))
    doc.recompute()
    for obj in solids:
        if obj.Shape.isNull() or not obj.Shape.isValid() or obj.Shape.Volume <= 0:
            raise RuntimeError("Invalid solid: "+obj.Name)
    config.transfer_travel=bx-x
    doc.recompute()
    actual=pallet.Shape.BoundBox.XMin
    if abs(actual-bx)>1e-6:
        raise RuntimeError("Transfer expression failed")
    config.transfer_travel=0
    doc.recompute()
    native=out/"molding-cell-concept.FCStd"
    step=out/"molding-cell-concept.step"
    doc.saveAs(str(native))
    Part.export(solids,str(step))
    reopened=App.openDocument(str(native))
    if abs(reopened.getObject("RemovablePallet").Shape.BoundBox.XMin-x)>1e-6:
        raise RuntimeError("Saved pallet position differs")
    imported=Part.read(str(step))
    if imported.isNull() or not imported.isValid():
        raise RuntimeError("STEP readback failed")
    receipt={"status":"concept conformance only","freecad_version":list(App.Version()),"physical_objects":len(solids),"transfer_travel_mm":bx-x,"measured_transfer_x_mm":actual,"spec_sha256":hashlib.sha256(Path(spec_path).read_bytes()).hexdigest(),"native_sha256":hashlib.sha256(native.read_bytes()).hexdigest(),"step_sha256":hashlib.sha256(step.read_bytes()).hexdigest()}
    (out/"geometry-receipt.json").write_text(json.dumps(receipt,indent=2))
    return receipt

if __name__ == "__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--spec",required=True)
    parser.add_argument("--output-dir",required=True)
    args=parser.parse_args()
    print(json.dumps(build(args.spec,args.output_dir),indent=2))

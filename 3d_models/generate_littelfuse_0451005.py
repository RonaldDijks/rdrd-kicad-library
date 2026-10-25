"""Generate the nominal external Littelfuse 0451005.MRL package (millimetres).

Requires cadquery-ocp (OCP Python bindings). Run with Python 3.
Source: Littelfuse 451/453 series datasheet, mechanical drawing on page 4:
https://www.littelfuse.com/assetdocs/littelfuse-fuse-451-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1
This is locally generated simplified geometry, not manufacturer-supplied CAD.
No internal fuse element or printed legend is represented.
"""

from OCP.gp import gp_Pnt
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.TDataStd import TDataStd_Name
from pathlib import Path
doc=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'))
shapes=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());colors=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
# Datasheet nominal envelope 6.10 x 2.69 x 2.69mm; 1.45mm end caps.
# Simplified external geometry, without internal fuse element or printed legend.
for name,x,L,rgb in [('gold cap 1',-3.05,1.45,(.73,.59,.28)),('ceramic body',-1.60,3.20,(.90,.88,.80)),('gold cap 2',1.60,1.45,(.73,.59,.28))]:
 shape=BRepPrimAPI_MakeBox(gp_Pnt(x,-1.345,0),L,2.69,2.69).Shape()
 label=shapes.AddShape(shape,False);TDataStd_Name.Set_s(label,TCollection_ExtendedString(name))
 colors.SetColor(label,Quantity_Color(*rgb,Quantity_TOC_RGB),XCAFDoc_ColorType.XCAFDoc_ColorGen)
w=STEPCAFControl_Writer();w.SetColorMode(True);assert w.Transfer(doc,STEPControl_AsIs)
out=Path(__file__).resolve().parent / 'Littelfuse_0451005_MRL.STEP'
assert int(w.Write(str(out)))==1
print(out)

import clr
import sys
sys.path.append('C:\Program Files (x86)\IronPython 2.7\Lib')
import System
from System import Array
from System.Collections.Generic import *
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager 
from RevitServices.Transactions import TransactionManager 

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

import Autodesk 
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
from rpw import db
from pyrevit import forms, DB, revit
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox)
import os
from Autodesk.Revit.DB import FilteredElementCollector, Material, Transaction
from Autodesk.Revit.DB.Visual import AppearanceAssetEditScope, AssetPropertyString
doc = __revit__.ActiveUIDocument.Document

__author__ = "Dolan Klock"

# Tooltip
__doc__ = "Changes materials asset image path under appearance tab in materials dialog"

def set_material_image(doc, material_name, new_image_path):
    materials = FilteredElementCollector(doc).OfClass(Material).ToElements()
    for material in materials:
        if material.Name == material_name:
            appearance_asset_id = material.AppearanceAssetId
            if appearance_asset_id == None or appearance_asset_id == Autodesk.Revit.DB.ElementId.InvalidElementId:
                continue
            with Transaction(doc, "Set Texture Path") as t:
                t.Start()
                with AppearanceAssetEditScope(doc) as edit_scope:
                    editable_asset = edit_scope.Start(appearance_asset_id)
                    asset_property = editable_asset.FindByName("generic_diffuse")
                    if asset_property and asset_property.GetSingleConnectedAsset():
                        connected_asset = asset_property.GetSingleConnectedAsset()
                        bitmap_property = connected_asset.FindByName("unifiedbitmap_Bitmap")
                        if isinstance(bitmap_property, AssetPropertyString):
                            bitmap_property.Value = new_image_path
                            print("Updated material '{}' with new texture path: {}".format(material_name, new_image_path))
                            edit_scope.Commit(True)
                    else:
                        print("No connected asset found for '{}'".format(material_name))
                t.Commit()

def get_all_material_asset_image_paths():
    all_materials = FilteredElementCollector(doc).OfClass(Material)
    material_images = []
    revit_rendering_path = "C:\Program Files (x86)\Common Files\Autodesk Shared\Materials\Textures"
    for mat in all_materials:
        # print(mat)
        appearance_asset_id = mat.AppearanceAssetId
        appearance_asset = doc.GetElement(appearance_asset_id)
        asset = appearance_asset.GetRenderingAsset()
        asset_property = asset.FindByName("generic_diffuse")
        # print(asset_property)
        if asset_property and asset_property.GetSingleConnectedAsset():
                connected_asset = asset_property.GetSingleConnectedAsset()
                bitmap_property = connected_asset.FindByName("unifiedbitmap_Bitmap") # Get the path to the texture image (bitmap)
                image_path = bitmap_property.Value
                if not os.path.isabs(image_path):
                        full_image_path = os.path.join(revit_rendering_path, image_path)
                else:
                    full_image_path = image_path

                material_images.append({
                    "MaterialName": mat.Name,
                    "ImagePath": full_image_path
                })
     
    print(material_images)


if __name__ == "__main__":
    material_name = "Analytical Panels" # name of material to replace image for
    # new image to replace old one
    new_image_path = "C:\\Program Files (x86)\\Common Files\\Autodesk Shared\\Materials\\Textures\\1\\mats\\Woods-Plastics.FinishCarpentry.Siding.SplitLog.jpg"
    set_material_image(doc, material_name, new_image_path)
    # get_all_material_asset_image_paths()














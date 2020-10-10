import os, sys, inspect, random, bpy, bmesh
from math import radians
from mathutils import Matrix

def import_STL_file(file_loc=None):
    """
    if file_loc is not given, it will pick last .STL in the current file location
    """
    
    # selects last .STL file in the dictionary and imports it to the project
    # There should be only one .STL file in the current file
    if file_loc == None:
        currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parentdir = os.path.dirname(currentdir)
        sys.path.append(parentdir)
        for i in os.listdir(parentdir):
            if i.upper().endswith(".STL") == True:
                imported_file = i
    else:
        parentdir = file_loc
        imported_file = file_loc.split("\\")[-1]
         
    imported_object = bpy.ops.import_mesh.stl(filepath=parentdir+"\\"+imported_file, filter_glob="*.stl", files=[{"name":imported_file, "name":imported_file}], directory=parentdir+"\\")

def origin_to_geomery(obj):
    # Put the object to the zeron point
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    obj.location[0] = 0
    obj.location[1] = 0
    obj.location[2] = 0
    return

def rotate_object(obj, deg, axis):
    # https://docs.blender.org/api/current/bmesh.html
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # The @ (at) operator is intended to be used for matrix multiplication. No builtin Python types implement this operator.
    #print(obj.matrix_world, Matrix.Rotation(radians(deg), 4, axis))
    obj.matrix_world @= Matrix.Rotation(radians(deg), 4, axis) # does the magic
    obj.select_set(False)

def move_object(obj, distance, axis):
    # https://docs.blender.org/api/current/bmesh.html
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    if axis.upper() == "X":
        obj.location.x = distance
    elif axis.upper() == "Y":
        obj.location.y = distance
    else:
        obj.location.z = distance
        
    obj.select_set(False)

def add_shrimkwarp(obj1, obj2):
    # adds shrimkwrap to imported_obj and stick two objects together
    obj1.select_set(True)
    bpy.context.view_layer.objects.active = obj1
    bpy.ops.object.modifier_add(type='SHRINKWRAP')

    # meshes objects together
    bpy.context.object.modifiers["Shrinkwrap"].target = obj2

def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """Returns a transformed, triangulated copy of the mesh"""

    assert obj.type == 'MESH'

    if apply_modifiers and obj.modifiers:
        import bpy
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        me = obj_eval.to_mesh()
        bm = bmesh.new()
        bm.from_mesh(me)
        obj_eval.to_mesh_clear()
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # TODO. remove all customdata layers.
    # would save ram

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm

def bmesh_calc_area(bm):
    """Calculate the surface area."""
    return sum(f.calc_area() for f in bm.faces)

def main(Xdeg=random.randint(-360, 360), Ydeg=random.randint(-360, 360), Zdeg=random.randint(-360, 360)):
    try:
        imported_obj = bpy.data.objects[0] # might have a diffirent name
    except KeyError:
        raise print("object did not found, Delete all objects and try again")
    # creates a plane object to project the .stl file object into it, and resizes it
    bpy.ops.mesh.primitive_plane_add(size=500, enter_editmode=False, location=(0, 0, 0))

    plane = bpy.data.objects["Plane"] # plane object
    
    #resets objects
    origin_to_geomery(plane)
    origin_to_geomery(imported_obj)
    
    #adjusts plane for shrimkwrap (raduius area)
    rotate_object(plane, 90, 'X')
    move_object(plane, 200, 'Y')
    
    #rotates imported objects accordingly (random in this case)
    rotate_object(imported_obj, Xdeg, 'Y')
    rotate_object(imported_obj, Ydeg, 'X')
    rotate_object(imported_obj, Zdeg, 'Z')
    
    
    add_shrimkwarp(imported_obj, plane) #obj1 => obj2
    
    obj = bpy.context.active_object
    bm = bmesh_copy_from_object(obj, apply_modifiers=True) # selected object should be imported_obj
    result = bmesh_calc_area(bm)
    print(result)
    return result

#    tower = bpy.data.objects['Eiffel tower sample']
#    random = random.randint(0, 10000000000000000000000) # random number to save file unique
#    filepath = parentdir + "\\" + str(random) + "_example_" + ".svg"
# C:\Program Files\Blender Foundation\Blender 2.82\2.82\scripts\addons\object_print3d_utils
try:
    for i in bpy.data.objects: i.select_set(True);bpy.ops.object.delete()
except:
    pass

import_STL_file() # Asks for file location parameter file_loc. If not given imports the last .STL file he found in the current file
main() # Requires 3 int parameters: Xdeg, Ydeg, Zdeg

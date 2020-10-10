import os, sys, inspect, random, bpy, bmesh
from math import radians
from mathutils import Matrix

def import_STL_file():
    # selects last .STL file in the dictionary and imports it to the project
    # There should be only one .STL file in the current file
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.append(parentdir)
    for i in os.listdir(parentdir):
        if i.upper().endswith(".STL") == True:
            imported_file = i
        
    imported_object = bpy.ops.import_mesh.stl(filepath=parentdir+"\\"+imported_file, filter_glob="*.stl", files=[{"name":imported_file, "name":imported_file}], directory=parentdir+"\\")

def origin_to_geomery(obj):
    # Put the object to the zero point
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


def main():
    try:
        # you should import the .stl file
        # .stl object need to be the only object in the project
        imported_obj = bpy.data.objects[0] # might have a diffirent name
        print(imported_obj.name)
    except KeyError:
        return print("object did not found, probable you should delete the camera objects")
    # creates a plane object to project the .stl file object into it, and resizes it
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(-45, 50, 10))
    plane = bpy.data.objects["Plane"] # plane object
    
    #resets objects
    origin_to_geomery(plane)
    origin_to_geomery(imported_obj)
    
    #adjusts plane for shrimkwrap (raduius area)
    rotate_object(plane, 90, 'X')
    move_object(plane, 200, 'Y')
    
    imported_obj.select_set(False)
    plane.select_set(True)
    # changes plane's size by 200%
    bpy.ops.transform.resize(value=(200, 200, 200), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
    #rotates imported objects accordingly (random in this case)
    rotate_object(imported_obj, random.randint(-360, 360), 'Y')
    rotate_object(imported_obj, random.randint(-360, 360), 'X')
    rotate_object(imported_obj, random.randint(-360, 360), 'Z')
    
    
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
import_STL_file()
main()
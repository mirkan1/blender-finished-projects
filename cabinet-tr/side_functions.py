import bpy
from os import listdir
from os.path import isfile, join
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
parentdir = os.path.dirname(currentdir)
file_loc = parentdir + '\\objects\\'

def import_obj(file_loc):
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
    obj_object = bpy.context.selected_objects[0] ####<--Fix
    print('Imported name: ', obj_object.name)
    parentdir
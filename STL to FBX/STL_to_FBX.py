from bpy_extras.io_utils import ExportHelper
import os.path
import os,sys, inspect, bpy, time
from os import listdir
from os.path import isfile, join

bl_info = {
    "name": "STL to FBX converter", 
    "author": "Raq",
    "category": "3D View",
    "blender": (2, 80, 0),
    "description": "VIEW3D_PT_RigConverter",
    "location": "View3D > Object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }
    
def get_file_name(filepath):
    onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    filepath = filepath + "\\" + "result" + str(len(onlyfiles)) + ".fbx"
    return filepath

def reset_blend():
    # bpy.ops.wm.read_factory_settings(use_empty=True) # FACTORY RESET
    # only worry about data in the startup scene    
    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
            #bpy.data.lamps,
            bpy.data.cameras,
    ):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

def main(mainfolder):
    onlyfolders = [f for f in listdir(mainfolder)]
    for i in onlyfolders:
        file = [f for f in listdir(mainfolder + "\\" + i) if isfile(join(mainfolder + "\\" + i, f))]
        for f in file:
            bpy.ops.import_mesh.stl(filepath=mainfolder + "\\" + i + "\\" + f)
        filepath = get_file_name(bpy.context.scene.STF_QueryProps.converting_path_prop)
        
        bpy.ops.export_scene.fbx(filepath=filepath, check_existing=True, axis_forward='-Z', axis_up='Y', filter_glob="*.fbx", use_selection=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', bake_space_transform=False, object_types={'MESH'}, use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='OFF', use_mesh_edges=False, use_tspace=False, use_custom_props=False, add_leaf_bones=True, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, armature_nodetype='NULL', bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
        reset_blend()
        
class STF_QueryProps(bpy.types.PropertyGroup):        
    path_prop = bpy.props.StringProperty(default="C://")
    converting_path_prop = bpy.props.StringProperty(default="C://")

class STF_PT_Panel(bpy.types.Panel):
    bl_idname = "STF_PT_.operator"
    bl_label = "STL_TO_FBX_PT"
    bl_description = "select the folder then click the button to change stl files to fbx"
    bl_category = 'STL to FBX'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        props = bpy.context.scene.STF_QueryProps
        layout = self.layout

        row = layout.row()
        row.label(text="Select STL(subfolders):")
        row.operator("export_scene.folder", text="STL Folder")
    
        row = layout.row()
        row.label(text="Select FBX:")
        row.operator("export_scene.folder_converting_path_prop", text="FBX Folder")
        
        row = layout.row()
        row.operator("object.stl_to_fbx", text="Run")
        
class STL_OT_Operator(bpy.types.Operator):
    bl_idname = "object.stl_to_fbx"
    bl_label = "STL to FBX"

    def execute(self, context):
        main(bpy.context.scene.STF_QueryProps.path_prop)
        return {'FINISHED'}
    

class ExportOperator(bpy.types.Operator, ExportHelper):
    """Operator for setting a directory path."""

    #: Name of function for calling the nif export operator.
    bl_idname = "export_scene.folder"

    #: How the nif import operator is labelled in the user interface.
    bl_label = "STL folder"

    filename_ext = "."
    use_filter_folder = True

    def execute(self, context):
        userpath = self.properties.filepath
#        if(not os.path.isdir(userpath)):
#            msg = "Please select a directory not a file\n" + userpath
#            self.report({'WARNING'}, msg)

        #Insert the desired logic here to write to the directory.
        bpy.context.scene.STF_QueryProps.path_prop = "\\".join(userpath.split("\\")[:-1])
        return{'FINISHED'}

class ExportOperator_converting_path(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.folder_converting_path_prop"
    bl_label = "FBX folder"

    filename_ext = "."
    use_filter_folder = True

    def execute(self, context):
        userpath = self.properties.filepath
        bpy.context.scene.STF_QueryProps.converting_path_prop = "\\".join(userpath.split("\\")[:-1])
        return{'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(
        ExportOperator.bl_idname, text="Export Scene to folder")
    
classes = (
    STF_QueryProps,
    STF_PT_Panel,
    STL_OT_Operator,
    ExportOperator,
    ExportOperator_converting_path,
)

    
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Register QueryProps
    bpy.types.Scene.STF_QueryProps = bpy.props.PointerProperty(type=STF_QueryProps)


def unregister():
    from bpy.utils import unregister_class
    bpy.utils.previews.remove(custom_icons)
    
    for cls in classes:
        unregister_class(cls)
    # $ delete QueryProps on unregister
    del(bpy.types.Scene.STF_QueryProps)

if __name__ == "__main__":
    print(__name__)
    register()
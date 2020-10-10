

#material_output = material.node_tree.nodes.get('Material Output')
#emission = material.node_tree.nodes.new('ShaderNodeTexImage') #new('ShaderNodeBsdfDiffuse')
#import pdb;pdb.set_trace()#emission.inputs['Color'].default_value = (randint(0,100) / 100, randint(0,100) / 100, randint(0,400) / 100, 1)
#material.node_tree.links.new(material_output.inputs[0], emission.outputs[0])
## set activer material to your new material 
#obj.active_material, curMat = material, material
#color = curMat.node_tree.nodes['Diffuse BSDF'].inputs[0]
#str = curMat.node_tree.nodes['Diffuse BSDF'].inputs[1]
import bpy
from random import randint

bl_info = {
    "name" : "texture_wear",
    "author" : "Mirkan",
    "description" : "Preview and change textures of the selected object",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

class TW_QueryProps(bpy.types.PropertyGroup):        
    path_prop = bpy.props.StringProperty(default="C://")

class TW_OT_changer_button(bpy.types.Operator):
    bl_idname = "object.texture_change"
    bl_label = "Texture Wearer"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = bpy.context.scene.TW_QueryProps
        
        image_path = props.path_prop#"C:\\Users\\Raq\\Desktop\\Textures\\black_and_yellow.png"
        obj = bpy.context.active_object
        # Create a new material each time. Need adjustings
        mat = bpy.data.materials.new(name="mat")
        bpy.context.object.active_material = mat
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        texture = nodes.new("ShaderNodeTexImage")
        texture.image = bpy.data.images.load(image_path)
        links.new(nodes[0].inputs[0], texture.outputs[0])
        return {'FINISHED'}
        
class TW_PT_panel(bpy.types.Panel):
    bl_idname = "texture_wear.operator"
    bl_label = "VIEW3D_PT_TextureWearer"
    bl_description = "Preview and change textures of the selected object"
    bl_category = 'Change Texture'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_options = {"REGISTER", "UNDO"}


    def draw(self, context):
        props = bpy.context.scene.TW_QueryProps
        layout = self.layout

        row = layout.row()
        row.label(text="Change the texture:")

        row = layout.row()
        row.prop(props, "path_prop", text="")
        row = layout.row()
        row.operator("object.texture_change", text="Execute")

classes = (
    TW_QueryProps,
    TW_OT_changer_button,
    TW_PT_panel,
)

# register(), unregister()
#register, unreguster = bpy.utils.register_classes_factory(classes)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Register QueryProps
    bpy.types.Scene.TW_QueryProps = bpy.props.PointerProperty(type=TW_QueryProps)


def unregister():

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    # $ delete QueryProps on unregister
    del(bpy.types.Scene.QueryProps)

if __name__ == "__main__":
    print(__name__)
    register()
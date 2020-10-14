bl_info = {
    "name": "Flipping Materials", 
    "author": "Mirkan(Raq)",
    "category": "3D View",
    "blender": (2, 80, 0),
    "description": "VIEW3D_PT_Flipy",
    "location": "View3D > Object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }
    
import bpy

#GUI
class RigConverter(bpy.types.Panel):
    bl_label = "Flipping Materials"
    bl_idname = "VIEW3D_PT_Flipy"
    bl_description = "Metallic flipper, and Rughness invert adder"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Flipping Materials'
    
    def draw(self, context):
        layout = self.layout
        
        # Main Operators/Basic
        row = layout.row()
        row.operator("object.single_target", text="Single Target")
        
        row = layout.row()
        row.operator("object.whole_scene", text="Whole Scene")
        
def main(mat):
    bpy_mat = bpy.data.materials
    # example mat
    # mat = bpy_mat["Weapon 1.000"]
    
    try:
        mat = bpy_mat[mat.name]
        matnodes = mat.node_tree.nodes
    except AttributeError:
        print("ERROR", AttributeError)
        return {"CANCELLED"}

    # Metalic node function
    metalic_input = False
    try:
        BSDF = matnodes["Principled BSDF"]
    except KeyError:
        print("ERROR doesnt have Principled BSDF connected to material" ) # KeyError
        return {"CANCELLED"}
    for i in BSDF.inputs:
        if i.name == "Metallic":
            metalic_input = i
            break

    if metalic_input != False:
        if metalic_input.default_value == 0:
            metalic_input.default_value = 1
        else:
            metalic_input.default_value = 0

    rougness_input = False
    for i in BSDF.inputs:
        if i.name == "Roughness":
            rougness_input = i
            break
        
    follow_node = False
    if rougness_input != False:
        if rougness_input.is_linked:
            follow_node = rougness_input.links[0].from_node

    if follow_node != False:
        # removes previous node connections
        if follow_node.type == "INVERT":
            # ERROR CATCH
            print("Error INVERT node is already connected")
            return {"CANCELLED"}
        lam = follow_node.outputs[0].links
        for i in lam: mat.node_tree.links.remove(i)
        
        # invert node append function
        invert_node = matnodes.new("ShaderNodeInvert")
        for i in follow_node.outputs:
            if i.name == "Color":
                #mat.node_tree.links.new(follow_node.outputs[0], invert_node.inputs[1])
                mat.node_tree.links.new(i, invert_node.inputs[1])
        # Finisher function / connecter function
        mat.node_tree.links.new(invert_node.outputs[0], rougness_input)
    else:
        # ERROR CATCH
        print("Error there is no such output connected to Rougness input")    
        

# Single Target
class Single_Target_OP(bpy.types.Operator):
    bl_idname = "object.single_target"
    bl_label = "for single target usage, select the object and run"

    def execute(self, context):
        try:
            for i in bpy.context.selected_objects[0].material_slots:
                mat = i
                main(i)
        except IndexError:
            self.report({"ERROR"}, "Object is not selected")
            return {"CANCELLED"}
        return {'FINISHED'}
    
# Whole Scene
class Whole_Scene_OP(bpy.types.Operator):
    bl_idname = "object.whole_scene"
    bl_label = "for single target usage, select the object and run"

    def execute(self, context):
        for i in bpy.data.objects:
            for j in i.material_slots:
                #print(i.name, "has", j.name)
                mat = j
                main(j)
        return {'FINISHED'}

classes = (
    Whole_Scene_OP,
    Single_Target_OP,
    RigConverter,
)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

if __name__ == "__main__":
    register();
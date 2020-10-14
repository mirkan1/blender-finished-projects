bl_info = {
    "name": "CopyPastarina", 
    "author": "LON, Mirkan",
    "category": "3D View",
    "blender": (2, 80, 0),
    "description": "VIEW3D_PT_RigConverter",
    "location": "View3D > Object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }
import bpy, random

class QueryProps(bpy.types.PropertyGroup):        
    tgt_armature = bpy.props.StringProperty(default="Controller")
    sl_armature = bpy.props.StringProperty(default="Avastar")
        
    tgt_vg1 = bpy.props.StringProperty(default="TGT-")
    slb_vg1 = bpy.props.StringProperty(default="")
    slb_b1 = bpy.props.StringProperty(default="")

#RENAMEVERTEX BUTTON
class ConvertToSL(bpy.types.Operator):

    bl_idname = "object.convert_to_sl"
    bl_label = "Convert vertex group to sl bones"

    def execute(self, context):
        props = bpy.context.scene.QueryProps            
        arr = bpy.context.scene.QueryProps.arr
        for a in range(len(arr)):
            try:
                # tgt_vg => slb_vg1
                tgt_vg = getattr(bpy.context.scene.QueryProps, arr[a][2])
                slb_vg = getattr(bpy.context.scene.QueryProps, arr[a][1])
                
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = bpy.data.objects[props.tgt_armature]
                #bpy.context.scene.QueryProps.tgt_vg1 = "Group1"
                bpy.context.object.vertex_groups[tgt_vg].name = slb_vg
                setattr(bpy.context.scene.QueryProps, arr[a][2], slb_vg)
                setattr(bpy.context.scene.QueryProps, arr[a][1], " ")
            except KeyError:
                pass

        return {'FINISHED'}
        
#COPYCONSTRAINT BUTTON               
class CopyConstraint(bpy.types.Operator):

    bl_idname = "object.copy_constraint"
    bl_label = "Copy Constraint"

    def execute(self, context):
        props = bpy.context.scene.QueryProps
        # props.sl_armature, [Avastar Armature] # Armature.001 
        # props.slb_b1, [Avastar Pose Bone] The bone that written on the target we want to change # myBone
        # props.tgt_armature,[Target Armature] # Armature.003 
        # props.tgt_vg1, [Target Vertext Group] # Bone
        
        arr = props.arr
        for a in range(len(arr)):
            slb_b = getattr(bpy.context.scene.QueryProps, arr[a][0])
            tgt_vg = getattr(bpy.context.scene.QueryProps, arr[a][2])
            
            # bone check
#            try:
#                # tgt_vg name (bone) spell check
#                bpy.data.objects[props.tgt_armature].data.bones[tgt_vg]
#            except KeyError:
#                continue
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            
            
            # active object change
            bpy.context.view_layer.objects.active = bpy.data.objects[props.sl_armature] # bpy.data.objects[props.sl_armature].select_set(True)
            bpy.ops.object.mode_set(mode='POSE') # bpy.ops.object.posemode_toggle()
            
            bpy.data.objects[props.sl_armature].data.bones[slb_b].select = True
            bpy.ops.pose.constraint_add(type='COPY_TRANSFORMS')
            bpy.context.object.pose.bones[slb_b].constraints[-1].target = bpy.data.objects[props.tgt_armature] # Target Armature
            bpy.context.object.pose.bones[slb_b].constraints[-1].subtarget = tgt_vg # Target Vertext Group
        return {'FINISHED'}       

#GUI
class RigConverter(bpy.types.Panel):
    bl_label = "Rig Converter"
    bl_idname = "VIEW3D_PT_RigConverter"
    bl_description = "Vertex groups name change and location copy"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Quickie'
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        props = bpy.context.scene.QueryProps
        layout = self.layout
        
        #RENAMEVERTEXGROUP & COPYCONSTRAINT BUTTON
        row = layout.row()
        row.operator("object.convert_to_sl", text="RenameVertexGroup")        
        row.operator("object.copy_constraint", text="CopyConstraintTransform")

        #LABELS
        row = layout.row()
        row.label(text="Target Armature:")
        row.label(text="Avastar Armature:")
        
        #TEXTBOX / INPUTBOX for TargetArmature & AvastarArmature names
        row = layout.row()
        row.prop(props, "tgt_armature", text="")
        row.prop(props, "sl_armature", text="")
        row = layout.row()
        
        #LABELS
        row.label(text="Target Vertext Group:")
        row.label(text="Avastar Deform Bone:")
        row.label(text="Avastar Pose Bone:")
        
        #TEXTBOX / INPUTBOX For Target, Deform & Pose bone names
        row = layout.row()
        row.prop(props, "tgt_vg1", text="")
        row.prop(props, "slb_vg1", text="")
        row.prop(props, "slb_b1", text="")


# Register Classes
classes = (
    QueryProps,
    ConvertToSL,
    CopyConstraint,
    RigConverter,
)

def menu_func(self, context):
    self.layout.operator(RigConverter.bl_idname)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Register QueryProps
    bpy.types.Scene.QueryProps = bpy.props.PointerProperty(type=QueryProps)
    bpy.types.Scene.QueryProps[1]['type'].arr = [['slb_b1', 'slb_vg1', 'tgt_vg1']]
    #bpy.types.WM_OT_toolbar.append(menu_func)


def unregister():

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    # $ delete QueryProps on unregister
    del(bpy.types.Scene.QueryProps)

if __name__ == "__main__":
    register();
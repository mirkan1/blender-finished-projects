bl_info = {
    "name" : "Insert/Delete Loops",                        # The name in the addon search menu
    "author" : "rdana2016",
    "description" : "Insert and Delete Loops",
    "blender" : (2, 80, 0),                             # Lowest version to use
    "location" : "View3D",
    "category" : "Generic"
}

import bpy

class PANEL_PT_theInterface(bpy.types.Panel):
    bl_label = "Fiverr"
    bl_category = "Fiverr"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text= "Your scripts:")
        row = layout.row()                       # Create a new line
        row.operator("object.insertloops", text = "Insert Loops", icon='WORLD_DATA')
        row = layout.row()
        row.operator("object.deleteloops", text = "Delete Loops", icon='WORLD_DATA') # Display the operator by calling his idname

class OBJECT_OT_insertloops(bpy.types.Operator):         # Create the operator
    bl_idname = "object.insertloops"                     # idname to display the operator
    bl_label = "Simple operator"
    bl_description = "Inserts Loops"

    def execute(self, context):                         # What the operator does        
        # bpy.ops.mesh.loop_multi_select(ring=True)
        # bpy.ops.mesh.subdivide(quadcorner='INNERVERT')
        # bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.loop_multi_select(ring=True)
        bpy.ops.mesh.hide(unselected=True)
        bpy.ops.mesh.subdivide_edgering(number_cuts=1, interpolation='LINEAR', smoothness=0, profile_shape_factor=0, profile_shape='LINEAR')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.reveal(select=False)
        bpy.ops.mesh.set_edge_flow(tension=180, iterations=1)
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}
               
class OBJECT_OT_deleteloops(bpy.types.Operator):         # Create the operator
    bl_idname = "object.deleteloops"                     # idname to display the operator
    bl_label = "Simple operator"
    bl_description = "Deletes Loops"

    def execute(self, context):                         # What the operator does         
        #bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.loop_multi_select(ring=False)
        bpy.ops.mesh.dissolve_edges()
        return {"FINISHED"}
        

def menu_func(self, context):
    self.layout.operator(ObjectCursorArray.bl_idname)

# store keymaps here to access after registration      
addon_keymaps = []  
classes = (PANEL_PT_theInterface,OBJECT_OT_insertloops,OBJECT_OT_deleteloops) # Classes name here
#register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_object.append(menu_func)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(OBJECT_OT_insertloops.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Screen Editing', space_type='EMPTY')
        kmi = km.keymap_items.new(OBJECT_OT_deleteloops.bl_idname, 'Q', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
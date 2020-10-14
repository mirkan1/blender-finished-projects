bl_info = {
    "name": "mirkan",
    "category": "Object",
}
import bpy


class ObjectCursorArray(bpy.types.Operator):
    """Object Cursor Array"""
    bl_idname = "object.cursor_array"
    bl_label = "Cursor Array"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.particle_system_add()
        bpy.data.particles[-1].type = 'HAIR'
        bpy.data.particles[-1].count = 0
        bpy.ops.particle.particle_edit_toggle()
        bpy.context.scene.tool_settings.particle_edit.brush.count = 1
        bpy.ops.particle.brush_edit(stroke=[{"name":"", "location":(0, 0, 0), "mouse":(374, 316), "pressure":0, "size":0, "pen_flip":False, "time":0, "is_start":False}])

        return {'FINISHED'}

def register():
    bpy.utils.register_class(ObjectCursorArray)


def unregister():
    bpy.utils.unregister_class(ObjectCursorArray)


if __name__ == "__main__":
    register()
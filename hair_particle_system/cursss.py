bl_info = {
    "name": "Cursor ArrayXXXX",
    "category": "Object",
}

import bpy


class ObjectCursorArray(bpy.types.Operator):
    """Object Cursor Array"""
    bl_idname = "object.cursor_array"
    bl_label = "Cursor Array"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        total = 10

        for i in range(total):
            obj_new = obj.copy()
            scene.objects.link(obj_new)

            factor = i / total
            obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        return {'FINISHED'}

def register():
    bpy.utils.register_class(ObjectCursorArray)


def unregister():
    bpy.utils.unregister_class(ObjectCursorArray)


if __name__ == "__main__":
    register()
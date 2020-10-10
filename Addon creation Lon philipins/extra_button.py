import bpy, random
arr = []

def render_panel(self, context):
    layout = self.layout
    row = layout.row()
    props = bpy.context.scene.QueryProps
    #print(arr[-1],arr[-2],arr[-3])
    #setattr(copy_cls, name, deepcopy(attr))
    #bpy.types.Scene.QueryProps[1]['type'].my_prop =  bpy.props.StringProperty()
    
    row.prop(props, arr[-1], text="")
    row.prop(props, arr[-2], text="")
    row.prop(props, arr[-3], text="")
    return {'FINISHED'}
        
def run():
    ct = bpy.context.scene.QueryProps.ct
    Qarr = bpy.context.scene.QueryProps.arr
    Qarr.append([])
    for i in range(3):
        if i == 0:
            myvar = "slb_b" + str(ct)
        elif i == 1:
            myvar =  "slb_vg" + str(ct)
        elif i == 2:
            myvar =  "tgt_vg" + str(ct)
            
        Qarr[-1].append(myvar)
        arr.append(myvar)
        setattr(bpy.types.Scene.QueryProps[1]['type'], myvar, bpy.props.StringProperty())
    #print(bpy.context.scene.QueryProps.arr[-1])
    bpy.types.VIEW3D_PT_RigConverter.append(render_panel)
    return {'FINISHED'}

if __name__ == "__main__":
    try:
        bpy.types.Scene.QueryProps[1]['type'].ct
        bpy.types.Scene.QueryProps[1]['type'].ct = int(bpy.context.scene.QueryProps.ct) + 1
    except AttributeError:
        bpy.types.Scene.QueryProps[1]['type'].ct = 2
    run()

#for i in dir(bpy.context.scene.QueryProps):
#     try:
#         setattr(bpy.context.scene.QueryProps, str(i), str(i));
#         #setattr(bpy.context.scene.QueryProps, "var10461", str(ct))
#     except:
#         pass
# Importing hair.py.
# It is not posible to import the module directly becuase the script is in a virtual file inside untitle.blend
import os,sys, inspect, bpy
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from hair import hair


######################################################################################
for i in hair: print(i, "\n")
bpy.context.area = 'VIEW_3D'
#trial_0
#obj = bpy.data.objects
#print(obj)
#obj.select_set(True)
bpy.ops.object.particle_system_add()
bpy.data.particles[-1].type = 'HAIR'
bpy.data.particles[-1].count = 0
bpy.ops.particle.particle_edit_toggle()

# Set number of hair per hit
bpy.context.scene.tool_settings.particle_edit.brush.count = 1

bpy.ops.particle.brush_edit(stroke=[{"name":"", "location":(0, 0, 0), "mouse":(374, 316), "pressure":0, "size":0, "pen_flip":False, "time":0, "is_start":False}])
#bpy.ops.particle.brush_edit(stroke=[{"name":"", "location":(0, 0, 0), "mouse":(3n46, 385), "pressure":0, "size":0, "pen_flip":False, "time":0, "is_start":False}])


###########################################################################################

# Importing hair.py.
# It is not posible to import the module directly becuase the script is in a virtual file inside untitle.blend
import os,sys, inspect, bpy, time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from hair import hair



######################################################################################
for i in hair: print(i, "\n")
bpy.ops.object.particle_system_add()
bpy.data.particles[-1].type = 'HAIR'
bpy.data.particles[-1].count = 0
bpy.ops.particle.particle_edit_toggle()
bpy.context.scene.tool_settings.particle_edit.brush.count = 1

#area = bpy.types.Area(bpy.context.area)
#area = bpy.types.RegionView3D(area)
#area.type = 'VIEW_3D'
#override = bpy.context.copy()
#time.sleep(5)



for window in bpy.context.window_manager.windows:
    screen = window.screen

for area in screen.areas:
        if area.type == 'VIEW_3D':
            area = bpy.types.RegionView3D(area)
            override = {'window': window, 'screen': screen, 'area': area}
            time.sleep(3)
            bpy.ops.particle.brush_edit(override, stroke=[{"name":"", "location":(0, 0, 0), "mouse":(374, 316), "pressure":0, "size":0, "pen_flip":False, "time":0, "is_start":False}])




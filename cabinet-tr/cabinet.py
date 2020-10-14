import bpy
from inspect import currentframe, getfile
from os import listdir
from os.path import isfile, join, dirname, abspath

bl_info = {
    "name": "Cabinet Create", 
    "author": "Mirkan",
    "category": "3D View",
    "blender": (2, 80, 0),
    "description": "VIEW3D_PT_CabinetCreate",
    "location": "View3D > Object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }

diffuse = "diffuse_xtm.jpg"
diffuse_png = "diffuse_xtm.png"
disabled_texture_obj = [
    "door_knop",
    "door_knop_right",
    "door_knop_left",
    "plint_foot_1",
    "plint_foot_2",
    "plint_foot_3",
    "plint_foot_4",
    ]

class QueryProps(bpy.types.PropertyGroup): 
    """ property, degiskenlerin tanimlandigi degisken kaydetme sinifi(fonskiyon'lar disizi de diyebilirsin) """    
    height = bpy.props.FloatProperty()
    width = bpy.props.FloatProperty()
    depth = bpy.props.FloatProperty()
    plint_foot_height = bpy.props.FloatProperty()
    
    row_longer = bpy.props.BoolProperty()
    column_longer = bpy.props.BoolProperty()
    
    #single_door = bpy.props.BoolProperty()
    #double_door = bpy.props.BoolProperty()
        
    tgt_vg1 = bpy.props.StringProperty(default="TGT-")
    slb_vg1 = bpy.props.StringProperty(default="")
    slb_b1 = bpy.props.StringProperty(default="")
    
#GUI
class MainPanel(bpy.types.Panel):
    """ Ana panel ve menu ekrani """
    bl_label = "Cabinet Create"
    bl_idname = "VIEW3D_PT_CabinetCreate"
    bl_description = "Cabinet and Shelf and Wardrope"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cabinet Create'

    def draw(self, context):
        props = bpy.context.scene.QueryProps
        layout = self.layout

        row = layout.row()
        row.label(text="Row longer")
        row.prop(props, "row_longer", text="")
        row = layout.row()
        row.label(text="Column longer")
        row.prop(props, "column_longer", text="")

        row = layout.row()
        row.label(text="height:")
        row.prop(props, "height", text="")
        
        row = layout.row()
        row.label(text="width:")
        row.prop(props, "width", text="")
        
        row = layout.row()
        row.label(text="depth:")
        row.prop(props, "depth", text="") # not working currently
        
        row = layout.row()
        row.operator("object.cabinet_creator_op", text="Create the frame")
        
        row = layout.row()
        column = row.column()
        column.label(text="single door")
        column.operator("object.add_single_door", text="Add single door")  
              
        column = row.column()
        column.label(text="double door")
        
        column.operator("object.add_double_door", text="Add double door") 
        
        row = layout.row()
        row.label(text="Add texture to the frame")
        row = layout.row()
        row.operator("object.texture_change_wood", text="Red Wood")
        row.operator("object.texture_change_brown_wood", text="Brown Wood")
        row = layout.row()
        row.operator("object.texture_change_brick", text="Marble")
        row.operator("object.texture_change_stone", text="Stone")
        
        # sildim gereksiz oldugu icin, kapiyi secerken otomatik yapiyor       
        # row = layout.row()
        # row.label(text="door knop") # kapi kolu
        # row.operator("object.doop_know_op", text="Add door knop")
        
        # row = layout.row()
        # row.label(text="Plinth Foot")
        # row = layout.row()
        # row.label(text="height:")
        # row.prop(props, "plint_foot_height", text="") 
        
        # sildim gereksiz oldugu icin, cerceveyi yaparken otomatik yapiyor
        # row = layout.row()
        # row.label(text="Back piece")
        # row.operator("object.backpiece_op", text="Add back piece")

class Add_Double_Door_OP(bpy.types.Operator):
    """ ikili kapi eklemeyi saglayan fonskyion"""
    
    bl_idname = "object.add_double_door"
    bl_label = "main function of cabinet create"

    def execute(self, context):
        reset_blend()
        main()
        props = bpy.context.scene.QueryProps
        height = props["height"]
        width = props["width"]
        depth = props["depth"]
        
        # double_door piece
        bpy.ops.mesh.primitive_cube_add()
        single_door = bpy.data.objects[0]
        single_door.name = "double_door_right"
        location(single_door, 2, depth/2)
        location(single_door, 0, -width/4)
        single_door.dimensions = width/2, height, 1
        
        bpy.ops.mesh.primitive_cube_add()
        single_door = bpy.data.objects[0]
        single_door.name = "double_door_left"
        location(single_door, 2, depth/2)
        location(single_door, 0, width/4)
        single_door.dimensions = width/2, height, 1
        
        #doot knop (kapi kolu)
        door_knop = import_obj("10407_Door_Knobs_ Pulls_v1_max2009_SG_iteration-2.obj")
        door_knop = bpy.data.objects[0]
        door_knop.name = "door_knop_right"
        location(door_knop, 2, depth/2)
        location(door_knop, 0, width/10)
        door_knop.rotation_euler.x = 0
        
        door_knop.dimensions = width/16, height/4, 2
        
        door_knop = import_obj("10407_Door_Knobs_ Pulls_v1_max2009_SG_iteration-2.obj")
        door_knop = bpy.data.objects[0]
        door_knop.name = "door_knop_left"
        location(door_knop, 2, depth/2)
        location(door_knop, 0, -width/10)
        door_knop.rotation_euler.x = 0
        
        door_knop.dimensions = width/16, height/4, 2
        
        return {'FINISHED'}
    
class Add_Single_Door_OP(bpy.types.Operator):
    """ tek kapi eklemeyi saglayan fonskyion"""
    bl_idname = "object.add_single_door"
    bl_label = "main function of cabinet create"

    def execute(self, context):
        reset_blend()
        main()
        props = bpy.context.scene.QueryProps
        height = props["height"]
        width = props["width"]
        depth = props["depth"]
        
        # single_door piece
        bpy.ops.mesh.primitive_cube_add()
        single_door = bpy.data.objects[0]
        single_door.name = "single_door"
        location(single_door, 2, depth/2)
        single_door.dimensions = width, height, 1
        
        #doot knop (kapi kolu)
        door_knop = import_obj("10407_Door_Knobs_ Pulls_v1_max2009_SG_iteration-2.obj")
        door_knop = bpy.data.objects[0]
        door_knop.name = "door_knop"
        location(door_knop, 2, depth/2)
        location(door_knop, 0, width/3)
        door_knop.rotation_euler.x = 0
        
        door_knop.dimensions = width/16, height/4, 2
        return {'FINISHED'}
    
class BackPiece_OP(bpy.types.Operator):
    """ Arka parca eklemeyi saglayan fonskyion
    Create the frame fonskiyonu ile birlikte calisiyor """
    bl_idname = "object.backpiece_op"
    bl_label = "main function of cabinet create"

    def execute(self, context):
#        reset_blend()
#        main()
#        props = bpy.context.scene.QueryProps
#        height = props["height"]
#        width = props["width"]
#        depth = props["depth"]
#        
#        bpy.ops.mesh.primitive_cube_add()
#        double_door = bpy.data.objects[0]
#        double_door.name = "double_door"
#        location(double_door, 2, -depth/2)
#        double_door.dimensions = width, height, 1
        return {'FINISHED'}
    
class CabinetCreator_OP(bpy.types.Operator):
    """ ana fonksyion // Create the frame tusu"""
    bl_idname = "object.cabinet_creator_op"
    bl_label = "main function of cabinet create"

    def execute(self, context):
        reset_blend()
        main()
        return {'FINISHED'}

class Add_texture_brick_OP(bpy.types.Operator):
    """Marble; mermer dokusunu eklemeyi saglayan fonksiyon"""
    bl_idname = "object.texture_change_brick"
    bl_label = "Texture Wearer"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # brick
        element = "Marble10"
        element_path = textures_path + element + "\\" + element + "_" + diffuse
        for i in bpy.data.objects:
            if i.name in disabled_texture_obj:
                continue 
            bpy.context.view_layer.objects.active = i
            
            # Create a new material each time. Need adjustings
            mat = bpy.data.materials.new(name="mat")
            bpy.context.object.active_material = mat
            mat.use_nodes = True

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            texture = nodes.new("ShaderNodeTexImage")
            texture.image = bpy.data.images.load(element_path)
            links.new(nodes[0].inputs[0], texture.outputs[0])
            
        return {'FINISHED'}
    
class Add_texture_wood_OP(bpy.types.Operator):
    """Wood; tahta dokusunu eklemeyi saglayan fonksiyon"""
    bl_idname = "object.texture_change_wood"
    bl_label = "Texture Wearer"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # regular Wood
        element = "Wood07"
        element_path = textures_path + element + "\\" + element + "_" + diffuse
        for i in bpy.data.objects:
            if i.name in disabled_texture_obj:
                continue 
            bpy.context.view_layer.objects.active = i
            
            # Create a new material each time. Need adjustings
            mat = bpy.data.materials.new(name="mat")
            bpy.context.object.active_material = mat
            mat.use_nodes = True

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            texture = nodes.new("ShaderNodeTexImage")
            texture.image = bpy.data.images.load(element_path)
            links.new(nodes[0].inputs[0], texture.outputs[0])
            
        return {'FINISHED'}

class Add_texture_brown_wood_OP(bpy.types.Operator):
    """Brown Wood; Kahve rengi tahta dokusunu eklemeyi saglayan fonksiyon"""
    bl_idname = "object.texture_change_brown_wood"
    bl_label = "Texture Wearer"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # brown wood
        element = "Wood_02"
        element_path = textures_path + element + "\\" + element + "_" + diffuse_png
        for i in bpy.data.objects:
            if i.name in disabled_texture_obj:
                continue 
            bpy.context.view_layer.objects.active = i
            
            # Create a new material each time. Need adjustings
            mat = bpy.data.materials.new(name="mat")
            bpy.context.object.active_material = mat
            mat.use_nodes = True

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            texture = nodes.new("ShaderNodeTexImage")
            texture.image = bpy.data.images.load(element_path)
            links.new(nodes[0].inputs[0], texture.outputs[0])
            
        return {'FINISHED'}
    
class Add_texture_stone_OP(bpy.types.Operator):
    """Rock; kaya dokusunu eklemeyi saglayan fonksiyon"""
    bl_idname = "object.texture_change_stone"
    bl_label = "Texture Wearer"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # stone
        element = "Rock05"
        element_path = textures_path + element + "\\" + element + "_" + diffuse
        for i in bpy.data.objects:
            if i.name in disabled_texture_obj:
                continue 
            bpy.context.view_layer.objects.active = i
            
            # Create a new material each time. Need adjustings
            mat = bpy.data.materials.new(name="mat")
            bpy.context.object.active_material = mat
            mat.use_nodes = True

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            texture = nodes.new("ShaderNodeTexImage")
            texture.image = bpy.data.images.load(element_path)
            links.new(nodes[0].inputs[0], texture.outputs[0])
            
        return {'FINISHED'}
       
# Register Classes 
############################################################ class'lari kaydetmek:

classes = (
    QueryProps,
    MainPanel,
    CabinetCreator_OP,
    BackPiece_OP,
    Add_Double_Door_OP,
    Add_Single_Door_OP,
    Add_texture_brick_OP,
    Add_texture_wood_OP,
    Add_texture_stone_OP,
    Add_texture_brown_wood_OP,
)

def register():
    # classes tuple'ini teker teker blendera yukluyor
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Register QueryProps
    bpy.types.Scene.QueryProps = bpy.props.PointerProperty(type=QueryProps)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    # $ delete QueryProps on unregister
    del(bpy.types.Scene.QueryProps)
    
############################################################ son:
    
def main():
    """ main fonksiyon; cerceve/iskelet/frame burada yaratiliyor """
    reset_blend()
    props = bpy.context.scene.QueryProps
    height = props["height"]
    width = props["width"]
    depth = props["depth"]
    column_longer = props["column_longer"]
    row_longer = props["row_longer"]
        
    # height
    bpy.ops.mesh.primitive_cube_add()
    left_column = bpy.data.objects[0]
    left_column.name = "left_column"
    location(left_column, 0, -width/2)
    
    bpy.ops.mesh.primitive_cube_add()
    right_column = bpy.data.objects[0]
    right_column.name = "right_column"
    location(right_column, 0, width/2)
    
    # width
    bpy.ops.mesh.primitive_cube_add()
    top_column = bpy.data.objects[0]
    top_column.name = "top_column"
    location(top_column, 1, -height/2)
    
    bpy.ops.mesh.primitive_cube_add()
    bottom_column = bpy.data.objects[0]
    bottom_column.name = "Tbottom_column"
    location(bottom_column, 1, height/2)
    if column_longer:
        left_column.dimensions = 2, height+2, depth
        right_column.dimensions = 2, height+2, depth
        top_column.dimensions = width-1, 2, depth
        bottom_column.dimensions = width-1, 2, depth
    else:
        top_column.dimensions = width+2, 2, depth
        bottom_column.dimensions = width+2, 2, depth
        left_column.dimensions = 2, height-1, depth
        right_column.dimensions = 2, height-1, depth
    
    dims = width/48, height/24, depth/12
    # top right
    bpy.ops.mesh.primitive_cube_add()
    plint_foot_1 = bpy.data.objects[0]
    plint_foot_1.name = "plint_foot_1"
    plint_foot_1.dimensions = dims
    print(plint_foot_1.dimensions.y)
    loc_y = - bottom_column.location.y - height/24/2
    print(loc_y,- plint_foot_1.dimensions.y)
    plint_foot_1.location = right_column.location.x - right_column.location.x/6, loc_y, depth/4
    
    # bottom right
    bpy.ops.mesh.primitive_cube_add()
    plint_foot_2 = bpy.data.objects[0]
    plint_foot_2.name = "plint_foot_2"
    plint_foot_2.location = right_column.location.x - right_column.location.x/6, loc_y, -depth/4
    plint_foot_2.dimensions = dims
    
    #  bottom left
    bpy.ops.mesh.primitive_cube_add()
    plint_foot_3 = bpy.data.objects[0]
    plint_foot_3.name = "plint_foot_3"
    plint_foot_3.location = left_column.location.x - left_column.location.x/6, loc_y, -depth/4
    plint_foot_3.dimensions = dims
    
    #  top left
    bpy.ops.mesh.primitive_cube_add()
    plint_foot_4 = bpy.data.objects[0]
    plint_foot_4.name = "plint_foot_4"
    plint_foot_4.location = left_column.location.x - left_column.location.x/6, loc_y, depth/4
    plint_foot_4.dimensions = dims
    
    bpy.ops.mesh.primitive_cube_add()
    double_door = bpy.data.objects[0]
    double_door.name = "double_door"
    location(double_door, 2, -depth/2)
    double_door.dimensions = width, height, 1
    

def onlyfolders(filepath):
    # .blend in oldugu ana doyadaki dosyalari okuyup sana getiriyor
    onlyfolders = [f for f in listdir(filepath) if not isfile(join(filepath, f))]
    return onlyfolders

##########################################################################################
currentdir = dirname(abspath(getfile(currentframe()))) 
parentdir = dirname(currentdir)
textures_path = parentdir + "\\textures\\"
file_loc = parentdir + '\\objects\\'

def import_obj(file_name):
    # doku(texture)'lari yuklemek icin kullanilan fonksiyon
    bpy.ops.import_scene.obj(filepath=file_loc + file_name)
    obj_object = bpy.context.selected_objects[0] ####<--Fix
    print('Imported name: ', obj_object.name)
    obj_object.name = file_name.split(".")[0]
    return obj_object
    
def reset_blend():
    # only worry about data in the startup scene
    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
                # eger sahnede lamba yoksa error veriyor
            # bpy.data.lamps, 
            bpy.data.cameras,
    ):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)
        
def dimensions(ob, rot, val): # 0,1,2 || X,Y,Z
    ob.dimensions[rot] = val
    return

def location(ob, rot, val):
    ob.location[rot] = val
    return
##########################################################################################

if __name__ == "__main__":
    register()
    
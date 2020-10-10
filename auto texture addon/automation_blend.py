import bpy
from random import randint

obj = bpy.context.active_object
# Create a new material
material = bpy.data.materials.new(name="Background Color")
material.use_nodes = True
curMat = bpy.context.object.active_material
material_output = material.node_tree.nodes.get('Material Output')
emission = material.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
emission.inputs['Color'].default_value = (randint(0,100) / 100, randint(0,100) / 100, randint(0,400) / 100, 1)
material.node_tree.links.new(material_output.inputs[0], emission.outputs[0])
# set activer material to your new material 
obj.active_material, curMat = material, material
color = curMat.node_tree.nodes['Diffuse BSDF'].inputs[0]
str = curMat.node_tree.nodes['Diffuse BSDF'].inputs[1] 
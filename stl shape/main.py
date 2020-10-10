import bpy
import os,sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

cube = bpy.data.objects['Cube 3d printing sample']
tower = bpy.data.objects['Eiffel tower sample']
bpy.ops.object.editmode_toggle()
bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=False)
bpy.data.window_managers["WinMan"].(null) = 'SVG'
bpy.ops.uv.export_layout(filepath="C:\\Users\\Raq\\Desktop\\stl shape\\Eiffel tower sample.svg", mode='SVG', size=(1024, 1024))

from bs4 import BeautifulSoup
html = open("divs.html").read()
soup = BeautifulSoup(html)
print soup.find(id='abc1')

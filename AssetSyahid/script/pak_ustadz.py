import bpy
import math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def make_mat(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = 0.4
    return mat

white = make_mat("White", (0.9, 0.9, 0.9))
black = make_mat("Black", (0.02, 0.02, 0.02))

parts = []

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.7, depth=1.85, location=(0, 0, 2.5))
body = bpy.context.object
body.name = "Body"
parts.append(body)

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.25, depth=0.5, location=(0, 0, 3.5))
neck = bpy.context.object
neck.name = "Neck"
parts.append(neck)

bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.75, location=(0, 0, 4.3))
head = bpy.context.object
head.name = "Head"
parts.append(head)

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.3, depth=1.5, location=(-1.45, 0, 3.1))
left_arm = bpy.context.object
left_arm.name = "LeftArm"
left_arm.rotation_euler = (0, math.radians(90), 0)
parts.append(left_arm)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(-2.25, 0, 3.1))
left_hand = bpy.context.object
parts.append(left_hand)

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.3, depth=1.5, location=(1.45, 0, 3.1))
right_arm = bpy.context.object
right_arm.name = "RightArm"
right_arm.rotation_euler = (0, math.radians(90), 0)
parts.append(right_arm)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(2.25, 0, 3.1))
right_hand = bpy.context.object
parts.append(right_hand)

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=2.0, location=(-0.35, 0, 1.0))
left_leg = bpy.context.object
parts.append(left_leg)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(-0.35, 0.1, 0.1))
left_foot = bpy.context.object
left_foot.scale = (1, 1.4, 0.6)
parts.append(left_foot)

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=2.0, location=(0.35, 0, 1.0))
right_leg = bpy.context.object
parts.append(right_leg)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0.35, 0.1, 0.1))
right_foot = bpy.context.object
right_foot.scale = (1, 1.4, 0.6)
parts.append(right_foot)

bpy.ops.object.select_all(action='DESELECT')
for part in parts:
    part.select_set(True)

bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
character = bpy.context.object
character.name = "Ustadz"

bpy.ops.object.shade_smooth()
character.data.materials.append(white)

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.75, depth=0.6, location=(0, 0, 2.25))
hat = bpy.context.object
hat.name = "Peci"
hat.rotation_euler = (0, 0, 0)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
lowest_z = 999 
bottom_face = None
for i, face in enumerate(hat.data.polygons):
    avg_z = sum(hat.data.vertices[v].co.z for v in face.vertices) / len(face.vertices)
    
    if avg_z < lowest_z:
        lowest_z = avg_z
        bottom_face = i
if bottom_face is not None:
    hat.data.polygons[bottom_face].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')

solidify = hat.modifiers.new(name="Solidify", type='SOLIDIFY')
solidify.thickness = 0.03
solidify.offset = -1

hat.data.materials.append(black)

bpy.ops.object.select_all(action='DESELECT')
hat.select_set(True)
bpy.context.view_layer.objects.active = hat
bpy.ops.object.shade_smooth()

hat.parent = character
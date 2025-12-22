import bpy
import math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def make_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    return mat

concrete_mat = make_material("Concrete", (0.7, 0.7, 0.7))
metal_mat = make_material("Metal", (0.4, 0.4, 0.4))
ceramic_mat = make_material("Ceramic", (0.1, 0.1, 0.1))
wire_mat = make_material("Wire", (0.05, 0.05, 0.05))

bpy.ops.mesh.primitive_cylinder_add(radius=0.18,depth=12,location=(0, 0, 6))
pole = bpy.context.object
pole.data.materials.append(concrete_mat)


def create_crossarm(z, length=2.5):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0, 0, z))
    arm = bpy.context.object
    arm.scale = (length, 0.1, 0.1)
    arm.data.materials.append(metal_mat)
    return arm

top_arm = create_crossarm(11.5, 2.8)
top_arm.name = "Top_Arm"
lower_arm = create_crossarm(10.2, 1.8)
lower_arm.name = "Lower_Arm"

def create_insulator(x, z):
    parts = []

    for i in range(3):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12 - i * 0.02,depth=0.15,location=(x, 0, z - i * 0.18))
        ins = bpy.context.object
        ins.data.materials.append(ceramic_mat)
        parts.append(ins)

    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    return bpy.context.object


left_top_insulator = create_insulator(-1.3, 11.8)
left_top_insulator.name = "Left_Top_Insulator"
right_top_insulator = create_insulator(1.3, 11.8)
right_top_insulator.name = "Right_Top_Insulator"

left_bot_insulator = create_insulator(-0.8, 10.5)
left_bot_insulator.name = "Left_Bot_Insulator"
right_bot_insulator = create_insulator(0.8, 10.5)
right_bot_insulator.name = "Right_Bot_Insulator"
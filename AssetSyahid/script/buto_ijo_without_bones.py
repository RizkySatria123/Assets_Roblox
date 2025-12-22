import bpy
import math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def make_mat(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = 0.6
    return mat

skin = make_mat("Skin", (0.1, 0.6, 0.1))
pants = make_mat("Pants", (0.4, 0.1, 0.5))
horn = make_mat("Horn", (0.86, 0.72, 0.52))

def cylinder(name, loc, radius, height, mat, sides=10):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=sides,
        radius=radius,
        depth=height,
        location=loc
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj

def sphere(name, loc, radius, mat, sides=12):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=sides,
        ring_count=sides//2,
        radius=radius,
        location=loc
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj

def cone(name, loc, radius, height, mat, sides=8):
    bpy.ops.mesh.primitive_cone_add(
        vertices=sides,
        radius1=radius,
        radius2=0.0,
        depth=height,
        location=loc
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj


sphere("Head", (0, 0, 4.7), 0.6, skin)

cylinder("UpperTorso", (0, 0, 3.6), 1.1, 1.4, skin, sides=12)
cylinder("LowerTorso", (0, 0, 2.5), 1.0, 1.2, pants, sides=12)

left_upper_arm = cylinder("LeftUpperArm", (-1.8, 0, 3.8), 0.45, 1.4, skin)
left_upper_arm.rotation_euler = (0, math.radians(90), 0)
left_lower_arm = cylinder("LeftLowerArm", (-2.9, 0, 3.8), 0.42, 1.3, skin)
left_lower_arm.rotation_euler = (0, math.radians(90), 0)
sphere("LeftHand", (-3.6, 0, 3.8), 0.45, skin)

right_upper_arm = cylinder("RightUpperArm", (1.8, 0, 3.8), 0.45, 1.4, skin)
right_upper_arm.rotation_euler = (0, math.radians(90), 0)
right_lower_arm = cylinder("RightLowerArm", (2.9, 0, 3.8), 0.42, 1.3, skin)
right_lower_arm.rotation_euler = (0, math.radians(90), 0)
sphere("RightHand", (3.6, 0, 3.8), 0.45, skin)

cylinder("LeftUpperLeg", (-0.6, 0, 1.5), 0.55, 1.5, pants)
cylinder("LeftLowerLeg", (-0.6, 0, 0.4), 0.5, 1.5, pants)
sphere("LeftFoot", (-0.6, -0.3, -0.3), 0.45, pants)

cylinder("RightUpperLeg", (0.6, 0, 1.5), 0.55, 1.5, pants)
cylinder("RightLowerLeg", (0.6, 0, 0.4), 0.5, 1.5, pants)
sphere("RightFoot", (0.6, -0.3, -0.3), 0.45, pants)

horn_left = cone("LeftHeadHorn",(0.4, -0.18, 5.2),0.12,0.3,horn,6)
horn_right = cone("RightHeadHorn",(-0.4, -0.18, 5.2),0.12,0.3,horn,6)

horn_left.rotation_euler = (math.radians(25), math.radians(40), 0)
horn_right.rotation_euler = (math.radians(25), math.radians(-40), 0)

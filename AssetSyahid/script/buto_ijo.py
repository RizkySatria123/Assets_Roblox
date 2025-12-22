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
sphere("LeftFoot", (-0.6, 0.3, -0.3), 0.45, pants)

cylinder("RightUpperLeg", (0.6, 0, 1.5), 0.55, 1.5, pants)
cylinder("RightLowerLeg", (0.6, 0, 0.4), 0.5, 1.5, pants)
sphere("RightFoot", (0.6, 0.3, -0.3), 0.45, pants)

horn_left = cone("LeftHeadHorn",(0.4, -0.18, 5.2),0.12,0.3,horn,6)
horn_right = cone("RightHeadHorn",(-0.4, -0.18, 5.2),0.12,0.3,horn,6)

horn_left.rotation_euler = (math.radians(25), math.radians(40), 0)
horn_right.rotation_euler = (math.radians(25), math.radians(-40), 0)

bpy.ops.object.armature_add(location=(0, 0, 0))
armature = bpy.context.object
armature.name = "Rig"
armature.show_in_front = True

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = armature.data.edit_bones

edit_bones.remove(edit_bones[0])

bones_data = {
    "LowerTorso": ((0, 0, 1.9), (0, 0, 3.1)),
    "UpperTorso": ((0, 0, 3.1), (0, 0, 4.3)),
    "Head": ((0, 0, 4.3), (0, 0, 5.3)),
    
    "LeftUpperArm": ((-1.1, 0, 4.3), (-1.8, 0, 3.8)),
    "LeftLowerArm": ((-1.8, 0, 3.8), (-2.9, 0, 3.8)),
    "LeftHand": ((-2.9, 0, 3.8), (-3.6, 0, 3.8)),
    
    "RightUpperArm": ((1.1, 0, 4.3), (1.8, 0, 3.8)),
    "RightLowerArm": ((1.8, 0, 3.8), (2.9, 0, 3.8)),
    "RightHand": ((2.9, 0, 3.8), (3.6, 0, 3.8)),
    
    "LeftUpperLeg": ((-0.6, 0, 1.9), (-0.6, 0, 0.75)),
    "LeftLowerLeg": ((-0.6, 0, 0.75), (-0.6, 0, -0.35)),
    "LeftFoot": ((-0.6, 0, -0.35), (-0.6, 0.3, -0.55)),
    
    "RightUpperLeg": ((0.6, 0, 1.9), (0.6, 0, 0.75)),
    "RightLowerLeg": ((0.6, 0, 0.75), (0.6, 0, -0.35)),
    "RightFoot": ((0.6, 0, -0.35), (0.6, 0.3, -0.55)),
}

created_bones = {}
for bone_name, (head_pos, tail_pos) in bones_data.items():
    bone = edit_bones.new(bone_name)
    bone.head = head_pos
    bone.tail = tail_pos
    created_bones[bone_name] = bone

created_bones["UpperTorso"].parent = created_bones["LowerTorso"]
created_bones["Head"].parent = created_bones["UpperTorso"]

created_bones["LeftUpperArm"].parent = created_bones["UpperTorso"]
created_bones["LeftLowerArm"].parent = created_bones["LeftUpperArm"]
created_bones["LeftHand"].parent = created_bones["LeftLowerArm"]

created_bones["RightUpperArm"].parent = created_bones["UpperTorso"]
created_bones["RightLowerArm"].parent = created_bones["RightUpperArm"]
created_bones["RightHand"].parent = created_bones["RightLowerArm"]

created_bones["LeftUpperLeg"].parent = created_bones["LowerTorso"]
created_bones["LeftLowerLeg"].parent = created_bones["LeftUpperLeg"]
created_bones["LeftFoot"].parent = created_bones["LeftLowerLeg"]

created_bones["RightUpperLeg"].parent = created_bones["LowerTorso"]
created_bones["RightLowerLeg"].parent = created_bones["RightUpperLeg"]
created_bones["RightFoot"].parent = created_bones["RightLowerLeg"]

bpy.ops.object.mode_set(mode='OBJECT')

mesh_objects = [
    "Head", "UpperTorso", "LowerTorso",
    "LeftUpperArm", "LeftLowerArm", "LeftHand",
    "RightUpperArm", "RightLowerArm", "RightHand",
    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
    "RightUpperLeg", "RightLowerLeg", "RightFoot", 
    "LeftHeadHorn","RightHeadHorn"
]

bpy.ops.object.select_all(action='DESELECT')
for obj_name in mesh_objects:
    if obj_name in bpy.data.objects:
        bpy.data.objects[obj_name].select_set(True)

armature.select_set(True)
bpy.context.view_layer.objects.active = armature

bpy.ops.object.parent_set(type='ARMATURE_AUTO')


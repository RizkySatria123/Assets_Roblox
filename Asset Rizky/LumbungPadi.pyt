import bpy
import math

def create_lumbung_padi():
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    if "Lumbung_Padi_Grp" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Lumbung_Padi_Grp"], do_unlink=True)

    def create_mat(name, color, roughness=0.9):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        return mat

    mat_kayu = create_mat("Kayu_Tua", (0.3, 0.2, 0.1, 1))
    mat_ijuk = create_mat("Atap_Ijuk", (0.05, 0.05, 0.05, 1)) 
    mat_batu = create_mat("Batu_Kali", (0.2, 0.2, 0.2, 1))
    mat_anyaman = create_mat("Bilik_Bambu", (0.7, 0.6, 0.4, 1))

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    lumbung_grp = bpy.context.active_object
    lumbung_grp.name = "Lumbung_Padi_Grp"

    spacing = 0.8
    for x in [-spacing, spacing]:
        for y in [-spacing, spacing]:
            bpy.ops.mesh.primitive_cube_add(size=0.4, location=(x, y, 0.2))
            stone = bpy.context.active_object
            stone.scale = (1, 1, 0.8)
            stone.data.materials.append(mat_batu)
            stone.parent = lumbung_grp
            
            bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, location=(x, y, 1.0))
            post = bpy.context.active_object
            post.data.materials.append(mat_kayu)
            post.parent = lumbung_grp
            
            bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.05, location=(x, y, 1.7))
            guard = bpy.context.active_object
            guard.data.materials.append(mat_batu) 
            guard.parent = lumbung_grp

    bpy.ops.mesh.primitive_cube_add(size=1)
    body = bpy.context.active_object
    body.scale = (1.8, 1.8, 1.5)
    body.location = (0, 0, 2.5)
    
    bpy.data.objects.remove(body, do_unlink=True)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.5, location=(0,0,2.5))
    body = bpy.context.active_object
    body.data.materials.append(mat_anyaman)
    body.parent = lumbung_grp


    bpy.ops.mesh.primitive_cube_add(size=1)
    door = bpy.context.active_object
    door.scale = (0.05, 0.4, 0.5)
    door.location = (0.95, 0, 2.5) 
    door.data.materials.append(mat_kayu)
    door.parent = lumbung_grp

    bpy.ops.mesh.primitive_cone_add(radius1=1.6, radius2=0, depth=1.8, location=(0,0,4.0))
    roof = bpy.context.active_object
    roof.data.materials.append(mat_ijuk)
    roof.parent = lumbung_grp

    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=2.8)
    ladder_L = bpy.context.active_object
    ladder_L.location = (0.4, -1.2, 1.2)
    ladder_L.rotation_euler = (math.radians(-30), 0, 0)
    ladder_L.data.materials.append(mat_kayu)
    ladder_L.parent = lumbung_grp

    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=2.8)
    ladder_R = bpy.context.active_object
    ladder_R.location = (-0.4, -1.2, 1.2)
    ladder_R.rotation_euler = (math.radians(-30), 0, 0)
    ladder_R.data.materials.append(mat_kayu)
    ladder_R.parent = lumbung_grp
    
    for i in range(5):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.9)
        step = bpy.context.active_object
        z_pos = 0.5 + (i * 0.4)
        y_pos = -1.6 + (i * 0.23)
        step.location = (0, y_pos, z_pos)
        step.rotation_euler = (0, math.radians(90), 0)
        step.data.materials.append(mat_kayu)
        step.parent = lumbung_grp


    bpy.ops.object.select_all(action='DESELECT')
    lumbung_grp.select_set(True)
    bpy.context.view_layer.objects.active = lumbung_grp
    print("Lumbung Padi Anti-Tikus Selesai!")

create_lumbung_padi()
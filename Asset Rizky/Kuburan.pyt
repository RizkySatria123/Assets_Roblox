import bpy
import random

def create_grave_prop_fixed():
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    # --- MATERIAL ---
    def get_material(name, color):
        if name in bpy.data.materials: return bpy.data.materials[name]
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = color
        return mat

    mat_tanah = get_material("Tanah_Kubur", (0.2, 0.15, 0.1, 1)) 
    mat_batu = get_material("Batu_Nisan", (0.3, 0.35, 0.35, 1))
    mat_bunga = get_material("Bunga_Kamboja", (0.9, 0.8, 0.9, 1))

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    grave_group = bpy.context.active_object
    grave_group.name = "Kuburan_Nusantara"

    # --- 1. GUNDUKAN TANAH ---
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1)
    mound = bpy.context.active_object
    mound.name = "Gundukan"
    
    mound.scale = (0.6, 1.2, 0.3) 
    mound.location = (0, 0, 0.1)
    mound.data.materials.append(mat_tanah)
    mound.parent = grave_group

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    bpy.ops.transform.vertex_random(offset=0.05, seed=random.randint(0,100))
    
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- 2. BATU NISAN ---
    def create_nisan(y_pos, is_head):
        bpy.ops.mesh.primitive_cube_add(size=1)
        nisan = bpy.context.active_object
        
        nisan.scale = (0.3, 0.1, 0.6)
        nisan.location = (0, y_pos, 0.4)
        
        bpy.ops.object.modifier_add(type='BEVEL')
        nisan.modifiers["Bevel"].width = 0.05
        
        nisan.data.materials.append(mat_batu)
        nisan.parent = grave_group
        
        tilt_x = random.uniform(-0.2, 0.2)
        tilt_y = random.uniform(-0.1, 0.1)
        nisan.rotation_euler[0] = tilt_x
        nisan.rotation_euler[1] = tilt_y
        
        return nisan

    create_nisan(0.9, True)  
    create_nisan(-0.9, False)

    # --- 3. BUNGA TABUR ---
    for i in range(random.randint(5, 8)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.05)
        flower = bpy.context.active_object
        
        fx = random.uniform(-0.3, 0.3)
        fy = random.uniform(-0.8, 0.8)
        fz = 0.35 
        
        flower.location = (fx, fy, fz)
        flower.data.materials.append(mat_bunga)
        flower.parent = grave_group

    bpy.ops.object.select_all(action='DESELECT')
    grave_group.select_set(True)
    bpy.context.view_layer.objects.active = grave_group
    print("Kuburan Siap (No Error)!")

create_grave_prop_fixed()
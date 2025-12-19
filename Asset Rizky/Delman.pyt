import bpy
import math

def create_delman_full_animated():
    # --- 1. BERSIHKAN AREA KERJA ---
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    def get_mat(name, color):
        if name in bpy.data.materials: return bpy.data.materials[name]
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = color
        return mat

    mat_kayu = get_mat("Kayu_Tua", (0.3, 0.2, 0.1, 1))
    mat_muda = get_mat("Kayu_Muda", (0.6, 0.4, 0.25, 1))
    mat_besi = get_mat("Besi_Hitam", (0.1, 0.1, 0.1, 1))
    mat_atap = get_mat("Atap_Biru", (0.1, 0.2, 0.3, 1))
    mat_emas = get_mat("Emas_Hiasan", (0.8, 0.7, 0.1, 1))

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    root = bpy.context.active_object
    root.name = "Delman_Maju_Jaya"

    wheel_radius = 0.7
    
    def create_wheel_group(is_left):
        x_pos = 0.9 if is_left else -0.9
        name = "Kiri" if is_left else "Kanan"
        
        bpy.ops.object.empty_add(type='ARROWS', location=(x_pos, 0, wheel_radius))
        wheel_holder = bpy.context.active_object
        wheel_holder.name = f"Roda_{name}_Holder"
        wheel_holder.parent = root 
        
        bpy.ops.mesh.primitive_torus_add(major_radius=wheel_radius, minor_radius=0.05, location=(0,0,0))
        rim = bpy.context.active_object
        rim.rotation_euler[1] = math.radians(90)
        rim.data.materials.append(mat_besi)
        rim.parent = wheel_holder 


        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.2, location=(0,0,0))
        hub = bpy.context.active_object
        hub.rotation_euler[1] = math.radians(90)
        hub.data.materials.append(mat_kayu)
        hub.parent = wheel_holder

        spoke_count = 8
        for i in range(spoke_count):
            angle = (2 * math.pi / spoke_count) * i
            bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=wheel_radius * 1.9, location=(0,0,0))
            spoke = bpy.context.active_object
            spoke.rotation_euler[0] = angle 
            spoke.data.materials.append(mat_muda)
            spoke.parent = wheel_holder

        return wheel_holder

    wheel_L = create_wheel_group(is_left=True)
    wheel_R = create_wheel_group(is_left=False)

    # Lantai
    bpy.ops.mesh.primitive_cube_add(size=1)
    floor = bpy.context.active_object
    floor.scale = (1.5, 2.2, 0.1)
    floor.location = (0, 0, 0.8)
    floor.data.materials.append(mat_kayu)
    floor.parent = root

    # Kursi Penumpang (Belakang)
    bpy.ops.mesh.primitive_cube_add(size=1)
    seat1 = bpy.context.active_object
    seat1.scale = (1.3, 0.7, 0.4)
    seat1.location = (0, 0.6, 1.0)
    seat1.data.materials.append(mat_muda)
    seat1.parent = root

    # Kursi Kusir (Depan)
    bpy.ops.mesh.primitive_cube_add(size=1)
    seat2 = bpy.context.active_object
    seat2.scale = (0.8, 0.5, 0.5)
    seat2.location = (0, -0.7, 1.1)
    seat2.data.materials.append(mat_muda)
    seat2.parent = root
    
    # As Roda Panjang 
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.8, location=(0, 0, wheel_radius))
    axle = bpy.context.active_object
    axle.rotation_euler[1] = math.radians(90)
    axle.data.materials.append(mat_besi)
    axle.parent = root

    # Tiang & Atap
    for x in [-0.6, 0.6]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=3.5)
        shaft = bpy.context.active_object
        shaft.rotation_euler[0] = math.radians(90)
        shaft.location = (x, -1.5, 0.9)
        shaft.data.materials.append(mat_kayu)
        shaft.parent = root
        
        # Tiang Atap
        for y in [-0.8, 0.9]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6)
            pole = bpy.context.active_object
            pole.location = (x, y, 1.8)
            pole.data.materials.append(mat_besi)
            pole.parent = root

    # Atap
    bpy.ops.mesh.primitive_cube_add(size=1)
    roof = bpy.context.active_object
    roof.scale = (1.6, 2.4, 0.1)
    roof.location = (0, 0, 2.6)
    bpy.ops.object.modifier_add(type='BEVEL')
    roof.data.materials.append(mat_atap)
    roof.parent = root

    # Lampu Hias
    for x in [-0.7, 0.7]:
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.15)
        lamp = bpy.context.active_object
        lamp.location = (x, -0.8, 1.8)
        lamp.data.materials.append(mat_emas)
        lamp.parent = root

    
    start_frame = 1
    end_frame = 120 
    distance = 20.0 
    rotation_amount = distance / wheel_radius 
    
    print(f"Menganimasikan: Jarak {distance}m, butuh rotasi {math.degrees(rotation_amount):.2f} derajat.")

    root.location.y = 0
    root.keyframe_insert(data_path="location", index=1, frame=start_frame) 
    
    root.location.y = -distance 
    root.keyframe_insert(data_path="location", index=1, frame=end_frame)
    
    for fcurve in root.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points: kf.interpolation = 'LINEAR'

    for wheel in [wheel_L, wheel_R]:
        wheel.rotation_euler[0] = 0
        wheel.keyframe_insert(data_path="rotation_euler", index=0, frame=start_frame)
        wheel.rotation_euler[0] = -rotation_amount
        wheel.keyframe_insert(data_path="rotation_euler", index=0, frame=end_frame)
        
        for fcurve in wheel.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points: kf.interpolation = 'LINEAR'

    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    bpy.ops.object.select_all(action='DESELECT')
    root.select_set(True)
    bpy.context.view_layer.objects.active = root
    print("Delman Siap Jalan! Tekan Spasi.")

create_delman_full_animated()
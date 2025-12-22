import bpy

def clear_scene():
    if bpy.context.active_object and bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def add_uv_unwrap(obj):
    """Membuka kulit objek otomatis agar siap ditempel gambar texture."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

def create_mat(name, color):
    """Material placeholder."""
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color
    return mat

def create_bool_cut(target_obj, cutter_size, cutter_loc):
    """Fungsi cepat untuk melubangi dinding."""
    bpy.ops.mesh.primitive_cube_add(size=1)
    cutter = bpy.context.active_object
    cutter.scale = cutter_size
    cutter.location = cutter_loc
    
    bpy.context.view_layer.objects.active = target_obj
    mod = target_obj.modifiers.new(name="Bool_Cut", type='BOOLEAN')
    mod.object = cutter
    mod.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(modifier="Bool_Cut")
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_rumah_desa():
    # SETUP MATERIAL
    mat_tiang = create_mat("Mat_Tiang_Kayu", (0.2, 0.1, 0.05, 1))
    mat_lantai = create_mat("Mat_Lantai_Papan", (0.4, 0.25, 0.1, 1))
    mat_dinding = create_mat("Mat_Dinding_Papan", (0.5, 0.35, 0.15, 1))
    mat_atap = create_mat("Mat_Genteng_Seng", (0.5, 0.5, 0.1, 1)) # Merah bata
    mat_pintu = create_mat("Mat_Pintu_Kayu", (0.3, 0.2, 0.1, 1))
    mat_jendela = create_mat("Mat_Kusen_Jendela", (0.6, 0.5, 0.4, 1))

    # DIMENSI UTAMA
    lebar_rumah = 5.0
    panjang_rumah = 6.0
    tinggi_panggung = 1.2
    tinggi_dinding = 2.8
    lebar_teras = 1.5
    
    # 1. TIANG PENYANGGA
    jarak_x = (lebar_rumah - 0.4) / 2
    jarak_y = (panjang_rumah - 0.4) / 2
    
    tiang_locs = [
        (-jarak_x, -jarak_y), (0, -jarak_y), (jarak_x, -jarak_y), # Belakang
        (-jarak_x, 0),        (0, 0),        (jarak_x, 0),        # Tengah
        (-jarak_x, jarak_y),  (0, jarak_y),  (jarak_x, jarak_y)   # Depan (Teras)
    ]
    
    for x, y in tiang_locs:
        bpy.ops.mesh.primitive_cube_add(size=1)
        tiang = bpy.context.active_object
        tiang.name = "Tiang_Panggung"
        tiang.scale = (0.3, 0.3, tinggi_panggung)
        tiang.location = (x, y, tinggi_panggung/2)
        add_uv_unwrap(tiang)
        tiang.data.materials.append(mat_tiang)

    # 2. LANTAI UTAMA
    bpy.ops.mesh.primitive_cube_add(size=1)
    lantai = bpy.context.active_object
    lantai.name = "Lantai_Rumah"
    lantai.scale = (lebar_rumah, panjang_rumah, 0.2)
    lantai.location = (0, 0, tinggi_panggung + 0.1)
    add_uv_unwrap(lantai)
    lantai.data.materials.append(mat_lantai)

    # 3. DINDING UTAMA
    panjang_ruangan = panjang_rumah - lebar_teras
    offset_y = -lebar_teras / 2 
    
    bpy.ops.mesh.primitive_cube_add(size=1)
    dinding = bpy.context.active_object
    dinding.name = "Dinding_Rumah"
    dinding.scale = (lebar_rumah - 0.2, panjang_ruangan, tinggi_dinding)
    dinding.location = (0, offset_y, tinggi_panggung + 0.2 + (tinggi_dinding/2))
    
    # Lubang Pintu (Depan Tengah)
    y_depan_dinding = offset_y + (panjang_ruangan/2)
    z_dasar_lantai = tinggi_panggung + 0.2
    
    create_bool_cut(dinding, (1.2, 1.0, 2.0), (0, y_depan_dinding, z_dasar_lantai + 1.0))
    
    # Lubang Jendela (Kiri & Kanan)
    create_bool_cut(dinding, (0.2, 1.0, 1.2), (-(lebar_rumah/2), offset_y, z_dasar_lantai + 1.5)) # Kiri
    create_bool_cut(dinding, (0.2, 1.0, 1.2), ((lebar_rumah/2), offset_y, z_dasar_lantai + 1.5))  # Kanan
    
    add_uv_unwrap(dinding)
    dinding.data.materials.append(mat_dinding)

    # 4. OBJEK PINTU & JENDELA (TERPISAH UTK TEXTURE)
    
    # Pintu
    bpy.ops.mesh.primitive_cube_add(size=1)
    pintu = bpy.context.active_object
    pintu.name = "Pintu_Kayu"
    pintu.scale = (1.1, 0.1, 1.9)
    pintu.location = (0, y_depan_dinding, z_dasar_lantai + 1.0 - 0.05)
    add_uv_unwrap(pintu)
    pintu.data.materials.append(mat_pintu)
    
    # Jendela (Frame Kiri)
    bpy.ops.mesh.primitive_cube_add(size=1)
    jendela_l = bpy.context.active_object
    jendela_l.name = "Jendela_Kiri"
    jendela_l.scale = (0.1, 0.9, 1.1)
    jendela_l.location = (-(lebar_rumah/2)+0.1, offset_y, z_dasar_lantai + 1.5)
    add_uv_unwrap(jendela_l)
    jendela_l.data.materials.append(mat_jendela)

    # Jendela (Frame Kanan)
    bpy.ops.mesh.primitive_cube_add(size=1)
    jendela_r = bpy.context.active_object
    jendela_r.name = "Jendela_Kanan"
    jendela_r.scale = (0.1, 0.9, 1.1)
    jendela_r.location = ((lebar_rumah/2)-0.1, offset_y, z_dasar_lantai + 1.5)
    add_uv_unwrap(jendela_r)
    jendela_r.data.materials.append(mat_jendela)

    # 5. ATAP LIMASAN (Hip Roof)
    bpy.ops.mesh.primitive_cube_add(size=1)
    atap = bpy.context.active_object
    atap.name = "Atap_Limas"
    atap.scale = (lebar_rumah + 0.5, panjang_rumah + 1.0, 1.5)
    z_atap = tinggi_panggung + 0.2 + tinggi_dinding + 0.75
    atap.location = (0, -0.70, z_atap)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type="FACE")
    import bmesh
    bm = bmesh.from_edit_mesh(atap.data)
    for f in bm.faces:
        if f.normal.z > 0.5:
            f.select = True
            
    bmesh.update_edit_mesh(atap.data)
    
    bpy.ops.transform.resize(value=(0.6, 0.4, 1.0)) 
    bpy.ops.object.mode_set(mode='OBJECT')
    
    add_uv_unwrap(atap)
    atap.data.materials.append(mat_atap)

    # 6. TANGGA DEPAN
    steps = 5
    step_depth = 0.3
    step_height = tinggi_panggung / steps
    
    for i in range(steps):
        bpy.ops.mesh.primitive_cube_add(size=1)
        step = bpy.context.active_object
        step.name = f"Tangga_{i}"
        step.scale = (1.2, step_depth, 0.05)
        
        # posisi tangga
        y_start_tangga = (panjang_rumah/2) + 0.2
        y_pos = y_start_tangga + (i * step_depth)
        z_pos = tinggi_panggung - (i * step_height) - 0.1
        
        step.location = (0, y_pos, z_pos)
        add_uv_unwrap(step)
        step.data.materials.append(mat_tiang)

    # LIGHTING
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))
    bpy.context.object.data.energy = 4

if __name__ == "__main__":
    clear_scene()
    create_rumah_desa()

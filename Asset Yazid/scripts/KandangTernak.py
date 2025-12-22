import bpy
import bmesh


def create_cube(name, location, scale):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    return obj


def create_hollow_trough(name, location, scale):
    base = create_cube(name, location, scale)

    cutter_scale = (scale[0] - 0.2, scale[1] - 0.2, scale[2])
    cutter_loc = (location[0], location[1], location[2] + 0.2)
    cutter = create_cube("Cutter", cutter_loc, cutter_scale)

    bool_mod = base.modifiers.new(name="HollowOut", type='BOOLEAN')
    bool_mod.object = cutter
    bool_mod.operation = 'DIFFERENCE'

    bpy.context.view_layer.objects.active = base
    bpy.ops.object.modifier_apply(modifier="HollowOut")

    bpy.data.objects.remove(cutter, do_unlink=True)
    return base


def create_fence(start_pos, end_pos, height=1.2):
    #Membuat tiang kecil dan papan horizontal
    mid_x = (start_pos[0] + end_pos[0]) / 2
    mid_y = (start_pos[1] + end_pos[1]) / 2

    #Papan Atas
    dist = ((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2) ** 0.5
    is_horizontal = abs(start_pos[0] - end_pos[0]) > abs(start_pos[1] - end_pos[1])

    scale = (dist, 0.1, 0.1) if is_horizontal else (0.1, dist, 0.1)
    create_cube("Pagar_Papan_Atas", (mid_x, mid_y, height), scale)
    create_cube("Pagar_Papan_Bawah", (mid_x, mid_y, height - 0.5), scale)

    #Tiang Pagar
    create_cube("Tiang_Pagar", (start_pos[0], start_pos[1], height / 2), (0.15, 0.15, height))
    create_cube("Tiang_Pagar", (end_pos[0], end_pos[1], height / 2), (0.15, 0.15, height))


def setup_complete_barn():
    #bersihkan scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    #dimensi Utama
    w, d, h = 10, 15, 4

    #1. Lantai
    create_cube("Lantai", (0, 0, 0.1), (w, d, 0.2))

    #2. Tiang Utama Struktur
    posts = [(w / 2 - 0.2, d / 2 - 0.2), (-w / 2 + 0.2, d / 2 - 0.2), (w / 2 - 0.2, -d / 2 + 0.2),
             (-w / 2 + 0.2, -d / 2 + 0.2)]
    for p in posts:
        create_cube("Tiang_Utama", (p[0], p[1], h / 2), (0.4, 0.4, h))

    #3. Gudang Pakan (Tertutup di bagian belakang)
    create_cube("Dinding_Gudang_Belakang", (0, d / 2 - 1.5, h / 2), (w - 0.5, 3, h))

    #4. Tempat Makan (Berlubang)
    create_hollow_trough("Tempat_Makan_Sapi", (-w / 2 + 1.2, 0, 0.6), (1.2, d / 2, 1))

    #5. Area Tidur
    create_cube("Area_Tidur", (w / 4, -d / 4, 0.3), (w / 2, d / 2, 0.4))

    #6. Pagar Samping dan Depan
    #Pagar Sisi Kanan
    create_fence((w / 2 - 0.2, d / 2 - 3), (w / 2 - 0.2, -d / 2 + 0.2))
    #Pagar Sisi Depan
    create_fence((w / 2 - 0.2, -d / 2 + 0.2), (1, -d / 2 + 0.2))
    #Pagar Sisi Depan
    create_fence((-w / 2 + 0.2, -d / 2 + 0.2), (-1, -d / 2 + 0.2))

    # 7. Pintu Pagar
    pintu = create_cube("Pintu_Pagar", (0, -d / 2 + 0.2, 0.6), (1.8, 0.1, 1.0))
    pintu.location.x += 0.5
    pintu.rotation_euler[2] = 0.5
    # 8. Atap
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=w / 1.4, depth=d, location=(0, 0, h + 0.8))
    atap = bpy.context.active_object
    atap.rotation_euler[0] = 1.5708
    atap.scale[1] = 0.6

setup_complete_barn()
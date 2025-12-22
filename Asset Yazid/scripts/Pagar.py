import bpy
import random


def clear_scene():
    if bpy.context.active_object and bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def add_uv_unwrap(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')


def create_mat(name, color):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color
    return mat


def create_pagar_roblox():
    jumlah_segmen = 5
    panjang_per_segmen = 3.0
    tinggi_tiang = 1.5

    mat_tiang = create_mat("Mat_Tiang_Pagar", (0.35, 0.25, 0.15, 1))
    mat_palang = create_mat("Mat_Palang_Pagar", (0.45, 0.30, 0.18, 1))

    for i in range(jumlah_segmen + 1):

        loc_x = i * panjang_per_segmen

        bpy.ops.mesh.primitive_cube_add(size=1)
        tiang = bpy.context.active_object
        tiang.name = f"Tiang_{i}"

        tiang.scale = (0.3, 0.3, tinggi_tiang)
        tiang.location = (0, loc_x, tinggi_tiang / 2)

        rotasi_acak = random.uniform(-0.05, 0.05)
        tiang.rotation_euler = (0, 0, rotasi_acak)

        add_uv_unwrap(tiang)
        tiang.data.materials.append(mat_tiang)

        if i < jumlah_segmen:
            bpy.ops.mesh.primitive_cube_add(size=1)
            palang_atas = bpy.context.active_object
            palang_atas.name = f"Palang_Atas_{i}"
            palang_atas.scale = (0.15, panjang_per_segmen + 0.1, 0.2)
            palang_atas.location = (0, loc_x + (panjang_per_segmen / 2), tinggi_tiang - 0.3)

            palang_atas.rotation_euler = (random.uniform(-0.02, 0.02), 0, random.uniform(-0.02, 0.02))

            add_uv_unwrap(palang_atas)
            palang_atas.data.materials.append(mat_palang)

            bpy.ops.mesh.primitive_cube_add(size=1)
            palang_bawah = bpy.context.active_object
            palang_bawah.name = f"Palang_Bawah_{i}"
            palang_bawah.scale = (0.15, panjang_per_segmen + 0.1, 0.2)
            palang_bawah.location = (0, loc_x + (panjang_per_segmen / 2), tinggi_tiang - 0.9)

            palang_bawah.rotation_euler = (random.uniform(-0.02, 0.02), 0, random.uniform(-0.02, 0.02))

            add_uv_unwrap(palang_bawah)
            palang_bawah.data.materials.append(mat_palang)

    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    bpy.context.object.data.energy = 3


if __name__ == "__main__":
    clear_scene()
    create_pagar_roblox()
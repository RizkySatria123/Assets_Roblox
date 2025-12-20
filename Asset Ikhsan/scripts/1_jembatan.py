import bpy
import math
import mathutils

# Config
jumlah_papan = 15
panjang_jembatan = 30.0
tinggi_lengkungan = 1.5
lebar_papan = 4
tebal_papan = 0.2
jarak_antar_papan = 0.01
faktor_peredam_kemiringan = 0.15

interval_tiang = 2
tinggi_tiang = 1.5
tebal_tiang = 0.4
extra_tinggi = 1

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for i in range(jumlah_papan):
    t = i / (jumlah_papan - 1)
    x_pos = (t - 0.5) * panjang_jembatan
    z_pos = math.sin(t * math.pi) * tinggi_lengkungan
    rotasi_y = -math.cos(t * math.pi) * faktor_peredam_kemiringan
    
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, z_pos))
    papan = bpy.context.active_object
    
    panjang_papan_individu = (panjang_jembatan / jumlah_papan) - jarak_antar_papan
    papan.scale = (panjang_papan_individu / 2, lebar_papan / 2, tebal_papan / 2)
    papan.rotation_euler[1] = rotasi_y
    papan.name = f"Papan_{i}"
    
    # TIANG PENOPANG
    if i % interval_tiang == 0:
        y_offset = (lebar_papan / 2) - (tebal_tiang / 2) + tebal_tiang
        
        # z_tiang = z_pos - (tinggi_tiang / 2)
        z_tiang = (z_pos - tinggi_tiang ) / 2
        
        bpy.ops.mesh.primitive_cube_add(location=(x_pos, y_offset, z_tiang))
        tiang_kanan = bpy.context.active_object
        tiang_kanan.scale = (tebal_tiang/2, tebal_tiang/2, (z_pos + tinggi_tiang + extra_tinggi) / 2)
        tiang_kanan.name = f"Tiang_Kanan_{i}"
        
        bpy.ops.mesh.primitive_cube_add(location=(x_pos, -y_offset, z_tiang))
        tiang_kiri = bpy.context.active_object
        tiang_kiri.scale = (tebal_tiang/2, tebal_tiang/2, (z_pos + tinggi_tiang + extra_tinggi) / 2)
        tiang_kiri.name = f"Tiang_Kiri_{i}"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
objek_jadi = bpy.context.active_object
objek_jadi.name = "Jembatan_Nusantara_Base"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bpy.context.view_layer.objects.active = objek_jadi
objek_jadi.select_set(True)

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

z_min_local = min(v[2] for v in objek_jadi.bound_box)
local_shift_vector = mathutils.Vector((0, 0, z_min_local))
shift = objek_jadi.matrix_world.to_3x3() @ local_shift_vector
bpy.context.scene.cursor.location = objek_jadi.location + shift

bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

objek_jadi.location = (0, 0, 0)

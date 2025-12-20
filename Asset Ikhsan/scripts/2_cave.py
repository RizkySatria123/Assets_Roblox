import bpy
import math
import random
import mathutils

# Config
radius_gua = 10            # Lebar mulut gua
kedalaman_gua = 40.0         # Panjang gua ke belakang
tinggi_gua = 6.0            # Tinggi langit-langit
ukuran_batu = 2           # Besar setiap bongkahan batu
variasi_acak = 0.7          # Seberapa "hancur/acak" bentuk batunya

jumlah_ring = 20             # Jumlah tumpukan ke belakang (Depth)
jumlah_batu_per_ring = 15    # Jumlah batu melengkung (Arch)

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for y in range(jumlah_ring):
    pos_y = (y / (jumlah_ring - 1)) * kedalaman_gua
    
    is_back_wall = (y == jumlah_ring - 1)
    
    range_batu = jumlah_batu_per_ring if not is_back_wall else jumlah_batu_per_ring * 2
    
    for i in range(range_batu):
        if is_back_wall:
            angle = (i / (range_batu - 1)) * math.pi
            r_mod = radius_gua * (1 - (random.random() * 0.7))
        else:
            angle = (i / (range_batu - 1)) * math.pi
            r_mod = radius_gua

        x = math.cos(angle) * r_mod
        z = math.sin(angle) * tinggi_gua
        
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, 
            radius=ukuran_batu, 
            location=(x, pos_y, z)
        )
        batu = bpy.context.active_object
        
        # Randomisasi Rotasi & Scale
        batu.rotation_euler = (random.random()*3, random.random()*3, random.random()*3)
        scale_rand = random.uniform(0.8, 1.2)
        batu.scale = (scale_rand, scale_rand, scale_rand)
        batu.select_set(True)

bpy.ops.object.select_all(action='SELECT')

bpy.ops.object.join()
objek_sementara = bpy.context.active_object
objek_sementara.name = "Gua_Temp_Mesh"

bpy.ops.object.mode_set(mode='EDIT')

bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.transform.vertex_random(offset=variasi_acak, uniform=0.1, normal=0.0, seed=0)

bpy.ops.object.mode_set(mode='OBJECT')


bpy.ops.object.join()
objek_jadi = bpy.context.active_object
objek_jadi.name = "Gua_Spawn_Monster"

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
bpy.context.scene.cursor.location = (0,0,0)

print("Gua Low Poly Berhasil Dibuat.")
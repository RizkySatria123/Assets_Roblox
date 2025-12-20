import bpy
import math
import mathutils

tinggi_tulang_belakang = 0.25
jumlah_ruas_tulang = 10
jumlah_rusuk = 6
lebar_dada_max = 1.2
jarak_antar_rusuk = 0.35
tinggi_kaki = 1.2

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# SPINE
for i in range(jumlah_ruas_tulang):
    z_pos = i * (tinggi_tulang_belakang + 0.05) + tinggi_kaki
    
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, z_pos))
    ruas = bpy.context.active_object
    ruas.scale = (0.15, 0.15, tinggi_tulang_belakang / 2)
    ruas.name = f"Spine_{i}"
    ruas.select_set(True)

tinggi_leher = (jumlah_ruas_tulang - 1) * (tinggi_tulang_belakang + 0.05) + tinggi_kaki

# TULANG RUSUK
start_rusuk_index = 3 

for i in range(jumlah_rusuk):
    progress = i / (jumlah_rusuk - 1)
    lebar_mod = math.sin(progress * math.pi) * 0.5 + 0.5
    
    z_pos = (start_rusuk_index + i) * (tinggi_tulang_belakang + 0.05) + tinggi_kaki
    
    bpy.ops.mesh.primitive_torus_add(
        align='WORLD', 
        location=(0, 0, z_pos), 
        rotation=(math.radians(90), 0, 0),
        major_radius=lebar_dada_max * lebar_mod * 0.6, 
        minor_radius=0.08,
        major_segments=8,
        minor_segments=4
    )
    rusuk = bpy.context.active_object
    rusuk.scale = (1, 0.5, 1)
    rusuk.name = f"Rusuk_{i}"
    rusuk.select_set(True)

# PLACEHOLDER KEPALA
bpy.ops.mesh.primitive_cube_add(location=(0, 0, tinggi_leher + 0.8))
kepala = bpy.context.active_object
kepala.scale = (0.4, 0.5, 0.6)
kepala.name = "Kepala_Base"
kepala.select_set(True)

# Bahu
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.3, location=(0.8, 0, tinggi_leher - 0.2))
bahu_kanan = bpy.context.active_object
bahu_kanan.name = "Bahu_R"
bahu_kanan.select_set(True)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.3, location=(-0.8, 0, tinggi_leher - 0.2))
bahu_kiri = bpy.context.active_object
bahu_kiri.name = "Bahu_L"
bahu_kiri.select_set(True)


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
objek_jadi = bpy.context.active_object
objek_jadi.name = "Skeleton_Nusantara_Base"

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
z_min = min(v[2] for v in objek_jadi.bound_box)
bpy.context.scene.cursor.location = (objek_jadi.location.x, objek_jadi.location.y, objek_jadi.location.z + z_min)

local_shift = mathutils.Vector((0, 0, z_min))
world_shift = objek_jadi.matrix_world.to_3x3() @ local_shift
bpy.context.scene.cursor.location = objek_jadi.location + world_shift

bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

objek_jadi.location = (0, 0, 0)
bpy.context.scene.cursor.location = (0,0,0)

print("Skeleton Base Mesh Created")
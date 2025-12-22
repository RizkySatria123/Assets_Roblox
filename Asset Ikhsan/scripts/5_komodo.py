import bpy
import math

def create_blocky_komodo():
    bpy.ops.object.select_all(action='DESELECT')
    parts = []

    # BADAN
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1))
    body = bpy.context.active_object
    body.scale = (1.5, 4, 1) 
    body.name = "Komodo_Body"
    parts.append(body)

    # KEPALA
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2.5, 1.2))
    head = bpy.context.active_object
    head.scale = (1.2, 1.5, 0.9)
    head.name = "Head"
    parts.append(head)

    # EKOR
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 4, 0.8))
    tail = bpy.context.active_object
    tail.scale = (0.8, 4, 0.8)
    tail.rotation_euler = (math.radians(-10), 0, 0) 
    parts.append(tail)

    # KAKI
    legs_info = [
        ("Leg_FL", 1.8, -1.5, -45), # Depan Kiri
        ("Leg_FR", -1.8, -1.5, 45), # Depan Kanan
        ("Leg_BL", 1.8, 1.5, -45),  # Belakang Kiri
        ("Leg_BR", -1.8, 1.5, 45)   # Belakang Kanan
    ]

    for name, x, y, rot in legs_info:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.5))
        leg = bpy.context.active_object
        leg.scale = (0.6, 0.6, 2)

        leg.rotation_euler = (math.radians(30), 0, math.radians(rot)) 
        leg.name = name
        parts.append(leg)

    for part in parts:
        part.select_set(True)
    
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    body.name = "Komodo_Base"
    
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

if __name__ == "__main__":
    create_blocky_komodo()
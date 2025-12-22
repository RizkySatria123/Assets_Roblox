import bpy
import math

def create_blocky_dragon():
    bpy.ops.object.select_all(action='DESELECT')
    
    parts = []

    # BADAN
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3))
    body = bpy.context.active_object
    body.scale = (1.5, 3, 1.5) # Lebar, Panjang, Tinggi
    body.name = "Dragon_Body"
    parts.append(body)

    # LEHER
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2.5, 4.5))
    neck = bpy.context.active_object
    neck.scale = (0.8, 2, 0.8)
    neck.rotation_euler = (math.radians(-45), 0, 0) # Miring ke atas
    parts.append(neck)

    # KEPALA
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -3.5, 6))
    head = bpy.context.active_object
    head.scale = (1, 1.5, 1)
    parts.append(head)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -4.5, 5.8))
    snout = bpy.context.active_object
    snout.scale = (0.6, 0.8, 0.5)
    parts.append(snout)

    # EKOR
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 3, 3))
    tail1 = bpy.context.active_object
    tail1.scale = (1, 2, 1)
    tail1.rotation_euler = (math.radians(20), 0, 0)
    parts.append(tail1)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 5, 2))
    tail2 = bpy.context.active_object
    tail2.scale = (0.6, 2.5, 0.6)
    tail2.rotation_euler = (math.radians(10), 0, 0)
    parts.append(tail2)

    # SAYAP
    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.5, 0, 5))
    wing_L = bpy.context.active_object
    wing_L.scale = (4, 2, 0.2)
    wing_L.rotation_euler = (0, math.radians(20), math.radians(15))
    parts.append(wing_L)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.5, 0, 5))
    wing_R = bpy.context.active_object
    wing_R.scale = (4, 2, 0.2)
    wing_R.rotation_euler = (0, math.radians(-20), math.radians(-15))
    parts.append(wing_R)

    # LEGS
    leg_positions = [
        (1.5, -1.5, 1),  
        (-1.5, -1.5, 1), 
        (1.5, 1.5, 1),   
        (-1.5, 1.5, 1)   
    ]

    for i, pos in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        leg = bpy.context.active_object
        leg.scale = (0.8, 0.8, 3) # Tinggi kaki
        parts.append(leg)


    for part in parts:
        part.select_set(True)
    
    bpy.context.view_layer.objects.active = body
    
    bpy.ops.object.join()
    
    body.name = "Naga_Base"

if __name__ == "__main__":
    create_blocky_dragon()
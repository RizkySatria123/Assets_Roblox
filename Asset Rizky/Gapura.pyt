import bpy

def create_gapura_bentar():
    bpy.ops.object.select_all(action='DESELECT')
    
    mat_bata = bpy.data.materials.new(name="Bata_Merah")
    mat_bata.use_nodes = True

    mat_bata.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.5, 0.15, 0.1, 1)

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    gapura_base = bpy.context.active_object
    gapura_base.name = "Gapura_Majapahit"

    def create_side(side_factor): 
 
        levels = 6
        base_size = 2.0
        height_step = 0.6
        
        previous_width = base_size
        
        for i in range(levels):
            z_pos = i * height_step

            current_width = base_size - (i * 0.25)
            if current_width < 0.5: current_width = 0.5
        
            bpy.ops.mesh.primitive_cube_add(size=1)
            block = bpy.context.active_object
            
            x_pos = (side_factor * current_width / 2) + (side_factor * 1.5) 
            
            block.location = (x_pos, 0, z_pos + (height_step/2))
            block.scale = (current_width, current_width, height_step)
            block.data.materials.append(mat_bata)
            block.parent = gapura_base


            bpy.ops.mesh.primitive_cube_add(size=1)
            detail = bpy.context.active_object
            detail.location = (x_pos, 0, z_pos + height_step)
            
            detail.scale = (current_width + 0.2, current_width + 0.2, 0.1) 
            detail.data.materials.append(mat_bata)
            detail.parent = gapura_base

       
        top_z = levels * height_step
        bpy.ops.mesh.primitive_cube_add(size=1)
        top = bpy.context.active_object
        
        
        top_width = 0.6
        x_top = (side_factor * top_width / 2) + (side_factor * 1.5)
        
        top.location = (x_top, 0, top_z + 0.5)
        top.scale = (top_width, top_width, 1.0) 
        top.data.materials.append(mat_bata)
        top.parent = gapura_base
        
        
        bpy.ops.mesh.primitive_cone_add(radius1=0.4, depth=0.5)
        spire = bpy.context.active_object
        spire.location = (x_top, 0, top_z + 1.2)
        spire.data.materials.append(mat_bata)
        spire.parent = gapura_base

    create_side(1)  
    create_side(-1) 

    bpy.ops.object.select_all(action='DESELECT')
    gapura_base.select_set(True)
    bpy.context.view_layer.objects.active = gapura_base
    print("Gapura Majapahit Siap!")

create_gapura_bentar()
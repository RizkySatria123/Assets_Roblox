import bpy

def create_archer_tower():
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    # --- MATERIAL ---
    def get_mat(name, color):
        if name in bpy.data.materials: return bpy.data.materials[name]
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = color
        return mat

    mat_batu = get_mat("Batu_Pondasi", (0.2, 0.2, 0.2, 1)) 
    mat_kayu = get_mat("Kayu_Menara", (0.4, 0.25, 0.1, 1)) 
    mat_lantai = get_mat("Lantai_Atas", (0.3, 0.2, 0.1, 1))


    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    tower_grp = bpy.context.active_object
    tower_grp.name = "Archer_Tower"

    bpy.ops.mesh.primitive_cube_add(size=1)
    base = bpy.context.active_object
    base.scale = (2.0, 2.0, 1.5) 
    base.location = (0, 0, 0.75)
    base.data.materials.append(mat_batu)
    base.parent = tower_grp

    bpy.ops.mesh.primitive_cube_add(size=1)
    body = bpy.context.active_object
    body.scale = (1.2, 1.2, 2.5) 
    body.location = (0, 0, 2.75) 
    body.data.materials.append(mat_kayu)
    body.parent = tower_grp

    bpy.ops.mesh.primitive_cube_add(size=1)
    top_floor = bpy.context.active_object
    top_floor.scale = (2.2, 2.2, 0.2)
    top_floor.location = (0, 0, 4.1)
    top_floor.data.materials.append(mat_lantai)
    top_floor.parent = tower_grp

    positions = [
        (0.9, 0.9), (-0.9, 0.9), (0.9, -0.9), (-0.9, -0.9), 
        (0.9, 0), (-0.9, 0), (0, 0.9), (0, -0.9)            
    ]
    
    for pos in positions:
        bpy.ops.mesh.primitive_cube_add(size=1)
        block = bpy.context.active_object
        block.scale = (0.4, 0.4, 0.5)
        block.location = (pos[0], pos[1], 4.45) 
        block.data.materials.append(mat_batu)
        block.parent = tower_grp

    mat_batu.use_nodes = True
    nodes = mat_bata_nodes = mat_batu.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    voronoi = nodes.new('ShaderNodeTexVoronoi') 
    voronoi.inputs['Scale'].default_value = 10.0
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 1)
    ramp.color_ramp.elements[1].color = (0.3, 0.3, 0.3, 1)
    
    mat_batu.node_tree.links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])
    mat_batu.node_tree.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    mat_batu.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    bpy.ops.object.light_add(type='AREA', location=(0,0, 4.5))
    lamp = bpy.context.active_object
    lamp.data.energy = 100
    lamp.data.color = (1.0, 0.8, 0.4)
    lamp.parent = tower_grp

    bpy.ops.object.select_all(action='DESELECT')
    tower_grp.select_set(True)
    bpy.context.view_layer.objects.active = tower_grp
    print("Archer Tower  Selesai Dibuat!")

create_archer_tower()
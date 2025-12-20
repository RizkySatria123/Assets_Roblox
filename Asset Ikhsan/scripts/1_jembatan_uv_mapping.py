import bpy

obj = bpy.context.active_object

if obj and obj.type == 'MESH':
    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Smart UV Project
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.03)
    
    bpy.ops.object.mode_set(mode='OBJECT')
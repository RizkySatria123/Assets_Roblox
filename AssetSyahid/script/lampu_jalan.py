import bpy
import math

def create_material(name, color, metallic=0.0, roughness=0.5, emission_strength=0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        if emission_strength > 0:
            bsdf.inputs['Emission Color'].default_value = (1, 1, 0.8, 1)
            bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

def create_street_light():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    mat_tiang = create_material("Mat_Logam", (0.4, 0.4, 0.4, 1.0), metallic=1.0, roughness=0.2, emission_strength=0)
    mat_lampu = create_material("Mat Kap", (0.9, 0.9, 0.95, 1.0), metallic=0.95, roughness=0.1, emission_strength=0)
    mat_outer = create_material("Mat_Outer", (0.7, 0.7, 0.7, 1.0), metallic=0.0, roughness=0.8, emission_strength=0)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=6, location=(0, 0, 3))
    pole = bpy.context.active_object
    pole.data.materials.append(mat_tiang)
    pole.name = "Tiang_Utama"

    curve_data = bpy.data.curves.new('LenganCurve', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.fill_mode = 'FULL'
    curve_data.bevel_depth = 0.06
    curve_data.bevel_resolution = 4

    polyline = curve_data.splines.new('BEZIER')
    polyline.bezier_points.add(1)

    p0 = polyline.bezier_points[0]
    p0.co = (0, 0, 5.5)
    p0.handle_right = (0, 0, 6.2)

    p1 = polyline.bezier_points[1]
    p1.co = (2.2, 0, 6.2)
    p1.handle_left = (1.0, 0, 6.2)

    arm_obj = bpy.data.objects.new('Lengan_Bengkok', curve_data)
    bpy.context.collection.objects.link(arm_obj)
    arm_obj.data.materials.append(mat_tiang)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.4, 0, 6.16))
    lamp_outer = bpy.context.active_object
    lamp_outer.name = "Kap_Lampu_Outer"
    lamp_outer.scale = (1.0, 0.5, 0.15)
    subsurf_outer = lamp_outer.modifiers.new(name="Mulus", type='SUBSURF')
    subsurf_outer.levels = 3
    subsurf_outer.render_levels = 3
    bpy.ops.object.shade_smooth()
    lamp_outer.rotation_euler[1] = math.radians(10)
    lamp_outer.data.materials.append(mat_outer)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.4, 0, 6.14))
    lamp_inner = bpy.context.active_object
    lamp_inner.name = "Kap_Lampu_Inner"
    lamp_inner.scale = (0.90, 0.40, 0.12)
    subsurf_inner = lamp_inner.modifiers.new(name="Mulus", type='SUBSURF')
    subsurf_inner.levels = 3
    subsurf_inner.render_levels = 3
    bpy.ops.object.shade_smooth()
    lamp_inner.rotation_euler[1] = math.radians(10)
    lamp_inner.data.materials.append(mat_lampu)

create_street_light()
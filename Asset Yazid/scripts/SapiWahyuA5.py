import bpy

COLLECTION_NAME = "SapiWahyuA5"
OBJECT_NAME = "Cow"
MESH_NAME = "Cow_Mesh"
UV_LAYER_NAME = "UVMap"
TEX_SIZE = 64.0

def get_uv_rect(x, y, w, h):
    u1 = x / TEX_SIZE
    v1 = 1.0 - ((y + h) / TEX_SIZE)  # Bottom
    u2 = (x + w) / TEX_SIZE
    v2 = 1.0 - (y / TEX_SIZE)  # Top
    return [(u1, v1), (u2, v1), (u2, v2), (u1, v2)]


VERTS = []
FACES = []
LOOP_UVS = []


def add_box(pos, size, uv_map):
    px, py, pz = pos
    sx, sy, sz = size
    start_idx = len(VERTS)

    VERTS.extend([
        (px, py, pz), (px + sx, py, pz), (px + sx, py + sy, pz), (px, py + sy, pz),
        (px, py, pz + sz), (px + sx, py, pz + sz), (px + sx, py + sy, pz + sz), (px, py + sy, pz + sz)
    ])

    # Faces & UVs
    # 1. RIGHT (X-)
    FACES.append((start_idx + 0, start_idx + 3, start_idx + 7, start_idx + 4))
    LOOP_UVS.extend(uv_map['right'])

    # 2. LEFT (X+)
    FACES.append((start_idx + 1, start_idx + 2, start_idx + 6, start_idx + 5))
    LOOP_UVS.extend(uv_map['left'])

    # 3. FRONT (Y-)
    FACES.append((start_idx + 0, start_idx + 1, start_idx + 5, start_idx + 4))
    LOOP_UVS.extend(uv_map['front'])

    # 4. BACK (Y+)
    FACES.append((start_idx + 3, start_idx + 7, start_idx + 6, start_idx + 2))
    LOOP_UVS.extend(uv_map['back'])

    # 5. TOP (Z+)
    FACES.append((start_idx + 4, start_idx + 7, start_idx + 6, start_idx + 5))
    LOOP_UVS.extend(uv_map['top'])

    # 6. BOT (Z-)
    FACES.append((start_idx + 0, start_idx + 1, start_idx + 2, start_idx + 3))
    LOOP_UVS.extend(uv_map['bot'])

def build_cow():
    # HEAD
    head_uv = {
        'right': get_uv_rect(0, 8, 8, 8),
        'front': get_uv_rect(8, 8, 8, 8),
        'left': get_uv_rect(16, 8, 8, 8),
        'back': get_uv_rect(24, 8, 8, 8),
        'top': get_uv_rect(8, 0, 8, 8),
        'bot': get_uv_rect(16, 0, 8, 8)
    }
    add_box((-4, -14, 16), (8, 8, 8), head_uv)

    # BODY (Fix: Padding 1px logic)
    body_uv = {
        'right': get_uv_rect(1, 22, 18, 12),
        'front': get_uv_rect(20, 22, 12, 12),
        'left': get_uv_rect(33, 22, 18, 12),
        'back': get_uv_rect(52, 22, 12, 12),
        'top': get_uv_rect(28, 4, 12, 18),
        'bot': get_uv_rect(40, 4, 12, 18)
    }
    add_box((-6, -9, 12), (12, 18, 10), body_uv)

    # LEGS
    leg_uv = {
        'right': get_uv_rect(0, 20, 4, 12),
        'front': get_uv_rect(4, 20, 4, 12),
        'left': get_uv_rect(8, 20, 4, 12),
        'back': get_uv_rect(12, 20, 4, 12),
        'top': get_uv_rect(4, 16, 4, 4),
        'bot': get_uv_rect(8, 16, 4, 4)
    }
    add_box((-6, 5, 0), (4, 4, 12), leg_uv)  # Back Right
    add_box((-6, -9, 0), (4, 4, 12), leg_uv)  # Front Right
    add_box((2, 5, 0), (4, 4, 12), leg_uv)  # Back Left
    add_box((2, -9, 0), (4, 4, 12), leg_uv)  # Front Left

    # EXTRAS
    horn_uv = {k: get_uv_rect(1, 1, 1, 1) for k in ['right', 'left', 'front', 'back', 'top', 'bot']}
    add_box((-5, -12, 24), (1, 1, 3), horn_uv)
    add_box((4, -12, 24), (1, 1, 3), horn_uv)

    udder_uv = {k: get_uv_rect(52, 0, 1, 1) for k in ['right', 'left', 'front', 'back', 'top', 'bot']}
    add_box((-2, -3, 11), (4, 6, 1), udder_uv)


def main():
    # Cleanup
    if COLLECTION_NAME in bpy.data.collections:
        col = bpy.data.collections[COLLECTION_NAME]
        for obj in col.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(col)

    col = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(col)

    build_cow()

    # Create Mesh
    mesh = bpy.data.meshes.new(MESH_NAME)
    obj = bpy.data.objects.new(OBJECT_NAME, mesh)
    col.objects.link(obj)

    mesh.from_pydata(VERTS, [], FACES)

    # Apply UVs
    if len(LOOP_UVS) == len(mesh.loops):
        uv_layer = mesh.uv_layers.new(name=UV_LAYER_NAME)
        for i, loop in enumerate(mesh.loops):
            uv_layer.data[i].uv = LOOP_UVS[i]

    mat = bpy.data.materials.new("Cow_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (300, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Roughness'].default_value = 1.0

    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    mesh.materials.append(mat)

    mesh.validate(verbose=False)
    mesh.update()

    # Select Object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    print("Cow Generated! Material siap (tanpa node image).")


if __name__ == "__main__":
    main()
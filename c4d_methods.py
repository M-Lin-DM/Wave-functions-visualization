import c4d
import numpy as np


def get_reference_mat(mat_name, doc):
    for i, m in enumerate(doc.GetMaterials()):
        if m.GetName() == mat_name:
            return m


def insert_object(o, doc, name_to_index_dict):
    # INSTANTIATE OBJECT
    if o.obj_type == 'sphere':
        obj = c4d.BaseObject(c4d.Osphere)  # Create new sphere
        obj[c4d.PRIM_SPHERE_SUB] = o.segments  # controls mesh density on surface of object
        obj[c4d.PRIM_SPHERE_RAD] = o.radius
    elif o.obj_type == 'cube':
        obj = c4d.BaseObject(c4d.Ocube)
        obj[c4d.PRIM_CUBE_LEN] = c4d.Vector(o.length, o.length, o.length)
    elif o.obj_type == 'tetrahedron':
        obj = c4d.BaseObject(c4d.Oplatonic)
        obj[c4d.PRIM_PLATONIC_TYPE] = 0
        obj[c4d.PRIM_PLATONIC_RAD] = o.radius

    # Name
    name = f'{o.id}'
    obj[c4d.ID_BASELIST_NAME] = name
    name_to_index_dict[name] = (
    o.i, o.j)  # modify dict containing object metadata. in this case, its indices in the grid

    # POSITION
    obj.SetRelPos(c4d.Vector(o.px, o.py, o.pz))  # Set position of obj

    # SCALE
    obj.SetRelScale(c4d.Vector(o.sx, o.sy, o.sz))

    # ROTATION
    obj.SetRelRot(c4d.Vector(o.ry, o.rx, o.rz))  # this is the correct rotation order for HPB

    # create material
    mat = c4d.Material()  # must use doc to insert mat
    mat.SetName(f'mat_{o.id}')

    # MODIFY MATERIAL -- # remove any of these that work by default
    mat[c4d.MATERIAL_USE_COLOR] = True
    mat[c4d.MATERIAL_USE_LUMINANCE] = False
    mat[c4d.MATERIAL_USE_REFLECTION] = False

    # COLOR
    mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(o.R, o.G, o.B)

    doc.InsertMaterial(mat, None)

    # create tag
    texture_tag = c4d.TextureTag()
    texture_tag.SetMaterial(mat)  # attach a certain material to this tag

    obj.InsertTag(texture_tag)  # attach tag containing material to object
    doc.InsertObject(obj)  # Insert object in document

    return name_to_index_dict  # may not be necessary


def remove_objects(doc):
    # Get a list of all objects in the document
    objects = doc.GetObjects()
    for obj in objects:
        if obj.GetType() == c4d.Osphere or obj.GetType() == c4d.Oplatonic or obj.GetType() == c4d.Ocube:
            obj.Remove()  # Delete object


def modify_objects(doc, attr_dict, name_to_index_dict):
    print('modifying the objects')
    objects = doc.GetObjects()
    materials = doc.GetMaterials()
    for obj, mat in zip(objects, materials):
        if obj.GetType() == c4d.Osphere or obj.GetType() == c4d.Oplatonic or obj.GetType() == c4d.Ocube:
            i, j = name_to_index_dict[obj[c4d.ID_BASELIST_NAME]]
            # SCALE
            obj.SetRelScale(c4d.Vector(attr_dict['sx'][i, j], attr_dict['sy'][i, j], attr_dict['sz'][i, j]))

            # ROTATION
            obj.SetRelRot(c4d.Vector(attr_dict['ry'][i, j], attr_dict['rx'][i, j],
                                     attr_dict['rz'][i, j]))  # this is the correct rotation order for HPB
            # COLOR
            mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(attr_dict['R'][i, j], attr_dict['G'][i, j], attr_dict['B'][i, j])


def camera_position(k, min_percent, max_percent, params):
    # this outputs the percentage (along a spline path) corresponding to frame t
    position_range = np.linspace(min_percent, max_percent, params['N_frames'])
    return position_range[k]

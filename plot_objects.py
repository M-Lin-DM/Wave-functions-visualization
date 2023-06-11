from typing import Optional
import c4d
import numpy as np
from generate_waves import Tetrahedron, Cube, compute_attribute_arrays
from utils import get_random_base_color, polar_wave, constant
from c4d_methods import insert_object, remove_objects, get_reference_mat, modify_objects, camera_position

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

params = dict()

grid_size_factor = 3
params['grid_length'] = int(16 * grid_size_factor)  # number of grid points
params['grid_height'] = int(9 * grid_size_factor)
params['plot_height'] = 4 * np.pi  # actual graph space
params['plot_length'] = params['plot_height'] * 16 / 9

# video params
params['fps'] = 30
params['video_duration'] = 5  # secs
params['N_frames'] = int(params['video_duration'] * params['fps'])
params['dpi'] = 120

# wave function params
# scale params
params['s_A'] = 1 / grid_size_factor * 2.6
params['s_w'] = 0.8
params['s_v'] = 0.03
params['s_b'] = 0.5  # osc about 0 doubles the spatial freq

# rotation params
params['r_A'] = 1
params['r_w'] = 1
params['r_v'] = 0.04
params['r_b'] = 0

# color params
params['base_color'] = get_random_base_color() + 0.1
params['c_A'] = 0.4
params['c_w'] = 1
params['c_v'] = 0.02
params['c_b'] = 0.5

# define attribute functions. Turn off functions here not in loop---------------------
func_dict = {}
func_dict['sx'] = lambda r, theta, t: params['s_A'] * np.sin(4*theta*params['s_w'] - params['s_v']*t)
func_dict['sy'] = lambda r, theta, t: params['s_A'] * np.sin(3*theta*params['s_w'] - params['s_v']*t)
func_dict['sz'] = lambda r, theta, t: params['s_A'] * np.sin(2*theta*params['s_w'] - params['s_v']*t)
#func_dict['sy'] = func_dict['sx']
#func_dict['sz'] = func_dict['sx']

#func_dict['sy'] = constant(params['s_A'])
#func_dict['sz'] = constant(params['s_A'])

# rotation
func_dict['ry'] = polar_wave(params['r_A'], params['r_w'], params['r_v'], params['r_b'])
func_dict['rx'] = polar_wave(params['r_A'], 1.2*params['r_w'], params['r_v'], params['r_b'])
func_dict['rz'] = polar_wave(0.7*params['r_A'], 0.5*params['r_w'], 1.5*params['r_v'], params['r_b'])

#func_dict['ry'] = constant(0)
#func_dict['rx'] = constant(0)
#func_dict['rz'] = constant(0)

# for uniform color:
base_color = params['base_color']
#func_dict['R'] = constant(base_color[0])
#func_dict['G'] = constant(base_color[1])
#func_dict['B'] = constant(base_color[2])

# for color waves:
func_dict['R'] = lambda r, theta, t: params['c_A'] * np.cos(5*theta*params['c_w'] - params['c_v']*t) + params['c_b']
func_dict['G'] = lambda r, theta, t: params['c_A'] * np.cos(4*theta*params['c_w'] - params['c_v']*t) + params['c_b']
func_dict['B'] = polar_wave(params['c_A'], params['c_w'], params['c_v'], params['c_b'])


def main() -> None:
    doc = c4d.documents.GetActiveDocument()
    save_path = 'C:/Users/MrLin/OneDrive/COMPLEX OBJECTS/PROJECTS/RIPPLES/JUPYTER NOTEBOOK/movies/image stack/'
    render_data = doc.GetActiveRenderData()

    # make bitmap
    bmp = c4d.bitmaps.BaseBitmap()
    bmp.Init(int(render_data[c4d.RDATA_XRES]), int(render_data[c4d.RDATA_YRES]), depth=24)

    frame_dict, r, theta, xx, yy = compute_attribute_arrays(params, func_dict)
    print('inserting objects')
    c = 0
    name_to_index_dict = {}

    bd = doc.GetActiveBaseDraw()  # Get active base draw
    activeCam = bd.GetSceneCamera(doc)  # Get active camera
    tags = activeCam.GetTags()  # get camera tags

    # only works with target camera following a spline:
    for g in tags:
        if g.GetType() == 5699:  # align to spline tag
            align_to_spline = g

    remove_objects(doc)

    for t in range(params['N_frames']):
        # adjust save path in render data
        render_data[
            c4d.RDATA_PATH] = f'{save_path}img_{t}.png'

        # Adjust cam position on path. Comment off if using fixed camera
        # align_to_spline[c4d.ALIGNTOSPLINETAG_POSITION] = camera_position(t, 0.25 - 0.02, 0.25+0.02, params)  # max range is 0.19, 0.31,

        attr_dict = frame_dict[str(t)]
        if t == 0:
            for i in range(params['grid_height']):
                for j in range(params['grid_length']):
                    obj = Tetrahedron()
                    obj.i = i
                    obj.j = j
                    obj.id = c  # defines the object's name, which will be used to link it to its location in the grid
                    c += 1

                    obj.px = 10 * xx[i, j]
                    obj.pz = 10 * yy[i, j]

                    obj.sx = attr_dict['sx'][i, j]
                    obj.sy = attr_dict['sy'][i, j]
                    obj.sz = attr_dict['sz'][i, j]

                    obj.rx = attr_dict['rx'][i, j]
                    obj.ry = attr_dict['ry'][i, j]
                    obj.rz = attr_dict['rz'][i, j]

                    # color
                    obj.R = attr_dict['R'][i, j]
                    obj.G = attr_dict['G'][i, j]
                    obj.B = attr_dict['B'][i, j]

                    name_to_index_dict = insert_object(obj, doc, name_to_index_dict)

            c4d.EventAdd()
        else:
            modify_objects(doc, attr_dict, name_to_index_dict)
            c4d.EventAdd()

        print('Rendering')
        if c4d.documents.RenderDocument(doc, render_data.GetData(), bmp,
                                        c4d.RENDERFLAGS_EXTERNAL) != c4d.RENDERRESULT_OK:
            raise RuntimeError("Failed to render the temporary document.")


if __name__ == '__main__':
    main()
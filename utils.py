import numpy as np


def normalize_vectors(vectors):
    # Calculate the length of each vector
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)

    # Normalize each vector by dividing it by its length
    normalized_vectors = vectors / norms

    return normalized_vectors


def dict_to_obj_list(obj_dict):
    # collapses dict of lists into a single list
    obj_list = []
    for key in obj_dict:
        obj_list.extend(obj_dict[key])
    return obj_list


def points_on_sphere(n):
    # points spread over the unit sphere. Note these are not uniformly distributed. The corners have slightly higher density due to sampling from the unit cube..
    return normalize_vectors(np.random.rand(n, 3) - 0.5)


def point_on_sphere_array(n):
    return np.repeat(points_on_sphere(1), n, axis=0)  # array of repeated single vector lying on surface of unit sphere


def points_on_sphere_cropped(n, v, theta):
    # n points spread over the unit sphere. we remove points pointed away from v beyond an angle theta
    points = points_on_sphere(n * 10)
    v_arr = normalize_vectors(np.repeat(v, n * 10, axis=0))
    dot_product = np.sum(points * v_arr, 1)

    angle = np.arccos(dot_product)
    points = points[angle < theta, :]  # remove points with angle greater than theta
    points = points[:n, :]  # take only n points

    return points


def constant_array(arr, n):
    return np.repeat(arr, n, axis=0)


def get_random_base_color():
    base_color = np.random.rand(3)
    base_color += 0.05
    base_color = np.clip(base_color, 0.1, 0.9)
    return base_color


def new_child_id():
    return float(np.random.rand(1))


def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def cartesian_to_polar(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)
    return r, theta


def polar_wave(A, w, v, b):
    # returns a function parametrized by the inputs but it accepts the array of coordinates and time
    def f(r, theta, t):
        # returns an array given arrays r and theta and scalar t
        return A * np.sin(r * w - v * t) + b

    return f


def constant(value):
    def f(r, theta, t):
        return np.ones_like(r) * value

    return f

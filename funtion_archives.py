func_dict['sx'] = lambda r, theta, t: 0.5 * np.sin(theta * params['s_w'] - 0.7 * params['s_v'] * t) + 0.5 * np.cos(
    r * params['s_w'] - 0.7 * params['s_v'] * t)

func_dict['ry'] = lambda r, theta, t: 0.6 * np.cos(theta * params['r_w'] - 0.4 * params['r_v'] * t) + np.sin(
    r * params['r_w'] - 0.4 * params['r_v'] * t)


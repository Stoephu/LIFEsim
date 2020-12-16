import warnings

import numpy as np
import pandas as pd


def single_habitable_zone(model: str,
                          temp_s: float,
                          radius_s: float):

    # TODO which paper is this model based on?
    if model == 'MS':
        s0_in, s0_out = 1.7665, 0.3240
        a_in, a_out = 1.3351E-4, 5.3221E-5
        b_in, b_out = 3.1515E-9, 1.4288E-9
        c_in, c_out = -3.3488E-12, -1.1049E-12
    elif model == 'POST-MS':
        s0_in, s0_out = 1.1066, 0.3240
        a_in, a_out = 1.2181E-4, 5.3221E-5
        b_in, b_out = 1.5340E-8, 1.4288E-9
        c_in, c_out = -1.5018E-12, -1.1049E-12
    else:
        raise ValueError('Unknown model')

    t_star = temp_s - 5780

    # in units of incoming flux, normalized to stellar flux on earth_0
    s_in = s0_in + a_in * t_star + b_in * t_star ** 2 + c_in * t_star ** 3
    s_out = s0_out + a_out * t_star + b_out * t_star ** 2 + c_out * t_star ** 3
    l_sun = radius_s ** 2 * (temp_s / 5780) ** 4  # luminosity in L_sun

    hz_in = np.sqrt(l_sun / s_in)  # HZ inner boundery in AU
    hz_out = np.sqrt(l_sun / s_out)  # HZ outer boundery in AU
    hz_center = (hz_in + hz_out) / 2  # HZ center  in AU

    return s_in, s_out, l_sun, hz_in, hz_out, hz_center
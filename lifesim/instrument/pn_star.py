import numpy as np

from lifesim.dataio.bus import Module
from lifesim.dataio.catalog import Catalog
from lifesim.instrument.transmission import fast_transmission
from lifesim.modules.util import black_body


def get_stellar_leakage(radius_s: float,
                        distance_s: float,
                        temp_s: float,
                        bl: float,
                        wl_bins: np.ndarray,
                        wl_edges: np.ndarray,
                        image_size: int = 50,
                        map_selection: str = 'tm3'):
    if map_selection not in ['tm1', 'tm2', 'tm3', 'tm4']:
        raise ValueError('Nonexistent transmission map')

    Rs_au = 0.00465047 * radius_s
    Rs_mas = Rs_au / distance_s * 1000
    Rs_mas = float(Rs_mas)

    # TODO Instead of recalculating the transmission map for the stelar radius here, one could try
    #   to reuse the inner part of the transmission map already calculated in the get_snr function
    #   of the instrument class
    tm_star = fast_transmission(wl=wl_bins,
                                hfov_mas=Rs_mas,
                                image_size=image_size,
                                bl=bl,
                                map_selection=[map_selection])[int(map_selection[-1]) - 1]

    x_map = np.tile(np.array(range(0, image_size)), (image_size, 1))
    y_map = x_map.T
    r_square_map = (x_map - (image_size - 1) / 2) ** 2 + (y_map - (image_size - 1) / 2) ** 2
    star_px = np.where(r_square_map < (image_size / 2) ** 2, 1, 0)

    sl = (star_px * tm_star).sum(axis=(-2, -1)) / star_px.sum(
    ) * black_body(wl=wl_edges,
                   temp=temp_s,
                   radius=radius_s,
                   distance=distance_s,
                   mode='star')
    return sl


class PhotonNoiseStar(Module):
    def __init__(self,
                 name: str):
        super().__init__(name=name)
        self.f_type = 'photon_noise'
        self.noise = None

    def run(self):
        mask = self.data['c'].data.nstar == self.data['nstar']
        self.noise = get_stellar_leakage(radius_s=self.data['c'].data.radius_s[mask].to_numpy()[0],
                                         distance_s=self.data['c'].data.distance_s[mask].to_numpy()[0],
                                         temp_s=self.data['c'].data.temp_s[mask].to_numpy()[0],
                                         bl=self.data['bl'],
                                         wl_bins=self.data['wl_bins'],
                                         wl_edges=self.data['wl_edges'])

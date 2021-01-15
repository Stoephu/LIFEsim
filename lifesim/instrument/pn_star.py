from typing import Union

import numpy as np

from lifesim.core.modules import PhotonNoiseModule, TransmissionModule
from lifesim.util.radiation import black_body


class PhotonNoiseStar(PhotonNoiseModule):

    def __init__(self,
                 name: str):
        super().__init__(name=name)
        self.add_socket(s_name='transmission_star',
                        s_type=TransmissionModule)

    def noise(self,
              index: Union[int, type(None)]):
        """
        Simulates the amount of photon noise originating from the star of the observed system leaking
        into the LIFE array measurement

        Parameters
        ----------
        image_size : int
            Number of pixels on one axis of a square detector (dimensionless). I.e. for a 512x512
            detector this value is 512
        telescope_area : float
            Area of all array apertures combined in [m^2]
        wl_bins : np.ndarray
            Central values of the spectral bins in the wavelength regime in [m]
        wl_bin_widths : np.ndarray
            Widths of the spectral wavelength bins in [m]
        distance_s : float
            Distance between the observed star and the LIFE array in [pc]
        temp_s : float
            Temperature of the observed star in [K]
        radius_s : float
            Radius of the observed star in [sun radii]
        bl : float
            Length of the shorter, nulling baseline in [m]
        map_selection : str
            Select from which mode of the array the transmission map for the calculation of the leakage
            is taken
        ratio : float
            Ratio between the nulling and the imaging baseline. E.g. if the imaging baseline is twice
            as long as the nulling baseline, the ratio will be 2

        Returns
        -------
        sl_leak
            Stellar light leakage in [s^-1] per wavelength bin

        Raises
        ______

        ValueError
            If the specified transmission map does not exits
        """

        image_size = 50
        map_selection = 'tm3'

        if index is None:
            radius_s = self.data.single['radius_s']
            distance_s = self.data.single['distance_s']
            temp_s = self.data.single['temp_s']
        else:
            radius_s = self.data.catalog.radius_s.iloc[index]
            distance_s = self.data.catalog.distance_s.iloc[index]
            temp_s = self.data.catalog.temp_s.iloc[index]

        # check if the specified map exists
        if map_selection not in ['tm1', 'tm2', 'tm3', 'tm4']:
            raise ValueError('Nonexistent transmission map')

        # convert units
        Rs_au = 0.00465047 * radius_s
        Rs_as = Rs_au / distance_s
        Rs_mas = float(Rs_as)
        Rs_rad = Rs_mas / (3600. * 180.) * np.pi

        # TODO Instead of recalculating the transmission map for the stellar radius here, one could try
        #   to reuse the inner part of the transmission map already calculated in the get_snr function
        #   of the instrument class
        # TODO: why are we not reusing the maps calculated in the instrument class
        tm_star = self.run_socket(method='transmission_map',
                                  s_name='transmission_star',
                                  map_selection=[map_selection],
                                  hfov=Rs_rad,
                                  image_size=image_size)[int(map_selection[-1]) - 1]

        x_map = np.tile(np.array(range(0, image_size)), (image_size, 1))
        y_map = x_map.T
        r_square_map = (x_map - (image_size - 1) / 2) ** 2 + (y_map - (image_size - 1) / 2) ** 2
        star_px = np.where(r_square_map < (image_size / 2) ** 2, 1, 0)

        # get the stellar leakage
        sl_leak = (star_px * tm_star).sum(axis=(-2, -1)) / star_px.sum(
        ) * black_body(bins=self.data.inst['wl_bins'],
                       width=self.data.inst['wl_bin_widths'],
                       temp=temp_s,
                       radius=radius_s,
                       distance=distance_s,
                       mode='star') * self.data.inst['telescope_area']

        return sl_leak

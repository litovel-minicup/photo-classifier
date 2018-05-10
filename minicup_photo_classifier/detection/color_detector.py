# coding=utf-8

import logging
from typing import Optional

import numpy as np

from ..utils.color import RGBColor


class ColorDetector(object):
    """
    Gets image and position in image and returns "average" color from local neighborhood.
    Probably only from maximum peak in color model.
    """

    WINDOW_HALF_SIZE = 3, 3
    WINDOW_HALF_SIZE_X, WINDOW_HALF_SIZE_Y = WINDOW_HALF_SIZE

    def detect_color(self, image: np.ndarray, position: np.ndarray) -> Optional[RGBColor]:
        """
        With little bit magic returns "average" color of masked part of image.
        """
        assert image.ndim == 3 and image.shape[2] == 3, "Image as RGB bitmap."
        assert position.ndim == 1 and position.shape[0] == 2, "Position as [x, y]."
        y, x = position
        if not (0 <= x < image.shape[1]) or not (0 <= y < image.shape[0]):
            logging.info('Skipping {}, position is not in image.'.format(position))
            return None
        image_height, image_width, _ = image.shape

        window = image[
                 max((
                     x - self.WINDOW_HALF_SIZE_X,
                     0
                 ))
                 :
                 min((
                     x + self.WINDOW_HALF_SIZE_X + 1,
                     image_width - 1
                 )),
                 max((
                     y - self.WINDOW_HALF_SIZE_Y,
                     0
                 ))
                 :
                 min((
                     y + self.WINDOW_HALF_SIZE_Y + 1,
                     image_height - 1
                 )),
                 ]
        if not window.size:
            logging.warning('Empty window.')
            return None

        return RGBColor(*np.nanmean(window, axis=(0, 1)).astype(int))


__all__ = ['ColorDetector']

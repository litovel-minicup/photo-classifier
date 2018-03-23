# coding=utf-8

import numpy

from ..typing_ import RGBColor


class ColorDetector(object):
    """
    Gets image&mask and returns "average" color value - in normal RGB space.
    Probably only from maximum peak in color model.
    """

    def __init__(self):
        # TODO: configuration parameters (threshold/gamma)
        pass

    def detect_color(self, image: numpy.ndarray, mask: numpy.ndarray) -> RGBColor:
        """
        With little bit magic returns "average" color of masked part of image.
        """
        return RGBColor(255, 0, 0)


__all__ = ['ColorDetector']

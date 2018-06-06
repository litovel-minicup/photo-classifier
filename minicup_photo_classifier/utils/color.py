# coding=utf-8
import colorsys
from typing import NamedTuple


class RGBColor(NamedTuple('RGBColor', [('red', float), ('green', float), ('blue', float)])):
    @property
    def as_hsv(self):
        return HSVColor(*colorsys.rgb_to_hsv(*self))


class HSVColor(NamedTuple('HSVColor', [('hue', float), ('value', float), ('saturation', float)])):

    def is_in_hue_range(self, first: "HSVColor", second: "HSVColor", range_help=.005):
        """

        :param range_help: constant to make range bigger
        :param first: first color in range
        :param second: second color in range
        :return: is self in range?
        """

        from_hue, to_hue = sorted((first.hue, second.hue))
        inner_range_size = to_hue - from_hue
        if inner_range_size < 0.5:  # inner interval
            if not ((from_hue - range_help) <= self.hue <= (to_hue + range_help)):
                return False
        else:  # circle interval
            if not ((0. <= self.hue <= from_hue + range_help) or (to_hue - range_help <= self.hue <= 1.)):
                return False

        return True

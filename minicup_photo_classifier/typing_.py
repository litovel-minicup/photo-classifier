# coding=utf-8
from typing import NamedTuple

RGBColor = NamedTuple('RGBColor', [('red', float), ('green', float), ('blue', float)])
HSVColor = NamedTuple('RGBColor', [('hue', float), ('saturation', float), ('blue', float)])

__all__ = [
    'RGBColor',
    'HSVColor',

]

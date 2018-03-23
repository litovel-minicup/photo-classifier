# coding=utf-8
from typing import Tuple

from minicup_photo_classifier.typing_ import RGBColor


class BucketSelector(object):
    """
    From RGB color and configurations parameter resolves hue ans value from HSL colorspace.
    (see import https://docs.python.org/3.5/library/colorsys.html)
    After that, hue is quantized into one of N defined buckets.
    Value has threshold to detect black/non black colors.
    # TODO: what about behaviour of saturation same like Value?
    """

    def __init__(self):
        pass
        # TODO: set bucket count, value threshold

    def select_buckets(self, color: RGBColor) -> Tuple[int, int, int]:
        # TODO: import colorsys
        # TODO: what about rescaling to maximal range - but from what values?

        return 0, 0, 0


__all__ = ['BucketSelector']

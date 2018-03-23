# coding=utf-8
from typing import List

import numpy


class ObjectDetector(object):
    """
    Class for detecting biggest and main objects in image.
    """

    def __init__(self):
        # TODO: some configuration
        pass

    def detect_objects(self, image: numpy.ndarray) -> List[numpy.ndarray]:
        # TODO: detect objects in image and return them as list of masks
        return [
            numpy.array(range(42))
        ]


__all__ = ['ObjectDetector']

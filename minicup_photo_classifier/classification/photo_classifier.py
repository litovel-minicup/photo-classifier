# coding=utf-8
import logging
from datetime import datetime
from typing import Optional

import cv2
from PIL import Image

from ..detection.color_detector import ColorDetector


class PhotoClassifier(object):
    """
    Gets photo as file and tries to process into TeamInfo classes.
    """

    EXIF_DATETIME_INDEX = 36867
    OBJECT_DETECTOR_PICKLED = 'object-detector.pickled'

    def __init__(self):
        pass

        # TODO: load teams info from db

        # if exists(self.OBJECT_DETECTOR_PICKLED):
        #     self._object_detector = pickle.load(open(self.OBJECT_DETECTOR_PICKLED, 'rb'))
        # else:
        from ..detection.object_detector import ObjectDetector
        self._object_detector = ObjectDetector()
        # pickle.dump(self._object_detector, open(self.OBJECT_DETECTOR_PICKLED, 'wb'))

        self._color_detector = ColorDetector()

    def process(self, image_path: str):
        taken = self._photo_taken(image_path)
        image = cv2.imread(image_path)
        image = cv2.resize(image, (0, 0), fx=.5, fy=.5)[:, :, ::-1]

        peoples = self._object_detector.detect_objects(image=image)

        colors = set()
        for people in peoples:
            for position in people:
                if not any(position):
                    continue
                color = self._color_detector.detect_color(image=image, position=position)
                if color is None:
                    continue
                colors.add(color)
        logging.debug(colors)

        # TODO: process whole pipeline from detection to classification
        # TODO: successfully classified photos upload to API and save tags via another class
        # TODO: think about GUI with image class correction by user

    def _photo_taken(self, path: str) -> Optional[datetime]:
        # TODO: optimalization
        exif = Image.open(path)._getexif()
        if not exif:
            return None

        taken = exif.get(self.EXIF_DATETIME_INDEX) or exif.get(306)
        if not taken:
            return None

        return datetime.strptime(
            taken,
            "%Y:%m:%d %H:%M:%S"
        )


__all__ = ['PhotoClassifier']

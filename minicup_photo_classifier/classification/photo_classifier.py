# coding=utf-8
import logging
from datetime import datetime
from typing import Optional

import cv2
from PIL import Image

from minicup_administration.core.models import TeamInfo
from minicup_photo_classifier.classification.time_team_selector import TeamByMatchTimeFinder
from minicup_photo_classifier.utils.color import RGBColor
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
        self._time_team_selector = TeamByMatchTimeFinder(None)

    def process(self, image_path: str):
        taken = self._photo_taken(image_path)
        image = cv2.imread(image_path)
        image = cv2.resize(image, (0, 0), fx=.5, fy=.5)[:, :, ::-1]

        peoples = self._object_detector.detect_objects(image=image)

        colors = dict()
        for people in peoples:
            for position in people:
                x, y = position
                if not any(position):
                    continue
                color = self._color_detector.detect_color(image=image, position=position)
                if color is None:
                    continue
                colors[(x, y)] = color

        logging.debug(colors)
        # self._show_markers(image, colors)

        possible_teams = TeamInfo.objects.filter(category__slug='mladsi', category__year__slug='2018')
        for team in possible_teams:  # type: TeamInfo
            if not (team.dress_color_min and team.dress_color_max):
                logging.debug('Skipping team {}.'.format(team))
                continue

            from_, to = map(self.hex_to_rgb, (team.dress_color_min, team.dress_color_max))

            logging.debug('Testing to team {}.'.format(team))
            for marker_color in colors.values():

                if marker_color.in_range(from_, to):
                    logging.debug('Color match with {}.'.format(marker_color))

        # TODO: process whole pipeline from detection to classification
        # TODO: successfully classified photos upload to API and save tags via another class
        # TODO: think about GUI with image class correction by user

    def _show_markers(self, image, colors):
        from matplotlib import pyplot as plt
        import numpy as np

        plt.imshow(image)

        for (x, y), color in colors.items():
            plt.plot(
                [x],
                [y],
                marker='o',
                markersize=sum(self._color_detector.WINDOW_HALF_SIZE),
                color=np.asarray(color) / 255,
                mew=.2,
                mec='black'
            )
        plt.show()

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

    @staticmethod
    def hex_to_rgb(color: str) -> RGBColor:
        return RGBColor(
            *tuple(
                int(color.lstrip('#')[i:i + 2], 16)
                for i in range(3)
            )
        )


__all__ = ['PhotoClassifier']

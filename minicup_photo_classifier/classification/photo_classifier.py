# coding=utf-8
import colorsys
import logging
from collections import OrderedDict
from datetime import datetime
from typing import Optional

import cv2
from PIL import Image

from minicup_administration.core.models import TeamInfo, Match, Category
from minicup_photo_classifier.classification.time_team_selector import TeamByMatchTimeFinder
from minicup_photo_classifier.utils.color import HSVColor, RGBColor
from ..detection.color_detector import ColorDetector


class PhotoClassifier(object):
    """
    Gets photo as file and tries to process into TeamInfo classes.
    """

    EXIF_DATETIME_INDEXES = 36867, 36868, 306
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
        self._time_team_selector = TeamByMatchTimeFinder(Category.objects.filter(slug='mladsi', year__slug='2017').first())

    def process(self, image_path: str):
        taken = self._photo_taken(image_path)
        image = cv2.imread(image_path)
        image = cv2.resize(image, (0, 0), fx=.5, fy=.5)[:, :, ::-1]
        # image = cv2.equalizeHist(image)

        peoples = self._object_detector.detect_objects(image=image)

        # extract all colors
        colors = OrderedDict()
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
        # self._debug_show_markers(image, colors)

        for teams in self._time_team_selector.find_possible_teams(taken=taken):
            logging.debug('Is photo from {}?.'.format(teams))
            for team in teams:  # type: TeamInfo
                if not (team.dress_color_min and team.dress_color_max):
                    logging.debug('Skipping team {}.'.format(team))
                    continue

                from_, to = map(
                    self.hue_to_hsv,
                    (team.dress_color_min, team.dress_color_max)
                )  # type: HSVColor, HSVColor

                logging.debug('Testing to team {} with range {:.3f} - {:.2f}.'.format(team, from_.hue, to.hue))

                for marker_color in colors.values():
                    if marker_color.as_hsv.is_in_hue_range(from_, to):
                        logging.debug('Color match with {:.3f}.'.format(marker_color.as_hsv.hue))
                        continue

                    logging.debug('Color does not match with {:.3f}.'.format(marker_color.as_hsv.hue))

        # TODO: process whole pipeline from detection to classification
        # TODO: successfully classified photos upload to API and save tags via another class
        # TODO: think about GUI with image class correction by user

    def _debug_show_markers(self, image, colors):
        from matplotlib import pyplot as plt
        import numpy as np

        plt.imshow(image)

        for (x, y), color in colors.items():
            plt.plot(
                [x],
                [y],
                marker='o',
                markersize=sum(self._color_detector.WINDOW_HALF_SIZE),
                color=np.asarray(color),
                mew=.2,
                mec='black'
            )
        plt.show()

    def _photo_taken(self, path: str) -> Optional[datetime]:
        # TODO: optimalization
        exif = Image.open(path)._getexif()
        if not exif:
            return None

        possible = tuple(filter(None, (exif.get(i) for i in self.EXIF_DATETIME_INDEXES)))
        if not possible:
            return None

        return datetime.strptime(
            possible[0],
            "%Y:%m:%d %H:%M:%S"
        )

    @staticmethod
    def hue_to_hsv(color: str) -> RGBColor:
        return HSVColor(
            int(color) / 360.,
            1.,
            1.,
        )


__all__ = ['PhotoClassifier']

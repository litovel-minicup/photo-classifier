# coding=utf-8
import logging
from datetime import datetime
from typing import Iterable

from minicup_administration.core.models import Category, TeamInfo


class TeamByMatchTimeFinder(object):
    """
    Tries find possible teams  in category playing in given time.
    """

    def __init__(self, category: Category):
        self._category = category

    def find_possible_teams(self, taken: datetime) -> Iterable[TeamInfo]:
        """
        Returns possible teams playing in given time.
        :param taken: time to detect
        :return: possible teams
        """
        if taken > datetime.now():
            logging.warning('Future taken date: {}.'.format(taken))

        return self._category.match_category.filter(
            match_term__start__time__lte=taken.time(),
            match_term__end__time__gte=taken.time(),
            match_term__day__date=taken.date(),
        )


__all__ = ['TeamByMatchTimeFinder']

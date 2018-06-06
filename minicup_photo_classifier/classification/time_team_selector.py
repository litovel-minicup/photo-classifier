# coding=utf-8
import logging
from datetime import datetime, timedelta
from typing import Iterable

from minicup_administration.core.models import Category, TeamInfo, Match, MatchTerm


class TeamByMatchTimeFinder(object):
    """
    Tries find possible teams  in category playing in given time.
    """

    def __init__(self, category: Category):
        self._category = category

    def find_possible_teams(self, taken: datetime) -> Iterable[Iterable[TeamInfo]]:
        """
        Returns possible teams playing in given time.
        :param taken: time to detect
        :return: possible teams
        """
        if taken > datetime.now():
            logging.warning('Future taken date: {}.'.format(taken))

        matches = self._category.match_category.filter(
            match_term__start__time__range=(
                (taken - MatchTerm.STANDARD_LENGTH).time(),
                taken.time()
            ),
            match_term__day__day=taken.date(),
        )  # type: Iterable[Match]
        return tuple((match.home_team_info, match.away_team_info) for match in matches)


__all__ = ['TeamByMatchTimeFinder']

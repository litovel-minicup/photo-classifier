# coding=utf-8
from functools import total_ordering
from typing import NamedTuple


@total_ordering
class RGBColor(NamedTuple('RGBColor', [('red', float), ('green', float), ('blue', float)])):
    pass

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return self == other

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()

        return all(s > o for s, o in zip(self, other))

    def __hash__(self):
        return super().__hash__()

    def in_range(self, first, second):
        for my, *parts in zip(self, first, second):
            from_part, to_part = sorted(parts)
            if not (from_part <= my <= to_part):
                return False

        return True

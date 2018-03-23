# coding=utf-8


class PhotoClassifier(object):
    """
    Gets photo as file and tries to process into TeamInfo classes.
    """

    def __init__(self):
        pass

        # TODO: load teams info from db

    def process(self, photo: str):
        pass

        # TODO: process whole pipeline from detection to classification
        # TODO: successfully classified photos upload to API and save tags via another class
        # TODO: think about GUI with image class correction by user


__all__ = ['PhotoClassifier']

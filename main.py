# coding=utf-8
import logging
from sys import argv

from minicup_administration.conf import configure_django

configure_django()
from minicup_photo_classifier.classification import PhotoClassifier

logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    classifier = PhotoClassifier()
    classifier.process(argv[1])

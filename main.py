# coding=utf-8
from sys import argv

import cv2

# TODO: process argv
# TODO: delegate to PhotoClassifier
import minicup_photo_classifier.detection.object_detector

dec = minicup_photo_classifier.detection.object_detector.ObjectDetector()

if __name__ == '__main__':
    print(dec.detect_objects(
        cv2.imread(argv[1])
    ))

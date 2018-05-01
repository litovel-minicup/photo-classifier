# coding=utf-8
import logging
import os
import warnings
from os.path import abspath, dirname, join

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

with warnings.catch_warnings():
    from minicup_photo_classifier.neural_network.neural_network import NeuralNetwork

TRAIN_DIR = abspath(join(dirname(__file__), 'train'))
SNAPSHOT_DIR = abspath(join(dirname(__file__), 'snapshot'))

logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    nn = NeuralNetwork(SNAPSHOT_DIR)

    nn.train(TRAIN_DIR)

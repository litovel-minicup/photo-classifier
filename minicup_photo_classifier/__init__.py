# coding=utf-8
import sys
from os.path import dirname, realpath, join

PACKAGE_ROOT = dirname(realpath(__file__))
sys.path.append(join(PACKAGE_ROOT, 'lib/nms_cython/'))
sys.path.append(join(PACKAGE_ROOT, 'lib/multicut_cython/'))

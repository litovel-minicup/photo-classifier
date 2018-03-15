# coding=utf-8
import sys

import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import morphology
from skimage.exposure import exposure
from skimage.feature import canny
from skimage.io import imread
from skimage.filters import sobel, threshold_otsu, gaussian
import numpy as np
from skimage.morphology import remove_small_objects


def main(path_):
    image = imread(path_, as_grey=True)
    fig, ax = plt.subplots()
    image = gaussian(image, 4)
    ax.imshow(image)

    image = exposure.equalize_hist(image)
    fig, ax = plt.subplots()
    ax.imshow(image)

    threshold = threshold_otsu(image, nbins=4)
    fig, ax = plt.subplots()
    ax.imshow(image <= threshold)

    # return
    edges = canny(image)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
    ax.set_title('Canny detector')
    ax.axis('off')
    ax.set_adjustable('box-forced')

    # edges = remove_small_objects(edges, 128)

    edges = ndi.grey_dilation(edges, size=(3,3))

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
    ax.set_title('Dilatated')
    ax.axis('off')
    ax.set_adjustable('box-forced')

    fill_coins = ndi.binary_fill_holes(edges)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(fill_coins, cmap=plt.cm.gray, interpolation='nearest')
    ax.set_title('filling the holes')
    ax.axis('off')

    elevation_map = sobel(image)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(elevation_map, cmap=plt.cm.gray, interpolation='nearest')
    ax.set_title('elevation map')
    ax.axis('off')
    ax.set_adjustable('box-forced')

    markers = np.ones_like(elevation_map)
    markers[elevation_map < 10] = 1
    markers[elevation_map > 190] = 2

    fig, ax = plt.subplots(figsize=(4, 3))
    # ax.imshow(markers, cmap=plt.cm.spectral, interpolation='nearest')
    # ax.set_title('markers')
    # ax.axis('off')
    # ax.set_adjustable('box-forced')

    segmentation = morphology.watershed(elevation_map, 10)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(segmentation, cmap=plt.cm.gray, interpolation='nearest')
    ax.set_title('segmentation')
    ax.axis('off')
    ax.set_adjustable('box-forced')


    plt.show()


for path_ in sys.argv[1:]:
    main(path_)

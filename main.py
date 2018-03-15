#!/usr/bin/env python

import sys
from os.path import basename

import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as ndi
from skimage.exposure import exposure
from skimage.morphology import convex_hull_object, remove_small_holes, binary_opening

from deepgaze.saliency_map import FasaSaliencyMapping


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image[np.nonzero(image)])

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


def main(path):
    image = cv2.imread(path)
    image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    image = exposure.rescale_intensity(image)

    # cv2.imshow("what", image)
    my_map = FasaSaliencyMapping(image.shape[0], image.shape[1])  # init the saliency object

    # cv2.imshow('original', image)
    converted = []

    for format_ in ('BGR2LAB', 'BGR2RGB', 'RGB2LAB', 'RGB'):
        masked = my_map.returnMask(image, tot_bins=8, format=format_)  # get the mask from the original image
        masked = cv2.GaussianBlur(masked, (17, 17), 0)  # applying gaussin blur to make it pretty
        # masked = cv2.medianBlur(masked, 11)
        masked = cv2.adaptiveThreshold(
            masked, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 1023, 0
        )
        # masked = cv2.GaussianBlur(masked, (7, 7), 1)  # applying gaussin blur to make it pretty
        # ret, masked = cv2.threshold(masked, 64, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        converted.append(masked)
        # cv2.imshow(format_, masked)

    result = np.zeros(converted[0].shape)
    print('conv', converted[0].shape)
    print('result', result.shape)

    CONF = (.35, .2, .25, .2)

    for i, (c, modifier) in enumerate(zip(converted, CONF)):
        result += c * modifier

    for i in range(3):
        for format_ in ('BGR2LAB', 'BGR2RGB', 'RGB2LAB', 'RGB'):
            copied = image.copy()
            copied[:, :, i] = 0
            copied[0, 0, i] = 1
            # copied = my_map.returnMask(copied, tot_bins=8, format=format_)
            # cv2.imshow("s" + str(i) + format_, copied)

            # cv2.imshow('zero: {}'.format(i), copied)

    # cv2.waitKey(0)

    # result = np.where(result, result, result > len(converted) * 127)
    # result = result[:, 0] > len(converted) * 127
    # result = np.clip(result[:,:, 0], 0, 127 * len(converted), out=result[:, :, 0])
    limit = 127
    print(result)
    result[result < limit] = 0
    result[result > limit] = 1

    # cv2.imshow("mask", result)

    # cv2.waitKey(0)

    return image, result

def compute_hist(img):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [HIST_RANGE], [0, 256])
        histr = np.where(histr > (HIST_RANGE - 1), 0, histr)
        plt.subplot(3, 3, i + 1)
        plt.plot(histr[:, :], color=col)
        plt.xlim([0, HIST_RANGE])

    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([orig], [i], None, [HIST_RANGE], [0, 256])
        plt.subplot(3, 3, i + 1 + 3 + 3)
        plt.plot(histr[:, :], color=col)
        plt.xlim([0, HIST_RANGE])

    plt.subplot(3, 3, 4)
    plt.imshow(img[:, :, ::-1])
    plt.subplot(3, 3, 5)
    from skimage.feature import canny

    edges = canny(img[:, :, 0])

    edges = ndi.grey_dilation(edges, size=(4, 4))
    edges = binary_opening(edges)
    edges = remove_small_holes(edges, 256)

    edges = convex_hull_object(edges, 4)
    # edges = reconstruction(edges, (64, 64))

    plt.imshow(edges)
    plt.subplot(3, 3, 6)
    plt.imshow(orig[:, :, ::-1])
    # plt.show()

def compute_filled_canny_edges(orig, mask):
    cv2.imshow('auto canny orig', auto_canny(orig))
    cv2.imshow('mask', mask)
    # cv2.imshow('auto canny mask', auto_canny(mask))
    cv2.imshow('orig', orig)
    mask_canned = auto_canny(np.where(mask == 0, 255, orig))
    filled = ndi.binary_fill_holes(mask_canned)
    cv2.imshow('auto canny masked', mask_canned)

    plt.imshow(filled, cmap=plt.cm.gray, interpolation='nearest')
    plt.show()

    cv2.imshow('masked', np.where(mask == 0, 255, orig))

    cv2.waitKey(0)


if __name__ == "__main__":
    for path_ in sys.argv[1:]:
        orig, mask = main(path_)
        print('orig', orig.shape)
        print('mask', mask.shape)
        mask = mask[:, :, np.newaxis]
        masked = np.where(mask == 0, 255, orig)
        res = np.concatenate((orig, masked), axis=1)

        # masked = np.digitize(masked, np.linspace(0, 255, 16))

        HIST_RANGE = 64
        if True:
            compute_hist(masked)

        if False:
            compute_filled_canny_edges(orig, mask)
            
        elif True:
            fig = plt.gcf()
            # fig.title(datetime.now())
            fig.savefig('output/{}.png'.format(basename(path_)))
            plt.clf()

        # plt.hist(img.ravel(), 256, [0, 256])
        # plt.show()
        # res = np.concatenate((res, mask), axis=1)
        # cv2.imwrite('output/{}'.format(basename(path_)), res)

    cv2.destroyAllWindows()

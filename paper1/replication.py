#################################################################
##===== Replication for Paper 1: Intra-object segmentation ====##
#################################################################

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Algorithm 1: Object segmentation
def objSegmentation(roi, img_t, img_d):
    # Grabbing and cutting
    mask = np.zeros(img_d.shape[:2], np.uint8)  # mask similar to image, with shape and return type
    bgdModel = np.zeros((1, 65), np.float64)  # background model init
    fgdModel = np.zeros((1, 65), np.float64)  # foreground model init
    cv2.grabCut(img_d, mask, roi, bgdModel, fgdModel, 15, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(
        'uint8')  # pixels flagged 0,2 convert to 0 otherwise convert to 1
    mask = img_d * mask2[:, :, np.newaxis]

    # Cropping images to make sizes correspond
    mask = mask[int(roi[1]): int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]  # cropping image
    img_t = img_t[int(roi[1]): int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]  # cropping image
    img_d = img_d[int(roi[1]): int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]  # cropping image

    # Normalizing and processing mask to find the desired threshold via image histogram
    mask = img_d & mask  # bitwise and operation
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # converting to grayscale for thresholding
    minD, maxD, shadesNZ = histMinMax(mask)

    # Binary thresholding mask from grab cut segmented depth image
    for y in range(0, mask.shape[0]):
        for x in range(0, mask.shape[1]):
            mask[y, x] = 255 if mask[y, x] > minD else 0

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # converting back to color for bitwise AND operation
    img_t_seg = img_t & mask
    img_d_seg = img_d & mask
    return img_t_seg, img_d_seg


# Algorithm 2: Histogram min/max identification for grayscale image
def histMinMax(img):
    shadesNZ = []  # init
    hist, bins = np.histogram(img.ravel(), 256, [0, 256])  # Calculate histogram of image
    plt.plot(hist, color='r'), plt.xlim([0, 256]), plt.title('Histogram of grayscale depth image pixels')
    plt.xlabel('Pixel intensity'), plt.ylabel('Pixel frequency')
    plt.savefig('media/histogram.png')
    plt.show()

    # Store non-zero bins (w.r.t pixel intensity value)
    for i in range(len(hist)):
        if hist[i] != 0:
            shadesNZ.append(i)

    minD = shadesNZ[0]
    maxD = shadesNZ[len(shadesNZ) - 1]
    return minD, maxD, shadesNZ


# Algorithm 3: Intra-object segmentation
def intraObjSegmentation(shadesNZ, minD, maxD, img_t_seg, img_d_seg):
    L_layers = []  # init list for layers

    for shade in shadesNZ:
        mask = np.zeros(img_t_seg.shape[:2], np.uint8)  # init mask per depth

        # Thresholding for mask per depth
        for y in range(0, img_d_seg.shape[0]):
            for x in range(0, img_d_seg.shape[1]):
                mask[y, x] = 255 if img_d_seg[y, x][0] == shade else 0
        layer = img_t_seg & mask[:, :, np.newaxis]
        L_layers.append(layer)
    return L_layers


# Prints layers in animation form and text form
def printLayers(L_layers,filename):
    print('Layer count: ', len(L_layers))
    i = 0
    for layer in L_layers:
        print('Depth layer: ', i)
        cv2.imshow("l", layer)
        file = 'media/layers/' + filename + '-'+str(i) + '.jpg'
        cv2.imwrite(file, layer)
        cv2.waitKey(250)
        i+=1
    return
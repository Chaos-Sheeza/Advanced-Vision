#################################################################
##===== Main for Paper 1: Intra-object segmentation ===========##
#################################################################

import cv2
from replication import *
from variations import *

# Importing images and obtaining region of interest
img_t = cv2.imread("..\P1 Resources\c4t.bmp",1)
img_d = cv2.imread("..\P1 Resources\c4d.bmp", 1)
#img_t = cv2.imread("../P1 Resources/balloons1f291t.bmp",1)
#img_d = cv2.imread("../P1 Resources/balloons1f291d.bmp", 1)

#=================Replication===================================#
roi = cv2.selectROI(img_t, True, False) # Region of Interest
img_t_seg, img_d_seg = objSegmentation(roi, img_t, img_d) # Algorithm 1
cv2.imwrite('media/img_t_seg.jpg', img_t_seg)
cv2.imwrite('media/img_d_seg.jpg', img_d_seg)
minD, maxD, shadesNZ = histMinMax(img_d_seg) # Algorithm 2
L_layers = intraObjSegmentation(shadesNZ, minD, maxD, img_t_seg, img_d_seg) # Algorithm 3

#=================Variations====================================#
L_brightness, L_hsv = getSoftHSVLayers(L_layers)
#for i in range (len(L_layers)):
#    print('====',i,'====')
#    print('brightness:', L_brightness[i])
#    print('hsv:', L_hsv[i])

# Preperation for manipulation methods
img_t = img_t[int(roi[1]): int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]  # cropping image
L_layers_d = intraObjSegmentationDepth(shadesNZ, minD, maxD, img_d_seg)
#L_layers = selectLayers(L_layers, 20, len(L_layers)) # reselection of depth layers
#L_layers_d = selectLayers(L_layers_d, 20, len(L_layers_d)) # reselection of depth layers
printLayers(L_layers, 'texture') # print depth layers
printLayers(L_layers_d, 'depth') # print depth layers

img = manipByAvgHSV(img_t, L_layers, L_layers_d, L_hsv)
resized = resizePercentage(img, 200)
cv2.imwrite('media/hsv.jpg', resized)
cv2.imshow('HSV', resized)
cv2.waitKey(200)

img = manipByAvgBright(img_t, L_layers, L_layers_d, L_brightness)
resized = resizePercentage(img, 200)
cv2.imwrite('media/bright.jpg', resized)
cv2.imshow('Bright', resized)
cv2.waitKey(200)

img = manipByRandCol(img_t, L_layers, L_layers_d)
resized = resizePercentage(img, 200)
cv2.imwrite('media/pink.jpg', resized)
cv2.imshow('Rand', resized)
cv2.waitKey(0)

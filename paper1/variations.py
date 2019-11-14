#################################################################
##===== Variations for Paper 1: Intra-object segmentation =====##
#################################################################

import cv2
import random
import numpy as np

# Selects region of depth layers via parameters
def selectLayers(L_layers, start, end):
    L_layers_sel = []
    try:
        for i in range(start, end):
            L_layers_sel.append(L_layers[i])
        return L_layers_sel
    except IndexError as e:
        print('Reselection of layers cancelled. [ Error:', e, ']')
        return L_layers


# Returns two lists: average brightness and average hsv for each layer
def getSoftHSVLayers(L_layers):
    L_brightness, L_hsv = [], []
    for layer in L_layers:
        brightness_sum = 0 # init sum for avg_brightness
        hsv_sum = [0, 0, 0] # init sum for avg_hsv
        px_i = 0  # init counter for pixel amount
        hsv_layer = cv2.cvtColor(layer, cv2.COLOR_BGR2HSV) # hsv_version of layer

        # Traversing layer as an image
        for y in range(0, layer.shape[0]):
            for x in range(0, layer.shape[1]):
                red = layer[y, x][2]
                green = layer[y, x][1]
                blue = layer[y, x][0]
                # Doesn't consider zero pixels
                if(red != 0 and green != 0 and blue != 0):
                    # Calculating brightness of pixel
                    # alternative method: brightness_sum += hsv_layer[y, x][2]
                    brightness_sum += max(red, green, blue)

                    # Calculating hsv of pixel, by referencing
                    hsv_sum = [hsv_sum[i] + hsv_layer[y, x][i] for i in range(len(hsv_sum))]
                    px_i += 1

        # note: "if px_i > 0 else 0" is to cater for the case of
        # a background layer, to avoid a zeroDivideByZero error
        avg_brightness = brightness_sum/px_i if px_i > 0 else 0
        avg_hsv = (hsv_sum[0] / px_i, hsv_sum[1] / px_i, hsv_sum[2] / px_i) if px_i > 0 else (0, 0, 0)
        L_brightness.append(avg_brightness)
        L_hsv.append(avg_hsv)
    return L_brightness, L_hsv

# Intra object segmentation for depth layers
# required for texture manipulation methods
def intraObjSegmentationDepth(shadesNZ, minD, maxD, img_d_seg):
    L_layers = []  # init list for layers

    for shade in shadesNZ:
        mask = np.zeros(img_d_seg.shape[:2], np.uint8)  # init mask per depth

        # Thresholding for mask per depth
        for y in range(0, img_d_seg.shape[0]):
            for x in range(0, img_d_seg.shape[1]):
                mask[y, x] = 255 if img_d_seg[y, x][0] == shade else 0
        layer = img_d_seg & mask[:, :, np.newaxis]
        L_layers.append(layer)
    return L_layers


# Manipulates texture image by average HSV per layer
# Future improvement: get it to include foreground black pixels
def manipByAvgHSV(img_t, L_layers, L_layers_d, L_hsv):
    for i in range(len(L_layers)):
        layer = cv2.cvtColor(L_layers[i], cv2.COLOR_BGR2HSV)
        layer_d = L_layers_d[i]
        for y in range(0, layer.shape[0]):
            for x in range(0, layer.shape[1]):
                value = layer_d[y, x][2]
                sat = layer_d[y, x][1]
                hue = layer_d[y, x][0]
                # Doesn't consider zero pixels
                if (hue != 0 and sat != 0 and value != 0):
                    layer[y, x] = (L_hsv[i][0], L_hsv[i][1], L_hsv[i][2])
                    img_t[y, x] = layer[y,x]
    return img_t

# Manipulates texture image by average brightness per layer only
# Future improvement: get it to include black pixels
def manipByAvgBright(img_t, L_layers, L_layers_d, L_brightness):
    for i in range(len(L_layers)):
        layer = cv2.cvtColor(L_layers[i], cv2.COLOR_BGR2HSV)
        layer_d = L_layers_d[i]
        for y in range(0, layer.shape[0]):
            for x in range(0, layer.shape[1]):
                value = layer_d[y, x][2]
                sat = layer_d[y, x][1]
                hue = layer_d[y, x][0]
                # Doesn't consider zero pixels
                if (hue != 0 and sat != 0 and value != 0):
                    layer[y, x] = (L_brightness[i], L_brightness[i], L_brightness[i])
                    img_t[y, x] = layer[y,x]
    return img_t

# Manipulates texture image by random colour per layer
def manipByRandCol(img_t, L_layers, L_layers_d):
    for i in range(len(L_layers)):
        layer = L_layers[i]
        layer_d = L_layers_d[i]
        #r, g, b = random.randint(50,100), random.randint(200,255), random.randint(100,200) # green pallette
        #r, g, b = random.randint(50,100), random.randint(100,200), random.randint(200,255) # blue pallette
        r, g, b = random.randint(200, 255), random.randint(50, 100) , random.randint(100, 200)  # red pallette
        for y in range(0, layer.shape[0]):
            for x in range(0, layer.shape[1]):
                blue = layer_d[y, x][2]
                green = layer_d[y, x][1]
                red = layer_d[y, x][0]
                # Doesn't consider zero pixels
                if (blue != 0 and green != 0 and red != 0):
                    layer[y, x] = (b, g, r)
                    img_t[y, x] = layer[y,x]
    return img_t

# A resizing method, returns resized image
def resizePercentage(img, scale_percentage):
    width = int(img.shape[1] * scale_percentage / 100)
    height = int(img.shape[0] * scale_percentage / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

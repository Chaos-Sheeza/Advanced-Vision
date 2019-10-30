#mosquito almost chocked me to death
#jenny's tale

import cv2

T = cv2.imread("P1 Resources/c4t.bmp")
D = cv2.imread("P1 Resources/c4d.bmp")
p1,p2 = [],[]

def mouse(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        p1.clear()
        p1.append(x)
        p2.clear()
        p2.append(y)
        return True

def patch(x,y,img, size):
        maxY,maxX = img.shape[0], img.shape[1]

        if x-(size/2) < 0:
                newX = 0
        elif x+(size/2) > maxX-1:
                newX = maxX-(size+1)
        else:
                newX = x-(size/2)

        if y-(size/2) < 0:
                newY = 0
        elif y+(size/2) > maxY-1:
                newY = maxY-(size+1)
        else:
                newY = y+(size/2)

        newX = int(newX)
        newY = int(newY)

        patch = img[newX:newX+size, newY:newY+size]
        return patch

def dtObj(x,y,treshD,treshT,T,D,Patch):
        # function for dPatch
        # function for tPatch
        return Ld, Lt

cv2.imshow('Texture',T)
#cv2.imshow('Depth',D)
cv2.setMouseCallback('Texture', mouse)
cv2.waitKey(0)
cv2.destroyAllWindows
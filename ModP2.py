import cv2
import numpy as np

img1 = cv2.imread("P1 Resources/c4t.bmp")
img2 = cv2.imread("P1 Resources/c4d.bmp")
T = cv2.GaussianBlur(img1,(5,5),0)
D = cv2.GaussianBlur(img2,(5,5),0)

td = 3000
tt = 3000
p1,p2 = [],[]
s = 6

# Standard deviation function
def SSD(refPatch, iPatch):
        #print(refPatch)
        #print(iPatch)
        temp = np.sum(np.subtract(refPatch,iPatch)**2)
        #ret = temp*temp
        return temp

# on mouse function to pass as a cv2.setMouseCallback() parameter.
def mouse(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:    # if left mouse button is double clicked
                # clears previous coordinates and appends current mouse coordinate.
                #p1.clear()
                p1.append(x)
                #p2.clear()
                p2.append(y)
                # grabs patch around mouse click and displays patch.
                #im2 = patch(p1[0],p2[0],T,s)
                #cv2.imshow('test',im2)
                # testing tmp = dtObj(x,y,tt,td,T,D,s)
                #print(tmp) # check cv2 tresholds.
                # testing plot(tmp[0],tmp[1],img1)
                return True

# function that returns a patch around a single coordinate.
def patch(y,x,img,size):
        temp = int(size/2)
        return img[x-temp:x+temp, y-temp:y+temp]

# resource: "Efficient Object Selection using Depth and Texture Information", Dylan Seychell, Carl James Debono 
def dtObj(xs,ys,treshD,treshT,T,D,Patch):
        y,i = Patch,0
        Ld,Lt = [],[]
        #ssdD,ssdT = [],[]
        dPatch = patch(xs,ys,D,Patch)
        tPatch = patch(xs,ys,T,Patch)
        while y<(T.shape[0]-Patch):
                x = Patch
                while x<(T.shape[1]-Patch):
                        idPatch = patch(x,y,D,Patch)
                        #print(idPatch)
                        itPatch = patch(x,y,T,Patch)
                        #print(itPatch)
                        ssdD = SSD(dPatch,idPatch)
                        ssdT = SSD(tPatch,itPatch)
                        #print(ssdD)

                        if ssdD < treshD:
                                Ld.append([y,x])
                        if ssdT < treshT:
                                Lt.append([y,x])

                        x = x + Patch
                y = y + Patch

        return Ld, Lt

def plot(Ld,Lt,img):
        temp = img
        Comm = comm(Ld,Lt)
        for j in range(len(Comm)):
                temp[Comm[j][0], Comm[j][1]] = [0,0,255]
        cv2.imshow('result',temp)

def comm(t,d):
        temp = []
        for j in range(len(t)):
                if t[j] in d:
                        temp.append(t[j])
        return temp

cv2.imshow('Texture',img1)
#cv2.imshow('Depth',D)
cv2.setMouseCallback('Texture', mouse)
cv2.waitKey(0)
for it in range(len(p1)):
        tmp = dtObj(p1[it],p2[it],tt,td,T,D,s)
        plot(tmp[0],tmp[1],img1)
cv2.waitKey(0)
cv2.destroyAllWindows
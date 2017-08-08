import cv2
import os,math
import numpy as np
from matplotlib import pyplot as plt



def isEqualLines(x,y):
    
    length1 = np.sqrt((x[2] - x[0])*(x[2] - x[0]) + (x[3] - x[1])*(x[3] - x[1]))
    center1 = (float(abs(x[2]-x[0])/2), float(abs(x[3]-x[1])/2))
    center2 = (float(abs(y[2]-y[0])/2), float(abs(y[3]-y[1])/2))

    if(np.sqrt((center1[0] - center2[0])*(center1[0] - center2[0]) + (center1[1] - center2[1])*(center1[1] - center2[1]))< 1):
        return True

    length2 = np.sqrt((y[2] - y[0])*(y[2] - y[0]) + (y[3] - y[1])*(y[3] - y[1]))
    if(float(x[2] - x[0]) != 0.0):
        mx = float(float(x[3] - x[1])/float(x[2] - x[0]))
    if(float(y[2] - y[0]) != 0.0):
        my = float(float(y[3] - y[1])/float(y[2] - y[0]))
    mx1 = (x[0] + x[2]) * 0.5
    mx2 = (y[0] + y[2]) * 0.5

    my1 = (x[1] + x[3]) * 0.5
    my2 = (y[1] + y[3]) * 0.5
    dist = np.sqrt((mx1 - mx2)*(mx1 - mx2) + (my1 - my2)*(my1 - my2));
    dist_check = 15
    #if(abs(mx) > 0.5):
    #    dist_check =10
    #    print dist_check
    if (dist > dist_check):
        return False
    return True


def detect_lines(img):
    ret,thresh = cv2.threshold(img,(np.mean(img))*1.3,255,0)
    edges = cv2.Canny(thresh,50,150,apertureSize = 3)
    #cv2.imwrite('Houhlines3.jpg',edges)
    minLineLength = img.shape[1]/8
    print minLineLength
    maxLineGap = 50
    i=0
    lines = cv2.HoughLinesP(edges,rho=1.0, theta=math.pi/180.0,
                                        threshold=50+i,minLineLength=minLineLength,
                                        maxLineGap=maxLineGap)
    while(len(lines[0]) > 60):
        i = i+1
        lines = cv2.HoughLinesP(edges,rho=1.0, theta=math.pi/180.0,
                                        threshold=50+i,minLineLength=minLineLength,
                                        maxLineGap=maxLineGap)
        print i
        if(lines == None):

            lines = cv2.HoughLinesP(edges,rho=1.0, theta=math.pi/180.0,
                                        threshold=50+i-1,minLineLength=minLineLength,
                                        maxLineGap=maxLineGap)
            break

    new_lines = lines[0]
    k = 0
    for x in lines[0]:
        for y in lines[0]:
            if(np.array_equal(x,y)):
                continue
            else:
                isEqual = isEqualLines(x,y)
                if(isEqual):
                    k = k+1
                    if(y in new_lines and x in new_lines):
                        i = 0
                        for item in new_lines:
                            i = i+1
                            if(item.all() == y.all()):
                                #i = i+1
                                break
                        if(len(new_lines)!= i):
                            new_lines = np.delete(new_lines,(i),0)
                        
    for x1,y1,x2,y2 in new_lines:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    #cv2.imwrite('houghlines3.jpg',img)
    return new_lines


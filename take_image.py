import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import os, time
cameraChoice = 0
cap = cv2.VideoCapture(cameraChoice)




def calibrate(inputImage, clb_pts):
    # 1. Slice the img 
    new_img = inputImage[np.min(clb_pts[:, 1]) : np.max(clb_pts[:,1]), \
        np.min(clb_pts[:, 0]): np.max(clb_pts[ :, 0])]
    row, column = np.shape(new_img)[0], np.shape(new_img)[1]

    # 2. Apply perspective adjustment
    pts1 = np.float32([[clb_pts[0,0], clb_pts[0,1] ], \
        [clb_pts[1,0], clb_pts[1,1]], \
        [clb_pts[2,0], clb_pts[2,1] ],\
        [clb_pts[3,0], clb_pts[3,1] ]])

    pts2 = np.float32(
        [
        [0, 0], [0 , column],[row, 0], [row, column]
        ]
        )

    pers = cv2.getPerspectiveTransform(pts1,pts2)
    # For some reason, the result is rotated -90 degrees. 
    # So I use rot90 to rotate it 270 degrees to get back to normal
    calibrated_img = cv2.warpPerspective(inputImage, pers, (row, column))
    calibrated_img =  np.rot90(calibrated_img, 3)
    calibrated_img=cv2.flip(calibrated_img,1)
    return calibrated_img


def getCalibrationCoordinates(inputImage):
    # Create a matplotlib figure for interactively choose 4 cornes
    fig = plt.figure(1, figsize = (10, 10))
    plt.gca().imshow(inputImage, cmap = cm.Greys_r), plt.title('Click on 4 corners to calibrate.')
    plt.xlabel("Start from top left then move Z shape.")
    pts = np.asarray(plt.ginput(4))
    if len(pts) == 4:
        plt.close()
    return pts.astype(int)





"""
Main Loop
""" 
def camera():
    ret, original_img = cap.read()
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    # Left and now is wrongly flip. 
    original_img = cv2.flip(original_img, 0)
    original_img = cv2.flip(original_img, 1)
    calibration_points = getCalibrationCoordinates(original_img)
    # ser.write(chr(0)+chr(0)+chr(0)+chr(0)+chr(0)) # Switch leds off



    # Here comes the main loop
    while True:
        ret,original_img = cap.read()
        # Transform video into greyscale
        # Left and now is wrongly flip. 
        # Throw an exception: cv2.error. Then jump to the end of the loop/ 
        img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        img = cv2.flip(img, 0)
        img = cv2.flip(img, 1)
        img = calibrate(img, calibration_points)
        row, column = np.shape(img)[0], np.shape(img)[1]


                    # Show edges, result image, and blobs
        cv2.imshow('Image',cv2.resize(img, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_AREA))

        # Put all send OSC here. 

        if cv2.waitKey(100) & 0xff == 27:
            cv2.destroyAllWindows()
            break




camera()








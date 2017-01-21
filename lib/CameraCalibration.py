# Image Gradients, edges
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import os, time


def calibrate(unscaledImg, clb_pts):
	# 1. Slice the img 
	new_img = unscaledImg[np.min(clb_pts[:, 1]) : np.max(clb_pts[:,1]), \
		np.min(clb_pts[:, 0]): np.max(clb_pts[ :, 0])]
	row, column = np.shape(new_img)[0], np.shape(new_img)[1]
	print clb_pts

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
	calibrated_img = cv2.warpPerspective(unscaledImg, pers, (row, column))
	calibrated_img = np.rot90(calibrated_img, 3)
	fig, ax = plt.subplots()
	plt.imshow(calibrated_img, cmap = cm.Greys_r), plt.title('Cropped.')
	plt.show()

def getCalibrationCoordinates(unscaledImg):
	fig = plt.figure(1, figsize = (10, 10))

	plt.gca().imshow(unscaledImg, cmap = cm.Greys_r), plt.title('Click on 4 corners to calibrate.')
	pts = np.asarray(plt.ginput(4))
	if len(pts) == 4:
		plt.close()
	pts = pts.astype(int)
	return pts

# Change to the dir of your folder. 
os.chdir ("./imgs")
# Img is r x c = y x x
img = cv2.imread('2.png',0)
img = cv2.flip(img, 0)
img = cv2.flip(img, 1)

pts = getCalibrationCoordinates(img)
calibrate(img,pts)



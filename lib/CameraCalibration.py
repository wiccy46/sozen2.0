# Image Gradients, edges
import cv2
import numpy as np
# Maybe put a system detection. Use the new backend if PC. Else nothing change.
# import matplotlib
# matplotlib.use('Qt4Agg')
from matplotlib import pyplot as plt
import matplotlib.cm as cm


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

def getCalibrationCoordinates():
	cap = cv2.VideoCapture(0)
	ret, original_img = cap.read()
	original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
	# Left and now is wrongly flip.
	original_img = cv2.flip(original_img, 0); original_img = cv2.flip(original_img, 1)
	fig = plt.figure(1, figsize = (10, 10))
	plt.gca().imshow(original_img, cmap = cm.Greys_r), plt.title('Click on 4 corners to calibrate.')
	pts = np.asarray(plt.ginput(4))
	if len(pts) == 4:
		plt.close()
	pts = pts.astype(int)
	return pts





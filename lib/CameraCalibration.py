# Image Gradients, edges
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm



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





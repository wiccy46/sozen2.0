import cv2, sys, time
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt4Agg')
import matplotlib.cm as cm
global pts
def getCalibrationCoordinates(choice,i):
	cap = cv2.VideoCapture(choice)
	ret, original_img = cap.read()
	original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
	original_img = cv2.equalizeHist(original_img)
	#original_img = np.hstack((original_img,newimg)) 
	# Left and now is wrongly flip.
	
	#original_img[:,:,2] = [[max(pixel - 25, 0) if pixel < 190 else min(pixel + 25, 255) for pixel in row] for row in original_img[:,:,2]]
	#cv2.imshow('contrast', cv2.cvtColor(original_img, cv2.COLOR_HSV2BGR))
	#cv2.waitKey(1000)
	
	print "Inside the function"
	fig = plt.figure(1, figsize = (10, 10))
	if(i != 1):
		plt.gca().imshow(original_img, cmap = cm.Greys_r),plt.title('Click on 4 corners to calibrate.')
		global pts 
		pts = np.asarray(plt.ginput(4))
		print pts
		if len(pts) == 4:
			plt.close()

	pts = pts.astype(int)
	print pts
	return calibrate(original_img,pts)
def calibrate(inputImage, clb_pts):
	# 1. Slice the img

	new_img = inputImage[np.min(clb_pts[:, 1]) : np.max(clb_pts[:,1]), \
		np.min(clb_pts[:, 0]): np.max(clb_pts[ :, 0])]

	return new_img
i = 0
directory = 'machineLearning/TrainData/'
for filename in os.listdir(directory):
    if filename.startswith("VerticalLine") and filename.endswith(".png"): 
        # print(os.path.join(directory, filename))
        i = i+1
print i

input = True
while(input):
	save = raw_input()
	i = i +1
	if(save == 's'):
		calibration_img = getCalibrationCoordinates(0,i)

		#row, column = np.shape(calibration_img)[0], np.shape(calibration_img)[1]
		#img =calibration_img[int(row ): int(row), int(column) : int(column)]
		#print img
		
		cv2.imwrite("machineLearning/TrainData/VerticalLine"+str(i)+".png",calibration_img) 
	if(save == 'x'):
		input = False
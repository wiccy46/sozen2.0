"""
Line Feature Extraction
Functions included: 
(1) findLineCenter (2) removeBlobLines (3) lineDetection
(4) circleDetection (unused) (5) contourDetection (unused)
(6) findDensity (Maybe not necessary anymore if I can get the lineDetection to work properly.)
(7) findZone, based on line center find which zone it belongs
(8) findAngle, return angle in degrees that is not based on the coordinate system but
	our view angle. 

Line length is not imprtant for the interaction, this is because the lenght is not accurate. 
One "straight" sand line can be split into a combination of the other lines. And when the 
actually sand lines locate so close to each other. It is hard to combinate the desired line 
together for meaningful line length extraction. 
"""	

import cv2
import numpy as np
import oscPart
import cv2.cv as cv  # Used in circle detection
import math
import stones # use its whichZone function

def lineDetectionFFT(img):
	"""
	1. Using super sampling to down sample to 100 x 100
	"""

	"""
	2. Run through a 5X5 window with the dimension of 95 x 95. In each run, take the FFT
	"""

	"""
	3. Using super sampling to down sample to 100 x 100
	"""

	"""
	4. Some averaging method.... (optional)
	"""

	"""
	5. Local PCA, that output the direction of the grid. 
	"""

	"""
	6. From PCA, the ratio of greater_eigenvalue/smaller_eigenvalue = the likelihood
	Then threshold to filter out low_likelihood lines. 
	"""

	"""
	7. Get line information and output. Realise the data format of the lines
	"""
	pass


def findLineCenter(lines):
	# This function find out the center position of each line. 
	line_row = np.shape(lines)[0]
	lines_center = np.empty([line_row, 2], dtype = int)
	for i in range(line_row):
	 	x1 = lines[i,0]
		y1 = lines[i,1]
		x2 = lines[i,2]
		y2 = lines[i,3]
		lines_center[i, 0] = int(abs(x2 - x1)/2 )+ min(x1, x2) 
		lines_center[i, 1] = int(abs(y1 - y2)/2 )+ min(y1, y2)  
	return lines_center

def findZone(lines_center, frame_row, frame_column):
	row = np.shape(lines_center)[0]
	sand_all_zone = np.zeros(row, dtype = int)
	for i in range(row):
		x = float(lines_center[i,0])/frame_row
		y = float(lines_center[i,1])/frame_column
		# Call function to detect which zone the point belongs to. 
		sand_all_zone[i] = stones.whichZone(x, y)
	# Find a histogram of the zones, treated as the density
	hist = np.histogram(sand_all_zone, bins = [1,2,3,4,5,6,7,8,9,10], density = False)
	return sand_all_zone, hist[0]

def angleAverage(angle, zone):
	temp = np.zeros(10)
	info = np.column_stack((zone, angle))
	hist = np.histogram(zone, bins = [1,2,3,4,5,6,7,8,9,10])
	hist = hist[0]
	for i in range(len(zone)):
		temp[info[i,0]] = temp[info[i,0]] + info[i,1]
	temp = temp[1:] # Dump zone 0 (invalid zone)
	temp = temp / hist
	return temp

	



def findAngle(lines):
	row = np.shape(lines)[0]
	a = np.zeros(row)
	for i in range(row):
		x1 = lines[i,0]
		y1 = lines[i,1]
		x2 = lines[i,2]
		y2 = lines[i,3]
		if x1 == x2: 
			a[i] = 90
		else:
			if y1 >= y2:
				a[i] = math.atan(float((y1- y2))/(x2 - x1))
				a[i] = math.degrees(a[i])
			else:
				a[i] = math.atan(float((x2 - x1))/(y2- y1)) 
				a[i] = math.degrees(a[i]) + 90
	return a
	# Remember the angle should be suitable for our view angle. So 
	# maybe the result should be rotate 180 degrees. 

"""
The quality of remove blob line depends on the quality of blob tracking. 
"""
def removeBlobLines(lines, bblob_coordinates, bblob_sizes):
	lines = lines[0]
	line_row = np.shape(lines)[0]
	idx2delete = [] # Create an empty list 
	# Boundary
	# (x - size/2) : (x + size/2), (y - size/2) : (y + size/2)
	for j in range(line_row):
		x1 = lines[j,0]
		y1 = lines[j,1]
		x2 = lines[j,2]
		y2 = lines[j,3]
		for i in range(len(bblob_sizes)):
			if (x1 > (bblob_coordinates[i,0] - bblob_sizes[i]/2)) and \
				(x1 < (bblob_coordinates[i,0] + bblob_sizes[i]/2)):
				if (y1 > (bblob_coordinates[i,1] - bblob_sizes[i]/2)) and \
					(y1 < (bblob_coordinates[i,1] + bblob_sizes[i]/2)):
					idx2delete.append(j) # Record the index 
	
				else: pass

			elif (x2 > (bblob_coordinates[i,0] - bblob_sizes[i]/2)) and \
				(x2 < (bblob_coordinates[i,0] + bblob_sizes[i]/2)):
				if (y2 > (bblob_coordinates[i,1] - bblob_sizes[i]/2)) and \
					(y2 < (bblob_coordinates[i,1] + bblob_sizes[i]/2)):
					idx2delete.append(j)
					# recod the index
				else: pass
			else:
				pass
	# Remove any duplicate. 
	idx2delete = set(idx2delete)
	idx2delete = list(idx2delete)
	return np.delete(lines, idx2delete, 0)


def regionalLineDetection(img, rho, theta, cannyMin, cannyMax, lenFactor, gapFactor, row):
	"""
	Leave it after the system is finished. Treat as an optimisation. 
	This functiom receives the initial edge detection and futhure finetune it.
	1. Divide the image into multiple slice 
	"""
	pass

def lineDetection(img, rho, theta, cannyMin, cannyMax, lenFactor, gapFactor, row):
	edges = cv2.Canny(img, cannyMin + 1, cannyMax + 1, apertureSize = 3)

	# Define limits. 
	minLineLength = int(row / lenFactor)
	maxLineGap = int(row/ gapFactor)

	# HoughLinesP: Progressive Probabilistic Hough Transform 
	# Arg1: binary img; Arg2: distance resolution, Arg3: angle resolution
	#Arg4: Threshold
	lines = cv2.HoughLinesP(edges,rho + 1,np.pi/(theta+1),50,30,\
	 minLineLength,maxLineGap)

	# Need a OSC send here . 
	return lines, edges
# -------------------------------------------------------------------#

def circleDetection(img, p1, p2, fontSize):
	img = cv2.medianBlur(img,1)
	row = np.shape(img)[0]
	# edges ratio of the accumulator resolution, minimum distance
	#param1 First method-specific parameter. In case of CV_HOUGH_GRADIENT , 
	#it is the higher threshold of the two passed to the Canny() edge detector (the lower one is twice smaller).
	#param2 Second method-specific parameter. In case of CV_HOUGH_GRADIENT , 
	#it is the accumulator threshold for the circle centers at the detection stage. 
	#The smaller it is, the more false circles may be detected. 
	#Circles, corresponding to the larger accumulator values, will be returned first.

	circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,10,5,
                            param1=p1,param2=p2,minRadius= int(row / 5),maxRadius=int(row / 2))
	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
	    # draw the outer circle
	    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
	    # draw the center of the circle
	    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

	p1t = "Param1: " + str(p1)
	p2t = "Param2: " + str(p2)
	cv2.putText(img, p1t, (10 , 20 ), cv2.FONT_HERSHEY_PLAIN, fontSize, 255)
	cv2.putText(img, p2t, (10 , 40 ), cv2.FONT_HERSHEY_PLAIN, fontSize, 255)
	cv2.imshow('detected circles',cv2.resize(img, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_AREA))

# This is not working
def contourDetection(img, cannyMin, cannyMax):
	global ratio
	img = cv2.medianBlur(img,3)

	# edges = cv2.Canny(temp, cannyMin, cannyMax, apertureSize = 3)
	ret,thresh = cv2.threshold(img,127,255,0)
	# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours, hierarchy = cv2.findContours(thresh,3,5)
	cv2.drawContours(img, contours, -1, (0,255,0), 3)
	cv2.imshow('detected circles',cv2.resize(img, None, fx = ratio, fy = ratio, interpolation = cv2.INTER_AREA))


# findDensity take the binary image and normal to 0, 1 (white). 
# Then out 9 different sum based on the zone. 
def findDensity(img, frame_row, frame_column, cannyMin, cannyMax, fontSize):
	lineAmount = 0
	img = cv2.medianBlur(img,1)   # Not sure if necessary
	edges = cv2.Canny(img, cannyMin + 1, cannyMax + 1, apertureSize = 3)

	temp = edges / 255

	# cv2.imshow('Edges',cv2.resize(edges, None, fx = ratio, fy = ratio, interpolation = cv2.INTER_AREA))

	# well this way is not too practical because the maxDen is way too much for any
	maxDen = frame_row * frame_column / 9

	density = np.zeros(9,dtype = np.float)
	density[0] = np.sum(temp[0:int(frame_column/3), 0: int(frame_row/3)])/maxDen
	density[1] = np.sum(temp[0:int(frame_column/3), int(frame_row/3): int(frame_row * 2/3)])/maxDen
	density[2] = np.sum(temp[0:int(frame_column/3), int(frame_row* 2/3): frame_row])/maxDen
	density[3] = np.sum(temp[int(frame_column/3):int(frame_column * 2 /3), 0: int(frame_row /3)])/maxDen
	density[4] = np.sum(temp[int(frame_column/3) :int(frame_column * 2 /3), int(frame_row/3): int(frame_row * 2/3)])/maxDen
	density[5] = np.sum(temp[int(frame_column/3) :int(frame_column * 2 /3), int(frame_row* 2/3): frame_row])/maxDen
	density[6] = np.sum(temp[int(frame_column* 2/3) :frame_column, 0: int(frame_row /3)])/maxDen
	density[7] = np.sum(temp[int(frame_column* 2/3) :frame_column, int(frame_row/3): int(frame_row * 2/3)])/maxDen
	density[8] = np.sum(temp[int(frame_column* 2/3) :frame_column, int(frame_row* 2/3): frame_row])/maxDen

	sumDensity = np.sum(density)
	oscPart.sendDensity(density, sumDensity)

	cMin = "CannyMin: " + str (cannyMin + 1)
	cMax = "CannyMax: " + str (cannyMax + 1)
	cv2.putText(edges, cMin, (10 , 60 ), cv2.FONT_HERSHEY_PLAIN, fontSize, 255)
	cv2.putText(edges, cMax, (10 , 80 ), cv2.FONT_HERSHEY_PLAIN, fontSize, 255)
	cv2.imshow('Canny Edges',cv2.resize(edges, None, fx = 0.75, fy = 0.75, interpolation = cv2.INTER_AREA))
	# cv2.imshow('Find Density', edges)
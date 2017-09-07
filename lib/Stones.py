"""
Stone Feature Extraction
Functions included:
(1) findSize: return the diameter of each keypoint
(2) findCoordinates: return the x,y of each keypoint
(3) whichZone: devided the area into 9 zones (3x3). Then return which zone the current coordinates belong.
(4) findallZone: return an array of the zone information of all keypoints
(5) combinations: detect stone arrangement pattern based on predefined patterns. 
(6) findBlobs and blobDetection: Blob tracking based on thresholdings. Return keypoints of the blobs. 
"""
import cv2
import numpy as np



def findSize(keypoints):
	amount = len(keypoints)
	sizes = np.zeros(amount)
	for i in range (amount):
		sizes[i] = keypoints[i].size
	return sizes

def findCoordinates(keypoints):
	amount = len(keypoints)
	# Find out the coordinate
	coordinates = np.ndarray(shape=(amount,2), dtype=int)
	for i in range(amount):
		# normalised the coordinate. 
		coordinates[i, 0] = keypoints[i].pt[0]
		coordinates[i, 1] = keypoints[i].pt[1]
	return coordinates

def whichZone(normalised_x, normalised_y):
	# The zone is devided into 9 pieces. 
	if normalised_x <= 0.33 and normalised_y < 0.33:
		return 1
	elif normalised_x > 0.33 and normalised_x <= 0.66 and normalised_y < 0.33:
		return 2
	elif normalised_x > 0.66 and normalised_x <= 1 and normalised_y < 0.33:
		return 3
	elif normalised_x <= 0.33 and normalised_y >= 0.33 and normalised_y <= 0.66:
		return 4
	elif normalised_x > 0.33 and normalised_x <= 0.66 and normalised_y >= 0.33 and normalised_y <= 0.66 :
		return 5
	elif normalised_x > 0.66 and normalised_x <= 1 and normalised_y >= 0.33 and normalised_y <= 0.66:
		return 6
	elif normalised_x <= 0.33 and normalised_y >= 0.66 and normalised_y <= 1:
		return 7
	elif normalised_x > 0.33 and normalised_x<= 0.66 and normalised_y >= 0.66 and normalised_y <= 1 :
		return 8
	elif normalised_x > 0.66 and normalised_x <= 1 and normalised_y >= 0.66 and normalised_y <= 1:
		return 9
	else:
		#  print ("Item zone invalid!")
		return 0



"""
This function is now mainly used for sending the OSC. 
"""
def findZonesCoordinates(keypoints, frame_row, frame_column):
	amount = len(keypoints)
	# init, because it has 9 zones. 
	blob_all_zone = np.zeros(9, dtype = int)
	blob_x = np.zeros(9)
	blob_y = np.zeros(9)
	sizes = np.zeros(9)
	for i in range(0, amount):
		# normalised the coordinate. 
		x = float(keypoints[i].pt[0]/frame_row)
		y = float(keypoints[i].pt[1]/frame_column)
		# Call function to detect which zone the point belongs to. 
		ids = whichZone(x, y)
		blob_all_zone[ids-1] = 1
		blob_x[ids -1] = x
		blob_y[ids - 1] = y
		sizes[ids - 1] = keypoints[i].size
	return blob_all_zone, blob_x, blob_y, sizes


"""
Blob Detection Function
"""	
def findBlobs(image, frame_row):
	# Setup SimpleBlobDetector parameters
	blobParams = cv2.SimpleBlobDetector_Params()
	# Change thresholds
	blobParams.minThreshold = 0
	blobParams.maxThreshold = 128

	# Filter by Area. 
	blobParams.filterByArea = True
	blobParams.minArea = frame_row * frame_row / 100 
	blobParams.maxArea = frame_row * frame_row / 16 + 200

	# Filter by Circularity
	blobParams.filterByCircularity = False
	# Filter by Convexity
	blobParams.filterByConvexity = False
	# blobParams.minConvexity = 0.8
	# Filter by Inertia
	blobParams.filterByInertia = False
	# Create a detector with the parameters
	blobVer = (cv2.__version__).split('.')
	if int(blobVer[0]) < 3:
		detector = cv2.SimpleBlobDetector(blobParams)
	else:
		detector = cv2.SimpleBlobDetector_create(blobParams)
	# Detect Blobs
	# Keypoint documentation
	#http://docs.opencv.org/modules/features2d/doc/common_interfaces_of_feature_detectors.html#Point2f%20pt
	keypoints = detector.detect(255-image)
	print "keypoint", keypoints
	return keypoints



# -------------------------------------------------------------------#

# Blob detection contains 3 parts:
# 1. Thresholding the image, black and white is an edges process
# 2. findBlobs() use blob detection to extract the keypoints of the blobs
# 3. send OSC. Send XY, Amount, Size, Zone to PureData
def blobDetection(img, threshold_black,  frame_row, \
	frame_column):
	# Convert to binary for blob tracking
	ret, black_blob = cv2.threshold(255-img, threshold_black, 255, cv2.THRESH_BINARY)
	print "black blob",black_blob
	keypoints_black = findBlobs(black_blob, frame_row)


	black_keypoint_amount = len(keypoints_black)
	print "key point amount ", black_keypoint_amount
	zones, x , y, sizes = findZonesCoordinates(keypoints_black, frame_row, frame_column)
	zones[np.argmax(sizes)] = 2 # Make the largest 2. 
	sortedZone = np.nonzero(zones)[0]  + 1
	# arguments: keypoints, blob amount, 1 for black 2 for white
	# OSC communication
	# oscPart.sendBlobs(zones, sortedZone, combo, x , y, black_keypoint_amount)
	# OscPart.sendBlobs2 (zones, sortedZone, x, black_keypoint_amount)

	# oscPart.sendBlobsViaOsc(keypoints_black, black_keypoint_amount, combination, 1, frame_row, frame_column, choice)

	#Draw detected blobs as red circles. 
	return keypoints_black, black_blob, zones



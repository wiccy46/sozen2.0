
"""
Zen Garden Ambient Soundscape
Designed by Jiajun Yang, Bielefeld University, 2017.

This is v2. Which includes a new musical mode. The GUI is reimplemented in QT. Sound will be
potentially controlled within python in a pure sample based trigger system through PYO.

It uses a standard webcam to extract stone and sand features of the zen garden and send the
information to PureData via OSC

Module required: OpenCV2, Numpy, matplotlib, PyOSC, pyserial
Subfiles: oscPart, stones, sands

Based on choice (1:2), the program can process either webcam image or saved image files. During the camera
extraction, the feature extraction functions are not ran constantly. Instead, the program takes a snapshot
everytime the user removes the hand from the captured area based on the frame differences. 

At the beginning of the program, one shall crop the image (both webcam and file) by choosing the 4 corner of the 
intended area. The user shall start from the top left corner --> top right --> bottom left --> bottom right (Z shape).

The python part only manage feature extraction, the Soundscape is generated/triggered entirely on the PureData. 
For information about the Soundscape, please refers to the PD patches. 
"""


import cv2, sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import os, time
from PyQt4 import QtGui, QtCore
# from lib.OscPart import OscPart    # Handle OSC communication
# from lib.Stones import Stones
# from lib.Sands import Sands


# Sakura: Only parameter you might need: 
cameraChoice = 0

# Important to choice the right mode
# 1: Camera, 2: stillImages
choice = 1
# 0: Dark, 1: Normal, 2: Bright
labLighting = 2
if choice == 1:
	ratio  = 2
	fontSize = 2
	# sometime 0 sometime 1 depends on your camera list
	# cap = cv2.VideoCapture(cameraChoice)
	# serial communication used for lighting. 
	# ser = serial.Serial(port = '/dev/cu.usbserial-AD023UK4')
else:
	ratio = 1
	fontSize = 1
	# Change to the dir of your folder. 
	os.chdir ("./imgsx")
	# Picture dimension: 600 x 800. 


# Create a trackbar in case for parameter tweaking
def nothing(x):
	pass



class Capture():
	def __init__(self):
		self.capturing = False
		self.cameraChoice = 0
		self.c = cv2.VideoCapture(cameraChoice)
		print "init complete"

	def changeCamera(self, choice):
		cameraChoice = choice
		self.c = cv2.VideoCapture(cameraChoice)

	def startCapture(self):
		print "start"
		self.capturing = True
		print self.c
		cap = self.c
		while(self.capturing):
			ret, frame = cap.read()
			cv2.imshow("Capture", frame)
			cv2.waitKey(200)

	def endCapture(self):
		print "end"
		self.capturing = False

	def quitCapture(self):
		print "quit"
		cap = self.c
		self.capturing = False
		cv2.destroyAllWindows()
		cap.release()
		QtCore.QCoreApplication.quit()

class Window(QtGui.QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.capture = Capture()
		self.setWindowTitle('SoZen v2.0')

		self.camera_choice_box = QtGui.QSpinBox()
		self.camera_choice_box.setValue(0)
		self.camera_choice_box.setRange(0, 4)
		self.camera_choice_box.setFixedWidth(60)
		self.camera_choice_box.setToolTip("Restart the camera after changing")
		self.camera_choice_box.valueChanged[int].connect(self.changeValue)

		self.start_button = QtGui.QPushButton('Start', self)
		self.start_button.clicked.connect(self.capture.startCapture)

		self.end_button = QtGui.QPushButton('End', self)
		self.end_button.clicked.connect(self.capture.endCapture)

		self.quit_button = QtGui.QPushButton('Quit', self)
		self.quit_button.clicked.connect(self.capture.quitCapture)
		self.setGeometry(100, 100, 200, 200)

		vbox = QtGui.QVBoxLayout(self)
		vbox.addWidget(self.start_button)
		vbox.addWidget(self.end_button)
		vbox.addWidget(self.quit_button)
		vbox.addWidget(self.camera_choice_box)

		self.setLayout(vbox)
		self.setGeometry(100, 100, 200, 200)
		self.show()

	def changeValue(self, value):
		if self.sender() == self.camera_choice_box:
			self.capture.changeCamera(value)





def main():
	app = QtGui.QApplication(sys.argv)
	sozen = Window()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
"""

trackbarWindowName = "Trackbars"
cv2.namedWindow(trackbarWindowName, cv2.cv.CV_WINDOW_NORMAL)
cv2.resizeWindow(trackbarWindowName, 400, 150)



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


#ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C
def adaptiveGaussian(inputImage, row, column):
	th3 = cv2.adaptiveThreshold(inputImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,15,6)
	cv2.imshow('adaptiveGaussian',\
		cv2.resize(th3, None, fx = 0.75, fy = 0.75, interpolation = cv2.INTER_AREA))


def lightingCondition(option):
	if option == 0:
		blackThreInit = 225
		whiteThreInit = 83


	elif option == 1:
		blackThreInit = 190
		whiteThreInit = 170

	else:
		blackThreInit = 183
		whiteThreInit = 186 
	return blackThreInit, whiteThreInit

"""

"""	
def camera():
	global snapshotFlag, ratio, labLighting
	textColor = 255
	initBrightness = 40
	# Create a previous frame buffer
	# ser.write(chr(initBrightness)+chr(initBrightness)+chr(initBrightness)+chr(initBrightness)+chr(0))
	# time.sleep(.5) # Coupe with the delay to Arudino
	ret, original_img = cap.read()
	original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
	# Left and now is wrongly flip. 
	original_img = cv2.flip(original_img, 0)
	original_img = cv2.flip(original_img, 1)
	calibration_points = getCalibrationCoordinates(original_img)
	# ser.write(chr(0)+chr(0)+chr(0)+chr(0)+chr(0)) # Switch leds off
	prev_video = np.array([])
	snapshotFlag = False
	justSnap = False # A flag that indicates a just snap is happened. 

	# The threshold should be based on sand density and std. 
	threshold_black = 0
	threshold_white = 0
	snap_thres = 8.0
	# This part is used temporally for the lab demostration.
	# Depending on the lighting condition. The initial thresholds of the bold detections will alter. 
	
	# Get initial lighting threshold for the slider. 
	blackThreInit, whiteThreInit = lightingCondition(labLighting)

		
	# -------------------------------------#	
	# Create sliders for parameter control
	cv2.createTrackbar("threshold_black", trackbarWindowName, blackThreInit, 240, nothing)
	cv2.createTrackbar("threshold_white", trackbarWindowName, whiteThreInit, 240, nothing)
	cv2.createTrackbar("lineRho", trackbarWindowName, 8, 20, nothing)
	cv2.createTrackbar("lineTheta", trackbarWindowName, 179, 360, nothing)
	cv2.createTrackbar("cannyMin", trackbarWindowName, 31, 250, nothing)
	cv2.createTrackbar("cannyMax", trackbarWindowName, 48, 250, nothing)
	cv2.createTrackbar("circleP1", trackbarWindowName, 30, 100, nothing)
	cv2.createTrackbar("circleP2", trackbarWindowName, 50, 100, nothing)
	cv2.createTrackbar("brightness", trackbarWindowName, 40, 150, nothing) # Range between 0 ~ 255
	cv2.createTrackbar("lineLenFac", trackbarWindowName, 25, 40, nothing)
	cv2.createTrackbar("lineGapFac", trackbarWindowName, 65, 80, nothing)

	# Here comes the main loop
	while True:
		ret,original_img = cap.read()
		# Transform video into greyscale
		# Left and now is wrongly flip. 
		# Throw an exception: cv2.error. Then jump to the end of the loop/ 
		img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
		img = cv2.flip(img, 0)
		img = cv2.flip(img, 1)
		# The unscaled image is used for 
		# scaleratio = 1.0 / ratio

		# Calibrate perspective.
		img = calibrate(img, calibration_points)
		row, column = np.shape(img)[0], np.shape(img)[1]

		# Retriving parameters.. 
		threshold_black = cv2.getTrackbarPos("threshold_black", trackbarWindowName)
		threshold_white = cv2.getTrackbarPos("threshold_white", trackbarWindowName)
		lineRho = cv2.getTrackbarPos("lineRho", trackbarWindowName)
		lineTheta = cv2.getTrackbarPos("lineTheta", trackbarWindowName)
		cannyMin = cv2.getTrackbarPos("cannyMin", trackbarWindowName)
		cannyMax = cv2.getTrackbarPos("cannyMax", trackbarWindowName)
		p1 = cv2.getTrackbarPos("circleP1", trackbarWindowName)
		p2 = cv2.getTrackbarPos("circleP2", trackbarWindowName)
		brightness = cv2.getTrackbarPos("brightness", trackbarWindowName)
		lineLenFac = cv2.getTrackbarPos("lineLenFac", trackbarWindowName)
		lineGapFac = cv2.getTrackbarPos("lineGapFac", trackbarWindowName)

	
		try:
			# Calculate the frame difference
			diff = cv2.absdiff(img, prev_video)
			mean_diff = float(np.mean(diff))

			# If a snap was just taken in the previous loop. By pass the mean_diff.
			# Because the difference between light_on and light_off is too big 
			# even if there is nothing changed on the zen garden. 
			if justSnap:
				mean_diff = 3.0
				justSnap = False
			# print mean_diff

			try:
			
				if (snapshotFlag == False) & (mean_diff > snap_thres) :
					snapshotFlag = True

				elif (snapshotFlag == True) & (mean_diff < snap_thres):
					# Take a snapshot
					# Wait 2 seconds to make sure the hand is moved away from the camera area
					time.sleep(1.5)
					print "SNAPPED!"
					# ser.write(chr(brightness)+chr(brightness)+chr(brightness)+chr(brightness)+chr(0))
					# time.sleep(0.5) # Coupe with the delay to Arudino
					ret,original_img = cap.read()
					# Transform video into greyscale
					img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
					img = cv2.flip(img, 0)
					img = cv2.flip(img, 1)
					img = calibrate(img, calibration_points)
					row, column = np.shape(img)[0], np.shape(img)[1]

		#---------------------------------------------------------------------------------------------------#
		# First step, stone detection
					keypoints_black, black_blob = stones.blobDetection(img, \
						threshold_black, threshold_white, row, column, choice)
					# Extract blob coordinates
					bblob_coordinates = stones.findCoordinates(keypoints_black)
					# Return the diameter of the blob. 
					bblob_sizes = stones.findSize(keypoints_black)

		# Draw circles for blob
					img = cv2.drawKeypoints(img, \
						keypoints_black, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		#---------------------------------------------------------------------------------------------------#
		# Line Detection here
					img = cv2.medianBlur(img,1)   # Not sure if necessary
					lines, edges = sands.lineDetection(img, lineRho, lineTheta, cannyMin, cannyMax,\
						lineLenFac, lineGapFac, row)
					# Need to add error exception 
					try:
						lines = sands.removeBlobLines(lines, bblob_coordinates, bblob_sizes)
						lines_center = sands.findLineCenter(lines)
						lines_zone, lines_hist = sands.findZone(lines_center, row, column)
						lines_angle = sands.findAngle(lines)
						lines_angAvg = sands.angleAverage(lines_angle, lines_zone)
						oscPart.sendSands(lines_hist, lines_angAvg)
					except TypeError:
						"No stones found!"
		# # --------------------------------------------------------------------------------------------------#
					try: 
						for eachLine in lines:
							for x1,y1,x2,y2 in lines:
								cv2.line(img,(x1,y1),(x2,y2),(15,15,200),2)
					except TypeError:
						print "No line found!"

					# Display parameters. 
					bblobStr = "Tr_b: " + str(threshold_black) 
					rhoStr = "rho: " + str(lineRho + 1) 
					thetaStr = "theta: " + str(lineTheta + 1) 
					cMin = "CannyMin: " + str (cannyMin + 1)
					cMax = "CannyMax: " + str (cannyMax + 1)
					lineLenFacStr = "lineLenFac: " + str (lineLenFac )
					lineGapFacStr = "lineGapFac: " + str (lineGapFac )
					brightnessStr = "brightness" + str (brightness)

					cv2.putText(img, rhoStr, (10 , 20 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
					cv2.putText(img, thetaStr, (10 , 40 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
					cv2.putText(img, cMin, (10 , 60 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
					cv2.putText(img, cMax, (10 , 80 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
					cv2.putText(img, bblobStr, (10 , 100 ), cv2.FONT_HERSHEY_PLAIN, fontSize,  textColor)
					cv2.putText(img, lineLenFacStr, (10 , 120 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
					cv2.putText(img, lineGapFacStr, (10 , 140 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
					cv2.putText(img, brightnessStr, (10 , 160 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
					# Show edges, result image, and blobs
					cv2.imshow('edges',cv2.resize(edges, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_AREA))
					cv2.imshow('Black', cv2.resize(black_blob, None, \
						fx = 0.5, fy = 0.5, interpolation = cv2.INTER_AREA))
					cv2.imshow('Results', cv2.resize(img, None, \
						fx = 0.5, fy = 0.5, interpolation = cv2.INTER_AREA))

					# Reset flags. 
					snapshotFlag =False
					justSnap = True
					# ser.write(chr(0)+chr(0)+chr(0)+chr(0)+chr(0)) # Switch leds off
				elif (snapshotFlag == True) & (mean_diff > snap_thres): 
					pass
				else: 
					pass

			except UnboundLocalError:
				pass

		except ValueError:
			pass
		except cv2.error:
			pass

		# Record the previous frame. 
		prev_video = img.copy()

		# Put all send OSC here. 

		if cv2.waitKey(500) & 0xff == 27:
			cv2.destroyAllWindows()
			break




def stillImage():
	print "still image mode loaded"
	# filename = "horizontal.png"
	filename = 'f2.png'
	viewRate = 1
	textColor = 255
	img = cv2.imread(filename,0)
	cpts = getCalibrationCoordinates(img)
	# Create trackbars for parameters

	cv2.createTrackbar("threshold_black", trackbarWindowName, 179, 200, nothing)
	cv2.createTrackbar("threshold_white", trackbarWindowName, 160, 200, nothing)
	cv2.createTrackbar("lineRho", trackbarWindowName, 8, 20, nothing)
	cv2.createTrackbar("lineTheta", trackbarWindowName, 179, 360, nothing)
	cv2.createTrackbar("cannyMin", trackbarWindowName, 22, 250, nothing)
	cv2.createTrackbar("cannyMax", trackbarWindowName, 48, 250, nothing)
	# cv2.createTrackbar("circleP1", trackbarWindowName, 30, 100, nothing)
	# cv2.createTrackbar("circleP2", trackbarWindowName, 50, 100, nothing)
	cv2.createTrackbar("lineLenFac", trackbarWindowName, 13, 40, nothing)
	cv2.createTrackbar("lineGapFac", trackbarWindowName, 65, 80, nothing)

	while True:
		img = cv2.imread(filename,0)
		img = calibrate(img, cpts)

		# Retrive parameters. 
		threshold_black = cv2.getTrackbarPos("threshold_black", trackbarWindowName)
		threshold_white = cv2.getTrackbarPos("threshold_white", trackbarWindowName)
		lineRho = cv2.getTrackbarPos("lineRho", trackbarWindowName)
		lineTheta = cv2.getTrackbarPos("lineTheta", trackbarWindowName)
		cannyMin = cv2.getTrackbarPos("cannyMin", trackbarWindowName)
		cannyMax = cv2.getTrackbarPos("cannyMax", trackbarWindowName)
		lineLenFac = cv2.getTrackbarPos("lineLenFac", trackbarWindowName)
		lineGapFac = cv2.getTrackbarPos("lineGapFac", trackbarWindowName)

		row, column =  np.shape(img)[0], np.shape(img)[1]
		# Stone tracking. 
		keypoints_black, black_blob = stones.blobDetection(img, \
			threshold_black, threshold_white, row, column, choice)

		bblob_coordinates = stones.findCoordinates(keypoints_black)		
		bblob_sizes = stones.findSize(keypoints_black) # Diameter Use it for getting rid of lines detected in that area.  

		# Draw circles for blob
		img = cv2.drawKeypoints(img, \
			keypoints_black, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# ---------------------------------------------------------------------------------------------------#
# Line Detection here
		img = cv2.medianBlur(img,3)   # Not sure if necessary
		lines, edges = sands.lineDetection(img, lineRho, lineTheta, cannyMin, cannyMax,\
			lineLenFac, lineGapFac, row)
		lines = sands.removeBlobLines(lines, bblob_coordinates, bblob_sizes)
		lines_center = sands.findLineCenter(lines)
		lines_zone, lines_hist = sands.findZone(lines_center, row, column)
		lines_angle = sands.findAngle(lines)
		lines_angAvg = sands.angleAverage(lines_angle, lines_zone)
		# I need to figure out the range of lines_hist in order to have a more precise mapping.
		# print "Histogram map is : "
		# print lines_hist
		# print lines_angle
		oscPart.sendSands(lines_hist, lines_angAvg)
# # --------------------------------------------------------------------------------------------------#
		try: 		
			for x1,y1,x2,y2 in lines:
				cv2.line(img,(x1,y1),(x2,y2),(15,15,200),2)
		except TypeError:
			print "No line found!"

		# Display parameters. 
		bblobStr = "Tr_b: " + str(threshold_black) 
		rhoStr = "rho: " + str(lineRho + 1) 
		thetaStr = "theta: " + str(lineTheta + 1) 
		cMin = "CannyMin: " + str (cannyMin + 1)
		cMax = "CannyMax: " + str (cannyMax + 1)
		lineLenFacStr = "lineLenFac: " + str (lineLenFac + 1)
		lineGapFacStr = "lineGapFac: " + str (lineGapFac + 1)
		cv2.putText(img, rhoStr, (10 , 20 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
		cv2.putText(img, thetaStr, (10 , 40 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
		cv2.putText(img, cMin, (10 , 60 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
		cv2.putText(img, cMax, (10 , 80 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
		cv2.putText(img, bblobStr, (10 , 100 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
		cv2.putText(img, lineLenFacStr, (10 , 120 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
		cv2.putText(img, lineGapFacStr, (10 , 140 ), cv2.FONT_HERSHEY_PLAIN, fontSize, textColor)
		# Show edges, result image, and blobs
		cv2.imshow('edges',cv2.resize(edges, None\
			, fx = viewRate, fy = viewRate, interpolation = cv2.INTER_AREA))
		cv2.imshow('Black', cv2.resize(black_blob, None, \
			fx = viewRate, fy = viewRate, interpolation = cv2.INTER_AREA))
		cv2.imshow('Results', cv2.resize(img, None,\
			fx = viewRate, fy = viewRate, interpolation = cv2.INTER_AREA))
		if cv2.waitKey(200000) & 0xff == 27:
			cv2.destroyAllWindows()
			break

print ("Press Esc to Quit")
if choice == 1:
	camera()
elif choice == 2:
	stillImage()
else:
	print "Program Quited, Invalid Input"

# Switch off the soundSwitch in PD. 
oscPart.closeup()
# Need to add a program stop

"""








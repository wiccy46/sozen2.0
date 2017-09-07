
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
extraction, the feat
Based on choice (1:2), the program can process either webcam image or saved image files. During the camerure extraction functions are not ran constantly. Instead, the program takes a snapshot
everytime the user removes the hand from the captured area based on the frame differences. 

At the beginning of the program, one shall crop the image (both webcam and file) by choosing the 4 corner of the 
intended area. The user shall start from the top left corner --> top right --> bottom left --> bottom right (Z shape).

The python part only manage feature extraction, the Soundscape is generated/triggered entirely on the PureData. 
For information about the Soundscape, please refers to the PD patches. 



"""


import cv2, sys, time
import numpy as np
from PyQt4 import QtGui, QtCore
import lib.Stones, lib.DevMode
from lib.CameraCalibration import getCalibrationCoordinates, calibrate
from lib.findLines import detect_lines
from lib.MusGen import MusGen
import matplotlib.pyplot as plt
global calibration_pts


cameraChoice = 0
choice = lib.DevMode.devChoice()



class Capture():
    def __init__(self,calibration_pts,black_val_percent,theme,sound_source = 'python'):        
        self.capturing = False  # Flag for frame difference capture. 
        self.cameraChoice = 0
        #self.c = cv2.VideoCapture(cameraChoice)
        self.textColor = 255
        self.initBrightness = 40
        self.calibration_pts = calibration_pts
        self.threshold_black = black_val_percent
        self.snap_thres = 8.0  # the mean difference value which allows snapshot to be taken. 
        self.just_snapped = False
        self.snapshot_flag = False
        self.snapshot_time_gap = 1.5  # Wait certain second before actually taking the shot. 
        self.threshold_black_val = 0
        self.sound_source = sound_source
        self.theme=theme

    def changeCamera(self, choice):
        cameraChoice = choice
        self.c = cv2.VideoCapture(cameraChoice)

    

    def frame_adjust(self, f):
        f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        # Left and now is wrongly flip.
        f = cv2.flip(f, 0)

        f = cv2.flip(f, 1)
        return calibrate(f, self.calibration_pts)

    def startCapture(self):
        self.capturing = True
        self.c=cv2.VideoCapture(cameraChoice)
        rubbish, original_frame = self.c.read()  # ret is useless
        original_frame = self.frame_adjust(original_frame)
        previous_frame = np.array([])
        self.just_snapped = False
        self.snapshot_flag = False
        while(self.capturing):
            ret, frame = self.c.read()
            frame = self.frame_adjust(frame)
            try:
                diff = cv2.absdiff(frame, previous_frame)
                mean_diff = float(np.mean(diff))
                print "previous frame", previous_frame
                print "mean diff",mean_diff
                if self.just_snapped:
                    mean_diff = 3.0
                    self.just_snapped = False

                try:
                    if(self.snapshot_flag == False) & (mean_diff > self.snap_thres):
                        print ("Mean Diff: " + str(mean_diff))
                        self.snapshot_flag = True
                    elif(self.snapshot_flag == True) & (mean_diff < self.snap_thres):

                        # Take a snap shot
                        time.sleep(self.snapshot_time_gap) # wait a bit
                        ret, frame = self.c.read()
                        frame = self.frame_adjust(frame)
                      
                        row,column = np.shape(frame)[0], np.shape(frame)[1]
                        mean_value= np.mean(frame)
                        self.threshold_black_val = mean_value + (self.threshold_black/100)* mean_value
                        print self.threshold_black_val
                        print "frame", frame
                        print "row", row
                        #print "columncolumn
                        self.keypoints, self.black_blob, self.blob_zones = lib.Stones.blobDetection(frame,\
                                        self.threshold_black_val,  row, column)
                        print "key points"
                        print self.keypoints
                        # Extract blob coordinates
                        self.bblob_coordinates = lib.Stones.findCoordinates(self.keypoints)
                        # Return the diameter of the blob.
                        self.bblob_sizes = lib.Stones.findSize(self.keypoints)
                        print " Checkout the sizes of the stones "
                        print self.bblob_sizes.shape

                        # Needs to put a mode selection: soundscapes, music, 
                        self.music = MusGen(self.blob_zones, self.sound_source)
                        self.music.start()
                        # Draw circles for blob
                        frame = cv2.drawKeypoints(frame, self.keypoints, np.array([]), (0, 255, 0),
                                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    # ---------------
                        cv2.imshow('Results', cv2.resize(frame, None, \
                            fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))
                        cv2.imshow('Black', cv2.resize(self.black_blob, None, \
                            fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))
                        self.snapshot_flag = False
                        self.just_snapped = True

                    elif (self.snapshot_flag == True) & (mean_diff > self.snap_thres):
                        pass
                    else:
                        pass
                except UnboundLocalError:
                    pass
            except ValueError:
                pass
            except cv2.error:
                pass
            previous_frame = frame.copy()
            cv2.waitKey(400)

    def endCapture(self):
        print ("Stop")
        self.capturing = False
        try:
            self.music.stop_play()
            self.music.stopit()
        except AttributeError:
            pass

    def quitCapture(self):
    	print "inside quit capture"
        cap = self.c
        self.capturing = False
        cv2.destroyAllWindows()
        try:
            self.music.stop_play()
            self.music.stopit()
        except AttributeError:
            pass
        cap.release()
        QtCore.QCoreApplication.quit()

class Window(QtGui.QWidget):
    def __init__(self):

        super(Window, self).__init__()
        self.setWindowTitle('SoZen v2.0')
        self.capture=0
        self.theme = "Forest"
        self.camera_choice_box = QtGui.QSpinBox()
        self.camera_choice_box.setValue(0)
        self.camera_choice_box.setRange(0, 4)
        self.camera_choice_box.setFixedWidth(60)
        self.camera_choice_box.setToolTip("Restart the camera after changing")
        self.camera_choice_box.valueChanged[int].connect(self.changeValue)
        self.camera_choice_laybel = QtGui.QLabel('Camera')
        self.camera_choice_laybel.setFixedSize(50, 20)
        #self.capture = 0
        self.thresholdPercent = 30
        self.start_button = QtGui.QPushButton('Start', self)
        self.start_button.setCheckable(True)
        self.start_button.setFixedWidth(250)
        self.start_button.clicked.connect(self.startButton)
        	
        	

        self.end_button = QtGui.QPushButton('Stop', self)
        self.end_button.setCheckable(True)
        self.end_button.setFixedWidth(250)
        self.end_button.clicked.connect(self.endButton)

        self.quit_button = QtGui.QPushButton('Quit', self)
        self.quit_button.setCheckable(True)
        self.quit_button.setFixedWidth(250)
        self.quit_button.clicked.connect(self.quitButton)

        self.bt_laybel = QtGui.QLabel('Blob Threshold')
        self.bt_laybel.setFixedSize(90, 20)
        self.bt_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.bt_laybel.setAlignment(QtCore.Qt.AlignCenter)
        self.bt_slider.setRange(0, 100)
        self.bt_slider.setValue(30) # Need to change here.
        self.bt_slider.valueChanged[int].connect(self.changeValue)
        self.bt_slider.setFixedSize(100,20)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.bt_laybel)
        hbox.addWidget(self.bt_slider)
        hboxCamera = QtGui.QHBoxLayout()
        hboxCamera.addWidget(self.camera_choice_laybel)
        hboxCamera.addWidget(self.camera_choice_box)
        
        lbox = QtGui.QVBoxLayout(self)
        
        lbox.addWidget(self.start_button)
        lbox.addWidget(self.end_button)
        lbox.addWidget(self.quit_button)
        lbox.addLayout(hbox)
        lbox.addLayout(hboxCamera)
        #
        #
        # rbox = QtGui.QGridLayout(self)
        # rbox.addWidget(self.bt_laybel, 1, 0)
        # rbox.addWidget(self.bt_slider,1,1)
        #
        #
        # box = QtGui.QHBoxLayout(self)
        # box.addLayout(lbox)
        # box.addLayout(rbox)
        
      	verticalradio = QtGui.QVBoxLayout(self)
      	self.label = QtGui.QLabel("Select the theme", self)
      	
      	verticalradio.addWidget(self.label)
      	radiobutton = QtGui.QHBoxLayout()
      	
      	self.r1 = QtGui.QRadioButton("Forest")
      	self.r1.setChecked(True)
      	self.r1.toggled.connect(lambda:self.btnstate(self.r1))
      	radiobutton.addWidget(self.r1)
		
      	self.r2 = QtGui.QRadioButton("Sea")
      	self.r2.toggled.connect(lambda:self.btnstate(self.r2))
      	radiobutton.addWidget(self.r2)
      	radiobutton1 = QtGui.QHBoxLayout()
      	self.r3 = QtGui.QRadioButton("Fireplace")
      	self.r3.toggled.connect(lambda:self.btnstate(self.r3))
      	radiobutton1.addWidget(self.r3)

      	self.r4 = QtGui.QRadioButton("Electronic")
      	self.r4.toggled.connect(lambda:self.btnstate(self.r4))
      	radiobutton1.addWidget(self.r4)
      	verticalradio.addLayout(radiobutton)
      	verticalradio.addLayout(radiobutton1)

        
      	lbox.addLayout(verticalradio)
      	self.setLayout(lbox)

        self.setFixedSize(300, 300)
        self.show()
    def btnstate(self,b):
    	
		
    	if b.text() == "Forest":
         if b.isChecked() == True:
            self.theme="Forest"
         else:
            print b.text()+" is deselected"
        if b.text() == "Sea":
         if b.isChecked() == True:
            self.theme="Sea"
         else:
            print b.text()+" is deselected"
        if b.text() == "Fireplace":
         if b.isChecked() == True:
            self.theme="Fireplace"
         else:
            print b.text()+" is deselected"
        if b.text() == "Electronic":
         if b.isChecked() == True:
            self.theme="Electronic"
         else:
            print b.text()+" is deselected"
				

	 
    def startButton(self):

    	calibration_pts = getCalibrationCoordinates(cameraChoice)
        if(calibration_pts.any()):
        	self.capture = Capture(calibration_pts,self.thresholdPercent,self.theme)
        	self.capture.startCapture()
    def endButton(self):
    	if(self.end_button.isChecked()):
    		if(self.capture == 0):
    			QtCore.QCoreApplication.quit()
    		else:
    			self.capture.endCapture()
    def quitButton(self):
    	if(self.quit_button.isChecked()):
    		print self.capture
    		if(self.capture == 0):
    			QtCore.QCoreApplication.quit()
    		else:
    			self.capture.quitCapture()
    def changeValue(self, value):
        if self.sender() == self.camera_choice_box:
            self.capture.changeCamera(value)

        elif self.sender() == self.bt_slider:
            self.thresholdPercent = value


# calibration_pts = getCalibrationCoordinates(cameraChoice)

def main():
	#calibration_pts = getCalibrationCoordinates(cameraChoice)
	app = QtGui.QApplication(sys.argv)
	sozen = Window()
	sys.exit(app.exec_())
if __name__ == '__main__':
    main()

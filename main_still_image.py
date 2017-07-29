


import cv2, sys, time
import numpy as np
from PyQt4 import QtGui, QtCore
import lib.Stones, lib.DevMode
from lib.CameraCalibration import getCalibrationCoordinates, calibrate
from lib.MusGen import MusGen
import matplotlib.pyplot as plt
global calibration_pts


choice = lib.DevMode.devChoice()
os.chdir('./imgs') # load image. 


class Still_Image():
    def __init__(self,calibration_pts):        
        self.capturing = False  # Flag for frame difference capture. 
        self.textColor = 255
        self.initBrightness = 40
        self.calibration_pts = calibration_pts
        self.threshold_black = 183


    def changeCamera(self, choice):
        pass

    def changeBt(self, val):
        self.threshold_black = val


    def frame_adjust(self, f):
        f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        f = cv2.flip(f, 0)
        return cv2.flip(f, 1)

    def startCapture(self):
        self.capturing = True
        filename = 'f3.png'
        frame = cv2.imread(filename, 0)
        frame = self.frame_adjust(frame)
        row,column = np.shape(frame)[0], np.shape(frame)[1]
        checkThreshold = np.mean(frame) + 0.3* np.mean(frame)
        print "Check threshold value "
        print checkThreshold
        while(self.capturing):

                        print "Check threshold value "
                        print checkThreshold
                        self.threshold_black=checkThreshold

                        # plt.hist(frame)
                        # plt.title("Histogram for automatic threshold selection")
                        # plt.show();
                        print np.mean(frame)
                        self.keypoints, self.black_blob, self.blob_zones = lib.Stones.blobDetection(frame,\
                                                self.threshold_black,  row, column)
                        # Extract blob coordinates
                        self.bblob_coordinates = lib.Stones.findCoordinates(self.keypoints)
                        # Return the diameter of the blob.
                        self.bblob_sizes = lib.Stones.findSize(self.keypoints)


                        # Needs to put a mode selection: soundscapes, music, 
                        self.music = MusGen(self.blob_zones)
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
        self.camera_choice_box = QtGui.QSpinBox()
        self.camera_choice_box.setValue(0)
        self.camera_choice_box.setRange(0, 4)
        self.camera_choice_box.setFixedWidth(60)
        self.camera_choice_box.setToolTip("Restart the camera after changing")
        self.camera_choice_box.valueChanged[int].connect(self.changeValue)
        self.camera_choice_laybel = QtGui.QLabel('Camera')
        self.camera_choice_laybel.setFixedSize(50, 20)
        #self.capture = 0
        self.start_button = QtGui.QPushButton('Start', self)
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.startButton)
        
        	
        	

        self.end_button = QtGui.QPushButton('Stop', self)
        self.end_button.setCheckable(True)
        self.end_button.clicked.connect(self.endButton)

        self.quit_button = QtGui.QPushButton('Quit', self)
        self.quit_button.setCheckable(True)
        self.quit_button.clicked.connect(self.quitButton)

        lbox = QtGui.QGridLayout(self)
        lbox.addWidget(self.start_button, 1,0, 1,1)
        lbox.addWidget(self.end_button, 2, 0, 2, 1)
        lbox.addWidget(self.quit_button, 3, 0, 3, 1)
        lbox.addWidget(self.camera_choice_laybel, 5, 0)
        lbox.addWidget(self.camera_choice_box, 5, 1)
        # self.bt_laybel = QtGui.QLabel('Blob Threshold')
        # self.bt_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        # self.bt_slider.setRange(0, 255)
        # self.bt_slider.setValue(183) # Need to change here.
        # self.bt_slider.valueChanged[int].connect(self.changeValue)
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
        self.setLayout(lbox)
        self.setGeometry(100, 100, 400, 400)
        self.show()
    def startButton(self):
    	if(self.start_button.isChecked()):
    		calibration_pts = getCalibrationCoordinates(cameraChoice)
        	if(calibration_pts.any()):
        		self.capture = Capture(calibration_pts)
        		print self.capture
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
            self.capture.changeBt(value)


# calibration_pts = getCalibrationCoordinates(cameraChoice)

def main():
	#calibration_pts = getCalibrationCoordinates(cameraChoice)
	app = QtGui.QApplication(sys.argv)
	sozen = Window()
	sys.exit(app.exec_())
if __name__ == '__main__':
    main()

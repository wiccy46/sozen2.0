import cv2
import numpy as np
# import Tkinter

# def cropping(img):
	# Create a 


# Need 4 sliders for copping
# Need to invert image. 

def nothing(x):
	pass





# white = np.ones((400, 500, 3), dtype = np.int) * 255
white = np.zeros((200,600, 1), dtype = np.int)
trackbarWindowName = 'Sliders'
cv2.namedWindow(trackbarWindowName)
# Value range (0 ~ 50%)
cv2.createTrackbar('cMin', trackbarWindowName, 10, 255, nothing)
cv2.createTrackbar('cMax', trackbarWindowName, 200, 255, nothing)
cv2.createTrackbar('T', trackbarWindowName, 0, 50, nothing)
cv2.createTrackbar('B', trackbarWindowName, 0, 50, nothing)


cap = cv2.VideoCapture(0)

def click(event, )

def main():

	while True:	



		ret, img = cap.read()
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
		img = cv2.flip(img,0)


		edges = cv2.Canny(img,cMax,cMin)
		cv2.imshow('Edges', edges)

		cv2.imshow('Cropping', img)
		if cv2.waitKey(1000) & 0xff == 27:
				cv2.destroyAllWindows()
				break

main()



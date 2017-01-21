"""
OSC Conmmunication 
"""
import OSC
import numpy as np

def closeup():
	send_address = ('127.0.0.1', 9003)
	close_client = OSC.OSCClient()
	close_client.connect(send_address)
	bundle = OSC.OSCBundle()
	bundle.setAddress("close")
	bundle.append(0)
	close_client.send(bundle)

def sendSands(lines_hist, lines_angAvg):
	send_address = ('127.0.0.1', 9002)
	sand_client = OSC.OSCClient()
	sand_client.connect(send_address)
	bundle = OSC.OSCBundle()
	bundle.setAddress("linesHist")
	bundle.append((lines_hist[0], lines_hist[1], lines_hist[2], \
		lines_hist[3], lines_hist[4], lines_hist[5], \
		lines_hist[6], lines_hist[7], lines_hist[8]))
	bundle.setAddress("linesAng")
	bundle.append((lines_angAvg[0], lines_angAvg[1], lines_angAvg[2], \
		lines_angAvg[3], lines_angAvg[4], lines_angAvg[5], \
		lines_angAvg[6], lines_angAvg[7], lines_angAvg[8]))
	sand_client.send(bundle)

# -------------------------------------------------------------------#
"""
OSC function to send out blob information.

The zone should be in a format of "0 1 0 0 1 0 1 0 0" (1 = on for that zone and 0 = off)
"""
# This is currently used/. 
def sendBlobs2(zones, sortedZone, x, amount):
	# Put the granular parameters her this time, 
	# But later they should be picked up more intuitively. 
	speed = [60, 75, 90, 67]
	dur = [2700, 2700, 2700, 2700]
	pitch = [0.25, 1.0 , 0.5, 0.25]
	randomness = [25, 73, 50, 25]
	pos = [40, 35, 30, 20]
	# pos = [80,80, 80, 80]
	send_address = ('127.0.0.1', 9000)
	# Create OSC client
	blob_client = OSC.OSCClient()
	blob_client.connect(send_address)
	# Create message bundle
	bundle = OSC.OSCBundle()
	bundle.setAddress("amount")
	bundle.append(amount)
	bundle.setAddress("sampleSelection")
	bundle.append((zones[0], zones[1], zones[2], \
		zones[3], zones[4], zones[5], \
		zones[6], zones[7], zones[8]))
	bundle.setAddress("x")
	bundle.append((x[0], x[1], x[2], \
		x[3], x[4], x[5], \
		x[6], x[7], x[8]))
	# This bit will send out parameter presets for granular synth
	if (amount == 0):
		granSam = 0
	else:
		granSam = np.random.randint(0,3) + 1
	print "Gransam is " + str(granSam)
	bundle.setAddress("granularSample")
	bundle.append(granSam)
	bundle.setAddress("granular")
	bundle.append((speed[granSam], dur[granSam], pitch[granSam], randomness[granSam], pos[granSam]))
	for i in range(len(sortedZone)):
		bundle.setAddress("sortedZone")
		bundle.append(sortedZone[i])
	blob_client.send(bundle)


def sendBlobs(zones, sortedZone , combo, x, y, amount):
	send_address = ('127.0.0.1', 9000)
	# Create OSC client
	blob_client = OSC.OSCClient()
	blob_client.connect(send_address)
	# Create message bundle
	bundle = OSC.OSCBundle()
	bundle.setAddress("combination")
	bundle.append(combo)
	bundle.setAddress("amount")
	bundle.append(amount)
	# Maybe I will need a loop for that. 
	for i in range(len(zones)):
		bundle.setAddress("zones")
		bundle.append(zones[i])
		bundle.setAddress("x")
		bundle.append(x[i])
		bundle.setAddress("y")
		bundle.append(y[i])
	for i in range(len(sortedZone)):
		bundle.setAddress("sortedZone")
		bundle.append(sortedZone[i])
	blob_client.send(bundle)


# This is not used. 
def sendBlobsViaOsc(keypoints, amount, combination, color, frame_row, frame_column, choice):
	if choice == 1:
		maxBBSize = 140
		maxWBSize = 75
	else:
	 	maxBBSize = 1360
		maxWBSize = 700

	if (color == 1):
		send_address = ('127.0.0.1', 9000) # 9000: for black blobs
	else:
		send_address = ('127.0.0.1', 9001) # 9001: for white blobs

	# Create OSC client
	blob_client = OSC.OSCClient()
	blob_client.connect(send_address)
	# Create message bundle
	bundle = OSC.OSCBundle()

	# 1 is black, 2 is white 
	bundle.setAddress("Color")
	bundle.append(color)
	if color == 1:
		bundle.setAddress("BlackBlobAmount")
	else:
		bundle.setAddress("WhiteBlobAmount")

	if (amount != 0 ):
		bundle.append(amount)

		for i in range(0, amount):

			# Multiple blobs information sending 
			normalised_x = float(keypoints[i].pt[0]/frame_row)
			normalised_y = float(keypoints[i].pt[1]/frame_column)

			if normalised_x <= 0.33 and normalised_y < 0.33:
				zone = 1

			elif normalised_x > 0.33 and normalised_x <= 0.66 and normalised_y < 0.33:
				zone = 2

			elif normalised_x > 0.66 and normalised_x <= 1 and normalised_y < 0.33:
				zone = 3

			elif normalised_x <= 0.33 and normalised_y >= 0.33 and normalised_y <= 0.66:
				zone = 4

			elif normalised_x > 0.33 and normalised_x <= 0.66 and normalised_y >= 0.33 and normalised_y <= 0.66 :
				zone = 5

			elif normalised_x > 0.66 and normalised_x <= 1 and normalised_y >= 0.33 and normalised_y <= 0.66:
				zone = 6

			elif normalised_x <= 0.33 and normalised_y >= 0.66 and normalised_y <= 1:
				zone = 7

			elif normalised_x > 0.33 and normalised_x<= 0.66 and normalised_y >= 0.66 and normalised_y <= 1 :
				zone = 8

			elif normalised_x > 0.66 and normalised_x <= 1 and normalised_y >= 0.66 and normalised_y <= 1:
				zone = 9

			else:
				print ("Item zone invalid!")
				break


			bundle.setAddress("attr")
			if color == 1:

				normalised_size = keypoints[i].size / maxBBSize

			else:
				normalised_size = keypoints[i].size / maxWBSize


 			bundle.append((normalised_x, normalised_y, normalised_size, zone))

			# bundle.append((normalised_x, normalised_y, int(keypoints[i].size), zone))
		bundle.setAddress("combination")
		bundle.append(combination)
		blob_client.send(bundle)
	else:
		bundle.append(amount)
		blob_client.send(bundle)


# def sendDensity(density, sumDensity):
# 	send_address = ('127.0.0.1', 9002) # 9000: for black blobs
# 	# Create OSC client
# 	blob_client = OSC.OSCClient()
# 	blob_client.connect(send_address)
# 	# Create message bundle
# 	bundle = OSC.OSCBundle()

# 	# 1 is black, 2 is white
# 	# for i in len(density):
# 	# 	name = "densityZone" + str(i)
# 	# 	bundle.setAddress(name)
# 	# 	bundle.append(density[i])
# 	bundle.setAddress("density")
# 	bundle.append((density[0], density[1],density[2],density[3],density[4],\
# 		density[5],density[6],density[7],density[8]))
# 	bundle.setAddress("sumDensity")
# 	bundle.append(sumDensity)

# 	blob_client.send(bundle)



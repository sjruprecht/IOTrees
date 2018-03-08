import argparse
import numpy as np
import cv2
import json

try:
    import serial
    SEND_DATA = True
except ImportError:
    SEND_DATA = False

# To execute:
# python EAB_find.py --image EAB-on-purple-trap.jpg

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to image')
args = vars(ap.parse_args())

# Upper and lower rgb space for background
# Unused
# blueLower = np.array([100, 67, 0], dtype='uint8')
# blueUpper = np.array([167, 85, 91], dtype='uint8')

# Unused in the end. Delete me.
# blue = cv2.inRange(frame, blueLower, blueUpper)
# blue = cv2.GaussianBlur(blue, (3, 3), 0)

# Upper and lower rgb space for selecting background
# Don't be fooled by the name. Started gray, ended up everything but
grayLower = np.array([0, 0, 10], dtype='uint8')
grayUpper = np.array([125, 168, 125], dtype='uint8')

frame = cv2.imread(args['image'])

# Again, don't be fooled by the variable name.
# Not whitish as much as it selected out the background
whiteish = cv2.inRange(frame, grayLower, grayUpper)
whiteish = cv2.GaussianBlur(whiteish, (5, 5), 1)

# Now flip the background to be white, subject dark
opposite = cv2.bitwise_not(whiteish)

# Begin edge detection
canny = cv2.Canny(opposite, 30, 150)

# Find the contours
_, cnts, _ = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

bug_count = 0

# Count what we think are EABs by the number of corners
if len(cnts) > 0:
    for index, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # print(len(approx))

        if len(approx) < 10:
            cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[index]
            rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
            perimeter = cv2.arcLength(cnt, True)
            # print(perimeter)
            if perimeter > 150:
                bug_count += 1
                cv2.drawContours(frame, [rect], -1, (0, 255, 0), 2)

# Dummy data to send with the bug_count
outgoing = {"lat": "100", "lon": "100", "count": bug_count, "coverage": "55"}

# Set serial for digi dongle and send the data to digi
# Must send as bytestring
if SEND_DATA:
    s = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    s.write(str.encode(json.dumps(outgoing)))
else:
    print(outgoing)

# Optional stuff for showing what was counted as EAB
# cv2.imshow('Canny', canny)
# cv2.imshow('Tracking', frame)
# cv2.imshow('Opposite', opposite)
# cv2.imshow('whiteish', whiteish)
# cv2.waitKey(0)
#
# Z = frame.reshape()

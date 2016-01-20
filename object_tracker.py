# Import packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# Construct and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32, help="max buffer size")
args = vars(ap.parse_args())

# Define lower and upper boundaries for color detection in HSV color space
# Example defines green
colorLower = (29, 86, 6)
colorUpper = (64, 255, 255)

# Initialize list of tracked points, frame counter, and coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# If video not supplied, grab reference to webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# Otherwise, grab reference to video file
else:
    camera = cv2.VideoCapture(args["video"])

# Keep looping
while True:
    # Grab current frame
    (grabbed, frame) = camera.read()

    # If using video and no frame available, we have reached the end
    if args.get("video") and not grabbed:
        break

    # Resize frame, blur, and convert to HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Construct mask for color (ex. green) then dilate/erode
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in mask and initialize current (x, y) center of object
    cnts = cv2.findContours(mask,copy(), cv2,RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # Only proceed if at least one contour found
    if len(cnts) > 0:
        # Find largest contour in mask, use to compute enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if radius meets minimum size
        if radius > 10:
            # Draw circle and centroid on frame then update list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    # Loop over set of tracked points ????arange????
    for i in np.arange(1, len(pts)):
        # If either of tracked points are None, ignore them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # Check to see if enough points accumulated in buffer
        if counter >= 10 and i == 1 and pts[-10] is not None:
            # Compute difference between x and y and reinitialize text variables
            

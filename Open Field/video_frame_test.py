# Import packages
import numpy as np
import argparse
import cv2

# Construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to the image")
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

camera = cv2.VideoCapture(args["video"])
_, image = camera.read()

cv2.imshow("image", image)
cv2.waitKey(0)

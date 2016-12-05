# Import packages
import argparse
import datetime
import imutils
import time
import cv2

# Construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# If no video argument, read from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

# Otherwise, read from video file
else:
    camera = cv2.VideoCapture(args["video"])

# Initialize first frame in the video stream
firstFrame = None

# Loop through frames of video
while True:
    # Grab current frame and initialize the occupied/unoccupied text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    # If frame could not be grabbed, the end of video has been reached
    if not grabbed:
        print "End of video stream"
        break

    # Resize the frame, convert to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # If first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # Compute absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilate thresholded image to fill in holes, then find contours
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for c in cnts:
        # If contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # Compute bounding box for contour, draw on frame, and update text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    # Draw text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # Show frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, break from the loop
    if key == ord("q"):
        break

# Cleanup camera and close any open windows
camera.release()
cv2.destroyAllWindows()

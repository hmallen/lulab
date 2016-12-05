# Import packages
import argparse
import cv2
import os

# Initialize list of reference points and boolean to indicate cropping status
refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # Grab references to global variables
    global refPt, cropping
    #global refPt, cropping, tempEndpoint

    # If left mouse click, record (x, y) coordinates and indicate cropping being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # Check to see if left mouse button released
    elif event == cv2.EVENT_LBUTTONUP:
        # Record ending coordinates and indicate cropping finished
        refPt.append((x, y))
        cropping = False

        # Draw rectangle around ROI
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

    #if event == cv2.EVENT_MOUSEMOVE and cropping:
        #tempEndpoint = [(x, y)]

# Construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to the image")
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

camera = cv2.VideoCapture(args["video"])
_, image = camera.read()
clone = image.copy()

# Load image and setup mouse callback function
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# Keep looping until 'q' key is pressed
while True:
    # Display image and wait for key to be pressed
    if not cropping:
        cv2.imshow("image", image)
    #elif cropping and tempEndpoint:
        #cv2.rectangle(image, refPt[0], tempEndpoint[0], (0, 255, 0), 1)
        #cv2.imshow("image", image)
    
    key = cv2.waitKey(1) & 0xFF

    # If 'r' key pressed, reset cropping region
    if key == ord("r"):
        _, image = camera.read()

    # If 'c' key pressed, break from the loop
    elif key == ord("c"):
        break

# If there are 2 reference points, crop ROI and display
if len(refPt) == 2:    
    leftEdge = refPt[0][0]
    vidWidth = refPt[1][0] - leftEdge
    topEdge = refPt[0][1]
    vidHeight = refPt[1][1] - topEdge
    
    print "Left edge:    " + str(leftEdge)
    print "Video width:  " + str(vidWidth)
    print "Top edge:     " + str(topEdge)
    print "Video height: " + str(vidHeight)
    
    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)

    fileNumber = 0
    fileName = args["video"]

    while True:
        fileNumber += 1
        newFile = str(fileNumber) + '-' + fileName
        filePresent = os.path.isfile(newFile)
        print filePresent
        #newDir = fileName.split('.')[0]
        #if not os.path.exists(newDir):
            #os.makedirs(newDir)
        if not filePresent:
            break
    
    #cmdString = "ffmpeg -i " + args["video"] + ' -vf "crop=' + str(vidWidth) + ':' + str(vidHeight) + ':' + str(leftEdge) + ':' + str(topEdge) + '" ' + newDir + '/' + newFile
    cmdString = "ffmpeg -i " + args["video"] + ' -vf "crop=' + str(vidWidth) + ':' + str(vidHeight) + ':' + str(leftEdge) + ':' + str(topEdge) + '" ' + newFile

    os.system(cmdString)

# Close all open windows
cv2.destroyAllWindows()

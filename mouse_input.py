# Import packages
import numpy as np
import argparse
import cv2

# Initialize current frame of video with info --> ROI points & Input mode status
frame = None
roiPts = []
inputMode = False

def selectROI(event, x, y, flags, param):
    # Grab reference to current frame, list of ROI points, and input mode status
    global frame, roiPts, inputMode

    # If in ROI input mode, mouse clicked, and less than 4 points, update list of ROI points and draw circle
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts,append((x, y))
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.imshow("frame", frame)

def main():
    # Construct argument parser and parse
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="Path to (optional) video file")
    args = vars(ap.parse_args())

    # Grab reference to current frame, list of ROI points, and input mode status
    global frame, roiPts, inputMode

    # If video path not supplied, grab reference to camera
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)

    # Otherwise, load the video
    else:
        camera = cv2.VideoCapture(args["video"])

    # Setup the mouse callback
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)

    # Initialize termination criteria for cam shift: Max of 10 iterations or movement by at least 1 pixel along with bounding box of the ROI
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    roiBox = None

    # Loop over all of the frames
    while True:
        # Grab current frame
        (grabbed, frame) = camera.read()

        # Check to see if end of video reached
        if not grabbed:
            break

        # Check if ROI box computed
        if roiBox is not None:
            # Convert current frame to HSV color space and perform mean shift
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)

            # Apply cam shift to back projection, convert points to bounding box, then draw them
            (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
            pts = np.int0(cv2.cv.BoxPoints(r))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        # Show frame and record if user presses a key
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # If 'i' pressed, enter ROI selection mode
        if key == ord("i") and len(roiPts) < 4:
            # Indicate input mode and clone frame
            inputMode = True
            orig = frame.copy()

            # Loop until 4 reference ROI points have been selected/Press any key to exit once points selected
            while len(roiPts) < 4:
                cv2.imshow("frame", frame)
                cv2.waitKey(0)

            # Determine top-left and bottom-left points
            roiPts = np.array(roiPts)
            s = roiPts.su(axis = 1)
            tl = roiPts[np.argmin(s)]
            br = roiPts[np.argmax(s)]

            # Grab ROI for bounding box and covert it to HSV color space
            roi = orig[tl[1]:br[1], tl[0]:br[0]]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Compute HSV histogram for the ROI and store the bounding box
            roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
            roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
            roiBox = (tl[0], tl[1], br[0], br[1])

        elif key == ord("q"):
            break

    # Cleanup camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

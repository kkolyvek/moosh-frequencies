# IMPORT PACKAGES
import cv2

def mooshFilters(frame):
   """
   General outline of video analysis script is as follows:
   1. Bilateral filter: to smooth image while keeping sharp shark edges. This step is very slow but
      greatly increases detection accuracy.
   2. Convert from RGB to HSV: to get to a color space that'll be easier to set filter limits in.
   3. Masking: this is the step that changes most from video to video. Play around with filtering here to get
      satisfactory edge detection. This script has two filters, often one will suffice.
   4. Convert from HSV to Grayscale: the findContours function requires grayscale images
   5. Set threshold and find Contours
   """

   # Perform bilateral filter to help contouring later on
   blur = cv2.bilateralFilter(frame,20,75,75)
   # Convert to HSV
   hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) # RGB to HSV

   # DEFINE MASKS. THIS IS WHAT WILL CHANGE MOST DEPENDING ON VIDEO
   mask_gray = cv2.inRange(hsv, (0,0,110),(180,255,255))    # <= filter out grays
   mask_green = cv2.inRange(hsv, (40,25,0),(100,255,255))   # <= filter out sea greens

   # Combine two masks and filter the blurred footage.
   mask = cv2.bitwise_or(mask_gray, mask_green)
   filtered = cv2.bitwise_and(blur, blur, mask = mask)

   # Convert footage to grayscale
   gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY) # HSV to Grayscale
   gray_invert = cv2.bitwise_not(gray) # Invert gray scale image as findContours program searches for light objects on dark backgrounds

   # Set contouring threshold for edge detection and run
   ret, thresh = cv2.threshold(gray_invert, 165, 255, cv2.THRESH_TOZERO)  # (165, 255, 0) is the best value combo ive found for threshold
   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   # Return the grayscale frame and contour points object
   return gray_invert, contours
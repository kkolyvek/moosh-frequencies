# IMPORT PACKAGES
import cv2
import numpy as np
import math
from datetime import datetime

# IMPORT METHODS
from helpers import isInCircle, progressBar

def create_vid(vidObj):
    # same process as display_freq() and display_vid() but to save video
    # rather than display or calculate frequencies.

    startTime = datetime.now()

    count = 0
    frame_width = int(vidObj.get(3))
    frame_height = int(vidObj.get(4)) - 150
    length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidObj.get(cv2.CAP_PROP_FPS))

    writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))

    slope_left = []
    slope_right = []
    while(True):
      enclosed_x = []
      enclosed_y = []
      enclosed_tuples = []
      x_in_circle = []

      ret, frame = vidObj.read()
      if ret == True:
        frame_resize = frame[75:int(vidObj.get(4))-75, 0:int(vidObj.get(3))]
        blur = cv2.bilateralFilter(frame_resize,20,75,75)

        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        mask_gray = cv2.inRange(hsv, (0,0,110),(180,255,255))
        mask_green = cv2.inRange(hsv, (40,25,0),(100,255,255))
        mask = cv2.bitwise_or(mask_gray, mask_green)
        filtered = cv2.bitwise_and(blur, blur, mask = mask)

        gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
        gray_invert = cv2.bitwise_not(gray)

        ret, thresh = cv2.threshold(gray_invert, 165, 255, cv2.THRESH_TOZERO)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cx = 0
        cy = 0
        for c in contours:
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            x_in_circle = np.array(list(range(int(x)-radius, int(x)+radius)))

            if 50 < radius < 10000:
                cv2.circle(gray_invert, center, radius, (255, 0, 0), 2)
                # display some of the info onto the image
                centertxt = 'Enclosing Circle Center: ' + str(x) + ',' + str(y)
                radtxt = 'Enclosing Circle Radius: ' + str(radius) + ' px'
                cv2.putText(gray_invert, centertxt, (75,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 4, cv2.LINE_4)
                cv2.putText(gray_invert, radtxt, (75,250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 4, cv2.LINE_4)

                for arrays in c:
                    if isInCircle(arrays[0], center, radius):
                        enclosed_x.append(arrays[0][0])
                        enclosed_y.append(arrays[0][1])
                        enclosed_tuples.append((arrays[0][0],arrays[0][1]))
                        cx += arrays[0][0]
                        cy += arrays[0][1]

                cx = int(cx/len(enclosed_x))
                cy = int(cy/len(enclosed_y))
                cv2.circle(gray_invert, (cx,cy), 10, (255,0,0), -1)

                # find two furthest tuples in enclosed_tuples
                tuple_left = center
                tuple_right = center
                for tuple in enclosed_tuples:
                    tuple_dist = math.sqrt(((center[1]-tuple[1]) ** 2) + ((center[0]-tuple[0]) ** 2))
                    tuple_left_dist = math.sqrt(((center[1]-tuple_left[1]) ** 2) + ((center[0]-tuple_left[0]) ** 2))
                    tuple_right_dist = math.sqrt(((center[1]-tuple_right[1]) ** 2) + ((center[0]-tuple_right[0]) ** 2))
                    if (tuple_dist > tuple_left_dist) and (tuple[0] < center[0]):
                        tuple_left = tuple
                    if (tuple_dist > tuple_right_dist) and (tuple[0] > center[0]):
                        tuple_right = tuple
                cv2.circle(gray_invert, tuple_left, 10, (255,0,0), -1)
                cv2.circle(gray_invert, tuple_right, 10, (255,0,0), -1)

                # take slopes of lines between head and center, center and tail
                slope_left.append((cy-tuple_left[1])/(cx-tuple_left[0]))
                slope_right.append((tuple_right[1]-cy)/(tuple_right[0]-cx))

                cv2.line(gray_invert, tuple_left, (cx,cy), (0,0,0), 10)
                cv2.line(gray_invert, (cx,cy), tuple_right, (0,0,0), 10)

        # convert back to BGR and write to video (openCV can only write BGR to vid)
        final = cv2.cvtColor(gray_invert, cv2.COLOR_GRAY2BGR)
        writer.write(final)

        progressBar(count, length, status = 'doin the math') # progress bar so i don't go crazy waiting
        count += 1

        # Press Q on keyboard to stop process
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      # Break the loop
      else:
        break
    # When everything done, release the video capture and video write objects
    vidObj.release()
    writer.release()
    # Closes all the frames
    cv2.destroyAllWindows()

    print(datetime.now() - startTime)
# IMPORT PACKAGES
import cv2
import numpy as np
import math

# IMPORT METHODS
from helpers import isInCircle
from filter import mooshFilters

def display_vid(vidObj):
    # function to display video analysis process.
    # Same process as display_freq() but doesn't perform frequency
    # calculations and instead displays video.

    # video windows
    cv2.namedWindow('orig', cv2.WINDOW_NORMAL) # Create window with freedom of dimensions
    cv2.resizeWindow('orig', 960,540) # scale window to half screen (view 2 at once)
    cv2.moveWindow('orig', 0,0)
    cv2.namedWindow('analysis', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('analysis', 960,540)
    cv2.moveWindow('analysis', 960,0)

    slope_left = []
    slope_right = []
    while(True):
        enclosed_x = []
        enclosed_y = []
        enclosed_tuples = []

        ret, frame = vidObj.read()

        if ret == True:
            frame = frame[75:int(vidObj.get(4))-75, 0:int(vidObj.get(3))]

            gray_invert, contours = mooshFilters(frame)

            cv2.drawContours(gray_invert, contours, -1, (0,255,0), 5)
            cv2.drawContours(frame, contours, -1, (0,0,255), 10)

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
                    cv2.circle(frame, (cx,cy), 10, (255,0,0), -1)

                    # Find two furthest tuples in enclosed_tuples.
                    # Currently this finds the furthest point to the right & left
                    # of the enclosing circle center. This might run into some
                    # issues when the shark is perfectly vertical in frame
                    # but that's unlikely so this works for now.

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
                    cv2.circle(frame, tuple_left, 10, (255,0,0), -1)
                    cv2.circle(frame, tuple_right, 10, (255,0,0), -1)

                    # take slopes of lines between head and center, center and tail
                    slope_left.append((cy-tuple_left[1])/(cx-tuple_left[0]))
                    slope_right.append((tuple_right[1]-cy)/(tuple_right[0]-cx))

                    cv2.line(frame, tuple_left, (cx,cy), (0,0,0), 10)
                    cv2.line(frame, (cx,cy), tuple_right, (0,0,0), 10)

            #enclosed_x_array = np.array(enclosed_x)
            #enclosed_y_array = np.array(enclosed_y)

            cv2.imshow('orig', frame)
            cv2.imshow('analysis', gray_invert)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break
    # When everything done, release the video capture and video write objects
    vidObj.release()
    # Closes all the frames
    cv2.destroyAllWindows()
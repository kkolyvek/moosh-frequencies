# IMPORT PACKAGES
import cv2
import numpy as np
import math

# IMPORT METHODS
from helpers import isInCircle
from filter import mooshFilters, hardFilter


def display_vid(vidObj):
    # function to display video analysis process.
    # Same process as display_freq() but doesn't perform frequency
    # calculations and instead displays video.

    # video windows
    # Create window with freedom of dimensions
    cv2.namedWindow('orig', cv2.WINDOW_NORMAL)
    # scale window to half screen (view 2 at once)
    cv2.resizeWindow('orig', 960, 540)
    cv2.moveWindow('orig', 0, 0)  # move window into place
    cv2.namedWindow('analysis', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('analysis', 960, 540)
    cv2.moveWindow('analysis', 10, 540)

    slope_left = []
    slope_right = []
    while(True):
        ret, frame = vidObj.read()

        if ret == True:
            frame = frame[75:int(vidObj.get(4))-75, 0:int(vidObj.get(3))]

            """
            SELECT FILTER IF NECESSARY - Comment out others.
            ---------------------------------------------------------------------
            """

            # Bilateral filter, sea-green colors
            # gray_invert, contours = mooshFilters(frame)

            # inRange, cutting out sea-greens
            gray_invert, contours = hardFilter(frame)

            """
            ---------------------------------------------------------------------
            """

            cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

            # TODO: Use Moments to find actual centroid
            # https://docs.opencv.org/4.5.1/dd/d49/tutorial_py_contour_features.html, section 1
            cx = 0  # average x value (for centroid approx)
            cy = 0  # average y value (for centroid approx)
            c_target = []  # array of contours on target

            for c in contours:
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                radius = int(radius)

                # this radius limit ensures no small artifacts and no larger circle around the image
                if 25 < radius < 10000:
                    # draw contour's min enclosing circle
                    cv2.circle(frame, center, radius, (0, 255, 0), 2)

                    # record a target contour
                    c_target.append(c)

                    # record center values
                    cx += center[0]
                    cy += center[1]

            """
            TODO
            THIS IS GOOD STUFF HERE BUT:
            - only grabs moment of one contour... this is fine for a starting point
            - find a way to combine moments of multiple contours... contour addition? i dunno
            ===========================================================================
            """
            print(c_target[0])
            Moments = cv2.moments(c_target[0])
            print(Moments)
            mx = int(Moments["m10"] / Moments["m00"])
            my = int(Moments["m01"] / Moments["m00"])
            cv2.circle(frame, (mx, my), 10, (0, 0, 255), 3)

            center = (cx/len(c_target[0]), cy/len(c_target[0]))
            """
            ===========================================================================
            """

            tuple_a = center
            tuple_a_dist = 0
            # Find two furthest tuples.
            for c in c_target:
                for tuple in c:
                    # loop through, find tuple furthest from center
                    tuple_dist = math.sqrt(
                        ((center[0]-tuple[0][0]) ** 2) + ((center[1]-tuple[0][1]) ** 2))
                    if tuple_dist > tuple_a_dist:
                        tuple_a = tuple[0]
                        tuple_a_dist = tuple_dist

            tuple_b = tuple_a
            tuple_b_dist = 0
            for c in c_target:
                for tuple in c:
                    # loop through, find tuple furthest from first tuple
                    tuple_dist = math.sqrt(
                        ((tuple_a[0]-tuple[0][0]) ** 2) + ((tuple_a[1]-tuple[0][1]) ** 2))
                    if tuple_dist > tuple_b_dist:
                        tuple_b = tuple[0]
                        tuple_b_dist = tuple_dist

            # draw tuples as points
            cv2.circle(
                frame, (int(tuple_a[0]), int(tuple_a[1])), 10, (255, 0, 0), -1)
            cv2.circle(
                frame, (int(tuple_b[0]), int(tuple_b[1])), 10, (255, 0, 0), -1)

            # draw new enclosing circle + center
            radius = math.sqrt(
                ((center[1]-tuple_a[1]) ** 2) + ((center[0]-tuple_a[0]) ** 2))
            cv2.circle(gray_invert, (int(center[0]), int(
                center[1])), int(radius), (255, 255, 255), 3)
            cv2.circle(frame, (int(center[0]), int(
                center[1])), int(radius), (0, 0, 0), 3)
            cv2.circle(frame, (int(center[0]), int(
                center[1])), 10, (0, 0, 0), 3)

            # display some of the info onto the image
            centertxt = 'Enclosing Circle Center: ' + \
                str(center[0]) + ',' + str(center[1])
            cv2.putText(gray_invert, centertxt, (75, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_4)
            radtxt = 'Enclosing Circle Radius: ' + str(radius) + ' px'
            cv2.putText(gray_invert, radtxt, (75, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_4)

            # take slopes of lines between head and center, center and tail
            # if (cy-tuple_left[1])/(cx-tuple_left[0]) != 0:
            #     slope_left.append((cy-tuple_left[1])/(cx-tuple_left[0]))
            # else:
            #     slope_left.append(0)
            # if (tuple_right[1]-cy)/(tuple_right[0]-cx) != 0:
            #     slope_right.append((tuple_right[1]-cy)/(tuple_right[0]-cx))
            # else:
            #     slope_right.append(0)
            cv2.line(frame, (tuple_a[0], tuple_a[1]),
                     (int(center[0]), int(center[1])), (255, 255, 255), 7)
            cv2.line(frame, (tuple_b[0], tuple_b[1]),
                     (int(center[0]), int(center[1])), (255, 255, 255), 7)

            cv2.imshow('orig', frame)
            cv2.imshow('analysis', gray_invert)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            print('Read error...')
            break

    # When everything done, release the video capture and video write objects
    vidObj.release()
    # Closes all the frames
    cv2.destroyAllWindows()

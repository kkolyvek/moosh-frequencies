# IMPORT PACKAGES
import cv2
import numpy as np
import math

from numpy.lib.function_base import average

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

    slope_a = []
    slope_b = []

    # counter / arr to record centroids
    counter = -1
    centr_arr = []
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

            c_target = []  # array of dictionaries of on-target contours

            for c in contours:
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                radius = int(radius)

                # this radius limit ensures no small artifacts and no larger circle around the image
                if 25 < radius < 10000:
                    # draw contour's min enclosing circle
                    cv2.circle(frame, center, radius, (0, 255, 0), 2)

                    # get moment
                    mu = cv2.moments(c)

                    # get centroid (+ 1e-5 to avoid div by zero)
                    mc = (mu['m10'] / (mu['m00'] + 1e-5), mu['m01'] / (mu['m00'] + 1e-5))

                    contour_dictionary = {
                        "contour": c,
                        "enc_circle_midpoint": (x, y),
                        "enc_circle_rad": radius,
                        "centroid": mc
                    }

                    # record a target contour
                    c_target.append(contour_dictionary)

            # If there is more than one contour, get weighted average of their locations
            averaged_centroid = None
            if len(c_target) > 1:
                total_rad = 0
                for i in range(len(c_target)):
                    total_rad += c_target[i]["enc_circle_rad"]

                avg_x = 0
                avg_y = 0
                for i in range(len(c_target)):
                    avg_x += (c_target[i]["centroid"][0] * (c_target[i]["enc_circle_rad"] / total_rad))
                    avg_y += (c_target[i]["centroid"][1] * (c_target[i]["enc_circle_rad"] / total_rad))
                averaged_centroid = (avg_x, avg_y)

                centr_arr.append(averaged_centroid)
                counter += 1
            elif len(c_target) == 1:
                averaged_centroid = c_target[0]["centroid"]

                centr_arr.append(averaged_centroid)
                counter += 1
            else:
                averaged_centroid = centr_arr[counter]

                centr_arr.append(averaged_centroid)
                counter += 1

            # Display centroids of all contours
            cv2.circle(frame, (int(averaged_centroid[0]), int(averaged_centroid[1])), 4, (0, 255, 0), -1)

            # Find two furthest tuples.
            tuple_a = averaged_centroid
            tuple_a_dist = 0
            for c in c_target:
                for tuple in c["contour"]:
                    # loop through, find tuple furthest from center
                    tuple_dist = math.sqrt(((averaged_centroid[0]-tuple[0][0]) ** 2) + ((averaged_centroid[1]-tuple[0][1]) ** 2))
                    if tuple_dist > tuple_a_dist:
                        tuple_a = tuple[0]
                        tuple_a_dist = tuple_dist

            tuple_b = tuple_a
            tuple_b_dist = 0
            for c in c_target:
                for tuple in c["contour"]:
                    # loop through, find tuple furthest from first tuple
                    tuple_dist = math.sqrt(((tuple_a[0]-tuple[0][0]) ** 2) + ((tuple_a[1]-tuple[0][1]) ** 2))
                    if tuple_dist > tuple_b_dist:
                        tuple_b = tuple[0]
                        tuple_b_dist = tuple_dist

            # draw tuples as points
            cv2.circle(frame, (int(tuple_a[0]), int(tuple_a[1])), 10, (255, 0, 0), -1)
            cv2.circle(frame, (int(tuple_b[0]), int(tuple_b[1])), 10, (255, 0, 0), -1)

            # draw lines between tuples
            cv2.line(frame, (int(tuple_a[0]), int(tuple_a[1])), (int(averaged_centroid[0]), int(averaged_centroid[1])), (255, 255, 255), 5)
            cv2.line(frame, (int(tuple_b[0]), int(tuple_b[1])), (int(averaged_centroid[0]), int(averaged_centroid[1])), (255, 255, 255), 5)

            # take slopes of lines between head and center, center and tail
            if averaged_centroid[0] == tuple_a[0]:
                slope_a.append(0)
            else:
                slope_a.append((averaged_centroid[1]-tuple_a[1]) / (averaged_centroid[0]-tuple_a[0]))

            if averaged_centroid[0] == tuple_b[0]:
                slope_b.append(0)
            else:
                slope_b.append((tuple_b[1]-averaged_centroid[1]) / (tuple_b[0]-averaged_centroid[0]))

            cv2.imshow('orig', frame)
            cv2.imshow('analysis', gray_invert)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            print('Read error...')
            break

    print(slope_a)
    print(slope_b)

    # When everything done, release the video capture and video write objects
    vidObj.release()
    # Closes all the frames
    cv2.destroyAllWindows()

# IMPORT PACKAGES
import math
import cv2
import sys

def crop_image(frame, dirName):
    # FUTURE WORK:
    # write program to crop image base on the bounding box around the shark
    # bounding box may need to be redefined based on center position as it does
    # not automatically change with size of shark in FOV.
    print('crop image')


def isInCircle(tuple_point, tuple_center, radius):
    # determines whether a point is within a circle definied by tuple_center and radius. Returns true/false
    px = tuple_point[0]
    py = tuple_point[1]
    cx = tuple_center[0]
    cy = tuple_center[1]
    return math.sqrt(((cy-py) ** 2) + ((cx-px) ** 2)) <= radius


# Function to get and print frame info
def getVideoInfo(vidObj):
    # Create a new dictionary
    vidInfo = dict()
    # Get info on the video
    vidInfo['frame_width'] = int(vidObj.get(3))
    vidInfo['frame_height'] = int(vidObj.get(4))
    vidInfo['length'] = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
    vidInfo['fps']    = vidObj.get(cv2.CAP_PROP_FPS)
    return vidInfo


def progressBar(count, total, status=''):
    # progress bar in powershell so we don't go crazy waiting
    # WARNING: this does mess with powershell interactivity so open another instance if you'd like to use powershell while this program is running
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
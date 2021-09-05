"""
ANALYZING SHARK TAIL-BEAT FREQUENCY FROM DRONE FOOTAGE USING OPENCV

@author: sirkt, Koppi Kolyvek - May 2020
"""

# TODO:
# AUTOMIZE TAIL_BEAT TO RUN ON A FULL VIDEO
# - Set thresholds for acceptable footage, etc
# - Highlight and rport acceptable areas with good visibilty

# IMPORT PACKAGES
import cv2

# IMPORT METHODS
from helpers import getVideoInfo
from displayFreq import display_freq
from displayVid import display_vid
from createVid import create_vid

"""
RUN FUNCTIONS FROM HERE
"""


def main():
    # DECLARE PATH TO VIDEO
    # directory data subject to change, of course
    # dirName = 'C:\\Users\\koppa\\Documents\\Moosh Data\\Initial Vid\\DJI_0002_10fps_trim3.mp4'
    dirName = 'C:\\Users\\koppa\\Desktop\\Personal\\Projects\\moosh-frequencies\\videos\\DJI_0024_Trim.mp4'
    print(dirName)

    # INIT VideoCapture OBJECT
    vidObj = cv2.VideoCapture(dirName)

    # DISPLAY DESIRED PROCESS (COMMENT OUT NOT-NEEDED PROCESSES)

    """
    MAIN FUNCTION:
    Performs tail-beat frequency analysis and saves a chart of tail slope and tail-beat frequencies to the working directory.
    """
    # display_freq(vidObj)

    """
    ASSISTANT FUNCTION:
    Performs all image processing tasks and displays the results.
    * It is recommended to use this process function first to test the accuracy of the countouring! *
    """
    display_vid(vidObj)

    """
    ASSISTANT FUNCTION:
    Performs all image processing tasks and creates a video file of the result in the working directory.
    """
    # create_vid(vidObj)


if __name__ == "__main__":
    main()

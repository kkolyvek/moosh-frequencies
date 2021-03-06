# IMPORT PACKAGES
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

# IMPORT METHODS
from helpers import getVideoInfo, isInCircle, progressBar
from filter import mooshFilters

def display_freq(vidObj):
    # function to find and display shark tail beat frequency.
    # This function doesn't display the video (just the final result),
    # see later functions to view video

    count = 0
    length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

    slope_left = []; # initialize arrays for slope data
    slope_right = []
    while(True):
        enclosed_x = []; # initialize arrays for tracking shark outline
        enclosed_y = []
        enclosed_tuples = []; # array for coordinates enclosed within bounding circle
        ret,frame = vidObj.read()

        if ret == True:
            frame = frame[75:int(vidObj.get(4))-75, 0:int(vidObj.get(3))] # crop frame to remove top and bottom bars of video

            gray_invert, contours = mooshFilters(frame)

            cx = 0
            cy = 0
            for c in contours:
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                radius = int(radius)
                x_in_circle = np.array(list(range(int(x)-radius, int(x)+radius)))

                if 50 < radius < 10000: # set minimum enclosing circle radius to ignore small noise... can play around with this size depending on size of shark in video
                    for arrays in c:
                        if isInCircle(arrays[0], center, radius):
                            enclosed_x.append(arrays[0][0])
                            enclosed_y.append(arrays[0][1])
                            enclosed_tuples.append((arrays[0][0],arrays[0][1]))
                            cx += arrays[0][0]
                            cy += arrays[0][1]

            cx = int(cx/len(enclosed_x))
            cy = int(cy/len(enclosed_y))

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

            # take slopes of lines between head and center, center and tail
            slope_left.append((cy-tuple_left[1])/(cx-tuple_left[0]))
            slope_right.append((tuple_right[1]-cy)/(tuple_right[0]-cx))

            progressBar(count, length, status = 'doin the math') # progress bar so i don't go crazy waiting
            count += 1

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break

    # When everything done, plot results and find FFT
    vidInfo = getVideoInfo(vidObj)

    x = np.linspace(1/vidInfo['fps'],vidInfo['length']/vidInfo['fps'],vidInfo['length'])
    y = slope_right

    FT = np.fft.fft(y)/len(y) # take FFT with normalized amplitude
    FT = FT[range(int(len(y)/2))]
    values = np.arange(int(len(x)/2))
    timePeriod = len(x)/vidInfo['fps']
    frequencies = values/timePeriod

    fig, (ax1,ax2) = plt.subplots(2)
    ax1.plot(x,y,'b-')
    ax1.set(title = 'Slope of Shark Tail Over Time',
            xlabel = 'time (s)',
            ylabel = 'Slope of Tail')


    ax2.loglog(frequencies,abs(FT),'r-')
    ax2.set(title = 'Fourier Transform of Shark Tail Slope',
            xlabel = 'freqs (hz)',
            ylabel = 'amplitude')


    plt.show()

    # save data (optional)
    """
    time = np.asarray(x)
    tail_slope = np.asarray(y)
    slope_transform = np.asarray(FT)
    freqs = np.asarray(frequencies)

    np.savetxt('time_period.txt',time,delimiter=',')
    np.savetxt('SharkTail_Slope.txt',tail_slope,delimiter=',')
    np.savetxt('SharkTail_Slope_Transform.txt',slope_transform,delimiter=',')
    np.savetxt('frequencies.txt',freqs,delimiter=',')
    """

    # release the video capture and video write objects
    vidObj.release()
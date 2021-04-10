import cv2
import os
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
lowerTh = 50000
upperTh = 300000
path = '/home/andi/everest.mp4'

frames = {}

def generatingHistograms(videopath):
    histograms = {}

    cap = cv2.VideoCapture(videopath)

    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video stream or file")

    #iterate over frames and calculate color histogram
    success, frame = cap.read()
    colors = ("b", "g", "r")
    frameNumber = 1
    while (success):

        histArray = []
        for i, col in enumerate(colors):
            hist = cv2.calcHist([frame], [i], None, [64], [0, 256])
             #plt.plot(hist, color=col)
             #plt.xlim([0, 64])
             #print(hist.astype(np.int).transpose)
            histArray.append(hist.astype(np.int).ravel())

        # plt.show()
        histograms[frameNumber] = histArray
        frames[frameNumber] = frame
        frameNumber += 1
        success, frame = cap.read()

    cap.release()
    return histograms

def calcManhattenDistance(histArray1,histArray2):
    i = 0
    j = 0
    distance = []
    while i < len(histArray1):
        distance.append(0)
        while j < len(histArray1[i]):
            distance[i] = distance[i] + abs(histArray1[i][j] - histArray2[i][j])
            j+=1
        i += 1
        j = 0
    return distance

def ExceededTreshhold(distance,lowerBuffer):

    if(lowerBuffer[0] > upperTh and lowerBuffer[1] > upperTh and lowerBuffer[2] > upperTh):
        print("Lower Cut")
        return True
    if (distance[0] > upperTh and distance[1] > upperTh and distance[2] > upperTh):
        return True
    return False

def splitInShots(histOfFrames):
    # Startindizes
    startShotIndex = 1
    currentFrameIndex = 1

    shots = {}

    # wenn Suchindex größer als Länge gibt es keine Shots mehr
    while (currentFrameIndex < len(histOfFrames)):

        ShotChangeSearching = True
        lowerBuffer = [0, 0, 0]
        while (ShotChangeSearching):

            currentFrameIndex += 1

            print("Frame: {}".format(currentFrameIndex))
            distance = calcManhattenDistance(histOfFrames[startShotIndex], histOfFrames[currentFrameIndex])
            print(distance)

            # upper Threshhol exceeded
            exceeded = ExceededTreshhold(distance, lowerBuffer)

            if (exceeded or currentFrameIndex == len(histOfFrames)):
                ShotChangeSearching = False
            else:
                # lower Treshhold exceeded
                i = 0
                while i < len(distance):
                    if (distance[i] > lowerTh):
                        lowerBuffer[i] = lowerBuffer[i] + (distance[i] - lowerTh)
                    i += 1

        print("Next Shot Frame: {}".format(currentFrameIndex))
        # cv2.imshow('Frame', frames[currentFrameIndex])
        # cv2.waitKey(1000)
        # cv2.destroyAllWindows()
        # Set new starting Point
        shots[startShotIndex] = currentFrameIndex - 1
        startShotIndex = currentFrameIndex

    return shots

def safeShotsinTextFile(shots):
    file = open("shots.txt", "w")

    i = 1
    for key in shots:
        file.write("{} : {} (Shot {})\n".format(key, shots[key],i))
        i+=1
    file.close()

def safeKeyframes(shots):
    i = 1

    directory = '{}/keyframes'.format(Path().absolute())
    os.mkdir(directory)

    for key in shots:
        frameIndex = int((shots[key] - key) / 2) + key
        imagePath = '{}/Shot{}.jpg'.format(directory,i)
        cv2.imwrite(imagePath, frames[frameIndex])
        i += 1




histOfFrames = generatingHistograms(path)

shots = splitInShots(histOfFrames)

safeShotsinTextFile(shots)
safeKeyframes(shots)

print(shots)



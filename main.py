from sys import argv

import cv2
import math
import numpy as np
#from matplotlib import pyplot as plt

import os
from pathlib import Path


framesDictionary = {}
histograms = {}
shots = {}

cap = None



def main(argv):
    path = '/Users/marcus/Documents/MasterInformatics/SS21/VideoSearchDeepLearning/everest.mp4'
    #lowerBound = 20000#argv[1]
    lowerBound = int(argv[1])

    #upperBound = 200000
    upperBound = int(argv[2])

    #distance = 'Manhattan'
    #distance = 'Euclidian'
    distance = argv[3]
    initVideo(path)
    shots = splitIntoShots(distance, lowerBound, upperBound)
    ShotsasText(shots)
    MiddleFrame(shots)


def initVideo(path):
    cap = cv2.VideoCapture(path)
    print("Video Stream opened")
    if (cap.isOpened() == False):
        print("No such file or video stream")

    amountOfFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(amountOfFrames)
    ret, frame = cap.read()
    i = 1
    color = ('b', 'g', 'r')
    while (ret):
        histograms[i] = createHist(frame, color)
        #print(histograms[i])
        i += 1

        #print(len(framesDictionary))
        #print(len(histograms))
        fps = cap.get(cv2.CAP_PROP_FPS)
        framesDictionary[i] = frame
        ret, frame = cap.read()
        #print("fps: ", fps)


        #cv2.waitKey(int(1000. / float(fps)))  # 1000 milliseconds / fps

    cap.release()


    #cv2.destroyAllWindows()

def createHist(frame, color):
    #for frame in framesDictionary:

        histogramArray = []
        for j, colors in enumerate(color):
            hist = cv2.calcHist([frame], [j], None, [64], [0, 256])
            histogramArray.append(hist.astype(int).ravel())

        return histogramArray


def calcDistance(distance, histA, histB):
    #print("Enter calc Distance Method: ", distance)
    #print(histA)
    #print(histB)
    diff = []
    if(distance == "Manhattan"):
        for i in range(0, len(histA)):
            #print(len(histA))
            diff.append(0)
            for j in range(0, len(histA[i])):
                #print(len(histA[i]))

                diff[i] = diff[i] + abs(histA[i][j]-histB[i][j])
        return diff

    if(distance == "Euclidian"):
        for i in range(0, len(histA)):
            diff.append(0)
            for j in range(0, len(histA[i])):
                sum_sq = np.sum(np.square(histA[i][j]-histB[i][j]))
                diff[i] = diff[i] + np.sqrt(sum_sq)

        return diff

def splitIntoShots(distance, lowerBound, upperBound):

    shotStartIndex = 1
    currentFrame = 1

    shotsDict = {}

    while (currentFrame<len(histograms)):

        breaktrough = False
        next = True

        lowBuff = [0, 0, 0]

        while(next):
            currentFrame += 1
            #if(currentFrame < len(histograms)):
            distancediff = calcDistance(distance, histograms[shotStartIndex], histograms[currentFrame])
            #print("Distancedifference: ", distancediff)


            if(lowBuff[0]>upperBound and lowBuff[1]>upperBound and lowBuff[2]>upperBound):
                breaktrough = True
            if (distancediff[0] > upperBound and distancediff[1] > upperBound and distancediff[2] > upperBound):
                breaktrough = True

            if (breaktrough or currentFrame == len(histograms)):
                next = False
            else:
                for i in range(0, len(distancediff)-1):
                    if(distancediff[i]>lowerBound):
                        lowBuff[i] = lowBuff[i] + (distancediff[i] - lowerBound)

        shotsDict[shotStartIndex] = currentFrame-1
        shotStartIndex = currentFrame

    return shotsDict

def ShotsasText(shots):
    file = open("shots.txt", "w")

    i = 1
    for key in shots:
        file.write("{} : {} (Shot {})\n".format(key, shots[key],i))
        i+=1
    file.close()

def MiddleFrame(shots):
    i = 1

    directory = '{}/keyframes'.format(Path().absolute())
    
    os.system("rm -rf {}".format(directory))
    print("deleted")


    os.mkdir(directory)

    for keyframe in shots:
        frameIndex = int((shots[keyframe] - keyframe) / 2) + keyframe
        imagePath = '{}/ShotNr{}.jpg'.format(directory,i)
        cv2.imwrite(imagePath, framesDictionary[frameIndex])
        i += 1

if __name__ == "__main__":
    main(argv)
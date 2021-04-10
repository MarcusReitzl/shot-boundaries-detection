import cv2
import numpy as np
from matplotlib import pyplot as plt

def histogram(frame):
    plt.hist(frame.ravel(), 64, [0, 64]);
    plt.show()
    return


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
    return distance


cap = cv2.VideoCapture('/home/andi/everest.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
firstRet, firstFrame = cap.read()
firstHistArray = []
firstChannels = cv2.split(firstFrame)
colors = ("b", "g", "r")
for i, col in zip(firstChannels, colors):
    firstHist = cv2.calcHist([i],  [0], None, [64], [0, 256])
#   print(hist.astype(np.int).transpose)
    firstHistArray.append(firstHist.astype(np.int).ravel())

frameNumber = 1
while(cap.isOpened()):
    try:
        # Capture frame-by-frame
        ret, frame = cap.read()
        #histogram(frame);
        channels = cv2.split(frame)

        histArray = []
        for i, col in zip(channels, colors):
            hist = cv2.calcHist([i],[0],None,[64],[0, 256])
            #plt.plot(hist, color=col)
            #plt.xlim([0, 64])
            #print(hist.astype(np.int).transpose)
            histArray.append(hist.astype(np.int).ravel())

        #plt.show()
        distance = calcManhattenDistance(firstHistArray,histArray)
        print("Frame: {}".format(frameNumber))
        print(distance[0])
        print(distance[1])
        print(distance[2])
        frameNumber += 1
    except:
        print("An exception occured")
 #
#

 # print(histAsArray[0][0])
  #p





# When everything done, release the video capture object
cap.release()

# Closes all the frames
#cv2.destroyAllWindows()





#img = cv2.imread('Lena.png') #zero for grayscale
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#edges = cv2.Canny(img,100,200)

#plt.subplot(121),plt.imshow(img)
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges)
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

#plt.show()





import cv2
import numpy as np
from matplotlib import pyplot as plt

def histogram(frame):
    plt.hist(frame.ravel(), 64, [0, 64]);
    plt.show()
    return


cap = cv2.VideoCapture('/Users/marcus/Documents/MasterInformatics/SS21/VideoSearchDeepLearning/everest.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  histogram(frame);


  if ret == True:

    # Display the resulting frame
    cv2.imshow('Frame',frame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()





#img = cv2.imread('Lena.png') #zero for grayscale
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#edges = cv2.Canny(img,100,200)

#plt.subplot(121),plt.imshow(img)
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges)
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

#plt.show()





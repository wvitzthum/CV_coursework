from materials.disparity import getDisparityMap, plot
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load left image
filename = 'materials/umbrellaL.png'
imgL = cv2.imread(filename, 0)
imgLGrey = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
imgLEdges = cv2.Canny(imgL,100,200)

# Load right image
filename = 'materials/umbrellaR.png'
imgR = cv2.imread(filename, 0)
imgRGrey = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
imgREdges = cv2.Canny(imgR,100,200)

# Get disparity map
disparityGrey = getDisparityMap(imgLGrey, imgRGrey, 64, 5)
disparityEdges = getDisparityMap(imgLEdges, imgREdges, 64, 5)

# Normalise for display
disparityImgGrey = np.interp(disparityGrey, (disparityGrey.min(), disparityGrey.max()), (0.0, 1.0))
disparityImgEdges = np.interp(disparityEdges, (disparityEdges.min(), disparityEdges.max()), (0.0, 1.0))

plt.figure(figsize=(15, 8))
plt.title('Disparity Images')
plt.subplot(131),plt.imshow(disparityImgGrey, 'gray'),plt.title('Grey')
plt.subplot(132),plt.imshow(disparityImgEdges, 'gray'),plt.title('Edge detected')
plt.savefig('disparity.png')

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]

cv2.destroyAllWindows()
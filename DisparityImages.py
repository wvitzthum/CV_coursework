from materials.disparity import getDisparityMap, plot
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load left image
filename = 'materials/umbrellaL.png'
imgL = cv2.imread(filename, 0)


# Load right image
filename = 'materials/umbrellaR.png'
imgR = cv2.imread(filename, 0)

def nothing(x):
    pass

cv2.namedWindow('image')

block_size = 5
num_disparities = 0

# create trackbars for different parameters
cv2.createTrackbar('Threshold1','image',0,255,nothing)
cv2.createTrackbar('Threshold2','image',0,255,nothing)
cv2.createTrackbar('# of Disparities','image',0,255,nothing)
cv2.createTrackbar('Block Size','image',-255,255,nothing)

while(True):

    b_input = cv2.getTrackbarPos('Block Size','image')
    n_dipsar_input =  cv2.getTrackbarPos('# of Disparities','image')
    t1 = cv2.getTrackbarPos('Threshold1','image')
    t2 = cv2.getTrackbarPos('Threshold2','image')
    num_disparities = n_dipsar_input if (n_dipsar_input % 16) == 0 and 0 <= n_dipsar_input else num_disparities
    block_size = b_input if (b_input % 2) != 0 and 5 < b_input else block_size

    imgREdges = cv2.Canny(imgR,t1,t2)
    imgLEdges = cv2.Canny(imgL,t1,t2)

    disparityEdges = getDisparityMap(imgLEdges, imgREdges, num_disparities, block_size)

    disparityImgEdges = np.interp(disparityEdges, (disparityEdges.min(), disparityEdges.max()), (0.0, 1.0))

    cv2.imshow('image', disparityImgEdges)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
from materials.disparity import getDisparityMap, plot
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load left image
girlL = 'materials/girlL.png'
imgL = cv2.imread(girlL, 0)
blurred_img = cv2.GaussianBlur(imgL, (21, 21), 0)

# Load right image
imgR = cv2.imread('materials/girlR.png', 0)
girl_clr_original = cv2.imread(girlL)
girl_clr = cv2.imread(girlL)

bg_blrd = cv2.filter2D(cv2.imread(girlL),-1,np.ones((5,5),np.float32)/25)

def nothing(x):
    pass

cv2.namedWindow('image')

block_size = 45
num_disparities = 48
k = 0

# create trackbars for different parameters
cv2.createTrackbar('k','image',k,255,nothing)
cv2.createTrackbar('Block Size','image',block_size,255,nothing)
cv2.createTrackbar('Disparities','image',num_disparities,255,nothing)

while(True):

    b_input = cv2.getTrackbarPos('Block Size','image')
    n_dipsar_input =  cv2.getTrackbarPos('Disparities','image')
    k = cv2.getTrackbarPos('k','image')
    num_disparities = n_dipsar_input if (n_dipsar_input % 16 == 0) and 0 < n_dipsar_input else num_disparities
    block_size = b_input if (b_input % 2 != 0) and 5 < b_input else block_size
    #print(f"Disparities: {num_disparities} input {n_dipsar_input}, Blocksize: {block_size} input {b_input}")
    disparityImg = getDisparityMap(imgL, imgR, num_disparities, block_size)

    z = np.zeros_like(disparityImg)

    for (x,y), value in np.ndenumerate(disparityImg):
        z[x,y] = 1 / (value+k)
    
    z_new = np.interp(z, (z.min(), z.max()), (0.0, 1.0))
    z_new[z_new < 1] = 0
    result = z_new * imgL
    
    x_vals, y_vals = np.where(z_new != 1)
    for x,y in zip(x_vals, y_vals):
        blurred_img[x,y] = imgL[x,y]
    
    girl_clr[z_new == 1] = bg_blrd[z_new == 1]


    h_stack = np.hstack((disparityImg, z_new*255))
    cv2.imshow('image3', h_stack)
    cv2.imshow('result', girl_clr)
    cv2.imshow('original', girl_clr_original)

    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
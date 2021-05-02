from materials.disparity import getDisparityMap, plot
import cv2
import numpy as np
from matplotlib import pyplot as plt


def plot_3d(x, y, z):
    ax = plt.axes(projection ='3d')
    ax.scatter(x, y, z, 'green')

    # Labels
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    #plt.savefig('myplot.pdf', bbox_inches='tight') # Can also specify an image, e.g. myplot.png
    plt.show()
    cv2.destroyAllWindows()
    cv2.waitKey(0)


focal_lenght_l = 38.38
focal_lenght_r = 41.454
baseline = 174.019
x_center = 1429.219
y_center = 993.403

# Scaling doffs to lower resolution
doffs = 114.291

# focal length in pixles
focal_length = 5806.559

# Load left image
filename = 'materials/umbrellaL.png'
imgL = cv2.imread(filename, 0)


# Load right image
filename = 'materials/umbrellaR.png'
imgR = cv2.imread(filename, 0)

imgREdges = cv2.Canny(imgR,86,131)
imgLEdges = cv2.Canny(imgL,86,131)

disparityMap = getDisparityMap(imgLEdges, imgREdges, 64, 5)
#import pdb; pdb.set_trace()

x_values = []
y_values = []
z_values = []

#import pdb; pdb.set_trace()

for (x,y), value in np.ndenumerate(disparityMap):
    x_1 = x-x_center
    y_1 = y-y_center

    if value < 1:
        continue

    z_new = baseline*(focal_length/(value+doffs))
    z_values.append(z_new)

    x_new = (x_1*z_new)/focal_length
    x_values.append(x_new)

    y_new = (y_1*z_new)/focal_length
    y_values.append(y_new)

    #print(f"{x_new}, {y_new}, {z_new}")
plot_3d(x_values, z_values, y_values,)

#cv2.imshow('Disparity',  np.interp(disparityMap, (disparityMap.min(), disparityMap.max()), (0.0, 1.0)))

#cv2.waitKey(0)
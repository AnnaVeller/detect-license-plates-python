
import os
import numpy as np
import sys
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import cv2
import warnings
warnings.filterwarnings('ignore')
from regions import *

#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

all_regions = load_regions()
print(all_regions)
#image = cv2.imread("test.jpg")
#cv2.imshow('sd', image)

import model
#state, textArr, status = model.detect_number(image, "A001MP05")
#print(state, textArr, status)

cap = cv2.VideoCapture("Y618XX123.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    state, textArr, status = model.detect_number(frame, "Y618XX123")
    print(status)
    #cv2.imshow('video', frame)
#cap.release()
#cv2.destroyAllWindows()

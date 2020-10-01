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

import model

cap = cv2.VideoCapture("video.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    state, textArr, status = model.detect_number(frame, "no name")
    print(status, textArr)


import os
import numpy as np
import sys
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import cv2
import warnings
warnings.filterwarnings('ignore')
import model

#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

cap = cv2.VideoCapture("Y618XX123.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    state, textArr, status = model.detect_number(frame, "Y618XX123")
    print(status, textArr)


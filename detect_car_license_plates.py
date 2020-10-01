import os
import numpy as np
import sys
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import cv2
import warnings
warnings.filterwarnings('ignore')
import read_video

#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

read_video.detect_one_video("test.mp4")
read_video.detect_one_video("Y618XX123.mp4", "Y618XX123")


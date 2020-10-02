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

read_video.detect_one_video("bandicam 2020-10-02 10-50-40-879.mp4", "H133OE123")
read_video.detect_one_video("Y618XX123.mp4", "Y618XX123")


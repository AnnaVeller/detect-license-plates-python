import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"   # For GPU inference
#os.environ["CUDA_VISIBLE_DEVICES"] = ""  # For CPU inference

# dynamically grow the memory used on the GPU
from tensorflow.compat.v1.keras.backend import set_session
import tensorflow as tf
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.compat.v1.Session(config=config)
set_session(sess)

import warnings
warnings.filterwarnings('ignore')
import read_video
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

PATH_VIDEO = "test_mini4.mp4"
NAME = os.path.splitext(PATH_VIDEO)[0]
logging.info(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, NAME)
logging.info(" Итоговый номер " + str(set(cars)) + "\n\n")


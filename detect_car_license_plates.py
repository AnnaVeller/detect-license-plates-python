import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"   # For GPU inference
#os.environ["CUDA_VISIBLE_DEVICES"] = ""  # For CPU inference
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


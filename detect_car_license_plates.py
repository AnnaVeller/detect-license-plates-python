import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import warnings
warnings.filterwarnings('ignore')
import read_video
import logging



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

PATH_VIDEO = "T576HB123_Y663YO750_3.36_720.mp4"
NAME = os.path.splitext(PATH_VIDEO)[0]
logging.info(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, NAME)
logging.info(" Итоговый номер " + str(set(cars)) + "\n\n")


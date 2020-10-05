import warnings
warnings.filterwarnings('ignore')
import read_video
import logging
import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

#PATH_VIDEO = "http://62.94.249.83/axis-cgi/mjpg/video.cgi"
#logging.info(" Запустили видео %s" % PATH_VIDEO)
#cars = read_video.detect_one_video(PATH_VIDEO, "no name")
#logging.info(" Итоговый номер " + str(set(cars)) + "\n\n")

PATH_VIDEO = "T576HB123_Y663YO750_3.36_720.mp4"
logging.info(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, "no name")
logging.info(" Итоговый номер " + str(set(cars)) + "\n\n")

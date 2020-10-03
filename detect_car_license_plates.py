import warnings
warnings.filterwarnings('ignore')
import read_video
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

PATH_VIDEO = "video.mp4"
logging.info(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, "no name")
logging.info(" Итоговый номер " + str(set(cars)) + "\n\n")

PATH_VIDEO = "T576HB123_Y663YO750_3.36_720.mp4"
logging.info(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, "no name")
logging.info(" Итоговый номер " + str(set(cars)) + "\n\n")

PATH_VIDEO = "B678XY178_T576HB123_1.57.mp4"
logging.info(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, "no name")
logging.info(" Итоговый номер " + str(set(cars)) + "\n\n")
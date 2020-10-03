import warnings
warnings.filterwarnings('ignore')
import read_video
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

PATH_VIDEO = "video4.mp4"
logging.debug(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, "no name")
logging.info(" Итоговый номер " + str(cars) + "\n\n")

PATH_VIDEO = "video4.mp4"
logging.debug(" Запустили видео %s" % PATH_VIDEO)
cars = read_video.detect_one_video(PATH_VIDEO, "no name")
logging.info(" Итоговый номер " + str(cars) + "\n\n")


#PATH_VIDEO = "video2.mp4"
#logging.debug(" Запустили видео %s" % PATH_VIDEO)
#cars = read_video.detect_one_video(PATH_VIDEO, "no name")
#logging.info(" Итоговый номер " + str(cars))

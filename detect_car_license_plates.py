import warnings
warnings.filterwarnings('ignore')
import read_video
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

#PATH_VIDEO = "video.mp4"
#logger.debug("Запустили видео " + PATH_VIDEO)
#read_video.detect_one_video(PATH_VIDEO, "no name")

PATH_VIDEO = "video2.mp4"
logging.debug(" Запустили видео %s" % PATH_VIDEO)
read_video.detect_one_video(PATH_VIDEO, "no name")
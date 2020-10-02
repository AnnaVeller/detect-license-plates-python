import warnings
warnings.filterwarnings('ignore')
import read_video
import logging
import sys
logger = logging.getLogger("detect")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%d-%b-%y %H:%M:%S')

fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

PATH_VIDEO = "video.mp4"
logger.debug("Запустили видео " + PATH_VIDEO)
read_video.detect_one_video(PATH_VIDEO, "no name")

PATH_VIDEO = "video2.mp4"
logger.debug("Запустили видео "+ PATH_VIDEO)
read_video.detect_one_video(PATH_VIDEO, "no name")
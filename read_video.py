import cv2
import model
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

def detect_one_video(video, name=" "):
    count = 0
    cadr = 0
    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        ret, frame = cap.read()
        cadr += 1
        state, number, status = model.detect_number(frame, name)
        if state:
            logger.debug(str(count) + str(number))
            count = 0
        else:
            if cadr % 10 == 0:
                logger.debug("nothing" + str(cadr))
            count += 1

    cap.release()
    cv2.destroyAllWindows()


import cv2
import model
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def detect_one_video(video, name=" "):
    count = 0
    cadr = 0
    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        ret, frame = cap.read()
        cadr += 1
        state, number, status = model.detect_number(frame, name)
        if state:
            logging.debug(" %d %d" %(count, number))
            count = 0
        else:
            logging.debug("Ничего уже %d кадров" %cadr)
            count += 1

    cap.release()
    cv2.destroyAllWindows()


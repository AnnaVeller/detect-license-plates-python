import cv2
import model
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')


def detect_one_video(video, name=" "):
    count = 0
    cadr = 0
    cap = cv2.VideoCapture(video)
    one_number = []
    ret = True
    while ret:
        ret, frame = cap.read()
        cadr += 1
        state, number, status = model.detect_number(frame, name)
        if state:
            text = " Спустя %d кадров нашли номер: " % count
            logging.debug(text + str(number))
            count = 0
        else:
            if count % 10 == 0:
                logging.debug(" Номер не найден. Обработали %d кадр" % cadr)
            count += 1
        if count < 4:
            one_number.extend(number)
        else:
            one_number.clear()
        print(one_number)
    cap.release()
    cv2.destroyAllWindows()


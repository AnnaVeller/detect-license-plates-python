import cv2
import model
import wrong_numbers
import numpy as np

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

MIN_CADRS_TO_DETECT = 2
CADRS_TO_FIND_NEW_CAR = 10

def detect_one_video(video, name=" "):
    count = 100000
    cadr = 0
    cap = cv2.VideoCapture(video)
    one_number = []
    ret = True
    car_list = []
    while ret:
        ret, frame = cap.read()
        length = int(cap.get(cv2.CAP_PROP_POS_MSEC))/1000
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        logging.info(" Кадр открылся? %s %s sec [%dx%d]" % (str(ret), str(length), h, w))
        if ret:
            cadr += 1
            state, number, status, cords, zones = model.detect_number(frame, " ")
            logging.info(" Координаты номера на %s кадре: \n%s" % (str(cadr), str(cords)))
            if state:
                text = " Спустя %d кадров нашли номер: " % count
                for c in cords:
                    pts = np.array(c, np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (255, 0, 0), 2)
                logging.debug(text + str(number))
                count = 0
            else:
                if count % 50 == 0:     # чтобы не выводить слишком часто отладочные сообщения
                    logging.debug(" Номер не найден. Обработали %d кадр" % cadr)
                count += 1
            if count < CADRS_TO_FIND_NEW_CAR:
                one_number.extend(number)   # список номер для текущей одной машины
                logging.debug(" список one_number " + str(one_number))
            elif count == CADRS_TO_FIND_NEW_CAR:
                if len(one_number) >= MIN_CADRS_TO_DETECT:
                    name = wrong_numbers.wrong(one_number)
                    car_list.append(name)
                    logging.info(" Номер машины на %d кадре: %s " % (cadr, name))
            else:
                one_number.clear()
            cv2.imshow('detect car plates', frame)
    if count < CADRS_TO_FIND_NEW_CAR:       # если видео закончилось на кадре где есть машина
        name = wrong_numbers.wrong(one_number)
        logging.info(" Номер машины на %d кадре: %s " % (cadr, name))
        logging.debug(" текущий номер " + str(name))
        car_list.append(name)
    cap.release()
    cv2.destroyAllWindows()
    return car_list


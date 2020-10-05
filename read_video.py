import cv2
import model
import wrong_numbers
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

MIN_CADRS_TO_DETECT = 2
CADRS_TO_FIND_NEW_CAR = 10
PATH = "/content/gdrive/My Drive/cars/detect/"


def detect_one_video(video, name=" "):
    count = 100000
    cadr = 0
    cap = cv2.VideoCapture(video)
    if (cap.isOpened() == False):
        logging.debug("Unable to read video")
    else:
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        out = cv2.VideoWriter(PATH + "output.mp4", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (w, h))
    one_number = []
    ret = True
    car_list = []
    while ret:
        ret, frame = cap.read()
        if ret:
            length = int(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000
            logging.DEBUG(" Параметры видео: %s sec [%dx%d]" % (str(length), h, w))
            cadr += 1
            state, number, status, cords, zones = model.detect_number(frame, " ")
            if state:
                logging.DEBUG(" Координаты номера на %s кадре: \n%s" % (str(cadr), str(cords)))
                for c in cords:
                    logging.debug(" c" + str(c))
                    pts = np.array(c, np.int32)
                    pts = pts.reshape((-1, 1, 2))
                logging.info(" Спустя %d кадров нашли номер: " % count + str(number))
                path_to_detect_plate = PATH + str(cadr) + ".jpg"
                cv2.imwrite(path_to_detect_plate, frame)
                count = 0
            else:
                if count % 50 == 0:     # чтобы не выводить слишком часто отладочные сообщения
                    logging.debug(" Номер не найден. Обработали %d кадр" % cadr)
                count += 1
            if count < CADRS_TO_FIND_NEW_CAR:
                one_number.extend(number)   # список номер для текущей одной машины
                logging.debug(" Список номеров для этой машины %s " % str(one_number))
            elif count == CADRS_TO_FIND_NEW_CAR:
                if len(one_number) >= MIN_CADRS_TO_DETECT:
                    name = wrong_numbers.wrong(one_number)
                    car_list.append(name)
                    logging.info(" Номер машины на %d кадре: %s " % (cadr, name))
                    path_to_detect_plate = PATH + "detectList/" + str(cadr) + ".jpg"
                    cv2.imwrite(path_to_detect_plate, frame)
            else:
                one_number.clear()
            #cv2.imshow('Detect car plates', frame)
            out.write(frame)
    if count < CADRS_TO_FIND_NEW_CAR:       # если видео закончилось на кадре где есть машина
        name = wrong_numbers.wrong(one_number)
        logging.info(" Номер машины на %d кадре: %s " % (cadr, name))
        car_list.append(name)
    cap.release()
    cv2.destroyAllWindows()
    return car_list

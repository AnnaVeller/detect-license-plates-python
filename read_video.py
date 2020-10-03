import cv2
import model
import wrong_numbers

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

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
        #logging.debug(" Кадр открылся? " + str(ret))
        if ret:
            cadr += 1
            state, number, status = model.detect_number(frame, " ")
            if state:
                text = " Спустя %d кадров нашли номер: " % count
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
    if count < CADRS_TO_FIND_NEW_CAR:       # если видео закончилось на кадре где есть машина
        name = wrong_numbers.wrong(one_number)
        logging.info(" Номер машины на %d кадре: %s " % (cadr, name))
        logging.debug(" текущий номер " + str(name))
        car_list.append(name)
    cap.release()
    cv2.destroyAllWindows()
    return car_list


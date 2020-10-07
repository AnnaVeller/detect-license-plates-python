import cv2
import model
import wrong_numbers
import numpy as np

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

MIN_CADRS_TO_DETECT = 2
CADRS_TO_FIND_NEW_CAR = 10
PATH = "/home/user/repos/detect-license-plates-python/video/"
#PATH = "C:/Users/Anna/Documents/sirius/"

def detect_one_video(video, name=" "):
    count = 100000      # сколько кадров прошло после обнаружения машины
    cadr = 0
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        logging.debug("Unable to read video")
    else:
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        out = cv2.VideoWriter(PATH + name + "_detect.mp4", cv2.VideoWriter_fourcc('m','p','4','v'), fps, (w, h))
    one_number = []
    ret = True
    car_list = []
    while ret:
        ret, frame = cap.read()
        if ret:
            length = int(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000
            logging.debug(" Параметры видео: %s sec [%dx%d]" % (str(length), h, w))
            TF_FORCE_GPU_ALLOW_GROWTH = True
            cadr += 1
            state, really_number, number, status, cords, zones = model.detect_number(frame, " ")
            if state:
                #logging.debug(" Координаты номера на %s кадре: \n%s" % (str(cadr), str(cords)))
                for c in cords:
                    pts = np.array(c, np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (255, 0, 0), 2)
                    if really_number:
                        color = (255,0,0)       # blue
                    else:
                        color = (250, 206, 135)     # Light Sky Blue
                    cv2.putText(frame, str(number), (20, h-30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                logging.debug(" Спустя %d кадров нашли номер: " % cadr + str(number))
                #path_to_detect_plate = PATH + str(cadr) + ".jpg"
                #cv2.imwrite(path_to_detect_plate, frame)
                count = 0
            else:
                if count % 10 == 0:     # чтобы не выводить слишком часто отладочные сообщения
                    logging.debug(" Номер не найден. Обработали %d кадр" % cadr)
                count += 1
            if count < CADRS_TO_FIND_NEW_CAR:
                one_number.extend(number)   # список номер для текущей одной машины
                name = wrong_numbers.wrong(one_number)
                red = (0, 0, 255)
                cv2.putText(frame, str(name), (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
                #logging.debug(" Список номеров для этой машины %s " % str(one_number))
            elif count == CADRS_TO_FIND_NEW_CAR:
                if len(one_number) >= MIN_CADRS_TO_DETECT:
                    name = wrong_numbers.wrong(one_number)
                    car_list.append(name)
                    logging.info(" Номер уехавшей машины с %d кадра: %s " % (cadr, name))
                    red = (0,0,255)
                    cv2.putText(frame, str(name), (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
            else:
                one_number.clear()
            #cv2.imshow('Detect car plates', frame)
            out.write(frame)
    if count < CADRS_TO_FIND_NEW_CAR:       # если видео закончилось на кадре где есть машина
        name = wrong_numbers.wrong(one_number)
        logging.info(" НомерНомер уехавшей машины с %d кадра: %s " % (cadr, name))
        cv2.putText(frame, str(number), (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
        out.write(frame)
        car_list.append(name)
    cap.release()
    cv2.destroyAllWindows()
    return car_list

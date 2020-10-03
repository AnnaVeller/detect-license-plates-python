import cv2
import model
import wrong_numbers

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def detect_one_video(video, name=" "):
    count = 100000
    cadr = 0
    cap = cv2.VideoCapture(video)
    one_number = []
    ret = True
    car_list = []
    while ret:
        ret, frame = cap.read()
        logging.debug(" Кадр открылся? " + str(ret))
        if ret:
            cadr += 1
            state, number, status = model.detect_number(frame, " ")
            if state:
                text = " Спустя %d кадров нашли номер: " % count
                logging.info(text + str(number))
                count = 0
            else:
                if count % 10 == 0:     # чтобы не выводить слишком часто отладочные сообщения
                    logging.debug(" Номер не найден. Обработали %d кадр" % cadr)
                count += 1
            if count < 4:     # чтобы это не сработало на первых 4 кадрах
                one_number.extend(number)
                logging.debug(" список one_number " + str(one_number))
            elif count == 4:      # прошло 4 кадра после обнаружения знака
                name = wrong_numbers.wrong(one_number)
                car_list.append(name)
                #logging.info(" текущий список номеров " + str(car_list))
            else:
                one_number.clear()
    if count < 4:       # если видео закончилось на кадре где есть машина
        name = wrong_numbers.wrong(one_number)
        logging.debug(" текущий номер " + str(name))
        car_list.append(name)
        #logging.info(" текущий список номеров " + str(car_list))
    cap.release()
    cv2.destroyAllWindows()
    return car_list


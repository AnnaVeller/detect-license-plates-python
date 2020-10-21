import logging.config

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import ModelDetect
import Regions
import WrongNumbers

MIN_CADRS_TO_DETECT = 3
CADRS_TO_FIND_NEW_CAR = 3

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

FONT = 'fonts/font2.ttf'
Red = (0, 0, 255)  # BGR
Blue = (255, 0, 0)
LightSkyBlue = (250, 206, 135)


def one_frame(frame, one_number, count, h):
    state, really_number, number, cords, zones = ModelDetect.detect_number(frame)

    if state:
        for c in cords:
            pts = np.array(c, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, Blue, 2)
            if really_number:
                cv2.putText(frame, str(number), (20, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, Blue, 2)
            else:
                cv2.putText(frame, str(number), (20, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, LightSkyBlue, 2)
        log.debug(" Found number %s" % str(number))
        count = 0
    else:
        count += 1

    car_number = 'no'
    if count < CADRS_TO_FIND_NEW_CAR:
        one_number.extend(number)  # список номеров для текущей одной машины
        flag_new_car = 0
        if len(one_number) >= MIN_CADRS_TO_DETECT:
            car_number = WrongNumbers.choose_number(one_number)
            reg = Regions.which_regions(car_number)
            font = ImageFont.truetype(FONT, 32)
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text((20, h - 150), str(reg), font=font, fill=Red)  # fill=(0, 0, 255, 0)
            frame = np.array(img_pil)
            cv2.putText(frame, str(car_number), (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, Red, 2)
    elif count == CADRS_TO_FIND_NEW_CAR:
        car_number = WrongNumbers.choose_number(one_number)
        flag_new_car = 1
        one_number.clear()
    else:
        one_number.clear()
        flag_new_car = 2
    return state, frame, car_number, count, one_number, flag_new_car, zones

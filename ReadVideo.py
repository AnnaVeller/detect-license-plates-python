import logging.config
import math
import os
import time

import cv2

import ProcessOneFrame

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH_TO_SAVE = 'car_numbers/'


def save_imgs(list_img, list_zone, name_video, count_cars):
    path_to_save_data = os.path.join(PATH_TO_SAVE, name_video) + '/'

    len_of_list = len(list_img)
    average = math.ceil((len_of_list - 1) / 2)
    log.debug(' Average count %d' % average)
    suffix = 1

    if len_of_list <= 3:
        first = 0
        last = len_of_list - 1
    elif len_of_list == 4:
        first = 1
        last = len_of_list - 1
    elif len_of_list <= 7:
        first = 1
        last = len_of_list - 2
    else:
        first = 2
        last = len_of_list - 2

    for i in range(len_of_list):
        if i == first or i == average or i == last:  # save 3 images
            img = list_img[i]
            zone = list_zone[i]
            path_to_img = path_to_save_data + str(count_cars) + '_' + str(suffix) + '.jpg'
            path_to_zone = path_to_save_data + str(count_cars) + '_' + str(suffix) + '_zone.jpg'
            cv2.imwrite(path_to_img, img)
            cv2.imwrite(path_to_zone, zone)
            log.debug(' Save images %s %s' % (path_to_img, path_to_zone))
            suffix += 1


def read_video(video, file, type, name_video, SEC_TO_WRITE, frame_size):
    path_to_save_data = os.path.join(PATH_TO_SAVE, name_video) + '/'
    try:
        os.mkdir(path_to_save_data)
        log.debug("Create dir %s" % path_to_save_data)
    except OSError:
        log.debug("Can't create dir %s" % path_to_save_data)
        exit(1)

    log.debug(' Opening %s' % file)
    file = open(path_to_save_data + file, 'w')
    cap = cv2.VideoCapture(video)
    if cap.isOpened():
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        new_fps = 1 / SEC_TO_WRITE
        log.info(' Video [%dx%d]' % (w, h))
        out = cv2.VideoWriter(PATH_TO_SAVE + name_video + "_detect.mp4",
                              cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), new_fps, (w, h))
        ret = True
        file.write('%d %d %s %d \n' % (w, h, name_video, fps))
    else:
        ret = False
        log.info(" Unable to read video %s" % video)

    last_frame_time_video = -SEC_TO_WRITE  # time of last capture frame on video
    start_time = time.time()  # time os starting process video/stream
    last_frame_time_stream = time.time() - SEC_TO_WRITE  # time of last capture frame on stream

    count = 100000  # сколько кадров прошло после обнаружения машины
    one_number = []
    count_cars = 1
    list_img = []
    list_zone = []
    while ret:
        ret, frame = cap.read()
        if frame_size != False:
            frame = frame[frame_size[0]:frame_size[1], frame_size[2]:frame_size[3]]  # img[y:y+h, x:x+w]
            h = frame_size[1] - frame_size[0]
            w = frame_size[3] - frame_size[2]
        length = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        try:
            if (time.time() - last_frame_time_stream >= SEC_TO_WRITE and type == 's') or (
                    length - last_frame_time_video >= SEC_TO_WRITE and type == 'v'):
                if ret:
                    if type == 'v':
                        last_frame_time_video = length
                        log.debug(' In video now : %f sec' % length)
                    else:
                        last_frame_time_stream = time.time()
                    run_time = time.time() - start_time
                    log.debug(' Last from begin in real time : %f sec' % run_time)

                    found_really_number, frame, car_number, count, one_number, flag_new_car, zone = \
                        ProcessOneFrame.one_frame(frame, one_number, count, h)

                    out.write(frame)

                    if flag_new_car == 'ENDING_FIND_THIS_CAR':
                        file.write('%d %s\n' % (count_cars, car_number))
                        log.info(' Wrote to file car number: %s' % car_number)
                        save_imgs(list_img, list_zone, name_video, count_cars)
                        list_img.clear()
                        list_zone.clear()
                        count_cars += 1

                    if found_really_number:  # add to list if found really number
                        list_img.append(frame)
                        list_zone.append(zone)
                        log.debug(' Add image')

                    if flag_new_car == 'NO_CARS':
                        list_img.clear()
                        list_zone.clear()
        except KeyboardInterrupt:
            log.info(' KeyboardInterrupt by ctrl+c')
            break
    if flag_new_car == 'ENOUGH_FRAMES_FOR_RECOGNITION':
        file.write('%d %s\n' % (count_cars, car_number))
        save_imgs(list_img, list_zone, name_video, count_cars)
    else:
        file.write('\n')
    file.close()
    cap.release()
    cv2.destroyAllWindows()

import logging.config
import math
import time

import cv2

import ProcessOneFrame

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH_TO_SAVE = 'car_numbers/'


def read_video(video, file, type, name_video, SEC_TO_WRITE):
    path_to_file_txt = PATH_TO_SAVE + file
    log.debug(' Opening %s' % path_to_file_txt)
    file = open(path_to_file_txt, 'w')
    cap = cv2.VideoCapture(video)
    if cap.isOpened():
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        new_fps = 1 / SEC_TO_WRITE
        log.debug(' Video [%dx%d]' % (w, h))
        out = cv2.VideoWriter(PATH_TO_SAVE + name_video + "_detect.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), new_fps,
                              (w, h))
        ret = True
        file.write('%d %d %s %d \n' % (w, h, name_video, fps))
    else:
        ret = False
        log.debug(" Unable to read video %s" % video)

    last_frame_time_video = -SEC_TO_WRITE  # time of last capture frame on video
    start_time = time.time()  # time os starting process video/stream
    last_frame_time_stream = time.time() - SEC_TO_WRITE  # time of last capture frame on stream

    count = 100000  # сколько кадров прошло после обнаружения машины
    one_number = []
    count_cars = 1
    list_img = []
    while ret:
        ret, frame = cap.read()
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

                    state, frame, car_number, count, one_number, flag_new_car = ProcessOneFrame.one_frame(frame,
                                                                                                          one_number,
                                                                                                          count, h)

                    out.write(frame)

                    if flag_new_car == 1:
                        file.write('%d %s\n' % (count_cars, car_number))
                        average = math.ceil((len(list_img)) / 2)
                        log.debug(' Average count %d' % average)
                        suffix = 1
                        for i in range(len(list_img)):
                            if i == 0 or i == average or i == len(list_img) - 1:  # save 3 images
                                img = list_img[i]
                                path_to_img = PATH_TO_SAVE + str(count_cars) + '_' + str(suffix) + '.jpg'
                                cv2.imwrite(path_to_img, img)
                                log.debug(' Save images %s' % path_to_img)
                                suffix += 1
                        list_img.clear()
                        count_cars += 1
                    if state:  # save img
                        list_img.append(frame)
                        log.debug(' Add image')
        except KeyboardInterrupt:
            log.debug(' KeyboardInterrupt by ctrl+c')
            break
    if flag_new_car == 0:
        file.write('%d %s\n' % (count_cars, car_number))
        average = math.ceil((len(list_img)) / 2)
        log.debug(' Average count %d' % average)
        suffix = 1
        for i in range(len(list_img)):
            if i == 0 or i == average or i == len(list_img) - 1:  # save 3 images
                img = list_img[i]
                path_to_img = PATH_TO_SAVE + str(count_cars) + '_' + str(suffix) + '.jpg'
                cv2.imwrite(path_to_img, img)
                log.debug(' Save images %s' % path_to_img)
                suffix += 1
    else:
        file.write('\n')
    file.close()
    cap.release()
    cv2.destroyAllWindows()

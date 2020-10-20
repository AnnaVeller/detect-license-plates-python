import cv2
import time
import logging.config
import ProcessOneCadr

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH = 'car_numbers/'


def read_video(video, file, type, name_video, SEC_TO_WRITE):
    path_to_file_txt = PATH + file
    file = open(path_to_file_txt, 'w')
    cap = cv2.VideoCapture(video)
    if cap.isOpened():
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        new_fps = 1/SEC_TO_WRITE
        log.debug(' Video [%dx%d]' % (w, h))
        out = cv2.VideoWriter(PATH + name_video + "_detect.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), new_fps, (w, h))
        ret = True
        file.write('%d %d %s %d \n' % (w, h, name_video, fps))
    else:
        ret = False
        log.debug(" Unable to read video %s" % video)

    last_cadr_time_video = -SEC_TO_WRITE  # time of last capture cadr on video
    start_time = time.time()  # time os starting process video/stream
    last_cadr_time_stream = time.time() - SEC_TO_WRITE  # time of last capture cadr on stream

    count = 100000      # сколько кадров прошло после обнаружения машины
    one_number = []
    flag_new_car = False
    while ret:
        ret, frame = cap.read()
        length = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        try:
            if (time.time() - last_cadr_time_stream >= SEC_TO_WRITE and type == 's') or (
                    length - last_cadr_time_video >= SEC_TO_WRITE and type == 'v'):
                if ret:
                    if type == 'v':
                        last_cadr_time_video = length
                        log.debug(' In video now : %f sec' % length)
                    else:
                        last_cadr_time_stream = time.time()
                    run_time = time.time() - start_time
                    log.debug(' Last from begin in real time : %f sec' % run_time)

                    frame, car_number, count, one_number, flag_new_car = ProcessOneCadr.one_cadr(frame, one_number, count, h)

                    out.write(frame)

                    if flag_new_car == 1:
                        file.write(car_number + '\n')
        except KeyboardInterrupt:
            log.debug(' KeyboardInterrupt by ctrl+c')
            break
    if flag_new_car == 0:
        file.write(car_number + '\n')
    else:
        file.write('\n')
    file.close()
    cap.release()
    cv2.destroyAllWindows()

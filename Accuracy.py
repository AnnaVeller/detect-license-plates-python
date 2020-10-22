import argparse
import logging.config
import cv2

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH_TO_IMG = 'car_numbers/'


def create_parser():
    parser = argparse.ArgumentParser(description='tutorial:')
    parser.add_argument('--file', '-f', dest='file', default='test.txt', help='File with coordinates of plates')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    file = open(PATH_TO_IMG + args.file)
    dict_numbers = {}
    line = file.readline()
    w, h, name_video, fps = line.split()
    line = file.readline()
    while line:
        count, number = line.split()
        count = int(count)
        dict_numbers[count] = number
        line = file.readline()

    for i in range(count):
        for k in [1, 2, 3]:
            path_to_img = PATH_TO_IMG + name_video + '_' + str(i + 1) + '_' + str(k) + '_zone.jpg'
            try:
                img = cv2.imread(path_to_img)
                (h_zone, w_zone, d_zone) = img.shape
                img = cv2.resize(img, (w_zone * 2, h_zone * 2))
                try:
                    cv2.imshow(str(k), img)
                    log.debug(' %s opened' % path_to_img)
                except cv2.error:
                    log.debug(" Could not open %s" % path_to_img)
                    break
            except AttributeError:
                log.debug(" %s not found" % path_to_img)
                break
        print('This is: %s' % dict_numbers[i + 1])
        print('Do you agree?')
        cv2.waitKey(0)
        answer = input().lower()
        if answer == '1' or answer == 't' or answer == 'true' or answer == 'yes':
            answer = True
        else:
            answer = False
        log.debug(' Answer is %s' % str(answer))
    cv2.destroyAllWindows()

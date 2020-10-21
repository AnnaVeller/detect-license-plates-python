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
        print(line)
        count, number = line.split()
        count = int(count)
        dict_numbers[count] = number
        line = file.readline()

    for i in range(count):
        for k in [1, 2, 3]:
            path_to_img = PATH_TO_IMG + name_video + '_' + str(i+1)+'_'+str(k)+'.jpg'
            img = cv2.imread(path_to_img)
            log.debug(path_to_img)
            cv2.imshow(str(k), img)
        cv2.waitKey(0)


    print(dict_numbers)
    cv2.destroyAllWindows()

import argparse
import logging.config

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH_TO_IMG = 'car_numbers/'


def create_parser():
    parser = argparse.ArgumentParser(description='tutorial:')
    parser.add_argument('--file', '-f', dest='filename', default='test.txt', help='File with coordinates of plates')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    file = open(PATH_TO_IMG + args.file)
    dict_numbers = []
    line = file.readline()
    w, h, name_video, fps = line.split()

    while line:
        line = file.readline()
        count, number = line.split()
        count = int(count)
        dict_numbers[count] = number

    print(dict_numbers)

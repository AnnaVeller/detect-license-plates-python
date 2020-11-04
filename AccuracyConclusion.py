import logging.config
import argparse
import os

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH_TO_DATA = 'car_numbers/'


def create_parser():
    parser = argparse.ArgumentParser(description='tutorial:')
    parser.add_argument('--name', '-f', dest='name', default='', help='Name of video or file without extension')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    path_to_imgs = os.path.join(PATH_TO_DATA, args.name) + '/'

    fin_file = path_to_imgs + args.name + '_asked.txt'
    file = open(fin_file)
    line = file.readline()
    state_array = []
    w, h, name_video, fps = line.split()
    line = file.readline()
    while line:
        try:
            count, number, state = line.split()
            state = int(state)
            state_array.append([number, state])
            line = file.readline()
        except ValueError:
            log.error('\nIn your file a few videos.\nYou should edit your file.\nNow we took only first video values')
            break
    file.close()

    count_true = 0
    count_unknown = 0
    count_false = 0
    for one_number in state_array:
        log.debug(one_number)
        if one_number[1] == 1:
            count_true += 1
        elif one_number[1] == -1:
            count_unknown += 1
        elif one_number[1] == 0:
            count_false += 1

    log.info(
        """ 
        All numbers          | %d
        -------------------------
        Clear numbers        | %d
        -------------------------
        Correctly recognized | %d
        -------------------------
        Not correctly        | %d
        -------------------------
        Numbers is not clear | %d
        -------------------------
        Precision            | %f %%
        """
        % (
            len(state_array),
            count_false + count_true,
            count_true,
            count_false,
            count_unknown,
            count_true / (count_false + count_true) * 100
        ))

import argparse
import logging.config

import cv2
import numpy as np
import os

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH_TO_DATA = 'car_numbers/'


def create_parser():
    parser = argparse.ArgumentParser(description='tutorial:')
    parser.add_argument('--name', '-f', dest='name', default='', help='Name of video or file without extension')
    return parser


def create_image(input_images, increase_const=3):
    images = []
    max_width = 0  # find the max width of all the images
    total_height = 0  # the total height of the images (vertical stacking)

    for img in input_images:
        (h_zone, w_zone, d_zone) = img.shape
        img = cv2.resize(img, (w_zone * increase_const, h_zone * increase_const))
        images.append(img)
        if img.shape[1] > max_width:
            max_width = img.shape[1]
        total_height += img.shape[0]

    # create a new array with a size large enough to contain all the images
    final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)

    current_y = 0  # keep track of where your current image was last placed in the y coordinate
    for img in images:
        # add an image to the final array and increment the y coordinate
        final_image[current_y:img.shape[0] + current_y, :img.shape[1], :] = img
        current_y += img.shape[0]

    return final_image


if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()

    path_to_imgs = os.path.join(PATH_TO_DATA, args.name) + '/'

    new_file = open(path_to_imgs + args.name + '_asked.txt', 'a')
    file = open(path_to_imgs + args.name + '.txt')
    dict_numbers = {}
    line = file.readline()
    w, h, name_video, fps = line.split()
    new_file.write('%s %s %s %s \n' % (w, h, name_video, fps))
    line = file.readline()
    while line:
        count, number = line.split()
        count = int(count)
        dict_numbers[count] = number
        line = file.readline()
    file.close()

    for i in range(count):
        images = []
        for k in [1, 2, 3]:
            path_to_img = path_to_imgs + str(i + 1) + '_' + str(k) + '_zone.jpg'
            try:
                img = cv2.imread(path_to_img)
                images.append(img)
            except AttributeError:
                log.debug(" %s not found" % path_to_img)
                break

        img = create_image(images)

        ask = True
        while ask:

            try:
                cv2.imshow('%d %s' % (i + 1, dict_numbers[i + 1]), img)
                log.debug(' %s opened' % path_to_img)
            except cv2.error:
                log.debug(" Could not open %s" % path_to_img)
                break

            log.info('This is: %s' % dict_numbers[i + 1])
            log.info('Do you agree?')
            cv2.waitKey(0)
            answer = input().lower()
            ask = False
            if answer == '1' or answer == 't' or answer == 'true' or answer == 'yes' or answer == 'y':
                answer = 1
            elif answer == '-1' or answer == '?' or answer == 'unknown' or answer == 'x':  # if we can't understand number
                answer = -1
            elif answer == '0' or answer == 'f' or answer == 'false' or answer == 'no' or answer == 'n':
                answer = 0
            else:
                log.info('Input again your answer')
                ask = True

        log.debug(' Answer is %s' % str(answer))
        new_file.write('%d %s %d\n' % (i + 1, dict_numbers[i + 1], answer))

    new_file.close()
    cv2.destroyAllWindows()

import argparse
import logging.config
import os

import cv2
import numpy as np

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

    fin_file = path_to_imgs + args.name + '_asked.txt'
    file = open(fin_file)
    dict = {}
    line = file.readline()
    w, h, name_video, fps = line.split()
    line = file.readline()
    while line:
        try:
            count, number, state = line.split()
            count = int(count)
            state = int(state)
            dict[count] = [number, state]
            line = file.readline()
        except ValueError:
            log.error('\nIn your file a few videos.\nYou should edit your file.\nNow we took only first video values')
            break
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
        try:
            num, state = dict[i + 1]
            if state == 1:
                state = True
            elif state == -1:
                state = 'Unknown'
            elif state == 0:
                state = False
            cv2.imshow('%d %s %s' % (i + 1, num, state), img)
            log.debug(' %s opened' % path_to_img)
            cv2.waitKey(0)
        except cv2.error:
            log.debug(" Could not open %s" % path_to_img)
            break

    cv2.destroyAllWindows()

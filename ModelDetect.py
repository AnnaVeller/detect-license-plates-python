import logging.config
import os
import sys

from NomeroffNet import filters, RectDetector, TextDetector, OptionsDetector, \
    Detector, textPostprocessing

import Regions

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

all_regions = Regions.load_regions()

# change this property
NOMEROFF_NET_DIR = os.path.abspath('../')

# specify the path to Mask_RCNN if you placed it outside Nomeroff-net project
MASK_RCNN_DIR = os.path.join(NOMEROFF_NET_DIR, 'Mask_RCNN')
MASK_RCNN_LOG_DIR = os.path.join(NOMEROFF_NET_DIR, 'logs')

log.debug(" Path to Mask_RCNN " + MASK_RCNN_DIR)

sys.path.append(NOMEROFF_NET_DIR)

# Initialize npdetector with default configuration file.
nnet = Detector(MASK_RCNN_DIR, MASK_RCNN_LOG_DIR)
nnet.loadModel("latest")

rectDetector = RectDetector()

optionsDetector = OptionsDetector()
optionsDetector.load("latest")

# Initialize text detector.
textDetector = TextDetector.get_static_module("ru")()
textDetector.load("latest")


def detect_number(img):  # кадр, номер, который должны обнаружить
    NP = nnet.detect([img])

    # Generate image mask.
    cv_img_masks = filters.cv_img_mask(NP)

    # Detect points.
    arrPoints = rectDetector.detect(cv_img_masks)
    zones = rectDetector.get_cv_zonesBGR(img, arrPoints)

    # find standart
    regionIds, stateIds, countLines = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)

    # find text with postprocessing by standart
    textArr = textDetector.predict(zones)
    textArr = textPostprocessing(textArr, regionNames)

    state = False  # нашли ли номер?
    really_number = False  # может ли номер быть таким?
    if len(textArr) > 0:
        state = True
        ok = check(textArr)
        if ok:
            really_number = True

    return state, really_number, textArr, arrPoints, zones  # нашли номер, может быть такой номер,
    # номер, координаты номера, фото номера


def check(textArr):
    for num in textArr:
        tmp = list(num)
        if len(tmp) == 8 or len(tmp) == 9:
            tmp_num = tmp[1:4]
            tmp_region = tmp[6:]
            tmp_literal = [tmp[0]]
            tmp_literal.extend(tmp[4:6])
            tmp_num = ''.join(map(str, tmp_num))  # должно быть числом
            tmp_region = ''.join(map(str, tmp_region))  # должно быть числом
            tmp_literal = ''.join(map(str, tmp_literal))  # должно быть буквами

            tmp_lit_truck = tmp[0:2]
            tmp_num_truck = tmp[2:6]
            tmp_lit_truck = ''.join(map(str, tmp_lit_truck))  # должно быть числом
            tmp_num_truck = ''.join(map(str, tmp_num_truck))  # должно быть буквами
            if (tmp_num.isdigit() and tmp_literal.isalpha() and tmp_region.isdigit()) or (
                    tmp_lit_truck.isalpha() and tmp_num_truck.isdigit()):
                if tmp_region in all_regions:
                    return True
        else:
            return False

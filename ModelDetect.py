import logging.config
import os
import sys

from NomeroffNet import filters, RectDetector, TextDetector, OptionsDetector, \
    Detector, textPostprocessing

import Regions
import WrongNumbers

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
    toShowZones = rectDetector.get_cv_zonesRGB(img, arrPoints)

    # find standart
    regionIds, stateIds, countLines = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)

    # find text with postprocessing by standart
    textArr = textDetector.predict(zones)
    textArr = textPostprocessing(textArr, regionNames)

    state = False  # нашли ли номер?
    really_number = False  # может ли номер быть таким?
    zone = ''
    answerArr = []
    i = 0
    if len(textArr) > 0:
        state = True
        for num in textArr:
            ok = WrongNumbers.check(num)
            if ok:
                really_number = True
                zone = toShowZones[i]  # !Problem! How we should do with zome. I suppose I have one zone
                answerArr.append(num)
            i += 1
        if not really_number:
            answerArr = textArr

    return state, really_number, answerArr, arrPoints, zone  # нашли номер, может быть такой номер,
    # номер, координаты номера, фото номера

import logging.config
import os
import sys

NOMEROFF_NET_DIR = os.path.abspath('../nomeroff-net/')
sys.path.append(NOMEROFF_NET_DIR)  # add path to search modules

from NomeroffNet import filters, RectDetector, TextDetector, OptionsDetector, \
    Detector, textPostprocessing

import Regions
import WrongNumbers

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

all_regions = Regions.load_regions()

rectDetector = RectDetector()

optionsDetector = OptionsDetector()
optionsDetector.load("latest")

# Initialize text detector.
textDetector = TextDetector({
    "eu_ua_2004_2015": {
        "for_regions": ["eu_ua_2015", "eu_ua_2004"],
        "model_path": "latest"
    },
    "eu_ua_1995": {
        "for_regions": ["eu_ua_1995"],
        "model_path": "latest"
    },
    "eu": {
        "for_regions": ["eu"],
        "model_path": "latest"
    },
    "ru": {
        "for_regions": ["ru", "eu-ua-fake-lnr", "eu-ua-fake-dnr"],
        "model_path": "latest"
    },
    "kz": {
        "for_regions": ["kz"],
        "model_path": "latest"
    },
    "ge": {
        "for_regions": ["ge"],
        "model_path": "latest"
    },
    "su": {
        "for_regions": ["su"],
        "model_path": "latest"
    }
})

# Initialize npdetector with default configuration file.
nnet = Detector()
nnet.loadModel(NOMEROFF_NET_DIR)


def detect_number(img):  # кадр, номер, который должны обнаружить
    cv_img_masks = nnet.detect([img])

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
    answer_nums = []
    answer_cords = []
    if len(textArr) > 0:
        state = True
        i = 0
        for num in textArr:
            ok = WrongNumbers.check(num)
            if ok:
                really_number = True
                zone = toShowZones[i]  # !Problem! How we should do with zome. I suppose I have one zone
                answer_nums.append(num)
                answer_cords.append(arrPoints[i])
                log.debug(' Found really number: %s' % str(answer_nums))
            i += 1
    if not really_number:
        answer_nums = textArr
        answer_cords = arrPoints

    return state, really_number, answer_nums, answer_cords, zone  # нашли номер, может быть такой номер,
    # номер, координаты номера, фото номера

import os
import cv2

PATH = 'test_folder/'  # choose path to save frames
PATH_WHERE_SEARCH = 'car_numbers/'
VIDEO = 'test_multy_detect.mp4'

name_video = os.path.splitext(VIDEO)[0]
path_to_save = os.path.join(PATH, name_video) + '/'
print(path_to_save)
try:
    os.mkdir(path_to_save)
except OSError:
    'Не получилось создать папку'

cap = cv2.VideoCapture(PATH_WHERE_SEARCH + VIDEO)
ret, frame = cap.read()
c = 1
while ret:
    length = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    if 0 <= length:
        p = path_to_save + str(c) + '.jpg'
        cv2.imwrite(p, frame)
        c += 1
    ret, frame = cap.read()

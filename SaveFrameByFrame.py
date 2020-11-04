import cv2
import os

path_to_save = 'test_folder/'   # choose path to save frames
path_where_search = 'car_numbers/'
name_video = 'problem_detect.mp4'
cap = cv2.VideoCapture(path_where_search + name_video)
ret, frame = cap.read()
c = 1
while ret:
    length = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    if 0 <= length:
        p = path_to_save + os.path.splitext(name_video)[0] + str(c) + '.jpg'
        cv2.imwrite(p, frame)
        c += 1
    ret, frame = cap.read()

#import cv2

#frame = cv2.imread("11.jpg")
#number = ["sdfsdfsd"]

#cv2.putText(frame, str(number), (200, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
#cv2.imshow("dd", frame)
#cv2.waitKey(0)

import os
PATH_VIDEO = "T576HB123_Y663YO750_3.36_720.mp4"
a = os.path.splitext(PATH_VIDEO)[0]
print(a)
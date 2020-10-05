import cv2

frame = cv2.imread("11.jpg")
number = ["sdfsdfsd"]
h = int(frame.get(cv2.CAP_PROP_FRAME_HEIGHT))
w = int(frame.get(cv2.CAP_PROP_FRAME_WIDTH))
cv2.putText(frame, str(number), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
cv2.imshow("dd", frame)
cv2.waitKey(0)
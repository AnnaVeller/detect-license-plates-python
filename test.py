import cv2

frame = cv2.imread("11.jpg")
number = ["sdfsdfsd"]
cv2.putText(frame, str(number), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
cv2.imshow("dd", frame)
cv2.waitKey(0)
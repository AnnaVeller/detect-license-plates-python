import cv2
import model

def detect_one_video(video, name=" "):
    count = 0
    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        ret, frame = cap.read()
        state, number, status = model.detect_number(frame, name)
        if state:
            print(count, number)
            count = 0
        else:
            count += 1

    cap.release()
    cv2.destroyAllWindows()

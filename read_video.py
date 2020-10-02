import cv2
import model

def detect_one_video(video, name=" "):
    count = 0
    cadr = 0
    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        ret, frame = cap.read()
        cadr += 1
        state, number, status = model.detect_number(frame, name)
        if state:
            print(count, number)
            count = 0
        else:
            print("nothing", cadr)
            count += 1

    cap.release()
    cv2.destroyAllWindows()


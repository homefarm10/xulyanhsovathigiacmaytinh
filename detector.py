import cv2
from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="best3.pt"):
        self.model = YOLO(model_path)

    def detect_image(self, path):
        img = cv2.imread(path)
        if img is None:
            return None

        results = self.model(img)
        return results[0].plot()

    def detect_video(self, path, callback, is_running):
        cap = cv2.VideoCapture(path)

        while is_running():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame)
            annotated = results[0].plot()

            callback(annotated)

        cap.release()

    def detect_webcam(self, callback, is_running):
        cap = cv2.VideoCapture(0)

        while is_running():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            results = self.model(frame)
            annotated = results[0].plot()

            callback(annotated)

        cap.release()

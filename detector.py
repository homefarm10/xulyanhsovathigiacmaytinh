import cv2
from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="D:\\Duong\\XLASvaTGMT\\code\\xulyanhso\\best4.pt"):
        self.model = YOLO(model_path)

    def detect_image(self, path):
        img = cv2.imread(path)
        if img is None: # kiểm tra ảnh có đọc được không
            return None

        results = self.model(img) # chạy model YOLO
        return results[0].plot() # trả về kết quả plot():vẽ bounding box, tên object, confidence

    def detect_video(self, path, callback, is_running):
        cap = cv2.VideoCapture(path)#VideoCapture dùng để:đọc video, đọc webcam

        while is_running(): #Lặp liên tục miễn: app chưa stop, user chưa bấm dừng
            ret, frame = cap.read() #ret: True → đọc thành công False → hết video, frame: ảnh hiện tại của video
            if not ret:
                break

            results = self.model(frame) # detect tung frame
            annotated = results[0].plot() # trả về kết quả plot():vẽ bounding box, tên object, confidence

            callback(annotated) #callback là hàm(bên ui là hàm update_frame(frame)) update GUI, hiển thị frame lên Tkinter

        cap.release() #Đóng file video.

    def detect_webcam(self, callback, is_running):
        cap = cv2.VideoCapture(0) # 0 = webcam mặc định

        while is_running():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1) #frame = cv2.flip(frame, 1): lật ngang, Giống camera selfie. giơ tay phải sẽ thấy bên trái

            results = self.model(frame)
            annotated = results[0].plot()

            callback(annotated) # gủi kết quả

        cap.release()

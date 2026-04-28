# # dùng cho webcam
# import cv2
# from ultralytics import YOLO

# # load model
# model = YOLO("best.pt")

# # mở webcam (0 = webcam laptop)
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # predict
#     results = model(frame)

#     # vẽ kết quả
#     annotated_frame = results[0].plot()

#     cv2.imshow("YOLO Webcam", annotated_frame)

#     # bấm ESC để thoát
#     if cv2.waitKey(25) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()

# dung cho video nhấn ESC để dừng
import cv2
from ultralytics import YOLO

# load model
model = YOLO("best.pt")

# mở video
cap = cv2.VideoCapture("testvideo.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # predict
    results = model(frame)

    # vẽ box lên frame
    annotated_frame = results[0].plot()

    # hiển thị
    cv2.imshow("YOLO Detection", annotated_frame)

    # bấm ESC để thoát
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

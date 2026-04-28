from ultralytics import YOLO

model = YOLO("best.pt")

results = model(r"D:\Duong\XLASvaTGMT\code\test7.jpg", save=True)
# results = model.predict(
#     source='D:\\Duong\\XLASvaTGMT\\code\\Student Behaviour Detection\\test\\images',  # folder ảnh test
#     conf=0.5, # chỉ hiện các đối tượng mà mô hình tự tin ít nhất 50% trở lên là đúng
#     save=True
# )
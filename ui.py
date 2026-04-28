import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from detector import Detector
import threading  
detector = Detector()

running = False
# ================= HIỂN THỊ =================

def show_menu():
    btn_img.pack(pady=5)
    btn_video.pack(pady=5)
    btn_webcam.pack(pady=5)
    btn_stop.pack_forget()

def show_stop():
    btn_img.pack_forget()
    btn_video.pack_forget()
    btn_webcam.pack_forget()
    btn_stop.pack(pady=10)

def stop():
    global running
    running = False
    show_menu()

def show_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = img.resize((500, 400))

    imgtk = ImageTk.PhotoImage(image=img)

    panel.imgtk = imgtk          # ⚠️ giữ reference (QUAN TRỌNG)
    panel.config(image=imgtk)   


# ================= IMAGE =================
def choose_image():
    global running
    show_stop()
    running = True

    path = filedialog.askopenfilename()
    if not path:
        stop()
        return

    result = detector.detect_image(path)
    if result is not None:
        show_frame(result)

    stop()



# ================= VIDEO =================
def choose_video():
    global running
    show_stop()
    running = True

    path = filedialog.askopenfilename()
    if not path:
        stop()
        return

    def run():
        detector.detect_video(path, update_frame)
        stop()

    threading.Thread(target=run, daemon=True).start()



# ================= WEBCAM =================
def open_webcam():
    global running
    show_stop()
    running = True

    def run():
        detector.detect_webcam(update_frame, lambda: running)
        stop()

    threading.Thread(target=run, daemon=True).start()



# callback update frame
def update_frame(frame):
    if not running:
        return

    show_frame(frame)
    root.update()


# ================= UI =================

root = tk.Tk()
root.title("YOLO Detection System")
root.geometry("600x550")
btn_stop = tk.Button(root, text="STOP", command=stop, width=20, bg="red", fg="white")
btn_stop.pack_forget()
title = tk.Label(root, text="YOLO Detection", font=("Arial", 20))
title.pack(pady=10)

panel = tk.Label(root)
panel.pack()

btn_img = tk.Button(root, text="Chọn ảnh", command=choose_image, width=20)
btn_img.pack(pady=5)

btn_video = tk.Button(root, text="Chọn video", command=choose_video, width=20)
btn_video.pack(pady=5)

btn_webcam = tk.Button(root, text="Mở webcam", command=open_webcam, width=20)
btn_webcam.pack(pady=5)

btn_exit = tk.Button(root, text="Thoát", command=root.quit, width=20)
btn_exit.pack(pady=10)

root.mainloop()

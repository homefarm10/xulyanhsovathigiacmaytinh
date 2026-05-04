import threading
import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk

from detector import Detector


detector = Detector()
running = False
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 560


# ================= HIEN THI =================
def show_menu():
    panel.config(image="", text="")
    panel.imgtk = None
    panel_frame.pack_forget()
    btn_stop.pack_forget()
    menu_frame.pack(expand=True)
    btn_img.pack(pady=5)
    btn_video.pack(pady=5)
    btn_webcam.pack(pady=5)
    btn_exit.pack(pady=10)


def show_stop():
    menu_frame.pack_forget()
    btn_img.pack_forget()
    btn_video.pack_forget()
    btn_webcam.pack_forget()
    btn_exit.pack_forget()
    panel_frame.pack(pady=15)
    panel.config(image="", text="Dang xu ly...")
    btn_stop.pack(pady=10)


def stop():
    global running
    running = False
    show_menu()


def finish_job():
    global running
    running = False
    root.after(0, show_menu)


def show_frame(frame):
    if not running:
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img.thumbnail((DISPLAY_WIDTH, DISPLAY_HEIGHT), Image.Resampling.LANCZOS)

    imgtk = ImageTk.PhotoImage(image=img)
    panel.imgtk = imgtk
    panel.config(image=imgtk, text="")


# ================= IMAGE =================
def choose_image():
    global running
    show_stop()
    running = True

    path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("All files", "*.*"),
        ]
    )
    if not path:
        stop()
        return

    result = detector.detect_image(path)
    if running and result is not None:
        show_frame(result)


# ================= VIDEO =================
def choose_video():
    global running
    show_stop()
    running = True

    path = filedialog.askopenfilename(
        filetypes=[
            ("Video files", "*.mp4 *.avi *.mov *.mkv"),
            ("All files", "*.*"),
        ]
    )
    if not path:
        stop()
        return

    def run():
        detector.detect_video(path, update_frame, lambda: running)
        finish_job()

    threading.Thread(target=run, daemon=True).start()


# ================= WEBCAM =================
def open_webcam():
    global running
    show_stop()
    running = True

    def run():
        detector.detect_webcam(update_frame, lambda: running)
        finish_job()

    threading.Thread(target=run, daemon=True).start()


def update_frame(frame):
    if running:
        root.after(0, show_frame, frame)


def close_app():
    global running
    running = False
    root.destroy()


# ================= UI =================
root = tk.Tk()
root.title("YOLO Detection System")
root.geometry("1000x720")
root.resizable(False, False)

menu_frame = tk.Frame(root)

panel_frame = tk.Frame(
    root,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    bg="#f2f2f2",
    relief="sunken",
    bd=1,
)
panel_frame.pack_propagate(False)

panel = tk.Label(panel_frame, text="", bg="#f2f2f2")
panel.pack(expand=True)

btn_stop = tk.Button(root, text="STOP", command=stop, width=20, bg="red", fg="white")

btn_img = tk.Button(menu_frame, text="Chon anh", command=choose_image, width=20)

btn_video = tk.Button(menu_frame, text="Chon video", command=choose_video, width=20)

btn_webcam = tk.Button(menu_frame, text="Mo webcam", command=open_webcam, width=20)

btn_exit = tk.Button(menu_frame, text="Thoat", command=close_app, width=20)

root.protocol("WM_DELETE_WINDOW", close_app)
show_menu()
root.mainloop()
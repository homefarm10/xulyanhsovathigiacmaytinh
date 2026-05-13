import threading
import tkinter as tk
from tkinter import filedialog, ttk

import cv2
from PIL import Image, ImageTk

from detector import Detector


detector = Detector()
running = False
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 560
BG_COLOR = "#eef2f7"
SURFACE_COLOR = "#ffffff"
PRIMARY_COLOR = "#2563eb"
DANGER_COLOR = "#dc2626"
TEXT_COLOR = "#0f172a"
MUTED_COLOR = "#64748b"
BORDER_COLOR = "#d8dee9"


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command,
        bg_color,
        hover_color,
        fg_color="#ffffff",
        parent_bg=SURFACE_COLOR,
        width=190,
        height=54,
        radius=18,
        font=("Segoe UI", 11, "bold"),
    ):
        super().__init__(
            parent,
            width=width,
            height=height + 8,
            bg=parent_bg,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.width_value = width
        self.height_value = height
        self.radius = radius
        self.font = font
        self.is_hovered = False
        self.draw()

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def draw(self):
        self.delete("all")
        y_offset = 1 if self.is_hovered else 5
        shadow_color = "#bac6d8" if self.is_hovered else "#d5dce8"
        fill_color = self.hover_color if self.is_hovered else self.bg_color

        self.rounded_rect(
            4,
            y_offset + 5,
            self.width_value - 4,
            y_offset + self.height_value + 5,
            self.radius,
            fill=shadow_color,
            outline="",
        )
        self.rounded_rect(
            3,
            y_offset,
            self.width_value - 5,
            y_offset + self.height_value,
            self.radius,
            fill=fill_color,
            outline="",
        )
        self.create_text(
            self.width_value // 2,
            y_offset + self.height_value // 2,
            text=self.text,
            fill=self.fg_color,
            font=self.font,
        )

    def on_enter(self, _event):
        self.is_hovered = True
        self.draw()

    def on_leave(self, _event):
        self.is_hovered = False
        self.draw()

    def on_click(self, _event):
        if self.command:
            self.command()


# ================= HIEN THI =================
def show_menu():
    panel.config(image="", text="")
    panel.imgtk = None
    panel_frame.pack_forget()
    action_bar.pack_forget()
    menu_frame.pack(expand=True)
    status_var.set("San sang nhan dien tu anh, video hoac webcam")


def show_stop():
    menu_frame.pack_forget()
    action_bar.pack(fill="x", pady=(18, 10))
    panel_frame.pack(pady=(0, 24))
    panel.config(image="", text="Dang xu ly...")
    status_var.set("Dang xu ly, co the dung bat ky luc nao")


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
    status_var.set("Ket qua nhan dien dang hien thi")


# ================= IMAGE =================
def choose_image():
    global running
    show_stop()
    running = True
    status_var.set("Dang cho chon anh...")

    path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("All files", "*.*"),
        ]
    )
    if not path:
        stop()
        return

    status_var.set("Dang xu ly anh...")

    def run():
        result = detector.detect_image(path)
        if running and result is not None:
            root.after(0, show_frame, result)

    threading.Thread(target=run, daemon=True).start()


# ================= VIDEO =================
def choose_video():
    global running
    show_stop()
    running = True
    status_var.set("Dang cho chon video...")

    path = filedialog.askopenfilename(
        filetypes=[
            ("Video files", "*.mp4 *.avi *.mov *.mkv"),
            ("All files", "*.*"),
        ]
    )
    if not path:
        stop()
        return
    status_var.set("Dang xu ly video...")

    def run():
        detector.detect_video(path, update_frame, lambda: running)
        finish_job()

    threading.Thread(target=run, daemon=True).start()


# ================= WEBCAM =================
def open_webcam():
    global running
    show_stop()
    running = True
    status_var.set("Dang mo webcam...")

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
root.title("Student Behaviour Detection")
root.geometry("1040x760")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "App.TFrame",
    background=BG_COLOR,
)
style.configure(
    "Surface.TFrame",
    background=SURFACE_COLOR,
    relief="flat",
)
style.configure(
    "Title.TLabel",
    background=BG_COLOR,
    foreground=TEXT_COLOR,
    font=("Segoe UI", 24, "bold"),
)
style.configure(
    "Subtitle.TLabel",
    background=BG_COLOR,
    foreground=MUTED_COLOR,
    font=("Segoe UI", 11),
)
style.configure(
    "Status.TLabel",
    background=BG_COLOR,
    foreground=MUTED_COLOR,
    font=("Segoe UI", 10),
)
style.configure(
    "Action.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=(18, 13),
    background=PRIMARY_COLOR,
    foreground="#ffffff",
    borderwidth=0,
    focusthickness=0,
)
style.map(
    "Action.TButton",
    background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
    foreground=[("disabled", "#dbeafe")],
)
style.configure(
    "Secondary.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=(18, 13),
    background="#e2e8f0",
    foreground=TEXT_COLOR,
    borderwidth=0,
    focusthickness=0,
)
style.map(
    "Secondary.TButton",
    background=[("active", "#cbd5e1"), ("pressed", "#b6c2d2")],
)
style.configure(
    "Danger.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=(18, 13),
    background=DANGER_COLOR,
    foreground="#ffffff",
    borderwidth=0,
    focusthickness=0,
)
style.map(
    "Danger.TButton",
    background=[("active", "#b91c1c"), ("pressed", "#991b1b")],
)

app = ttk.Frame(root, style="App.TFrame", padding=(44, 28))
app.pack(fill="both", expand=True)

header = ttk.Frame(app, style="App.TFrame")
header.pack(fill="x")

title = ttk.Label(
    header,
    text="Student Behaviour Detection",
    style="Title.TLabel",
)
title.pack(anchor="w")

subtitle = ttk.Label(
    header,
    text="Nhan dien hanh vi hoc sinh bang YOLO tu anh, video hoac camera truc tiep.",
    style="Subtitle.TLabel",
)
subtitle.pack(anchor="w", pady=(6, 0))

status_var = tk.StringVar(value="San sang nhan dien tu anh, video hoac webcam")
status = ttk.Label(app, textvariable=status_var, style="Status.TLabel")
status.pack(anchor="w", pady=(14, 0))

menu_frame = ttk.Frame(app, style="App.TFrame")

menu_card = tk.Frame(
    menu_frame,
    bg=SURFACE_COLOR,
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=BORDER_COLOR,
    padx=34,
    pady=30,
)
menu_card.pack()

menu_title = tk.Label(
    menu_card,
    text="Chon nguon dau vao",
    bg=SURFACE_COLOR,
    fg=TEXT_COLOR,
    font=("Segoe UI", 18, "bold"),
)
menu_title.pack(anchor="w")

menu_hint = tk.Label(
    menu_card,
    text="Tai anh, mo video co san, hoac dung webcam de bat dau nhan dien.",
    bg=SURFACE_COLOR,
    fg=MUTED_COLOR,
    font=("Segoe UI", 10),
)
menu_hint.pack(anchor="w", pady=(6, 22))

button_grid = ttk.Frame(menu_card, style="Surface.TFrame")
button_grid.pack(fill="x")

panel_frame = tk.Frame(
    app,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    bg="#f8fafc",
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=BORDER_COLOR,
)
panel_frame.pack_propagate(False)

panel = tk.Label(
    panel_frame,
    text="Ket qua se hien thi tai day",
    bg="#f8fafc",
    fg=MUTED_COLOR,
    font=("Segoe UI", 14, "bold"),
)
panel.pack(expand=True)

action_bar = ttk.Frame(app, style="App.TFrame")
btn_stop = RoundedButton(
    action_bar,
    text="Dung xu ly",
    command=stop,
    bg_color=DANGER_COLOR,
    hover_color="#b91c1c",
    parent_bg=BG_COLOR,
    width=180,
)
btn_stop.pack(side="right")

btn_img = RoundedButton(
    button_grid,
    text="Chon anh",
    command=choose_image,
    bg_color=PRIMARY_COLOR,
    hover_color="#1d4ed8",
)
btn_img.grid(row=0, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))

btn_video = RoundedButton(
    button_grid,
    text="Chon video",
    command=choose_video,
    bg_color=PRIMARY_COLOR,
    hover_color="#1d4ed8",
)
btn_video.grid(row=0, column=1, sticky="ew", pady=(0, 12))

btn_webcam = RoundedButton(
    button_grid,
    text="Mo webcam",
    command=open_webcam,
    bg_color=PRIMARY_COLOR,
    hover_color="#1d4ed8",
)
btn_webcam.grid(row=1, column=0, sticky="ew", padx=(0, 12))

btn_exit = RoundedButton(
    button_grid,
    text="Thoat",
    command=close_app,
    bg_color="#e2e8f0",
    hover_color="#cbd5e1",
    fg_color=TEXT_COLOR,
)
btn_exit.grid(row=1, column=1, sticky="ew")

button_grid.columnconfigure(0, weight=1, minsize=190)
button_grid.columnconfigure(1, weight=1, minsize=190)

root.protocol("WM_DELETE_WINDOW", close_app)
show_menu()
root.mainloop()

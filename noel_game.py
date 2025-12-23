import tkinter as tk
from tkinter import filedialog
import random, threading, time
import pygame
from PIL import Image, ImageTk

# ================== CONFIG ==================
config = {
    "bg": "background.jpg",
    "spin": "spin.mp3",
    "win": "win.mp3",
    "notify": "notify.png",
    "notify_small": "notify_small.png"
}

# ================== AUDIO ==================
pygame.mixer.init()

def stop_all_audio():
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def play_spin():
    stop_all_audio()
    pygame.mixer.music.load(config["spin"])
    pygame.mixer.music.play(-1)

def play_win():
    stop_all_audio()
    pygame.mixer.Sound(config["win"]).play()

# ================== RANDOM ==================
def weighted_random(a, b):
    split = 1_900_000
    if random.random() < 0.5:
        t = random.random() ** 2.5
        return int(a + t * (min(split, b) - a))
    t = random.random() ** 4
    return int(split + t * (b - split))

# ================== UI ROOT ==================
root = tk.Tk()
root.title("🎄 Quay Số Noel 🎄")
root.geometry("1280x720")
root.minsize(900, 600)

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# ================== BACKGROUND (COVER MODE) ==================
bg_raw = None
bg_img = None
bg_id = canvas.create_image(0, 0, anchor="nw")

def load_background():
    global bg_raw
    try:
        bg_raw = Image.open(config["bg"])
    except:
        bg_raw = None

def draw_bg(event=None):
    global bg_img
    if not bg_raw:
        return

    w, h = canvas.winfo_width(), canvas.winfo_height()
    if w < 10 or h < 10:
        return

    img_w, img_h = bg_raw.size
    scale = max(w / img_w, h / img_h)  # 🔥 COVER

    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    img = bg_raw.resize((new_w, new_h), Image.LANCZOS)

    # CROP GIỮA
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    img = img.crop((left, top, left + w, top + h))

    bg_img = ImageTk.PhotoImage(img)
    canvas.itemconfig(bg_id, image=bg_img)
    canvas.coords(bg_id, 0, 0)

load_background()
canvas.bind("<Configure>", draw_bg)


# ================== TEXT ==================
title_id = canvas.create_text(
    0, 0,
    text="🎄Noel tới rồi! THƠM chúc HƯƠNG tất cả , trừ vất vả ....GIỰT QUÀ THÔIIIII🎄💗 YÊU HƯƠNG 💗",
    fill="#ff69b4",   # màu hồng
    font=("Arial", 42, "bold"),
    width=900,
    justify="center"
)

number_id = canvas.create_text(
    0, 0,
    text="------",
    fill="yellow",
    font=("Arial", 90, "bold"),
    width=900,
    justify="center"
)

# ================== STATE ==================
running = False
stop_count = 0
notify_id = notify_bg_id = None
notify_small_id = None
notify_img = notify_small_img = None

# ================== SPIN ==================
def fake_spin():
    global running
    running = True
    play_spin()
    a, b = int(entry_min.get()), int(entry_max.get())
    while running:
        canvas.itemconfig(number_id, text=f"{random.randint(a, b):,}")
        time.sleep(speed.get() / 1000)

def start():
    global stop_count
    stop_count = 0
    clear_notify()
    if running:
        return
    threading.Thread(target=fake_spin, daemon=True).start()

def stop():
    global running, stop_count
    stop_count += 1

    if stop_count == 1:
        running = False
        stop_all_audio()
        res = weighted_random(int(entry_min.get()), int(entry_max.get()))
        canvas.itemconfig(number_id, text=f"{res:,}")
        play_win()

    elif stop_count == 2:
        show_notify()

# ================== NOTIFY ==================
def show_notify():
    global notify_id, notify_img, notify_bg_id
    global notify_small_id, notify_small_img

    w, h = canvas.winfo_width(), canvas.winfo_height()

    notify_bg_id = canvas.create_rectangle(
        0, 0, w, h, fill="black", stipple="gray50"
    )

    img = Image.open(config["notify"]).resize(
        (int(w * 0.6), int(h * 0.6)), Image.LANCZOS
    )
    notify_img = ImageTk.PhotoImage(img)
    notify_id = canvas.create_image(w // 2, h // 2, image=notify_img)

    try:
        img_s = Image.open(config["notify_small"]).resize(
            (220, 220), Image.LANCZOS
        )
        notify_small_img = ImageTk.PhotoImage(img_s)
        notify_small_id = canvas.create_image(
            w - 140, 140, image=notify_small_img
        )
    except:
        pass

def clear_notify():
    global notify_id, notify_bg_id, notify_small_id
    for i in (notify_id, notify_bg_id, notify_small_id):
        if i:
            canvas.delete(i)
    notify_id = notify_bg_id = notify_small_id = None

# ================== SETTINGS ==================
def open_settings():
    win = tk.Toplevel(root)
    win.title("⚙ Cài đặt")
    win.geometry("520x420")
    win.resizable(False, False)

    def choose(k):
        p = filedialog.askopenfilename(
            filetypes=[("Media", "*.png *.jpg *.mp3")]
        )
        if p:
            config[k] = p
            if k == "bg":
                load_background()
                draw_bg()

    items = [
        ("🎵 Nhạc quay", "spin"),
        ("🎵 Nhạc thắng", "win"),
        ("🖼 Background", "bg"),
        ("🖼 Notify lớn", "notify"),
        ("🔔 Notify nhỏ", "notify_small"),
    ]

    for t, k in items:
        tk.Label(win, text=t).pack(pady=5)
        tk.Button(win, text="Chọn file",
                  command=lambda x=k: choose(x)).pack()

# ================== CONTROLS ==================
entry_min = tk.Entry(root, font=("Arial", 18), justify="center")
entry_min.insert(0, "1000000")

entry_max = tk.Entry(root, font=("Arial", 18), justify="center")
entry_max.insert(0, "2000000")

btn_start = tk.Button(
    root, text="▶ QUAY",
    font=("Arial", 26),
    bg="green", fg="white",
    command=start
)

btn_stop = tk.Button(
    root, text="⏹ DỪNG",
    font=("Arial", 26),
    bg="red", fg="white",
    command=stop
)

btn_setting = tk.Button(
    root, text="⚙ CÀI ĐẶT",
    font=("Arial", 20),
    command=open_settings
)

speed = tk.Scale(
    root, from_=20, to=200,
    orient="horizontal", label="TỐC ĐỘ"
)
speed.set(60)

# ================== LAYOUT ==================
def reposition(e=None):
    w, h = canvas.winfo_width(), canvas.winfo_height()

    canvas.coords(title_id, w // 2, int(h * 0.15))
    canvas.coords(number_id, w // 2, h // 2)

    canvas.create_window(w // 2 - 200, int(h * 0.3), window=entry_min)
    canvas.create_window(w // 2 + 200, int(h * 0.3), window=entry_max)

    canvas.create_window(w // 2 - 200, int(h * 0.82), window=btn_start)
    canvas.create_window(w // 2 + 200, int(h * 0.82), window=btn_stop)
    canvas.create_window(w // 2, int(h * 0.72), window=btn_setting)
    canvas.create_window(w // 2, int(h * 0.92), window=speed)

canvas.bind("<Configure>", reposition)

# ================== START ==================
root.mainloop()

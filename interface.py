import tkinter as tk
import sys
import os
import subprocess

text_scroll = False
scroll_time = 30

if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(APP_DIR)

if "--scroller" in sys.argv:
    import doomscroller
    sys.exit()

try:
    with open("save_file.txt", "r") as file:
        lines = file.readlines()
    text_scroll = lines[0].strip() == "True"
    scroll_time = int(lines[1].strip())
except (FileNotFoundError, IndexError, ValueError):
    text_scroll = False
    scroll_time = 30

screen_w = 800
screen_h = 600
scroll_button_text = "Scroll method: Speak"

doomscroller = None

screen = tk.Tk()
screen.title("Doomscroller")
screen.geometry(f"{screen_w}x{screen_h}")

title = tk.Label(screen, text="Doomscroller", font=("Arial", 50))
title.place(x=screen_w/2, y=screen_h/6, anchor="center")

def clicked():
    global text_scroll
    global scroll_button_text

    if text_scroll:
        text_scroll = False
        scroll_button_text = "Scroll method: Speak"
        scroll_method.config(text=scroll_button_text)
        scroll_time_label.config(state="disabled")
        scroll_time_entry.config(state="disabled")
    else:
        text_scroll = True
        scroll_button_text = "Scroll method: Time"
        scroll_method.config(text=scroll_button_text)
        scroll_time_label.config(state="normal")
        scroll_time_entry.config(state="normal")

def run():
    global scroll_time
    global doomscroller

    if doomscroller is not None:
        doomscroller.terminate()
        doomscroller = None

    try:
        scroll_time = int(scroll_time_entry.get())
        scroll_time_entry.delete(0, tk.END)
    except ValueError:
        pass

    with open("save_file.txt", "w") as file:
        file.write(str(text_scroll) + "\n")
        file.write(str(scroll_time))

    if getattr(sys, "frozen", False):
        command = [sys.executable, "--scroller"]
    else:
        command = [sys.executable, os.path.abspath(__file__), "--scroller"]
    
    doomscroller = subprocess.Popen(command)

def exit():
    global doomscroller

    if doomscroller is not None:
        doomscroller.terminate()
    screen.destroy()

scroll_method = tk.Button(screen, text=scroll_button_text, command=clicked, bg="black", fg="white", font=("Arial", 16), padx=5, pady=5)
scroll_method.place(x=screen_w/2, y=screen_h/2, anchor="center")

scroll_time_label = tk.Label(screen, text="Scroll time (seconds):", font=("Arial", 10), state="disabled")
scroll_time_label.place(x=screen_w/2 - 142, y=screen_h/2 + 50, anchor="center")

scroll_time_entry = tk.Entry(screen, width=10, font=("Arial", 15), fg="black", bg="white", state="disabled", bd=6, selectborderwidth=6)
scroll_time_entry.place(x=screen_w/2, y=screen_h/2 + 50, anchor="center")

start = tk.Button(screen, text="Start", font=("Arial", 20), command=run)
start.place(x=screen_w/2, y=screen_h - 50, anchor="center")

screen.protocol("WM_DELETE_WINDOW", exit)

if text_scroll:
    scroll_method.config(text="Scroll method: Time")
    scroll_time_label.config(state="normal")
    scroll_time_entry.config(state="normal")

screen.mainloop()
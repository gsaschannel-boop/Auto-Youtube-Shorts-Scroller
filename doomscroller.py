import speech_recognition as sr
import pygetwindow as gw
import pyautogui
import ctypes
import time

with open("save_file.txt", "r") as file:
    lines = file.readlines()

text_scroll = lines[0].strip() == "True"
scroll_time = int(lines[1].strip())
    
r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 5
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def find_shorts_window() -> gw.Window | None:
    for w in gw.getAllWindows():
        if "YouTube" in w.title and "Google Chrome" in w.title:
            return w
        
    return None

def focus(hwnd) -> None:
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)
    fg_thread = user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), None)
    my_thread = kernel32.GetCurrentThreadId()
    user32.AttachThreadInput(my_thread, fg_thread, True)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(my_thread, fg_thread, False)

    return None

def scroll_youtube(key) -> None:
    yt = find_shorts_window()
    if yt is None:
        return

    previous = user32.GetForegroundWindow()
    old_x, old_y = pyautogui.position()

    focus(yt._hWnd)
    time.sleep(0.3)
    pyautogui.moveTo(yt.left + yt.width // 2, yt.top + yt.height // 2)
    pyautogui.scroll(-120 if key == "down" else 120)
    time.sleep(0.1)

    pyautogui.moveTo(old_x, old_y)
    focus(previous)

    return None

if not text_scroll:
    with sr.Microphone() as source:
        while True:
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
                text = r.recognize_google(audio).lower()

                if "up" in text:
                    scroll_youtube("up")
                elif "scroll" in text:
                    scroll_youtube("down")

            except sr.UnknownValueError:
                pass
            except sr.WaitTimeoutError:
                pass
            except sr.RequestError as e:
                pass
else:
    while True:
        scroll_youtube("down")
        time.sleep(scroll_time)
import numpy as np
import mss
import pygetwindow as gw
from predict import predict
import cv2

# Get the Camo Studio Window
window = gw.getWindowsWithTitle("Camo Studio")[0]
window.moveTo(-2780, -248)
window.resizeTo(500, 600)


with mss.mss() as sct:
    monitor = sct.monitors[0]

    # Section being recorded
    region = {
        "top": monitor["top"] + 300,
        "left": monitor["left"] + 200,
        "width": 1500,
        "height": 800
    }

    while True:
        # Get the current frame
        screenshot = sct.grab(region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        gesture = predict(frame)

        print(gesture)
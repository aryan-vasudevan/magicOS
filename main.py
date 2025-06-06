import numpy as np
import mss
import pygetwindow as gw
import cv2
import time
import json
from predict import predict
from execute import execute

MAPPINGS_FILE = "gesture_mappings.json"

# Get the Camo Studio Window
window = gw.getWindowsWithTitle("Camo Studio")[0]
window.moveTo(-2780, -248)
window.resizeTo(500, 600)

# Cooldown
COOLDOWN_PERIOD = 2.0
last_action_time = 0
cooldown_active = False

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

        # Time for cooldown
        current_time = time.time()

        # If a gesture is made outside of cooldown
        if not cooldown_active and gesture != "neutral":
            print(f"Gesture detected: {gesture}")

            # Execute necessary action
            with open(MAPPINGS_FILE, "r") as f:
                mappings = json.load(f)
            action = mappings.get(gesture)
            execute(action)
            
            # Reset cooldown
            cooldown_active = True
            last_action_time = current_time

        elif cooldown_active:
            if current_time - last_action_time >= COOLDOWN_PERIOD:
                cooldown_active = False

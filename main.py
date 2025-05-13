import cv2
import numpy as np
import mss
import os
import pygetwindow as gw
from dotenv import load_dotenv
from roboflow import Roboflow

load_dotenv()

# Roboflow model
rf = Roboflow(api_key=os.getenv("API_KEY"))
project = rf.workspace("personal-nh81v").project("magicos")
model = project.version(1).model

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

        # Convert BGRA to RGB to ensure compatibility
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        # Make prediction of the frame
        predictions = model.predict(frame, confidence=40, overlap=30).json()

        # Process predictions through rf model
        for prediction in predictions['predictions']:
            gesture = prediction['class']
            confidence = prediction['confidence']

            if gesture == "1" and confidence >= 0.6:
                print("swipe")
            elif gesture == "2" and confidence >= 0.42:
                print("snap")
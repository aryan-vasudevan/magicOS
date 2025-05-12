import cv2
import numpy as np
import mss
import os
from dotenv import load_dotenv
from roboflow import Roboflow

load_dotenv()

# Roboflow model
rf = Roboflow(api_key=os.getenv("API_KEY"))
project = rf.workspace("personal-nh81v").project("magicos")
model = project.version(1).model

with mss.mss() as sct:
    monitor = sct.monitors[0]

    # Section being recorded
    region = {
        "top": monitor["top"] + 470,
        "left": monitor["left"] + 770,
        "width": 1440,
        "height": 1200
    }

    while True:
        # Get the current frame
        screenshot = sct.grab(region)
        frame = np.array(screenshot)

        # Convert BGRA to RGB to ensure compatibility
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        # Make prediction of the frame
        predictions = model.predict(frame_rgb, confidence=40, overlap=30).json()

        # Process predictions through rf model
        for prediction in predictions['predictions']:
            gesture = prediction['class']
            confidence = prediction['confidence']
            
            # Only include reasonable predictions
            if confidence > 0.75:
                print("swipe" if gesture == "1" else "snap")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()

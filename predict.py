from roboflow import Roboflow
import os
from dotenv import load_dotenv

load_dotenv()

# Roboflow model
rf = Roboflow(api_key=os.getenv("API_KEY"))
project = rf.workspace("personal-nh81v").project("magicos")
model = project.version(1).model

def predict(frame):
    # Make prediction of the frame
        predictions = model.predict(frame, confidence=40, overlap=30).json()

        # Process predictions through rf model
        for prediction in predictions['predictions']:
            gesture = prediction['class']
            confidence = prediction['confidence']

            if gesture == "1" and confidence >= 0.1:
                return "swipe"
            elif gesture == "2" and confidence >= 0.1:
                return "snap"
        
        return "neutral"
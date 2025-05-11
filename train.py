import os
from dotenv import load_dotenv
from roboflow import Roboflow

load_dotenv()

rf = Roboflow(api_key=os.getenv("API_KEY"))
project = rf.workspace("personal-nh81v").project("magicos")
version = project.version(1)
dataset = version.download("yolov8")
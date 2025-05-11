import cv2
import numpy as np
import mss

with mss.mss() as sct:
    print(sct.monitors)
    monitor= sct.monitors[0]  # Adjust if needed

    # Define a smaller region within the secondary monitor (adjust as needed)
    region = {
        "top": monitor["top"] + 470,     # y-offset inside monitor
        "left": monitor["left"] + 770,   # x-offset inside monitor
        "width": 1440,
        "height": 1200
    }

    while True:
        screenshot = sct.grab(region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        cv2.imshow("Camo Preview (Screen Capture)", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()

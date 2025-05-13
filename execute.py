import subprocess
import keyboard

def execute(action):
    if action["type"] == "keybind":
        keys = action.get("value", "")
        if keys:
            keyboard.send(keys)
            
    elif action["type"] == "app":
        app_path = action.get("value", "")
        if app_path:
            try:
                subprocess.Popen(app_path)
            except Exception as e:
                print(f"Failed to launch application: {e}")

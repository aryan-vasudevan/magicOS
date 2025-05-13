import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import winapps
import json
import threading
import keyboard
import os

MAPPINGS_FILE = "gesture_mappings.json"

class magicOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("magicOS")
        self.style = Style("darkly")
        self.selected_gesture = tk.StringVar()
        self.action_type = tk.StringVar(value="keybind")
        self.selected_app = tk.StringVar()
        self.keybind = tk.StringVar()
        self.app_list = self.get_installed_apps()

        self.create_layout()

    def create_layout(self):
        sidebar = ttk.Frame(self.root, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        main_panel = ttk.Frame(self.root)
        main_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(sidebar, text="Gestures", font=("Segoe UI", 12, "bold")).pack(pady=5)
        gestures = ["swipe", "snap"]
        for g in gestures:
            ttk.Radiobutton(
                sidebar,
                text=g.capitalize(),
                variable=self.selected_gesture,
                value=g,
                command=self.on_gesture_select,
                style="success"
            ).pack(fill="x", pady=5)

        ttk.Label(main_panel, text="Choose Action Type:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=5)
        ttk.Radiobutton(main_panel, text="Record Keybind", variable=self.action_type, value="keybind",
                        command=self.update_action_panel).pack(anchor="w", pady=2)
        ttk.Radiobutton(main_panel, text="Open Application", variable=self.action_type, value="app",
                        command=self.update_action_panel).pack(anchor="w", pady=2)

        self.action_container = ttk.Frame(main_panel)
        self.action_container.pack(fill="x", pady=10)

        self.save_btn = ttk.Button(main_panel, text="Save Mapping", command=self.save_mapping)
        self.save_btn.pack(pady=10)

        self.update_action_panel()

    def on_gesture_select(self):
        print(f"Selected gesture: {self.selected_gesture.get()}")

    def record_keybind(self):
        self.keybind_display.config(text="Listening... Press your combo")

        def listen():
            combo = keyboard.read_hotkey(suppress=True)
            self.keybind.set(combo)
            self.keybind_display.config(text=combo)

        threading.Thread(target=listen, daemon=True).start()

    def update_action_panel(self):
        for widget in self.action_container.winfo_children():
            widget.destroy()

        if self.action_type.get() == "keybind":
            ttk.Label(self.action_container, text="Press a key combination below:").pack(anchor="w")
            self.keybind_display = ttk.Label(self.action_container, text="Not recorded", font=("Segoe UI", 10, "italic"))
            self.keybind_display.pack(pady=5)
            ttk.Button(self.action_container, text="Start Recording", command=self.record_keybind).pack()
        else:
            ttk.Label(self.action_container, text="Select an App to Launch:").pack(anchor="w")
            self.app_dropdown = ttk.Combobox(self.action_container, textvariable=self.selected_app)
            self.app_dropdown['values'] = [name for name, _ in self.app_list]
            self.app_dropdown.pack(fill="x", pady=5)

    def save_mapping(self):
        gesture = self.selected_gesture.get()
        if not gesture:
            messagebox.showwarning("No gesture", "Please select a gesture to map.")
            return

        if self.action_type.get() == "keybind":
            value = self.keybind.get().strip()
            if not value:
                messagebox.showwarning("Empty Keybind", "Please enter a keybind.")
                return
        else:
            app_name = self.selected_app.get()
            if not app_name:
                messagebox.showwarning("No App", "Please select an application.")
                return

            # Find the corresponding winapps object
            app_obj = next((app for name, app in self.app_list if name == app_name), None)
            if not app_obj:
                messagebox.showerror("Error", f"Application '{app_name}' not found.")
                return

            value = self.resolve_app_path(app_obj)
            if not value:
                messagebox.showerror("Error", f"Could not find executable for '{app_name}'.")
                return

        # Load existing mappings
        try:
            with open(MAPPINGS_FILE, "r") as f:
                mappings = json.load(f)
        except FileNotFoundError:
            mappings = {}

        mappings[gesture] = {
            "type": self.action_type.get(),
            "value": value
        }

        with open(MAPPINGS_FILE, "w") as f:
            json.dump(mappings, f, indent=4)

        messagebox.showinfo("Success", f"Mapped '{gesture}' to {self.action_type.get()}:\n{value}")

    def get_installed_apps(self):
        apps = list(winapps.list_installed())
        return sorted([(app.name, app) for app in apps], key=lambda x: x[0]) or [("No apps found", None)]

    def resolve_app_path(self, app):
        if app.install_location and os.path.isdir(app.install_location):
            for file in os.listdir(app.install_location):
                if file.lower().endswith(".exe"):
                    return os.path.join(app.install_location, file)
        return None

root = tk.Tk()
root.geometry("400x250")
root.resizable(False, False)
app = magicOSApp(root)
root.mainloop()

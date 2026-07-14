import json
import os
from tkinter import filedialog, messagebox

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "length": 16,
    "uppercase": True,
    "lowercase": True,
    "numbers": True,
    "symbols": True,
    "exclude_ambiguous": False,
    "prevent_repeats": True,
    "policy": "Enterprise"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            # Merge with defaults in case of missing keys in old saves
            merged = DEFAULT_SETTINGS.copy()
            merged.update(data)
            return merged
    except (json.JSONDecodeError, IOError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings_dict):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings_dict, f, indent=4)
    except IOError as e:
        print(f"Failed to save settings: {e}")


def export_history_to_txt(history_list):
    if not history_list:
        messagebox.showinfo("Export Empty", "There is no history to export.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="password_history.txt",
        title="Export Password History",
        filetypes=[("Text Files", "*.txt")]
    )

    if filepath:
        try:
            with open(filepath, "w") as f:
                f.write("Generated Password History\n")
                f.write("--------------------------\n\n")
                for pwd in history_list:
                    f.write(f"{pwd}\n")
            messagebox.showinfo("Success", "History exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save file:\n{e}")
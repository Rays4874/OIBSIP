import psutil
import os
import subprocess
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_battery():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        is_plugged = "plugged in" if battery.power_plugged else "on battery power"
        return f"Your battery is at {percent} percent and is currently {is_plugged}."
    return "I couldn't detect a battery. You might be on a desktop computer."

def get_cpu_ram():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return f"CPU usage is at {cpu} percent. RAM usage is at {ram} percent."

def get_system_report():
    battery = psutil.sensors_battery()
    bat_str = f"{battery.percent}%" if battery else "N/A"
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    
    return bat_str, cpu, ram

def get_audio_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def change_volume(action):
    try:
        volume = get_audio_interface()
        current_vol = volume.GetMasterVolumeLevelScalar()
        
        if action == "increase":
            new_vol = min(1.0, current_vol + 0.2) # Increase by 20%
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            return "Volume increased."
        elif action == "decrease":
            new_vol = max(0.0, current_vol - 0.2) # Decrease by 20%
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            return "Volume decreased."
        elif action == "mute":
            volume.SetMute(1, None)
            return "Audio muted."
        elif action == "unmute":
            volume.SetMute(0, None)
            return "Audio unmuted."
    except Exception as e:
        return f"I couldn't adjust the volume. Error: {str(e)}"

def open_app(app_name):
    apps = {
        "chrome": "start chrome",
        "vs code": "code",
        "notepad": "notepad",
        "calculator": "calc"
    }
    app_key = app_name.lower().strip()

    for key in apps:
        if key in app_key:
            subprocess.run(apps[key], shell=True)
            return f"Opening {key}."
            
    return f"I don't have a shortcut configured for {app_name}."

def close_app(app_name):
    app_name = app_name.lower().strip()
    closed = False
    
    process_map = {
        "chrome": "chrome.exe",
        "vs code": "Code.exe",
        "notepad": "notepad.exe"
    }
    
    target_process = process_map.get(app_name, f"{app_name}.exe")

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and target_process.lower() in proc.info['name'].lower():
            try:
                proc.kill()
                closed = True
            except psutil.AccessDenied:
                return f"I don't have permission to close {app_name}."
                
    if closed:
        return f"I have closed {app_name}."
    return f"I couldn't find {app_name} running."

def manage_folder(action, folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_path = os.path.join(desktop_path, folder_name.title())

    try:
        if action == "create":
            os.makedirs(target_path, exist_ok=True)
            return f"I have created the {folder_name} folder on your desktop."
        elif action == "delete":
            os.rmdir(target_path)
            return f"I have deleted the {folder_name} folder."
    except OSError:
        return f"I could not {action} the folder. Ensure it is empty and not currently open."

def open_downloads():
    path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.startfile(path)
    return "Opening your Downloads folder."

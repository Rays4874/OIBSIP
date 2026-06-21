import speech_recognition as sr
import edge_tts
import asyncio
import pygame
import datetime
import os
import webbrowser
import subprocess
from dotenv import load_dotenv

# Import our custom modules
from modules import wake_word
from modules import plugin_manager
from modules import memory
from modules import chat_ai
from modules import reminder
from modules import weather
from modules import email_module
from modules import system_control

AI_NAME = "Vector"

load_dotenv()


def get_contact_from_env(spoken_name):
    formatted_name = spoken_name.strip().replace(" ", "_").upper()
    env_key = f"CONTACT_{formatted_name}"
    return os.getenv(env_key)


pygame.mixer.init()


def speak(text):
    print(f"{AI_NAME}: {text}")
    audio_file = "temp_audio.mp3"

    async def generate_audio():
        communicate = edge_tts.Communicate(text, voice="en-US-ChristopherNeural", rate="+15%")
        await communicate.save(audio_file)

    asyncio.run(generate_audio())
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove(audio_file)


def invert_pronouns(text):
    words = text.split()
    replacements = {"i": "you", "me": "you", "my": "your", "mine": "yours", "am": "are"}
    for i, word in enumerate(words):
        if word in replacements:
            words[i] = replacements[word]
    return " ".join(words)


def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good morning! I am {AI_NAME}. How can I help you today?")
    elif 12 <= hour < 18:
        speak(f"Good afternoon! I am {AI_NAME}. How can I help you today?")
    else:
        speak(f"Good evening! I am {AI_NAME}. How can I help you today?")


def listen_command(timeout=8, phrase_time_limit=20):
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.5
    with sr.Microphone() as source:
        print("\n[ Listening... ]")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("[ Recognizing... ]")
            command = recognizer.recognize_google(audio).lower()
            print(f"User Command: '{command}'")
            return command
        except sr.UnknownValueError:
            print(f"{AI_NAME}: (Could not understand the audio)")
            return None
        except sr.RequestError as e:
            print(f"{AI_NAME}: Service error. {e}")
            return None
        except sr.WaitTimeoutError:
            return None


def execute_command(command):
    if command is None:
        return True

    if "battery percentage" in command or "battery level" in command:
        speak(system_control.get_battery())
        return True

    elif "cpu usage" in command or "how much ram" in command or "memory usage" in command:
        speak(system_control.get_cpu_ram())
        return True

    elif "increase volume" in command or "volume up" in command:
        speak(system_control.change_volume("increase"))
        return True

    elif "decrease volume" in command or "volume down" in command:
        speak(system_control.change_volume("decrease"))
        return True

    elif "mute volume" in command or "mute audio" in command:
        speak(system_control.change_volume("mute"))
        return True

    elif command.startswith("open app"):
        app = command.replace("open app", "").strip()
        speak(system_control.open_app(app))
        return True

    elif command.startswith("open vs code"):
        speak(system_control.open_app("vs code"))
        return True

    elif command.startswith("open chrome"):
        speak(system_control.open_app("chrome"))
        return True

    elif command.startswith("close app") or command.startswith("close chrome"):
        app = command.replace("close app", "").replace("close", "").strip()
        speak(system_control.close_app(app))
        return True

    elif "create a folder called" in command:
        folder = command.split("called")[-1].strip()
        speak(system_control.manage_folder("create", folder))
        return True

    elif "delete folder" in command:
        folder = command.replace("delete folder", "").strip()
        speak(system_control.manage_folder("delete", folder))
        return True

    elif "open downloads" in command:
        speak(system_control.open_downloads())
        return True

    elif "system report" in command or "daily status" in command:
        speak("Compiling your system report now.")
        bat, cpu, ram = system_control.get_system_report()
        reminders = reminder.get_pending_reminders()


        city = weather.get_city_from_ip()
        weather_str = "Unavailable"
        if city:
            _, text_report = weather.get_weather(city)
            if text_report:
                weather_str = text_report.split("\n")[2].replace("Temperature: ", "")

        print("\n" + "=" * 40)
        print(" DAILY SYSTEM REPORT")
        print("=" * 40)
        print(f" Battery Usage : {bat}")
        print(f" CPU Usage     : {cpu}%")
        print(f" RAM Usage     : {ram}%")
        print(f" Reminders     : {len(reminders)} pending tasks")
        print(f" Local Weather : {weather_str}")
        print("=" * 40 + "\n")

        speak(
            f"Your system report is ready. CPU is at {cpu} percent, RAM is at {ram} percent, and you have {len(reminders)} pending tasks.")
        return True

    elif "send an email" in command or "email" in command:
        speak("Who is the recipient?")
        raw_recipient = listen_command(phrase_time_limit=15)
        if not raw_recipient:
            speak("I didn't catch that. Canceling.")
            return True

        saved_email = get_contact_from_env(raw_recipient)
        if saved_email:
            recipient = saved_email
            speak(f"Found {raw_recipient} in your contacts.")
        else:
            recipient = email_module.sanitize_spoken_email(raw_recipient)

        if not email_module.is_valid_email(recipient):
            speak(f"The address I heard was {recipient}, which doesn't seem valid. Canceling.")
            return True

        speak("What is the subject?")
        subject = listen_command(phrase_time_limit=15)
        if not subject:
            speak("I didn't hear a subject. Canceling.")
            return True

        speak("What message would you like to send?")
        message = listen_command(phrase_time_limit=30)
        if not message:
            speak("I didn't hear a message. Canceling.")
            return True

        speak(f"Here is your email summary. To: {recipient}. Subject: {subject}. Message: {message}.")
        speak("Do you want me to send it? Say yes to confirm.")

        attempts = 0
        confirmed = False
        while attempts < 3:
            confirmation = listen_command(timeout=5, phrase_time_limit=5)
            if confirmation:
                positive_triggers = ["yes", "yeah", "yep", "sure", "send", "do it", "go ahead", "absolutely"]
                negative_triggers = ["no", "cancel", "stop", "don't", "abort"]
                if any(word in confirmation for word in positive_triggers):
                    confirmed = True
                    break
                elif any(word in confirmation for word in negative_triggers):
                    break
            attempts += 1
            if attempts < 3:
                speak("I didn't quite catch that. Please say yes to send, or no to cancel.")

        if confirmed:
            speak("Sending email now. Please wait.")
            success, response_msg = email_module.send_email(recipient, subject, message)
            speak(response_msg)
        else:
            speak("Email canceled. It has not been sent.")

    elif "hello" in command:
        speak("Hello there! I am ready for your commands.")

    elif "that's all for now" in command or "thats all for now" in command:
        speak("Goodbye. I'll be here when you need me.")
        return False

    elif command.startswith("remind me to"):
        clean_command = command.replace("remind me to", "").strip()
        if " at " in clean_command:
            task, time_str = clean_command.rsplit(" at ", 1)
        elif " in " in clean_command:
            task, time_str = clean_command.rsplit(" in ", 1)
            time_str = "in " + time_str
        elif " tomorrow" in clean_command:
            task = clean_command.replace(" tomorrow", "")
            time_str = "tomorrow"
        else:
            speak("Please specify a time, like 'at 8 PM' or 'in 30 minutes'.")
            return True

        task = invert_pronouns(task.strip())
        success, response = reminder.add_reminder(task.strip(), time_str.strip())
        speak(response)

    elif "show my reminders" in command:
        reminders = reminder.get_pending_reminders()
        if not reminders:
            speak("You have no pending reminders.")
        else:
            speak(f"You have {len(reminders)} reminders.")
            print("\n--- Pending Reminders ---")
            for r_id, task, time_str in reminders:
                if '.' in time_str:
                    dt_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
                else:
                    dt_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                formatted_time = dt_obj.strftime("%b %d at %I:%M %p")
                print(f"ID {r_id}: {task.title()} ({formatted_time})")
            print("-------------------------\n")
            speak(
                "I have displayed them in the terminal. Say 'delete reminder' followed by the ID number to remove one.")

    elif command.startswith("set an alarm for"):
        time_str = command.replace("set an alarm for", "").strip()
        success, response = reminder.add_reminder("Alarm", time_str)
        speak(response)

    elif "delete reminder" in command:
        try:
            r_id = int(command.replace("delete reminder", "").strip())
            success = reminder.delete_reminder(r_id)
            if success:
                speak(f"Reminder {r_id} has been deleted.")
            else:
                speak(f"I couldn't find a reminder with ID {r_id}.")
        except ValueError:
            speak("Please specify the exact reminder ID number you wish to delete.")

    elif any(command.startswith(trigger) for trigger in
             ["ask vector", "explain", "what is", "who is", "how does", "tell me about", "write"]):
        speak("Processing your request...")
        short_summary, full_answer = chat_ai.ask_vector(command)
        print("\n" + "=" * 50)
        print(" VECTOR AI")
        print("=" * 50)
        print(full_answer)
        print("=" * 50 + "\n")
        speak(short_summary)

    elif command.startswith("my name is"):
        name = command.replace("my name is", "").strip().title()
        memory.update_profile_value("name", name)
        speak(f"Got it. I will remember that your name is {name}.")

    elif "cybersecurity student" in command or "cse student" in command:
        memory.update_profile_value("profession", "Cybersecurity Student")
        speak("Profile updated. I've noted down your profession.")

    elif command.startswith("remember that i like"):
        interest = command.replace("remember that i like", "").strip()
        memory.update_profile_value("interests", interest)
        speak(f"Added {interest} to your interests list.")

    elif "favorite language is" in command:
        lang = command.split("favorite language is")[-1].strip().title()
        memory.update_profile_value("favorite_language", lang)
        speak(f"Updated your profile. Your favorite language is set to {lang}.")

    elif "what do you know about me" in command or "who am i" in command:
        summary = memory.get_all_memory_summary()
        print("\n" + "=" * 40)
        print(" USER PROFILE MEMORY")
        print("=" * 40)
        print(summary)
        print("=" * 40 + "\n")
        user_name = memory.get_profile_value("name")
        if user_name:
            speak(f"I am speaking with {user_name}. I have displayed your full profile in the terminal.")
        else:
            speak("I've pulled up everything I know about you in the terminal.")

    elif command.startswith("forget my"):
        target = command.replace("forget my", "").strip().replace(" ", "_")
        success = memory.delete_profile_key(target)
        if not success:
            success = memory.delete_profile_key(f"{target}s")

        if success:
            speak("Done. I have cleared that information from my database.")
        else:
            speak("I couldn't find a matching record to delete.")

    elif command.startswith("list plugins"):
        loaded = plugin_manager.get_plugin_list()
        if loaded:
            speak(f"I have {len(loaded)} plugins active: {', '.join(loaded)}.")
        else:
            speak("I do not have any external plugins loaded right now.")
        return True

    elif command.startswith("reload plugins"):
        count = plugin_manager.load_plugins()
        speak(f"Successfully reloaded {count} modules into my system.")
        return True

    elif command.startswith("disable plugin"):
        target = command.replace("disable plugin", "").strip()
        if plugin_manager.toggle_plugin(target, enable=False):
            speak(f"The {target} module has been disabled.")
        else:
            speak(f"I could not find a plugin named {target}.")
        return True

    elif command.startswith("enable plugin"):
        target = command.replace("enable plugin", "").strip()
        if plugin_manager.toggle_plugin(target, enable=True):
            speak(f"The {target} module is now online.")
        else:
            speak(f"I could not find a plugin named {target}.")
        return True

    elif plugin_manager.handle_command(command, speak):
        return True

    else:
        speak("I heard you, but I don't have a module for that command yet.")

    return True


from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
from gui.dashboard import VectorDashboard
import sys
import time


class AIEngineThread(QThread):
    # These signals send data from the background AI back to the main GUI
    log_signal = pyqtSignal(str)
    state_signal = pyqtSignal(str)
    stats_signal = pyqtSignal(float, float, str)
    profile_signal = pyqtSignal(str)

    def run(self):

        global speak

        def gui_speak(text):
            self.state_signal.emit("speaking")
            self.log_signal.emit(f"<b>VECTOR:</b> {text}")
            print(f"{AI_NAME}: {text}")
            audio_file = "temp_audio.mp3"

            async def generate_audio():
                communicate = edge_tts.Communicate(text, voice="en-US-ChristopherNeural", rate="+15%")
                await communicate.save(audio_file)

            asyncio.run(generate_audio())
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            os.remove(audio_file)

        speak = gui_speak

        plugin_manager.load_plugins()
        greet_user()
        self.update_gui_readouts()

        is_running = True
        while is_running:
            self.update_gui_readouts()
            reminder.process_due_reminders(speak)

            self.state_signal.emit("standby")
            detected = wake_word.wait_for_wake_word()

            if detected:
                speak("Yes?")

                self.state_signal.emit("listening")
                command = listen_command()

                if command:
                    self.log_signal.emit(f"<span style='color:#f07178;'><b>USER:</b> {command}</span>")
                    self.state_signal.emit("processing")
                    is_running = execute_command(command)
                else:
                    speak("I didn't hear a command. Returning to standby.")

    def update_gui_readouts(self):

        try:
            bat, cpu, ram = system_control.get_system_report()
            self.stats_signal.emit(cpu, ram, str(bat))
        except Exception:
            pass

        try:
            profile_summary = memory.get_all_memory_summary()
            self.profile_signal.emit(profile_summary)
        except Exception:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VectorDashboard()
    window.show()
    sys.exit(app.exec())
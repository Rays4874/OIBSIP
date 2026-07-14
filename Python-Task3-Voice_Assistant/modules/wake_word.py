import speech_recognition as sr

WAKE_WORDS = ["hey vector", "vector", "hey victor", "victor"]

def wait_for_wake_word():

    recognizer = sr.Recognizer()
    
    recognizer.dynamic_energy_threshold = False
    
    with sr.Microphone() as source:
        print("\n[ Calibrating microphone for background noise... ]")
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        
        calibrated_threshold = recognizer.energy_threshold + 150
        recognizer.energy_threshold = calibrated_threshold
        recognizer.pause_threshold = 0.5
        
        print(f"[ Debug ]: Microphone energy threshold set to {calibrated_threshold:.0f}")
        print("[ Standby - Waiting for 'Hey Vector' ]")
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
                command = recognizer.recognize_google(audio).lower()
                
                if any(word in command for word in WAKE_WORDS):
                    return True
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("[ ERROR ]: Network error. Ensure you have internet for wake-word detection.")
                continue
            except Exception:
                continue
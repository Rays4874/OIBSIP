from modules import weather

PLUGIN_NAME = "Weather"

TRIGGERS = [
    "weather here",
    "temperature here",
    "weather in",
    "temperature in"
]

def execute(command):
    command = command.lower()
    
    if "weather here" in command or "temperature here" in command:
        city = weather.get_city_from_ip()
        if city:
            speech, text_report = weather.get_weather(city)
            if text_report:
                print(f"\n{text_report}\n")
            return f"Detecting your location as {city}. {speech}"
        else:
            return "I couldn't determine your local city. Please specify a city name."
            
    elif "weather in" in command or "temperature in" in command:
        if "weather in" in command:
            city = command.split("weather in")[-1].strip()
        else:
            city = command.split("temperature in")[-1].strip()
            
        speech, text_report = weather.get_weather(city)
        if text_report:
            print(f"\n{text_report}\n")
        return speech
        
    return "I am not sure how to check the weather for that location."

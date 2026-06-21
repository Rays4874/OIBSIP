import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_city_from_ip():
    try:
    
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return data["city"]
    except Exception:
        pass
    return None

def get_weather(city):
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "your_actual_api_key_goes_here":
        return "My weather API key is missing. Please add it to the dot env file.", None

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric" 
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)
        data = response.json()

        if data["cod"] == 200:
            temp = round(data["main"]["temp"])
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            speech_report = f"The current temperature in {city} is {temp} degrees Celsius. The weather is {desc} with {humidity} percent humidity."
            
            text_report = (
                f"\n--- Weather Report: {city.title()} ---\n"
                f"Temperature: {temp}°C\n"
                f"Condition:   {desc.capitalize()}\n"
                f"Humidity:    {humidity}%\n"
                f"Wind Speed:  {wind_speed} m/s\n"
                f"-----------------------------------"
            )
            return speech_report, text_report
            
        elif str(data["cod"]) == "404":
            return f"I couldn't find the city {city}. Please check the name.", None
        else:
            return f"Error retrieving weather data. The server said: {data.get('message')}", None

    except requests.exceptions.ConnectionError:
        return "I cannot check the weather right now because there is no internet connection.", None
    except requests.exceptions.Timeout:
        return "The connection to the weather server timed out.", None
    except Exception as e:
        return "An unexpected error occurred while checking the weather.", None
# 🌤️ Weather Forecast Application

A modern desktop Weather Forecast Application built with Python and Tkinter that provides real-time weather information, hourly forecasts, and multi-day weather predictions through a clean and interactive graphical user interface.

## 📌 Overview

This application allows users to search weather information for any city worldwide or automatically detect their current location. It displays detailed weather data, including current conditions, hourly forecasts, and 7-day forecasts, along with weather icons, alerts, and theme customization.

The project was developed to demonstrate GUI development, API integration, multithreading, error handling, and software design using Python.

---

## ✨ Features

### 🌍 Location Support

* Search weather by city name
* Automatic location detection using IP-based geolocation
* Quick weather retrieval for the detected location

### 🌡️ Current Weather Information

* Current temperature
* Feels-like temperature
* Humidity
* Wind speed
* Weather condition
* Dynamic weather icons

### ⏰ 24-Hour Forecast

* Hourly weather forecast
* Temperature predictions
* Weather condition updates
* Forecast cards with weather icons

### 📅 7-Day Forecast

* Daily weather predictions
* Minimum and maximum temperatures
* Weather conditions for each day
* Easy-to-read forecast cards

### 🎨 User Interface

* Modern Tkinter GUI
* Dark Theme
* Light Theme
* Responsive layout
* Weather icons and visual indicators

### ⚠️ Weather Alerts

* Severe weather warnings
* High temperature alerts
* Heavy rain alerts
* Storm notifications

### 🔒 Security

* API key protection using `.env`
* Sensitive data excluded from GitHub using `.gitignore`

### ⚡ Performance

* Multithreading for API requests
* Non-blocking user interface
* Smooth weather updates

---

## 🛠️ Technologies Used

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| Python             | Core Programming Language       |
| Tkinter            | GUI Development                 |
| Requests           | API Communication               |
| Pillow (PIL)       | Image Processing                |
| OpenWeatherMap API | Weather Data                    |
| dotenv             | Environment Variable Management |
| Threading          | Background API Requests         |

---

## 📂 Project Structure

```text
Weather_app/
│
├── icons/
│   ├── clear.png
│   ├── clouds.png
│   ├── rain.png
│   ├── storm.png
│   └── ...
│
├── main.py
├── .env
├── .gitignore
├── README.md
└── screenshots/
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Rays4874/OIBSIP.git
```

### 2. Navigate to the Project Folder

```bash
cd OIBSIP/Weather_app
```

### 3. Install Dependencies

```bash
pip install requests pillow python-dotenv
```

---

## 🔑 API Configuration

### Create a `.env` File

Create a file named:

```text
.env
```

Add your OpenWeatherMap API key:

```env
OPENWEATHER_API_KEY=YOUR_API_KEY_HERE
```

### Get an API Key

1. Create an account on OpenWeatherMap.
2. Generate a free API key.
3. Add the key to the `.env` file.

---

## ▶️ Running the Application

```bash
python main.py
```

---

## 📸 Screenshots

### Dark Theme

*Add screenshot here*

### Light Theme

*Add screenshot here*

### Weather Forecast View

*Add screenshot here*

---

## ⚙️ Key Functionalities

### Search Weather

Users can search weather information by entering a city name.

### Current Location Detection

Automatically detects the user's city and retrieves weather information.

### Forecast Generation

Displays:

* Current Weather
* Hourly Forecast
* 7-Day Forecast

### Weather Alerts

Shows warning messages based on weather conditions.

### Theme Switching

Allows users to switch between:

* 🌙 Dark Mode
* ☀️ Light Mode

---

## 🧠 Concepts Demonstrated

* Object-Oriented Programming
* API Integration
* Environment Variables
* GUI Design
* Error Handling
* Multithreading
* JSON Data Processing
* User Experience Design
* Git & GitHub Workflow

---

## 🔮 Future Improvements

* Temperature trend charts
* Export weather reports to PDF
* Search history
* Favorites locations
* GPS-based location support
* Weather radar integration
* Multiple language support

---

## 👨‍💻 Author

**Chayan Das**

GitHub: https://github.com/Rays4874

---

## 📄 License

This project is intended for educational, internship, and portfolio purposes.

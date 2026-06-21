# 🎙️ Vector AI - Intelligent Voice Assistant

Vector AI is an advanced Python-based voice assistant designed to provide a natural and intelligent user experience through voice interaction, AI-powered conversations, task automation, and system management.

Unlike traditional command-based assistants, Vector AI combines speech recognition, text-to-speech synthesis, local Large Language Models (LLMs), persistent memory, reminders, weather services, email automation, and a plugin architecture to create a personalized AI assistant.

---

# ✨ Features

## 🎤 Voice Recognition

* Real-time voice command recognition
* Speech-to-text using Google Speech Recognition
* Ambient noise adjustment
* Continuous listening mode

## 🔊 Natural Voice Responses

* High-quality neural voices using Edge TTS
* Natural and human-like responses
* Dynamic speech generation

## 🤖 AI Chat Mode

Powered by Ollama Local LLMs.

Supported Models:

* Llama 3.2
* Llama 3.1
* Qwen
* Other Ollama-compatible models

Capabilities:

* Answer questions
* Explain concepts
* Programming assistance
* Study support
* General conversations

Example:

User:

> What is a binary number?

Vector:

> A binary number is a number represented using only 0 and 1.

---

## 🌦️ Weather Assistant

Get real-time weather information.

Commands:

* Weather in Delhi
* Temperature in Kolkata
* Weather here

Provides:

* Temperature
* Weather conditions
* Humidity
* Wind speed

---

## 📧 Email Assistant

Send emails entirely through voice commands.

Features:

* Voice-based recipient selection
* Subject dictation
* Message dictation
* Confirmation before sending
* Contact management

Example:

User:

> Send an email

Vector:

> Who is the recipient?

---

## ⏰ Reminder & Alarm System

Create reminders using natural language.

Examples:

* Remind me to study at 8 PM
* Remind me to drink water in 30 minutes
* Set an alarm for 6 AM

Features:

* SQLite storage
* Background reminder checking
* Voice notifications
* Reminder management

---

## 🧠 Persistent Memory System

Vector AI remembers information across sessions.

Examples:

User:

> Remember that I like Python

User:

> What do you know about me?

Vector:

> You are interested in Python.

Features:

* User preferences
* Personal information
* Persistent storage
* Memory updates
* Memory deletion

---

## 💻 System Control Hub

Monitor and manage system resources.

Commands:

* Battery percentage
* CPU usage
* RAM usage
* System report

Provides:

* Battery status
* CPU utilization
* Memory usage
* System information

---

## 🔌 Plugin Architecture

Vector AI supports dynamic plugin loading.

Features:

* Automatic plugin discovery
* Plugin management
* Dynamic module loading
* Extensible functionality

Benefits:

* Easy feature expansion
* Modular architecture
* Clean code structure

---

# 🏗️ Project Architecture

Voice_assitant/
├── main.py
├── modules/
│ ├── chat_ai.py
│ ├── weather.py
│ ├── email_module.py
│ ├── reminder.py
│ ├── memory.py
│ └── plugin_manager.py
│
├── plugins/
│ ├── calculator_plugin.py
│ ├── joke_plugin.py
│ └── custom_plugins.py
│
├── memory/
│ ├── conversation.json
│ └── user_memory.json
│
├── database/
│ └── reminders.db
│
├── requirements.txt
└── README.md

---

# 🛠️ Technologies Used

## Programming Language

* Python 3.12+

## AI & Machine Learning

* Ollama
* Llama 3.2
* Local LLM Integration

## Speech Processing

* SpeechRecognition
* Edge TTS
* PyAudio

## APIs

* OpenWeather API
* Gmail SMTP

## Database

* SQLite3
* JSON Storage

## System Utilities

* psutil
* subprocess
* webbrowser

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/Rays4874/OIBSIP.git

cd Voice_assstant
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Install Ollama

Download:

https://ollama.com

Pull model:

```bash
ollama pull llama3.2
```

Verify:

```bash
ollama run llama3.2
```

## 5. Configure Environment Variables

Create a `.env` file:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

OPENWEATHER_API_KEY=your_api_key
```

---

# 🚀 Running Vector AI

Start Ollama:

```bash
ollama serve
```

Run Vector AI:

```bash
python main.py
```

---

# 🎯 Example Commands

## General

* Hello
* What is the time?
* Open Google
* Open YouTube

## Weather

* Weather in Delhi
* Temperature in Mumbai

## AI Chat

* What is SQL Injection?
* Explain Queue Data Structure
* Write a Python Password Generator

## Email

* Send an email

## Reminders

* Remind me to study at 8 PM
* Show my reminders

## Memory

* Remember that I like Python
* What do you know about me?

## System

* Show battery percentage
* Give me a system report

---

# 🔒 Security Features

* Environment variables for credentials
* Local AI processing through Ollama
* No cloud dependency for AI conversations
* Secure email authentication
* Modular architecture for future security enhancements

---

# 📈 Future Improvements

* GUI Dashboard (PyQt6)
* Wake Word Detection ("Hey Vector")
* Multi-language Support
* Mobile Companion App
* Advanced Scheduling
* Voice Authentication
* Smart Home Integration
* Calendar Integration

---

# 👨‍💻 Developer

**Chayan Das**

B.Tech CSE (Cybersecurity)

SRM University Delhi-NCR

---

# 📜 License

This project is intended for educational and personal learning purposes.

Feel free to fork, modify, and improve the project.

---

# ⭐ If You Like This Project

Consider starring the repository and sharing feedback.
# 🔐 Advanced Password Generator

A professional desktop application built with **Python** and **Tkinter** that generates secure, customizable passwords using modern security practices. The application provides password strength analysis, entropy estimation, password history management, clipboard integration, and configurable security policies through an intuitive graphical user interface.

---

## 📌 Overview

The Advanced Password Generator helps users create strong and secure passwords while providing detailed security feedback. Unlike basic password generators, this application includes:

* Password strength analysis
* Entropy estimation
* Security policy presets
* Password history tracking
* Clipboard integration
* User preference persistence
* Advanced security controls

The project demonstrates Python GUI development, modular software architecture, file handling, security concepts, and user experience design.

---

## ✨ Features

### Password Generation

* Generate secure random passwords
* Adjustable password length (8–128 characters)
* Cryptographically secure randomness
* Multiple character set support

### Character Types

* Uppercase Letters (A–Z)
* Lowercase Letters (a–z)
* Numbers (0–9)
* Symbols and Special Characters

### Advanced Security Rules

* Exclude ambiguous characters (`0`, `O`, `I`, `l`, `1`)
* Prevent repeated characters
* Guaranteed inclusion of selected character types
* Validation for invalid configurations

### Password Strength Analysis

* Weak
* Medium
* Strong
* Very Strong

Includes:

* Strength score calculation
* Visual strength meter
* Color-coded feedback

### Entropy Estimation

Calculates password entropy using:

Entropy = Length × log₂(Character Pool Size)

Provides an estimate of password unpredictability in bits.

### Security Policy Presets

#### Standard

* Uppercase
* Lowercase
* Numbers
* Minimum length: 8

#### Strong

* Uppercase
* Lowercase
* Numbers
* Symbols
* Minimum length: 12

#### Enterprise

* Uppercase
* Lowercase
* Numbers
* Symbols
* Prevent repeated characters
* Minimum length: 16

### Clipboard Integration

* One-click password copying
* Instant clipboard access

### Password History

* Stores recent generated passwords
* Displays history in a dedicated panel
* Prevents duplicate consecutive entries
* Supports history export

### User Preferences

Automatically saves:

* Password length
* Character type selections
* Security options
* Selected policy

Preferences are restored when the application is reopened.

### About Dialog

Includes application information, version details, and feature summary.

---

## 🏗 Project Structure

```text
AdvancedPasswordGenerator/
│
├── main.py
├── ui.py
├── generator.py
├── security.py
├── storage.py
├── settings.json
│
├── assets/
│   ├── icon.png
│   └── password.png
│
└── README.md
```

### File Descriptions

#### main.py

Application entry point.

#### ui.py

Handles:

* GUI layout
* User interactions
* Event handling
* Password history display

#### generator.py

Handles:

* Password generation
* Character pool construction
* Security option processing

#### security.py

Handles:

* Strength calculation
* Entropy calculation
* Security metrics

#### storage.py

Handles:

* Settings persistence
* History export
* Configuration management

---

## 🛠 Technologies Used

* Python 3.13.7
* Tkinter
* JSON
* OS Module
* Math Module
* Secrets Module

---

## 🚀 Installation

### Clone the Repository

```bash
https://github.com/Rays4874/OIBSIP.git
```

### Install Dependencies

This project primarily uses Python standard libraries.

If a requirements file exists:

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

---

## 💻 Building an Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed --add-data "assets;assets" main.py
```

The executable will be created inside:

```text
dist/
└── main.exe
```

---

## 📷 Screenshots

### Main Application Window
<img width="1067" height="857" alt="Screenshot 2026-06-16 181635" src="https://github.com/user-attachments/assets/ad9cdf4b-fadc-42de-8b7e-682c295fc901" />


### Password Strength Analysis
<img width="736" height="162" alt="Screenshot 2026-06-16 193823" src="https://github.com/user-attachments/assets/45a2d9c3-07a6-4bf0-a361-9e451138ad8f" />


### Password History Panel
<img width="268" height="748" alt="image" src="https://github.com/user-attachments/assets/020bc418-a499-4233-8923-21a39fc4d64d" />


## 🔒 Security Features

* Cryptographically secure password generation
* Entropy estimation
* Strength classification
* Character type enforcement
* Password policy presets
* Prevention of weak configurations

---

## 📈 Future Enhancements

* Dark/Light theme switching
* Password generation statistics
* Password expiration reminders
* Encrypted password vault
* Password breach checking
* Multi-language support
* QR code export
* Cloud synchronization

---

## 🎯 Learning Outcomes

This project demonstrates:

* Python Programming
* GUI Development with Tkinter
* Object-Oriented Programming
* Modular Software Design
* File Handling
* JSON Data Persistence
* Security Principles
* User Interface Design
* Application Packaging with PyInstaller

---

## 👨‍💻 Author

Developed as a Python Desktop Application Project.

Version: 1.0.0

---

📄 License
This project is intended for educational and portfolio purposes.
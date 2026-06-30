import smtplib
import sqlite3
import os
import datetime
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def init_db():

    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/emails.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT,
            subject TEXT,
            message TEXT,
            sent_time TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def sanitize_spoken_email(spoken_text):

    text = spoken_text.lower().strip()

    replacements = {
        " at the rate ": "@",
        " at ": "@",
        " dot ": ".",
        " point ": ".",
        " underscore ": "_",
        " dash ": "-",
        " hyphen ": "-"
    }
    
    for spoken, symbol in replacements.items():
        text = text.replace(spoken, symbol)

    text = text.replace("dotcom", ".com")
    text = text.replace("gmailcom", "gmail.com")

    text = text.replace(" ", "")
    
    return text

def is_valid_email(email_address):
    try:

        validate_email(email_address)
        return True
    except EmailNotValidError:
        return False

def log_email(recipient, subject, message):
    conn = sqlite3.connect("database/emails.db")
    cursor = conn.cursor()
    sent_time = datetime.datetime.now()
    
    cursor.execute('''
        INSERT INTO sent_emails (recipient, subject, message, sent_time)
        VALUES (?, ?, ?, ?)
    ''', (recipient, subject, message, sent_time))
    
    conn.commit()
    conn.close()

def send_email(recipient, subject, message):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return False, "Email credentials are missing in the dot env file."

    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        log_email(recipient, subject, message)
        return True, "Email sent successfully."
        
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Please check your app password."
    except Exception as e:
        return False, f"Failed to send email. Error: {str(e)}"

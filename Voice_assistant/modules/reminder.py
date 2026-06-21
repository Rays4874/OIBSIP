import sqlite3
import dateparser
import datetime
import os
from plyer import notification
from playsound import playsound

def init_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/reminders.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            reminder_time DATETIME NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def add_reminder(task, time_string):
    parsed_time = dateparser.parse(time_string, settings={'PREFER_DATES_FROM': 'future'})
    
    if not parsed_time:
        return False, "I couldn't understand the time format."
    
    if parsed_time < datetime.datetime.now():
        return False, "That time is in the past! Please choose a future time."

    conn = sqlite3.connect("database/reminders.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reminders (task, reminder_time) VALUES (?, ?)', (task, parsed_time))
    conn.commit()
    conn.close()
    
    friendly_time = parsed_time.strftime("%A at %I:%M %p")
    return True, f"Reminder set for {friendly_time}: {task}"

def get_pending_reminders():
    conn = sqlite3.connect("database/reminders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, reminder_time FROM reminders WHERE status = 'pending' ORDER BY reminder_time ASC")
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def delete_reminder(reminder_id):
    conn = sqlite3.connect("database/reminders.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

def mark_completed(reminder_id):
    conn = sqlite3.connect("database/reminders.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE reminders SET status = 'completed' WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()


def process_due_reminders(speak_callback):
    now = datetime.datetime.now()
    reminders = get_pending_reminders()
    
    for r_id, task, time_str in reminders:
        try:

            if '.' in time_str:
                reminder_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
            else:
                reminder_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        
        if now >= reminder_time:

            notification.notify(title="Vector AI Reminder", message=task, app_name="Vector AI", timeout=10)
            print(f"\n[ ALARM TRIGGERED ]: {task}")
            
            try:
                playsound("alarm.mp3")
            except Exception:
                pass
            
            speak_callback(f"Reminder alert! It is time to {task}.")
            mark_completed(r_id)
import json
import os
import datetime

MEMORY_FILE = "memory/user_memory.json"

def init_memory():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({}, f)

init_memory()

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def update_profile_value(key, value):
   
    memory = load_memory()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    list_keys = ["interests", "favorite_websites", "frequent_contacts", "favorite_language"]

    if any(lk in key for lk in [list_keys[0], list_keys[1], list_keys[2]]):
        if key not in memory or not isinstance(memory[key].get("value"), list):
            memory[key] = {"value": [], "updated_at": timestamp}
        if value not in memory[key]["value"]:
            memory[key]["value"].append(value)
            memory[key]["updated_at"] = timestamp
    else:
        memory[key] = {
            "value": value,
            "updated_at": timestamp
        }
        
    save_memory(memory)
    return True

def get_profile_value(key):
    memory = load_memory()
    if key in memory:
        return memory[key]["value"]
    return None

def get_all_memory_summary():
    memory = load_memory()
    if not memory:
        return "I don't know anything about you yet!"
        
    summary_lines = []
    for key, data in memory.items():
        clean_key = key.replace("_", " ").title()
        val = data["value"]
        if isinstance(val, list):
            val = ", ".join(val)
        summary_lines.append(f"{clean_key}: {val}")
        
    return "\n".join(summary_lines)

def delete_profile_key(key):
    memory = load_memory()
    if key in memory:
        del memory[key]
        save_memory(memory)
        return True
    return False
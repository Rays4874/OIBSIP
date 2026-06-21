import requests
import json
import os
import time

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

MEMORY_FILE = "memory/conversation.json"
MAX_HISTORY = 6  


def init_memory():
    os.makedirs("memory", exist_ok=True)

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


init_memory()


def load_history():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    history = history[-MAX_HISTORY:]

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def ask_vector(user_prompt):

    history = load_history()

    system_instruction = {
        "role": "system",
        "content": """
You are Vector AI.

Rules:
- Give detailed answers.
- Explain concepts clearly.
- Use examples when useful.
- Keep spoken summaries short.
- Never answer with only 1 or 2 words unless explicitly requested.
"""
    }

    messages = [system_instruction]
    messages.extend(history)
    messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 300,
            "num_ctx": 4096
        }
    }

    try:

        print("\n[VECTOR DEBUG]")
        print(f"Sending prompt: {user_prompt}")

        start_time = time.time()

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        elapsed = time.time() - start_time

        print(f"Response received in {elapsed:.2f} seconds")

        response.raise_for_status()

        data = response.json()

        ai_response = data["message"]["content"].strip()

        if not ai_response:
            return (
                "I did not receive a valid response.",
                "Error: Empty response from Ollama."
            )

        history.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )

        save_history(history)

        sentences = ai_response.split(".")

        spoken_summary = sentences[0].strip()

        if len(spoken_summary) < 15:
            spoken_summary = ai_response[:200]

        return spoken_summary, ai_response

    except requests.exceptions.Timeout:
        return (
            "The model took too long to respond.",
            "ERROR: Request timed out after 180 seconds."
        )

    except requests.exceptions.ConnectionError:
        return (
            "My neural network is offline.",
            "ERROR: Could not connect to Ollama."
        )

    except Exception as e:
        return (
            "I encountered an error.",
            f"ERROR: {str(e)}"
        )
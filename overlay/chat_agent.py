# ~/Soap/chat_agent.py

"""
Chat Agent - Oracle AI SOP Interface
Receives natural language from UI and returns AI-generated response.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

QUEUE_DIR = Path.home() / "Soap" / "agent_queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

CHAT_LOG = QUEUE_DIR / "oracle_chat_log.txt"

def log_message(role, message):
    with open(CHAT_LOG, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().isoformat()}] {role.upper()}: {message}\n")

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No message provided"}))
        return

    message = sys.argv[1].strip()
    if not message:
        print(json.dumps({"error": "Empty input"}))
        return

    # Log the user input
    log_message("user", message)

    # Simulated AI response (replace with real LLM or API call)
    reply = f"🧠 Oracle received: '{message}' — SOP synthesis AI is operational."

    # Log the response
    log_message("oracle", reply)

    # Output structured response
    print(json.dumps({ "reply": reply }))

if __name__ == "__main__":
    main()

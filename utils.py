import json
from datetime import datetime

def validate_email(email):
    return "@" in email and "." in email.split("@")[1]

def validate_phone(phone):
    return sum(c.isdigit() for c in phone) >= 8

def save_conversation(conversation):
    try:
        with open("conversation_log.json", "a") as f:
            log_entry = {
                "timestamp": str(datetime.now()),
                "conversation": conversation
            }
            json.dump(log_entry, f)
            f.write("\n")
    except Exception as e:
        print(f"Error saving conversation: {e}")
import csv
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "events.csv")

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def log_event(event: dict):
    os.makedirs(LOG_DIR, exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(event.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(event)

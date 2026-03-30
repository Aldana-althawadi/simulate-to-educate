import csv
import os
from datetime import datetime

LOG_FILE = "logs/game_log.csv"


def log_game_event(player, target, case_id, status, message, level="", flag=""):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "player",
                "target",
                "case_id",
                "level",
                "status",
                "flag",
                "message"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            player,
            target,
            case_id,
            level,
            "SUCCESS" if status else "FAILED",
            flag if status else "",
            message.replace("\n", " ").strip()
        ])
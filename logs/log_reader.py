import csv
import os

LOG_FILE = "logs/game_log.csv"


def read_game_logs():
    if not os.path.isfile(LOG_FILE):
        return []

    rows = []
    with open(LOG_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    return rows
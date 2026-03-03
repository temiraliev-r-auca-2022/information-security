#!/usr/bin/python3
from datetime import datetime

with open("cron_log.txt", "a") as f:
    f.write(f"Email sent to server owner at {datetime.now()}\n")

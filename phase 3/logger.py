from datetime import datetime


def log(event: str, data: str):
    print(f"[{datetime.utcnow().isoformat()}] {event}\n{data}\n")

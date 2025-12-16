from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def log_event(event_type: str, content: str):
    timestamp = datetime.utcnow().isoformat()
    filename = LOG_DIR / f"{event_type}.log"

    with filename.open("a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}]\n")
        f.write(content)
        f.write("\n" + "-" * 80 + "\n")

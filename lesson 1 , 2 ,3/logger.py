from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def log_event(name: str, content: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S-%f")
    file = LOG_DIR / f"{timestamp}_{name}.txt"
    file.write_text(str(content), encoding="utf-8")

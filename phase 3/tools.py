from pathlib import Path


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_file(data: str) -> str:
    path, content = data.split("::", 1)
    Path(path).write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} chars"


TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
}


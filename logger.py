import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(os.getenv("LOG_DIRECTORY"))

def current_date_as_str() -> str:
  return datetime.today().strftime('%Y-%m-%d')

def log(line: str) -> None:
  with open(BASE_DIR / f"{current_date_as_str()}.log", "a") as f:
    f.write(line)
    f.write("\n")
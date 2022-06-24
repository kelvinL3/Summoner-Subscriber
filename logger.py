import os
from datetime import datetime
import pytz
from pathlib import Path

BASE_DIR = Path(os.getenv("LOG_DIRECTORY"))


def current_date_as_str() -> str:
    return datetime.today().strftime("%Y-%m-%d")


def log(line: str, withTimeStamp: bool = True) -> None:
    with open(BASE_DIR / f"{current_date_as_str()}.log", "a") as f:
        if withTimeStamp:
            f.write(str(datetime.now(pytz.utc)))
        f.write(line)
        f.write("\n")

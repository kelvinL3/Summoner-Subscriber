import mysql.connector
from datetime import datetime
import os
from typing import Optional

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

assert MYSQL_HOST
assert MYSQL_USERNAME
assert MYSQL_PASSWORD
assert MYSQL_DATABASE

db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
)


def last_game(summoner: str) -> Optional[str]:
    db.ping(reconnect=True)
    cursor = db.cursor()
    query = (
        "SELECT match_id FROM games "
        "WHERE summoner = %s "
        "ORDER BY datetime DESC "
        "LIMIT 1"
    )
    cursor.execute(query, (summoner,))

    for (match_id,) in cursor:
        return match_id

    cursor.close()
    # No game found
    return None


def add_game(
    match_id: str,
    summoner: str,
    win: bool,
    champion: str,
    dt: datetime,
) -> None:
    db.ping(reconnect=True)
    cursor = db.cursor()
    query = (
        "INSERT INTO games "
        "(match_id, summoner, win, champion, datetime) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    cursor.execute(query, (match_id, summoner, win, champion, dt))
    db.commit()
    cursor.close()

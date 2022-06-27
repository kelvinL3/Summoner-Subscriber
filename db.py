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


def last_recorded_match_id(summoner: str) -> Optional[str]:
    db.ping(reconnect=True)
    cursor = db.cursor()
    query = (
        "SELECT match_id FROM games "
        "WHERE summoner = %s "
        "ORDER BY datetime DESC "
        "LIMIT 1"
    )
    cursor.execute(query, (summoner,))

    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


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

def update_discord_name(
    discord_handle: str,
    discord_name: str,
    name_override: Optional[str],
) -> None:
    db.ping(reconnect=True)
    cursor = db.cursor()
    query = (
        "INSERT INTO discord_name_info "
        "(discord_handle, discord_name, name_override) "
        "VALUES (%s, %s, %s) ON DUPLICATE KEY "
        "UPDATE discord_name = %s, name_override = %s"
    )
    cursor.execute(query, (discord_handle, discord_name, name_override, discord_name, name_override))
    db.commit()
    cursor.close()

def get_discord_names(discord_handle: str):
    db.ping(reconnect=True)
    cursor = db.cursor()
    query = (
        "SELECT discord_name, name_override FROM discord_name_info "
        "WHERE discord_handle = %s "
        "LIMIT 1"
    )
    cursor.execute(query, (discord_handle,))

    row = cursor.fetchone()
    cursor.close()
    return row

def delete_discord_names(discord_handle: str):
    db.ping(reconnect=True)
    cursor = db.cursor()
    query = (
        "DELETE FROM discord_name_info "
        "WHERE discord_handle = %s "
    )
    cursor.execute(query, (discord_handle,))
    db.commit()
    cursor.close()

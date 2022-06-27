#!/usr/bin/env python3
from riot import api as riot
import logger
from discord_api import api as discord
import asyncio
import db

ANKUR_NAME = "the kid#7020"
victim = "anchor1"
COOLDOWN = 60


async def run_loop() -> None:
    riot.clear_cache()
    ankur = riot.get_summoner(victim)
    riot.pull_latest_matches(ankur)
    current_match = riot.get_current_match(ankur)
    rank = riot.get_solo_queue_rank(ankur.ranks)
    logger.log(f"Ankur's current rank is {rank[0]} {rank[1]}")
    if current_match:
        logger.log("Ankur is currently in game")
        ankur_participant = riot.find_participant_in_match(current_match, ankur)
        logger.log(f"Ankur is playing {ankur_participant.champion.name}")
        await discord.change_name(ANKUR_NAME, ankur_participant.champion.name, rank[0], rank[1])
    else:
        logger.log("Ankur is currently not in game")
        await discord.revert_name(ANKUR_NAME)
    logger.log("Done")
    logger.log("===========")


if __name__ == "__main__":
    try:
        discord.connect(run_loop, COOLDOWN)
    except:
        db.db.close()
        raise

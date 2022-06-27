#!/usr/bin/env python3

# https://towardsdatascience.com/how-to-use-riot-api-with-python-b93be82dbbd6
# https://cassiopeia.readthedocs.io/en/latest/

import cassiopeia as cass
from datapipelines import NotFoundError
import os
from typing import Optional
import logger
import db
from collections import namedtuple

DEFAULT_REGION = "NA"

cass.set_riot_api_key(os.getenv("RIOT_API_KEY"))

TOKEN = os.getenv("RIOT_API_KEY")
if not TOKEN:
    raise Exception("RIOT_API_KEY missing from env vars")

cass.set_riot_api_key(TOKEN)

def clear_cache():
    cass.configuration.settings.pipeline._cache.clear(cass.Summoner)

def get_summoner(name: str, region: str = DEFAULT_REGION) -> cass.Summoner:
    return cass.Summoner(name=name, region=region)


def get_current_match(summoner: cass.Summoner) -> Optional[cass.CurrentMatch]:
    try:
        return summoner.current_match
    except NotFoundError as e:
        return None


def find_participant_in_match(
    match: cass.CurrentMatch, summoner: cass.Summoner
) -> "cass.Participant":
    return next(p for p in match.participants if p.summoner.name == summoner.name)


def pull_latest_matches(summoner: cass.Summoner, limit: int = 20) -> None:
    latest_match_id = db.last_recorded_match_id(summoner.name)
    match_history = summoner.match_history
    for match in match_history:
        if limit == 0:
            break
        limit -= 1

        match_id = match.id
        if match_id == latest_match_id:
            logger.log(f"Match {match_id} already in db. Stopping...")
            break

        participant = find_participant_in_match(match, summoner)
        summoner_name = summoner.name
        win = participant.stats.win
        champion_name = participant.champion.name
        dt = match.creation.datetime
        logger.log(
            f"Adding match {match_id}. {summoner_name} played {champion_name} at {dt}. Win: {win}"
        )
        db.add_game(
            match_id=match_id,
            summoner=summoner_name,
            win=win,
            champion=champion_name,
            dt=dt,
        )


def get_solo_queue_rank(ranks: cass.Rank) -> str:
    for rank, value in ranks.items():
        if rank.name == "ranked_solo_fives":
            return (value.tier, value.division)


def get_flex_queue_rank(ranks: cass.Rank) -> str:
    for rank, value in ranks.items():
        if rank.name == "ranked_flex_fives":
            return (value.tier, value.division)

def get_solo_ranked_stats(summoner: cass.Summoner):
    return next(league_entry for league_entry in summoner.league_entries if league_entry.queue.name == "ranked_solo_fives")

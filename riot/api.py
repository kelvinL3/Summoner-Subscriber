#!/usr/bin/env python3

# https://towardsdatascience.com/how-to-use-riot-api-with-python-b93be82dbbd6
# https://cassiopeia.readthedocs.io/en/latest/

import cassiopeia as cass
from datapipelines import NotFoundError
import os
from typing import Optional

DEFAULT_REGION = "NA"

cass.set_riot_api_key(os.getenv("RIOT_API_KEY"))

TOKEN = os.getenv("RIOT_API_KEY")
if not TOKEN:
    raise Exception("RIOT_API_KEY missing from env vars")

cass.set_riot_api_key(TOKEN)


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


def pull_latest_matches(summoner: cass.Summoner) -> None:
    # use summoner.match_history
    # 1 - get latest match not stored in DB
    # 2 - scan all matches from past week up until latest_match
    # 3 - store match id, datetime, summoner, outcome, champion into db
    #     participant.stats.win
    #     participant.champion.name
    pass


def get_solo_queue_rank(ranks: cass.Rank) -> str:
    for rank, value in ranks.items():
        if rank.name == "ranked_solo_fives":
            return (value.tier, value.division)


def get_flex_queue_rank(ranks: cass.Rank) -> str:
    for rank, value in ranks.items():
        if rank.name == "ranked_flex_fives":
            return (value.tier, value.division)

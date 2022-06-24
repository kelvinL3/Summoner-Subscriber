#!/usr/bin/env python3

# https://towardsdatascience.com/how-to-use-riot-api-with-python-b93be82dbbd6
# https://cassiopeia.readthedocs.io/en/latest/

import cassiopeia as cass
from datapipelines import NotFoundError
import os
from typing import Optional

DEFAULT_REGION = 'NA'

cass.set_riot_api_key(os.getenv('RIOT_API_KEY'))

def get_summoner(name: str, region: str = DEFAULT_REGION):
    return cass.Summoner(name=name, region=region)

def get_current_match(summoner: cass.Summoner) -> Optional[cass.CurrentMatch]:
    try:
        return summoner.current_match
    except NotFoundError as e:
        return None

def find_participant_in_match(match: cass.CurrentMatch, summoner: cass.Summoner) -> "cass.Participant":
  participants = list(filter(lambda p: p.summoner.name == summoner.name, match.participants))
  assert len(participants) == 1, f"There are {len(participants)} people named {summoner.name} in this match."
  return participants[0]

def get_solo_queue_rank(ranks: cass.Rank) -> str:
    for rank, value in ranks.items():
        if rank.name == 'ranked_solo_fives':
            return (value.tier, value.division)

def get_flex_queue_rank(ranks: cass.Rank) -> str:
    for rank, value in ranks.items():
        if rank.name == 'ranked_flex_fives':
            return (value.tier, value.division)

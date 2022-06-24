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

def get_current_match_details(summoner: cass.Summoner) -> Optional[cass.CurrentMatch]:
    try:
        return summoner.current_match
    except NotFoundError as e:
        return None

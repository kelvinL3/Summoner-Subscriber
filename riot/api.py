#!/usr/bin/env python3

# https://towardsdatascience.com/how-to-use-riot-api-with-python-b93be82dbbd6
# https://cassiopeia.readthedocs.io/en/latest/

# from cassiopeia import Summoner
import cassiopeia as cass
from .secrets import API_KEY, API_KEY2

ANKUR = 'anchor1'
ANKUR_ALT = 'anchor2'

REGION = 'NA'

# def get_player()
# pass

cass.set_riot_api_key(API_KEY)

anchor = cass.Summoner(name=ANKUR, region=REGION)
# kalturi.match_history

#!/usr/bin/env python3

# https://towardsdatascience.com/how-to-use-riot-api-with-python-b93be82dbbd6
# https://cassiopeia.readthedocs.io/en/latest/

# from cassiopeia import Summoner
import cassiopeia as cass
from datapipelines import NotFoundError
from setuptools import setup
import os

ANKUR = 'anchor1'
ANKUR_ALT = 'anchor2'

REGION = 'NA1'

cass.set_riot_api_key(os.getenv('RIOT_API_KEY'))

def setup_summoner():
    return cass.Summoner(name=ANKUR, region=REGION)

def get_current_match_details(anchor):
    try:
        anchor.current_match
    except NotFoundError as e:
        print("Anchor not in match", e)
    except Exception as e:
        raise e
    
    return anchor.current_match

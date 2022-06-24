#!/usr/bin/env python3
from riot import api as riot

if __name__ == "__main__":
	ankur = riot.get_summoner('anchor1')
	current_match = riot.get_current_match_details(ankur)

	if current_match:
		print("Ankur is currently in game")
	else:
		print("Ankur is currently not in game")

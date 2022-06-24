#!/usr/bin/env python3
from riot import api as riot

victim = 'anchor1'

if __name__ == "__main__":
	ankur = riot.get_summoner(victim)
	# import ipdb; ipdb.set_trace()
	current_match = riot.get_current_match(ankur)

	if current_match:
		print("Ankur is currently in game")
		ankur_participant = riot.find_participant_in_match(
			current_match, ankur)
		print(f"Ankur is playing {ankur_participant.champion.name}")
		rank = riot.get_solo_queue_rank()
		print(f"Ankur's current rank is {rank[0]} {rank[1]}")

	else:
		print("Ankur is currently not in game")

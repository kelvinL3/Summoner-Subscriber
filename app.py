#!/usr/bin/env python3
from riot import api as riot

if __name__ == "__main__":
	anchor = riot.setup()
	riot.get_current_match_details(anchor)

print(1)

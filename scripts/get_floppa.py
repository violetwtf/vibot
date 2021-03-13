# get_floppa.py: Fills the floppas directory with floppas
# Depends on assets/floppa.json, which I got from https://instagram.com/floppa.official?__a=1

import json
import requests

floppa = 0

with open('assets/floppa.json') as file:
    data = json.load(file)
    edges = data['graphql']['user']['edge_owner_to_timeline_media']['edges']
    for edge in edges:
        with open(f'assets/floppas/floppa_{floppa}.jpg', 'wb') as floppa_file:
            floppa_file.write(
                requests.get(edge['node']['display_url']).content)
        floppa = floppa + 1

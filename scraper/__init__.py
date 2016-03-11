import sys

import requests

from scraper.database import get_session
from scraper.models import Player
from scraper.settings import Config


def fetch(resource, **kwargs):
    url = 'https://br.api.pvp.net/api/lol/br/v2.2/' + resource
    kwargs['api_key'] = Config.TOKEN
    response = requests.get(url, params=kwargs)
    return response.json()


def main():
    if len(sys.argv) < 2:
        sys.exit('No match id provided, exiting')

    session = get_session()

    match_id = sys.argv[-1]
    match_data = fetch('match/%s' % match_id)

    for participant in match_data['participantIdentities']:
        summoner_id = participant['player']['summonerId']
        summoner_name = participant['player']['summonerName']

        player = session.query(Player).filter_by(id=summoner_id).first()
        if player is not None:
            player.username = summoner_name
            print 'updated', player.username
            continue

        player = Player(
            id=summoner_id,
            username=summoner_name
        )
        session.add(player)
        print 'created', player.username
    session.commit()

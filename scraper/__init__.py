import sys

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Player
try:
    from scraper.localconfig import Config
except ImportError:
    from scraper.config import Config


def fetch(resource, **kwargs):
    url = 'https://br.api.pvp.net/api/lol/br/v2.2/' + resource
    kwargs['api_key'] = Config.TOKEN
    response = requests.get(url, params=kwargs)
    return response.json()


def main():
    if len(sys.argv) < 2:
        sys.exit('No match id provided, exiting')

    uri = '{}://{}:{}@{}/{}'.format(Config.RDBMS, Config.DB_USER,
                                    Config.DB_PASS, Config.DB_HOST,
                                    Config.DB_NAME)
    engine = create_engine(uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    match_id = sys.argv[-1]
    match_data = fetch('match/%s' % match_id)

    for participant in match_data['participantIdentities']:
        player = Player(
            id=participant['player']['summonerId'],
            username=participant['player']['summonerName']
        )
        session.add(player)
    session.commit()

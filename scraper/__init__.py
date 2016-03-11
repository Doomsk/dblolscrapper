import requests

from scraper.database import get_session
from scraper.models import Player, Match, PlayerMatch
from scraper.settings import Config


def fetch(resource, **kwargs):
    url = 'https://br.api.pvp.net/api/lol/br/v2.2/' + resource
    kwargs['api_key'] = Config.TOKEN
    response = requests.get(url, params=kwargs)
    return response.json()


def scrap_match(match_id):
    session = get_session()

    match_data = fetch('match/%s' % match_id)

    for participant in match_data['participantIdentities']:
        summoner_id = participant['player']['summonerId']
        summoner_name = participant['player']['summonerName']
        print 'parsing', summoner_name
        Player.get_or_create(session, {'id': summoner_id},
                             username=summoner_name)
    session.commit()


def scrap_summoner(summoner_ids=None):
    session = get_session()
    if summoner_ids is None:
        summoner_ids = [p.id for p in session.query(Player.id)]

    for summoner_id in summoner_ids:
        print 'fetching data for', summoner_id
        summoner_data = fetch('matchlist/by-summoner/%s' % summoner_id)
        for match in summoner_data['matches']:
            print 'parsing', match['matchId']
            data = {
                'player_id': summoner_id,
                'match_id': match['matchId'],
                'champion_id': match['champion'],
                'lane': match['lane'],
                'role': match['role'],
                'queue': match['queue'],
                'season': match['season'],
            }

            Match.get_or_create(session, {'id': match['matchId']})
            PlayerMatch.get_or_create(session, {
                'player_id': summoner_id,
                'match_id': data['match_id'],
            }, **data)
        session.commit()

from datetime import datetime

import requests

from scraper.database import get_session
from scraper.models import Champion, Player, Match, PlayerMatchMap
from scraper.settings import Config


def fetch_base(base, resource, **kwargs):
    url = base + resource
    kwargs['api_key'] = Config.TOKEN
    response = requests.get(url, params=kwargs)
    return response.json()


def fetch_static(resource, **kwargs):
    base = 'https://br.api.pvp.net/api/lol/static-data/br/'
    return fetch_base(base, resource, **kwargs)

def fetch(resource, **kwargs):
    base = 'https://br.api.pvp.net/api/lol/br/'
    return fetch_base(base, resource, **kwargs)


def scrap_match(match_id):
    session = get_session()
    print 'fetching data for match', match_id

    match_data = fetch('v2.2/match/%s' % match_id)
    participants = match_data['participants']

    # Create the match
    creation =  datetime.fromtimestamp(match_data['matchCreation'] / 1000.0)
    data = {
        'type': match_data['matchType'],
        'version': match_data['matchVersion'],
        'queue_type': match_data['queueType'],
        'creation': creation,
        'duration': match_data['matchDuration'],
    }
    Match.get_or_create(session, {'id': match_id}, **data)

    for participant in match_data['participantIdentities']:
        summoner_id = participant['player']['summonerId']
        summoner_name = participant['player']['summonerName']
        print 'parsing', summoner_name
        Player.get_or_create(session, {'id': summoner_id},
                             username=summoner_name)
        details = [p for p in participants
                   if participant['participantId'] == p['participantId']][0]
        data = {
            'champion_id': details['championId'],
            'season': match_data['season'],
            'deaths': details['stats']['deaths'],
            'kills': details['stats']['kills'],
            'assists': details['stats']['assists'],
            'has_won': details['stats']['winner'],
        }
        PlayerMatchMap.get_or_create(session, {
            'player_id': summoner_id,
            'match_id': match_id,
        }, **data)
    session.commit()


def scrap_summoner(summoner_ids=None, details=False):
    session = get_session()
    if summoner_ids is None:
        summoner_ids = [p.id for p in session.query(Player.id)]

    summoners_data = fetch('v1.4/summoner/%s' % ','.join(summoner_ids))
    for id, data in summoners_data.iteritems():
        Player.get_or_create(session, {'id': id},
                             username=data['name'])

    for summoner_id in summoner_ids:
        print 'fetching data for summoner', summoner_id
        summoner_data = fetch('v2.2/matchlist/by-summoner/%s' % summoner_id)
        for match in summoner_data['matches']:
            print 'parsing', match['matchId']
            Champion.get_or_create(session, {'id': match['champion']})
            Match.get_or_create(session, {'id': match['matchId']})

            data = {
                'player_id': summoner_id,
                'match_id': match['matchId'],
                'champion_id': match['champion'],
                'lane': match['lane'],
                'role': match['role'],
                'queue': match['queue'],
                'season': match['season'],
            }

            PlayerMatchMap.get_or_create(session, {
                'player_id': summoner_id,
                'match_id': data['match_id'],
            }, **data)

            if details:
                scrap_match(data['match_id'])

        session.commit()


def scrap_champions():
    session = get_session()

    for name, data in fetch_static('v1.2/champion')['data'].iteritems():
        print 'parsing', name
        Champion.get_or_create(session, {'id': data['id']}, name=name)
    session.commit()

import requests
import json

RIOT_API_KEY = "RGAPI-d62b2bd9-b84f-4f0a-8b78-7726ac3dba73"
GAME_NAME = "NickNickNick"
TAG_LINE = "NICK"

def get_puuid(game_name, tag_line):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['puuid']
    else:
        print(f"Error fetching PUUID: {response.status_code} {response.text}")
        return None

def get_most_recent_match_id(puuid):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1"
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        match_ids = response.json()
        if match_ids:
            return match_ids[0]
    print(f"Error fetching match IDs: {response.status_code} {response.text}")
    return None

def get_match_details(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching match details: {response.status_code} {response.text}")
        return None

def display_match_details(match_data, puuid):
    match_info = {
        'match_id': match_data['metadata']['matchId'],
        'game_duration': match_data['info']['gameDuration'],
        'game_mode': match_data['info']['gameMode'],
        'teams': []
    }
    
    for team in match_data['info']['teams']:
        team_info = {
            'team_id': team['teamId'],
            'win': team['win'],
            'objectives': team['objectives']
        }
        match_info['teams'].append(team_info)
    
    for participant in match_data['info']['participants']:
        if participant['puuid'] == puuid:
            participant_info = {
                'summoner_name': participant['summonerName'],
                'champion': participant['championName'],
                'kills': participant['kills'],
                'deaths': participant['deaths'],
                'assists': participant['assists'],
                'total_damage_dealt': participant['totalDamageDealt'],
                'gold_earned': participant['goldEarned'],
                'champ_level': participant['champLevel'],
                'vision_score': participant['visionScore'],
                'total_minions_killed': participant['totalMinionsKilled'],
                'items': [participant[f'item{i}'] for i in range(7)]
            }
            match_info['participant'] = participant_info
            break
    
    print(json.dumps(match_info, indent=4))

def main():
    puuid = get_puuid(GAME_NAME, TAG_LINE)
    if puuid:
        match_id = get_most_recent_match_id(puuid)
        if match_id:
            match_data = get_match_details(match_id)
            if match_data:
                display_match_details(match_data, puuid)
            else:
                print("Failed to fetch match details.")
        else:
            print("Failed to fetch most recent match ID.")
    else:
        print("Failed to fetch PUUID.")

if __name__ == "__main__":
    main()
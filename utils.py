import requests
import json
from fastapi import HTTPException
from config import riot_api_key, openai_api_key
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo")

def get_puuid(game_name: str, tag_line: str):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {
        "X-Riot-Token": riot_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="PUUID not found")
    return response.json()['puuid']

def get_recent_match_ids(puuid: str, count: int = 10):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    headers = {
        "X-Riot-Token": riot_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200):
        raise HTTPException(status_code=404, detail="Match IDs not found")
    return response.json()

def get_match_details(match_id: str):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": riot_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Match details not found")
    return response.json()

def get_updated_summoner_name(original_name: str):
    name_mapping = {
        "Jujutsu Biden": "NickNickNick",
        "XxLoliSlayerxX": "Boostio",
        "ShreyashImSorry": "CyborgBarber"
    }
    return name_mapping.get(original_name, original_name)

def format_match_details(match_data, puuid):
    match_info = {
        'match_id': match_data['metadata']['matchId'],
        'game_duration': match_data['info']['gameDuration'],
        'game_mode': match_data['info']['gameMode'],
        'teams': []
    }

    player_team_id = None
    for participant in match_data['info']['participants']:
        if participant['puuid'] == puuid:
            player_team_id = participant['teamId']
            break

    good_player = None
    bad_player = None
    players = []

    for team in match_data['info']['teams']:
        team_info = {
            'team_id': team['teamId'],
            'win': team['win'],
            'objectives': team['objectives'],
            'players': []
        }
        for participant in match_data['info']['participants']:
            if participant['teamId'] == player_team_id:
                updated_name = get_updated_summoner_name(participant['summonerName'])
                player_info = {
                    'summoner_name': updated_name,
                    'champion': participant['championName'],
                    'kills': participant['kills'],
                    'deaths': participant['deaths'],
                    'assists': participant['assists'],
                    'total_damage_dealt_to_champions': participant['totalDamageDealtToChampions'],
                    'gold_earned': participant['goldEarned'],
                    'champ_level': participant['champLevel'],
                    'vision_score': participant['visionScore'],
                    'total_minions_killed': participant['totalMinionsKilled'],
                    'items': [participant[f'item{i}'] for i in range(7)]
                }
                team_info['players'].append(player_info)
                players.append(player_info)
        match_info['teams'].append(team_info)
    
    if players:
        good_player = max(players, key=lambda x: x['kills'])
        bad_player = min(players, key=lambda x: x['kills'])
    
    return match_info, good_player, bad_player

def get_response_from_openai(match_details: str):
    prompt_template = PromptTemplate(
        input_variables=["match_details"],
        template="""Analyze the following match data and provide a detailed description of who was the carry and who was the most useless. Make the analysis detailed and include some humorous or funny comments.
        Here are some examples of how to analyze the data:
        Example 1:
        The carry was Player A due to *stats and praises*. Meanwhile, Player B was the least useful human being due to *stats and literal insults*.
        Now analyze the following match data:
        {match_details}"""
    )
    sequence = prompt_template | llm
    response = sequence.invoke({"match_details": match_details})
    return response

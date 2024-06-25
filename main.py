import requests
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()
riot_api_key = os.getenv('RIOT_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo")

def get_puuid(game_name: str, tag_line: str):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {
        "X-Riot-Token": riot_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching PUUID: {response.status_code} {response.text}")
    return response.json()['puuid']

def get_recent_match_ids(puuid: str, count: int = 20):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    headers = {
        "X-Riot-Token": riot_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching match IDs: {response.status_code} {response.text}")
    return response.json()

def get_match_details(match_id: str):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": riot_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching match details: {response.status_code} {response.text}")
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
        if team_info['team_id'] == player_team_id:
            match_info['teams'].append(team_info)
    
    return match_info

def get_response_from_openai(match_details: str):
    prompt_template = PromptTemplate(
        input_variables=["match_details"],
        template="Analyze the following match data and provide a detailed description of who was the carry and who was the most useless player:\n{match_details}"
    )
    sequence = prompt_template | llm
    response = sequence.invoke({"match_details": match_details})
    return response

def main():
    game_name = "NickNickNick"  # replace with your game name
    tag_line = "NICK"  # replace with your tag line
    
    try:
        puuid = get_puuid(game_name, tag_line)
        match_ids = get_recent_match_ids(puuid)
        print("Recent Matches:")
        for i, match_id in enumerate(match_ids):
            print(f"{i + 1}: Match ID {match_id}")
        
        match_choice = int(input("Enter the number of the match you want to analyze (1-20): ")) - 1
        if match_choice < 0 or match_choice >= len(match_ids):
            raise ValueError("Invalid match choice")
        
        match_id = match_ids[match_choice]
        match_data = get_match_details(match_id)
        match_details = format_match_details(match_data, puuid)
        match_details_str = json.dumps(match_details, indent=4)
        print("Match Details:")
        print(match_details_str)
        openai_response = get_response_from_openai(match_details_str)
        print("\nOpenAI Analysis:")
        print(openai_response)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

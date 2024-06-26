import requests
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

riot_api_key = os.getenv('RIOT_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo")

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    game_name: str
    tag_line: str

class MatchChoiceRequest(BaseModel):
    game_name: str
    tag_line: str
    match_index: int

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
    if response.status_code != 200:
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
        template="""Analyze the following match data and provide a detailed description of who was the carry and who was the most useless. Have some serious insults and pretend you're disappointed
        Example: In this match, the carry of the team was clearly "CyborgBarber" playing as Sivir. With an impressive 15 kills, 8 deaths, and 19 assists, CyborgBarber dealt a whopping 60533 damage to champions and earned 23192 gold. Their performance was crucial in securing the victory for their team, leading the charge in team fights and dealing significant damage throughout the game. Now, onto the most useless player in this match, we have to point fingers at "AmazonFireTV" playing as Bard. With only 1 kill, 6 deaths, and a staggering 31 assists, AmazonFireTV's impact on the game was minimal at best. Their total damage dealt to champions was a measly 15646, and they earned the least gold among the team members. It's safe to say that AmazonFireTV was dead weight in this match, being carried by the rest of the team and contributing very little to the overall success. AmazonFireTV, if you're reading this, I have to say that your performance was incredibly disappointing and you should seriously reconsider your choice of champion. You were a burden to your team and your lackluster performance was a disgrace to the game. Step up your game or consider finding a new hobby because League of Legends clearly isn't your forte.
        Now analyze the following match data:
        {match_details}"""
    )
    sequence = prompt_template | llm
    response = sequence.invoke({"match_details": match_details})
    return response

@app.post("/get_matches/")
async def get_matches(request: UserRequest):
    puuid = get_puuid(request.game_name, request.tag_line)
    match_ids = get_recent_match_ids(puuid)
    return {"match_ids": match_ids}

@app.post("/analyze_match/")
async def analyze_match(request: MatchChoiceRequest):
    puuid = get_puuid(request.game_name, request.tag_line)
    match_ids = get_recent_match_ids(puuid)
    if request.match_index < 0 or request.match_index >= len(match_ids):
        raise HTTPException(status_code=400, detail="Invalid match index")
    
    match_id = match_ids[request.match_index]
    match_data = get_match_details(match_id)
    match_details = format_match_details(match_data, puuid)
    match_details_str = json.dumps(match_details, indent=4)
    openai_response = get_response_from_openai(match_details_str)
    return {"openai_response": openai_response.content}  # Correctly access the content attribute

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

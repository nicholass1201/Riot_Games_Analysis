import requests
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

riot_api_key = os.getenv('RIOT_API_KEY')

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

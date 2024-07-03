from fastapi import APIRouter, HTTPException
from models import UserRequest, MatchChoiceRequest
from riot_api import get_puuid, get_recent_match_ids, get_match_details
from openai_api import get_response_from_openai
from utils import format_match_details
import json

router = APIRouter()

@router.post("/get_matches/")
async def get_matches(request: UserRequest):
    puuid = get_puuid(request.game_name, request.tag_line)
    match_ids = get_recent_match_ids(puuid)
    return {"match_ids": match_ids}

@router.post("/analyze_match/")
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

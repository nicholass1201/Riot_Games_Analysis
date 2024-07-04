from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import get_db
from riot_api import get_puuid, get_recent_match_ids, get_match_details
from openai_api import get_response_from_openai
from utils import format_match_details
import json

router = APIRouter()

@router.post("/get_matches/")
async def get_matches(request: schemas.UserRequest, db: Session = Depends(get_db)):
    puuid = get_puuid(request.game_name, request.tag_line)
    match_ids = get_recent_match_ids(puuid)
    return {"match_ids": match_ids}

@router.post("/analyze_match/")
async def analyze_match(request: schemas.MatchChoiceRequest, db: Session = Depends(get_db)):
    puuid = get_puuid(request.game_name, request.tag_line)
    match_ids = get_recent_match_ids(puuid)
    if request.match_index < 0 or request.match_index >= len(match_ids):
        raise HTTPException(status_code=400, detail="Invalid match index")
    
    match_id = match_ids[request.match_index]
    match_data = get_match_details(match_id)
    match_details = format_match_details(match_data, puuid)
    match_details_str = json.dumps(match_details, indent=4)
    openai_response = get_response_from_openai(match_details_str)
    
    good_player = match_details['teams'][0]['players'][0]  # Example: first player of the first team
    bad_player = match_details['teams'][0]['players'][-1]  # Example: last player of the first team

    match_analysis = schemas.MatchAnalysisCreate(
        match_id=match_id,
        good_player_name=good_player['summoner_name'],
        good_player_stats=good_player,
        bad_player_name=bad_player['summoner_name'],
        bad_player_stats=bad_player,
        analysis=openai_response.content
    )

    crud.create_match_analysis(db=db, match_analysis=match_analysis)

    return {
        "openai_response": openai_response.content,
        "good_player": good_player,
        "bad_player": bad_player
    }

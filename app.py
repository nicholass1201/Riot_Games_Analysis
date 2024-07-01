from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import UserRequest, MatchChoiceRequest
from utils import get_puuid, get_recent_match_ids, get_match_details, format_match_details, get_response_from_openai

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    match_info, good_player, bad_player = format_match_details(match_data, puuid)
    match_details_str = json.dumps(match_info, indent=4)
    openai_response = get_response_from_openai(match_details_str)
    return {
        "openai_response": openai_response.content,
        "good_player": good_player,
        "bad_player": bad_player
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

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

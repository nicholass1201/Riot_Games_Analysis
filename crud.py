from sqlalchemy.orm import Session
import models, schemas

def create_match_analysis(db: Session, match_analysis: schemas.MatchAnalysisCreate):
    db_match_analysis = models.MatchAnalysis(
        match_id=match_analysis.match_id,
        good_player_name=match_analysis.good_player_name,
        good_player_stats=match_analysis.good_player_stats,
        bad_player_name=match_analysis.bad_player_name,
        bad_player_stats=match_analysis.bad_player_stats,
        analysis=match_analysis.analysis
    )
    db.add(db_match_analysis)
    db.commit()
    db.refresh(db_match_analysis)
    return db_match_analysis

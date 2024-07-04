from sqlalchemy import Column, Integer, String, JSON
from database import Base

class MatchAnalysis(Base):
    __tablename__ = "match_analysis"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, index=True)
    good_player_name = Column(String, index=True)
    good_player_stats = Column(JSON)
    bad_player_name = Column(String, index=True)
    bad_player_stats = Column(JSON)
    analysis = Column(String)

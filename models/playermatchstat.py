from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class PlayerMatchStat(Base):
    __tablename__ = 'player_match_stats'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    player_id = Column(BigInteger, ForeignKey('players.id'))
    match_id = Column(BigInteger)
    minutes_played = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    substitutions_time = Column(Integer)
    key_absences = Column(Text)

    # Nuevas columnas añadidas
    player_number = Column(Integer)
    nation = Column(Text)
    position = Column(Text)
    age = Column(Integer)
    minutes = Column(Integer)
    penalty_kicks = Column(Integer)
    penalty_kicks_attempted = Column(Integer)
    shots = Column(Integer)
    shots_on_target = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    touches = Column(Integer)
    tackles = Column(Integer)
    interceptions = Column(Integer)
    blocks = Column(Integer)
    expected_goals = Column(Float)
    non_penalty_expected_goals = Column(Float)
    expected_assists = Column(Float)
    shot_creating_actions = Column(Integer)
    goal_creating_actions = Column(Integer)
    passes_completed = Column(Integer)
    passes_attempted = Column(Integer)
    pass_completion_percentage = Column(Float)
    progressive_passes = Column(Integer)
    carries = Column(Integer)
    progressive_carries = Column(Integer)
    dribbles_attempted = Column(Integer)
    dribbles_successful = Column(Integer)

    player = relationship("Player", back_populates="match_stats")

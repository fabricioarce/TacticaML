from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class TeamSeasonStat(Base):
    __tablename__ = 'team_season_stats'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    team_id = Column(BigInteger, ForeignKey('teams.id'))
    season = Column(Text)
    matches = Column(Integer)
    points = Column(Integer)
    points_per_game = Column(Float)
    league_position = Column(Text)
    home_record = Column(Text)
    home_points = Column(Integer)
    away_record = Column(Text)
    away_points = Column(Integer)
    goals = Column(Integer)
    goals_per_game = Column(Float)
    goals_against = Column(Integer)
    goals_against_per_game = Column(Float)
    goal_difference = Column(Integer)
    expected_goals = Column(Float)
    expected_goals_against = Column(Float)
    expected_goal_difference = Column(Float)

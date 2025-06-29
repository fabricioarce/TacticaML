from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = 'matches'

    id = Column(String, primary_key=True, autoincrement=True)
    home_team_id = Column(String, ForeignKey('teams.id'))
    away_team_id = Column(String, ForeignKey('teams.id'))
    date = Column(Date)
    time = Column(Time)
    location = Column(Text)
    altitude = Column(Float)
    field_type = Column(Text)
    competition_id = Column(String, ForeignKey('competitions.id'))
    match_type = Column(Text)
    league_round = Column(Integer)
    home_team_points_before = Column(Integer)
    away_team_points_before = Column(Integer)
    home_team_points_after = Column(Integer)
    away_team_points_after = Column(Integer)
    referee_id = Column(String, ForeignKey('referees.id'))

    competition = relationship("Competition", back_populates="matches")
    referee = relationship("Referee", back_populates="matches")
    home_team = relationship("Team", back_populates="home_matches", foreign_keys=[home_team_id])
    away_team = relationship("Team", back_populates="away_matches", foreign_keys=[away_team_id])

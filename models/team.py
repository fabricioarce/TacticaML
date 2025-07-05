from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

from models.base import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    city = Column(Text)
    country = Column(Text)
    confederence_ranking = Column(Integer)
    ten_season_club_coefficients = Column(Text)
    league = Column(Text)

    players = relationship("Player", back_populates="team")
    travel_conditions = relationship("TravelCondition", back_populates="team")
    home_matches = relationship("Match", back_populates="home_team", foreign_keys='Match.home_team_id')
    away_matches = relationship("Match", back_populates="away_team", foreign_keys='Match.away_team_id')

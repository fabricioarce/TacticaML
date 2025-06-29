from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class Competition(Base):
    __tablename__ = 'competitions'

    id = Column(String, primary_key=True, autoincrement=True)
    player_name = Column(Text)
    player_id = Column(String, ForeignKey('teams.id'))
    player_season_id = Column(Text)

    matches = relationship("Match", back_populates="competition")

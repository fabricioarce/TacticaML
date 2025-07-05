from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

from models.base import Base

class Player(Base):
    __tablename__ = 'players'

    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)

    team = relationship("Team", back_populates="players")
    season_stats = relationship("PlayerSeasonStat", back_populates="player")
    match_stats = relationship("PlayerMatchStat", back_populates="player")
    duels_as_player1 = relationship("KeyDuel", foreign_keys='KeyDuel.player1_id', back_populates="player1")
    duels_as_player2 = relationship("KeyDuel", foreign_keys='KeyDuel.player2_id', back_populates="player2")

from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

from models.base import Base

class KeyDuel(Base):
    __tablename__ = 'key_duels'

    id = Column(String, primary_key=True)
    match_id = Column(String, ForeignKey('matches.id'))
    player1_id = Column(String, ForeignKey('players.id'))
    player2_id = Column(String, ForeignKey('players.id'))
    duel_type = Column(Text)

    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="duels_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="duels_as_player2")

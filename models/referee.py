from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

from models.base import Base

class Referee(Base):
    __tablename__ = 'referees'

    id = Column(String, primary_key=True)
    name = Column(Text)
    tendency_to_give_cards = Column(Float)
    tendency_to_favor_home_team = Column(Float)

    matches = relationship("Match", back_populates="referee")

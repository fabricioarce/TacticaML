from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import Base

class Competition(Base):
    __tablename__ = 'competitions'

    id = Column(String, primary_key=True)
    name = Column(Text)
    type = Column(Text)
    stage = Column(Text)

    matches = relationship("Match", back_populates="competition")

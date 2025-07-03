from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class Competition(Base):
    __tablename__ = 'competitions'

    id = Column(String, primary_key=True)
    name = Column(Text)
    type = Column(Text)
    stage = Column(Text)

    matches = relationship("Match", back_populates="competition")

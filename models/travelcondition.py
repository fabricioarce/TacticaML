from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

from models.base import Base

class TravelCondition(Base):
    __tablename__ = 'travel_conditions'

    id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey('teams.id'))
    match_id = Column(String, ForeignKey('matches.id'))
    days_of_rest = Column(Integer)
    recent_travel_distance = Column(Float)
    arrival_time = Column(Time)
    jet_lag = Column(Boolean)
    match_congestion = Column(Boolean)
    hotel_conditions = Column(Text)

    team = relationship("Team", back_populates="travel_conditions")

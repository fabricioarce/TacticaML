from sqlalchemy import Column, Integer, String, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class WeatherCondition(Base):
    __tablename__ = 'weather_conditions'

    id = Column(String, primary_key=True)
    match_id = Column(String, ForeignKey('matches.id'))
    temperature = Column(Float)
    humidity = Column(Float)
    rain = Column(Boolean)
    wind = Column(Float)
    fog = Column(Boolean)
    solar_radiation = Column(Float)
    thermal_sensation = Column(Float)

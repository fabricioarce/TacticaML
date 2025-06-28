from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class PlayerSeasonStat(Base):
    __tablename__ = 'player_season_stats'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    player_id = Column(BigInteger, ForeignKey('players.id'))
    season = Column(Text)
    goals = Column(Integer)
    assists = Column(Integer)
    passes = Column(Integer)
    tackles = Column(Integer)
    cards = Column(Integer)
    fatigue_level = Column(Integer)

    player = relationship("Player", back_populates="season_stats")

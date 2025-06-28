from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class TeamMatchStat(Base):
    __tablename__ = 'team_match_stats'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    match_id = Column(BigInteger, ForeignKey('matches.id'))
    team_id = Column(BigInteger, ForeignKey('teams.id'))
    possession = Column(Float)
    corners = Column(Integer)
    fouls = Column(Integer)
    offsides = Column(Integer)
    tactical_formation = Column(Text)
    playing_style = Column(Text)
    tactical_changes = Column(Text)

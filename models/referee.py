from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Float, Date, Time, ForeignKey, Text
from sqlalchemy.ext.declarative import relationship, declarative_base

Base = declarative_base()

class Referee(Base):
    __tablename__ = 'referees'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text)
    tendency_to_give_cards = Column(Float)
    tendency_to_favor_home_team = Column(Float)

    matches = relationship("Match", back_populates="referee")

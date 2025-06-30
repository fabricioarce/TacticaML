from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

# 
def get_session():
    engine = create_engine("postgresql+psycopg2://usuario:clave@localhost:5432/db")
    Session = sessionmaker(bind=engine)
    return Session()

def get_or_create_team(session, team_id=None, name=None, country=None, city=None):
    if team_id:
        team = session.query(Team).filter_by(id=team_id).first()
    elif name:
        team = session.query(Team).filter_by(name=name).first()
    else:
        raise ValueError("Debes proporcionar team_id o name")
    if not team:
        team = Team(id=team_id, name=name, country=country, city=city)
        session.add(team)
        session.commit()
    elif not team.country and country:
        team.country = country
        team.city = city
        session.commit()
    return team

# def get_or_create_player(session, player_name):
#     player_season = session.query(PlayerSeasonStat).filter_by()

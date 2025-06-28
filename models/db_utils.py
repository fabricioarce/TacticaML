from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.team import Team

# 
def get_session():
    engine = create_engine("postgresql+psycopg2://usuario:clave@localhost:5432/db")
    Session = sessionmaker(bind=engine)
    return Session()

def get_or_create_team(session, name, country=None, city=None):
    team = session.query(Team).filter_by(name=name).first()
    if not team:
        team = Team(name=name, country=country, city=city)
        session.add(team)
        session.commit()
    elif not team.country and country:
        team.country = country
        team.city = city
        session.commit()
    return team
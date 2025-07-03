from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

# 
def get_session():
    engine = create_engine("postgresql+psycopg2://fabri:supersegura123@localhost:5432/futbol_stats")
    Session = sessionmaker(bind=engine)
    return Session()

def get_or_create_team(session, team_id=None, name=None):
    if team_id:
        team = session.query(Team).filter_by(id=team_id).first()
    elif name:
        team = session.query(Team).filter_by(name=name).first()
    else:
        raise ValueError("Debes proporcionar team_id o name")
    if not team:
        team = Team(id=team_id, name=name)
        session.add(team)
        session.commit()
    return team

def get_or_create_team_season(session, team_id=None, season_id=None):
    if team_id and season_id:
        team_season = session.query(TeamSeason).filter_by(team_id=team_id, season_id=season_id).first()
    else:
        raise ValueError("Debes proporcionar team_id o season_id")
    if not team_season:
        team_season = TeamSeason(team_id=team_id, season_id=season_id)
        session.add(team_season)
        session.commit()
    return team_season

def get_or_create_player(session, player_id=None, name=None):
    if player_id:
        player = session.query(Player).filter_by(id=player_id).first()
    elif name:
        player = session.query(Player).filter_by(name=name).first()
    else:
        raise ValueError("Debes proporcionar player_id o name")
    if not player:
        player = Player(id=player_id, name=name, position=position)
        session.add(player)
        session.commit()
    return player

def get_or_create_player_stat(session, player_id, team_season_id, **stat_fields):
    stat = session.query(PlayerSeasonStat).filter_by(
        player_id=player_id,
        team_season_id=team_season_id
    ).first()
    if not stat:
        stat_id = f"{player_id}_{team_season_id}"
        stat = PlayerSeasonStat(id=stat_id, player_id=player_id, team_season_id=team_season_id, **stat_fields)
        session.add(stat)
        session.commit()
    return stat
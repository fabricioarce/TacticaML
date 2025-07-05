from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db_utils import create_engine
from sqlalchemy import create_engine
from models.base import Base
from models.team import Team
from models.teamseasonstat import TeamSeasonStat
from models.player import Player
from models.playerseasonstat import PlayerSeasonStat
from models.match import Match
from models.referee import Referee
from models.travelcondition import TravelCondition
from models.competition import Competition
from models.keyduel import KeyDuel

# 
def get_engine():
    engine = create_engine("sqlite:///futbol_stats.db")
    Base.metadata.create_all(engine)
    print("Engine created")
    return engine

def get_session():
    engine = get_engine()
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
        player = Player(id=player_id, name=name)
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
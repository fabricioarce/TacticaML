# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from models.db_utils import get_or_create_team, get_or_create_team_season, get_or_create_player, get_or_create_player_stat
from models.team import Team
from models.teamseasonstat import TeamSeasonStat
from models.player import Player
from models.playerseasonstat import PlayerSeasonStat
from sqlalchemy import create_engine
from models.base import Base

class NameTeamPipeline:
    def open_spider(self, spider):
        # Conect with PostgreSQL
        engine = create_engine("sqlite:///futbol_stats.db")

        # Create Table if it doesn't exist
        Base.metadata.create_all(engine)
        print("Engine created")

        # Create session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        print("Procesando item:", item)
        team = None
        if item.get("should_create_team"):
            team = get_or_create_team(
                session=self.session,
                name=item["name"],
                team_id=item["team_id"]
            )
            
        if item.get("should_create_team_season"):
            if not team:
                team = get_or_create_team(
                    session=self.session,
                    name=item["name"],
                    team_id=item["team_id"]
                )
            get_or_create_team_season(
                session=self.session,
                team_id=team.id,
                season_id=item["season_id"]
            )
            
        player = None
        if item.get("should_create_player"):
            player = get_or_create_player(
                session=self.session,
                player_id=item["player_id"],
                name=item["name"]
            )
        
        player_season_stat = None
        if item.get("should_create_player_stat"):
            player_season_stat = get_or_create_player_stat(
                session=self.session,
                player_id=item["player_id"],
                team_season_id=item["team_season_id"],
                **item["player_stat_fields"]
            )
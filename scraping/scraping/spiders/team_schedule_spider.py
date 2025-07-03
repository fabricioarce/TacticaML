import scrapy
import json
import os

class TeamScheduleSpiderSpider(scrapy.Spider):
    """
    A Scrapy spider to scrape football team and player stats from fbref.com.
    """
    name = "team_schedule_spider"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/comps"]

    def start_requests(self):
        """
        Loads league data from a JSON file and yields requests for each season's page.
        """
        # Load the updated JSON file.
        with open("/home/n0de/Documents/syncthing/Programacion-de-proyectos/predict/data/domestic_leagues_data.json", "r") as f:
            data = json.load(f)

        # Iterate through each category (e.g., "Spain"), league (e.g., "La Liga"), and season.
        for category, leagues in data.items():  # "España"
            for league_name, league_info in leagues.items():  # "LaLiga"
                seasons = league_info.get("seasons", {})
                for season_name, url in seasons.items():
                    # Yield a request for each season's URL.
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        meta={
                            "category": category,
                            "league": league_name,
                            "season": season_name
                        }
                    )

    def parse(self, response):
        """
        Parses the league page to find links to individual team pages and follows them.
        """
        rows = response.xpath("/html/body/div[1]/div[6]/div[3]/div[4]/div[1]/table/tbody/tr")
        for row in rows:
            team_name = response.xpath(".//td[1]/a/text()").get()
            team_url  = response.xpath(".//td[1]/a/@href").get()

            yield response.follow(
                url=team_url,
                callback=self.pas,
                meta={
                    "team_name": team_name,
                    "team_url": team_url
                }
            )

    def pas(self, response):
        """
        On a team page, finds and follows the link to the 'All Competitions' stats page.
        """
        all_competition = response.xpath("/html/body/div[4]/div[6]/div[2]/div[1]/a/@href").get()
        
        yield response.follow(
            url=all_competition,
            callback=self.team_and_season_player,
            meta={
                "team_name": response.meta["team_name"],
                "team_url": response.meta["team_url"]
            }
        )

    def team_and_season_player(self, response):
        """
        A dispatcher method that calls methods to scrape both team and player data.
        """
        yield from self.team(response)
        yield from self.player_season(response)

    def team(self, response):
        """
        Extracts and yields basic team information (ID and name).
        """
        season = response.xpath("/html/body/div[4]/div[3]/div[1]/div[2]/h1/span[1]/text()").get()
        
        team_name = season.split()
        season_id = response.url
        team_id = season_id.split("/")[-3]
        season_id = season_id.split("/")
        season_id = season_id[-3] + "_" + season_id[-2]

        yield {
            "should_create_team": True,
            "name": team_name[1],
            "team_id": team_id
        }
        yield {
            "should_create_team_season": True,
            "season_id": season_id,
            "team_id": team_id
        }

    def player_season(self, response):
        """
        Scrapes multiple tables of player statistics for a given team and season.
        It calls `extraer_tabla` for each stats table.
        """
        team_season_id = response.url
        team_season_id = team_season_id.split("/")
        team_season_id = team_season_id[-3] + "_" + team_season_id[-2]
        jugadores = {}

        # Table 1: Standard Stats
        campos_std = ["pos", "age"]
        self.extraer_tabla(
            response,
            '//div[6]/div[3]/div[7]/div[1]/table/tbody/tr',
            campos_std,
            jugadores,
            td_offset=1  # Data starts in the second td, so use offset=1
        )

        # Table 2: Shooting Stats
        campos_shoot = [
            "gls", "sh", "sot", "sot_pct", "sh_per90", "sot_per90", "g_sh", "g_sot", "dist", "fk",
            "pk", "pkatt", "xg", "npxg", "npxgpersh", "glsminusxg", "npgminusnpxg"
        ]
        self.extraer_tabla(
            response,
            '//div[6]/div[11]/div[7]/div[1]/table/tbody/tr',
            campos_shoot,
            jugadores,
            td_offset=4  # Data starts in the fifth td
        )

        # Table 3: Passing Stats
        campos_pass = [
            "cmp", "att", "cmp_pct", "totdist", "prgdist",
            "cmp_short", "att_short", "cmp_pct_short",
            "cmp_medium", "att_medium", "cmp_pct_medium",
            "cmp_long", "att_long", "cmp_pct_long",
            "ast", "xag", "xa", "aminusxag", "kp", "ft", "ppa", "crspa", "prgp"
        ]
        self.extraer_tabla(
            response,
            '//div[6]/div[12]/div[7]/div[1]/table/tbody/tr',
            campos_pass,
            jugadores,
            td_offset=4
        )

        # Table 4: Pass Type Stats
        campos_pass_type = [
            "live", "dead", "pfk", "tb", "sw", "crs", "ti", "ck", "pass_off", "blocks",
            "corner_in", "corner_out", "corner_str"
        ]
        self.extraer_tabla(
            response,
            '//div[6]/div[14]/div[7]/div[1]/table/tbody/tr',
            campos_pass_type,
            jugadores,
            td_offset=4
        )
        
        campos_goal_and_shot_creation = [
            "sca", "sca_per90", "sca_passlive", "sca_passdead", "sca_to", "sca_sh", "sca_fld", "sca_def", "gca", "gca_per90", "gca_passlive", "gca_passdead", "gca_sh", "gca_to", "gca_fld", "gca_def" 
        ]

        self.extraer_tabla(
            response,
            '//div[6]/div[15]/div[7]/div[1]/table/tbody/tr',
            campos_goal_and_shot_creation,
            jugadores,
            td_offset=4
        )
        
        campos_defensive_actions = [
            "tackles_tkl", "tackles_tklw", "def_3rd", "mid_3rd", "att_3rd", "challenges_tkl", "challenges_att", "tackles_tkl_percentage", "challenges_lost", "def_blocks", "def_blocks_sh", "def_blocks_pass", "interceptions", "tklplusinterceptions", "clearences", "errors"
        ]

        self.extraer_tabla(
            response,
            '//div[6]/div[16]/div[7]/div[1]/table/tbody/tr',
            campos_defensive_actions,
            jugadores,
            td_offset=4
        )

        campos_possesion = [
            "touches", "def_pen", "def_3rd", "mid_3rd", "att_3rd", "att_pen", "touches_live", "tale_on_att", "success", "success_pct", "tkld", "tkld_pct", "carries", "tot_dist", "prg_dist", "prgc", "one_third", "cpa", "mis", "dis"
        ]

        self.extraer_tabla(
            response,
            '//div[6]/div[17]/div[7]/div[1]/table/tbody/tr',
            campos_possesion,
            jugadores,
            td_offset=4
        )
        
        campos_playing_time = [
            "mp", "min", "minpermp", "min_pct", "ninetys", "starts", "minperstart", "compl", "subs", "minpersub", "unsub", "ppm", "ong", "onga", "plusminus", "plusminus_per90", "onoff", "onxg", "onxga", "xgplusminus", "xgplusminus_per90", "xg_onoff"
        ]

        self.extraer_tabla(
            response,
            '//div[6]/div[18]/div[7]/div[1]/table/tbody/tr',
            campos_playing_time,
            jugadores,
            td_offset=4
        )
        
        campos_miscellaneous = [
            "crdy", "crdr", "secondcrdy", "fls", "fld", "off", "m_crs", "tkl_won", "pk_won", "og", "recov", "won", "lost", "won_pct"
        ]

        self.extraer_tabla(
            response,
            '//div[6]/div[19]/div[7]/div[1]/table/tbody/tr',
            campos_miscellaneous,
            jugadores,
            td_offset=4
        )
        
        # To add more tables, follow this pattern:
        # campos_nueva_tabla = ["campo1", "campo2", ...]
        # self.extraer_tabla(response, 'XPATH_TO_THE_TABLE', campos_nueva_tabla, jugadores, td_offset=...)
        
        # After processing all rows for the current table, yield all player items.
        # stat = PlayerSeasonStat(player_id=player_id, team_season_id=team_season_id, **stat_fields)
        for player in jugadores.values():
            yield {
                    "should_create_player": True,
                    "player_id": player["player_id"],
                    "name": player["player_name"],
                    "should_create_player_stat": True,
                    "team_season_id": team_season_id,
                    "player_stat_fields": player["stats"],
                    }

    def extraer_tabla(self, response, xpath_tabla, campos, jugadores, td_offset=0):
        """
        Extracts data from a player stats table and adds it to the 'jugadores' dictionary.

        Args:
            response: The Scrapy response object.
            xpath_tabla (str): XPath to the table rows (specifically the 'All Competitions' section).
            campos (list): A list of field names corresponding to the table columns.
            jugadores (dict): The accumulator dictionary for player data.
            td_offset (int): The column offset if data doesn't start in the first 'td' (e.g., due to hidden columns).
        """
        rows = response.xpath(xpath_tabla)
        for row in rows:
            player_link = row.xpath('./th/a/@href').get()
            player_name = row.xpath('./th/a/text()').get()
            player_id = None
            
            if player_link:
                segments = player_link.split('/')
                if len(segments) >= 3:
                    player_id = segments[-2]
            
            # Use the player link or name as a unique key.
            key = player_id or player_link or player_name
            if not key:
                continue
            # If the player is not yet in the dictionary, add them.
            if key not in jugadores:
                jugadores[key] = {
                    "player_id": player_id,
                    "player_name": player_name,
                    "player_link": player_link,
                    "stats": {}
                }
            # Extract each stat and add it to the player's dictionary.
            for idx, campo in enumerate(campos, start=1 + td_offset):
                jugadores[key]["stats"][campo] = row.xpath(f'./td[{idx}]/text()').get()

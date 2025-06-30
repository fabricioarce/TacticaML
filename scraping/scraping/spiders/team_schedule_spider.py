import scrapy
import json

class TeamScheduleSpiderSpider(scrapy.Spider):
    name = "team_schedule_spider"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/comps"]

    def start_requests(self):
        # Cargar el JSON actualizado
        with open("domestic_leagues_data.json", "r") as f:
            data = json.load(f)

        for category, leagues in data.items():  # "España"
            for league_name, league_info in leagues.items():  # "LaLiga"
                seasons = league_info.get("seasons", {})
                for season_name, url in seasons.items():
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
        rows = response.xpath("/html/body/div[1]/div[6]/div[3]/div[4]/div[1]/table/tbody/tr")
        for row in rows:
            team_name = response.xpath(".//td[1]/a/text()")
            team_url  = response.xpath(".//td[1]/a/@href")

            yield response.follow(
                url=team_url,
                callback=self.pas,
            )

    def pas(self, response):
        all_compettion = response.xpath("/html/body/div[4]/div[6]/div[2]/div[1]/a/@href")
        
        yield response.follow(
            url=all_compettion,
            callback=self.team_and_season_player
        )

    def team_and_season_player(self, response):
        yield from self.team(response)
        yield from self.player_season(response)

    def team(self, response):
        season = response.xpath("/html/body/div[4]/div[3]/div[1]/div[2]/h1/span[1]/text()")
        team_name = season.split()
        team_id = response.url
        team_id = team_id.split("/")

        yield {
            "team_id": team_id[5],
            "name": team_name[1],
            "should_create_team": True
        }

    def player_season(self, response):
        season = response.xpath("/html/body/div[4]/div[3]/div[1]/div[2]/h1/span[1]/text()")
        team_name = season.split()

        campos = [
            # Datos generales
            "pos", "age", "mp", "starts", "min", "ninetys",
            # Goles y asistencias
            "gls", "ast", "gplusa", "gminuspk", "pk", "pkatt",
            # Tarjetas
            "crdy", "crdr", "secondcrdy",
            # xG y variantes
            "xg", "npxg", "xag", "npxg_xag",
            # Progresiones
            "prgc", "prgp", "prgr",
            # Tiros
            "sh", "sot", "sot_pct", "sh_per90", "sot_per90", "g_sh", "g_sot", "dist", "fk",
            # xG adicionales
            "npxg_sh", "g_xg", "npg_xg",
            # Pases
            "cmp", "att", "cmp_pct", "totdist", "prgdist",
            # Pases por zona
            "cmp_short", "att_short", "cmp_pct_short",
            "cmp_medium", "att_medium", "cmp_pct_medium",
            "cmp_long", "att_long", "cmp_pct_long",
            # Asistencias avanzadas
            "xag_adv", "xa", "a_xag", "kp", "third", "ppa", "crspa", "prgp_adv",
            # Centros y jugadas
            "att_adv", "live", "dead", "fk_adv", "tb", "sw", "crs", "ti", "ck", "in_adv", "out_adv", "str_adv",
            # Ofensivas y bloqueos
            "off", "blocks",
            # SCA/GCA
            "sca", "sca90", "passlive", "passdead", "to", "sh_adv", "fld", "def_adv",
            "gca", "gca90", "passlive_gca", "passdead_gca", "to_gca", "sh_gca", "fld_gca", "def_gca",
            # Defensa
            "tkl", "tklw", "def_3rd", "mid_3rd", "att_3rd", "tkl_adv", "att_adv2", "tkl_pct", "lost", "blocks_adv", "sh_block", "pass_block", "interceptions", "tkl_int", "clr", "err",
            # Conducción y toques
            "touches", "def_pen", "def_3rd_touch", "mid_3rd_touch", "att_3rd_touch", "att_pen", "live_touch", "att_touch", "succ", "succ_pct", "tkld", "tkld_pct", "carries", "totdist_carry", "prgdist_carry", "prgc_carry", "third_carry", "cpa", "mis", "dis", "rec", "prgr_carry",
            # Minutos y partidos
            "mp2", "min2", "mn_mp", "min_pct", "ninetys2", "starts2", "mn_start", "compl", "subs", "mn_sub", "unsub", "ppm", "ong", "onga", "plus_minus", "plus_minus90", "on_off", "onxg", "onxga", "xg_plus_minus", "xg_plus_minus90", "on_off_adv",
            # Faltas y disciplina
            "crdy2", "crdr2", "twocrdy", "fls", "fld2", "off2", "crs2", "int2", "tklw2", "pkwon", "pkcon", "og", "recov", "won", "lost2", "won_pct"
        ]
        # Estandar: '//div[6]/div[?]/div[7]/div[1]/table/tbody/tr'
        # Tabla 1: estadísticas estándar
        rows_std = response.xpath('//div[6]/div[3]/div[7]/div[1]/table/tbody/tr')
        for row in rows_std:
            player_name = row.xpath('./th/a/text()').get()
            player_link = row.xpath('./th/a/@href').get()
            if not player_name:
                continue
            key = player_link or player_name
            jugadores[key] = {
                "player_name": player_name,
                "player_link": player_link,
                
                "pos": row.xpath("./td[2]/text()").get(),
                "age": row.xpath("./td[3]/text()").get(),
                "mp": row.xpath("./td[4]/text()").get(),
                "starts": row.xpath("./td[5]/text()").get(),
                "min": row.xpath("./td[6]/text()").get(),
                "ninetys": row.xpath("./td[7]/text()").get(),
            }
        
        # Table 2: Shoots table 
        rows_shoot = response.xpath('//div[6]/div[11]/div[7]/div[1]/table/tbody/tr')
        for row in rows_shoot:
            player_link = row.xpath('./th/a/@href').get()
            player_name = row.xpath('./th/a/text()').get()
            key = player_link or player_name
            if key not in jugadores:
                jugadores[key] = {
                    "player_name": player_name,
                    "player_link": player_link,
                }
            # get the info of the shoot table
            # Goals
            jugadores[key]["gls"] = row.xpath('./td[5]/text()').get()
            jugadores[key]["sh"] = row.xpath('./td[6]/text()').get()
            jugadores[key]["sot"] = row.xpath('./td[7]/text()').get()
            jugadores[key]["sot_pct"] = row.xpath('./td[8]/text()').get()
            jugadores[key]["sh_per90"] = row.xpath('./td[9]/text()').get()
            jugadores[key]["sot_per90"] = row.xpath('./td[10]/text()').get()
            jugadores[key]["g_sh"] = row.xpath('./td[11]/text()').get()
            jugadores[key]["g_sot"] = row.xpath('./td[12]/text()').get()
            jugadores[key]["dist"] = row.xpath('./td[13]/text()').get()
            jugadores[key]["fk"] = row.xpath('./td[14]/text()').get()
            jugadores[key]["pk"] = row.xpath('./td[15]/text()').get()
            jugadores[key]["pkatt"] = row.xpath('./td[16]/text()').get()
            # xG y variantes
            jugadores[key]["xg"] = row.xpath('./td[17]/text()').get()
            jugadores[key]["npxg"] = row.xpath('./td[18]/text()').get()
            jugadores[key]["npxgpersh"] = row.xpath('./td[19]/text()').get()
            jugadores[key]["glsminusxg"] = row.xpath('./td[20]/text()').get()
            jugadores[key]["npgminusnpxg"] = row.xpath('./td[21]/text()').get()

        rows_pass = response.xpath('//div[6]/div[12]/div[7]/div[1]/table/tbody/tr')
        for row in rows_shoot:
            player_link = row.xpath('./th/a/@href').get()
            player_name = row.xpath('./th/a/text()').get()
            key = player_link or player_name
            if key not in jugadores:
                jugadores[key] = {
                    "player_name": player_name,
                    "player_link": player_link,
                }
            # Total
            jugadores[key]["cmp"] = row.xpath('./td[5]/text()').get()
            jugadores[key]["att"] = row.xpath('./td[6]/text()').get()
            jugadores[key]["cmp_pct"] = row.xpath('./td[7]/text()').get()
            jugadores[key]["totdist"] = row.xpath('./td[8]/text()').get()
            jugadores[key]["prgdist"] = row.xpath('./td[9]/text()').get()

                # Short
            jugadores[key]["cmp_short"] = row.xpath('./td[10]/text()').get()
            jugadores[key]["att_short"] = row.xpath('./td[11]/text()').get()
            jugadores[key]["cmp_pct_short"] = row.xpath('./td[12]/text()').get()

                # medium
            jugadores[key]["cmp_medium"] = row.xpath('./td[13]/text()').get()
            jugadores[key]["att_medium"] = row.xpath('./td[14]/text()').get()
            jugadores[key]["cmp_pct_medium"] = row.xpath('./td[15]/text()').get()
            
                # long
            jugadores[key]["cmp_long"] = row.xpath('./td[16]/text()').get()
            jugadores[key]["att_long"] = row.xpath('./td[17]/text()').get()
            jugadores[key]["cmp_pct_long"] = row.xpath('./td[18]/text()').get()

            # Expected
            jugadores[key]["ast"] = row.xpath('./td[19]/text()').get()
            jugadores[key]["xag"] = row.xpath('./td[20]/text()').get()
            jugadores[key]["xa"] = row.xpath('./td[21]/text()').get()
            jugadores[key]["aminusxag"] = row.xpath('./td[22]/text()').get()
            jugadores[key]["kp"] = row.xpath('./td[23]/text()').get()
            jugadores[key]["ft"] = row.xpath('./td[24]/text()').get()
            jugadores[key]["ppa"] = row.xpath('./td[25]/text()').get()
            jugadores[key]["crspa"] = row.xpath('./td[26]/text()').get()
            jugadores[key]["prgp"] = row.xpath('./td[27]/text()').get()

        rows_pass_type = response.xpath('//div[6]/div[13]/div[7]/div[1]/table/tbody/tr')
        for row in rows_shoot_type:
            player_link = row.xpath('./th/a/@href').get()
            player_name = row.xpath('./th/a/text()').get()
            key = player_link or player_name
            if key not in jugadores:
                jugadores[key] = {
                    "player_name": player_name,
                    "player_link": player_link,
                }
            # Total
            jugadores[key]["live"] = row.xpath('./td[5]/text()').get()
            jugadores[key]["dead"] = row.xpath('./td[6]/text()').get()
            jugadores[key]["pfk"] = row.xpath('./td[7]/text()').get()
            jugadores[key]["tb"] = row.xpath('./td[8]/text()').get()
            jugadores[key]["sw"] = row.xpath('./td[9]/text()').get()
            jugadores[key]["crs"] = row.xpath('./td[10]/text()').get()
            jugadores[key]["ti"] = row.xpath('./td[11]/text()').get()
            jugadores[key]["ck"] = row.xpath('./td[12]/text()').get()
            jugadores[key]["off"] = row.xpath('./td[13]/text()').get()
            jugadores[key]["blocks"] = row.xpath('./td[14]/text()').get()
            jugadores[key]["corner_in"] = row.xpath('./td[16]/text()').get()
            jugadores[key]["corner_out"] = row.xpath('./td[17]/text()').get()
            jugadores[key]["corner_str"] = row.xpath('./td[18]/text()').get()

        

        for item in jugadores.values():
            yield item
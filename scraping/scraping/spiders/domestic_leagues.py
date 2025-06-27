import scrapy
import json
import re

class DomesticLeaguesSpider(scrapy.Spider):
    name = "domestic-leagues"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/comps"]

    def parse(self, response):
        # Extract the links to the domestic leagues
        rows = response.xpath("/html/body/div[1]/div[5]/div[9]/div[2]/table/tbody/tr")

        # Iterate through each row in the table
        for row in rows:
            gender = row.xpath("./td[1]/text()").get()
            if gender == 'M':
                league_link = row.xpath(".//th/a/@href").get()
                league_name = row.xpath(".//th/a/text()").get()

                yield response.follow(
                    url=league_link,
                    callback=self.leagues_seasons,
                    meta={"league_name": league_name}
                )

    def leagues_seasons(self, response):
        league_name = response.meta["league_name"]
        season_links = response.xpath("/html/body/div[1]/div[6]/div[2]/div[2]/table/tbody/tr/th")

        # Iterate through each season link
        for season_link in season_links:
            season_url = season_link.xpath("./a/@href").get()
            full_url = response.urljoin(season_url)

            # Extract the season from the URL
            match = re.search(r'/(\d{4}-\d{2})', season_url)
            season_name = match.group(1) if match else "Unknown Season"

            if league_name not in self.data:
                self.data[league_name] = {}
            self.data[league_name][season_name] = full_url

    def closed(self, reason):
        # Save the data to a JSON file when the spider is closed
        with open("domestic_leagues_data.json", "w") as f:
            json.dump(self.data, f, indent=4)
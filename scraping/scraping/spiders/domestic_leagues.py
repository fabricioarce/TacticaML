import scrapy
import json
import re

class DomesticLeaguesSpider(scrapy.Spider):
    name = "domestic-leagues"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/comps"]

    # Define the data structure to hold the league data
    div_categories = {
        5: "Club International Cups",
        6: "National Team Competitions",
        9: "Domestic Leagues - 1st Tier",
        10: "Domestic Leagues - 2nd Tier",
        12: "Domestic Leagues - 3rd Tier and Lower",
        13: "National Team Qualification",
        14: "Domestic Cups",
        15: "Domestic Youth Leagues"
    } 

    def __init__(self, *args, **kwargs):
        # Initialize the spider with an empty data structure
        self.data = {}

    def parse(self, response):
        # Extract the div indices for the categories we are interested in
        for idx, category in self.div_categories.items():
            xpath = f"/html/body/div[1]/div[5]/div[{idx}]/div[2]/table/tbody/tr"
            rows = response.xpath(xpath)
            for row in rows:
                gender = row.xpath("./td[1]/text()").get()
                if gender == 'M':
                    league_link = row.xpath(".//th/a/@href").get()
                    league_name = row.xpath(".//th/a/text()").get()

                    yield response.follow(
                        url=league_link,
                        callback=self.leagues_seasons,
                        meta={"league_name": league_name, "category": category}
                    )

    def leagues_seasons(self, response):
        league_name = response.meta["league_name"]
        category = response.meta["category"]
        season_links = response.xpath("/html/body/div[1]/div[6]/div[2]/div[2]/table/tbody/tr/th")

        # Iterate through each season link
        for season_link in season_links:
            # Extract the season URL
            season_url = season_link.xpath("./a/@href").get()
            full_url = response.urljoin(season_url)

            # Extract the season from the URL
            match = re.search(r'/(\d{4}-\d{2})', season_url)
            season_name = match.group(1) if match else "Unknown Season"

        if country not in self.data:
            self.data[country] = {}
        if league_name not in self.data[country]:
            self.data[country][league_name] = {"seasons": {}}
        self.data[country][league_name]["seasons"][season_name] = full_url

    def closed(self, reason):
        # Save the data to a JSON file when the spider is closed
        with open("/data/domestic_leagues_data.json", "w") as f:
            json.dump(self.data, f, indent=4)
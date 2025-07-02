import scrapy
import json
import re

class DomesticLeaguesSpider(scrapy.Spider):
    """
    A Scrapy spider that crawls fbref.com to collect URLs for various football league seasons.
    It organizes the data by country, league, and season, then saves it to a JSON file.
    """
    name = "domestic-leagues"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/comps"]

    # A dictionary mapping div indices on the page to their corresponding competition category.
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
        """Initializes the spider, creating an empty dictionary to store the scraped data."""
        super().__init__(*args, **kwargs)
        # Initialize the main data structure to hold all scraped information.
        self.data = {}

    def parse(self, response):
        """
        The main parsing method. It iterates through predefined categories, finds male competitions,
        and follows the links to their respective pages.
        """
        # Iterate through the categories defined in div_categories.
        for idx, category in self.div_categories.items():
            xpath = f"/html/body/div[1]/div[5]/div[{idx}]/div[2]/table/tbody/tr"
            rows = response.xpath(xpath)
            for row in rows:
                # Check the gender column to filter for male leagues ('M').
                gender = row.xpath("./td[1]/text()").get()
                if gender == 'M':
                    league_link = row.xpath(".//th/a/@href").get()
                    league_name = row.xpath(".//th/a/text()").get()
                    
                    # Follow the link to the league's page.
                    yield response.follow(
                        url=league_link,
                        callback=self.leagues_seasons,
                        meta={"league_name": league_name, "category": category}
                    )

    def leagues_seasons(self, response):
        """
        Parses a league's main page to find links to all its past and current seasons.
        It extracts the country, league name, season name, and the URL for that season.
        """
        # Retrieve metadata passed from the parse method.
        league_name = response.meta["league_name"]
        category = response.meta["category"]
        
        # Find all table rows that contain links to seasons.
        season_links = response.xpath("/html/body/div[1]/div[6]/div[2]/div[2]/table/tbody/tr/th")

        # Extract the country of the league.
        country = response.xpath("/html/body/div[1]/div[3]/div[1]/div[2]/p[1]/a/text()").get()

        # Iterate through each season link found.
        for season_link in season_links:
            season_url = season_link.xpath("./a/@href").get()
            if not season_url:
                continue
            
            full_url = response.urljoin(season_url)

            # Extract the season year (e.g., '2023-2024') from the URL using regex.
            match = re.search(r'/(\d{4}-\d{4}|\d{4})/', full_url)
            season_name = match.group(1) if match else "Unknown Season"

            # Populate the data dictionary with the structured information.
            if country not in self.data:
                self.data[country] = {}
            if league_name not in self.data[country]:
                self.data[country][league_name] = {"seasons": {}}
            self.data[country][league_name]["seasons"][season_name] = full_url

    def closed(self, reason):
        """
        This method is called when the spider has finished crawling.
        It saves the collected data into a JSON file.
        """
        # Write the final data dictionary to a JSON file.
        with open("domestic_leagues_data.json", "w") as f:
            json.dump(self.data, f, indent=4)
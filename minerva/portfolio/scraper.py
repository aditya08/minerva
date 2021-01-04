from bs4 import BeautifulSoup
import requests
import json
import time
import importlib.resources

class Scraper(object):
    def __init__(self, source='google'):
        self.source = source
        self.baseurl = ''
        self.delimiter = ''
        self.exchange = ''
        with importlib.resources.path("minerva.portfolio", "_scraper_assets.json") as fp:
            with open(fp) as f:
                scraper_assets = json.load(f)
        if (self.source == 'google'):
            self.baseurl = scraper_assets['scraper_googlefinance_baseurl']
        elif (self.source == 'yahoo'):
            self.baseurl = scraper_assets['scraper_yahoofinance_baseurl']

    def quote(self, ticker):
        url = self.baseurl+ticker.upper()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        if self.source == 'google':
            data = soup.find("div", class_='eYanAe')
            keys = [x.get_text() for x in data.find_all("div", class_='iYuiXc')]
            vals = [x.get_text() for x in  data.find_all("div", class_='P6K39c')]
            data = dict(zip(keys, vals))
            return data
        elif self.source == 'yahoo':
            #TODO
            raise NotImplementedError("yahoo scraping is not implemented yet.")
        else:
            raise ValueError("Scraping source must be 'google' or 'yahoo'. Got {} instead.".format(self.source))
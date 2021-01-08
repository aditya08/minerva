from bs4 import BeautifulSoup
import requests
import json
import re
import importlib.resources


class Scraper(object):
    def __init__(self, source='google'):
        self.source = source.lower()
        self.baseurl = ''
        self.delimiter = ''
        self.exchange = ''
        with importlib.resources.path("minerva.portfolio",
             "_scraper_assets.json") as fp:
            with open(fp) as f:
                scraper_assets = json.load(f)
        if (self.source == 'google'):
            self.baseurl = scraper_assets['scraper_googlefinance_baseurl']
        elif (self.source == 'yahoo'):
            self.baseurl = scraper_assets['scraper_yahoofinance_baseurl']
        else:
            raise ValueError("source must be 'google'"
                  + " or 'yahoo'. Instead got {}".format(self.source))

    def quote(self, ticker):
        if ticker == '':
            raise ValueError("'ticker' cannot be an empty string")
        url = self.baseurl+ticker.upper()
        if self.source == 'google':
            if re.search("[a-zA-Z0-9]:[a-zA-Z0-9]", ticker) is None:
                raise ValueError("Google ticker must follow the format "
                      + "<ticker>:<exchange>")
            return self._scrape_google_finance(url)
        elif self.source == 'yahoo':
            return self._scrape_yahoo_finance(url)
        else:
            raise ValueError("Scraping source must be 'google' or 'yahoo'."
                  + "Got {} instead.".format(self.source))

    def _scrape_google_finance(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        close = soup.find("div", class_="YMlKec fxKbKc")
        if close is None:
            raise TypeError("Quote returned 'NoneType'"
                  + "for the ticker specified.")

        keys = ['Close']
        vals = [close.get_text()]
        data = soup.find("div", class_='eYanAe')
        keys += [x.get_text() for x in data.find_all("div", class_='iYuiXc')]
        vals += [x.get_text() for x in data.find_all("div", class_='P6K39c')]
        data = dict(zip(keys, vals))
        return data

    def _scrape_yahoo_finance(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        close = soup.find("span",
                          class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
        if close is None:
            raise TypeError("Quote returned 'NoneType'"
                  + " for the ticker specified.")
        keys = ['Close']
        vals = [close.text]
        data = soup.find("div", {'id': 'quote-summary'})
        data = [x.get_text() for x in data.find_all("td")]
        keys += data[::2]
        vals += data[1::2]
        data = dict(zip(keys, vals))
        return data

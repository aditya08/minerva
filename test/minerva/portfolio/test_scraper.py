from minerva.portfolio.scraper import Scraper
from minerva.portfolio.fund import Fund

def test_scraper_yahoo():
    yahoo_scraper = Scraper('yahoo')
    data = yahoo_scraper.quote('VTI')
    assert data != None, "Should not be 'None'."

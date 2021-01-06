from minerva.portfolio.scraper import Scraper
from minerva.portfolio.fund import Fund

def test_scraper_yahoo():
    yahoo_scraper = Scraper('yahoo')
    data = yahoo_scraper.quote('VTI')
    assert data != None, "Should not be 'None'."
    assert float(data['Close'].strip('$')) > 0, "Should be > 0."

def test_scraper_google():
    google_scraper = Scraper('google')
    data = google_scraper.quote('VTI:NYSEARCA')
    assert data != None, "Should not be 'None'."
    assert float(data['Close'].strip('$')) > 0, "Should be > 0."
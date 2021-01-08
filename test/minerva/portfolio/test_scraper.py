from minerva.portfolio.scraper import Scraper


def test_scraper_yahoo():
    yahoo_scraper = Scraper('yahoo')
    data = yahoo_scraper.quote('VTI')
    assert data is not None, "Should not be 'None'."
    assert float(data['Close'].replace('$', '').replace(',', '')) > 0,\
           "Should be > 0."


def test_scraper_google():
    google_scraper = Scraper('google')
    data = google_scraper.quote('VTI:NYSEARCA')
    assert data is not None, "Should not be 'None'."
    assert float(data['Close'].replace('$', '').replace(',', '')) > 0,\
           "Should be > 0."

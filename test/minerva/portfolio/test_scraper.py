from minerva.portfolio.scraper import Scraper
import pytest


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


def test_scraper_badinitargs():
    with pytest.raises(ValueError):
        scraper = Scraper('')
        scraper = Scraper('asfjads;f')
    scraper = Scraper('YAhoo')
    assert scraper.baseurl != '', "Should not be empty."
    scraper = Scraper('GooGLE')
    assert scraper.baseurl != '', 'Should not be empty.'


def test_scraper_badquoteargs():
    yahoo_scraper = Scraper('yahoo')
    google_scraper = Scraper('google')
    with pytest.raises(ValueError):
        yahoo_scraper.quote('')
        google_scraper.quote('')
    with pytest.raises(TypeError):
        yahoo_scraper.quote('asdfdsaf')
        google_scraper.quote('asdfadf')
        google_scraper.quote(':adfa')
        google_scraper.quote('adfad:')

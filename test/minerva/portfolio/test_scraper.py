from minerva.portfolio.scraper import Scraper
from minerva.portfolio.fund import Fund

google_scraper = Scraper('google')
google_scraper.quote('AAPL:NASDAQ')
google_scraper.quote('VTI:NYSEARCA')
google_scraper.quote('VTSAX:MUTF')

vti = Fund('VTI:NYSEARCA', 10, 10.4, 0.03, 'domestic', 'Total Market Fund')


from minerva.portfolio.asset import Asset
from minerva.portfolio.scraper import Scraper

class Stock(Asset):
    def __init__(self, ticker, quantity, basis, sector, description):
        self.ticker = ticker.lower()
        self.quantity = quantity
        self.basis = basis
        self.sector = sector
        self.description = description
        scraper = Scraper()
        quote = scraper.quote(ticker)
        self.price = float(quote['Close'].strip('$'))

    def update_quantity(self, quantity):
        if quantity > 0:
            self.quantity = quantity
        else:
            raise ValueError('quantity must be > 0 but got {}'.format(quantity))

    def update_basis(self, basis):
        if basis > 0.:
            self.basis = basis
        else:
            raise ValueError('basis must be > 0. but got {}'.format(basis))
    
    def update_price(self, price):
        if price > 0.:
            self.price = price
        else:
            raise ValueError('price must be > 0. but got {}'.format(price))
    
    def update_sector(self, sector):
        if len(sector) > 0:
            self.sector = sector
        else:
            raise ValueError('got empty string for sector')
    
    def update_description(self, description):        
        if len(description) > 0:
            self.description = description
        else:
            raise ValueError('got empty string for description')

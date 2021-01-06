from minerva.portfolio.asset import Asset
from minerva.portfolio.scraper import Scraper

class Fund(Asset):
    def __init__(self, ticker, quantity, basis, expense_ratio, sector, description):
        self.ticker = ticker
        self.update_quantity(quantity)
        self.update_basis(basis)
        self.price = -1
        self.update_expense_ratio(expense_ratio)
        self.update_sector(sector)
        self.update_description(description)
        scraper = Scraper()
        quote = scraper.quote(ticker)
        self.price = float(quote['Close'].replace('$', '').replace(',', ''))

    def update_price(self, price):
        if price > 0.:
            self.price = price
        else:   
            raise ValueError('price must be > 0. but got {}'.format(price))

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

    def update_expense_ratio(self, expense_ratio):
        if isinstance(expense_ratio, str):
            expense_ratio = float(expense_ratio.strip('%'))/100
        elif isinstance(expense_ratio, float):
            pass
        else:
            raise TypeError("expense_ratio must be of type str or float. Instead got {}".format(type(expense_ratio)))
        if expense_ratio > 0.:
            self.expense_ratio = expense_ratio
        else:
            raise ValueError('expense_ratio must be > 0. but got {}'.format(expense_ratio))
    
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

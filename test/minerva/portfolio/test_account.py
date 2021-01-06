from minerva.portfolio.account import Account
from minerva.portfolio.stock import Stock
from minerva.portfolio.fund import Fund
import pytest

def test_account_creation():
    aapl = Stock('AAPL:NASDAQ', 1, 131.10, 'Technology', 'Apple Inc.')
    abv = Stock('ABBV:NYSE', 2, 105.5, 'Pharma', 'AbbVie Inc.')
    fxnax = Fund('FXNAX:MUTF', 5.2, 12.2, '0.03%', 'US Total Bond', 'US Total Bond Market Index Fund')
    vti = Fund('VTI:NYSEARCA', 10, 130.1, '0.03%', 'US Total Market', 'US Total Stock Market Index Fund')
    assets = [aapl, fxnax, abv, vti]
    acct = Account('Roth IRA', assets)
    assert acct.name == 'Roth IRA', "Should be 'Roth IRA'."
    assert acct.assets == assets, "Should be the list of assets."
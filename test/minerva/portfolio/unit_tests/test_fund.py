from minerva.portfolio.fund import Fund
from minerva.portfolio.scraper import Scraper
import pytest


def test_etf_creation():
    vti = Fund('VTI:NYSEARCA', 10, 139.50, 0.0003,
               "US Total Market", "Vanguard US Total Market ETF")
    scraper = Scraper()
    price = float(scraper.quote('vti:nysearca')['Close'].strip('$'))
    assert vti.ticker == 'VTI:NYSEARCA', "Should be VTI:NYSEARCA."
    assert vti.quantity == 10, "Should be 10."
    assert vti.basis == 139.50, "Should be 139.50."
    assert vti.expense_ratio == 0.0003, "Should be 0.0003."
    assert vti.sector == 'US Total Market', "Should be 'US Total Market'"
    assert vti.description == 'Vanguard US Total Market ETF', \
                              "Should be 'Vanguard US Total Market ETF'"
    print(vti.price)
    assert vti.price == price, "Should be {}.".format(price)
    assert vti.value == 10*price, "Should be {}.".format(10*price)


def test_mutualfund_creation():
    vti = Fund('VTSAX:MUTF', 10, 139.50, 0.0003, "US Total Market",
               "Vanguard US Total Market Index Fund")
    scraper = Scraper()
    price = float(scraper.quote('vtsax:mutf')['Close'].strip('$'))
    assert vti.ticker == 'VTSAX:MUTF', "Should be VTSAX:MUTF."
    assert vti.quantity == 10, "Should be 10."
    assert vti.basis == 139.50, "Should be 139.50."
    assert vti.expense_ratio == 0.0003, "Should be 0.0003."
    assert vti.sector == 'US Total Market', "Should be 'US Total Market'"
    assert vti.description == 'Vanguard US Total Market Index Fund', \
                              "Should be 'Vanguard US Total Market Index Fund'"
    assert vti.price == price, "Should be > 0."
    assert vti.value == price*10, "Should be {}".format(price*10)


def test_fund_expense_ratio_type():
    vti = Fund('VTSAX:MUTF', 10, 139.50, "0.03%", "US Total Market",
               "Vanguard US Total Market ETF")
    assert vti.expense_ratio == 0.0003, "Should be 0.0003"
    with pytest.raises(TypeError):
        vti = Fund('VTSAX:MUTF', 10, 139.50, 3, "US Total Market",
                   "Vanguard US Total Market ETF")


def test_fund_update_methods():
    # test success
    vti = Fund('VTI:NYSEARCA', 10, 139.50, "0.03%", "US Total Market",
               "Vanguard US Total Market ETF")
    vti.update_basis(100)
    assert vti.basis == 100, "Should be 100."
    vti.update_price(100)
    assert vti.price == 100, "Should be 100."
    assert vti.value == 100*10, "Should be 1000."
    vti.update_expense_ratio(0.3)
    assert vti.expense_ratio == 0.3, "Should be 0.3."
    vti.update_sector('Testing')
    assert vti.sector == 'Testing', "Should be 'Testing'."
    vti.update_description('This is a test')
    assert vti.description == 'This is a test', "Should be 'This is a test'."
    # test exception raised
    with pytest.raises(ValueError):
        vti.update_description('')
    with pytest.raises(ValueError):
        vti.update_sector('')
    with pytest.raises(ValueError):
        vti.update_basis(0)
    with pytest.raises(ValueError):
        vti.update_basis(-1)
    with pytest.raises(ValueError):
        vti.update_quantity(0)
    with pytest.raises(ValueError):
        vti.update_quantity(-1)
    with pytest.raises(ValueError):
        vti.update_price(0)
    with pytest.raises(ValueError):
        vti.update_price(-1)
    with pytest.raises(ValueError):
        vti.update_expense_ratio(-1.)
    with pytest.raises(ValueError):
        vti.update_expense_ratio("-0.03%")

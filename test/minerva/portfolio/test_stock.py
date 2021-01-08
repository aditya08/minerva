from minerva.portfolio.stock import Stock
from minerva.portfolio.scraper import Scraper
import pytest


def test_stock_creation():
    aapl = Stock('AAPL:NASDAQ', 10, 200, 'Technology', 'Apple Inc.')
    scraper = Scraper()
    quote = scraper.quote('AAPL:NASDAQ')
    price = float(quote['Close'].strip('$'))
    assert aapl.price == price, "Should be {}.".format(price)
    assert aapl.quantity == 10, "Should be 10."
    assert aapl.basis == 200, "Should be 200."
    assert aapl.sector == 'Technology', "Should be 'Technology'."
    assert aapl.description == 'Apple Inc.', "Should be 'Apple Inc.'."
    assert aapl.value == 10*price, "Should be {}.".format(20*price)


def test_stock_malformed_args():
    with pytest.raises(TypeError):
        Stock('AAPLL:NASDAQ', 10, 200, 'Technology', 'Apple Inc.')


def test_stock_update_methods():
    goog = Stock('GOOG:NASDAQ', 1, 1000, 'Technology', 'Alphabet Inc.')
    goog.update_basis(1500)
    goog.update_description("Was Google Inc.")
    goog.update_price(100)
    goog.update_quantity(5)
    goog.update_sector('IT')
    assert goog.basis == 1500, "Should be 1500."
    assert goog.description == "Was Google Inc.",\
                               "Should be 'Was Google Inc.'."
    assert goog.price == 100, "Should be 100."
    assert goog.quantity == 5, "Should be 5."
    assert goog.sector == 'IT', "Should be 'IT'."
    assert goog.value == 100*5, "Should be {}.".format(100*5)

    with pytest.raises(ValueError):
        goog.update_basis(-1)
    with pytest.raises(ValueError):
        goog.update_basis(0)
    with pytest.raises(ValueError):
        goog.update_description('')
    with pytest.raises(ValueError):
        goog.update_price(-1)
    with pytest.raises(ValueError):
        goog.update_price(0)
    with pytest.raises(ValueError):
        goog.update_quantity(0)
    with pytest.raises(ValueError):
        goog.update_quantity(-1)
    with pytest.raises(ValueError):
        goog.update_sector('')

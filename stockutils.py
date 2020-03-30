import yfinance as yf
import math
def stock_price(ticker):
    if len(ticker) == 1:
        tickerdf = yf.Ticker(ticker[0])
        data = tickerdf.history(period='1d')
        return {ticker[0] : data['Close'][0]}
    else:
        tickerdf = yf.Tickers(ticker)
        data = tickerdf.history(period='1d')
        quote_dict = {}
        for symb in ticker:
            price = data['Close'][symb][0]
            if not math.isnan(price):
                quote_dict[symb] = price
            else:
                print('Caution: Some tickers were not found and are not include in returned dictionary')
        return quote_dict
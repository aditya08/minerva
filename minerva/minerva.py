import argparse
import pandas as pd
import numpy as np
import stockutils as stk
parser = argparse.ArgumentParser()
parser.add_argument('--ticker',
                    type=str, nargs='+',
                    help='Ticker symbol of the securities to add/remove/update in the existing portfolio'
                    )
parser.add_argument('--buy',
                    action='store_true',
                    help='Buy shares of security specified by ticker symbol.'
                    )
parser.add_argument('--sell',
                    action='store_true',
                    help='Sell shares of security specified by ticker symbol.'
                    )
parser.add_argument('--quantity',
                    type=float,
                    help='specify the quantity of shares for the specified ticker.'
                    )
parser.add_argument('--price',
                    type=float,
                    help='specify the price of shares for the specified ticker.')
parser.add_argument('--summarize',
                    action = 'store_true',
                    help = 'Display a summary of the portfolio.')
parser.add_argument('--update-portfolio',
                    action = 'store_true',
                    help = 'Update the portfolio based on current market prices.')
args = parser.parse_args()

print(stk.stock_price([symb.upper() for symb in args.ticker]))
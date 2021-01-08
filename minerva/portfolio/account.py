from minerva.portfolio.stock import Stock
from minerva.portfolio.fund import Fund
from minerva.portfolio.asset import Asset
from minerva.portfolio.scraper import Scraper
import json
import pickle


class Account(object):
    def __init__(self, name, assets=[]):
        """An Account object that contains a list of Assets (e.g. Stocks, Funds).
        Typically, this class will represent the various Assets
        held in Brokerages, IRAs, and Retirement Accounts (401k, 403b, etc.).

        Args:
            name (str): Name of the account.
            assets (list, optional): List of assets to add to account.
            Defaults to [].
        """
        self.name = name
        self.value = 0
        self.assets = []
        self.weights = []
        if len(assets) > 0:
            self.assets += assets
            self.update_weights()
            self.update_value()

    def __len__(self):
        return len(self.assets)

    def __str__(self):
        acct_str = self.name + ': ' + len(self.assets) + ' assets\n'
        acct_str += '----------------------------------------------'
        for asset in self.assets:
            acct_str += asset.ticker + '- [quantity]: ' + asset.quantity \
                        + ' [price]: ' + asset.price + ' [basis]: ' \
                        + asset.basis + '\n'
        return acct_str

    def __repr__(self):
        # TODO: Complete repr string
        return ''

    def __iadd__(self, other):
        if isinstance(other, Asset):
            idx = [asset.ticker for asset in self.assets] \
                  .index(other.ticker.lower())
            self._buy_asset(idx, other)
        elif isinstance(other, Account):
            self.buy_assets(assets=other.assets)
        elif isinstance(other, list):
            self.buy_assets(assets=other)
        else:
            raise TypeError('unexpected type {} found.'.format(type(other)))
        self.update()
        return self

    def __isub__(self, other):
        if isinstance(other, Asset):
            idx = [asset.ticker for asset in self.assets] \
                 .index(other.ticker.lower())
            self._sell_asset(idx, other)
        elif isinstance(other, Account):
            self.sell_assets(assets=other.assets)
        elif isinstance(other, list):
            self.sell_assets(assets=other)
        else:
            raise TypeError('unexpected type {} found.'.format(type(other)))
        self.update()
        return self

    def save(self, path):
        """Saves a pickled Account object to the filesystem (at the path provided).

        Args:
            path (str): Path where to save the pickled Account object.
        """
        if len(path) < 1:
            path = './' + self.name + '.mrva'
        pickle.dump(self, open(path, "wb"))

    def buy_assets(self, assets=[], path='', replace=False):
        """Adds Assets to the Account object. The new Assets can be provided as a list
        through `assets` arg or as a json file through the `path` arg.
        Mixing of the two input args is allowed. If the `replace` flag is True,
        then existing Assets in the Account object are overwritten.
        If False, then existing Assets are modified by adding quantities and
        by adjusting the cost basis.

        Args:
            assets (list, optional): A list of Assets (e.g. Stocks, Funds).
            Defaults to [].
            path (str, optional): path to a json file containing Assets.
            Defaults to ''.
            replace (bool, optional): If True, existing Asset will be
            overwritten. Otherwise, existing Asset will be modified to
            reflect the additional quantity and computes a new cost
            basis. Defaults to False.

        Raises:
            ValueError: If path or assets args are improperly specified.
        """
        if len(path) == 0 and len(assets) == 0:
            raise ValueError('assets or path must be non-empty.')
        if len(assets) > 0:
            # add assets from input list
            self._buy_assets_from_list(assets, replace=replace)
        if len(path) > 0:
            # add assets from input path
            self._buy_assets_from_path(path, replace=replace)
        # update prices
        self.update()

    def _buy_assets_from_list(self, assets, replace=False):
        existing_tickers = [asset.ticker for asset in self.assets]
        for asset in assets:
            if not isinstance(asset, Asset):
                raise TypeError('unexpected type {} found for asset.'
                      .format(type(asset)))
            if asset.ticker.lower() in existing_tickers:
                idx = existing_tickers.index(asset.ticker.lower())
                self._buy_asset(idx, asset, replace=replace)
            else:
                # ticker is new and not in self.assets
                self.assets.append(asset)
                existing_tickers.append(asset.ticker.lower())

    def _buy_assets_from_path(self, path, replace=False):
        with open(path) as fp:
            # parse assets from json
            lines = json.load(fp)
            # return list of assets
            assets = self._parse_assets(lines)
        self._buy_assets_from_list(assets, replace=replace)

    def _buy_asset(self, idx, asset, replace=False):
        if asset.quantity <= 0:
            raise ValueError('quantity must be > 0 but got {} for {}'
                             .format(asset.quantity, asset.ticker))
        found_asset = self.assets[idx]
        if type(found_asset) != type(asset):
            raise TypeError('type mismatch for asset {}'.format(asset.ticker))
        if not replace:
            adj_quantity = found_asset.quantity + asset.quantity
            adj_basis = (found_asset.quantity*found_asset.basis +
                         asset.quantity*asset.basis)/adj_quantity
        else:
            adj_quantity = asset.quantity
            adj_basis = asset.basis
        found_asset.update_quantity(adj_quantity)
        found_asset.update_basis(adj_basis)
        if isinstance(found_asset, Fund) and replace:
            # for Funds update expense ratio, sector, and description
            found_asset.update_expense_ratio(asset.expense_ratio)
            found_asset.update_sector(asset.sector)
            found_asset.update_description(asset.description)

    def sell_assets(self, assets=[], path=''):
        """[summary]

        Args:
            assets (list, optional): [description]. Defaults to [].
            path (str, optional): [description]. Defaults to ''.

        Raises:
            ValueError: [description]
        """
        if len(path) == 0 and len(assets) == 0:
            raise ValueError('assets or path must be non-empty.')
        if len(assets) > 0:
            # add assets from input list
            self._sell_assets_from_list(assets)
        if len(path) > 0:
            # add assets from input path
            self._sell_assets_from_path(path)
        # update prices
        self.update()

    def _sell_assets_from_list(self, assets):
        existing_tickers = [asset.ticker for asset in self.assets]
        for asset in assets:
            if not isinstance(asset, Asset):
                raise TypeError('unexpected type {} found for asset.'
                      .format(type(asset)))
            if asset.ticker.lower() in existing_tickers:
                idx = existing_tickers.index(asset.ticker.lower())
                self._sell_asset(idx, asset)
            else:
                print('Ticker {} not found. Skipping...'
                      .format(asset.ticker))

    def _sell_assets_from_path(self, path):
        with open(path) as fp:
            lines = json.load(fp)
        assets = self._parse_assets(lines)
        self._sell_assets_from_list(assets)

    def _sell_asset(self, idx, asset):
        if asset.quantity <= 0:
            raise ValueError('quantity must be > 0 but got {} for {}.'
                             .format(asset.quantity, asset.ticker))
        found_asset = self.assets[idx]
        if type(found_asset) != type(asset):
            raise TypeError('type mismatch for asset {}'.format(asset.ticker))
        if found_asset.quantity < asset.quantity:
            raise ValueError('quantity ({}) to sell exceedes '
                             .format(asset.quantity) +
                             'quantity ({}) available in account.'
                             .format(found_asset.quantity))
        adj_quantity = found_asset.quantity - asset.quantity
        adj_basis = (found_asset.quantity*found_asset.basis -
                     asset.quantity*asset.basis)/adj_quantity
        if adj_basis < 0:
            raise ValueError(
                  'basis of selling asset exceeds basis in account.')
        found_asset.update_quantity(adj_quantity)
        found_asset.update_basis(adj_basis)

    def remove_assets(self, tickers=[]):
        if len(tickers) == 0:
            return
        existing_tickers = [asset.ticker for asset in self.assets]
        for ticker in tickers:
            try:
                idx = existing_tickers.index(ticker)
                del self.assets[idx]
            except IndexError:
                print('Ticker {} not found. Skipping...'.format(ticker))

    def update(self):
        scraper = Scraper()
        for asset in self.assets:
            # update price of each asset with current closing price
            price = float(scraper.quote(asset.ticker)['Previous close']
                          .strip('$'))
            asset.update_price(price)
        self.update_weights()

    def update_weights(self):
        self.weights = []
        asset_values = [asset.price*asset.quantity for asset in self.assets]
        value = sum(asset_values)
        for v in asset_values:
            self.weights.append(v/value)

    def update_value(self):
        self.value = 0
        for asset in self.assets:
            self.value += asset.value

    def _parse_assets(self, lines):
        assets = []
        for idx in lines:
            asset = lines[idx]
            assets.append(self._create_new_asset_from_dict(asset))
        return assets

    def _create_new_asset_from_dict(self, asset):
        if asset['type'].lower() == 'stock':
            # Create new Stock instance with values from json file
            item = Stock(asset['ticker'], asset['quantity'], asset['basis'],
                         sector=asset['sector'],
                         description=asset['description'])
        elif asset['type'].lower() == 'fund':
            # Create new Fund instance with values from json file
            item = Fund(asset['ticker'], asset['quantity'], asset['basis'],
                        asset['expense_ratio'], asset['sector'],
                        asset['description'])
        else:
            raise ValueError("Unsupported 'type' {} found."
                             .format(asset['type']))
        return item

    def asset_sectors(self):
        asset_sectors = []
        for asset in self.assets:
            asset_sectors.append(asset.sector)

    def asset_weights(self):
        return self.weights

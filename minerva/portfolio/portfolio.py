from .account import Account
import pickle


class Portfolio(object):
    def __init__(self, name=''):
        self.name = name
        self.accounts = []
        self.weights = []
        self.value = 0

    def __len__(self):
        return len(self.accounts)

    def __str__(self):
        port_str = self.name + ': ' + len(self.accounts) + ' accounts\n'
        port_str += '---------------------------------------------------'
        for acct in self.accounts:
            port_str += str(acct)
        return port_str

    def __repr__(self):
        return ''

    def __add__(self, other):
        return 0

    def save(self, path=''):
        if len(path) < 1:
            path = './' + self.name + '.mrva'
        pickle.dump(self, open(path, "wb"))

    def update(self):
        for acct in self.accounts:
            acct.update()
        self.update_weights()

    def update_weights(self):
        self.weights = []
        acct_values = [acct.value for acct in self.accounts]
        self.value = sum(acct_values)
        for acct_value in acct_values:
            self.weights.append(acct_value/self.value)

    def asset_sectors(self):
        asset_sectors = []
        for account in self.accounts:
            asset_sectors.append(account.asset_sectors())
        return asset_sectors

    def asset_weights(self):
        asset_weights = []
        for i, account in enumerate(self.accounts):
            asset_weights.append(self.weights[i]*account.asset_weights())
        return asset_weights

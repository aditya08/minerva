from minerva.portfolio.portfolio import Portfolio
import bokeh


class Visualize(object):
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def build(self):
        return

    def _category_donut(self):
        categories = self.portfolio.asset_categories()
        weights = self.portfolio.asset_weights()
        weights *= 100
        plt = ""
        return plt

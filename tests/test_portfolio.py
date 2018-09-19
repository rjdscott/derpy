# -*- coding: utf-8 -*-

from derpy import portfolio
import pandas as pd


class TestPortfolio:

    def test_portfolio(self):
        securities = ['AAA', 'BBB']
        positions = [[11, 10], [12, 10], [13, 10]]
        prices = [[10, 10], [11, 10], [12, 10]]
        dates = ['2018-07-01', '2018-08-01', '2018-09-01']

        df_positions = pd.DataFrame(data=positions, columns=securities, index=dates)
        df_prices = pd.DataFrame(data=prices, columns=securities, index=dates)
        df_values = df_positions * df_prices

        p = portfolio.Portfolio()


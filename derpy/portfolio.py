#!/usr/bin/env python
# -*- coding: utf-8 -*-

# future proof py2 vs py3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import numpy as np


class Portfolio(object):

    def __init__(self, names, positions, prices):
        self.sec_names = names
        self.positions = positions
        self.prices = prices

    def sec_values(self):
        return self.positions * self.prices

    def sec_weights(self):
        sec_vals = self.sec_values()
        return sec_vals.divide(sec_vals.sum(axis='columns'), axis='rows')

    def portfolio_value(self):
        sec_vals = self.sec_values()
        return pd.DataFrame(sec_vals.sum(axis=1), columns=['value'])

    def portfolio_returns(self):
        port_val = self.portfolio_value()
        port_val['simple_ret'] = port_val['value'].pct_change()
        port_val['log_ret'] = np.log(port_val['value']) - np.log(port_val['value'].shift(1))
        return port_val


if __name__ == '__main__':
    securities = ['AAA', 'BBB']
    positions = [[11, 10], [12, 10], [13, 10], [13, 11], [13, 12]]
    prices = [[10, 10], [11, 10], [12, 10], [12, 10], [12, 10]]
    dates = ['2018-07-01', '2018-08-01', '2018-09-01', '2018-10-01', '2018-11-01']

    df_positions = pd.DataFrame(data=positions, columns=securities, index=dates)
    df_prices = pd.DataFrame(data=prices, columns=securities, index=dates)

    qf = Portfolio(names=securities, positions=df_positions, prices=df_prices)

    print(qf.sec_values())
    print('-----')
    print(qf.sec_weights())
    print('-----')
    print(qf.portfolio_value())
    print('-----')
    print(qf.portfolio_returns())

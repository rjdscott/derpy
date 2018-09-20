#!/usr/bin/env python
# -*- coding: utf-8 -*-

# future proof py2 vs py3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from derpy import portfolio as pt
import pandas as pd
import unittest


class TestQuickFolio(unittest.TestCase):

    def test_portfolio(self):
        securities = ['AAA', 'BBB']
        positions = [[11, 10]]
        prices = [[10, 10]]
        dates = ['2018-07-01']
        df_positions = pd.DataFrame(data=positions, columns=securities, index=dates)
        df_prices = pd.DataFrame(data=prices, columns=securities, index=dates)
        port = pt.Portfolio(names=securities, positions=df_positions, prices=df_prices)

        self.assertAlmostEqual(port.sec_names, securities)


if __name__ == '__main__':
    unittest.main()

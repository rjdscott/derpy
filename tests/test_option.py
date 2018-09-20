#!/usr/bin/env python
# -*- coding: utf-8 -*-

# future proof py2 vs py3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
from derpy import option


class TestOption(unittest.TestCase):

    def test_bsm_euro_call(self):
        opt = option.Option(strike=10, underlying=16, time_to_mat=60, volatility=0.16, interest_rate=0.02)
        opt_px = opt.option_price(opt_type='e', call_put='c', px_method='bsm')
        opt_expected = 13.29762576988012
        self.assertAlmostEqual(opt_px, opt_expected)

    def test_binomial_euro_call(self):
        opt = option.Option(strike=10, underlying=16, time_to_mat=60, volatility=0.16, interest_rate=0.02)
        opt_px = opt.option_price(opt_type='e', call_put='c', px_method='binomial')
        opt_expected = 13.300074416857715
        self.assertAlmostEqual(opt_px, opt_expected)

    def test_binomial_euro_put(self):
        opt = option.Option(strike=10, underlying=16, time_to_mat=60, volatility=0.16, interest_rate=0.02)
        opt_px = opt.option_price(opt_type='e', call_put='p', px_method='binomial')
        opt_expected = 0.3120165359797314
        self.assertAlmostEqual(opt_px, opt_expected)

    def test_bsm_euro_put(self):
        opt = option.Option(strike=10, underlying=16, time_to_mat=60, volatility=0.16, interest_rate=0.02)
        opt_px = opt.option_price(opt_type='e', call_put='p', px_method='bsm')
        opt_expected = 0.3095678890021424
        self.assertAlmostEqual(opt_px, opt_expected)

    def test_binomial_amer_call(self):
        opt = option.Option(strike=10, underlying=16, time_to_mat=60, volatility=0.16, interest_rate=0.02)
        opt_px = opt.option_price(opt_type='a', call_put='c', px_method='binomial')
        opt_expected = 13.300074416857715
        self.assertAlmostEqual(opt_px, opt_expected)

    def test_binomial_amer_put(self):
        opt = option.Option(strike=10, underlying=16, time_to_mat=60, volatility=0.16, interest_rate=0.02)
        opt_px = opt.option_price(opt_type='a', call_put='p', px_method='binomial')
        opt_expected = 0.3120165359797314
        self.assertAlmostEqual(opt_px, opt_expected)


if __name__ == '__main__':
    unittest.main()

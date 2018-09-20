#!/usr/bin/env python
# -*- coding: utf-8 -*-

# future proof py2 vs py3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from derpy import option_binomial as bn
from derpy import option_bsm as bsm


class Option:

    def __init__(self, strike, underlying, time_to_mat, volatility, interest_rate):
        self.strike = strike
        self.underlying = underlying
        self.time_to_mat = time_to_mat
        self.volatility = volatility
        self.interest_rate = interest_rate

    def option_price(self, opt_type='euro', call_put='call', px_method='bsm', step=10):
        if opt_type in ['e', 'european', 'euro']:
            if px_method in ['bsm', 'black']:

                opt_px = bsm.euro_option(call_put=call_put,
                                         stock_price=self.underlying,
                                         strike=self.strike,
                                         volatility=self.volatility,
                                         time_to_maturity=self.time_to_mat,
                                         interest_rate=self.interest_rate)

                return opt_px

            elif px_method in ['binomial']:
                opt_px = bn.binomial_option(flag='european',
                                            call_put=call_put,
                                            stock_price=self.underlying,
                                            strike=self.strike,
                                            volatility=self.volatility,
                                            time_to_maturity=self.time_to_mat,
                                            interest_rate=self.interest_rate,
                                            step=step)

                return opt_px
            else:
                raise ValueError("Pricing method: {} not supported".format(px_method))

        elif opt_type in ['a', 'american', 'amer']:
            if px_method in ['bsm', 'black']:
                raise ValueError("BSM American options not available.. please submit enhancement request..")

            elif px_method in ['binomial']:
                opt_px = bn.binomial_option(flag='european',
                                            call_put=call_put,
                                            stock_price=self.underlying,
                                            strike=self.strike,
                                            volatility=self.volatility,
                                            time_to_maturity=self.time_to_mat,
                                            interest_rate=self.interest_rate,
                                            step=step)
                return opt_px

            else:
                raise ValueError("Pricing method: {} not supported".format(px_method))

        else:
            ValueError("Option type not supported: {} not supported".format(px_method))

    def delta(self):
        pass

    def theta(self):
        pass

    def gamma(self):
        pass

    def rho(self):
        pass

    def implied_vol(self):
        pass


if __name__ == '__main__':
    opt = Option(strike=10, underlying=16, time_to_mat=60, volatility=0.16, interest_rate=0.02)
    print(opt.option_price(opt_type='e', call_put='c', px_method='bsm'))
    print(opt.option_price(opt_type='e', call_put='c', px_method='binomial'))
    print(opt.option_price(opt_type='a', call_put='p', px_method='binomial'))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# European option, Black - Scholes - Merton formula
# August 2018
# version 1.1
# --------------------------------------------------------

# future proof py2 vs py3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy.stats import norm
import numpy as np
import math


def option_pricing(func, args):
    """
    :param func: option or greeks pricing formula
    :param args: define all inputs once using an array,
                and call as one input argument
    :return: return values of the underlying functions

    @usage
    import black_scholes_merton as bsm

    # define input argument once
    args = ['c', 20, 21, 0.12, 2, 0.05] # div_yield is optional

    # call option_pricing wrapper function
    bsm.option_pricing(bsm.euro_option, args)
    """
    output = func(*args)
    return output


def euro_option(call_put,
                stock_price,
                strike,
                volatility,
                time_to_maturity,
                interest_rate,
                div_yield=0):
    """
    :param call_put: the type of European options
    :param stock_price: spot price of the underlying asset
    :param strike: strike price
    :param volatility: annual volatility of the underlying asset
    :param time_to_maturity: time to maturity expressed in years
    :param interest_rate: annual continuous interest rate
    :param div_yield: continuous dividend yield
    :return: european call option price
    """

    d1 = (math.log(stock_price / strike)
          + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    d2 = d1 - volatility * (time_to_maturity ** 0.5)

    call_price = stock_price * np.exp(-1 * div_yield * time_to_maturity) * norm.cdf(d1) \
                 - strike * np.exp(-1 * interest_rate * time_to_maturity) * norm.cdf(d2)

    put_price = strike * np.exp(-1 * interest_rate * time_to_maturity) * norm.cdf(-1 * d2) \
                - stock_price * np.exp(-1 * div_yield * time_to_maturity) * norm.cdf(-1 * d1)

    if call_put in ['c', 'C', 'call', 'Call', 'CALL']:
        return call_price
    elif call_put in ['p', 'P', 'put', 'Put', 'PUT']:
        return put_price
    else:
        return "Please specify option type"


def delta(call_put,
          stock_price,
          strike,
          volatility,
          time_to_maturity,
          interest_rate,
          div_yield=0):
    d1 = (math.log(stock_price / strike)
          + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    call_delta = norm.cdf(d1)

    put_delta = norm.cdf(d1) - 1

    if call_put in ['c', 'C', 'call', 'Call', 'CALL']:
        return call_delta
    elif call_put in ['p', 'P', 'put', 'Put', 'PUT']:
        return put_delta
    else:
        return "Please specify option type"


def gamma(call_put,
          stock_price,
          strike,
          volatility,
          time_to_maturity,
          interest_rate,
          div_yield=0):
    d1 = (math.log(stock_price / strike)
          + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    call_gamma = norm.pdf(d1) / (stock_price * volatility * (time_to_maturity ** (1 / 2)))

    put_gamma = norm.pdf(d1) / (stock_price * volatility * (time_to_maturity ** (1 / 2)))

    if call_put in ['c', 'C', 'call', 'Call', 'CALL']:
        return call_gamma
    elif call_put in ['p', 'P', 'put', 'Put', 'PUT']:
        return put_gamma
    else:
        return "Please specify option type"


def vega(call_put,
         stock_price,
         strike,
         volatility,
         time_to_maturity,
         interest_rate,
         div_yield=0):
    d1 = (math.log(stock_price / strike)
          + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    call_vega = stock_price * norm.pdf(d1) * (time_to_maturity ** 0.5)

    put_vega = stock_price * norm.pdf(d1) * (time_to_maturity ** 0.5)

    if call_put in ['c', 'C', 'call', 'Call', 'CALL']:
        return call_vega
    elif call_put in ['p', 'P', 'put', 'Put', 'PUT']:
        return put_vega
    else:
        return "Please specify option type"


def theta(call_put,
          stock_price,
          strike,
          volatility,
          time_to_maturity,
          interest_rate,
          div_yield=0):
    d1 = (math.log(stock_price / strike)
          + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    d2 = d1 - volatility * (time_to_maturity ** 0.5)

    call_theta = -1 * stock_price * norm.pdf(d1) \
                 * volatility / (2 * (time_to_maturity ** 0.5)) - interest_rate * strike \
                 * np.exp(-1 * interest_rate * time_to_maturity) * norm.cdf(d2)

    put_theta = -1 * stock_price * norm.pdf(d1) \
                * volatility / (2 * (time_to_maturity ** 0.5)) + interest_rate * strike \
                * np.exp(-1 * interest_rate * time_to_maturity) * norm.cdf(-1 * d2)

    if call_put in ['c', 'C', 'call', 'Call', 'CALL']:
        return call_theta
    elif call_put in ['p', 'P', 'put', 'Put', 'PUT']:
        return put_theta
    else:
        return "Please specify option type"


def rho(call_put,
        stock_price,
        strike,
        volatility,
        time_to_maturity,
        interest_rate,
        div_yield=0):
    d1 = (math.log(stock_price / strike)
          + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    d2 = d1 - volatility * (time_to_maturity ** 0.5)

    call_rho = strike * time_to_maturity \
               * np.exp(-1 * interest_rate * time_to_maturity) * norm.cdf(d2)

    put_rho = -1 * strike * time_to_maturity \
              * np.exp(-1 * interest_rate * time_to_maturity) * norm.cdf(-1 * d2)

    if call_put in ['c', 'C', 'call', 'Call', 'CALL']:
        return call_rho
    elif call_put in ['p', 'P', 'put', 'Put', 'PUT']:
        return put_rho
    else:
        return "Please specify option type"


def implied_vol(call_put,
                target_option_value,
                stock_price,
                strike,
                time_to_maturity,
                interest_rate,
                div_yield=0):
    max_iteration = 100
    precision = 0.00001
    sigma = 0.25  # initial guess

    for i in xrange(0, max_iteration):
        guess_price = euro_option(call_put,
                                  stock_price,
                                  strike,
                                  sigma,
                                  time_to_maturity,
                                  interest_rate,
                                  div_yield)

        guess_vega = vega(call_put,
                          stock_price,
                          strike,
                          sigma,
                          time_to_maturity,
                          interest_rate,
                          div_yield)

        diff = target_option_value - guess_price

        if abs(diff) < precision:
            return sigma
        sigma = sigma + diff / guess_vega

    return "Max iteration reached: cannot converge"

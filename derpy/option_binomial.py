#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# Binomial option pricing, American & European options
# August 2018
# version 1.0
# Notes:
#       This model applies the simple Cox-Ross-Rubinstein (CRR)
#       model. Advanced alternatives may be added in future
#       releases. (i.e. Jarrow-Rudd, CRR with drift..)
# --------------------------------------------------------

# future proof py2 vs py3
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import numpy as np


def binomial_option(flag,
                    call_put,
                    stock_price,
                    strike,
                    volatility,
                    time_to_maturity,
                    interest_rate,
                    step):
    """

    :param flag: indicating American or European option
    :param call_put: indicating Call or Put option
    :param stock_price: the current price of underlying security
    :param strike: pre-defined strike price of option
    :param volatility: assumed annual volatility of the underlying security
    :param time_to_maturity: time to expiration of the option
    :param interest_rate: risk-free interest rate
    :param step: number of steps of the binomial tree
    :return: the option price using binomial method
    """

    # set up binomial inputs
    period = time_to_maturity / step
    up_prob = np.exp(volatility * (period ** 0.5))
    down_prob = np.exp(-1 * volatility * (period ** 0.5))  # 1/up_prob
    drift = np.exp(interest_rate * period)
    rn_prob = (drift - down_prob) / (up_prob - down_prob)

    # calculate underlying tree price
    price_asset = np.zeros((step + 1, step + 1))
    price_asset[0, 0] = stock_price

    for i in range(1, step + 1):
        price_asset[i, i] = price_asset[i - 1, i - 1] * down_prob
        for j in range(i):
            price_asset[j, i] = price_asset[j, i - 1] * up_prob

    # set option type
    if call_put in ['c', 'C', 'call', 'Call', 'CALL']:
        call_put = 1
    elif call_put in ['p', 'P', 'put', 'Put', 'PUT']:
        call_put = -1
    else:
        print("please specify option types")

    # set option flag
    if flag in ['a', 'A', 'am', 'Am', 'AM', 'american', 'American', 'AMERICAN']:
        flag = 1
    elif flag in ['e', 'E', 'eu', 'Eu', 'EU', 'european', 'European', 'EUROPEAN']:
        flag = 0
    else:
        print("please specify Am or EU option flag")

    # calculate option tree price
    price_option = np.zeros((step + 1, step + 1))
    for i in range(step + 1):
        price_option[i, step] = max(call_put * (price_asset[i, step] - strike), 0)
    for j in range(step):
        for i in range(step - j):
            price_option[i, step - 1 - j] = (rn_prob * price_option[i, step - j]
                                             + (1 - rn_prob) * price_option[i + 1, step - j]) / drift
            if flag == 1:
                price_option[i, step - 1 - j] = max(call_put * (price_asset[i, step - 1 - j] - strike),
                                                    price_option[i, step - 1 - j])

    return price_option[0, 0]

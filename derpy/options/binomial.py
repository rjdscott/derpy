# --------------------------------------------------------
# Binomial option pricing, American & European options
# August 2018
# version 1.0
# Notes:
#       This model applies the simple Cox-Ross-Rubinstein (CRR)
#       model. Advanced alternatives may be added in future
#       releases. (i.e. Jarrow-Rudd, CRR with drift..)
# --------------------------------------------------------

from __future__ import division
import numpy as np


def binomial(flag,
             option_type,
             stock_price,
             strike,
             volatility,
             time_to_maturity,
             interest_rate,
             step):
    """

    :param flag: indicating American or European option
    :param option_type: indicating Call or Put option
    :param stock_price: the current price of underlying security
    :param strike: pre-defined strike price of option
    :param volatility: assumed annual volatility of the underlying security
    :param time_to_maturity: time to expiration of the option
    :param interest_rate: risk-free interest rate
    :param step: number of steps of the binomial tree
    :return: the option price using binomial method
    """

    # set up binomial inputs
    period = time_to_maturity/step
    up_prob = np.exp(volatility*(period ** 0.5))
    down_prob = np.exp(-1*volatility*(period ** 0.5))  # 1/up_prob
    drift = np.exp(interest_rate*period)
    rn_prob = (drift - down_prob)/(up_prob - down_prob)

    # calculate underlying tree price
    price_asset = np.zeros((step + 1, step + 1))
    price_asset[0, 0] = stock_price

    for i in xrange(1, step + 1):
        price_asset[i, i] = price_asset[i - 1, i - 1] * down_prob
        for j in xrange(i):
            price_asset[j, i] = price_asset[j, i - 1] * up_prob

    # set option type
    if option_type in ['c', 'C', 'call', 'Call', 'CALL']:
        option_type = 1
    elif option_type in ['p', 'P', 'put', 'Put', 'PUT']:
        option_type = -1
    else:
        print("please specify option types")

    # set option flag
    if flag in ['a', 'A', 'am', 'Am', 'AM', 'american',  'American', 'AMERICAN']:
        flag = 1
    elif flag in ['e', 'E', 'eu', 'Eu', 'EU', 'european', 'European', 'EUROPEAN']:
        flag = 0
    else:
        print("please specify Am or EU option flag")

    # calculate option tree price
    price_option = np.zeros((step + 1, step + 1))
    for i in xrange(step + 1):
        price_option[i, step] = max(option_type * (price_asset[i, step] - strike), 0)
    for j in xrange(step):
        for i in xrange(step - j):
            price_option[i, step - 1 - j] = (rn_prob*price_option[i, step - j]
                                             + (1 - rn_prob)*price_option[i + 1, step - j])/drift
            if flag == 1:
                price_option[i, step - 1 - j] = max(option_type*(price_asset[i, step - 1 - j] - strike),
                                                    price_option[i, step - 1 - j])

    return price_option[0, 0]

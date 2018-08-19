# --------------------------------------------------------
# European option, Black - Scholes - Merton formula
# August 2018
# --------------------------------------------------------

from __future__ import division
import math
import numpy as np
from scipy.stats import norm


def option_pricing(func, args):
    """
    :param func: option or greeks pricing formula
    :param args: define all inputs once using an array, and call as one input argument
    :return: return values of the underlying functions

    @usage
    import BlackScholesMerton as bsm

    # define input argument once
    args = [20, 21, 0.12, 2, 0.05] # div_yield is optional

    # call option_pricing wrapper function
    bsm.option_pricing(bsm.euro_call, args)
    """
    output = func(*args)
    return output


def euro_call(stock_price, strike, volatility, time_to_maturity, interest_rate, div_yield=0):
    """
    :param stock_price: spot price of the underlying asset
    :param strike: strike price
    :param volatility: annual volatility of the underlying asset
    :param time_to_maturity: time to maturity expressed in years
    :param interest_rate: annual continuous interest rate
    :param div_yield: continuous dividend yield
    :return: european call option price
    """

    d1 = (math.log(stock_price/strike) + (interest_rate - div_yield + (volatility**2)/2)
          * time_to_maturity)/(volatility*(time_to_maturity**0.5))

    d2 = d1 - volatility*(time_to_maturity**0.5)

    call_price = stock_price*np.exp(-1*div_yield*time_to_maturity)*norm.cdf(d1) - \
        strike*np.exp(-1*interest_rate*time_to_maturity)*norm.cdf(d2)

    return call_price


def euro_put(stock_price, strike, volatility, time_to_maturity, interest_rate, div_yield=0):

    d1 = (math.log(stock_price/strike) + (interest_rate - div_yield + (volatility**2)/2)
          * time_to_maturity)/(volatility*(time_to_maturity**0.5))

    d2 = d1 - volatility*(time_to_maturity**0.5)

    put_price = strike*np.exp(-1*interest_rate*time_to_maturity)*norm.cdf(-1*d2) \
        - stock_price*np.exp(-1*div_yield*time_to_maturity)*norm.cdf(-1*d1)

    return put_price


def delta(stock_price, strike, volatility, time_to_maturity, interest_rate, div_yield=0):

    d1 = (math.log(stock_price / strike) + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    call_delta = norm.cdf(d1)
    put_delta = norm.cdf(d1) - 1

    return call_delta, put_delta


def gamma(stock_price, strike, volatility, time_to_maturity, interest_rate, div_yield=0):

    d1 = (math.log(stock_price / strike) + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    call_gamma = norm.pdf(d1)/(stock_price * volatility * (time_to_maturity**(1/2)))
    put_gamma = norm.pdf(d1)/(stock_price * volatility * (time_to_maturity**(1/2)))

    return call_gamma, put_gamma


def vega(stock_price, strike, volatility, time_to_maturity, interest_rate, div_yield=0):

    d1 = (math.log(stock_price / strike) + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    call_vega = stock_price * norm.pdf(d1) * (time_to_maturity**0.5)
    put_vega = stock_price * norm.pdf(d1) * (time_to_maturity**0.5)

    return call_vega, put_vega


def theta(stock_price, strike, volatility, time_to_maturity, interest_rate, div_yield=0):

    d1 = (math.log(stock_price/strike) + (interest_rate - div_yield + (volatility**2)/2)
          * time_to_maturity)/(volatility*(time_to_maturity**0.5))

    d2 = d1 - volatility*(time_to_maturity**0.5)

    call_theta = -1 * stock_price*norm.pdf(d1)*volatility/(2*(time_to_maturity**0.5)) \
        - interest_rate*strike*np.exp(-1*interest_rate*time_to_maturity)*norm.cdf(d2)
    put_theta = -1 * stock_price*norm.pdf(d1)*volatility/(2*(time_to_maturity**0.5)) \
        + interest_rate*strike*np.exp(-1*interest_rate*time_to_maturity)*norm.cdf(-1*d2)

    return call_theta, put_theta


def rho(stock_price, strike, volatility, time_to_maturity, interest_rate, div_yield=0):

    d1 = (math.log(stock_price / strike) + (interest_rate - div_yield + (volatility ** 2) / 2)
          * time_to_maturity) / (volatility * (time_to_maturity ** 0.5))

    d2 = d1 - volatility * (time_to_maturity ** 0.5)

    call_rho = strike*time_to_maturity*np.exp(-1*interest_rate*time_to_maturity)*norm.cdf(d2)
    put_rho = -1*strike*time_to_maturity*np.exp(-1*interest_rate*time_to_maturity)*norm.cdf(-1*d2)

    return call_rho, put_rho

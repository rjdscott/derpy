#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy.optimize as optimize


def bond_convexity(price, face_value, time_to_mat, cpn_rate, cpn_freq, dy=0.01):
    '''
    Calculates bond convexity
    :param price: bond price
    :param face_value: bond face value
    :param time_to_mat: time to maturity
    :param cpn_rate: coupon rate
    :param cpn_freq: coupon freq
    :param dy:
    :return: convexity
    '''
    ytm = bond_ytm(price, face_value, time_to_mat, cpn_rate, cpn_freq)

    ytm_minus = ytm - dy
    price_minus = bond_price(face_value, time_to_mat, ytm_minus, cpn_rate, cpn_freq)

    ytm_plus = ytm + dy
    price_plus = bond_price(face_value, time_to_mat, ytm_plus, cpn_rate, cpn_freq)

    convexity = (price_minus + price_plus - 2 * price) / (price * dy ** 2)

    return convexity


def bond_duration(price, face_value, time_to_mat, cpn_rate, cpn_freq, dy=0.01):
    '''
    Calculates bond modified duration and mac duration
    :param price: float >= 0 (e.g. 99.90)
    :param face_value: float >= 0 (e.g. 99.90)
    :param time_to_mat: float >= 0 (e.g. 9.20)
    :param cpn_rate: float >= 0 (e.g. 2.5 to represent 2.5%)
    :param cpn_freq: float >= 0 (e.g. 99.90)
    :param dy: float >= 0 (e.g. 0.01)
    :return: float: mod_dur, mac_dir
    '''

    ytm = bond_ytm(price=price, face_value=face_value, time_to_mat=time_to_mat, cpn_rate=cpn_rate, cpn_freq=cpn_freq)
    ytm_minus = ytm - dy
    price_minus = bond_price(face_value=face_value, time_to_mat=time_to_mat, yld_to_mat=ytm_minus, cpn_rate=cpn_rate,
                             cpn_freq=cpn_freq)
    ytm_plus = ytm + dy
    price_plus = bond_price(face_value=face_value, time_to_mat=time_to_mat, yld_to_mat=ytm_plus, cpn_rate=cpn_rate,
                            cpn_freq=cpn_freq)
    mac_dur = (price_minus - price_plus)
    mod_dur = mac_dur / (2. * price * dy)

    return mod_dur, mac_dur


def bond_price(face_value, time_to_mat, yld_to_mat, cpn_rate, cpn_freq=2):
    '''
    Calculates bond price from yield to mat
    :param face_value: float >= 0 (e.g. 99.90)
    :param time_to_mat: float >= 0 (e.g 12.5)
    :param yld_to_mat: float >= 0 (e.g. 2.5 to represent 2.5%)
    :param cpn_rate: float >= 0 (e.g. 2.5 to represent 2.5%)
    :param cpn_freq: int >= 0 (1 = annual, 2 = semi-annual, 4 = quarterly)
    :return:
    '''
    cpn_freq = float(cpn_freq)
    periods = time_to_mat * cpn_freq
    coupon = cpn_rate / 100. * face_value / cpn_freq
    dt = [(i + 1) / cpn_freq for i in range(int(periods))]
    price = sum([coupon / (1 + yld_to_mat / 100.0 / cpn_freq) ** (cpn_freq * t) for t in dt]) + \
                 face_value / (1 + yld_to_mat / 100.0 / cpn_freq) ** (cpn_freq * time_to_mat)

    return price


def bond_ytm(price, face_value, time_to_mat, cpn_rate, cpn_freq=2, guess=0.05):
    '''

    :param price:
    :param face_value:
    :param time_to_mat:
    :param cpn_rate:
    :param cpn_freq:
    :param guess:
    :return:
    '''
    cpn_freq = float(cpn_freq)
    periods = time_to_mat * cpn_freq
    coupon = cpn_rate / 100. * face_value / cpn_freq
    dt = [(i + 1) / cpn_freq for i in range(int(periods))]
    ytm_func = lambda y: \
        sum([coupon / (1 + y / cpn_freq) ** (cpn_freq * t) for t in dt]) + \
        face_value / (1 + y / cpn_freq) ** (cpn_freq * max(dt)) - price

    return optimize.newton(ytm_func, guess)


def bond_cashflow(price, time_to_mat, cpn_rate, cpn_freq, face_value):
    """

    :param price: current price of the bond
    :param time_to_mat: number of years to time_to_mat
    :param cpn_rate: coupon rate of the bond
    :param face_value: faceValue of the bond
    :param cpn_freq: frequency of the compounding
    :return: the irr (YTM) of the bond

    Notes: The yield to time_to_mat (irr) calculation uses the numpy.irr library,
           which adopts a method that finds the root of a polynomial by solving
           the eigenvalue of the companion matrix. For a detailed explanation,
           please see http://web.mit.edu/18.06/www/Spring17/Eigenvalue-Polynomials.pdf

           There are other faster, and generic ways to solve for the root of polynomial.
           i.e. the Newton-Raphson method. For an example of YTM calculation using this
           method please see https://github.com/jamesmawm/Mastering-Python-for-Finance-source-codes/blob/master/B03898_05_Codes/bond_ytm.py
    """

    cash_flow = [-1 * float(price)]
    cash_flow.extend([face_value * cpn_rate / cpn_freq] * (time_to_mat * cpn_freq - 2))
    cash_flow.append(face_value * (1 + cpn_rate / cpn_freq))

    return cash_flow


class Bond(object):

    def __init__(self, price=None, cpn_rate=None, cpn_freq=None, maturity=None, face_value=None):
        self.coupon_rate = cpn_rate
        self.coupon_freq = cpn_freq
        self.maturity = maturity
        self.face_value = face_value
        self.price = price
        self.yield_to_mat = None
        self.convexity = None
        self.duration = []
        self.cash_flows = []

    def __repr__(self):
        return "Bond(face_value={}, coupon_rate={}, coupon_freq={}, maturity={})".format(self.face_value,
                                                                                         self.coupon_rate,
                                                                                         self.coupon_freq,
                                                                                         self.maturity)

    def calc_ytm(self):

        if self.maturity is None:
            raise ValueError("Bond maturity is None, please set variable before recalculating...")

        elif self.coupon_freq is None:
            raise ValueError("Bond coupon_freq is None, please set variable before recalculating...")

        elif self.coupon_rate is None:
            raise ValueError("Bond coupon_rate is None, please set variable before recalculating...")

        elif self.price is None:
            raise ValueError("Bond price is None, please set variable before recalculating...")

        elif self.face_value is None:
            raise ValueError("Bond face_value is None, please set variable before recalculating...")

        else:

            self.yield_to_mat = bond_ytm(face_value=self.face_value,
                                         time_to_mat=self.maturity,
                                         cpn_rate=self.coupon_rate,
                                         cpn_freq=self.coupon_freq,
                                         price=self.price)

            return self.yield_to_mat

    def calc_duration(self):
        self.duration = bond_duration(price=self.price,
                                      face_value=self.face_value,
                                      time_to_mat=self.maturity,
                                      cpn_rate=self.coupon_rate,
                                      cpn_freq=self.coupon_freq)
        return self.duration

    def calc_px(self):
        self.price = bond_price(yld_to_mat=self.yield_to_mat,
                                face_value=self.face_value,
                                time_to_mat=self.maturity,
                                cpn_rate=self.coupon_rate,
                                cpn_freq=self.coupon_freq)
        return self.price


if __name__ == '__main__':
    px = 95.0428
    face_val = 100.0
    mat = 1.5
    cpn_frq = 2
    cpn_rate = 5.25
    ytm = 5.5

    print(' Price: {}'.format(bond_price(face_val, mat, ytm, cpn_rate, cpn_frq)))
    print(' Yield: {}'.format(bond_ytm(px, face_val, mat, cpn_rate, cpn_frq)))
    print('ModDur: {}'.format(bond_duration(px, face_val, mat, cpn_rate, cpn_frq)[0]))
    print('MacDur: {}'.format(bond_duration(px, face_val, mat, cpn_rate, cpn_frq)[1]))
    print('Convex: {}'.format(bond_convexity(px, face_val, mat, cpn_rate, cpn_frq)))


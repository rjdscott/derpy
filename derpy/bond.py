#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def bond_price(rate, maturity, coupon_rate, coupon_freq, face_value, due=0):
    """
    :param rate: annual interest rate used for discounting future value
    :param maturity: number of years to maturity
    :param coupon: coupon rate of the bond
    :param face_value: principal payment of the bond at maturity
    :param freq: frequency of the compounding
    :param due: annuity due (type = 1), ordinary annuity (type = 0, default)
    :return: the npv of all bond future cash flows
    """

    npv = np.pv(rate / coupon_freq, maturity * coupon_freq, -1 * coupon_freq * face_value / coupon_freq,
                -1 * face_value, due)

    return npv


def bond_px(par, T, ytm, coup, freq=2):
    freq = float(freq)
    periods = T*freq
    coupon = coup/100.*par/freq
    dt = [(i+1)/freq for i in range(int(periods))]
    price = sum([coupon/(1+ytm/freq)**(freq*t) for t in dt]) + \
            par/(1+ytm/freq)**(freq*T)
    return price


def bond_ytm(price, maturity, coupon_rate, coupon_freq, face_value=100.00):
    """

    :param price: current price of the bond
    :param maturity: number of years to maturity
    :param coupon_rate: coupon rate of the bond
    :param face_value: faceValue of the bond
    :param coupon_freq: frequency of the compounding
    :return: the irr (YTM) of the bond

    Notes: The yield to maturity (irr) calculation uses the numpy.irr library,
           which adopts a method that finds the root of a polynomial by solving
           the eigenvalue of the companion matrix. For a detailed explanation,
           please see http://web.mit.edu/18.06/www/Spring17/Eigenvalue-Polynomials.pdf

           There are other faster, and generic ways to solve for the root of polynomial.
           i.e. the Newton-Raphson method. For an example of YTM calculation using this
           method please see https://github.com/jamesmawm/Mastering-Python-for-Finance-source-codes/blob/master/B03898_05_Codes/bond_ytm.py
    """

    cash_flow = [-1 * price]
    cash_flow.extend([face_value * coupon_rate / coupon_freq] * (maturity * coupon_freq - 2))
    cash_flow.append(face_value * (1 + coupon_rate / coupon_freq))

    ytm = np.irr(cash_flow)

    return ytm


class Bond(object):

    def __init__(self, price=None, cpn_rate=None, cpn_freq=None, maturity=None, face_value=None):
        self.coupon_rate = cpn_rate
        self.coupon_freq = cpn_freq
        self.maturity = maturity
        self.face_value = face_value
        self.price = price
        self.yield_to_mat = None
        self.convexity = None
        self.mod_dur = None

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
                                         maturity=self.maturity,
                                         coupon_rate=self.coupon_rate,
                                         coupon_freq=self.coupon_freq,
                                         price=self.price)

            return self.yield_to_mat

    def calc_px(self):
        pass


if __name__ == '__main__':

    px = 139.87
    mat = 12
    cpn_frq = 2
    cpn_rate = 6.25
    dc_rate = 3.0
    face_val = 99.94

    bond = Bond(price=px, maturity=mat, cpn_freq=cpn_frq, cpn_rate=cpn_rate, face_value=face_val)

    print('--- bond ytm ---')
    print(bond.calc_ytm())
    print(bond_ytm(price=px, maturity=mat, coupon_rate=cpn_rate, coupon_freq=cpn_frq, face_value=face_val))


    print('--- bond prices ---')
    print(bond.price)
    print(bond_price(rate=dc_rate, maturity=mat, coupon_rate=cpn_rate, coupon_freq=cpn_frq, face_value=face_val))


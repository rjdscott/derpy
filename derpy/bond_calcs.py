#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# Bond price calculator with given inputs
# August 2018
# --------------------------------------------------------

import numpy as np


def bond_price(rate, maturity, coupon, face_value, freq, due=0):

    """
    :param rate: annual interest rate used for discounting future value
    :param maturity: number of years to maturity
    :param coupon: coupon rate of the bond
    :param face_value: principal payment of the bond at maturity
    :param freq: frequency of the compounding
    :param due: annuity due (type = 1), ordinary annuity (type = 0, default)
    :return: the npv of all bond future cash flows
    """

    npv = np.pv(rate/freq, maturity*freq, -1*coupon*face_value/freq, -1*face_value, due)

    return npv


def ytm_calculation(price, maturity, coupon, face_value, freq):

    """
    :param price: current price of the bond
    :param maturity: number of years to maturity
    :param coupon: coupon rate of the bond
    :param face_value: faceValue of the bond
    :param freq: frequency of the compounding
    :return: the irr (YTM) of the bond

    Notes: The yield to maturity (irr) calculation uses the numpy.irr library,
           which adopts a method that finds the root of a polynomial by solving
           the eigenvalue of the companion matrix. For a detailed explanation,
           please see http://web.mit.edu/18.06/www/Spring17/Eigenvalue-Polynomials.pdf

           There are other faster, and generic ways to solve for the root of polynomial.
           i.e. the Newton-Raphson method. For an example of YTM calculation using this
           method please see https://github.com/jamesmawm/
                    Mastering-Python-for-Finance-source-codes/blob/master/B03898_05_Codes/bond_ytm.py
    """

    cash_flow = [-1*price]
    cash_flow.extend([face_value * coupon / freq] * (maturity*freq - 2))
    cash_flow.append(face_value*(1 + coupon/freq))

    ytm = np.irr(cash_flow)

    return ytm

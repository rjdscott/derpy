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

    npv = np.pv(rate/coupon_freq, maturity*coupon_freq, -1*coupon_freq*face_value/coupon_freq, -1*face_value, due)

    return npv


def bond_yield_to_maturity(price, maturity, coupon_rate, face_value, coupon_freq):
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
           method please see http://web.mit.edu/18.06/www/Spring17/Eigenvalue-Polynomials.pdf
    """

    cash_flow = [-1 * price]
    cash_flow.extend([face_value * coupon_rate / coupon_freq] * (maturity * coupon_freq - 2))
    cash_flow.append(face_value * (1 + coupon_rate / coupon_freq))

    ytm = np.irr(cash_flow)

    return ytm


class Bond(object):

    def __init__(self, face_value=None, cpn_rate=None, cpn_freq=None, maturity=None):
        self.face_value = face_value
        self.coupon_rate = cpn_rate
        self.coupon_freq = cpn_freq
        self.maturity = maturity
        self.price = None
        self.yield_to_maturity = None
        self.convexity = None
        self.modified_duration = None

    def __repr__(self):
        return "Bond(face_value={}, coupon_rate={}, coupon_freq={}, maturity={})".format(self.face_value,
                                                                                    self.coupon_rate,
                                                                                    self.coupon_freq,
                                                                                    self.maturity)

    def get_yield_to_maturity(self):

        if self.maturity is None:
            raise ValueError("Bond maturity is None, please set variable before recalculating...")

        elif self.coupon_freq is None:
            raise ValueError("Bond coupon_freq is None, please set variable before recalculating...")

        elif self.coupon_rate is None:
            raise ValueError("Bond coupon_rate is None, please set variable before recalculating...")

        elif self.face_value is None:
            raise ValueError("Bond face_value is None, please set variable before recalculating...")

        try:
            self.yield_to_maturity = bond_yield_to_maturity(face_value=self.face_value,
                                                            maturity=self.maturity,
                                                            coupon_rate=self.coupon_rate,
                                                            coupon_freq=self.coupon_freq)

        except ValueError:
            raise("Cannot price bond, please check inputs...")

        return self.yield_to_maturity


if __name__ == '__main__':
    bond = Bond(face_value=1000, maturity=20, cpn_freq=2, cpn_rate=3 )
    bond_px = bond_price(3, 20, 2.5, 100, 2)
    print(bond_px)

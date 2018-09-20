=====
Usage
=====


Bonds
========

.. code-block:: python

        from derpy import bond as bd

        px = 139.87
        mat = 12
        cpn_frq = 2
        cpn_rate = 6.25
        dc_rate = 3.0
        face_val = 99.94

        bond = bd.Bond(price=px, maturity=mat, cpn_freq=cpn_frq, cpn_rate=cpn_rate, face_value=face_val)

        print('--- bond ytm ---')
        print('Bond ytm = {}'.format(bond.ytm()))
        # returns Bond ytm = 2.2328769571733056

Options
============

.. code-block:: python

        from derpy.options import black_scholes_merton as bsm

        # usage method 1: use function wrapper
        input = ['call', 20, 21, 0.20, 0.1, 0.0002, 0]
        call_price = bsm.option_pricing(bsm.euro_option, input)
        call_gamma = bsm.option_pricing(bsm.gamma, input)

        # usage method 2: call individual functions
        put_price = bsm.euro_option('put', 20, 21, 0.2, 0.1, 0.0002) # div_yield is optional
        put_gamma = bsm.gamma('put', 20, 21, 0.2, 0.1, 0.0002, 0.0001)

        print(call_price)  # return 0.16384395..
        print(call_gamma)  # return 0.23993880..
        print(put_price)  # return 1.16342..
        print(put_gamma)  # return 0.2399107..

Portfolio analysis
=====================

.. code-block:: python

        from derpy import portfolio as pt

        securities = ['AAA', 'BBB']
        positions = [[11, 10], [12, 10], [13, 10], [13, 11], [13, 12]]
        prices = [[10, 10], [11, 10], [12, 10], [12, 10], [12, 10]]
        dates = ['2018-07-01', '2018-08-01', '2018-09-01', '2018-10-01', '2018-11-01']

        df_positions = pd.DataFrame(data=positions, columns=securities, index=dates)
        df_prices = pd.DataFrame(data=prices, columns=securities, index=dates)

        p = pt.Portfolio(names=securities, positions=df_positions, prices=df_prices)

        print(p.sec_values())
        print(p.sec_weights())
        print(p.portfolio_value())
        print(p.portfolio_returns())


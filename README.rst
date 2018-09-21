=====
derpy
=====

.. image:: https://img.shields.io/pypi/v/derpy.svg
        :target: https://pypi.python.org/pypi/derpy

.. image:: https://img.shields.io/travis/rjdscott/derpy.svg
        :target: https://travis-ci.org/rjdscott/derpy

.. image:: https://readthedocs.org/projects/derpy/badge/?version=latest
        :target: https://derpy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Financial derivatives and portfolio analysis tools for python

* Free software: MIT license
* Documentation: https://derpy.readthedocs.io.


How to get up and running
*****************************
to include the module in your project, you can simply use `pip install derpy` then in your python project

.. code-block:: python

        import derpy
        print(derpy.__version__) # returns '0.0.1'

Example uses
***************

Bonds
==========

.. code-block:: python

        from derpy import bond as bd

        px = 95.0428
        face_val = 100.0
        mat = 1.5
        cpn_frq = 2
        cpn_rate = 5.25
        ytm = 5.5

        print('    Price: {}'.format(bd.bond_price(face_val, mat, ytm, cpn_rate, cpn_frq)))
        print('    Yield: {}'.format(bd.bond_ytm(px, face_val, mat, cpn_rate, cpn_frq)))
        print('   ModDur: {}'.format(bd.bond_duration(px, face_val, mat, cpn_rate, cpn_frq)[0]))
        print('   MacDur: {}'.format(bd.bond_duration(px, face_val, mat, cpn_rate, cpn_frq)[1]))
        print('Convexity: {}'.format(bd.bond_convexity(px, face_val, mat, cpn_rate, cpn_frq)))

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

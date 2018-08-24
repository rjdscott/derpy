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
******************
to include the module in your project, you can simply use `pip install derpy` then in your python project

.. code-block:: python

        import derpy as dp

        print(dp.version()) # returns derpy-v0.0.1


Example uses
************

Bonds:
==========

.. code-block:: python

        import derpy as dp

        bond = dp.Bond(yield=2.3, maturity=3.4, coupon=2.3)
        print(bond.price) # returns 100


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
============

.. code-block:: python

        import derpy as dp

        assets = ['a','b','c']
        prices = [1,2,3]
        quantities = [100,100,100]

        portfolio = dp.Portfolio(assets=assets,
                                prices=prices,
                                quantities=quantities)

        print(portfolio.value) # returns 500
        print(portfolio.weights) # returns {'a':20, 'b':40, 'c': 60}

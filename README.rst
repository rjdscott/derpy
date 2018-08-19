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
to include the module in your project, you can simply use `pip install derpy` then in your python project:

.. code-block:: python
        import derpy as dp

        print(dp.version()) # returns derpy-v0.0.1


Example uses
************

Bonds
==========

.. code-block:: python
        import derpy as dp

        bond = dp.Bond(yield=2.3, maturity=3.4, coupon=2.3)
        print(bond.price) # returns 100


Options
============

.. code-block:: python
        import derpy as dp

        opt = dp.Option(strike=20, 
                        underlying=13, 
                        type='american', 
                        volatility=30, 
                        maturity=340)

        print(opt.price(method='monte-carlo')) # returns 100
        print(opt.price(method='black-scholes')) # returns 100
        print(opt.price(method='binomial')) # returns 100


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
        
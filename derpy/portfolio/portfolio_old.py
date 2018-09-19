# portfolio related functions
import pandas as pd
from datetime import date


def calc_portfolio_values(df_positions, df_prices, position_date=None):

    if not isinstance(df_positions, pd.DataFrame):
        raise ValueError("Position is not a DataFrame")

    if not isinstance(df_prices, pd.DataFrame):
        raise ValueError("df_prices is not a DataFrame")

    df_values = df_positions * df_prices

    if position_date is None:
        return df_values

    else:
        # if not isinstance(position_date, date):
        # raise ValueError("Position is not a DataFrame")
        if position_date not in df_weights.index:
            raise ValueError("position date {} not in DataFrame.")
        else:
            return df_values.loc[position_date, :]


def calc_portfolio_weights(df_positions, df_prices, position_date=None):

    if not isinstance(df_positions, pd.DataFrame):
        raise ValueError("Position is not a DataFrame")

    if not isinstance(df_prices, pd.DataFrame):
        raise ValueError("df_prices is not a DataFrame")

    df_values = calc_portfolio_weights(df_positions * df_prices)
    df_weights = df_values.divide(df_values.sum(axis='columns'), axis='rows')

    if position_date is None:
        return df_weights

    else:
        # if not isinstance(position_date, date):
        # raise ValueError("Position is not a DataFrame")
        if position_date not in df_weights.index:
            raise ValueError("position date {} not in DataFrame.")
        else:
            return df_weights.loc[position_date,:]


class Transaction:

    def __init__(self, ticker, price, volume, position_date, buy_sell):
        self.ticker = ticker
        self.price = price
        self.volume = volume
        self.position_date = position_date
        self.buy_sell = buy_sell

    def __repr__(self):
            str_raw = "Transaction(ticker='{}', price='{}', volume='{}', transation_date='{}', buy_sell='{}')"
            return str_raw.format(self.ticker,
                                  self.price,
                                  self.volume,
                                  self.position_date,
                                  self.buy_sell)


class Portfolio(object):

    def __init__(self, sec_weights=None, sec_holdings=None, initial_value=None, sec_prices=None):
        self.sec_weights = sec_weights
        self.sec_holdings = sec_holdings
        self.sec_prices = sec_prices
        self.initial_value = initial_value
        self.portfolio_values = None
        self.portfolio_start_date = None
        self.portfolio_end_date = None


    def get_weights(self, position_date=None):
        pass

    def get_portfolio_value(self, position_date=None):
        # need to clean data - this will take two dataframes and multiply.
        # in order od priority, positions take preference over prices
        # where prices are null, offer ability to use previous (for weekends, etc)
        pass

    def get_performance(self, start_date, end_date):
        pass

    def get_portfolio_from_transactions(self, tbl_transactions):
        pass


if __name__ == '__main__':
    tr = Transaction("bhp.ax", 100, 20, '2018-08-01', 'b')
    print(tr)

    # lets try some portfolio weight examples
    # this needs to be moved to tests after they work
    securities = ['AAA','BBB']

    positions = [[11,10],
                 [12,10],
                 [13,10]
                 ]

    prices = [[10,10],
             [11,10],
             [12,10]]

    dates = ['2018-07-01', '2018-08-01', '2018-09-01']

    df_positions = pd.DataFrame(data=positions, columns=securities, index=dates)
    df_prices = pd.DataFrame(data=prices, columns=securities, index=dates)
    df_values = df_positions * df_prices
    df_weights = df_values.divide(df_values.sum(axis='columns'),axis='rows')
    print(df_positions)
    print(df_prices)
    print('-------')
    print(df_weights)
    test = calc_portfolio_weights(df_positions=df_positions, df_prices=df_prices)
    print(test)
    test2 = calc_portfolio_weights(df_positions=df_positions, df_prices=df_prices, position_date='2018-08-01')
    print(test)
    print(test2)

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


class Portfolio:

    def __int__(self, sec_names, sec_holdings, sec_prices):
        self.sec_names = sec_names
        self.sec_holdings = sec_holdings
        self.sec_prices = sec_prices

    def sec_weights(self, date_dt=None, date_rel=None):
        sec_values_df = self.sec_values(date_dt=date_dt, date_rel=date_rel)
        sec_weights_df = sec_values_df.divide(df_values.sum(axis='columns'), axis='rows')

        if date_dt is None and date_rel is None:
            return sec_weights_df

        elif date_dt is not None:
            return sec_weights_df.loc[date_dt, :]

        elif date_rel is not None:
            return sec_weights_df.loc[int(date_dt), :]

        else:
            raise ValueError("Something went wrong generating portfolio weights..")

    def sec_values(self, date_dt=None, date_rel=None):

        if self.sec_prices is not None and self.sec_holdings is not None:

            sec_values_df = pd.DataFrame(self.sec_prices * self.sec_holdings)

            if date_dt is None and date_rel is None:
                return sec_values_df

            elif date_dt is not None:
                return pd.DataFrame(sec_values_df.loc[date_dt, :]).transpose()

            elif date_rel is not None:
                return pd.DataFrame(sec_values_df.loc[int(date_dt), :]).transpose()

        elif self.sec_prices is None:
            raise ValueError("Cannot compute values.. no sec_prices available..")

        elif self.sec_holdings is None:
            raise ValueError("Cannot compute values.. no sec_holdings available..")

    def portfolio_value(self, date_dt=None, date_rel=None):
        # todo: this can be improved to get the self. values first then progress

        sec_vals_df = self.sec_values()
        port_val_df = pd.DataFrame(sec_vals_df.sum(axis=1), columns=['port_value'])

        if date_dt is None and date_rel is None:
            return port_val_df

        elif date_dt is not None:
            return pd.DataFrame(port_val_df.loc[date_dt, :]).transpose()

        elif date_rel is not None:
            return pd.DataFrame(port_val_df.loc[int(date_dt), :]).transpose()

        else:
            raise ValueError("Something went wrong, please check your inputs...")

    def portfolio_return(self):

        sec_vals_df = self.sec_values()
        port_val_df = pd.DataFrame(sec_vals_df.sum(axis=1), columns=['port_value'])

        port_val_df['arithmetic_return'] = port_val_df['port_value'].pct_change()
        port_val_df['log_return'] = np.log(port_val_df['port_value']) - np.log(port_val_df['port_value'].shift(1))

        return port_val_df


class QuickFolio:

    def __init__(self, names, positions, prices):
        self.sec_names = names
        self.positions = positions
        self.prices = prices

    def sec_values(self):
        return self.positions * self.prices

    def sec_weights(self):
        sec_vals = self.sec_values()
        return sec_vals.divide(sec_vals.sum(axis='columns'), axis='rows')

    def portfolio_value(self):
        sec_vals = self.sec_values()
        return pd.DataFrame(sec_vals.sum(axis=1), columns=['value'])

    def portfolio_returns(self):
        port_val = self.portfolio_value()
        port_val['simple_ret'] = port_val['value'].pct_change()
        port_val['log_ret'] = np.log(port_val['value']) - np.log(port_val['value'].shift(1))
        return port_val


if __name__ == '__main__':

    securities = ['AAA', 'BBB']
    positions = [[11, 10], [12, 10], [13, 10], [13, 11], [13, 12]]
    prices = [[10, 10], [11, 10], [12, 10], [12, 10], [12, 10]]
    dates = ['2018-07-01', '2018-08-01', '2018-09-01', '2018-10-01', '2018-11-01']

    df_positions = pd.DataFrame(data=positions, columns=securities, index=dates)
    df_prices = pd.DataFrame(data=prices, columns=securities, index=dates)

    qf = QuickFolio(names=securities, positions=df_positions, prices=df_prices)
    print(qf.sec_values())
    print('-----')
    print(qf.sec_weights())
    print('-----')
    print(qf.portfolio_value())
    print('-----')
    print(qf.portfolio_returns())

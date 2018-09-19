import pandas as pd
from . import portfolio_old as pt

securities = ['AAA', 'BBB']

positions = [[11, 10],
             [12, 10],
             [13, 10]]

prices = [[10, 10],
          [11, 10],
          [12, 10]]

dates = ['2018-07-01', '2018-08-01', '2018-09-01']

df_positions = pd.DataFrame(data=positions, columns=securities, index=dates)
df_prices = pd.DataFrame(data=prices, columns=securities, index=dates)
df_values = df_positions * df_prices

test = pt.calc_portfolio_weights(df_positions=df_positions, df_prices=df_prices)
print(test)
test2 = pt.calc_portfolio_weights(df_positions=df_positions, df_prices=df_prices, position_date='2018-08-01')
print(test)
print(test2)

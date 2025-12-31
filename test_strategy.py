'''from src.strategy import GoldenCrossStrategy
import pandas as pd

prices = pd.read_csv('data/hsi_prices.csv', index_col=0, parse_dates=True)['Close_Price']

strategy = GoldenCrossStrategy(prices, stop_loss_pct=0.10)
strategy.track_positions()
strategy.plot_strategy()
print(strategy.data[['price', 'position', 'high_since_buy', 'signal']].tail(20))  # Check last 20 days'''

import pandas as pd
from src.strategy import GoldenCrossStrategy
from src.backtester import Backtester

# Load data
prices = pd.read_csv('data/hsi_prices.csv', index_col='Date', parse_dates=True)['Close_Price']

# Strategy (with your stop-loss)
strategy = GoldenCrossStrategy(prices, stop_loss_pct=0.10)
strategy.track_positions()
strategy.plot_strategy()  # Optional: Re-generate signals plot

# Backtest
backtester = Backtester(strategy.data)
backtester.calculate_returns()
backtester.simulate_portfolio()
backtester.plot_equity_curve()

# Print final results
print("Final Portfolio Values:")
print(backtester.data[['strategy_equity', 'buy_hold_equity']].tail(1))
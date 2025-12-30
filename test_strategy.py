from src.strategy import GoldenCrossStrategy
import pandas as pd

prices = pd.read_csv('data/hsi_prices.csv', index_col=0, parse_dates=True)['Close_Price']

strategy = GoldenCrossStrategy(prices, stop_loss_pct=0.10)
strategy.track_positions()
strategy.plot_strategy()
print(strategy.data[['price', 'position', 'high_since_buy', 'signal']].tail(20))  # Check last 20 days
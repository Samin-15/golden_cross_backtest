import pandas as pd
from src.data_fetcher import fetch_hsi_data
from src.strategy import GoldenCrossStrategy
from src.backtester import Backtester
from src.analytics import calculate_metrics

def main():
    # Fetch data
    prices = fetch_hsi_data()
    
    # Strategy
    strategy = GoldenCrossStrategy(prices, stop_loss_pct=0.10)
    strategy_data = strategy.track_positions()
    strategy.plot_strategy()
    
    # Backtest
    backtester = Backtester(strategy_data)
    backtester.calculate_returns()
    backtester.simulate_portfolio()
    backtester.plot_equity_curve()
    
    # Metrics
    strategy_metrics = calculate_metrics(backtester.data['strategy_return'])
    buy_hold_metrics = calculate_metrics(backtester.data['buy_hold_return'])
    metrics_df = pd.DataFrame([strategy_metrics, buy_hold_metrics], index=['Strategy', 'Buy and Hold']).T
    metrics_df.to_csv('results/metrics_summary.csv')
    print("Metrics Summary:")
    print(metrics_df)

if __name__ == "__main__":
    main()
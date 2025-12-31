import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class Backtester:
    def __init__(self, strategy_data: pd.DataFrame):
        """
        Initializes with data from GoldenCrossStrategy (has 'price', 'position').
        """
        self.data = strategy_data.copy()
    
    def calculate_returns(self):
        """Daily % returns for strategy and benchmark."""
        # HSI daily return
        self.data['index_return'] = self.data['price'].pct_change()
        
        # Strategy: Lagged position * return
        self.data['strategy_return'] = self.data['position'].shift(1) * self.data['index_return']
        
        # Buy-hold: Full index return
        self.data['buy_hold_return'] = self.data['index_return']
        
        self.data = self.data.dropna()
        return self.data
    
    def simulate_portfolio(self, initial_capital=10000):
        """Grow $ over time."""
        self.data['strategy_equity'] = initial_capital * (1 + self.data['strategy_return']).cumprod()
        self.data['buy_hold_equity'] = initial_capital * (1 + self.data['buy_hold_return']).cumprod()
        return self.data
    
    def plot_equity_curve(self, save_path='results/figures/equity_curve.png'):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['strategy_equity'], label='Golden Cross (with Stop-Loss)', color='green')
        plt.plot(self.data['buy_hold_equity'], label='Buy and Hold ^HSI', color='blue')
        plt.title('Portfolio Growth: $10,000 Initial Investment')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.grid()
        plt.savefig(save_path)
        plt.close()
        print(f"Equity curve saved to {save_path}")
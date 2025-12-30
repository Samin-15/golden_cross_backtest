import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class GoldenCrossStrategy:
    def __init__(self, prices: pd.Series, short_window=50, long_window=200, stop_loss_pct=0.10):
        """
        Initializes with prices, SMA windows, and stop-loss percentage.
        - stop_loss_pct: Fraction for trailing stop-loss (e.g., 0.10 = 10%).
        """
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.stop_loss_pct = stop_loss_pct
        self.data = pd.DataFrame(index=prices.index)
        self.data['price'] = prices
    
    def calculate_smas(self):
        """Computes the two SMAs."""
        self.data['sma_short'] = self.prices.rolling(window=self.short_window).mean()
        self.data['sma_long'] = self.prices.rolling(window=self.long_window).mean()
        self.data = self.data.dropna()  # Drop NaN SMA rows
        return self.data
    
    def generate_signals(self):
        """Generates buy/sell signals from SMA crossovers."""
        self.calculate_smas()
        
        self.data['signal_raw'] = 0
        # Buy (1)
        self.data['signal_raw'] = np.where(
            (self.data['sma_short'] > self.data['sma_long']) &
            (self.data['sma_short'].shift(1) <= self.data['sma_long'].shift(1)),
            1, self.data['signal_raw']
        )
        # Sell (-1)
        self.data['signal_raw'] = np.where(
            (self.data['sma_short'] < self.data['sma_long']) &
            (self.data['sma_short'].shift(1) >= self.data['sma_long'].shift(1)),
            -1, self.data['signal_raw']
        )
        
        self.data['signal'] = self.data['signal_raw'].shift(1).fillna(0)
        return self.data
    
    def track_positions(self):
        """Turns signals into positions, with trailing stop-loss."""
        self.generate_signals()
        
        self.data['position'] = 0
        self.data['high_since_buy'] = np.nan  # Tracks max price since entry
        
        current_position = 0
        high_since_buy = 0
        
        for i in range(len(self.data)):
            price = self.data['price'].iloc[i]
            signal = self.data['signal'].iloc[i]
            
            # Apply signal first
            if signal == 1:
                current_position = 1
                high_since_buy = price  # Reset high on new buy
            elif signal == -1:
                current_position = 0
                high_since_buy = 0
            
            # Apply trailing stop-loss if in position
            if current_position == 1:
                high_since_buy = max(high_since_buy, price)
                if price < high_since_buy * (1 - self.stop_loss_pct):
                    current_position = 0
                    high_since_buy = 0
                    self.data['signal'].iloc[i] = -1  # Mark as stop-loss sell
            
            self.data['position'].iloc[i] = current_position
            self.data['high_since_buy'].iloc[i] = high_since_buy
        
        return self.data
    
    def plot_strategy(self, save_path='results/figures/signals_plot_with_stop.png'):
        """Plots with stop-loss sells highlighted."""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(self.data['price'], label='HSI Price', alpha=0.5)
        ax.plot(self.data['sma_short'], label='50-day SMA', color='blue')
        ax.plot(self.data['sma_long'], label='200-day SMA', color='orange')
        
        # Regular buys (green ^)
        buys = self.data[self.data['signal'] == 1]
        ax.scatter(buys.index, buys['price'], marker='^', color='green', s=100, label='Buy')
        
        # Regular sells (red v)
        regular_sells = self.data[(self.data['signal'] == -1) & (self.data['position'].shift(1) == 1) & ~self.data.index.isin(buys.index - pd.Timedelta(1, 'D'))]  # Approximate filter
        ax.scatter(regular_sells.index, regular_sells['price'], marker='v', color='red', s=100, label='Sell (Cross)')
        
        # Stop-loss sells (purple x)
        stop_sells = self.data[self.data['signal'] == -1]  # All sells, but in practice stops are subset
        ax.scatter(stop_sells.index, stop_sells['price'], marker='x', color='purple', s=100, label='Sell (Stop-Loss)')
        
        ax.set_title('Golden Cross with 10% Trailing Stop-Loss on Hang Seng Index')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid()
        plt.savefig(save_path)
        plt.close()
        print(f"Plot saved to {save_path}")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class GoldenCrossStrategy:
    def __init__(self, prices: pd.Series, short_window=50, long_window=200):
        """
        Initializes with prices and SMA windows.
        - prices: Our HSI closing prices (from CSV).
        - short_window: Days for fast SMA.
        - long_window: Days for slow SMA.
        """
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.data = pd.DataFrame(index=prices.index)  # Empty DF with dates
        self.data['price'] = prices  # Add prices column
    
    def calculate_smas(self):
        """Computes the two SMAs."""
        # rolling() averages last N values; mean() computes average
        self.data['sma_short'] = self.prices.rolling(window=self.short_window).mean()
        self.data['sma_long'] = self.prices.rolling(window=self.long_window).mean()
        
        # Drop rows where SMA is NaN (first 199 days for 200-SMA)
        self.data = self.data.dropna()
        
        return self.data
    
    def generate_signals(self):
        """Generates buy/sell signals from SMA crossovers."""
        # Call SMAs first
        self.calculate_smas()
        
        # Raw signal: Detect crossovers
        self.data['signal_raw'] = 0
        # Buy (1): Short > long today, but <= yesterday
        self.data['signal_raw'] = np.where(
            (self.data['sma_short'] > self.data['sma_long']) &
            (self.data['sma_short'].shift(1) <= self.data['sma_long'].shift(1)),
            1, self.data['signal_raw']
        )
        # Sell (-1): Short < long today, but >= yesterday
        self.data['signal_raw'] = np.where(
            (self.data['sma_short'] < self.data['sma_long']) &
            (self.data['sma_short'].shift(1) >= self.data['sma_long'].shift(1)),
            -1, self.data['signal_raw']
        )
        
        # CRITICAL: Shift to avoid look-ahead bias
        self.data['signal'] = self.data['signal_raw'].shift(1).fillna(0)
        
        return self.data
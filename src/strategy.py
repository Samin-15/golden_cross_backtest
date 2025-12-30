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
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_hsi_data(period_years=10, ticker='^HSI', filename='data/hsi_prices.csv'):
    """
    Fetches historical close prices for Hang Seng Index (^HSI) over the specified period.
    Note: Indices like ^HSI do not have 'Adj Close' in yfinance (no dividends/splits to adjust),
    so we use 'Close' instead.
    
    Args:
        period_years (int): Number of years of data to fetch (default 10).
        ticker (str): Yahoo ticker symbol (default '^HSI').
        filename (str): Path to save CSV (default 'data/hsi_prices.csv').
    
    Returns:
        pd.Series: Close prices with DateTime index.
    """
    # Calculate start date with buffer
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=365 * period_years + 20)  # Extra buffer
    
    # Fetch data
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    if data.empty:
        raise ValueError(f"No data downloaded for {ticker}. Check ticker or internet connection.")
    
    # Use 'Close' for indices (no 'Adj Close' available)
    if 'Adj Close' in data.columns:
        prices = data['Adj Close']
    else:
        prices = data['Close']  # This will be used for ^HSI
    
    # Clean up
    prices = prices.dropna()
    prices.index = pd.to_datetime(prices.index)
    prices.name = 'Close_Price'  # Clearer name
    
    # Ensure data folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save to CSV
    prices.to_csv(filename)
    
    print(f"Data fetched: {len(prices)} trading days from {prices.index[0].date()} to {prices.index[-1].date()}")
    print(f"Saved to {filename}")
    return prices

# Test when running directly
if __name__ == "__main__":
    fetch_hsi_data()
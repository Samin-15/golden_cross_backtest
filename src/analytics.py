import pandas as pd
import numpy as np

def calculate_metrics(returns: pd.Series, risk_free_rate=0.02):
    """
    Computes metrics for a daily return series.
    - returns: pd.Series of daily % returns.
    - risk_free_rate: Annual safe rate (default 2%).
    """
    if len(returns) == 0:
        return {k: np.nan for k in ['Total Return (%)', 'Annualized Return (%)', 'Annualized Volatility (%)', 'Sharpe Ratio', 'Maximum Drawdown (%)']}
    
    metrics = {}
    
    # Total Return
    cumulative = (1 + returns).prod() - 1
    metrics['Total Return (%)'] = cumulative * 100
    
    # Annualized Return
    num_days = len(returns)
    ann_return = (1 + cumulative) ** (252 / num_days) - 1
    metrics['Annualized Return (%)'] = ann_return * 100
    
    # Annualized Volatility
    daily_vol = returns.std()
    ann_vol = daily_vol * np.sqrt(252)
    metrics['Annualized Volatility (%)'] = ann_vol * 100
    
    # Sharpe Ratio
    metrics['Sharpe Ratio'] = (ann_return - risk_free_rate) / ann_vol if ann_vol != 0 else 0
    
    # Maximum Drawdown
    wealth = (1 + returns).cumprod()
    peak = wealth.cummax()
    drawdown = (wealth - peak) / peak
    metrics['Maximum Drawdown (%)'] = drawdown.min() * 100
    
    return metrics
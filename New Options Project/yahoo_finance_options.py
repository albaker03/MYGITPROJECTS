import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json

def get_stock_info(symbol):
    """Fetch current stock information from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if data.empty:
            raise ValueError(f"No data found for {symbol}")
        
        current_price = data["Close"].iloc[-1]
        return {
            'symbol': symbol,
            'current_price': current_price,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise ValueError(f"Error fetching stock data for {symbol}: {e}")

def get_option_chain(symbol, expiration_date=None):
    """
    Fetch option chain data from Yahoo Finance.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        expiration_date: Specific expiration date (format: 'YYYY-MM-DD')
                        If None, uses nearest expiration
    
    Returns:
        Dictionary with calls and puts DataFrames
    """
    try:
        stock = yf.Ticker(symbol)
        expirations = stock.options  # Get list of available expirations
        
        if not expirations:
            raise ValueError(f"No options data available for {symbol}")
        
        # Select expiration date
        if expiration_date:
            if expiration_date not in expirations:
                available = ", ".join(expirations[:5])
                raise ValueError(f"Expiration {expiration_date} not available. Available: {available}...")
            selected_exp = expiration_date
        else:
            selected_exp = expirations[0]  # Use nearest expiration
        
        # Fetch option chain
        option_chain = stock.option_chain(selected_exp)
        
        return {
            'symbol': symbol,
            'expiration': selected_exp,
            'calls': option_chain.calls,
            'puts': option_chain.puts,
            'available_expirations': expirations
        }
    except Exception as e:
        raise ValueError(f"Error fetching option chain for {symbol}: {e}")

def find_nearest_strike(current_price, target_price, option_chain_df, option_type='call'):
    """
    Find the nearest strike price to target from available options.
    
    Args:
        current_price: Current stock price
        target_price: Target strike price
        option_chain_df: DataFrame of option chain (calls or puts)
        option_type: 'call' or 'put'
    
    Returns:
        Dictionary with strike info and option data
    """
    if option_chain_df.empty:
        return None
    
    available_strikes = option_chain_df['strike'].unique()
    
    # Find closest strike to target
    nearest_strike = min(available_strikes, key=lambda x: abs(x - target_price))
    
    # Get option data for that strike
    option_data = option_chain_df[option_chain_df['strike'] == nearest_strike].iloc[0]
    
    return {
        'strike': nearest_strike,
        'bid': option_data['bid'],
        'ask': option_data['ask'],
        'last_price': option_data['lastPrice'],
        'volume': option_data['volume'],
        'open_interest': option_data['openInterest'],
        'implied_volatility': option_data['impliedVolatility'],
        'distance_from_target': abs(nearest_strike - target_price)
    }

def display_available_options(symbol, expiration=None):
    """Display available option expirations and retrieve option chain."""
    try:
        print(f"\nFetching option data for {symbol}...")
        chain_data = get_option_chain(symbol, expiration)
        
        current_price = get_stock_info(symbol)['current_price']
        
        print(f"\nStock: {symbol} | Current Price: ${current_price:.2f}")
        print(f"Option Expiration: {chain_data['expiration']}")
        print(f"\nAvailable Expirations (next 10):")
        for i, exp in enumerate(chain_data['available_expirations'][:10], 1):
            print(f"  {i}. {exp}")
        
        return chain_data
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_real_market_price(symbol, strike_price, option_type, expiration_date=None):
    """
    Get real market price for a specific option from Yahoo Finance.
    
    Args:
        symbol: Stock symbol
        strike_price: Strike price of the option
        option_type: 'call' or 'put'
        expiration_date: Expiration date (format: 'YYYY-MM-DD')
    
    Returns:
        Dictionary with market price data
    """
    try:
        chain_data = get_option_chain(symbol, expiration_date)
        option_chain_df = chain_data['calls'] if option_type == 'call' else chain_data['puts']
        
        # Find exact or nearest strike
        if strike_price in option_chain_df['strike'].values:
            option_data = option_chain_df[option_chain_df['strike'] == strike_price].iloc[0]
        else:
            # Find nearest strike
            nearest_option = find_nearest_strike(
                get_stock_info(symbol)['current_price'],
                strike_price,
                option_chain_df,
                option_type
            )
            if nearest_option:
                option_data = option_chain_df[option_chain_df['strike'] == nearest_option['strike']].iloc[0]
            else:
                return None
        
        return {
            'symbol': symbol,
            'strike': option_data['strike'],
            'option_type': option_type,
            'bid': option_data['bid'],
            'ask': option_data['ask'],
            'last_price': option_data['lastPrice'],
            'volume': option_data['volume'],
            'open_interest': option_data['openInterest'],
            'implied_volatility': option_data['impliedVolatility'],
            'expiration': chain_data['expiration']
        }
    except Exception as e:
        raise ValueError(f"Error getting market price: {e}")

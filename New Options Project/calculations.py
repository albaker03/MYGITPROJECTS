import math
from scipy.stats import norm

def calculate_strike_price(target_price, contract_length, current_price, option_type):
    """
    Calculate strike price based on target price and time to expiration.
    
    Formula:
    - For calls: Strike = Current Price + (Target Price - Current Price) * (Contract Length / 12)
    - For puts: Strike = Current Price - (Current Price - Target Price) * (Contract Length / 12)
    
    Args:
        target_price: Target price of stock at expiration
        contract_length: Contract length in months
        current_price: Current stock price
        option_type: 'call' or 'put'
    
    Returns:
        Calculated strike price
    """
    if option_type == 'call':
        # For calls, strike is based on upside target
        price_difference = target_price - current_price
        strike = current_price + price_difference * (contract_length / 12)
    else:
        # For puts, strike is based on downside protection
        price_difference = current_price - target_price
        strike = current_price - price_difference * (contract_length / 12)
    
    return max(strike, 0.01)  # Ensure strike is positive

def black_scholes(S, K, T, sigma, r, option_type='call'):
    """
    Calculate option price using Black-Scholes model.
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to expiration (in years)
        sigma: Volatility (annualized)
        r: Risk-free rate
        option_type: 'call' or 'put'
    
    Returns:
        Option price
    """
    if T <= 0:
        # Option has expired
        if option_type == 'call':
            return max(S - K, 0)
        else:
            return max(K - S, 0)
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return max(price, 0)

def calculate_greeks(S, K, T, sigma, r, option_type='call'):
    """
    Calculate option Greeks (Delta, Gamma, Theta, Vega, Rho).
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to expiration (in years)
        sigma: Volatility (annualized)
        r: Risk-free rate
        option_type: 'call' or 'put'
    
    Returns:
        Dictionary with Greeks: delta, gamma, theta, vega, rho
    """
    if T <= 0:
        return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    # Delta: Rate of change of option price with respect to stock price
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    
    # Gamma: Rate of change of delta with respect to stock price
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    
    # Theta: Rate of change of option price with respect to time (per day)
    if option_type == 'call':
        theta = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) - 
                 r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
    else:
        theta = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) + 
                 r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365
    
    # Vega: Sensitivity to 1% change in volatility (per 1% change, per day)
    vega = S * norm.pdf(d1) * math.sqrt(T) / 100
    
    # Rho: Sensitivity to 1% change in interest rate
    if option_type == 'call':
        rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100
    else:
        rho = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100
    
    return {
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega,
        'rho': rho
    }

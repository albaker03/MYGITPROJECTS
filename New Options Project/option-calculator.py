import os
import csv
from datetime import datetime
from calculations import calculate_strike_price, calculate_greeks, black_scholes
from yahoo_finance_options import (
    get_stock_info, get_option_chain, display_available_options,
    get_real_market_price, find_nearest_strike
)

def ensure_output_dir():
    """Ensure output directory exists."""
    if not os.path.exists('output'):
        os.makedirs('output')

def get_positive_float(prompt):
    """Get positive float input with validation."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Error: Value must be positive.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def get_volatility():
    """Get volatility input (0.0 to 1.0)."""
    while True:
        try:
            value = float(input("Enter implied volatility (0.0-1.0, default 0.2): ") or "0.2")
            if not (0.0 <= value <= 1.0):
                print("Error: Volatility must be between 0.0 and 1.0.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def get_risk_free_rate():
    """Get risk-free rate input."""
    while True:
        try:
            value = float(input("Enter risk-free rate (default 0.05): ") or "0.05")
            if value < 0:
                print("Error: Rate cannot be negative.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def get_option_type():
    """Get option type (call or put)."""
    while True:
        option_type = input("Enter option type (call/put): ").lower().strip()
        if option_type in ['call', 'put', 'c', 'p']:
            return 'call' if option_type in ['call', 'c'] else 'put'
        print("Error: Please enter 'call' or 'put'.")

def get_stock_symbol():
    """Get stock symbol from user."""
    while True:
        symbol = input("Enter stock symbol (e.g., AAPL): ").upper().strip()
        if len(symbol) > 0 and len(symbol) <= 5:
            return symbol
        print("Error: Please enter a valid stock symbol.")

def fetch_real_market_data(symbol, option_type, strike_price):
    """Fetch real market data from Yahoo Finance."""
    try:
        market_data = get_real_market_price(symbol, strike_price, option_type)
        return market_data
    except Exception as e:
        print(f"Warning: Could not fetch market data - {e}")
        return None

def get_implied_volatility_from_market(symbol, option_type):
    """Get implied volatility from market if available."""
    try:
        chain_data = get_option_chain(symbol)
        option_chain_df = chain_data['calls'] if option_type == 'call' else chain_data['puts']
        
        # Get average implied volatility from near-the-money options
        avg_iv = option_chain_df['impliedVolatility'].mean()
        return avg_iv if avg_iv > 0 else 0.2  # Default to 0.2 if no valid IV
    except Exception as e:
        print(f"Warning: Could not fetch implied volatility - {e}")
        return 0.2  # Default volatility

def save_calculation(data):
    """Save calculation to CSV."""
    ensure_output_dir()
    file_path = 'output/calculations_history.csv'
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'target_price', 'contract_length', 'current_price',
                     'option_type', 'volatility', 'risk_free_rate', 'strike_price',
                     'contract_price', 'delta', 'gamma', 'theta', 'vega', 'rho']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

def display_greeks(greeks):
    """Display Greek values with explanations."""
    print("\n" + "="*50)
    print("OPTION GREEKS")
    print("="*50)
    print(f"Delta (Δ):  {greeks['delta']:.4f}")
    print("  └─ Price sensitivity to $1 stock move")
    print(f"\nGamma (Γ):  {greeks['gamma']:.4f}")
    print("  └─ Rate of delta change")
    print(f"\nTheta (Θ):  {greeks['theta']:.4f}")
    print("  └─ Daily time decay value")
    print(f"\nVega (ν):   {greeks['vega']:.4f}")
    print("  └─ Sensitivity to 1% volatility change")
    print(f"\nRho (ρ):    {greeks['rho']:.4f}")
    print("  └─ Sensitivity to 1% interest rate change")
    print("="*50)

def display_recommendation(option_type, greeks, volatility):
    """Display trading recommendation based on Greeks."""
    print("\n" + "="*50)
    print("TRADING ANALYSIS")
    print("="*50)
    
    if option_type == 'call':
        print("Position Type: LONG CALL")
        if greeks['delta'] > 0.6:
            print("Direction: BULLISH (Strong upside bet)")
        elif greeks['delta'] > 0.3:
            print("Direction: MODERATELY BULLISH")
        else:
            print("Direction: LOW DELTA (Out-of-the-money)")
    else:
        print("Position Type: LONG PUT")
        if greeks['delta'] < -0.6:
            print("Direction: BEARISH (Strong downside protection)")
        elif greeks['delta'] < -0.3:
            print("Direction: MODERATELY BEARISH")
        else:
            print("Direction: LOW DELTA (Out-of-the-money)")
    
    if greeks['theta'] < -0.05:
        print("Time Decay: RAPID (Loses value daily)")
    elif greeks['theta'] < -0.01:
        print("Time Decay: MODERATE")
    else:
        print("Time Decay: SLOW")
    
    if volatility > 0.3:
        print("Volatility: HIGH (Increased premium)")
    elif volatility > 0.2:
        print("Volatility: MODERATE")
    else:
        print("Volatility: LOW")
    
    print("="*50)

def main():
    """Main application loop."""
    print("\n" + "="*50)
    print("OPTIONS CALCULATOR WITH YAHOO FINANCE DATA")
    print("="*50)
    
    while True:
        try:
            # Ask if user wants to use real market data
            use_market_data = input("\nFetch real data from Yahoo Finance? (yes/no, default: yes): ").lower().strip()
            use_market_data = use_market_data in ['yes', 'y', '']
            
            if use_market_data:
                # Get stock symbol
                symbol = get_stock_symbol()
                
                # Fetch current stock price
                print(f"\nFetching data for {symbol}...")
                try:
                    stock_info = get_stock_info(symbol)
                    current_price = stock_info['current_price']
                    print(f"✓ Current price: ${current_price:.2f}")
                except Exception as e:
                    print(f"Error fetching stock price: {e}")
                    continue
                
                # Display available options
                print("\nFetching available options...")
                chain_data = display_available_options(symbol)
                if not chain_data:
                    continue
                
                # Get remaining inputs
                target_price = get_positive_float(f"Enter target price of {symbol} at expiration: $")
                contract_length_months = (datetime.strptime(chain_data['expiration'], '%Y-%m-%d') - datetime.now()).days / 30.44
                print(f"Contract length: {contract_length_months:.2f} months")
                
                # Use market implied volatility
                option_type = get_option_type()
                print("\nFetching market implied volatility...")
                volatility = get_implied_volatility_from_market(symbol, option_type)
                print(f"✓ Market IV: {volatility:.2%}")
                
                risk_free_rate = get_risk_free_rate()
                
            else:
                # Manual input mode
                symbol = None
                target_price = get_positive_float("Enter target price of stock: $")
                contract_length_months = get_positive_float("Enter contract length (months): ")
                current_price = get_positive_float("Enter current price of stock: $")
                option_type = get_option_type()
                volatility = get_volatility()
                risk_free_rate = get_risk_free_rate()
            
            # Calculate strike price
            strike_price = calculate_strike_price(target_price, contract_length_months, 
                                                  current_price, option_type)
            
            # Calculate contract price using Black-Scholes
            contract_price = black_scholes(current_price, strike_price, 
                                          contract_length_months / 12, volatility, 
                                          risk_free_rate, option_type)
            
            # Calculate Greeks
            greeks = calculate_greeks(current_price, strike_price, 
                                     contract_length_months / 12, volatility, 
                                     risk_free_rate, option_type)
            
            # Display results
            print("\n" + "="*50)
            print("CALCULATION RESULTS")
            print("="*50)
            if symbol:
                print(f"Stock: {symbol}")
            print(f"Strike Price:   ${strike_price:.2f}")
            print(f"Calculated Price: ${contract_price:.2f}")
            
            # Fetch and display real market data if available
            if symbol and use_market_data:
                print("\nFetching real market price...")
                try:
                    market_data = fetch_real_market_data(symbol, option_type, strike_price)
                    if market_data:
                        print("\n" + "-"*50)
                        print("REAL MARKET DATA (Yahoo Finance)")
                        print("-"*50)
                        print(f"Strike:         ${market_data['strike']:.2f}")
                        print(f"Bid:            ${market_data['bid']:.2f}")
                        print(f"Ask:            ${market_data['ask']:.2f}")
                        print(f"Last Trade:     ${market_data['last_price']:.2f}")
                        print(f"Implied Vol:    {market_data['implied_volatility']:.2%}")
                        print(f"Volume:         {int(market_data['volume'])}")
                        print(f"Open Interest:  {int(market_data['open_interest'])}")
                        print("-"*50)
                        
                        # Compare calculated vs market
                        mid_market = (market_data['bid'] + market_data['ask']) / 2
                        diff_percent = ((contract_price - mid_market) / mid_market) * 100 if mid_market > 0 else 0
                        print(f"\nCalculated vs Market: ${contract_price:.2f} vs ${mid_market:.2f}")
                        print(f"Difference: {diff_percent:+.2f}%")
                except Exception as e:
                    print(f"Could not fetch market data: {e}")
            
            print("="*50)
            
            # Display Greeks
            display_greeks(greeks)
            
            # Display recommendation
            display_recommendation(option_type, greeks, volatility)
            
            # Save calculation
            save_calculation({
                'timestamp': datetime.now().isoformat(),
                'target_price': target_price,
                'contract_length': contract_length_months,
                'current_price': current_price,
                'option_type': option_type,
                'volatility': volatility,
                'risk_free_rate': risk_free_rate,
                'strike_price': strike_price,
                'contract_price': contract_price,
                'delta': greeks['delta'],
                'gamma': greeks['gamma'],
                'theta': greeks['theta'],
                'vega': greeks['vega'],
                'rho': greeks['rho']
            })
            print("\n✓ Calculation saved to output/calculations_history.csv")
            
            # Ask if user wants to continue
            again = input("\nCalculate another option? (yes/no): ").lower().strip()
            if again not in ['yes', 'y']:
                print("\nThank you for using Options Calculator!")
                break
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\nApplication terminated by user.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()

# Options Calculator with Yahoo Finance Integration

A comprehensive Python options calculator that uses the Black-Scholes model to price options and calculate Greeks. It can pull real option prices from Yahoo Finance and compare them with calculated theoretical prices.

## Features

- **Strike Price Calculator**: Calculates strike prices based on target prices and time to expiration
- **Black-Scholes Pricing**: Uses the Black-Scholes model to calculate theoretical option prices
- **Greeks Calculation**: Computes Delta, Gamma, Theta, Vega, and Rho
- **Yahoo Finance Integration**: Fetches real market data, current stock prices, and implied volatility
- **Market Comparison**: Compares calculated prices with real market prices
- **Trading Recommendations**: Provides analysis based on Greeks and volatility
- **Historical Tracking**: Saves all calculations to CSV for analysis

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- `yfinance` - Fetches stock and option data from Yahoo Finance
- `scipy` - Statistical functions for Black-Scholes model
- `pandas` - Data manipulation
- `numpy` - Numerical computations

## Usage

### Basic Usage

Run the calculator:
```bash
python option-calculator.py
```

### Modes

The calculator supports two modes:

#### Mode 1: Real Market Data (Default)
- Fetches live stock prices from Yahoo Finance
- Retrieves available option expiration dates
- Pulls real implied volatility from the market
- Compares your calculated prices with market prices

#### Mode 2: Manual Input
- Enter all values manually
- Useful for theoretical analysis
- No internet connection required

### Workflow Example

```
1. Choose to fetch real data or enter manually
2. Enter stock symbol (e.g., AAPL)
3. Enter target price at expiration
4. Select option type (call or put)
5. The calculator automatically:
   - Calculates strike price using the formula
   - Prices the option using Black-Scholes
   - Computes all Greeks
   - Fetches real market data
   - Compares calculated vs market prices
6. View analysis and trading recommendations
```

## Strike Price Formula

The strike price is calculated based on your target price and time to expiration:

**For Call Options:**
```
Strike = Current Price + (Target Price - Current Price) × (Contract Length / 12)
```

**For Put Options:**
```
Strike = Current Price - (Current Price - Target Price) × (Contract Length / 12)
```

This formula allows you to set a strike price that progressively moves from the current price toward your target price as the contract approaches expiration.

## Black-Scholes Model

The calculator uses the standard Black-Scholes formula:

**For Call Options:**
```
C = S₀N(d₁) - Ke^(-rT)N(d₂)
```

**For Put Options:**
```
P = Ke^(-rT)N(-d₂) - S₀N(-d₁)
```

Where:
- `d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)`
- `d₂ = d₁ - σ√T`
- `S₀` = Current stock price
- `K` = Strike price
- `r` = Risk-free rate
- `σ` = Volatility
- `T` = Time to expiration (in years)
- `N()` = Cumulative normal distribution

## Greeks Explained

- **Delta (Δ)**: Price change for a $1 move in the stock
  - Range: 0 to 1 for calls, -1 to 0 for puts
  
- **Gamma (Γ)**: Rate of change of delta
  - Highest at-the-money, lower for deep ITM/OTM
  
- **Theta (Θ)**: Daily time decay
  - Represents how much value is lost daily due to time decay
  
- **Vega (ν)**: Sensitivity to 1% change in volatility
  - Highest at-the-money options
  
- **Rho (ρ)**: Sensitivity to 1% change in interest rates
  - Less commonly used in short-term trading

## Output

The calculator saves all calculations to `output/calculations_history.csv` with the following columns:
- timestamp
- target_price
- contract_length
- current_price
- option_type
- volatility
- risk_free_rate
- strike_price
- contract_price
- delta, gamma, theta, vega, rho

## Example Session

```
Options Calculator with Yahoo Finance Data
==================================================

Fetch real data from Yahoo Finance? (yes/no, default: yes): yes
Enter stock symbol (e.g., AAPL): AAPL

Fetching data for AAPL...
✓ Current price: $192.45

Stock: AAPL | Current Price: $192.45
Option Expiration: 2024-05-17

Available Expirations (next 10):
  1. 2024-05-17
  2. 2024-05-24
  ...

Enter target price of AAPL at expiration: $200
Contract length: 2.34 months
Enter option type (call/put): call
✓ Market IV: 0.1850

==================================================
CALCULATION RESULTS
==================================================
Stock: AAPL
Strike Price:   $200.23
Calculated Price: $3.45

REAL MARKET DATA (Yahoo Finance)
--------------------------------------------------
Strike:         $200.00
Bid:            $3.20
Ask:            $3.50
Last Trade:     $3.35
Implied Vol:    0.1825
Volume:         15234
Open Interest:  42891
--------------------------------------------------

Calculated vs Market: $3.45 vs $3.35
Difference: +2.99%
```

## Tips for Using the Calculator

1. **Implied Volatility**: Higher volatility makes options more expensive
2. **Time Decay**: Options lose value as expiration approaches (Theta)
3. **Strike Selection**: Use the calculator to find profitable strike prices
4. **Greeks**: Use Greeks to understand risk exposure
5. **Compare Prices**: Use real market data to validate your calculations

## Troubleshooting

### "No data found for SYMBOL"
- Check the stock symbol spelling (e.g., AAPL not APPLE)
- Verify the stock trades on US exchanges (limited international support)

### "No options data available"
- Some stocks don't have liquid options markets
- Try major stocks like AAPL, MSFT, TSLA, etc.

### Connection errors
- Ensure you have an internet connection for Yahoo Finance data
- Use manual mode if internet is unavailable

## Files

- `option-calculator.py` - Main calculator application
- `calculations.py` - Black-Scholes and Greeks calculations
- `yahoo_finance_options.py` - Yahoo Finance data fetching
- `requirements.txt` - Python dependencies
- `output/calculations_history.csv` - Calculation history

## References

- [Black-Scholes Model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
- [The Greeks (Finance)](https://en.wikipedia.org/wiki/Greeks_(finance))
- [Options (Finance)](https://en.wikipedia.org/wiki/Option_(finance))
- [Yahoo Finance](https://finance.yahoo.com)

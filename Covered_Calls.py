import yfinance as yf
import datetime

# Parameters
STOCK_SYMBOL = "AAPL"  # Stock symbol for the strategy
BUDGET = 15000  # Maximum capital to buy the stock
DAYS_TO_EXPIRY = 30  # Time to expiry for the option contracts

# Step 1: Check Stock Price
def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")["Close"].iloc[-1]
    return price

# Step 2: Run the Wheel Strategy
def wheel_strategy():
    stock_price = get_stock_price(STOCK_SYMBOL)
    number_of_shares = int(BUDGET / stock_price)  # Calculate number of shares affordable
    cash_required = number_of_shares * stock_price

    # Placeholder for logic to decide what to do
    # Let's assume you already have the stock for this simplified logic
    have_stock = True  # Set True if you have the stock already; otherwise set False

    # Placeholder function to sell an option (to be implemented with broker API)
    def sell_option(option_type, strike_price):
        print(f"Selling a {option_type} with strike price {strike_price}")

    # Selling puts if you don't own the stock yet
    if not have_stock:
        strike_price = round(stock_price * 0.95)  # Pick a strike price slightly below current price
        print(f"Selling cash-secured put for {STOCK_SYMBOL} at strike price {strike_price}")
        sell_option("put", strike_price)

    # Selling calls if you have the stock already
    elif have_stock:
        strike_price = round(stock_price * 1.05)  # Pick a strike price slightly above current price
        print(f"Selling covered call for {STOCK_SYMBOL} at strike price {strike_price}")
        sell_option("call", strike_price)

if __name__ == "__main__":
    wheel_strategy()

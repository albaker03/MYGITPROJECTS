import argparse
import datetime as dt
from dataclasses import dataclass
import yfinance as yf

# ----------------- config via CLI -----------------
parser = argparse.ArgumentParser(description="Option Wheel helper (paper)")
parser.add_argument("--symbol", default="AAPL", help="Underlying ticker, e.g. AAPL")
parser.add_argument("--budget", type=float, default=15000, help="Cash available (USD)")
parser.add_argument("--dte", type=int, default=30, help="Target days to expiration")
parser.add_argument("--have-stock", action="store_true", help="If you already own 100 shares")
parser.add_argument("--contracts", type=int, default=1, help="Number of option contracts")
args = parser.parse_args()

SYMBOL          = args.symbol.upper()
BUDGET          = args.budget
TARGET_DTE      = args.dte
HAVE_STOCK      = args.have_stock
CONTRACTS       = args.contracts  # 1 contract = 100 shares

# ----------------- helpers -----------------
@dataclass
class OrderIdea:
    side: str           # "SELL"
    option_type: str    # "PUT" or "CALL"
    symbol: str
    expiry: str         # "YYYY-MM-DD"
    strike: float
    qty: int            # contracts
    ref_mid: float      # mid price reference
    rationale: str

def nearest_expiry(expirations, target_days):
    """Pick the expiry date nearest to target DTE but not earlier than today+7 (avoid weekly noise if desired)."""
    today = dt.date.today()
    best = None
    best_delta = 10**9
    for e in expirations:
        try:
            d = dt.datetime.strptime(e, "%Y-%m-%d").date()
        except Exception:
            continue
        dte = (d - today).days
        if dte < 7:  # skip very short-dated by default; tweak if you like
            continue
        delta = abs(dte - target_days)
        if delta < best_delta:
            best, best_delta = e, delta
    # fallback: if everything is <7 days, just take the first
    return best or (expirations[0] if expirations else None)

def pick_option_row(chain_df, target_strike, option_type):
    """Pick the row with strike closest to target_strike and decent quotes."""
    if chain_df is None or chain_df.empty:
        return None
    df = chain_df.copy()
    df["dist"] = (df["strike"] - target_strike).abs()
    # Prefer contracts with non-zero bid/ask
    df = df.sort_values(by=["dist", "bid"], ascending=[True, False])
    return df.iloc[0]

# ----------------- fetch data -----------------
ticker = yf.Ticker(SYMBOL)
hist = ticker.history(period="1d")
if hist.empty:
    raise SystemExit(f"No price data for {SYMBOL}")

spot = float(hist["Close"].iloc[-1])
lot_cost = 100 * spot

print(f"Underlying: {SYMBOL}")
print(f"Spot: ${spot:,.2f} | Lot of 100 shares ≈ ${lot_cost:,.2f}")
print(f"Budget: ${BUDGET:,.2f} | Have stock: {HAVE_STOCK} | Contracts: {CONTRACTS} | Target DTE: {TARGET_DTE}")

exps = ticker.options
if not exps:
    raise SystemExit("No listed options found for this ticker.")
expiry = nearest_expiry(exps, TARGET_DTE)
if not expiry:
    raise SystemExit("Could not select an expiry.")
print(f"Chosen expiry: {expiry}")

chains = ticker.option_chain(expiry)  # returns (calls, puts) as DataFrames
calls, puts = chains.calls, chains.puts

# ----------------- wheel logic -----------------
ideas = []

if not HAVE_STOCK:
    # SELL CASH-SECURED PUT: choose ~5% OTM strike
    target_put_strike = round(spot * 0.95, 2)
    put_row = pick_option_row(puts, target_put_strike, "PUT")
    if put_row is not None:
        bid = float(put_row.get("bid", 0) or 0)
        ask = float(put_row.get("ask", 0) or 0)
        mid = (bid + ask) / 2 if (bid > 0 and ask > 0) else max(bid, ask)
        strike = float(put_row["strike"])
        # Ensure budget can actually secure the put (100 * strike * contracts)
        collateral = 100 * strike * CONTRACTS
        if collateral <= BUDGET:
            ideas.append(OrderIdea(
                side="SELL",
                option_type="PUT",
                symbol=SYMBOL,
                expiry=expiry,
                strike=strike,
                qty=CONTRACTS,
                ref_mid=mid,
                rationale=f"Cash-secured put ≈5% OTM; collateral ≈ ${collateral:,.2f} within budget."
            ))
        else:
            print(f"⚠️ Collateral ${collateral:,.2f} exceeds budget ${BUDGET:,.2f}. Consider lower strike.")
    else:
        print("No suitable put found near target strike.")

else:
    # SELL COVERED CALL: choose ~5% OTM strike
    target_call_strike = round(spot * 1.05, 2)
    call_row = pick_option_row(calls, target_call_strike, "CALL")
    if call_row is not None:
        bid = float(call_row.get("bid", 0) or 0)
        ask = float(call_row.get("ask", 0) or 0)
        mid = (bid + ask) / 2 if (bid > 0 and ask > 0) else max(bid, ask)
        strike = float(call_row["strike"])
        ideas.append(OrderIdea(
            side="SELL",
            option_type="CALL",
            symbol=SYMBOL,
            expiry=expiry,
            strike=strike,
            qty=CONTRACTS,
            ref_mid=mid,
            rationale="Covered call ≈5% OTM for premium while allowing upside."
        ))
    else:
        print("No suitable call found near target strike.")

# ----------------- output “paper order” -----------------
if not ideas:
    print("No trade idea generated based on current inputs.")
else:
    print("\n--- Suggested Paper Order ---")
    for i in ideas:
        mult = 100 * i.qty
        credit_est = (i.ref_mid or 0) * mult
        print(
            f"{i.side} {i.qty} {i.option_type} "
            f"{i.symbol} {i.expiry} {i.strike:.2f} "
            f"@ mid ≈ ${i.ref_mid:.2f}  | Est. credit ≈ ${credit_est:,.2f}"
        )
        print(f"Rationale: {i.rationale}")
    print("\nNOTE: This script does NOT place real orders. Use a broker API to execute.")
 

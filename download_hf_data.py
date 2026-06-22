import pandas as pd
import requests
import json
import os
import yfinance as yf

os.makedirs('data/hedge_fund_datasets', exist_ok=True)

print("Pulling Custom Hedge Fund Alt-Data...")

# 1. Dow 30 Cross-Sectional Fundamentals (Statistical Arbitrage)
# We will use yfinance to pull live fundamental data for 30 major US companies
tickers = ["AAPL", "MSFT", "JPM", "V", "JNJ", "WMT", "PG", "XOM", "UNH", "HD", "CVX", "MRK", "KO", "DIS", "CSCO", "MCD", "BA", "CRM", "VZ", "NKE", "IBM", "CAT", "GS", "TRV", "AMGN", "HON", "WBA", "MMM", "DOW", "AXP"]

data = []
for ticker in tickers:
    try:
        t = yf.Ticker(ticker)
        info = t.info
        data.append({
            "Ticker": ticker,
            "Sector": info.get("sector", "Unknown"),
            "Industry": info.get("industry", "Unknown"),
            "MarketCap": info.get("marketCap"),
            "TrailingPE": info.get("trailingPE"),
            "ForwardPE": info.get("forwardPE"),
            "PriceToBook": info.get("priceToBook"),
            "DividendYield": info.get("dividendYield"),
            "Beta": info.get("beta"),
            "ProfitMargin": info.get("profitMargin"),
            "OperatingMargin": info.get("operatingMargin"),
            "ReturnOnAssets": info.get("returnOnAssets"),
            "ReturnOnEquity": info.get("returnOnEquity"),
            "RevenueGrowth": info.get("revenueGrowth"),
            "DebtToEquity": info.get("debtToEquity")
        })
    except Exception as e:
        pass

df_fundamentals = pd.DataFrame(data)
df_fundamentals.to_csv('data/hedge_fund_datasets/dow30_fundamentals.csv', index=False)

print("\n--- 1. Cross-Sectional Fundamentals Dataset ---")
print(f"Shape: {df_fundamentals.shape[0]} rows, {df_fundamentals.shape[1]} variables")
print(f"Categorical Variables: {sum(df_fundamentals.dtypes == 'object')}")
print(f"Numeric Variables: {sum(df_fundamentals.dtypes != 'object')}")
print(f"Missing Values: {df_fundamentals.isnull().sum().sum()}")
print(f"Meets 10+ Variable requirement? {'Yes' if df_fundamentals.shape[1] >= 10 else 'No'}")


# 2. Corporate Insider Transactions (SEC Form 4)
# Pulling a sample of historical insider trading data from a public GitHub mirror
insider_url = "https://raw.githubusercontent.com/rohan-chhajed/Insider-Trading-Analysis/master/Data/insider_trades.csv"
try:
    df_insider = pd.read_csv(insider_url)
    df_insider.to_csv('data/hedge_fund_datasets/corporate_insider_trades.csv', index=False)
    print("\n--- 2. Corporate Insider Transactions Dataset ---")
    print(f"Shape: {df_insider.shape[0]} rows, {df_insider.shape[1]} variables")
    print(f"Categorical Variables: {sum(df_insider.dtypes == 'object')}")
    print(f"Numeric Variables: {sum(df_insider.dtypes != 'object')}")
    print(f"Missing Values: {df_insider.isnull().sum().sum()}")
    print(f"Meets 10+ Variable requirement? {'Yes' if df_insider.shape[1] >= 10 else 'No'}")
except Exception as e:
    print("Failed to pull insider data:", e)


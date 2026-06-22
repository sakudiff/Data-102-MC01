import pandas as pd
import yfinance as yf
import requests
import io
import os

os.makedirs('data/hedge_fund_datasets', exist_ok=True)

print("Fetching S&P 500 Tickers...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', headers=headers)
table = pd.read_html(io.StringIO(response.text))
tickers = table[0]['Symbol'].tolist()

print(f"Found {len(tickers)} tickers. Fetching fundamental data (this will take a minute)...")

data = []
for ticker in tickers[:100]: # Just pulling 100 for now to be fast, you can remove [:100] for all 500
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
    except Exception:
        pass

df = pd.DataFrame(data)
df.to_csv('data/hedge_fund_datasets/sp500_fundamentals_sample.csv', index=False)

print("\n--- S&P 500 Fundamentals Dataset ---")
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} variables")
print(f"Categorical Variables: {sum(df.dtypes == 'object')} (e.g. Sector, Industry)")
print(f"Numeric Variables: {sum(df.dtypes != 'object')} (e.g. P/E, MarketCap, ROA)")
print(f"Missing Values: {df.isnull().sum().sum()} (Great for Data Cleaning section!)")
print(f"Meets 10+ Variable requirement? {'Yes' if df.shape[1] >= 10 else 'No'}")

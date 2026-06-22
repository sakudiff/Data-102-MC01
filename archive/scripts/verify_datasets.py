import pandas as pd
import requests
import urllib.request
import os
import yfinance as yf
import io

os.makedirs('data/credit_card', exist_ok=True)
os.makedirs('data/hedge_fund_datasets', exist_ok=True)

print("--- 1. Re-fetching S&P 500 Fundamentals (FULL 500 COMPANIES) ---")
try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', headers=headers)
    table = pd.read_html(io.StringIO(response.text))
    tickers = table[0]['Symbol'].tolist()
    
    print(f"Fetching data for {len(tickers)} tickers. Please wait...")
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
        except Exception:
            pass
            
    df_sp500 = pd.DataFrame(data)
    df_sp500.to_csv('data/hedge_fund_datasets/sp500_fundamentals_full.csv', index=False)
    print(f"VERIFIED S&P 500: {df_sp500.shape[0]} Rows, {df_sp500.shape[1]} Columns.")
except Exception as e:
    print(f"Failed S&P 500: {e}")

print("\n--- 2. Fetching Credit Card Defaults (UCI) ---")
try:
    url_cc = "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls"
    # Download the xls file
    urllib.request.urlretrieve(url_cc, "data/credit_card/default_clients.xls")
    
    # Read and convert to CSV
    # header=1 because row 0 is ID, LIMIT_BAL... row 1 is actually the column names sometimes in this dataset
    df_cc = pd.read_excel("data/credit_card/default_clients.xls", header=1) 
    df_cc.to_csv('data/credit_card/credit_card_defaults.csv', index=False)
    
    print(f"VERIFIED CREDIT CARD: {df_cc.shape[0]} Rows, {df_cc.shape[1]} Columns.")
except Exception as e:
    print(f"Failed Credit Card Defaults: {e}")

print("\n--- 3. Verifying Bank Marketing Dataset ---")
try:
    df_bank = pd.read_csv('data/bank-additional/bank-additional-full.csv', sep=';')
    print(f"VERIFIED BANK MARKETING: {df_bank.shape[0]} Rows, {df_bank.shape[1]} Columns.")
except Exception as e:
    print(f"Failed Bank Marketing: {e}")

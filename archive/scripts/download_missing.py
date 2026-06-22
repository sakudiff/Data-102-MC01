import pandas as pd
from datasets import load_dataset
import os

os.makedirs('data/sba_loans', exist_ok=True)
os.makedirs('data/college_scorecard', exist_ok=True)

print("--- Downloading SBA Loan Defaults ---")
try:
    # Load from huggingface
    sba_dataset = load_dataset("MaddRaf/SBAnational", split="train")
    df_sba = sba_dataset.to_pandas()
    df_sba.to_csv('data/sba_loans/sba_national.csv', index=False)
    print(f"VERIFIED SBA: {df_sba.shape[0]} Rows, {df_sba.shape[1]} Columns.")
except Exception as e:
    print(f"Failed SBA: {e}")

print("\n--- Downloading College Scorecard ---")
try:
    cs_dataset = load_dataset("tongtong24x/us-college-scorecard-2022", split="train")
    df_cs = cs_dataset.to_pandas()
    df_cs.to_csv('data/college_scorecard/college_scorecard_2022.csv', index=False)
    print(f"VERIFIED SCORECARD: {df_cs.shape[0]} Rows, {df_cs.shape[1]} Columns.")
except Exception as e:
    print(f"Failed Scorecard: {e}")

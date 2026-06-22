import pandas as pd
import os

os.makedirs('data/final_datasets', exist_ok=True)

print("Subsetting datasets to fit GitHub's 100MB file limit...")

# 1. SBA Subset (100k rows)
df_sba = pd.read_csv('data/sba_loans/SBAnational.csv', low_memory=False)
df_sba_subset = df_sba.sample(n=100000, random_state=42)
df_sba_subset.to_csv('data/final_datasets/SBA_Loans_Subset.csv', index=False)
print(f"Saved SBA Subset. Size: {os.path.getsize('data/final_datasets/SBA_Loans_Subset.csv') / (1024*1024):.2f} MB")

# 2. College Scorecard Subset (24 Columns)
cols = ['UNITID', 'INSTNM', 'CITY', 'STABBR', 'PREDDEG', 'CONTROL', 'LOCALE', 'HBCU', 'PBI', 'ANNHI', 'TRIBAL', 'AANAPII', 'HSI', 'NANTI', 'MENONLY', 'WOMENONLY', 'RELAFFIL', 'ADM_RATE', 'SAT_AVG', 'UGDS', 'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'MD_EARN_WNE_P10', 'GRAD_DEBT_MDN']
df_cs = pd.read_csv('data/college_scorecard/College_Scorecard_Raw_Data_06032026/Most-Recent-Cohorts-Institution.csv', low_memory=False, usecols=cols)
df_cs.to_csv('data/final_datasets/College_Scorecard_Subset.csv', index=False)
print(f"Saved Scorecard Subset. Size: {os.path.getsize('data/final_datasets/College_Scorecard_Subset.csv') / (1024*1024):.2f} MB")

import nbformat as nbf

notebook_path = 'DATA102_Project_Group1.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code' and 'def clean_data(data):' in cell.source:
        cell.source = """import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('data/final_datasets/College_Scorecard_Subset.csv', low_memory=False)

def clean_data(data):
    df_clean = data.copy()
    
    # 1 & 2. Safely convert to float, automatically turning 'PrivacySuppressed', 'PS', or any string into NaN
    numeric_cols = ['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'SAT_AVG', 'GRAD_DEBT_MDN', 'ADM_RATE']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
    # 3. Drop rows missing target or primary predictor
    df_clean.dropna(subset=['MD_EARN_WNE_P10', 'TUITIONFEE_IN'], inplace=True)
    
    # 4. Impute remaining NaNs with Median (e.g., SAT_AVG)
    for col in numeric_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
            
    # 5. Outlier Detection (IQR Method) - Statistician's Addition
    Q1 = df_clean['MD_EARN_WNE_P10'].quantile(0.25)
    Q3 = df_clean['MD_EARN_WNE_P10'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    df_clean = df_clean[df_clean['MD_EARN_WNE_P10'] <= upper_bound] # Remove extreme high earners that skew correlation
            
    return df_clean

df_cleaned = clean_data(df)
print(f"Data Cleaning Complete. Remaining valid rows: {len(df_cleaned)}")
df_cleaned.head()"""

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook fixed.")

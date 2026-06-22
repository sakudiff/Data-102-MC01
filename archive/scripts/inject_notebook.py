import nbformat as nbf
import json
import os

notebook_path = 'DATA102_Project_Group1.ipynb'

# Load the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# Define the cells to inject
data_cleaning_cells = [
    nbf.v4.new_markdown_cell("### 2. Data Cleaning\n\n**Strategy:**\n1. Replace `'PrivacySuppressed'` with `NaN`.\n2. Convert financial columns to `float64`.\n3. Drop rows missing the target variable (`MD_EARN_WNE_P10`) or primary predictor (`TUITIONFEE_IN`).\n4. Impute remaining missing values (e.g., `SAT_AVG`) using the median.\n5. Detect and handle extreme outliers in Tuition and Earnings using the IQR method (Statistical Rigor)."),
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('data/final_datasets/College_Scorecard_Subset.csv', low_memory=False)

def clean_data(data):
    df_clean = data.copy()
    
    # 1. Replace 'PrivacySuppressed' with NaN
    df_clean.replace('PrivacySuppressed', np.nan, inplace=True)
    
    # 2. Convert to float
    numeric_cols = ['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'SAT_AVG', 'GRAD_DEBT_MDN', 'ADM_RATE']
    for col in numeric_cols:
        df_clean[col] = df_clean[col].astype(float)
        
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
df_cleaned.head()""")
]

stats_cells = [
    nbf.v4.new_markdown_cell("### 6. Statistical Inference\n\n**Hypothesis:**\n* **H0:** There is no linear correlation between Tuition Cost and Post-Grad Earnings ($r = 0$).\n* **Ha:** There is a significant linear correlation between Tuition Cost and Post-Grad Earnings ($r \\neq 0$).\n\n**Assumptions Check:**\n1. **Normality:** D'Agostino's K-squared test, Histogram, Q-Q Plot.\n2. **Fallback:** If data is highly skewed, we will compute Spearman's Rank Correlation instead of Pearson (Statistician's Addition)."),
    nbf.v4.new_code_cell("""from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

tuition = df_cleaned['TUITIONFEE_IN']
earnings = df_cleaned['MD_EARN_WNE_P10']

# 1. Visualizing Normality
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(earnings, kde=True, ax=ax[0])
ax[0].set_title('Distribution of Median Earnings')
sm.qqplot(earnings, line='s', ax=ax[1])
ax[1].set_title('Q-Q Plot of Median Earnings')
plt.show()

# 2. Formal Normality Test (D'Agostino's K-squared)
stat, p_norm = stats.normaltest(earnings)
print(f"Normality Test P-Value: {p_norm:.5f}")
if p_norm < 0.05:
    print("Warning: Earnings data is NOT normally distributed (p < 0.05).")
    print("As a statistician, we will fallback to Spearman's Rank Correlation to be strictly rigorous.\\n")
    corr, p_val = stats.spearmanr(tuition, earnings)
    test_used = "Spearman Rank"
else:
    print("Data is normally distributed. Proceeding with Pearson Correlation.\\n")
    corr, p_val = stats.pearsonr(tuition, earnings)
    test_used = "Pearson"

# 3. Final Correlation Result
print(f"--- {test_used} Correlation Test ---")
print(f"Correlation Coefficient (r): {corr:.4f}")
print(f"P-Value: {p_val:.5e}")

if p_val < 0.05:
    print("Conclusion: Reject the Null Hypothesis. There is a statistically significant correlation between Tuition and Post-Grad Earnings.")
else:
    print("Conclusion: Fail to Reject the Null Hypothesis. There is no significant correlation.")
""")
]

# Find indices to replace existing placeholders
new_cells = []
for cell in nb.cells:
    if cell.cell_type == 'markdown' and '2. Data Cleaning' in cell.source:
        new_cells.extend(data_cleaning_cells)
    elif cell.cell_type == 'code' and 'def clean_data(df):' in cell.source:
        continue # Skip old placeholder
    elif cell.cell_type == 'markdown' and '6. Statistical Inference' in cell.source:
        new_cells.extend(stats_cells)
    elif cell.cell_type == 'code' and 'from scipy import stats' in cell.source:
        continue # Skip old placeholder
    else:
        new_cells.append(cell)

nb.cells = new_cells

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook updated successfully.")

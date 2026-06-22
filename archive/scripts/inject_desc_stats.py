import nbformat as nbf

notebook_path = 'DATA102_Project_Group1.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

stats_cells = [
    nbf.v4.new_markdown_cell("### Descriptive Statistics Summary\n*Note: Our group is responsible for the statistical rigor of this dataset. Below are the core numerical summaries (central tendency, dispersion, and shape) for our primary variables before we dive into specific EDA questions.*"),
    nbf.v4.new_code_cell("""# 1. Standard Summary (Mean, Std, Min, Max, Quartiles)
desc_stats = df_cleaned[['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'SAT_AVG', 'GRAD_DEBT_MDN']].describe()

# 2. Add Median, Variance, Skewness, and Kurtosis
desc_stats.loc['median'] = df_cleaned[['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'SAT_AVG', 'GRAD_DEBT_MDN']].median()
desc_stats.loc['var'] = df_cleaned[['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'SAT_AVG', 'GRAD_DEBT_MDN']].var()
desc_stats.loc['skewness'] = df_cleaned[['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'SAT_AVG', 'GRAD_DEBT_MDN']].skew()
desc_stats.loc['kurtosis'] = df_cleaned[['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'SAT_AVG', 'GRAD_DEBT_MDN']].kurt()

# 3. Add Mode (Mode can return multiple values, so we take the first one)
desc_stats.loc['mode'] = df_cleaned[['MD_EARN_WNE_P10', 'TUITIONFEE_IN', 'SAT_AVG', 'GRAD_DEBT_MDN']].mode().iloc[0]

# Display the master descriptive statistics table
print("--- MASTER DESCRIPTIVE STATISTICS TABLE ---")
display(desc_stats.round(2))
""")
]

# Insert right before '### 3. Exploratory Data Analysis (EDA)'
new_cells = []
for cell in nb.cells:
    if cell.cell_type == 'markdown' and '3. Exploratory Data Analysis (EDA)' in cell.source:
        new_cells.extend(stats_cells)
    new_cells.append(cell)

nb.cells = new_cells

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Descriptive Stats injected.")

import nbformat as nbf

notebook_path = 'DATA102_Project_Group1.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code' and 'fillna' in cell.source:
        cell.source = cell.source.replace(
            "df_clean[col].fillna(df_clean[col].median(), inplace=True)",
            "df_clean[col] = df_clean[col].fillna(df_clean[col].median())"
        )

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Pandas Copy-on-Write warnings fixed.")

"""Fix corrupted notebook JSON from groupmate's raw markdown paste."""
import re, json, sys

with open('DATA102_Project_Group1.ipynb', 'r') as f:
    raw = f.read()

# Find the Insights TODO cell and where raw markdown was pasted after it
corrupt_start = raw.rfind('"### 7. Insights and Conclusions')
corrupt_md_start = raw.find('\n\n## 7.1', corrupt_start)

# Find the cell boundaries
cell_start = raw.rfind('{\n   "cell_type"', 0, corrupt_md_start)
cell_end = raw.find('\n  },\n  {', corrupt_md_start)
if cell_end < 0:
    cell_end = raw.rfind('\n  }\n]', corrupt_md_start)

# Rebuild with just the TODO placeholder
replacement = '''{
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 7. Insights and Conclusions\\n",
    "*TODO: Clearly state your insights and conclusions from the data to answer the research question.*"
   ]
  }'''

fixed = raw[:cell_start] + replacement + raw[cell_end:]

with open('DATA102_Project_Group1.ipynb', 'w') as f:
    f.write(fixed)

# Validate
try:
    nb = json.loads(fixed)
    print(f'Fixed. {len(nb["cells"])} cells valid.')
    for i, c in enumerate(nb['cells']):
        ct = c['cell_type']
        src = ''.join(c['source'])[:90].replace('\n', ' | ')
        print(f'  Cell {i} [{ct}]: {src}')
except json.JSONDecodeError as e:
    print(f'Still broken: {e}')
    sys.exit(1)

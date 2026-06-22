# Modeling Degree ROI Through University Financial Data

DATA102 machine case project (Section S30B, Group 1) at De La Salle University. The project evaluates whether published in-state tuition predicts median post-graduation earnings ten years post-entry using administrative institution-level data from the US Department of Education College Scorecard.

The analysis cleans the Scorecard dataset from 6,273 to 2,894 institutions, constructs institutional sector classifications and composite minority-serving indicators, and executes a D'Agostino K-squared normality test, Spearman rank-order correlation analysis, and a nested sequence of three Ordinary Least Squares (OLS) log-log regression models with HC3 jackknife heteroskedasticity-robust standard errors, alongside a selectivity sensitivity analysis on the admission-reporting sub-sample ($N = 1,466$).

## Repository Structure

```
.
├── DATA102_Project_Group1.ipynb   Companion analysis notebook with executed outputs
├── Paper/                         LaTeX source files, figures, bibliography, and compiled main.pdf
├── data/                          College Scorecard subset and derived analytical datasets
├── docs/                          Planning documentation and literature review PDFs
├── specs/                         Machine case project specifications
└── presentations/                 Slide decks and phase presentation PDFs
```

## Setup & Installation

The notebook runs on Python 3.12 with dependencies defined in `pyproject.toml`. Use `uv` to initialize the virtual environment.

```bash
uv sync
```

## Notebook Execution

To launch Jupyter and interact with the companion notebook:

```bash
uv run jupyter notebook DATA102_Project_Group1.ipynb
```

To execute the notebook headlessly and update all outputs in-place:

```bash
uv run python -c "import nbformat; from nbconvert.preprocessors import ExecutePreprocessor; nb = nbformat.read('DATA102_Project_Group1.ipynb', as_version=4); ep = ExecutePreprocessor(timeout=600, kernel_name='python3'); ep.preprocess(nb, {'metadata': {'path': './'}}); nbformat.write(nb, open('DATA102_Project_Group1.ipynb', 'w'))"
```

## Paper Compilation

The manuscript is written in LaTeX under `Paper/`. To compile the 42-page PDF document with `biber` bibliography:

```bash
cd Paper
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

`Paper/main.pdf` is the compiled output, building cleanly with zero LaTeX warnings or citation errors.

## Key Empirical Findings

- Baseline correlation between published in-state tuition and 10-year median earnings is moderate ($r_s = 0.464, p < .001$), explaining less than 22 percent of earnings rank variance.
- Baseline OLS tuition elasticity in Model 1 is $\beta_1 = 0.121$ ($R^2 = 0.187$), demonstrating that a 100 percent increase in tuition is associated with only a 12.1 percent increase in median earnings.
- Holding enrollment scale ($\log(1+\text{UGDS})$), predominant degree level (`PREDDEG`), and state fixed effects (`STABBR`) constant in Model 3 yields adjusted elasticities of $\beta = 0.189$ for public institutions, $\beta = 0.147$ for private nonprofits, and $\beta = 0.119$ for for-profit institutions ($R^2 = 0.582$).
- The sub-unity elasticities confirm diminishing relative returns to tuition pricing across all postsecondary sectors.

## Methodological References

The methodology and citations build on seven core empirical literature sources in `Paper/references.bib`:

- Dale and Krueger (2011)
- Faber (2017)
- Faber and Slantcheva-Durst (2021)
- Hotelling and Pabst (1936)
- MacKinnon and White (1985)
- Muse and Muse (2024)
- Pepinsky (2018)

## Authors & Group Members

- Antiado, Leonna F.
- Cuevas, Gheann Christie M.
- Divina, Precious Mae M.
- Martinez, Mikaella Kaye A.
- Sison, Aaron Joshua E.

Department of Software Technology, College of Computer Studies, De La Salle University.

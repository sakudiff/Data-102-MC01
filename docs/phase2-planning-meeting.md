# Phase 2 Planning Meeting

## Project Context

### Dataset

A subset of the US Department of Education College Scorecard containing 6,273 institutions and 24 variables. Each row represents one postsecondary institution. The data includes institutional characteristics, costs, student debt, and post-graduation earnings drawn from federal reporting requirements and matched tax records.

### Data Handling and Cleaning

The dataset went through a structured cleaning pipeline before analysis. Here is a summary of each step, the numbers affected, and the reasoning.

| Step | What Happened | Rows Affected | Why |
|---|---|---|---|
| Raw data | 6,273 institutions, 24 variables | — | College Scorecard subset via federal Title IV reporting. Earnings from de-identified Treasury tax records |
| PrivacySuppressed coercion | "PS" values in `GRAD_DEBT_MDN` converted to NaN | 1,228 values flagged | Small cohort sizes trigger privacy suppression. Coercing to NaN prevents misreading "PS" as a valid entry |
| Drop missing tuition or earnings | Listwise deletion on `TUITIONFEE_IN` and `MD_EARN_WNE_P10` | 2,915 rows removed | Research question requires both values. Missing these makes an institution unusable |
| Drop missing debt | Listwise deletion on `GRAD_DEBT_MDN` | 296 rows removed | Debt is a secondary variable. Dropping preserves complete cases for multi-variable models |
| Group-wise median imputation | Missing `UGDS` filled with per-sector median | 257 values imputed | Preserves sample size without distorting each sector's central tendency |
| Drop zero tuition | Removed institutions reporting $0 in-state tuition | 1 row removed | Zero tuition institutions distort the investment-return framing of the study |
| IQR outlier removal | Symmetric global IQR on earnings, per-sector IQR on tuition | 167 extreme values removed total | Prevents extreme observations from driving results. Per-sector trim respects different tuition distributions |
| **Final cleaned dataset** | **2,894 institutions, complete on all five key variables** | — | Ready for descriptive statistics, EDA, and modelling |

**Limitation.** PrivacySuppressed debt data is Missing Not At Random (MNAR). The final sample skews toward larger, more transparent institutions. Conclusions about debt should carry this caveat.

### Research Question

*After controlling for institutional selectivity, do colleges that charge higher tuition produce higher post-graduation earnings, and does this relationship differ across public, private nonprofit, and for-profit institutions?*

### Phase 1 Summary (Complete)

Six EDA questions established three key patterns:

1.  Earnings and tuition differ systematically by sector. Private nonprofits charge the most and earn the most. Publics charge the least yet produce competitive earnings. For-profits charge mid-range tuition but produce the lowest earnings.
2.  The within-sector tuition-earnings correlation is strongest among public institutions and weakest among for-profits.
3.  Debt burdens relative to earnings are substantially lighter for public graduates.

Statistical inference confirmed a significant Spearman correlation between tuition and earnings (p \< 0.05) after testing for normality via the D'Agostino K-squared test.

### Phase 2 Sections

| Section | Status | Owner |
|---------------------------------------|-----------------|-----------------|
| 6\. Data Modelling (3 models) | Scaffold ready | Aaron, Leonna, Mikaella |
| 7a. Insights | Scaffold ready | Gheann |
| 7b. Conclusions | Scaffold ready | Precious |
| Presentation slides (Phase 2 update) | Pending | All members |
| Final zip packaging | Pending Phase 2 | Aaron |

------------------------------------------------------------------------

## Meeting Agenda: Finalize Phase 2 Plan

### How the Three Models Answer the Research Question

The research question has three layers. Each model targets one layer.

| Model | Answers This Part of the Question | Why It's Needed |
|---|---|---|
| **Model 1: Baseline Regression** | *Do colleges that charge higher tuition produce higher post-graduation earnings?* | Establishes whether a significant relationship exists at all. Without this, the rest of the analysis has no foundation |
| **Model 2: Sector Interaction** | *Does this relationship differ across public, private nonprofit, and for-profit institutions?* | Tests whether the tuition-earnings slope is uniform or varies by sector. The interaction term is the statistical test for this |
| **Model 3: To Be Decided** | *Does the relationship hold after controlling for other factors?* | Acts as a robustness check. If the tuition coefficient survives after adding controls, the conclusion is stronger. If it collapses, the original relationship may be driven by confounding variables |

Together, the three models form a complete answer: existence of a relationship, variation across sectors, and robustness to additional controls.

### 1. Decide Model 3 Approach

Model 1 and Model 2 are regression-based and directly test the research question. Model 3 is open for the group to choose. Some options:

| Approach | What It Does | Why It Fits |
|------------------------|------------------------|------------------------|
| **Extended regression with covariates** | Add debt, enrollment, locale as controls | Tests if tuition-earnings relationship holds when other factors are accounted for |
| **K-means clustering** | Cluster institutions by tuition, earnings, debt | Answers: do natural groupings exist beyond sector labels? Maps back to EDA Q3 |
| **Decision tree / Random Forest** | Predict earnings tier (high/medium/low) from tuition, sector, debt | Non-linear alternative to regression, shows which variables matter most |
| **Logistic regression** | Predict whether an institution's graduates earn above or below median | Simpler interpretation, works with binned earnings |

Discuss which technique your instructor covered in class and which fits best. Update the notebook header and code scaffold once decided.

### 2. Confirm Model 1 (Baseline Linear Regression)

-   Log-transform `TUITIONFEE_IN` and `MD_EARN_WNE_P10` (both right-skewed)
-   Fit simple OLS regression: `log_earnings ~ log_tuition`
-   Report: R-squared, coefficient, p-value, RMSE
-   Diagnostics: residuals-vs-fitted plot, Q-Q plot

### 3. Confirm Model 2 (Sector Interaction Model)

-   One-hot encode `CONTROL` (Public, Private Nonprofit, For-Profit)
-   Fit regression with interaction: `log_earnings ~ log_tuition * sector`
-   F-test comparing Model 2 vs Model 1
-   Interaction plot showing separate regression lines per sector
-   Report per-sector slopes and significance

### 4. Clarify Insights and Conclusions

**Insights (Gheann)** should synthesize:
- What each model tells us (direction, magnitude, significance)
- How sector changes the story
- Whether adding controls changed the results
- Any surprising or non-obvious findings

**Conclusions (Precious)** should state:
- The direct answer to the research question
- Practical implications for students and policymakers
- Limitations of the analysis
- Suggested future directions

### 5. Slides and Submission

-   Who will update the Canva slides with Phase 2 content? (All members contribute their sections, one person assembles)
-   Deadline for individual code completion
-   Schedule for final review and zip packaging

------------------------------------------------------------------------

## Notes

-   We will be presenting phase one on Monday

-
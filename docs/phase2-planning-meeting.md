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

*Is there a significant relationship between in-state tuition and median post-graduation earnings, and does this relationship differ across public, private nonprofit, and for-profit institutions?*

### Phase 1 Summary (Complete)

Six EDA questions established three key patterns:

1.  Earnings and tuition differ systematically by sector. Private nonprofits charge the most and earn the most. Publics charge the least yet produce competitive earnings. For-profits charge mid-range tuition but produce the lowest earnings.
2.  The within-sector tuition-earnings correlation is strongest among public institutions and weakest among for-profits.
3.  Debt burdens relative to earnings are substantially lighter for public graduates.

Statistical inference confirmed a significant Spearman correlation between tuition and earnings (p \< 0.05) after testing for normality via the D'Agostino K-squared test.

### Phase 2 Sections

| Section | Status | Owner |
|---------------------------------------|-----------------|-----------------|
| 6a. Model 1: Baseline Log-Log Regression | Implemented | Leonna |
| 6b. Model 2: Sector Interaction Model | Implemented | Mikaella |
| 6c. Model 3: Institutional-Control Robustness Model | Implemented | Aaron |
| 7a. Insights | Scaffold ready | Gheann |
| 7b. Conclusions | Scaffold ready | Precious |
| Presentation slides (Phase 2 update) | Pending | All members |
| Final zip packaging | Pending Phase 2 | Aaron |

------------------------------------------------------------------------

## Meeting Agenda: Finalize Phase 2 Plan

### How the Three Models Answer the Research Question

The research question has three layers. Each model targets one layer.

| Model | Answers This Part of the Question | Assigned To |
|---|---|---|
| **Model 1: Baseline Log-Log Regression** | *Is tuition associated with post-graduation earnings across institutions overall?* | Leonna |
| **Model 2: Sector Interaction** | *Does this association differ across public, private nonprofit, and for-profit institutions?* | Mikaella |
| **Model 3: Institutional-Control Robustness Model** | *Does the sector-specific association remain after adjusting for enrollment, predominant degree, and state?* | Aaron |

Together, the three models form a complete answer: existence of a relationship, variation across sectors, and robustness to additional controls.

### 1. Final Model 3 Approach (Aaron)

Model 3 is an extended institution-level regression that preserves the Model 2 tuition-by-sector interaction and adds undergraduate enrollment, predominant degree, and state fixed effects. Guam, Puerto Rico, and the U.S. Virgin Islands are grouped as `US Territory` because Guam and the U.S. Virgin Islands otherwise have only one and two observations. The primary specification is:

`log_earnings ~ log_tuition * sector + log_enrollment + predominant_degree + state`

Faber and Slantcheva-Durst (2021, pp. 687–700) provide the closest peer-reviewed precedent. Their study relates College Scorecard earnings to fixed, compositional, and financial institutional characteristics. The open dissertation underlying the article defines institution-level earnings and identifies state, enrollment, and tuition among the explanatory variables before describing OLS estimation (Faber, 2017, pp. 41–45). Muse and Muse (2024, pp. 36–40) provide a second College Scorecard precedent using tuition, institutional type, size, degree offerings, geography, selectivity, and log earnings.

Graduate debt is not included in the primary model because debt may transmit part of tuition's relationship with later outcomes. Admission rate is added only in a disclosed sensitivity analysis. Only 1,466 of the 2,894 cleaned institutions report admission rate, including just 55 for-profit institutions. Two regressions are therefore estimated on the same restricted sample, first without admission rate and then with it. Muse and Muse (2024, pp. 35–37) document comparable missingness in institutional selectivity measures.

All three models use HC3 heteroskedasticity-consistent standard errors because their residuals reject constant variance. MacKinnon and White (1985, pp. 307–309) derive the jackknife-based HC3 covariance estimator. The models estimate conditional associations and do not identify causal effects.

### 2. Model 1 — Leonna (Baseline Log-Log Regression)

-   Log-transform `TUITIONFEE_IN` and `MD_EARN_WNE_P10`.
-   Fit `log_earnings ~ log_tuition` with HC3 standard errors.
-   Report the tuition elasticity, 95% confidence interval, p-value, R-squared, adjusted R-squared, and log RMSE.
-   Show the fitted relationship, residuals-versus-fitted plot, Q-Q plot, and Breusch-Pagan test.
-   Interpret the coefficient as an association, consistent with Faber's warning that institution-level correlational analysis does not establish cause and effect (Faber, 2017, pp. 43–46).

### 3. Model 2 — Mikaella (Sector Interaction Model)

-   Treat public institutions as the reference sector.
-   Fit `log_earnings ~ log_tuition * sector` with HC3 standard errors.
-   Use a joint robust Wald test for the two tuition-by-sector interaction terms.
-   Report the public, private nonprofit, and for-profit tuition elasticities with 95% confidence intervals and p-values.
-   Plot the three fitted log-log relationships. Muse and Muse (2024, pp. 36, 39) justify distinguishing the same institutional control types in College Scorecard earnings models.

### 4. Method References

Faber, A. (2017). *The impact of college attributes on the earnings of community college graduates* [Doctoral dissertation, University of Toledo]. OhioLINK Electronic Theses and Dissertations Center. http://rave.ohiolink.edu/etdc/view?acc_num=toledo151335572292832

Faber, A., & Slantcheva-Durst, S. (2021). The impact of community college attributes on the earnings of their students. *Community College Journal of Research and Practice, 45*(9), 687–700. https://doi.org/10.1080/10668926.2020.1798302

MacKinnon, J. G., & White, H. (1985). Some heteroskedasticity-consistent covariance matrix estimators with improved finite sample properties. *Journal of Econometrics, 29*(3), 305–325. https://doi.org/10.1016/0304-4076(85)90158-7

Muse, W. B., & Muse, I. (2024). College selectivity, choice of major, and post-college earnings. *Journal of Economic Analysis, 3*(2), 33–51. https://doi.org/10.58567/jea03020003

### 5. Clarify Insights and Conclusions

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

### 6. Slides and Submission

-   Who will update the Canva slides with Phase 2 content? (All members contribute their sections, one person assembles)
-   Deadline for individual code completion
-   Schedule for final review and zip packaging

------------------------------------------------------------------------

## Notes

-   We will be presenting phase one on Monday

-
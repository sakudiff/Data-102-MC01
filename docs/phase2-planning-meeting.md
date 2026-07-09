# Phase 2 Planning Meeting

## Project Context

### Dataset

A subset of the US Department of Education College Scorecard containing 6,273 institutions and 24 variables. Each row represents one postsecondary institution. The data includes institutional characteristics, costs, student debt, and post-graduation earnings drawn from federal reporting requirements and matched tax records.

### Research Question

*After controlling for institutional selectivity, do colleges that charge higher tuition produce higher post-graduation earnings, and does this relationship differ across public, private nonprofit, and for-profit institutions?*

### Phase 1 Summary (Complete)

Six EDA questions established three key patterns:

1. Earnings and tuition differ systematically by sector. Private nonprofits charge the most and earn the most. Publics charge the least yet produce competitive earnings. For-profits charge mid-range tuition but produce the lowest earnings.
2. The within-sector tuition-earnings correlation is strongest among public institutions and weakest among for-profits.
3. Debt burdens relative to earnings are substantially lighter for public graduates.

Statistical inference confirmed a significant Spearman correlation between tuition and earnings (p < 0.05) after testing for normality via the D'Agostino K-squared test.

### Phase 2 Sections

| Section | Status | Owner |
|---|---|---|
| 6a. Model 1: Baseline Linear Regression | Scaffold ready | Aaron |
| 6b. Model 2: Sector Interaction Model | Scaffold ready | Leonna |
| 6c. Model 3: To Be Decided | Scaffold ready | Mikaella |
| 7a. Insights | Scaffold ready | Gheann |
| 7b. Conclusions | Scaffold ready | Precious |
| Presentation slides (Phase 2 update) | Pending | All members |
| Final zip packaging | Pending Phase 2 | Aaron |

---

## Meeting Agenda: Finalize Phase 2 Plan

### 1. Decide Model 3 Approach (Mikaella leads, all decide)

Model 1 and Model 2 are regression-based and directly test the research question. Model 3 is open for the group to choose. Some options:

| Approach | What It Does | Why It Fits |
|---|---|---|
| **Extended regression with covariates** | Add debt, enrollment, locale as controls | Tests if tuition-earnings relationship holds when other factors are accounted for |
| **K-means clustering** | Cluster institutions by tuition, earnings, debt | Answers: do natural groupings exist beyond sector labels? Maps back to EDA Q3 |
| **Decision tree / Random Forest** | Predict earnings tier (high/medium/low) from tuition, sector, debt | Non-linear alternative to regression, shows which variables matter most |
| **Logistic regression** | Predict whether an institution's graduates earn above or below median | Simpler interpretation, works with binned earnings |

Discuss which technique your instructor covered in class and which fits best. Update the notebook header and code scaffold once decided.

### 2. Confirm Model 1 Implementation Details (Aaron)

- Log-transform `TUITIONFEE_IN` and `MD_EARN_WNE_P10` (both right-skewed)
- Fit simple OLS regression: `log_earnings ~ log_tuition`
- Report: R-squared, coefficient, p-value, RMSE
- Diagnostics: residuals-vs-fitted plot, Q-Q plot

### 3. Confirm Model 2 Implementation Details (Leonna)

- One-hot encode `CONTROL` (Public, Private Nonprofit, For-Profit)
- Fit regression with interaction: `log_earnings ~ log_tuition * sector`
- F-test comparing Model 2 vs Model 1
- Interaction plot showing separate regression lines per sector
- Report per-sector slopes and significance

### 4. Clarify Insights (Gheann) and Conclusions (Precious)

**Insights** should synthesize:
- What each model tells us (direction, magnitude, significance)
- How sector changes the story
- Whether adding controls changed the results
- Any surprising or non-obvious findings

**Conclusions** should state:
- The direct answer to the research question
- Practical implications for students and policymakers
- Limitations of the analysis
- Suggested future directions

### 5. Slides and Submission

- Who will update the Canva slides with Phase 2 content? (All members contribute their sections, one person assembles)
- Deadline for individual code completion
- Schedule for final review and zip packaging

---

## Pre-Work Before the Meeting

Everyone should have the repo cloned and the notebook open. The code scaffolds are on the `chore/roadmap-readme` branch (PR #1). Each person's code cell has their name in a comment at the top and a TODO describing what to implement.

```bash
git clone https://github.com/sakudiff/Data-102-MC01.git
cd Data-102-MC01
git fetch origin
git switch chore/roadmap-readme
```

## Notes

Use this document during the meeting to record decisions made, especially for Model 3. Update the notebook scaffolds immediately after decisions are finalized.

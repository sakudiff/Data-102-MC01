# Phase 1 Complete Review — Presentation Prep

> **Group 1** — Antiado, Cuevas, Divina, Martinez, Sison\
> **Section:** S30B \| **Course:** DATA102\
> **Notebook status:** Clean execution — all cells pass with zero errors

------------------------------------------------------------------------

## Slide Map

| Slide | Section in This Doc | Key Content |
|-----------------|----------------------------------|---------------------|
| Title + Title | — | Group members, project title |
| Libraries & Data Set | §1 | Dataset source, variables, libraries used |
| Data Cleaning | §2 | Full pipeline, every decision justified |
| EDA Overview | §3.0 | The 6 questions, what each examines |
| Q1: Earnings | §3.1 | Spearman r values, KDE + boxplot |
| Q2: Tuition | §3.2 | Medians, % above national median |
| Q3: Joint Tuition-Earnings | §3.3 | Scatter plot, sector correlations |
| Q4: Debt As Mediating | §3.4 | Debt-to-earnings ratios, debt ceiling |
| Q5: Selectivity | §3.5 | Elite-only premium, For-Profit negative r |
| Q6: MSI Profiles | §3.6 | Debt-to-earnings by MSI status |
| Research Question | §4 | RQ wording, how EDA motivated it |
| Statistical Inference | §5 | Hypotheses, Spearman result, defense |
| Thank You | — | — |

------------------------------------------------------------------------

## §1. Dataset & Libraries

**Corresponds to slide:** *Data Set & Libraries*

### Dataset Summary

| Property | Value |
|------------------------------------------|------------------------------|
| Source | US Department of Education College Scorecard |
| Raw rows | 6,273 institutions |
| Columns | 24 institutional and financial attributes |
| Collection method | Title IV federal reporting + Treasury tax records (de-identified) |
| Limitation | Only captures students who received federal aid AND had matched tax records |

### Key Variables Used

| Variable | What It Measures |
|---------------------------|---------------------------------------------|
| `TUITIONFEE_IN` | Published in-state tuition and fees |
| `MD_EARN_WNE_P10` | Median earnings 10 years after entry (among working, not enrolled) |
| `CONTROL` | Ownership: 1=Public, 2=Private Nonprofit, 3=For-Profit |
| `GRAD_DEBT_MDN` | Median graduate debt (federal + private loans) |
| `UGDS` | Total undergraduate enrollment |

### Libraries Used

| Library | Purpose |
|------------------------------------|------------------------------------|
| **Pandas & NumPy** | Data cleaning, manipulation, numerical operations |
| **Matplotlib & Seaborn** | Data visualization and exploratory analysis |
| **Scipy.stats** | Statistical testing: normality tests, Spearman correlation |
| **Statsmodels** | Statistical modeling and diagnostic tools |

### Variables Excluded & Why

| Variable | Missing Rate | Reason Excluded |
|-------------------|------------------------|------------------------------|
| `SAT_AVG` | 83.5% | Imputing majority of observations introduces more bias than it solves |
| `ADM_RATE` | 69.6% | Same rationale; used as sensitivity check in Q5 but not primary analysis |

### Full Variable List (all 24 columns)

- **UNITID** — Unique institution ID
- **INSTNM** — Institution name
- **CITY, STABBR** — Location
- **PREDDEG** — Predominant degree (0=non-degree, 4=graduate)
- **CONTROL** — Ownership (1=Public, 2=Private NP, 3=For-Profit)
- **LOCALE** — Urban-centric locale code
- **HBCU, PBI, ANNHI, TRIBAL, AANAPII, HSI, NANTI** — MSI flags (0/1)
- **MENONLY, WOMENONLY** — Single-gender flags
- **RELAFFIL** — Religious affiliation code
- **ADM_RATE** — Admission rate (proportion)
- **SAT_AVG** — Average SAT score
- **UGDS** — Undergraduate enrollment
- **TUITIONFEE_IN, TUITIONFEE_OUT** — Tuition
- **GRAD_DEBT_MDN** — Median graduate debt
- **MD_EARN_WNE_P10** — Median earnings 10 years post-entry

------------------------------------------------------------------------

## §2. Data Cleaning Pipeline

**Corresponds to slide:** *Data Cleaning*

### Complete Step Log

| Step | Action | Count Change | Running Total | Rationale |
|--------------|--------------|--------------|----------------|--------------|
| 1 | Load raw CSV | — | **6,273** | — |
| 2 | Coerce `GRAD_DEBT_MDN` 'PS' → NaN | 1,228 values coerced | 6,273 | PrivacySuppressed = institution opted not to report. MNAR mechanism. |
| 3 | Drop null `MD_EARN_WNE_P10` or `TUITIONFEE_IN` | **-2,915** | **3,358** | Core target variables missing — cannot analyze what we don't observe |
| 4 | Drop \$0 tuition | **-1** | **3,357** | Erroneous value — ROI framing requires positive cost baseline |
| 5 | Drop null `GRAD_DEBT_MDN` (after coercion) | **-296** | **3,061** | MNAR — remaining nulls after PS conversion are legitimately missing |
| 6 | Impute `UGDS` with per-CONTROL-group median | 257 imputed, 0 dropped | 3,061 | 8.4% missing — group median preserves sector central tendency |
| 7 | Drop duplicate `UNITID` | **-0** | 3,061 | No duplicates found |
| 8 | Global IQR on earnings | **-105** | **2,956** | Tukey fences \[\$11,818, \$84,278\]. Earnings distributions overlap across sectors — single fence appropriate |
| 9 | Per-group IQR on tuition | **-62** | **2,894** | Tuition distributions completely separated by sector (Public median \$5,981 vs Private \$33,928). Global fence would destroy valid data |

**Final cleaned dataset: 2,894 institutions (53.8% attrition)**

### Decision Justifications — Professor Defense

#### Why not impute the missing tuition/earnings?

The missingness is **MNAR (Missing Not at Random)** — schools that don't report earnings are systematically different (lower-performing, smaller, for-profit). Any imputation would bias toward reporting schools and give false confidence. Transparent reporting is the methodologically honest choice.

#### Why global IQR on earnings but per-group IQR on tuition?

- **Earnings** — distributions overlap substantially across sectors (all three KDE curves share the x-axis range). A single IQR fence is appropriate.
- **Tuition** — distributions are completely separated (Public median \$5,981, Private NP \$33,928). A single fence would flag legitimate private schools as outliers. Per-group IQR respects the **heterogeneous variance**.

#### Why median imputation for UGDS and not others?

UGDS was 8.4% missing — small enough that group-median imputation preserves central tendency without distorting variance. Target variables (tuition/earnings/debt) had 18-42% missing with systematic patterns.

#### The 53.8% attrition — is this still representative?

2,894 institutions is still a large sample. Most College Scorecard studies use similar cleaning because missingness is endemic to the dataset. The alternative — imputing 40%+ of target variables — introduces far more bias. The attrition is transparently documented in the transformation log.

------------------------------------------------------------------------

## §3. Exploratory Data Analysis — 6 Questions

**Corresponds to slide:** *EDA Overview + Q1–Q6 individual slides*

### §3.0 EDA Overview

The six questions move from univariate description to joint and contextual relationships, building toward the research question:

1. How do post-graduation earnings vary by sector?
2. How does in-state tuition vary by sector, and what share charges above the national median?
3. What patterns emerge when examining tuition and earnings jointly?
4. How does graduate debt relate to tuition and earnings across sectors?
5. Controlling for sector, does the tuition-earnings link hold among similarly selective schools?
6. Within each sector, do minority-serving institutions differ from non-MSIs?

------------------------------------------------------------------------

### §3.1 Q1 — Earnings Distribution by Sector

**Corresponds to slide:** *Earnings Distribution By Sector*

#### Numerical Summary

| Sector | Mean | Median | Std | IQR | Skewness |
|-------------------|----------|--------------|----------|----------|----------|
| Public | \$45,993 | **\$43,466** | \$10,269 | \$12,918 | 1.0 |
| Private Nonprofit | \$52,375 | **\$52,198** | \$13,368 | \$17,056 | 0.0 |
| For-Profit | \$38,274 | **\$37,480** | \$10,132 | \$11,419 | 1.0 |

#### Key Findings

- **Private NP** has highest mean (\$52,375) and median (\$52,198) earnings
- **For-Profit** trails significantly — median \$37,480 is \$5,986 below Public and \$14,718 below Private NP
- **Private NP** has widest dispersion (Std \$13,368, IQR \$17,056) — high variance, high risk/reward
- All sectors overlap — individual institutions span wide ranges, but central tendencies differ sharply

#### Professor Defense: "Why does Private NP have the lowest KDE peak?"

**Peak height = concentration, not magnitude.** Private NP has the lowest peak because its earnings are spread across the widest range (IQR \$17,056 — 47% wider than Public). The probability mass is diluted across a broader x-axis. Public has the tallest peak because 50% of public schools earn within a tight \$12,918 band. Private NP graduates earn the *most* (median \$52,198) — the flat peak just signals higher variance.

#### Visual Elements

- **Left**: KDE — Public (blue) tallest, For-Profit (red) second, Private NP (green) flattest/widest
- **Right**: Boxplot — Entire middle 50% of For-Profit (red box) sits below Public's box. Private NP box sits above both.

------------------------------------------------------------------------

### §3.2 Q2 — Tuition Distribution by Sector

**Corresponds to slide:** *Tuition Distribution By Sector*

#### Numerical Summary

| Sector | Mean | Median | Std | IQR | \% Above Nat'l Median |
|-----------|-----------|-----------|-----------|-----------|--------------------|
| Public | \$6,786 | **\$5,981** | \$3,572 | \$4,664 | **9.5%** |
| Private Nonprofit | \$33,370 | **\$33,928** | \$16,069 | \$23,741 | **91.2%** |
| For-Profit | \$15,934 | **\$16,326** | \$3,626 | \$4,225 | **84.4%** |
| **Overall** | \$18,065 | **\$12,221** | \$16,101 | \$19,101 | — |

#### Key Findings

- **Public**: Median \$5,981 — less than *half* the national median. Only 9.5% charge above it. Remarkably consistent pricing (IQR \$4,664).
- **Private NP**: Median \$33,928 — nearly **3× the national median**. 91.2% above. Massive variance (IQR \$23,741 \> Public's *entire* median).
- **For-Profit**: Median \$16,326 — deceptive middle ground. 84.4% above national median despite mid-tier pricing.
- **Skewness insight**: Public Mean (\$6,786) \> Median (\$5,981) = positive skew (flagship premium). Private NP Mean (\$33,370) \< Median (\$33,928) = negative skew (tail of affordable religious/regional colleges).

#### Professor Defense: "84.4% of For-Profits above the national median — doesn't that make them expensive?"

Yes, it does. For-Profit pricing is a paradox: they charge mid-tier prices (half of Private NP) but more than Public. 84.4% above national median proves they position as premium-priced, yet deliver the **lowest earnings**. That's the structural market failure.

#### Professor Defense: "Why per-group IQR for tuition outliers?"

Because Public and Private NP tuition distributions have almost no overlap. A single global IQR fence would flag a \$25k private school as an outlier when it's actually within the normal Private NP range. The `groupby().apply()` approach respects each sector's variance structure.

#### Visual Elements

- **Violin plot** with overall median line (\$12,221, red dashed)
- Public: squat, tight violin at bottom
- Private NP: tall, wide violin reaching \$80k
- For-Profit: pinched violin around \$16k

------------------------------------------------------------------------

### §3.3 Q3 — Joint Tuition-Earnings Relationship

**Corresponds to slide:** *Joint Tuition-Earnings Relationship*

#### Spearman Correlations

| Group | r | p-value | Interpretation |
|---------------|---------------|---------------|-----------------------------|
| **Overall** | **0.4641** | 1.53e-154 | Moderate positive — statistically significant |
| Public | **0.6286** | 4.29e-158 | **Strong** — steepest slope, tightest cluster |
| Private Nonprofit | **0.5874** | 2.14e-103 | Strong but enormous scatter around trendline |
| For-Profit | **0.3352** | 6.68e-11 | **Weak** — noisy cloud, shifted downward |

#### Key Findings

- All p-values effectively zero → relationship is real in all sectors
- **Public** (r=0.63): tightest link — tuition is a strong signal of quality in this sector
- **Private NP** (r=0.59): strong correlation but massive **unexplained variance** — at \$60k tuition, earnings range from \$30k to \$80k+
- **For-Profit** (r=0.34): only \~11% of earnings variance explained by tuition — the market signal is degraded

#### Professor Defense: "For-Profit r = 0.34 — what does that mean?"

Only \~11% of earnings variation is explained by tuition rank in For-Profit (vs \~40% in Public). The scatter plot shows a flat, noisy cloud shifted downward. Even when a For-Profit charges \$20k+, graduates earn \~\$40k — whereas a Public school charging \$20k would produce earnings of \$60k+. Within For-Profit, paying more does not reliably buy better outcomes.

#### Professor Defense: "Three distinct clusters?"

Yes. The scatter plot doesn't show a single continuum. Public schools cluster in the bottom-left (low tuition, moderate earnings), Private NPs in the top-right (high tuition, high earnings), For-Profits in the middle-left (mid tuition, low earnings). Switching sectors means switching to a **different cost-outcome curve** — not just a marginal price change.

#### Visual Elements

- Scatter plot with three colored clusters and regression lines
- Public (blue): tight, steep slope — compressed x-range
- Private NP (green): wide spread, flatter slope due to x-range stretching to \$80k
- For-Profit (red): flat, noisy cloud, lowest y-values

------------------------------------------------------------------------

### §3.4 Q4 — Debt as Mediating Variable

**Corresponds to slide:** *Debt As A Mediating Variable*

#### Spearman: Tuition vs Debt

| Sector | r (Tuition vs Debt) | p-value |
|-------------------|---------------------|-----------|
| Public | **0.7292** | 1.41e-237 |
| Private Nonprofit | **0.2739** | 1.87e-20 |
| For-Profit | **0.1114** | 3.46e-02 |

#### Debt-to-Earnings Ratios (Median)

| Sector | Median Ratio | Meaning |
|-------------------|--------------|--------------------------------------------|
| **Public** | **0.2896** | 29¢ debt per \$1 earnings — **healthiest** |
| Private Nonprofit | 0.4531 | 45¢ per \$1 |
| For-Profit | 0.4323 | 43¢ per \$1 |

#### Key Findings

- **Public** has the strongest tuition→debt link (r=0.73) — tuition passes through directly to student debt
- **Private NP** correlation is weak (r=0.27) due to the **debt ceiling effect** (see below)
- **For-Profit** correlation is essentially zero (r=0.11) — debt determined by factors other than tuition
- Public's debt-to-earnings ratio (0.29) is in a completely different tier from Private NP (0.45) and For-Profit (0.43)

#### Professor Defense: "What causes the debt ceiling effect?"

In Private NP schools, despite tuition scaling to \$80k+, median debt flatlines around \$25k. This is due to **federal Stafford loan caps** (\~\$31k aggregate for undergraduates). Once tuition exceeds what federal loans can cover, the *observable* debt can't increase — the remainder shifts to family out-of-pocket, Parent PLUS loans, or private loans not captured in this dataset. We're only seeing the *financed* portion of cost. The true burden is likely higher.

#### Professor Defense: "Private NP ratio (0.45) is slightly worse than For-Profit (0.43)?"

Yes — Private NP is technically the *worst* ratio, not For-Profit. But they arrive there via different paths: Private NP through high absolute debt (\$24,517), For-Profit through low absolute earnings (\$37,480). Both are in the same "distressed" tier.

#### Visual Elements

- **Left**: Tuition vs Debt scatter — Public tight cluster, Private NP ceiling effect visible as horizontal band at \$25k, For-Profit scattered
- **Right**: Bar chart of Debt-to-Earnings ratios — Public bar dramatically lower

------------------------------------------------------------------------

### §3.5 Q5 — Selectivity Stratification

**Corresponds to slide:** *Admissions Selectivity and Earnings by Sector*

#### Median Earnings by Selectivity × Sector

| Selectivity | Public | Private NP | For-Profit |
|-------------------------------|--------------|------------|------------|
| Highly selective (\<40%) | **\$68,726** | \$63,952 | \$40,359 |
| Moderately selective (40-70%) | \$54,764 | \$52,889 | \$38,174 |
| Less selective (\>70%) | \$53,250 | \$54,064 | \$34,657 |

#### Spearman Correlations (Reporting Subset)

| Sector | r | p-value |
|-------------------|-------------|----------|
| Public | **0.4043** | 3.37e-21 |
| Private Nonprofit | **0.5514** | 2.36e-73 |
| For-Profit | **-0.2803** | 0.038 |

#### Key Findings

- **Selectivity gradient**: More selective = higher earnings in every sector
- **The Private premium is an elite-only phenomenon**: At highly selective tier, Private NP (\$63,952) ≈ Public (\$68,726). At moderately/less selective tiers, they're virtually identical (\~\$53k). For 95% of students, Private NP offers **no earnings advantage** over Public.
- **For-Profit flips to negative**: r = -0.28 — charging higher tuition associates with *lower* earnings. But sample is tiny (n=3 highly selective, n=10 moderate).
- **Public correlation dropped**: 0.63 in full sample → 0.40 in reporting subset — suggests missing schools are systematically lower-earning

#### Professor Defense: "So the Private premium is fake?"

For the 95% of students who don't attend elite schools — **yes**. In the moderately and less selective tiers, Private NP and Public earnings are statistically indistinguishable (\$52,889–\$54,064 vs \$53,250–\$54,764). The Private premium observed in Q1 is entirely driven by the highly selective tier. But those schools admit \<40% of applicants.

#### Professor Defense: "For-Profit correlation went negative — is that real?"

r = -0.28, p = 0.038 — statistically significant. Within For-Profits that report admissions data, higher tuition is associated with *lower* earnings. This is the opposite of a functioning market. However, the sample is very small (n=54 total with ADM_RATE data), so interpret cautiously. The direction is alarming but the precision is low.

#### Sample Size Caveat

| Selectivity | Public | Private NP | For-Profit |
|----------------------|--------|------------|------------|
| Highly selective | 21 | 86 | **3** |
| Moderately selective | 100 | 275 | **10** |
| Less selective | 382 | 547 | **41** |

For-Profit Highly Selective (n=3) is statistically unreliable — treat that bar with extreme caution.

#### Visual Elements

- **Left**: Line chart — earnings drop as selectivity decreases, consistent across sectors
- **Right**: Scatter with regression lines — public and private NP still positive, For-Profit slightly negative

------------------------------------------------------------------------

### §3.6 Q6 — Minority-Serving Institution Profiles

**Corresponds to slide:** *Minority-Serving Institution Profiles by Sector*

#### Counts

| Sector | MSI | Non-MSI |
|-------------------|-------|---------|
| Public | 486 | 842 |
| Private Nonprofit | 231 | 809 |
| For-Profit | **0** | **269** |

#### Median Tuition, Earnings, and Debt

| Sector | MSI Status | Median Tuition | Median Earnings | Median Debt | **Debt/Earnings Ratio** |
|------------|------------|------------|------------|------------|--------------|
| **Public** | **MSI** | **\$5,193** | **\$43,172** | **\$11,631** | **0.269** |
| Public | Non-MSI | \$6,361 | \$44,298 | \$13,532 | 0.305 |
| Private NP | MSI | \$26,709 | \$49,669 | \$24,250 | **0.488** |
| Private NP | Non-MSI | \$35,860 | \$53,501 | \$24,736 | 0.462 |
| For-Profit | Non-MSI only | \$16,337 | \$36,642 | \$18,062 | 0.493 |

#### Key Findings

- **Zero For-Profit MSIs** — structural finding, not data error. For-profits don't meet federal MSI criteria or don't serve predominantly minority populations.
- **Public MSIs are the best value in the entire dataset**: Lowest tuition (\$5,193), lowest debt (\$11,631), best debt-to-earnings ratio (0.269).
- **Private NP MSIs are a trap within a trap**: They charge \$9,200 less tuition than non-MSIs, but graduates carry *the same debt* (\$24k+) and earn \$3,800 less. Their ratio (0.488) is tied with For-Profit (0.493).
- The tuition discount at Private MSIs doesn't translate to lower debt — likely because students come from lower-income backgrounds and borrow more for living expenses.

#### Professor Defense: "Are MSIs a good deal?"

**It depends on sector.** Public MSIs are the absolute best value: lowest tuition, lowest debt, healthiest ratio in the entire dataset. Private NP MSIs are the opposite: the tuition discount is real, but graduates end up with identical debt, lower earnings, and a worse debt-to-earnings ratio than non-MSIs. The "MSI discount" narrative oversimplifies.

#### Visual Elements

- **Left**: Tuition bar chart — MSI bars consistently lower within each sector
- **Right**: Earnings bar chart — MSI bars consistently lower
- For-Profit has only one bar (non-MSI only)

------------------------------------------------------------------------

## §4. Research Question

**Corresponds to slide:** *Research Question*

> **Is there a significant relationship between in-state tuition and median post-graduation earnings, and does this relationship differ across public, private nonprofit, and for-profit institutions?**

### How EDA Motivated This Question

1. **Q1 + Q2**: Earnings and tuition differ systematically by sector — Private NP charges the most and earns the most, Public charges the least yet produces competitive earnings, For-Profit charges mid-range but produces the lowest earnings
2. **Q3**: Within-sector tuition-earnings correlations vary dramatically — Public r=0.63, For-Profit r=0.34
3. **Q4**: Debt burdens relative to earnings are substantially lighter for Public graduates (ratio 0.29 vs 0.45)

### Why This Question Matters

- **Students/families**: Need to know whether higher tuition systematically translates to higher earnings within each sector
- **Policymakers**: Need evidence on whether the tuition-earnings link is uniform or sector-dependent, especially for regulating for-profit education

------------------------------------------------------------------------

## §5. Statistical Inference

**Corresponds to slide:** *Statistical Inference*

### Hypotheses

| Element | Statement |
|---------------------------------|---------------------------------------|
| H₀ | ρ = 0 (no monotonic correlation between tuition and earnings) |
| Hₐ | ρ ≠ 0 |
| α | 0.05 |
| Method | D'Agostino K-squared normality check → Spearman rank correlation |

### Results

| Test | Value |
|---------------------------------|---------------------------------------|
| D'Agostino K-squared p-value | **0.00000** |
| Decision after normality test | Data not normal → **Spearman** |
| Spearman correlation coefficient (r) | **0.4641** |
| p-value | **1.53 × 10⁻¹⁵⁴** |
| Conclusion | **Reject H₀** — statistically significant moderate positive monotonic relationship |

### Why Spearman, Not Pearson (Triple Defense)

| Layer | Evidence |
|------------------------------|------------------------------------------|
| **1. Statistical** | D'Agostino p = 0.00000 — formally rejects normality |
| **2. Visual** | Q-Q plot shows **platykurtic tails** (floor effect at low end, ceiling at high end). Histogram shows a **mixture distribution** — three modes from three sectors |
| **3. Theoretical** | Spearman captures any monotonic relationship (not just linear), robust to heteroscedasticity visible across sectors, no normality assumption |

### What the Global r = 0.4641 Actually Means

- A moderate-to-strong positive monotonic relationship across the full dataset
- But this is a **weighted average** of three very different sector-specific correlations (0.63, 0.59, 0.34)
- Public (49.4% of sample) dominates the global estimate
- The **sector-specific correlations** are more informative than the global number

### Professor Defense: "r² = 0.215 — does that mean 21.5% of variance explained?"

**Technically no — this is a vulnerability.** Spearman's r² is not the same as OLS R². Spearman measures *rank* association, not linear variance explained. The safe phrasing: *"A Spearman correlation of 0.46 indicates a moderate-to-strong positive monotonic relationship."* If pressed: "The true shared variance is difficult to quantify because the relationship is nonlinear and heteroscedastic across sectors. This is why we emphasize the sector-specific correlations over the global number."

### Key Numbers for the Slide

| Metric | Value |
|-------------------------|---------------------------|
| Normality test p-value | 0.0000 |
| Test used | Spearman rank correlation |
| Correlation coefficient | 0.4641 |
| p-value | 1.53 × 10⁻¹⁵⁴ |
| Decision | Reject H₀ |

------------------------------------------------------------------------

## §6. Key Numbers Cheat Sheet

### Cleaning Pipeline

| Metric | Value |
|--------------------------------|------------------------|
| Raw institutions | 6,273 |
| Final cleaned | 2,894 |
| Attrition rate | 53.8% |
| PrivacySuppressed debt records | 1,228 |
| Earnings IQR bounds | \[\$11,818, \$84,278\] |

### Sector Profile

| | Public | Private NP | For-Profit |
|-------------------------------|----------|------------|------------|
| Count | 1,430 | 1,104 | 360 |
| \% of sample | 49.4% | 38.1% | 12.4% |
| Median tuition | \$5,981 | \$33,928 | \$16,326 |
| Median earnings | \$43,466 | \$52,198 | \$37,480 |
| Median debt | \$12,250 | \$24,517 | \$18,668 |
| Debt/earnings ratio | **0.29** | 0.45 | 0.43 |
| \% above nat'l tuition median | **9.5%** | 91.2% | 84.4% |

### Critical Correlations (Spearman r)

| Relationship | Public | Private NP | For-Profit | Overall |
|---------------|---------------|---------------|---------------|---------------|
| Tuition vs Earnings | **0.6286** | 0.5874 | **0.3352** | 0.4641 |
| Tuition vs Debt | **0.7292** | 0.2739 | 0.1114 | — |
| Tuition vs Earnings (ADM_RATE subset) | 0.4043 | 0.5514 | **-0.2803** | — |

### Inference

| Test | Value |
|----------------------|---------------|
| D'Agostino p | 0.00000 |
| Spearman r (overall) | 0.4641 |
| p-value | 1.53 × 10⁻¹⁵⁴ |
| Decision | Reject H₀ |

------------------------------------------------------------------------

## §7. Professor Defense Kit

### Anticipated Questions and Answers

#### "53.8% attrition — is this still representative?"

**Answer:** 2,894 institutions is still a large sample. The 2,915 dropped for missing tuition/earnings are institutions that simply didn't report — we can't analyze what we don't observe. The remaining 464 removals are standard (outliers, +\$0 tuition, debt). Most College Scorecard studies use similar cleaning. The alternative — imputing 40%+ of target variables — introduces far more bias.

#### "Why didn't you impute the missing tuition and earnings?"

The missingness mechanism is **MNAR**. Schools that don't report earnings data are systematically different (smaller, for-profit, lower-performing). Imputation would bias toward reporting schools and give false precision. Transparent reporting is the honest approach.

#### "Why does Private NP have the lowest KDE peak?"

**Peak height = concentration, not magnitude.** Private NP has the flattest peak because its earnings are spread across the widest range (IQR \$17,056). The probability mass is diluted. Public has the tallest peak because 50% of schools earn in a tight \$12,918 band. Private NP graduates still earn the *most* (median \$52,198).

#### "What causes the debt ceiling?"

Federal Stafford loan caps (\~\$31k aggregate). Once Private NP tuition exceeds what federal loans cover, observable debt flatlines because the remainder shifts to family out-of-pocket or private loans not captured in this dataset. We're only seeing the financed portion.

#### "The Private premium is only for elite schools?"

**Yes.** Q5 proves it. At highly selective schools, Private NP earnings (\$63,952) ≈ Public (\$68,726). At moderately/less selective tiers, they're virtually identical (\~\$53k across both sectors). For 95% of students, Private NP offers no earnings advantage over Public — but with far higher tuition and debt.

#### "For-Profit correlation flipped to negative in Q5?"

r = -0.28, p = 0.038. Within For-Profits that report admissions data, higher tuition associates with lower earnings. Sample is small (n=3 highly selective, n=10 moderate) so precision is low, but the direction is a red flag.

#### "r² = 0.215 — 21.5% of variance explained?"

**Technically not for Spearman.** Spearman's r² doesn't equal OLS R². Safe phrasing: *"A Spearman correlation of 0.46 indicates a moderate-to-strong positive monotonic relationship."* The global number masks more interesting sector variation.

#### "What would you do with more time?"

- Moderated multiple regression with tuition × sector interaction (Phase 2)
- Fisher z-tests to compare pairwise correlation differences
- Sensitivity analysis re-weighting for PrivacySuppressed dropout
- Explore additional institutional controls

------------------------------------------------------------------------

## §8. Narrative Pillars — Three Core Takeaways

1. **Sector is the dominant stratifier.** Public, Private NP, and For-Profit operate on completely different cost-outcome curves. Switching sectors is not a marginal price change — it's a structural shift.

2. **For-Profit shows a broken market signal.** r = 0.34 tuition-earnings correlation (weakest), with 84.4% charging above national median yet delivering the lowest earnings. Within-sector, paying more doesn't reliably buy better outcomes.

3. **The Private premium exists only at elite schools.** At moderate and less selective tiers (95%+ of institutions), Public and Private NP earnings are indistinguishable. The "Private advantage" is entirely driven by the highly selective tier.

------------------------------------------------------------------------

## §9. Important Caveats & Limitations

| Limitation | Impact | Mitigation in This Study |
|-----------------|-----------------|--------------------------------------|
| PrivacySuppressed (MNAR) | 1,228 debt records systematically missing → sample biased toward transparent institutions | Acknowledged; framed as conservative choice |
| Cross-sectional data | Cannot establish causation — tuition doesn't *cause* higher earnings | Use associational language ("associated with," "predicts") throughout |
| Only federal aid recipients | Earnings may understate outcomes for higher-income students | Acknowledged in dataset description |
| ADM_RATE/SAT_AVG missingness | Q5 sample shrinks from 2,894 to \~1,900 | Used as sensitivity check, not primary analysis |
| Spearman r² ≠ OLS R² | "21.5% variance explained" is a rank-based approximation | Safe phrasing emphasizes "moderate-to-strong monotonic relationship" |

------------------------------------------------------------------------

## §10. Phase 2 Preview (TODO)

The notebook has placeholder cells for: - **§6 Data Modelling**: Multiple linear regression with tuition × sector interaction, log-transformed variables, robustness checks - **§7 Insights and Conclusions**: Synthesis of Phase 1 + Phase 2 into policy-relevant findings

**Rubric weight for Phase 2**: Data Modelling (20 pts) + Statistical Inference (20 pts) + Insights & Conclusions (10 pts) = 50 pts
# AAL Sales Analysis | Applied Data Science with Python

**Status: Final course-end report complete.** This project analyses AAL's Q4 2020 clothing sales using the original course-provided training dataset. The required submission format is a JupyterLab notebook.

## Primary report

**[AAL_Sales_Analysis.ipynb](notebooks/AAL_Sales_Analysis.ipynb)** is the final, reproducible notebook, following the assignment rubric in strict order:

1. **Data Wrangling:** inspection with isna()/notna(), data validity, missing-date handling, Min-Max normalization and GroupBy explanation.
2. **Data Analysis:** mean/median/mode/standard deviation, highest and lowest demographic and state totals, weekly/monthly/quarterly reports, regional and volume extensions.
3. **Data Visualization:** state vs demographic, demographic across states, time of day, daily/weekly/monthly/quarterly charts, Seaborn box plot and histogram, four-panel dashboard.
4. **Report Generation:** executive summary, methods, evidence tables, month/state analysis, targeted November promotional pilot, experimental evaluation, limitations and recommendations.

For a brief business-facing conclusion, see **[04_final_executive_summary.md](04_final_executive_summary.md)**. The more detailed draft experiment rationale is in **[04_november_promotion_proposal.md](04_november_promotion_proposal.md)**.

## Running the notebook

- **Simplilearn Practice Labs:** place `AAL_Sales_Analysis.ipynb` beside `AusApparalSales4thQrt2020.csv` and run all cells in JupyterLab.
- **Local project folder:** put the supplied original ZIP `1739523823_ausapparalsales4thqrt2020.zip` in `data/` and open `notebooks/AAL_Sales_Analysis.ipynb`. The loader detects `../data/`.
- The Python environment needs Pandas, Matplotlib, Seaborn, JupyterLab and a Python 3 kernel.

The GitHub notebook intentionally has **cleared execution outputs** to keep source reviewable. A separate complete downloadable package from the ChatGPT conversation includes the *executed* notebook, an offline HTML report, original untouched ZIP dataset, original course problem statement and an executive summary. The original course files are not published into this public GitHub repository.

## Evidence and analytical limits

- **7,560** recorded rows, **136,121** units and **340,302,500** recorded sales values; currency is unspecified.
- **7** states/territories, **4** customer groups and **3** dayparts. There is no ACT data.
- Every month has exactly **30** recorded days. The CSV lacks 31 October and 31 December 2020. Store closures are **not verified**, and missing days were not imputed or recorded as zero sales.
- Every source row obeys `Sales = 2,500 x Unit`; these columns are proportional. The source contains no customer baskets, receipts, margins, store counts, footfall or historical campaign costs.
- Victoria is the highest-sales state, WA the lowest; Men lead in demographic totals, Seniors are lowest; November has the lowest recorded monthly sales. Sales value alone cannot justify dropping a customer demographic or predict promotion profitability.
- The business proposal is to **pilot, measure, and evaluate incremental contribution profit** from a targeted November campaign, guarding against any December sales displacement.

## Other analysis notes

- [Initial inspection findings](01_inspection_findings.md)
- [Regional demographic analysis](02_regional_demographic_findings.md)
- [High/low recorded sales-volume analysis](02_spending_intensity_findings.md)
- [Visualization findings](03_visualization_findings.md)

## Review status

All four sections are complete and locally tested. The notebook was executed against the original input ZIP: **92 cells; 37 code cells; 11 rendered chart figures; zero execution errors**. A separate five-test report-validation suite passed. Changes remain in **[draft PR #1](https://github.com/sillymotives/Learning-and-Fun/pull/1)** until approved for merge.

## State-by-state daypart extension

[Detailed state × demographic × daypart analysis](04_state_group_daypart_findings.md) investigates all 84 combinations and identifies the Queensland Men evening shortfall, Victoria Seniors' absolute difference and state-specific counterexamples. A user-reviewed, fully executed Jupyter notebook with the two associated heatmaps is available in the conversation's downloadable analysis package. The existing final course notebook on this branch has not been replaced with an older revision.

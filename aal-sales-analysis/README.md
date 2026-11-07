# AAL Sales Analysis (AI Engineering course project)

This course assignment analyses AAL's recorded Australian apparel sales in Q4 2020.
The main Jupyter notebook follows the assignment rubric in order.

| Section | Status |
| --- | --- |
| 1. Data Wrangling | Complete: validation, missing-day decision, Min-Max normalization, GroupBy |
| 2. Data Analysis | Complete: descriptive statistics, state/group comparisons, regional demographic breakdown, weekly/monthly/quarterly reports, high/low sales-volume periods |
| 3. Data Visualization | Complete: state/group/daypart plots, daily/weekly/monthly/quarterly charts, box plot, histogram, dashboard |
| 4. Report Generation | Not started |

## Start here

- `notebooks/AAL_Sales_Analysis.ipynb` - main rubric-ordered notebook for Sections 1–3.
- `notebooks/01_data_inspection.ipynb` - earlier exploratory work; kept unchanged.
- `01_inspection_findings.md` - source checks and caveats.
- `02_regional_demographic_findings.md` - demographic patterns in the lower-selling areas and decision cautions.
- `02_spending_intensity_findings.md` - sales-volume comparisons, not customer-level spend.
- `03_visualization_findings.md` - Section 3 chart inventory, takeaways and caveats.
- `AAL_Section_3_Dashboard.png` - optional dashboard preview in the downloadable project package.
- `data/1739523823_ausapparalsales4thqrt2020.zip` - untouched original CSV archive.
- `sales_analysis_problem_statement.docx` - untouched course instructions.

## Run in JupyterLab

**Simplilearn Practice Labs:** upload `AAL_Sales_Analysis.ipynb` next to
`AusApparalSales4thQrt2020.csv`. Open the notebook and select `Run All Cells`.

**Local project:** open `notebooks/AAL_Sales_Analysis.ipynb` in JupyterLab.
Its loader can read the original ZIP at `../data/` without extraction.
Install Pandas and JupyterLab if your environment does not include them.

## Interpretation cautions

- The dataset has 7,560 records and omits 31 October and 31 December 2020.
- Holiday-related closure is a hypothesis, not an established finding.
- Source `Sales` currency is unspecified; do not assume AUD.
- Every row follows `Sales = Unit x 2500`. Normalized Units/Sales therefore match.
- The data includes seven geographic categories but no ACT, store counts or marketing spend.
- Every group supplies about one-quarter of its state sales; no segment can be responsibly dropped based solely on revenue.
- We do not have customer identifiers, receipts or transaction counts, so recorded-period volume is not average customer spend.
- Weekly reports use Monday-Sunday calendar weeks; first/last weeks cover partial Q4 periods.

## GitHub

https://github.com/sillymotives/Learning-and-Fun/pull/1

Changes to Sections 1 and 2 are staged in draft PR #1, not merged into main.
## Current status

**Section 3 is complete.** The Jupyter notebook includes a labelled four-panel dashboard and the required daily, weekly, monthly, and quarterly charts, with missing-date warnings. Section 4 (final report) remains to be completed.

## Section 4 recommendation candidate

The first agreed recommendation is a **controlled November promotion pilot**, potentially around Black Friday, with profitability, store-level controls and possible December sales displacement evaluated before rollout. This is a hypothesis to test, not an established cause of November's lower recorded revenue.

See **[November promotion pilot recommendation](04_november_promotion_proposal.md)** for evidence, design, metrics and limitations. Section 4's final report remains **unfinished**.

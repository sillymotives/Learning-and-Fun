# AAL Sales Analysis (AI Engineering course project)

This course assignment analyses AAL's recorded Australian apparel sales in Q4 2020.
The main Jupyter notebook follows the assignment rubric in order.

| Section | Status |
| --- | --- |
| 1. Data Wrangling | Complete: validation, missing-day decision, Min-Max normalization, GroupBy |
| 2. Data Analysis | Complete: descriptive statistics, group/state rankings, weekly/monthly/quarterly reports |
| 3. Data Visualization | Not started |
| 4. Report Generation | Not started |

## Start here

- `notebooks/AAL_Sales_Analysis.ipynb` - main notebook for Sections 1 and 2.
- `notebooks/01_data_inspection.ipynb` - earlier exploratory work; kept unchanged.
- `01_inspection_findings.md` - source checks and caveats.
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
- Weekly reports use Monday-Sunday calendar weeks; first/last weeks cover partial Q4 periods.

## GitHub

https://github.com/sillymotives/Learning-and-Fun/tree/main/aal-sales-analysis

Changes to Sections 1 and 2 are staged in draft PR #1, not merged into main.
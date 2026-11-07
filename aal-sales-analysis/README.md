# AAL Sales Analysis

Course-end project for **Applied Data Science with Python**.

## Purpose

Analyse AAL's Australian clothing sales for Q4 2020, comparing states/territories, customer groups, and sales times. Support evidence-based recommendations for AAL's sales and marketing team.

## Current work

- [01 · Data inspection notebook](notebooks/01_data_inspection.ipynb): raw file loading, null checks, type validation, duplicate checks, calendar completeness, sales/units relationship, Pandas GroupBy, and the first Seaborn chart.
- [Initial inspection findings](01_inspection_findings.md): verified figures and methodological cautions.

**Status:** Data inspection complete. Further statistical analysis and dashboard development remain to be done.

## Source materials

The course provides two source files: `1739523775_sales_analysis_problem_statement.docx` and `1739523823_ausapparalsales4thqrt2020.zip`, whose only member is `AusApparalSales4thQrt2020.csv`.

These **original binary/source files are not yet committed** to this GitHub folder. The course files were supplied in the ChatGPT conversation, and the notebook requires you to put the ZIP or CSV in `aal-sales-analysis/data/` when running locally. Do not commit altered source data as if it were raw.

## First notebook: running locally

1. Place the original ZIP (or extracted CSV) in `data/`.
2. Open `notebooks/01_data_inspection.ipynb` in JupyterLab.
3. Install `pandas`, `matplotlib` and `seaborn` if your Python environment lacks them.
4. Run all notebook cells, then compare the output with the [findings](01_inspection_findings.md).

## Planned course deliverables

1. **Wrangling:** report missing values, explain treatment decisions, and use normalization.
2. **Analysis:** descriptive statistics, GroupBy, weekly/monthly/quarterly aggregation.
3. **Visualizations:** state × group, group × state, time of day; daily/weekly/monthly/quarterly charts.
4. **JupyterLab report:** findings, methods, limitations and actionable recommendations.

**Methodology cautions:** two entire dates are missing from Q4, source currency is unspecified, the source does not include ACT, and every row has `Sales = Unit × 2,500`. See the findings file for details.

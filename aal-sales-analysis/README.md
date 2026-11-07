# AAL Sales Analysis

Course-end project for **Applied Data Science with Python**, based on the AAL Q4 2020 Australian apparel sales dataset.

## Start here: rubric-ordered notebook

**[AAL_Sales_Analysis.ipynb](notebooks/AAL_Sales_Analysis.ipynb)** is the main working notebook. It follows the course rubric in the requested order.

| Section | Status |
| --- | --- |
| **1. Data Wrangling** (a–d) | Implemented and tested |
| **2. Data Analysis** | Next |
| **3. Data Visualization** | Later |
| **4. Report Generation** | Last |

Section 1 covers missing and invalid value checks with `isna()`/`notna()`, a documented approach to handling missing records, Min-Max normalization of Unit and Sales, and `GroupBy()` with the grouping-vs-merging explanation.

**[01_data_inspection.ipynb](notebooks/01_data_inspection.ipynb)** remains as a separate exploration notebook, preserving the initial analysis and visualization. It is *not* the final assignment structure.

## How to run

- **In Simplilearn Practice Labs:** place `AAL_Sales_Analysis.ipynb` alongside `AusApparalSales4thQrt2020.csv` in JupyterLab's file browser. Open the notebook and run the cells in order.
- **In a local copy of this project:** place the supplied ZIP in `data/`, open `notebooks/AAL_Sales_Analysis.ipynb` in JupyterLab, and run its cells.

The original input files (the course problem statement DOCX and CSV ZIP) were supplied in the conversation; they are **not currently committed** to this GitHub repository.

## Data quality notes

- The original data has **7,560 rows** and no null cell values or duplicate business keys.
- There are **no records for 31 October or 31 December 2020**. Possible holiday closure/altered trading is an **unverified hypothesis**, not a confirmed explanation; reporting gaps are also possible.
- The original `Sales` values are always `Unit × 2,500`. Both normalized columns are therefore identical within floating-point precision.
- The source does **not** specify sales currency, and ACT does not appear in its state/territory records.

Additional inspection findings are in **[01_inspection_findings.md](01_inspection_findings.md)**. We will complete Sections 2–4 in order, with brief explanations accompanying each code cell.

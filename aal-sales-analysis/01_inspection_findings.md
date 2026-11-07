# AAL · Initial data inspection

**Source:** supplied `AusApparalSales4thQrt2020.csv` in the original ZIP, covering the recorded part of Q4 2020.

## Audit results

| Measure | Finding |
| --- | ---: |
| Rows / columns | 7,560 / 6 |
| Date coverage | 1 Oct–30 Dec 2020, 90 distinct dates |
| Missing Q4 dates | 31 Oct 2020 and 31 Dec 2020 |
| Missing or invalid cell values | 0 |
| Exact duplicate rows | 0 |
| Duplicate date × state × group × time keys | 0 |
| Records per observed day | 84 |
| States and territories represented | NSW, NT, QLD, SA, TAS, VIC, WA |
| Customer groups | Kids, Men, Women, Seniors |
| Day periods | Morning, Afternoon, Evening |
| Total sales | 340,302,500 (currency not specified) |
| Total units | 136,121 |
| Unit-to-sales relationship | Sales = 2,500 × Unit for every row |

## State/territory ranking

| Rank | State/territory | Recorded sales |
| ---: | --- | ---: |
| 1 | VIC | 105,565,000 |
| 2 | NSW | 74,970,000 |
| 3 | SA | 58,857,500 |
| 4 | QLD | 33,417,500 |
| 5 | TAS | 22,760,000 |
| 6 | NT | 22,580,000 |
| 7 | WA | 22,152,500 |

## Other summaries

**By group:** Men 85,750,000; Women 85,442,500; Kids 85,072,500; Seniors 84,037,500.

**By time:** Morning 114,207,500; Afternoon 114,007,500; Evening 112,087,500.

**By month:** October 114,290,000; November 90,682,500; December 135,330,000. Each month has 30 recorded days.

## Interpretation and caveats

This first audit identified no empty cells, parsing failures, duplicate business keys or negative sales. It did identify two *absent whole days*, which cannot be repaired responsibly without more information. The raw categorical fields require whitespace trimming.

Every recorded combination of the 90 observed days, seven geographic categories, four groups and three day periods is present: `90 × 7 × 4 × 3 = 7,560`.

State differences in sales alone do **not** prove relative store-level productivity or untapped market potential. The source provides no location count, marketing-spend, price variability, store footfall, or geographic population data. The Australian Capital Territory is not represented, and the source does not specify currency.

**Next:** justify treatment of the missing dates; descriptive statistics; Min–Max normalization (as required by the brief); weekly, monthly and quarterly reporting; Seaborn dashboards.

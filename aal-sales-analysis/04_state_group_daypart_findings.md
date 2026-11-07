# State-by-state demographic and daypart analysis | AAL Q4 2020

This is an **exploratory extension** to the final JupyterLab coursework report. The figures are from the supplied training dataset, not verified real-world retail activity. Its `Sales` currency is unspecified.

## How the comparison works

Every state × demographic × time-of-day combination has **90 recorded rows**. For each state and demographic group, calculate `Evening difference (%) = 100 × (Evening Sales ÷ average(Morning Sales, Afternoon Sales) − 1)`. Negative means Evening recorded less than its own other-daypart average. This is **not** lost sales and cannot be automatically recovered with discounts.

## Which groups have the largest relative evening shortfall in each state?

| State | Largest evening shortfall | Gap vs Morning/Afternoon | Difference in recorded sales value | Strongest evening relative group | Relative Evening gap |
|---|---|---:|---:|---|---:|
| NSW | Men | -2.83% | -181,250 | Seniors | -0.74% |
| NT | Women | -4.06% | -77,500 | Seniors | +7.24% |
| QLD | Men | -13.20% | -386,250 | Women | +0.54% |
| SA | Seniors | -7.33% | -368,750 | Men | +1.78% |
| TAS | Men | -5.87% | -115,000 | Kids | +3.95% |
| VIC | Seniors | -5.77% | -516,250 | Women | +1.75% |
| WA | Men | -4.24% | -82,500 | Women | +4.85% |

**Top candidates for investigation:** QLD Men (−13.20%, −386,250), SA Seniors (−7.33%, −368,750), and VIC Seniors (−5.77%, −516,250). VIC Seniors have the largest absolute evening deficit, QLD Men the largest relative percentage deficit. All figures are recorded sales values, not margins or opportunity forecasts.

**Groups with stronger evenings:** NT Seniors (+7.24%), NT Kids (+5.84%), and WA Women (+4.85%). These are not obvious targets for an evening discount, but their strength may be useful for assortment and staffing hypotheses.

## Detailed state × group × time-of-day results

| State | Demographic | Morning | Afternoon | Evening | Evening vs other-period average |
|---|---|---:|---:|---:|---:|
| NSW | Kids | 6,267,500 | 6,187,500 | 6,132,500 | -1.53% |
| NSW | Men | 6,290,000 | 6,512,500 | 6,220,000 | -2.83% |
| NSW | Seniors | 6,170,000 | 5,985,000 | 6,032,500 | -0.74% |
| NSW | Women | 6,420,000 | 6,425,000 | 6,327,500 | -1.48% |
| NT | Kids | 1,847,500 | 1,880,000 | 1,972,500 | +5.84% |
| NT | Men | 1,962,500 | 1,885,000 | 1,915,000 | -0.45% |
| NT | Seniors | 1,760,000 | 1,797,500 | 1,907,500 | +7.24% |
| NT | Women | 1,872,500 | 1,947,500 | 1,832,500 | -4.06% |
| QLD | Kids | 2,935,000 | 2,860,000 | 2,715,000 | -6.30% |
| QLD | Men | 2,845,000 | 3,007,500 | 2,540,000 | -13.20% |
| QLD | Seniors | 2,757,500 | 2,840,000 | 2,592,500 | -7.37% |
| QLD | Women | 2,900,000 | 2,640,000 | 2,785,000 | +0.54% |
| SA | Kids | 4,747,500 | 4,970,000 | 4,797,500 | -1.26% |
| SA | Men | 4,952,500 | 4,760,000 | 4,942,500 | +1.78% |
| SA | Seniors | 4,965,000 | 5,092,500 | 4,660,000 | -7.33% |
| SA | Women | 4,800,000 | 5,202,500 | 4,967,500 | -0.67% |
| TAS | Kids | 1,927,500 | 1,872,500 | 1,975,000 | +3.95% |
| TAS | Men | 1,885,000 | 2,030,000 | 1,842,500 | -5.87% |
| TAS | Seniors | 1,915,000 | 1,880,000 | 1,855,000 | -2.24% |
| TAS | Women | 1,797,500 | 1,887,500 | 1,892,500 | +2.71% |
| VIC | Kids | 8,950,000 | 8,787,500 | 8,622,500 | -2.78% |
| VIC | Men | 8,817,500 | 8,690,000 | 8,900,000 | +1.67% |
| VIC | Seniors | 9,057,500 | 8,830,000 | 8,427,500 | -5.77% |
| VIC | Women | 8,797,500 | 8,755,000 | 8,930,000 | +1.75% |
| WA | Kids | 1,842,500 | 1,945,000 | 1,837,500 | -2.97% |
| WA | Men | 2,007,500 | 1,882,500 | 1,862,500 | -4.24% |
| WA | Seniors | 1,950,000 | 1,770,000 | 1,792,500 | -3.63% |
| WA | Women | 1,767,500 | 1,685,000 | 1,810,000 | +4.85% |

## Monthly reliability check

- QLD Men: evening gaps of approximately −10.89% (October), −12.68% (November), and −15.32% (December), but below the other-daypart average on **55 of 90 days**.
- VIC Seniors: October evening +1.53%, November −11.13%, December −7.64%; this suggests a time-specific trial rather than treating all months alike.
- SA Seniors: October −16.95%, November −4.67%, December +1.26%. A strong quarterly shortfall can conceal changes of sign.
- At the **whole Queensland** level, November’s evening gap is relatively small, while **QLD Men** individually still have a −12.68% evening difference. State-level aggregation masks group-level variation.

## Recommended experiments (not proven outcomes)

1. **First pilot:** QLD Men during Evening, comparing appropriate control stores or equivalent customer audiences. Investigate stock, assortment and targeted creative before deciding whether a discount is necessary.
2. **Second pilot hypothesis:** VIC Seniors in November/December, where the evening shortfall is concentrated. Compare a limited offer to a controlled baseline; verify margins and accessibility.
3. **Third pilot hypothesis:** SA Seniors, especially in October, after checking whether the pattern repeats in additional years. Be careful about seasonal confounding.
4. **Avoid blanket discounts:** in NT, Seniors and Kids already skew more heavily toward Evening; in WA, Women’s Evening value exceeds other-daypart average.

Measure *incremental contribution profit* after promotion and operating costs, unit sales, stockouts, customer satisfaction, and whether a promotion merely shifts purchases across dayparts. The supplied data contains no transactions, store counts, customer-level spending, pricing changes, gross margins or previous campaigns. Do not claim causality, profitability or recoverable lost revenue.

## Data checks

- 7 states/territories × 4 demographic groups × 3 periods = 84 distinct cells; each has 90 rows.
- Grand total: **340,302,500** recorded sales values, reconciled to original CSV.
- Two whole dates have no data: 31 October and 31 December 2020. Do not fill them with zero.
- As a teaching dataset, this is appropriate for practicing analytics and designing testable marketing recommendations, not inferring actual Australian shoppers’ behaviour.
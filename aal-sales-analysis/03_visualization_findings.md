# AAL | Section 3 visualization findings

**Source:** AAL apparel sales CSV for Q4 2020. Sales units are recorded numeric values; the source does not specify currency.

## Visual checklist (all in the main Jupyter notebook)

- State × demographic sales heatmap, with numeric labels in millions
- Group-wise sales across states as grouped bars
- Morning/Afternoon/Evening sales totals and state daypart percentage heatmap
- Daily chart with gaps for missing 31 October and 31 December
- Weekly bars with partial weeks annotated by observed days
- Monthly bars for October, November and December
- Quarterly chart (Q4 only, one bar)
- Seaborn box plot and histogram for units per recorded row
- Four-panel executive dashboard

## Observed findings

| Measure | Recorded value |
|---|---:|
| Total Q4 sales | 340,302,500 |
| Days with records | 90 of 92 |
| Strongest state/territory | VIC: 105,565,000 |
| Lowest state/territory | WA: 22,152,500 |
| Morning sales | 114,207,500 |
| Afternoon sales | 114,007,500 |
| Evening sales | 112,087,500 |
| October | 114,290,000 |
| November | 90,682,500 |
| December | 135,330,000 |

**Time-of-day insight:** Morning is the peak *recorded* daypart and Evening the lowest. Morning's total is only about **1.89%** above Evening, so a major shift in marketing spending is not yet justified.

**Coverage:** October and December each have only 30 recorded days: 31 October (Halloween) and 31 December (New Year's Eve) have no rows. Closures are a hypothesis, not a confirmed explanation. Daily missing dates stay NaN, not zero.

**State and demographic:** All four demographic groups contribute materially in the lower-selling states. Compare group shares and margins before considering removal of a range.

**Data limitations:** The source does not show customer baskets, transactions, prices charged, margin, inventory, footfall, store counts, exact clock times, ACT or other quarters. Sales equals Unit × 2,500 throughout, so the two are not independent evidence of customer spending. No chart proves profit, purchase behaviour or causal campaign effects.

## Why these packages?

Seaborn handles heatmaps, box plots and distributions simply, as preferred by the assignment. Matplotlib helps with calendar-axis formatting, annotations and a clear four-panel dashboard. The charts use numeric values, labels and legends so colour is not the only guide.

**Carry forward to Section 4:** recommend small measurable marketing/assortment trials rather than dropping customer demographics or blanket discounts from revenue totals alone.

# AAL: higher-versus-lower recorded sales volume

**Part of rubric Section 2 (optional extension).** Source: the original Q4 2020 apparel sales CSV in `data/1739523823_ausapparalsales4thqrt2020.zip`.

## What can we actually measure?

Rows are aggregated **date × state/territory × customer group × time-of-day** records, not identified customers, visits, receipts or baskets. Sales always equals 2,500 × Unit in the data. We can therefore compare *unit volume and sales per recorded period*, but **not whether individuals spent more, bought larger baskets, or paid higher prices**. The currency is unspecified.

## Low-volume vs high-volume recorded periods

We classified each recorded period using its own state's unit quartiles. High means units at or above the 75th percentile; low means units at or below the 25th percentile; middle contains the rest. Threshold ties are included, so each band need not contain exactly a quarter of records.

| State/territory | Low cutoff (units) | High cutoff (units) | Low-volume share of state sales | High-volume share of state sales |
|---|---:|---:|---:|---:|
| Western Australia (WA) | 5 | 11 | 12.4% | 42.5% |
| Northern Territory (NT) | 6 | 11 | 18.1% | 43.5% |
| Tasmania (TAS) | 6 | 11 | 17.4% | 44.5% |
| Queensland (QLD) | 8 | 16 | 13.3% | 42.0% |

In WA, high-volume records (11+ units) generated **9,407,500** in recorded sales, while low-volume records (5 or fewer units) generated **2,737,500**. Those figures describe aggregated selling periods, not the amounts spent by individual people. All four demographic groups have similar shares of state sales; the evidence does not justify discontinuing any group.

## Implications for a sales programme

- Protect stock availability during high-volume time slots before adding incentives that may reduce margin on purchases that would have happened anyway.
- Investigate lower-volume periods, then test changes in promotions, assortment, messaging, or opening hours *with a control group* and a defined profitability metric.
- Check performance by demographic **within the same state**; do not confuse Victoria's greater recorded volume with higher average customer spending.
- To choose between targeting high-spending shoppers versus increasing smaller baskets, first obtain store count, transaction count, receipts/basket identifiers, prices paid, margins, returns and footfall (and customer-level information only where appropriate and lawful).

**Interpretation limit:** No causal effect or customer spending strategy can be identified from aggregated revenue and units alone. Compare incremental **profit**, not just revenue, before shifting a budget.
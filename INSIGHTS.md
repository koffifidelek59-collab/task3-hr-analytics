# Key Insights and Recommendations

**IBM HR Employee Attrition** &middot; 1,470 employees &middot; **KOUAME Koffi Fidèle**

---

## Headline figures

| KPI | Value | Why it is on this list |
| :--- | ---: | :--- |
| Headcount | 1,470 | The denominator for everything below |
| Attrition rate | 16.1% | 237 departures. The single number the board asks for |
| Median monthly income | 4,919 | Median, not mean: income is right-skewed |
| Average tenure | 7.0 years | Short tenure and high attrition are the same problem seen twice |
| Average age | 36.9 years | Frames the tenure figure |
| Overtime share | 28.3% | The strongest single lever, see Insight 1 |
| Departments / roles | 3 / 9 | The granularity every segment table uses |

---

## Insight 1. Overtime is the strongest single predictor, and it is a management choice

Employees working overtime leave at **30.5%**. Those who do not leave at
**10.4%**. That is a **2.93-fold difference**, the largest
produced by any single field in the dataset.

This matters more than the size of the gap. Age, marital status and job level are attributes
of the employee. Overtime is an **outcome of how work is allocated**, which means it is the
one strong factor the company directly controls.

**Recommendation.** Audit overtime by manager and by role before touching pay or benefits. The
28.3% of staff currently on overtime contain a disproportionate share of the
next twelve months' departures, and the lever is already in the company's hands.

## Insight 2. Risk factors compound, they do not add

Taken alone, each factor is a moderate risk. Combined they are not additive:

| Group | Headcount | Attrition |
| :--- | ---: | ---: |
| Company baseline | 1,470 | 16.1% |
| Works overtime | 416 | 30.5% |
| Overtime and job level 1 | 156 | 52.6% |
| **Overtime, level 1 and single** | **59** | **67.8%** |
| No overtime, level 2 and above | 667 | 7.3% |

**59 employees sit in a group where more than two in three leave**, a lift of
4.21 against the company rate. At the other end, 667 employees sit in a
group leaving at 7.3%.

**Recommendation.** Stop treating attrition as a company-wide average. It is
16.1% on paper and ranges from 7.3% to 67.8% in
practice. Target the 59 identified individuals rather than launching a general
engagement programme, which spends most of its budget on the 667 people who were
never going to leave.

## Insight 3. The first two years carry nearly half the departures

Employees with two years or less represent **23.3% of the workforce** but
**43.0% of all departures**. In the first year alone the rate reaches
**34.9%**, against 16.1% company-wide, and it falls
steadily with every tenure band thereafter.

This reframes the problem. It is not primarily a retention problem across the workforce; it is
an **onboarding and early-career problem** concentrated in a narrow window.

**Recommendation.** Move retention spending to the first 24 months: structured onboarding, an
assigned mentor, and a review at month 6 and month 18. An intervention at year five reaches a
population already leaving at half the company rate.

## Insight 4. Pay explains attrition at the bottom of the scale only

Median income among leavers is **3,202** against
**5,204** among those who stay, a gap of
**38%**.

But the effect is not linear. The lowest income quartile leaves at **29.3%**;
the other three sit between 10.3% and 14.2% and are barely distinguishable
from one another.

**Pay is a floor, not a ladder.** Below a threshold it drives departures; above it, further
increases buy very little retention.

**Recommendation.** Review the lowest quartile against the local market. Do not fund a
general pay rise: the data shows it would have almost no effect on the other three quartiles,
which together hold 1,101 employees.

## Insight 5. Satisfaction matters, and the company cannot currently measure performance

Employees in the lowest composite satisfaction band leave at **31.3%** against **2.4%** in the
highest. Of the individual scales, **work-life balance is the sharpest**: employees rating it
"Bad" leave at 31.2%, nearly double the company rate.

Against this, the performance dimension the brief asks about **cannot be analysed at all**.
`PerformanceRating` contains only the values 3 and 4, so no employee in 1,470 is rated
below 3. Its correlation with income is -0.017, indistinguishable from
zero. The scale cannot separate a strong performer from a weak one.

**Recommendation.** Two actions. First, work-life balance is the satisfaction dimension worth
acting on, and it connects directly to the overtime finding in Insight 1: they are likely the
same problem. Second, the performance rating process needs rebuilding before any
performance-based analysis is possible. A scale on which nobody scores below 3 is not
measuring performance.

---

## What the data cannot tell you

**No leaving date and no reason for leaving.** `Attrition` is a yes or no flag with no date
attached, so no departure trend over time can be computed and no voluntary resignation can be
separated from a dismissal. Every rate in this report is a snapshot.

**No manager identifier.** The overtime finding points at how work is allocated, but the data
cannot say by whom. Adding a manager key would make Insight 1 actionable at the level of the
individual team.

**No performance measure**, as set out above.

**Correlation, not causation.** These are observed associations in a snapshot of
1,470 employees. That overtime accompanies departure does not prove it causes it,
though the mechanism is plausible and the effect is large. Testing it requires a controlled
change, not more analysis of this file.

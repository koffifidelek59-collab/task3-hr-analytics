# Data Quality Report

**Dataset:** IBM HR Employee Attrition &middot; **KOUAME Koffi Fidèle** &middot; Data Analysis Internship

---

## 1. Summary

The file holds **1,470 employee records across 35 columns**. It arrives in
better condition than most HR extracts: **zero missing values, zero duplicate rows, zero
duplicate employee identifiers**, and every internal consistency rule passes.

That does not make it ready to analyse. Three defects were found, and none of them is a
missing value. Two would silently corrupt a conclusion; the third sends an analyst down a
dead end.

## 2. Checks that passed

| Check | Result |
| :--- | ---: |
| Missing values, all columns | **0** |
| Duplicate rows | **0** |
| Duplicate `EmployeeNumber` | **0** |
| Years at company exceeds total working years | **0** |
| Years in role exceeds years at company | **0** |
| Years with manager exceeds years at company | **0** |
| Last promotion predates the hire | **0** |
| Implied start of career before age 16 | **0** |
| Non-positive income | **0** |
| Satisfaction code outside 1 to 4 | **0** |

Every rule holds on all 1,470 records. No row was removed, because none needed to be.

## 3. Defect 1: three columns carry no information

| Column | Value on every row |
| :--- | :--- |
| `EmployeeCount` | 1 |
| `Over18` | Y |
| `StandardHours` | 80 |

A column with one distinct value cannot explain any difference between employees.

**Handling: dropped.** 35 columns become 32, then rise to
44 once the labelled scales and derived fields are added.

**Impact if left:** they inflate a correlation matrix and a feature list, and
`StandardHours = 80` invites the false conclusion that everyone works the same hours. The
`OverTime` column says otherwise for 28.3% of staff.

## 4. Defect 2: the performance scale is censored

`PerformanceRating` takes only the values **3 and 4**: 1,244 employees rated 3 and
226 rated 4. **Not one employee in 1,470 is rated below 3.** The scale is
documented as running from 1 to 4, and two thirds of it is empty.

**This is the defect that matters most for the task as briefed**, because the brief asks for
an analysis of performance. The column cannot separate a strong performer from a weak one:

- it cannot explain attrition,
- it cannot be related to pay, since the correlation between rating and monthly income is
  **-0.017**, indistinguishable from zero,
- and any claim that high performers are leaving would be unfounded.

**Handling: kept in the table, excluded from every conclusion,** with the reason stated
rather than the column quietly ignored. A reader who expects a performance finding is owed an
explanation of why there is none.

## 5. Defect 3: three pay columns are unrelated to pay

`MonthlyRate`, `DailyRate` and `HourlyRate` look like compensation fields. Their correlations
with `MonthlyIncome` are **+0.035**,
**+0.008** and **-0.016**.

An hourly rate bearing no relationship to monthly income is not a rate. These are synthetic
filler in the source dataset.

**Handling: excluded from every pay analysis.** `MonthlyIncome` is the only compensation field
used. An analyst who takes `HourlyRate` at face value produces a pay analysis that is entirely
noise, and nothing in the column name warns them.

## 6. Transformations applied

**Ordinal scales labelled.** Six columns store a coded rank. Stored as bare integers they
invite an average that means nothing, since the distance between "Medium" and "High" is not a
quantity. Each now has a labelled twin, so every chart reads without a codebook.

**Derived fields added:** an attrition flag, tenure bands, income quartiles, age bands and a
composite satisfaction score. The composite is the mean of the four satisfaction scales and is
used **only to band employees**, never reported as a quantity: averaging ordinal codes is
defensible for ranking and not for measurement.

## 7. Conclusion

**No row was deleted. All 1,470 records are retained.**

Three columns were dropped for carrying no information, three excluded from pay analysis for
being unrelated to pay, and one excluded from performance conclusions for being censored.

The substantive work was not repair. It was establishing that a file with no missing values
and no duplicates still contains three defects that a checklist-driven audit passes over
entirely.

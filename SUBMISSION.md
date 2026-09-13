# Task 3: Employee Data Analysis
## Submission Summary

**KOUAME Koffi Fidèle** &middot; Data Analysis Internship &middot; koffifidelek59@gmail.com
IBM HR Employee Attrition &middot; 1,470 employee records &middot; 35 columns

---

## The four required deliverables

| Required | Delivered | File |
| :--- | :--- | :--- |
| Cleaned dataset | 1,470 rows, labelled scales, derived analysis fields | `data/HR_Attrition_clean.csv` |
| Data analysis | Diagnosis, validation, fifteen segment tables | `Task3_HR_Analysis.ipynb`, `results/` |
| Visualisations | Six analytical figures | `charts/01` to `charts/06` |
| Interactive Power BI dashboard | One page, six KPIs, six visuals, four slicers | `powerbi/KOUAME_Koffi_Fidele_HR_Dashboard.pbix` |
| Key insights summary | Five insights, five recommendations | `INSIGHTS.md`, `report.pdf` |
| Data quality summary | Three defects found, each with its handling | `DATA_QUALITY.md` |

---

## The headline result

**Attrition is 16.1%, and that number is almost useless on its own.**
It ranges from **7.3%** to **67.8%** depending on three
questions asked about an employee.

| Group | Headcount | Attrition |
| :--- | ---: | ---: |
| Company baseline | 1,470 | 16.1% |
| Works overtime | 416 | 30.5% |
| Overtime and job level 1 | 156 | 52.6% |
| **Overtime, level 1 and single** | **59** | **67.8%** |
| No overtime, level 2 and above | 667 | 7.3% |

That is a list of **59 identifiable individuals** an HR team can work
through this quarter, rather than a company-wide engagement programme that would
spend most of its budget on the 667 employees leaving at 7.3%.

---

## Three defects found in a file that passes every routine check

The dataset has **zero missing values, zero duplicate rows**, and passes all eight
internal consistency rules. It was still not ready to analyse.

**1. Three columns carry no information.** `EmployeeCount`, `Over18` and
`StandardHours` hold one value on all 1,470 rows. Dropped.

**2. The performance scale is censored.** `PerformanceRating` contains only the
values **3 and 4**: no employee is rated below 3, and its correlation with income is
**-0.017**. **The performance analysis the brief requests cannot
be carried out.** This is reported rather than faked, and it is a finding about the
company's appraisal process.

**3. Three pay columns are not pay.** `MonthlyRate`, `DailyRate` and `HourlyRate`
correlate with actual monthly income at r below 0.04. Excluded from every pay figure.

**No row was deleted.** All 1,470 records are retained.

---

## The five insights

1. **Overtime is the strongest single predictor**, 30.5% against
   10.4%. It is also the only strong factor the company directly
   controls: the others are attributes of the employee.
2. **Risk factors compound rather than add**, as the table above shows.
3. **The first two years hold 23.3% of staff and
   43.0% of all departures.** This is an onboarding problem, not
   a company-wide retention problem.
4. **Pay is a floor, not a ladder.** The lowest income quartile leaves at
   29.3%; the other three sit between 10.3% and
   14.2% and barely differ.
5. **Work-life balance is the sharpest satisfaction scale**, and it connects directly
   to the overtime finding: they are likely the same problem.

---

## Contents of this folder

```
KOUAME_Koffi_Fidele_Task3/
├── SUBMISSION.md                  This file
├── report.pdf                     Formal report, 9 pages
├── INSIGHTS.md                    Insights and recommendations
├── DATA_QUALITY.md                Full audit
├── powerbi/
│   └── KOUAME_Koffi_Fidele_HR_Dashboard.pbix
├── dashboard.html                 Browser dashboard, no software required
├── Task3_HR_Analysis.ipynb        Colab-ready notebook, executed
├── analysis.py                    Cleaning, validation, analysis
├── dashboard.py                   Dashboard build script
├── POWERBI_GUIDE.md               How the Power BI page was built
├── POWERBI_THEME.json             The colour and formatting theme
├── VIDEO_RESOURCES.md             Reference material
├── data/
│   ├── HR_Attrition.csv           Original
│   ├── HR_Attrition_clean.csv     Cleaned
│   └── PowerBI_import.csv         Analysis table used by the .pbix
├── charts/                        Nine images, including the dashboard screenshots
└── results/                       Fifteen segment tables and the audit JSON
```

---

## Method in one paragraph

Nothing was modified before the problem was measured. The file was diagnosed first,
then types were fixed, then duplicates checked on the full record, then invalid values
handled, then the analysis fields derived. Every attrition figure is expressed as a
**lift** against the company baseline, because a rate on its own is not comparable
between segments, and headcount is reported beside every rate so a figure computed on
twelve people is never mistaken for a finding.

## What the data cannot answer

**No leaving date**, so no trend over time and no separation of resignation from
dismissal. **No manager identifier**, so the overtime finding cannot be traced to the
teams producing it, which is the single most valuable field to add. **No usable
performance measure**, as established above. And the dataset is **synthetic**: every
finding is a method demonstration until reproduced on the company's own records.

---

**Tools.** Power BI Desktop, Python 3, pandas, NumPy, Matplotlib, Seaborn, Plotly.

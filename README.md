# Task 3: Employee Data Analysis

**KOUAME Koffi Fidèle** &middot; Data Analysis Internship &middot; koffifidelek59@gmail.com

IBM HR Employee Attrition &middot; 1,470 employees &middot; 35 columns

---

## Contents

```
KOUAME_Koffi_Fidele_Task3/
├── KOUAME_Koffi_Fidele_HR_Dashboard.pbix   Interactive Power BI dashboard
├── Task3_HR_Analysis.ipynb                 Colab-ready notebook, executed, with all outputs
├── report.pdf                              Formal report, includes the dashboard screenshots
├── INSIGHTS.md                             Five insights and five recommendations
├── DATA_QUALITY.md                         Full audit: what was found and how it was handled
├── analysis.py                             Cleaning, validation and analysis, commented
├── data/
│   ├── HR_Attrition.csv                    Original file
│   ├── HR_Attrition_clean.csv              Cleaned dataset, 1,470 rows
│   └── PowerBI_import.csv                  Analysis table, ready for Power BI with no transformation
├── charts/                                 Six analysis figures, plus two Power BI dashboard screenshots, PNG
└── results/                                Fifteen segment tables and the audit JSON
```

## Start here

**The dashboard.** Open `KOUAME_Koffi_Fidele_HR_Dashboard.pbix` in Power BI Desktop.
Three slicers, department, overtime and gender, update **every KPI and every chart at
once**. Two screenshots of it are also in `charts/` and in `report.pdf`, for anyone
without Power BI Desktop installed.

**The notebook.** Open `Task3_HR_Analysis.ipynb` with the Colab badge at the top and run
every cell. Upload the dataset when prompted; the last cell downloads the outputs back to
your machine.

## On the Power BI requirement

The brief asks for a Power BI dashboard. `KOUAME_Koffi_Fidele_HR_Dashboard.pbix` is that
dashboard, built in Power BI Desktop against `data/PowerBI_import.csv`, which is already
cleaned and labelled so the model needed no Power Query transformation. The KPI cards,
the six charts and the key-insights panel mirror the findings and recommendations in
`report.pdf`.

## The short version

The file has **zero missing values, zero duplicates**, and passes all eight internal
consistency rules. It is still not ready to analyse. **Three defects, none of them a missing
value:**

1. **Three columns carry no information.** `EmployeeCount`, `Over18` and `StandardHours` hold
   one value on every row. Dropped.
2. **The performance scale is censored.** `PerformanceRating` contains only 3 and 4, so no
   employee in 1,470 is rated below 3, and its correlation with income is
   -0.017. **The performance analysis the brief asks for cannot be done**,
   and that is reported rather than faked.
3. **Three pay columns are not pay.** `MonthlyRate`, `DailyRate` and `HourlyRate` correlate
   with actual income at r below 0.04. Excluded from every pay figure.

**No row was deleted.**

## Headline findings

| Finding | Figure |
| :--- | ---: |
| Company attrition | 16.1% (237 of 1,470) |
| Works overtime, against not | 30.5% against 10.4% (2.93x) |
| Overtime + level 1 + single | **67.8%** on 59 employees (4.21x) |
| No overtime, level 2 and above | 7.3% on 667 employees |
| First two years | 23.3% of staff, 43.0% of departures |
| Lowest income quartile | 29.3% against 10.3% in the highest |

**The company rate of 16.1% is almost useless on its own.** It ranges from
7.3% to 67.8% depending on three questions about an employee.

## Method

| Stage | What was done |
| :--- | :--- |
| Diagnosis | Missing values, duplicates, constant columns, and a distribution check on every ordinal scale. Nothing modified |
| Cleaning | Constant columns dropped, six ordinal scales labelled, types set, six analysis fields derived |
| Validation | Eight internal consistency rules, plus a correlation test on the three rate columns |
| Analysis | Attrition rate and **lift** for fifteen segments, with headcount reported beside every rate |
| Charts | Six figures, each carrying the company baseline, because a rate without its reference is not interpretable |

## Reproducing

### Option A. The notebook in Colab, recommended

Open `Task3_HR_Analysis.ipynb` with the badge at the top, then **Runtime**, then
**Run all**. Upload the dataset when the picker appears. The last cell downloads the
clean dataset, the charts and the tables back to your machine.

### Option B. The scripts in Colab

Paste this into a single Colab cell:

```python
# 1. Upload the two files: HR_Attrition.csv, analysis.py
from google.colab import files
files.upload()

# 2. Run the analysis
!python analysis.py

# 3. Download everything
import shutil
shutil.make_archive("Task3_outputs", "zip", ".", "charts")
files.download("data/HR_Attrition_clean.csv")
files.download("Task3_outputs.zip")
```

`analysis.py` writes the cleaned table, the segment tables and the six charts. The
Power BI dashboard is built separately, in Power BI Desktop, against
`data/PowerBI_import.csv`.

### Option C. Locally

```bash
pip install pandas numpy matplotlib seaborn
python analysis.py      # cleaning, validation, analysis, six charts
```

### Three things that used to break in Colab, and no longer do

**Missing output folders.** Colab starts with an empty filesystem. The scripts
created `data/` but assumed `results/` and `charts/` already existed, which is true
on a developer machine and false in a fresh session. All three folders are now
created at the top of the script.

**An unhelpful crash when the data file was absent.** The file lookup used
`next(...)` with no default, which raises `StopIteration` with no message. It now
searches six locations, offers an upload picker in Colab, and if all else fails
prints the list of paths it searched.

**No guard on the run order.** An earlier version split cleaning and analysis across
two scripts, and the second read files the first had not always written yet. Both
steps are now in `analysis.py`, in the right order, so this class of error can no
longer occur.

## Tools

Python 3, pandas, NumPy, Matplotlib, Seaborn &middot; Power BI Desktop for the dashboard.

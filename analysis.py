# -*- coding: utf-8 -*-
"""
Task 3: Employee data analysis, IBM HR Attrition
================================================

Every section states its INPUT, its METHOD and its OUTPUT before the code, and
defines each term the first time it appears.

Reading order: load, clean, validate, analyse, plot. Diagnosing after correcting
would report the wrong counts, which is why nothing is modified in section 2.

Outputs
-------
data/HR_Attrition_clean.csv   the cleaned, labelled table
results/*.csv                 the aggregate tables behind every chart
results/findings.json         every figure quoted in the report and dashboard
charts/*.png                  the figures
"""
import json, os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# ---------------------------------------------------------------- house style
# One blue scale. Dark blue marks the value to look at first, lighter blues carry
# context, amber is reserved for the value that needs attention. A categorical
# rainbow would imply the groups differ in kind, when here they differ only in
# magnitude. The grid is drawn behind the bars, otherwise grid lines cross them
# and leave white stripes that read as missing data.
NAVY, BLUE, MID, LIGHT, PALE = "#12395E", "#1F6FB2", "#6BAED6", "#9ECAE1", "#DEEBF7"
AMBER, TEAL = "#E08A1E", "#17A2A2"
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 180, "figure.facecolor": "white",
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlepad": 10,
    "axes.labelsize": 11, "axes.edgecolor": "#3A3A3A", "axes.linewidth": 0.9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#E3E8ED", "grid.linewidth": 0.8,
    "axes.axisbelow": True, "legend.frameon": False, "legend.fontsize": 10,
    "xtick.labelsize": 10, "ytick.labelsize": 10})
sns.set_palette([BLUE, MID, LIGHT, NAVY])
F = {}   # every figure quoted downstream

# =============================================================================
# 1. LOAD
# -----------------------------------------------------------------------------
# INPUT  : HR_Attrition.csv, the file as supplied
# METHOD : read once, keep the original for the duplicate check in section 2
# OUTPUT : raw and df
# =============================================================================
# Colab starts with an empty filesystem and a different working directory, so
# every output folder is created here rather than assumed to exist. Omitting this
# is the single most common reason a script that runs locally fails in Colab.
for _folder in ["data", "results", "charts"]:
    os.makedirs(_folder, exist_ok=True)

# Locate the data file. Searching, then prompting for an upload, keeps the script
# portable: a hard-coded path runs on the author's machine and nowhere else.
_IN_COLAB = "google.colab" in sys.modules
_CANDIDATES = ["HR_Attrition.csv", "data/HR_Attrition.csv",
               "/content/HR_Attrition.csv",
               "WA_Fn-UseC_-HR-Employee-Attrition.csv",
               "/content/WA_Fn-UseC_-HR-Employee-Attrition.csv",
               "/content/drive/MyDrive/HR_Attrition.csv"]
CSV = next((p for p in _CANDIDATES if os.path.exists(p)), None)

if CSV is None and _IN_COLAB:
    print("Dataset not found in this session. Please upload it now.")
    from google.colab import files
    CSV = next(iter(files.upload()))

if CSV is None:
    raise FileNotFoundError(
        "The HR attrition CSV was not found.\n"
        "Searched: " + ", ".join(_CANDIDATES) + "\n"
        "In Colab, upload it when prompted or mount your Drive with:\n"
        "    from google.colab import drive; drive.mount('/content/drive')")

print(f"Running in Colab : {_IN_COLAB}")
print(f"Data file        : {CSV}")
raw = pd.read_csv(CSV)
df = raw.copy()
F["rows"], F["cols_raw"] = len(df), df.shape[1]
print(f"Loaded {len(df):,} employee records, {df.shape[1]} columns")

# =============================================================================
# 2. DIAGNOSIS, before anything is changed
# -----------------------------------------------------------------------------
# INPUT  : df
# METHOD : missing values, duplicates, and a search for columns that carry no
#          information at all
# OUTPUT : the diagnosis block of F
#
# Term. A CONSTANT COLUMN holds the same value on every row. It cannot explain
# any difference between employees, so it adds width to the table and nothing to
# the analysis. Finding these is part of cleaning, not an optimisation.
# =============================================================================
F["missing_total"] = int(df.isna().sum().sum())
F["dup_full"] = int(df.duplicated().sum())
F["dup_id"] = int(df["EmployeeNumber"].duplicated().sum())
CONSTANT = [c for c in df.columns if df[c].nunique() == 1]
F["constant_cols"] = {c: str(df[c].iloc[0]) for c in CONSTANT}
print(f"\nMissing values      : {F['missing_total']}")
print(f"Duplicate rows      : {F['dup_full']}")
print(f"Duplicate employee id: {F['dup_id']}")
print(f"Constant columns    : {F['constant_cols']}")

# The censored performance scale. This is the second structural defect and the
# one a routine audit misses, because the column looks perfectly valid.
F["perf_values"] = sorted(int(v) for v in df.PerformanceRating.unique())
F["perf_counts"] = {int(k): int(v) for k, v in df.PerformanceRating.value_counts().items()}
F["perf_income_corr"] = round(float(df.PerformanceRating.corr(df.MonthlyIncome)), 3)
print(f"\nPerformanceRating values present: {F['perf_values']}")
print("  No employee is rated below 3. The scale is censored at the bottom, so")
print("  it cannot separate a strong performer from a weak one.")

# =============================================================================
# 3. CLEANING
# -----------------------------------------------------------------------------
# INPUT  : df, 35 columns with ordinal scales stored as bare integers
# METHOD : drop the constant columns, label the ordinal scales, set the types,
#          and derive the analysis fields
# OUTPUT : a cleaned df and data/HR_Attrition_clean.csv
#
# Term. An ORDINAL SCALE is a coded rank: 1 to 4 here, where 4 is better than 3
# but the distance between them is not a quantity. Stored as a bare integer it
# invites an average that means nothing. Labelling it makes every chart readable
# without a codebook and stops the mean being taken by accident.
# =============================================================================
df = df.drop(columns=CONSTANT)
print(f"\nDropped {len(CONSTANT)} constant columns, {df.shape[1]} remain")

SCALE4 = {1: "1 Low", 2: "2 Medium", 3: "3 High", 4: "4 Very High"}
WLB    = {1: "1 Bad", 2: "2 Good", 3: "3 Better", 4: "4 Best"}
EDU    = {1: "1 Below College", 2: "2 College", 3: "3 Bachelor",
          4: "4 Master", 5: "5 Doctor"}
LABELS = {"JobSatisfaction": SCALE4, "EnvironmentSatisfaction": SCALE4,
          "RelationshipSatisfaction": SCALE4, "JobInvolvement": SCALE4,
          "WorkLifeBalance": WLB, "Education": EDU}
for col, mapping in LABELS.items():
    df[col + "_label"] = df[col].map(mapping).astype("category")

for c in df.select_dtypes(include="str").columns:
    df[c] = df[c].astype("string").str.strip()
for c in ["Attrition", "BusinessTravel", "Department", "EducationField",
          "Gender", "JobRole", "MaritalStatus", "OverTime"]:
    df[c] = df[c].astype("category")

# Derived fields used throughout.
df["attrition_flag"] = (df.Attrition == "Yes").astype(int)
df["tenure_band"] = pd.cut(df.YearsAtCompany, [-1, 1, 2, 5, 10, 100],
                           labels=["Under 1 year", "1 to 2", "3 to 5",
                                   "6 to 10", "Over 10"])
df["income_quartile"] = pd.qcut(df.MonthlyIncome, 4,
                                labels=["Q1 lowest", "Q2", "Q3", "Q4 highest"])
df["age_band"] = pd.cut(df.Age, [17, 25, 35, 45, 60],
                        labels=["18 to 25", "26 to 35", "36 to 45", "46 to 60"])

# A COMPOSITE SATISFACTION SCORE: the mean of the four satisfaction scales. It is
# used only to band employees, never reported as a quantity, because averaging
# ordinal codes is defensible for ranking and not for measurement.
SAT = ["JobSatisfaction", "EnvironmentSatisfaction",
       "RelationshipSatisfaction", "WorkLifeBalance"]
df["satisfaction_mean"] = df[SAT].mean(axis=1)
df["satisfaction_band"] = pd.cut(df.satisfaction_mean, [0, 2, 2.75, 3.5, 4],
                                 labels=["Low", "Below average", "Good", "High"])

os.makedirs("data", exist_ok=True)
df.to_csv("data/HR_Attrition_clean.csv", index=False)
F["cols_clean"] = df.shape[1]
print(f"Clean table written: {len(df):,} rows x {df.shape[1]} columns")

# =============================================================================
# 4. VALIDATION
# -----------------------------------------------------------------------------
# INPUT  : the cleaned df
# METHOD : eight rules that must hold if the records are internally consistent
# OUTPUT : the validation block of F
#
# Term. An INTERNAL CONSISTENCY RULE relates two fields that cannot contradict
# each other. Years at the company cannot exceed total working years; a promotion
# cannot predate the hire. A breach is a defect, never a business event.
# =============================================================================
V = {
 "years_at_company_gt_total": int((df.YearsAtCompany > df.TotalWorkingYears).sum()),
 "years_in_role_gt_at_company": int((df.YearsInCurrentRole > df.YearsAtCompany).sum()),
 "years_with_manager_gt_at_company": int((df.YearsWithCurrManager > df.YearsAtCompany).sum()),
 "promotion_gt_at_company": int((df.YearsSinceLastPromotion > df.YearsAtCompany).sum()),
 "age_minus_working_years_lt_16": int(((df.Age - df.TotalWorkingYears) < 16).sum()),
 "income_le_0": int((df.MonthlyIncome <= 0).sum()),
 "rate_inconsistent": int((df.MonthlyRate < df.DailyRate).sum()),
 "satisfaction_out_of_range": int((~df[SAT].isin([1, 2, 3, 4]).all(axis=1)).sum()),
}
F["validation"] = V
print("\nINTERNAL CONSISTENCY")
for k, n in V.items():
    print(f"  {k:<34} {n:>5}")
print("\n  MonthlyRate and DailyRate are unrelated to MonthlyIncome in this file:")
for c in ["MonthlyRate", "DailyRate", "HourlyRate"]:
    F[f"corr_income_{c}"] = round(float(df.MonthlyIncome.corr(df[c])), 3)
    print(f"    corr(MonthlyIncome, {c:<12}) = {F[f'corr_income_{c}']:+.3f}")
print("  They are synthetic filler and are excluded from every pay analysis.")
json.dump(F, open("results/findings.json", "w"), indent=2, default=str)

# =============================================================================
# 5. ANALYSIS
# -----------------------------------------------------------------------------
# INPUT  : the validated df
# METHOD : the attrition rate within every segment, expressed as a LIFT against
#          the company baseline
# OUTPUT : the aggregate tables in results/ and the findings block of F
#
# Term. LIFT is the attrition rate of a group divided by the company rate. A lift
# of 2.0 means the group leaves twice as often as the company average. A rate on
# its own is not actionable, because 20% is alarming in one company and normal in
# another; a lift is comparable across segments and is what makes the ranking
# below meaningful.
# =============================================================================
BASE = df.attrition_flag.mean()
F["headcount"] = int(len(df))
F["leavers"] = int(df.attrition_flag.sum())
F["attrition_rate"] = round(100 * BASE, 1)
F["avg_income"] = float(df.MonthlyIncome.mean())
F["median_income"] = float(df.MonthlyIncome.median())
F["avg_tenure"] = round(float(df.YearsAtCompany.mean()), 1)
F["avg_age"] = round(float(df.Age.mean()), 1)
F["departments"] = int(df.Department.nunique())
F["job_roles"] = int(df.JobRole.nunique())
F["overtime_share"] = round(100 * (df.OverTime == "Yes").mean(), 1)

def by(col, min_n=20):
    """Attrition rate, headcount and lift for one segmenting column."""
    g = (df.groupby(col, observed=True)
           .agg(headcount=("attrition_flag", "size"),
                leavers=("attrition_flag", "sum"),
                rate=("attrition_flag", "mean"),
                median_income=("MonthlyIncome", "median")))
    g["attrition_pct"] = (100 * g.rate).round(1)
    g["lift"] = (g.rate / BASE).round(2)
    return g[g.headcount >= min_n].sort_values("rate", ascending=False)

TABLES = {}
for col in ["Department", "JobRole", "OverTime", "MaritalStatus", "BusinessTravel",
            "JobLevel", "StockOptionLevel", "Gender", "tenure_band",
            "income_quartile", "satisfaction_band", "age_band",
            "JobSatisfaction_label", "WorkLifeBalance_label",
            "EnvironmentSatisfaction_label"]:
    t = by(col)
    TABLES[col] = t
    t.drop(columns="rate").to_csv(f"results/attrition_by_{col}.csv")

print(f"\nBaseline attrition {F['attrition_rate']}%  "
      f"({F['leavers']} leavers of {F['headcount']} employees)\n")
for col in ["OverTime", "JobRole", "JobLevel", "tenure_band", "income_quartile"]:
    print(f"--- {col} ---")
    print(TABLES[col][["headcount", "attrition_pct", "lift"]].to_string())
    print()

# The compounding effect. Each factor alone is a moderate risk; together they are
# not additive, and that is the operational point.
risk = (df.OverTime == "Yes") & (df.JobLevel == 1) & (df.MaritalStatus == "Single")
safe = (df.OverTime == "No") & (df.JobLevel >= 2)
F["risk_n"] = int(risk.sum())
F["risk_rate"] = round(100 * df.loc[risk, "attrition_flag"].mean(), 1)
F["risk_lift"] = round(df.loc[risk, "attrition_flag"].mean() / BASE, 2)
F["safe_n"] = int(safe.sum())
F["safe_rate"] = round(100 * df.loc[safe, "attrition_flag"].mean(), 1)

early = df[df.YearsAtCompany <= 2]
F["early_n"] = int(len(early))
F["early_staff_share"] = round(100 * len(early) / len(df), 1)
F["early_leaver_share"] = round(100 * early.attrition_flag.sum() / df.attrition_flag.sum(), 1)
F["first_year_rate"] = round(100 * df.loc[df.YearsAtCompany <= 1, "attrition_flag"].mean(), 1)

F["overtime_rate"] = round(100 * df.loc[df.OverTime == "Yes", "attrition_flag"].mean(), 1)
F["no_overtime_rate"] = round(100 * df.loc[df.OverTime == "No", "attrition_flag"].mean(), 1)
F["overtime_lift"] = round(F["overtime_rate"] / F["no_overtime_rate"], 2)
F["income_q1_rate"] = float(TABLES["income_quartile"].loc["Q1 lowest", "attrition_pct"])
F["income_q4_rate"] = float(TABLES["income_quartile"].loc["Q4 highest", "attrition_pct"])
F["median_income_stayed"] = float(df.loc[df.attrition_flag == 0, "MonthlyIncome"].median())
F["median_income_left"] = float(df.loc[df.attrition_flag == 1, "MonthlyIncome"].median())
F["top_role"] = str(TABLES["JobRole"].index[0])
F["top_role_rate"] = float(TABLES["JobRole"].iloc[0]["attrition_pct"])
F["top_role_lift"] = float(TABLES["JobRole"].iloc[0]["lift"])

print(f"Overtime            : {F['overtime_rate']}% against {F['no_overtime_rate']}%"
      f"  ({F['overtime_lift']}x)")
print(f"Compound risk group : n={F['risk_n']}, {F['risk_rate']}% leave "
      f"({F['risk_lift']}x baseline)")
print(f"Protected group     : n={F['safe_n']}, {F['safe_rate']}% leave")
print(f"First two years     : {F['early_staff_share']}% of staff, "
      f"{F['early_leaver_share']}% of all departures")
json.dump(F, open("results/findings.json", "w"), indent=2, default=str)

# =============================================================================
# 6. CHARTS
# -----------------------------------------------------------------------------
# INPUT  : the tables from section 5
# METHOD : the chart type follows the data type. Horizontal bars where the labels
#          are long, vertical bars where the categories are ordered, a line where
#          the x axis is a progression, and a waterfall where the point is that
#          risks compound.
# OUTPUT : six PNG files in charts/
# =============================================================================
def save(fig, name):
    """Write the figure AND display it, so the notebook shows the result."""
    fig.savefig(f"charts/{name}.png", bbox_inches="tight", dpi=180)
    # In a notebook this renders the figure below the cell. Run as a script with
    # !python there is no display, so the call is harmless but does nothing.
    plt.show()
    plt.close(fig)

def ratebar(ax, t, title, xlab="Attrition rate (%)"):
    """Horizontal attrition bars with the baseline drawn in, because a rate
    without its reference is not interpretable."""
    s = t.sort_values("attrition_pct")
    cols = [AMBER if v >= 100 * BASE * 1.5 else (BLUE if v >= 100 * BASE else MID)
            for v in s.attrition_pct]
    b = ax.barh(s.index.astype(str), s.attrition_pct, color=cols,
                edgecolor="white", linewidth=0.9, zorder=3)
    for bb, v, n in zip(b, s.attrition_pct, s.headcount):
        ax.text(v + 0.6, bb.get_y() + bb.get_height() / 2, f"{v:.1f}%  (n={n})",
                va="center", fontsize=9.5, color="#334155")
    ax.set_xlim(0, s.attrition_pct.max() * 1.34)
    ax.set_xlabel(xlab)
    # The reference sits in the subtitle and in the colour, not as a line across
    # the plot. Amber marks any segment at 1.5 times the company rate or above.
    ax.set_title(f"{title}\ncompany rate {100*BASE:.1f}%, amber marks 1.5x and above",
                 loc="left", fontsize=12)
    ax.grid(axis="y", alpha=0)

# Figure 1: who leaves, by job role
fig, ax = plt.subplots(figsize=(10, 4.6))
ratebar(ax, TABLES["JobRole"], "Figure 1. Attrition rate by job role")
plt.tight_layout(); save(fig, "01_attrition_by_role")

# Figure 2: the four strongest single factors, on one scale
fig, axes = plt.subplots(2, 2, figsize=(13, 7.4))
for ax, col, title in zip(axes.ravel(),
        ["OverTime", "JobLevel", "MaritalStatus", "BusinessTravel"],
        ["(a) Overtime", "(b) Job level", "(c) Marital status", "(d) Business travel"]):
    ratebar(ax, TABLES[col], title)
plt.tight_layout(); save(fig, "02_attrition_factors")

# Figure 3: tenure curve. A line, because tenure is a progression.
fig, ax = plt.subplots(figsize=(10, 4.4))
t = TABLES["tenure_band"].reindex(
    ["Under 1 year", "1 to 2", "3 to 5", "6 to 10", "Over 10"]).dropna()
ax.plot(t.index.astype(str), t.attrition_pct, "o-", color=BLUE, lw=2.6, ms=8, zorder=3)
ax.fill_between(range(len(t)), 0, t.attrition_pct, color=PALE, zorder=0)
for i, (v, n) in enumerate(zip(t.attrition_pct, t.headcount)):
    ax.text(i, v + 1.4, f"{v:.1f}%\nn={n}", ha="center", fontsize=9.5, color=NAVY)
ax.set_ylim(0, t.attrition_pct.max() * 1.32)
ax.set_xlabel("Years at the company"); ax.set_ylabel("Attrition rate (%)")
ax.set_title(f"Figure 3. Attrition falls steeply with tenure\ncompany rate {100*BASE:.1f}%".replace("{100*BASE:.1f}", f"{100*BASE:.1f}"), loc="left", fontsize=12)
ax.grid(axis="x", alpha=0)
plt.tight_layout(); save(fig, "03_tenure_curve")

# Figure 4: pay. Two panels, because the distribution and the rate say different
# things and neither alone is enough.
fig, ax = plt.subplots(1, 2, figsize=(13, 4.4))
for lab, col, c in [("Stayed", 0, MID), ("Left", 1, AMBER)]:
    ax[0].hist(df.loc[df.attrition_flag == col, "MonthlyIncome"], bins=34,
               alpha=0.72, color=c, label=lab, edgecolor="white", linewidth=0.5, zorder=3)
# Median lines, drawn solid and thin so they read as annotation, not as a grid.
ax[0].axvline(F["median_income_left"], color=AMBER, lw=2.0, alpha=0.9)
ax[0].axvline(F["median_income_stayed"], color=NAVY, lw=2.0, alpha=0.9)
ax[0].set_xlabel("Monthly income"); ax[0].set_ylabel("Employees")
ax[0].set_title("(a) Income distribution, stayed against left", loc="left")
ax[0].legend(); ax[0].xaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
q = TABLES["income_quartile"].reindex(["Q1 lowest", "Q2", "Q3", "Q4 highest"]).dropna()
cols = [AMBER if v >= 100 * BASE * 1.5 else MID for v in q.attrition_pct]
b = ax[1].bar(q.index.astype(str), q.attrition_pct, color=cols,
              edgecolor="white", linewidth=0.9, zorder=3)
for bb, v in zip(b, q.attrition_pct):
    ax[1].text(bb.get_x() + bb.get_width() / 2, v + 0.7, f"{v:.1f}%",
               ha="center", fontsize=10, fontweight="bold", color="#334155")
ax[1].set_ylim(0, q.attrition_pct.max() * 1.22)
ax[1].set_ylabel("Attrition rate (%)")
ax[1].set_title(f"(b) Attrition by income quartile, company {100*BASE:.1f}%", loc="left", fontsize=12)
ax[1].grid(axis="x", alpha=0)
plt.tight_layout(); save(fig, "04_pay_and_attrition")

# Figure 5: satisfaction. The composite band plus the individual scales.
fig, ax = plt.subplots(1, 2, figsize=(13, 4.4))
s = TABLES["satisfaction_band"].reindex(
    ["Low", "Below average", "Good", "High"]).dropna()
cols = [AMBER if v >= 100 * BASE * 1.5 else MID for v in s.attrition_pct]
b = ax[0].bar(s.index.astype(str), s.attrition_pct, color=cols,
              edgecolor="white", linewidth=0.9, zorder=3)
for bb, v, n in zip(b, s.attrition_pct, s.headcount):
    ax[0].text(bb.get_x() + bb.get_width() / 2, v + 0.8, f"{v:.1f}%\nn={n}",
               ha="center", fontsize=9.5, color="#334155")
ax[0].set_ylim(0, s.attrition_pct.max() * 1.32)
ax[0].set_ylabel("Attrition rate (%)")
ax[0].set_title(f"(a) Composite satisfaction band, company {100*BASE:.1f}%", loc="left", fontsize=12); ax[0].grid(axis="x", alpha=0)
w = 0.26
scales = [("JobSatisfaction_label", BLUE, "Job"),
          ("EnvironmentSatisfaction_label", MID, "Environment"),
          ("WorkLifeBalance_label", LIGHT, "Work-life balance")]
lv = ["1", "2", "3", "4"]
for i, (col, c, lab) in enumerate(scales):
    t2 = TABLES[col]
    vals = [t2[t2.index.astype(str).str.startswith(l)].attrition_pct.mean() for l in lv]
    ax[1].bar(np.arange(4) + (i - 1) * w, vals, w, color=c, label=lab,
              edgecolor="white", linewidth=0.7, zorder=3)
ax[1].set_xticks(range(4)); ax[1].set_xticklabels(["1 Low", "2", "3", "4 High"])
ax[1].set_ylabel("Attrition rate (%)"); ax[1].legend(ncol=3, fontsize=9)
ax[1].set_title("(b) Each satisfaction scale separately", loc="left")
ax[1].grid(axis="x", alpha=0)
plt.tight_layout(); save(fig, "05_satisfaction")

# Figure 6: the compounding effect, the operational centrepiece.
fig, ax = plt.subplots(figsize=(10.5, 4.4))
groups = [
    ("Company baseline", 100 * BASE, len(df), MID),
    ("Works overtime", F["overtime_rate"], int((df.OverTime == "Yes").sum()), BLUE),
    ("Overtime + job level 1",
     100 * df.loc[(df.OverTime == "Yes") & (df.JobLevel == 1), "attrition_flag"].mean(),
     int(((df.OverTime == "Yes") & (df.JobLevel == 1)).sum()), NAVY),
    ("Overtime + level 1 + single", F["risk_rate"], F["risk_n"], AMBER),
    ("No overtime, level 2+", F["safe_rate"], F["safe_n"], LIGHT),
]
labs = [g[0] for g in groups][::-1]
vals = [g[1] for g in groups][::-1]
ns   = [g[2] for g in groups][::-1]
cols = [g[3] for g in groups][::-1]
b = ax.barh(labs, vals, color=cols, edgecolor="white", linewidth=0.9, zorder=3)
for bb, v, n in zip(b, vals, ns):
    ax.text(v + 1.2, bb.get_y() + bb.get_height() / 2,
            f"{v:.1f}%   n={n}", va="center", fontsize=10,
            fontweight="bold", color="#334155")
ax.set_xlim(0, max(vals) * 1.32)
ax.set_xlabel("Attrition rate (%)")
ax.set_title("Figure 6. Risk factors compound, they do not add", loc="left")
ax.grid(axis="y", alpha=0)
plt.tight_layout(); save(fig, "06_compounding_risk")

json.dump(F, open("results/findings.json", "w"), indent=2, default=str)
print("\nCharts written:", sorted(os.listdir("charts")))


import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Allow pages to import the shared data file.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from data import load_data

st.set_page_config(
    page_title="OpsPulse 2.0 | Executive Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Overview")
st.caption("OpsPulse 2.0 | Operations Intelligence Platform")
st.info("Portfolio demonstration using synthetic sample data.")

df = load_data()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

employees = st.sidebar.multiselect(
    "Employees",
    sorted(df["analyst"].unique()),
    default=sorted(df["analyst"].unique())
)

slices = st.sidebar.multiselect(
    "Work Slices",
    sorted(df["slice"].unique()),
    default=sorted(df["slice"].unique())
)

filtered = df[
    df["analyst"].isin(employees)
    & df["slice"].isin(slices)
].copy()

if filtered.empty:
    st.warning("No records match your filters.")
    st.stop()

# Calculate KPIs
assigned = int(filtered["tasks_assigned"].sum())
completed = int(filtered["tasks_completed"].sum())
dents = int(filtered["dents"].sum())
quality = filtered["quality_score"].mean()
completion_rate = completed / assigned * 100 if assigned else 0
pending = assigned - completed
dent_rate = dents / completed * 100 if completed else 0

st.subheader("Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tasks Completed", f"{completed:,}")
c2.metric("Completion Rate", f"{completion_rate:.1f}%")
c3.metric("Average Quality", f"{quality:.1f}/100")
c4.metric("Total Dents", f"{dents:,}")

c5, c6, c7 = st.columns(3)
c5.metric("Tasks Assigned", f"{assigned:,}")
c6.metric("Pending Tasks", f"{pending:,}")
c7.metric("Dents per 100 Completed", f"{dent_rate:.1f}")

st.divider()

# Daily trends
st.subheader("Daily Performance Trends")

daily = filtered.groupby("date", as_index=False).agg(
    tasks_completed=("tasks_completed", "sum"),
    tasks_assigned=("tasks_assigned", "sum"),
    quality_score=("quality_score", "mean")
)

st.line_chart(
    daily.set_index("date")[
        ["tasks_completed", "tasks_assigned"]
    ]
)

st.subheader("Quality Trend")
st.line_chart(daily.set_index("date")["quality_score"])

# Employee comparison
st.subheader("Employee Productivity")

employee_summary = (
    filtered.groupby("analyst", as_index=False)
    .agg(
        completed=("tasks_completed", "sum"),
        dents=("dents", "sum"),
        quality=("quality_score", "mean")
    )
    .sort_values("completed", ascending=False)
)

st.bar_chart(
    employee_summary.set_index("analyst")["completed"]
)

st.subheader("Employee Summary")
st.dataframe(
    employee_summary,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "All data is synthetic. Quality scores and dents "
    "are illustrative metrics."
)

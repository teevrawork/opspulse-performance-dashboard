import streamlit as st
import pandas as pd

st.set_page_config(page_title="OpsPulse | Performance Intelligence", page_icon="📊", layout="wide")

st.title("📊 OpsPulse")
st.caption("Operations Performance Intelligence — a portfolio prototype using synthetic sample data.")

@st.cache_data
def load_data():
    data = [
        ["2026-10-01","Aarav","Slice A",24,22,2,91],
        ["2026-10-01","Diya","Slice B",24,24,0,98],
        ["2026-10-01","Kabir","Slice C",24,20,4,84],
        ["2026-10-02","Aarav","Slice B",24,23,1,95],
        ["2026-10-02","Diya","Slice C",24,21,3,88],
        ["2026-10-02","Kabir","Slice A",24,22,2,90],
        ["2026-10-03","Aarav","Slice C",24,19,5,80],
        ["2026-10-03","Diya","Slice A",24,23,1,96],
        ["2026-10-03","Kabir","Slice B",24,21,3,87],
        ["2026-10-04","Aarav","Slice A",24,24,0,99],
        ["2026-10-04","Diya","Slice B",24,22,2,92],
        ["2026-10-04","Kabir","Slice C",24,23,1,94],
        ["2026-10-05","Aarav","Slice B",24,21,3,89],
        ["2026-10-05","Diya","Slice C",24,24,0,99],
        ["2026-10-05","Kabir","Slice A",24,20,4,83],
        ["2026-10-06","Aarav","Slice C",24,22,2,91],
        ["2026-10-06","Diya","Slice A",24,24,0,98],
        ["2026-10-06","Kabir","Slice B",24,22,2,91],
        ["2026-10-07","Aarav","Slice A",24,23,1,96],
        ["2026-10-07","Diya","Slice B",24,23,1,95],
        ["2026-10-07","Kabir","Slice C",24,21,3,88],
    ]
    df = pd.DataFrame(data, columns=["date","analyst","slice","tasks_assigned","tasks_completed","dents","quality_score"])
    df["date"] = pd.to_datetime(df["date"])
    df["completion_rate"] = (df["tasks_completed"] / df["tasks_assigned"] * 100).round(1)
    return df

df = load_data()
st.sidebar.header("Filters")
people = st.sidebar.multiselect("Team member", sorted(df["analyst"].unique()), default=sorted(df["analyst"].unique()))
slices = st.sidebar.multiselect("Work slice", sorted(df["slice"].unique()), default=sorted(df["slice"].unique()))
filtered = df[df["analyst"].isin(people) & df["slice"].isin(slices)].copy()

if filtered.empty:
    st.warning("No rows match these filters. Select at least one team member and one work slice.")
    st.stop()

tasks_assigned = int(filtered["tasks_assigned"].sum())
tasks_completed = int(filtered["tasks_completed"].sum())
dents = int(filtered["dents"].sum())
completion = tasks_completed / tasks_assigned * 100 if tasks_assigned else 0
avg_quality = filtered["quality_score"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tasks completed", f"{tasks_completed:,}", help="Total completed tasks in the selected data.")
c2.metric("Completion rate", f"{completion:.1f}%")
c3.metric("Total dents", f"{dents:,}", help="Illustrative quality/deduction count in this sample dataset.")
c4.metric("Average quality score", f"{avg_quality:.1f}/100")

left, right = st.columns(2)
with left:
    st.subheader("Completed tasks by team member")
    by_person = filtered.groupby("analyst", as_index=False)["tasks_completed"].sum().sort_values("tasks_completed", ascending=False)
    st.bar_chart(by_person.set_index("analyst"))
with right:
    st.subheader("Quality score by work slice")
    by_slice = filtered.groupby("slice", as_index=False)["quality_score"].mean().sort_values("quality_score", ascending=False)
    st.bar_chart(by_slice.set_index("slice"))

st.subheader("Daily performance trend")
daily = filtered.groupby("date", as_index=False).agg(
    tasks_completed=("tasks_completed","sum"),
    quality_score=("quality_score","mean"),
    dents=("dents","sum")
).sort_values("date")
st.line_chart(daily.set_index("date")[["tasks_completed", "quality_score"]])

st.subheader("Automated operational insights")
lowest_quality = by_slice.sort_values("quality_score").iloc[0]
highest_dents = filtered.groupby("analyst")["dents"].sum().sort_values(ascending=False)
top_person = by_person.iloc[0]
insight_col1, insight_col2 = st.columns(2)
with insight_col1:
    st.info(f"**Quality watch:** {lowest_quality['slice']} has the lowest average quality score ({lowest_quality['quality_score']:.1f}/100) in the current selection. Review examples from this slice before making staffing or process changes.")
with insight_col2:
    if len(highest_dents):
        st.info(f"**Review opportunity:** {highest_dents.index[0]} has the highest dent count ({int(highest_dents.iloc[0])}) in the current selection. Check task mix and context before drawing conclusions.")
st.success(f"**Throughput:** {top_person['analyst']} has the highest completed-task total ({int(top_person['tasks_completed'])}) among the filtered team members.")

st.subheader("Underlying sample records")
st.dataframe(filtered.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", data=csv, file_name="opspulse_filtered_data.csv", mime="text/csv")

with st.expander("Project notes & limitations"):
    st.markdown("""
    - This is a portfolio demo built with **synthetic sample data**. It is not connected to any employer's systems.
    - The dashboard includes rule-based insights and an optional Gemini-powered AI Analyst.
    - Gemini analyzes aggregated synthetic metrics only.
    - AI outputs are generated on demand and require human review.
    - AI requests are password-protected for portfolio demonstration.
    - Dent counts and quality scores are illustrative fields, not a universal performance standard.
    """)

st.divider()
st.header("🧠 Smart Performance Insights")

if filtered.empty:
    st.info("No data available for the selected filters.")
else:
    total_dents = filtered["dents"].sum()
    average_quality = filtered["quality_score"].mean()

    if average_quality < 90:
        st.warning(
            "Quality Alert: Average quality is below 90. "
            "Review tasks with lower quality scores."
        )
    else:
        st.success(
            "Quality Insight: Average quality is healthy "
            "for the selected data."
        )

    if total_dents > 20:
        st.warning(
            "Dent Risk: High number of dents detected. "
            "Investigate recurring task errors."
        )
    else:
        st.success(
            "Dent Insight: Dent count is within the demo threshold."
        )

    member_performance = (
        filtered.groupby("analyst")["quality_score"]
        .mean()
        .sort_values(ascending=False)
    )

    best_member = member_performance.index[0]

    st.info(
        f"Top Quality Performer: {best_member} "
        "has the highest average quality score "
        "for the selected filters."
    )

    st.caption(
        "Insights are generated using rule-based analytics "
        "on synthetic sample data. Thresholds are illustrative."
    )

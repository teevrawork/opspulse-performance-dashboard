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


# ---------------------------------------
# Gemini AI Performance Analyst
# ---------------------------------------

import hmac
from google import genai
from google.genai import types

st.divider()
st.header("🤖 Gemini AI Performance Analyst")
st.caption(
    "Generative AI analysis of the selected synthetic data. "
    "AI suggestions require human review."
)

if "ai_unlocked" not in st.session_state:
    st.session_state.ai_unlocked = False

if "ai_requests" not in st.session_state:
    st.session_state.ai_requests = 0

if "ai_report" not in st.session_state:
    st.session_state.ai_report = None

if "AI_ACCESS_PASSWORD" not in st.secrets:
    st.warning("AI access password is not configured.")
else:
    if not st.session_state.ai_unlocked:
        password = st.text_input(
            "Enter AI access password",
            type="password",
            key="ai_password_input"
        )

        if st.button("Unlock AI Analyst"):
            if hmac.compare_digest(
                password,
                st.secrets["AI_ACCESS_PASSWORD"]
            ):
                st.session_state.ai_unlocked = True
                st.rerun()
            else:
                st.error("Incorrect password.")

    if st.session_state.ai_unlocked:
        st.success("AI Analyst unlocked.")

        if st.button("Lock AI Analyst"):
            st.session_state.ai_unlocked = False
            st.session_state.ai_report = None
            st.rerun()

        # Prepare aggregated metrics only.
        summary = {
            "tasks_assigned": tasks_assigned,
            "tasks_completed": tasks_completed,
            "completion_rate_percent": round(completion, 1),
            "total_dents": dents,
            "average_quality_score": round(float(avg_quality), 1),
            "quality_by_slice": {
                str(row["slice"]): round(float(row["quality_score"]), 1)
                for _, row in by_slice.iterrows()
            },
            "dents_by_analyst": {
                str(name): int(count)
                for name, count in highest_dents.items()
            }
        }

        st.caption(
            f"AI requests this session: "
            f"{st.session_state.ai_requests}/3"
        )

        if st.button(
            "✨ Generate AI Analysis",
            disabled=st.session_state.ai_requests >= 3
        ):
            st.session_state.ai_requests += 1
            st.session_state.ai_report = None

            prompt = f"""
You are an operations performance analyst.

Analyze these synthetic demo metrics:
{summary}

Write a concise report containing:

1. Executive summary
2. Key performance observations
3. Quality and dent risks
4. Three practical recommendations

Rules:
- Use only the supplied metrics.
- Do not invent causes or additional data.
- Distinguish observations from hypotheses.
- Avoid judging employees from dent counts alone.
- Clearly state this is synthetic demonstration data.
- Keep the report under 300 words.
"""

            try:
                if "GEMINI_API_KEY" not in st.secrets:
                    st.error("Gemini API key is missing.")
                else:
                    with st.spinner("Gemini is analyzing performance..."):
                        client = genai.Client(
                            api_key=st.secrets["GEMINI_API_KEY"]
                        )

                        response = client.models.generate_content(
                            model="gemini-2.5-flash-lite",
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                temperature=0.2,
                                max_output_tokens=900
                            )
                        )

                        if response.text:
                            st.session_state.ai_report = response.text
                        else:
                            st.warning(
                                "Gemini returned no text. "
                                "Please try again later."
                            )

           
            except Exception as e:
                st.error("Gemini API request failed.")
                st.code(str(e))

        if st.session_state.ai_report:
            st.markdown(st.session_state.ai_report)

        st.caption(
            "Prototype access control and session request limit. "
            "Not a global quota limit or production security system."
        )

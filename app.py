import pandas as pd
import plotly.express as px
import streamlit as st

from data import simulate

st.set_page_config(page_title="HR Analytics", page_icon="🧑‍💼", layout="wide")
st.title("🧑‍💼 Employee Job Satisfaction & Attrition Dashboard")
st.caption("HR analytics: attrition drivers and job satisfaction by department · web version of the Tableau dashboard · simulated workforce")

SAT = {1: "Low", 2: "Medium", 3: "High", 4: "Very high"}


@st.cache_data
def load():
    df = simulate()
    df["age_band"] = pd.cut(df.age, [17, 25, 35, 45, 55, 60], labels=["< 25", "25–34", "35–44", "45–54", "55 +"])
    df["left"] = (df.attrition == "Yes").astype(int)
    return df


df = load()
with st.sidebar:
    st.header("Filters")
    dept = st.multiselect("Department", sorted(df.department.unique()), default=sorted(df.department.unique()))
    gender = st.multiselect("Gender", sorted(df.gender.unique()), default=sorted(df.gender.unique()))
    field = st.multiselect("Education field", sorted(df.education_field.unique()), default=sorted(df.education_field.unique()))
    st.markdown("[Portfolio](https://noe2019.github.io/DA-Portfolio-Website/)")

f = df[df.department.isin(dept) & df.gender.isin(gender) & df.education_field.isin(field)]
if f.empty:
    st.warning("No employees match the filters.")
    st.stop()

k = st.columns(6)
k[0].metric("Employees", f"{len(f):,}")
k[1].metric("Attrition", f"{f.left.sum():,}")
k[2].metric("Attrition rate", f"{f.left.mean():.1%}")
k[3].metric("Active employees", f"{(1 - f.left).sum():,}")
k[4].metric("Avg age", f"{f.age.mean():.0f}")
k[5].metric("Avg monthly income", f"${f.monthly_income.mean():,.0f}")

l, r = st.columns(2)
by_dept = f.groupby("department").left.agg(["sum", "mean"]).reset_index()
by_dept["label"] = by_dept["mean"].map("{:.0%}".format)
l.plotly_chart(px.bar(by_dept, x="department", y="sum", text="label", title="Attrition by department (count and rate)",
                      labels={"sum": "Employees who left", "department": ""}), use_container_width=True)
r.plotly_chart(px.bar(f.groupby("job_role").left.mean().sort_values().reset_index(), x="left", y="job_role", orientation="h",
                      title="Attrition rate by job role", labels={"left": "Attrition rate", "job_role": ""}).update_xaxes(tickformat=".0%"), use_container_width=True)

a, b, c = st.columns(3)
a.plotly_chart(px.bar(f.groupby(["age_band", "gender"], observed=True).left.sum().reset_index(), x="age_band", y="left", color="gender", barmode="group",
                      title="Attrition by age band and gender", labels={"left": "Employees who left", "age_band": "Age"}), use_container_width=True)
b.plotly_chart(px.pie(f[f.left == 1], names="overtime", hole=.5, title="Overtime among leavers"), use_container_width=True)
c.plotly_chart(px.pie(f[f.left == 1], names="education_field", hole=.5, title="Leavers by education field"), use_container_width=True)

st.subheader("Job satisfaction by role")
heat = pd.crosstab(f.job_role, f.job_satisfaction.map(SAT)).reindex(columns=list(SAT.values()), fill_value=0)
st.plotly_chart(px.imshow(heat, text_auto=True, color_continuous_scale="Blues", aspect="auto", labels=dict(x="Job satisfaction", y="", color="Employees")),
                use_container_width=True)

st.subheader("Attrition drivers")
drv = pd.concat([f.groupby(f[c].map(SAT) if c != "overtime" else f[c]).left.mean().rename(c) for c in
                 ["job_satisfaction", "environment_satisfaction", "work_life_balance", "overtime"]], axis=1)
drv.index.name = "level"
st.plotly_chart(px.bar(drv.reset_index().melt(id_vars="level").dropna(), x="level", y="value", color="variable", barmode="group",
                       labels={"level": "Level", "value": "Attrition rate", "variable": "Factor"},
                       category_orders={"level": list(SAT.values()) + ["No", "Yes"]}).update_yaxes(tickformat=".0%"), use_container_width=True)

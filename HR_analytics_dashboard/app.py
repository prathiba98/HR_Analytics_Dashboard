import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
sns.set_style("whitegrid")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("hr_cleaned.csv")

df = load_data()

# ---------------- TITLE ----------------
st.title(" HR Analytics – Employee Attrition Dashboard")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header(" Filters")

department = st.sidebar.multiselect(
    "Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

job_role = st.sidebar.multiselect(
    "Job Role",
    df["JobRole"].unique(),
    default=df["JobRole"].unique()
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["JobRole"].isin(job_role))
]

# ---------------- KPIs ----------------
total_employees = filtered_df.shape[0]
attrition_count = filtered_df[filtered_df["Attrition"] == "Yes"].shape[0]
active_employees = total_employees - attrition_count
attrition_rate = round((attrition_count / total_employees) * 100, 2) if total_employees > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric(" Total Employees", total_employees)
k2.metric(" Attrition", attrition_count)
k3.metric(" Active Employees", active_employees)
k4.metric(" Attrition Rate (%)", f"{attrition_rate}")

st.markdown("---")

# ---------------- CHARTS ----------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Attrition by Department")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x="Department", hue="Attrition",color='teal', ax=ax)
    st.pyplot(fig)

with c2:
    st.subheader("OverTime vs Attrition")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x="OverTime", hue="Attrition",color='teal', ax=ax)
    st.pyplot(fig)

st.subheader("Monthly Income vs Attrition")
fig, ax = plt.subplots(figsize=(8,5))
sns.boxplot(data=filtered_df, x="Attrition", y="MonthlyIncome",color='teal', ax=ax)
st.pyplot(fig)

st.markdown("---")

c3, c4 = st.columns(2)

with c3:
    st.subheader("Age Distribution vs Attrition")
    fig, ax = plt.subplots()
    sns.histplot(
        data=filtered_df,
        x="Age",
        hue="Attrition",
        bins=30,
        kde=True,
        palette=['black','teal'],
        ax=ax
    )
    st.pyplot(fig)

with c4:
    st.subheader("Job Satisfaction vs Attrition")
    fig, ax = plt.subplots()
    sns.countplot(
        data=filtered_df,
        x="JobSatisfaction",
        hue="Attrition",
        color='teal',
        ax=ax
    )
    st.pyplot(fig)

st.markdown("---")

# ---------------- INSIGHTS ----------------
st.subheader(" Key Insights and Recommendations")

st.markdown("""
- Research and Development department has higher attrition.
- Younger employees are more likely to leave.
- Lower salary correlates with higher attrition.
- Overtime is a major attrition trigger.
- Most attrition occurs in early tenure.


###  Recommendations
- Review **workload and overtime policies**, especially in high-attrition departments.
- Introduce **early-career engagement and mentorship programs**.
- Re-evaluate **compensation bands** for roles with consistently high attrition.
- Conduct regular **job satisfaction surveys** and act on low scores proactively.
""")

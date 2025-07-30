#pages/2_incident_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Incident Dashboard", layout="wide")

#load data
@st.cache_data
def load_data():
    df = pd.read_csv("incident_data.csv", parse_dates=["date_reported", "follow_up_due"])
    return df

df = load_data()

st.title("📊 Patient Safety Dashboard")

#KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", len(df))
col2.metric("Open Cases", len(df[df["status"] == "Open"]))
col3.metric("High Severity", len(df[df["severity"] == "High"]))
col4.metric("Critical Incidents", len(df[df["severity"] == "Critical"]))

st.markdown("---")

#Charts
st.subheader("Incidents by Severity")
severity_chart = px.bar(df["Severity"].value_counts().reset_inndex(),
                        x="index", y="severity", labels={"index": "Severity", "severity": "Count"},
                        color="index", title="Incidents by Severity")
st.plotly_chart(severity_chart, use_container_width=True)

st.subheader("Incidents by Department")
dept_chart = px.pie(df, names="Department", title="Incident by Department")
st.plotly_chart(dept_chart, use_container_width=True)

st.subheader("Trend Over Time")
df["date_reported"] = pd.to_datetime(df["date_reported"])
daily_counts = df.groupby("date_reported").size().reset_index(name="count")
time_chart = px.line(daily_counts, x="date_reported", y="count", title="Daily Incident Reports")
st.plotly_chart(time_chart, use_container_width=True)

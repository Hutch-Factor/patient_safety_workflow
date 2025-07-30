#pages/2_incident_dashboard.py
import streamlit as st
import pandas as pd

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
st.markdown("Incidents by Severity")
severity_counts = df["severity"].value_counts()
st.bar_chart(severity_counts)

st.markdown("Incidents by Department")
dept_counts = df["department"].value_counts()
st.bar_chart(dept_counts)

st.markdown("Trend Over Time")
daily_counts = df["date_reported"].value_counts().sort_index()
st.line_chart(daily_counts)

import streamlit as st
import pandas as pd

#page configuration
st.set_page_config(page_title="Patient Safety Workflow", layout="wide")

#Load data
@st.cache_data
def load_data():
    df = pd.read_csv("incident_data.csv", parse_dates=["date_reported", "follow_up_due"])
    return df

df = load_data()

#sidebar filters
st.sidebar.header("Filter Incidents")
status_filter = st.sidebar.multiselect("Status", options=df["status"].unique(), default=df["status"].unique())
severity_filter = st.sidebar.multiselect("Severity", options=df["severity"].unique(), default=df["severity"].unique())
dept_filter = st.sidebar.multiselect("Department", options=df["department"].unique(), default=df["department"].unique())

#Apply filters
filtered_df = df.copy()
if status_filter:
    filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
if severity_filter:
    filtered_df = filtered_df[filtered_df["severity"].isin(severity_filter)]
if dept_filter:
    filtered_df = filtered_df[filtered_df["department"].isin(dept_filter)]
if st.sidebar.button("Reset Filters"):
    st.experimental_rerun()

#Title and table
st.title("🛡️ Patient Safety Incident Tracker")
st.subheader(f"Displaying {len(filtered_df)} incidents")
st.dataframe(filtered_df, use_container_width=True)

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
status_filter = st.sidebar.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())
severity_filter = st.sidebar.multiselect("Severity", options=df["Severity"].unique(), default=df["Severity"].unique())
dept_filter = st.sidebar.multiselect("Department", options=df["Department"].unique(), default=df["Department"].unique())

#Apply filters
filtered_df = df[
    (df["Status"].isin(status_filter)) &
    (df["Severity"].isin(severity_filter)) &
    (df["Department"].isin(dept_filter))
    ]

#Title and table
st.title("🛡️ Patient Safety Incident Tracker")
st.subheader(f"Displaying {len(filtered_df)} incidents")
st.dataframe(filtered_df, use_container_width=True)

#pages/3_incident_detail view.py
import streamlit as st
import pandas as pd

st.title("Incident Detail View")

#Load Data
@st.cache_data
def load_data():
    return pd.read_csv("incident_data.csv", parse_dates=["date_reported"])

df = load_data()

#Sidebar Filters
st.sidebar.header("🔍 Filter Incidents")

status_options = st.sidebar.multiselect("status", df["status"].unique(), default=df["status"].unique())
severity_options = st.sidebar.multiselect("severity", df["severity"].unique(), default=df["severity"].unique())
department_options = st.sidebar.multiselect("department", df["department"].unique(), default=df["department"].unique())

filtered_df = df[
    df["status"].isin(status_options) &
    df["severity"].isin(severity_options) &
    df["department"].isin(department_options)
]

st.markdown(f"### {len(filtered_df)} Incident(s) Found")

#Table View
selected_index = st.selectbox("Select an incident to view details:", filtered_df.index)

if selected_index:
    selected_incident = filtered_df.loc[selected_index]

    st.subheader(f"📌Incident: {selected_incident['report_id']}")
    st.markdown(f"**Date Reported:** {selected_incident['date_reported'].date()}")
    st.markdown(f"**Reported By:** {selected_incident['reporter']}")
    st.markdown(f"**Department:** {selected_incident['department']}")
    st.markdown(f"**Severity:** {selected_incident['severity']}")
    st.markdown(f"**Status:** {selected_incident['status']}")
    st.markdown(f"**Description**")
    st.info(selected_incident['description'])

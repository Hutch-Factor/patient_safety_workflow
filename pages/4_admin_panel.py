#pages/4_Admin_Panel.py

import streamlit as st
import pandas as pd
import os

st.title("⚙️ Admin Panel")

#Load Data
@st.cache_data
def load_data():
    return pd.read_csv("incident_data.csv", parse_dates=["date_reported"])

@st.cache_resource
def save_data(df):
    df.to_csv("incident_data.csv", index=False)

df = load_data()

st.markdown("### Incident Management")

incident_ids = df["report_id"].tolist()
selected_id = st.selectbox("Select Incident ID to Manage", incident_ids)

incident = df[df["report_id"] == selected_id].iloc[0]

#Editable Fields
new_status = st.selectbox("Update status", ["Open", "In Progress", "Resolved", "Closed"], index=["Open", "In Progress", "Resolved", "Closed"].index(incident["status"]))
new_severity = st.selectbox("Update severity", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(incident["severity"]))
new_dept = st.selectbox("Update department", sorted(df["department"].unique()), index=sorted(df["department"].unique()).index(incident["department"]))

#Update Button
if st.button("💾 Save Changes"):
    df.loc[df["report_id"] == selected_id, "status"] = new_status
    df.loc[df["report_id"] == selected_id, "severity"] = new_severity
    df.loc[df["report_id"] == selected_id, "department"] = new_dept
    save_data(df)
    st.success("Incident Updated Successfully!")

#Optional: Delete Incident
if st.button("🗑️ Delete Incident"):
    df = df[df["report_id"] != selected_id]
    save_data(df)
    st.warning("Incident Deleted.")

#Optional: Download Full Dataset
st.markdown("---")
st.download_button("📥 Export All Incidents (CSV)", df.to_csv(index=False), file_name="all_incidents.csv")

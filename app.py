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
if st.sidebar.button("Reset Filters"):
    st.session_state.reset = True
    st.rerun()

#Apply filters
filtered_df = df.copy()
if status_filter:
    filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
if severity_filter:
    filtered_df = filtered_df[filtered_df["severity"].isin(severity_filter)]
if dept_filter:
    filtered_df = filtered_df[filtered_df["department"].isin(dept_filter)]
#Initialize session state on first run
if "reset" not in st.session_state:
    st.session_state.reset = False

#Title and table
st.title("🛡️ Patient Safety Incident Tracker")
st.subheader(f"Displaying {len(filtered_df)} incidents")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
with st.expander(" Submit a New Patient Safety Incident"):
    with st.form("incident_form"):
        st.subheader("New Incident Form")

        date_reported = st.date_input("Date Reported")
        reporter = st.text_input("Reported By (Name or Role)")
        department = st.selectbox("Department", options=sorted(df["department"].unuique()))
        event_type = st.selectbox("Event Type", options=[
            "Fall", "Medication Error", "Equipment Malfunction", "Pressure Injury",
             "Misidentification", "Documentation Error", "Delayed Care"
        ])
        severity = st.selectbox("Severity", options=["Low", "Moderate", "High", "Critical"])
        assigned_to = st.selectbox("Assigned To", options=[
            "Safety Officer", "Risk Manager", "Quality Lead", "Biomed Team", "Wound Team"])
        corrective_action = st.text_area("Initial Corrective Action (Optional)")
        follow_up_due = st.date_input("Follow-Up Due Date")

        submit = st.form_submit_button("Submit Incident")

        if submit:
            #Create new incident dictionary
            new_incident = {
                "report_id": f"PS{len(df) + 1:03d}",
                "date_reported": date_reported,
                "reporter": reporter,
                "department": department,
                "event_type": event_type,
                "severity": severity,
                "status": "Open",
                "assigned_to": assigned_to,
                "rca_complete": "No",
                "corrective_action": corrective_action if corrective_action else "TBD",
                "follow_up_due": follow_up_due,
                "outcome": "Pending"
            }

            #Append to DataFrame
            df = pd.concat([df, pd.DataFrame([new_incident])], ignore_index=True)

            st.success("Incident submitted successfully!")

            #Optional: Save to CSV (or database)
            df.to_csv("incident_data.csv", index=False) 




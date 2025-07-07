import streamlit as st
import pandas as pd
from modules.parser import parse_criteria
from modules.matcher import is_eligible
from modules.recommender import score_match

st.set_page_config(page_title="Clinical Trial Matching System", layout="centered")
st.title("🔬 Clinical Trial Matching System")

trials = pd.read_csv("data/trials.csv")

with st.form("patient_form"):
    name = st.text_input("🆔 Patient ID", "P001")
    age = st.number_input("🎂 Age", min_value=0, value=45)
    conditions = st.text_input("🩺 Conditions (comma separated)", "diabetes, hypertension")
    location = st.text_input("📍 Location", "New York")
    submitted = st.form_submit_button("🔍 Find Matching Trials")

if submitted:
    patient = {"patient_id": name, "age": age, "conditions": conditions.lower(), "location": location}
    matches = []
    for _, t in trials.iterrows():
        inc = parse_criteria(t["inclusion_criteria"])
        exc = parse_criteria(t["exclusion_criteria"])
        if is_eligible(patient, inc, exc):
            score = score_match(patient, t)
            matches.append((t["trial_id"], t["condition"], score, t["location"]))

    if matches:
        df = pd.DataFrame(matches, columns=["Trial ID", "Condition", "Score", "Location"])
        df = df.sort_values(by="Score", ascending=False)
        st.success("✅ Trials matched!")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, f"{name}_matched_trials.csv", "text/csv")
    else:
        st.warning("🚫 No matching trials found for this patient.")

# -------------------- Batch Matching for Uploaded CSV --------------------
st.markdown("---")
st.header("📁 Batch Match for Multiple Patients")
uploaded_file = st.file_uploader("Upload a CSV file with patient data", type="csv")

if uploaded_file is not None:
    patients_df = pd.read_csv(uploaded_file)
    results = []

    for _, p in patients_df.iterrows():
        patient = {
            "patient_id": p["patient_id"],
            "age": p["age"],
            "conditions": str(p["conditions"]).lower(),
            "location": p["location"]
        }
        for _, t in trials.iterrows():
            inc = parse_criteria(t["inclusion_criteria"])
            exc = parse_criteria(t["exclusion_criteria"])
            if is_eligible(patient, inc, exc):
                score = score_match(patient, t)
                results.append({
                    "patient_id": p["patient_id"],
                    "trial_id": t["trial_id"],
                    "condition": t["condition"],
                    "score": score,
                    "location": t["location"]
                })

    if results:
        result_df = pd.DataFrame(results)
        st.success("✅ Matches generated for uploaded patients")
        st.dataframe(result_df)
        csv_all = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download All Matches CSV", csv_all, "all_patient_matches.csv", "text/csv")
    else:
        st.warning("🚫 No matches found for any patients.")

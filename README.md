import streamlit as st
import pandas as pd

# Load your dataset
@st.cache_data
def load_data():
    df = pd.read_csv("batch 2024-25 full data enrollment.csv", encoding="latin1")
    return df

df = load_data()

st.set_page_config(page_title="Student Birthday Finder", layout="wide")
st.title("🎂 Student Birthday Finder")

# User input for day and month
col1, col2 = st.columns(2)
with col1:
    day = st.number_input("Enter Day", min_value=1, max_value=31, step=1)
with col2:
    month = st.number_input("Enter Month", min_value=1, max_value=12, step=1)

# Filter students
if st.button("Find Birthdays"):
    results = df[(df["DOB Day"] == day) & (df["DOB Month"] == month)]

    if results.empty:
        st.warning("No student found with this birthday.")
    else:
        st.success(f"🎉 Found {len(results)} student(s) with birthday on {day}-{month}!")

        # Display student cards
        for _, row in results.iterrows():
            img_url = f"https://bteup.ac.in/PDFFILES/STUDENTIMAGES/P{row['Enrollment Number']}.jpg"

            with st.container():
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; 
                                border: 1px solid #ddd; padding: 15px; 
                                border-radius: 12px; margin-bottom: 10px; 
                                background-color: #f9f9f9; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                        <img src="{img_url}" width="100" style="border-radius:10px; margin-right:15px;">
                        <div>
                            <h4 style="margin:0;">{row['Name']}</h4>
                            <p style="margin:0;"><b>Branch:</b> {row['Branch']}</p>
                            <p style="margin:0;"><b>Enrollment No:</b> {row['Enrollment Number']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

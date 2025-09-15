import streamlit as st
import pandas as pd
import datetime

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("batch 2024-25 full data enrollment.csv", encoding="latin1")
    return df

df = load_data()

st.set_page_config(page_title="Student Birthday Finder", layout="wide")
st.title("🎓 Student Birthday Finder")

# --- Navigation ---
mode = st.radio(
    "Choose Search Mode:",
    ["By Date", "By Name", "By Enrollment No"],
    horizontal=True
)

st.markdown("---")

# --- Utility to render cards ---
def render_cards(results):
    if results.empty:
        st.error("No student found.")
        return
    card_html = ""
    for _, row in results.iterrows():
        img_url = f"https://bteup.ac.in/PDFFILES/STUDENTIMAGES/P{row['Enrollment Number']}.jpg"
        card_html += f"""
        <div style="flex: 0 0 auto; width: 280px; margin: 10px; 
                    border: 1px solid #ddd; border-radius: 12px; 
                    background: #f9f9f9; padding: 12px; 
                    text-align: center; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); 
                    word-wrap: break-word; white-space: normal; min-height: 250px;">
            <img src="{img_url}" height="150" width="120" 
                 style="border-radius: 10px; margin-bottom: 8px; object-fit: cover;">
            <h4 style="margin:0 0 6px 0;">{row['Name']}</h4>
            <p style="margin:2px 0;"><b>Branch:</b><br>{row['Branch']}</p>
            <p style="margin:2px 0;"><b>Enrollment:</b><br>{row['Enrollment Number']}</p>
            <p style="margin:2px 0; color:#d9534f;"><b>DOB:</b> {row['DOB Day']}-{row['DOB Month']}-{row['DOB Year']}</p>
        </div>
        """
    st.markdown(
        f"""
        <div style="display: flex; overflow-x: auto; padding: 10px; 
                    white-space: nowrap; max-width: 100%;">
            {card_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# --- MODE 1: By Date ---
if mode == "By Date":
    col1, col2, col3 = st.columns([1,1,2])

    with col1:
        selected_date = st.date_input("Pick a date", datetime.date.today())
    with col2:
        if st.button("Today"):
            selected_date = datetime.date.today()
        if st.button("Tomorrow"):
            selected_date = datetime.date.today() + datetime.timedelta(days=1)

    day = selected_date.day
    month = selected_date.month

    results = df[(df["DOB Day"] == day) & (df["DOB Month"] == month)]
    if not results.empty:
        st.success(f"🎉 Found {len(results)} student(s) with birthday on {day}-{month}!")
    render_cards(results)

# --- MODE 2: By Name ---
elif mode == "By Name":
    name_query = st.selectbox("Select Student Name", [""] + sorted(df["Name"].unique()))
    if name_query:
        results = df[df["Name"].str.lower() == name_query.lower()]
        render_cards(results)

# --- MODE 3: By Enrollment ---
elif mode == "By Enrollment No":
    enroll_query = st.selectbox("Select Enrollment Number", [""] + sorted(df["Enrollment Number"].astype(str).unique()))
    if enroll_query:
        results = df[df["Enrollment Number"].astype(str) == enroll_query]
        render_cards(results)

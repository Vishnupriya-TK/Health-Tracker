import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
#title 
st.set_page_config(page_title="Welcome To Health Tracker",layout="centered")

#persistent storage
if "water_intake" not in st.session_state:
  st.session_state.water_intake=[]
if "sleep_log" not in st.session_state:
  st.session_state.sleep_log=[]
#header
st.title("🏥 Personal Health Tracker")
st.markdown("<p style='color:gray;'>Track your BMI, water intake, and sleep patterns easily.</p>", unsafe_allow_html=True)
st.divider()

#bmi
st.header("1️⃣ BMI Calculator")
col_bmi1, col_bmi2 = st.columns([1, 1])

with col_bmi1:
    with st.form("bmi_form"):
        weight = st.number_input("⚖️ Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("📏 Height (cm)", min_value=50.0, step=0.1)
        bmi_submit = st.form_submit_button("✅ Calculate BMI")

with col_bmi2:
    if bmi_submit:
        bmi = weight / ((height / 100) ** 2)
        st.metric(label="Your BMI", value=f"{bmi:.2f}")
        if bmi < 18.5:
            st.warning("Underweight 🥗")
        elif 18.5 <= bmi < 24.9:
            st.success("Normal weight 💪")
        elif 25 <= bmi < 29.9:
            st.warning("Overweight ⚠️")
        else:
            st.error("Obese ❌")

st.divider()

#water log
st.header("2️⃣ Water Intake Tracker")
with st.form("water_form"):
    water_today = st.number_input("💧 Water Intake Today (liters)", min_value=0.0, step=0.1)
    water_submit = st.form_submit_button("📥 Log Water Intake")

if water_submit:
    st.session_state.water_intake.append({
        "date": date.today().strftime("%Y-%m-%d"),
        "liters": water_today
    })

if st.session_state.water_intake:
    latest = st.session_state.water_intake[-1]["liters"]
    st.write(f"💧 **Today's Water Intake:** {latest} liters")
    st.progress(min(latest / 3, 1.0))
    if latest < 1.5:
        st.warning("Drink more water! 🚰")
    elif latest < 3:
        st.info("Almost there! 🥤")
    else:
        st.success("Goal reached! 🎉")

st.divider()

# sleep log
st.header("3️⃣ Sleep Log")
with st.form("sleep_form"):
    sleep_hours = st.number_input("🛌 Sleep Hours Last Night", min_value=0.0, max_value=24.0, step=0.1)
    sleep_submit = st.form_submit_button("📥 Log Sleep")

if sleep_submit:
    st.session_state.sleep_log.append({
        "date": date.today().strftime("%Y-%m-%d"),
        "hours": sleep_hours
    })
if st.session_state.sleep_log:
    df = pd.DataFrame(st.session_state.sleep_log)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    avg_sleep = df["hours"].mean()
    st.write(f"📊 **Average Sleep (past {len(df)} days):** {avg_sleep:.1f} hrs")

    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["date"], df["hours"], marker="o", linestyle="-", color="#0A6EE9")
    ax.set_title("Sleep Hours Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hours Slept")
    ax.axhline(8, color="green", linestyle="--", label="Recommended (8 hrs)")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
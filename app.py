import hashlib
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from database import init_db, insert_reading, get_readings

st.set_page_config(
    page_title="AI Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Security / demo authentication
# -----------------------------
# Demo only. In production, use a real identity provider and secure secrets.
DEMO_USERNAME = "admin"
DEMO_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

def check_login(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return username == DEMO_USERNAME and password_hash == DEMO_PASSWORD_HASH

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🌍 AI-Powered Air Quality Monitoring Dashboard")
    st.subheader("Administrator Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.info("Demo credentials: admin / admin123")
    st.caption("This authentication is for an academic prototype, not production security.")
    st.stop()

# -----------------------------
# Initialize
# -----------------------------
init_db()

@st.cache_resource
def load_model():
    return joblib.load("model/air_quality_model.pkl")

@st.cache_data
def load_dataset():
    return pd.read_csv("data/air_quality.csv", parse_dates=["timestamp"])

model = load_model()
df = load_dataset()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙ Controls")

locations = sorted(df["location"].unique())
selected_location = st.sidebar.selectbox("Select location", locations)

st.sidebar.markdown("### Prototype architecture")
st.sidebar.write("IoT Sensors → Network → Server → Database → AI → Dashboard")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# -----------------------------
# Header
# -----------------------------
st.title("🌍 AI-Powered Air Quality Monitoring Dashboard")
st.markdown(
    "A student prototype combining simulated IoT data, networking concepts, "
    "database storage, machine learning, alerts and an interactive dashboard."
)

# -----------------------------
# Current simulated reading
# -----------------------------
location_df = df[df["location"] == selected_location].sort_values("timestamp")
latest = location_df.iloc[-1]

pm25 = float(latest["PM2.5"])
pm10 = float(latest["PM10"])
co2 = float(latest["CO2"])
temperature = float(latest["temperature"])
humidity = float(latest["humidity"])

features = pd.DataFrame([{
    "PM2.5": pm25,
    "PM10": pm10,
    "CO2": co2,
    "temperature": temperature,
    "humidity": humidity
}])

prediction = model.predict(features)[0]

try:
    probabilities = model.predict_proba(features)[0]
    confidence = float(np.max(probabilities))
except Exception:
    confidence = None

st.subheader(f"📍 Current Reading — {selected_location}")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("PM2.5", f"{pm25:.1f}")
c2.metric("PM10", f"{pm10:.1f}")
c3.metric("CO₂", f"{co2:.0f} ppm")
c4.metric("Temperature", f"{temperature:.1f} °C")
c5.metric("Humidity", f"{humidity:.1f}%")

st.divider()

# -----------------------------
# AI prediction
# -----------------------------
left, right = st.columns(2)

with left:
    st.subheader("🤖 AI Prediction")
    st.metric("Predicted Air Quality", prediction)

    if confidence is not None:
        st.write(f"Model confidence: **{confidence:.1%}**")

with right:
    st.subheader("🚨 Alert System")

    if pm25 >= 125:
        st.error("CRITICAL: Very high PM2.5 level detected.")
    elif pm25 >= 75:
        st.warning("WARNING: High PM2.5 level detected.")
    else:
        st.success("Normal: No high-PM2.5 alert for this prototype reading.")

# -----------------------------
# Store current reading
# -----------------------------
if st.button("💾 Save Current Reading to Database"):
    insert_reading(
        datetime.now().isoformat(timespec="seconds"),
        selected_location,
        pm25,
        pm10,
        co2,
        temperature,
        humidity,
        prediction
    )
    st.success("Reading saved to SQLite database.")

# -----------------------------
# Historical charts
# -----------------------------
st.subheader("📊 Historical Air Quality")

chart_df = location_df.tail(200).copy()

fig_pm = px.line(
    chart_df,
    x="timestamp",
    y=["PM2.5", "PM10"],
    title="PM2.5 and PM10 Trend"
)
st.plotly_chart(fig_pm, use_container_width=True)

fig_env = px.line(
    chart_df,
    x="timestamp",
    y=["temperature", "humidity"],
    title="Temperature and Humidity Trend"
)
st.plotly_chart(fig_env, use_container_width=True)

fig_co2 = px.line(
    chart_df,
    x="timestamp",
    y="CO2",
    title="CO₂ Trend"
)
st.plotly_chart(fig_co2, use_container_width=True)

# -----------------------------
# Quality distribution
# -----------------------------
st.subheader("📈 Air Quality Distribution")

quality_counts = location_df["air_quality"].value_counts().reset_index()
quality_counts.columns = ["air_quality", "count"]

fig_quality = px.bar(
    quality_counts,
    x="air_quality",
    y="count",
    title="Recorded Air Quality Categories"
)
st.plotly_chart(fig_quality, use_container_width=True)

# -----------------------------
# Database history
# -----------------------------
st.subheader("🗄 Stored Database Readings")

db_df = get_readings(selected_location, limit=20)

if db_df.empty:
    st.info("No readings have been manually saved yet. Click 'Save Current Reading'.")
else:
    st.dataframe(db_df, use_container_width=True)

# -----------------------------
# System architecture
# -----------------------------
st.subheader("🏗 System Workflow")

st.code("""
Simulated IoT Sensors
        ↓
Wi-Fi / MQTT / HTTP
        ↓
IoT Gateway / Server
        ↓
Data Validation
        ↓
SQLite Database
        ↓
Machine Learning Model
        ↓
Prediction + Alert
        ↓
Streamlit Dashboard
""")

st.subheader("🔐 Cybersecurity Mechanisms")
st.write("""
• Login authentication for the dashboard
• Password comparison using a SHA-256 hash in this academic prototype
• Input/range validation should be applied to real sensor data
• HTTPS/TLS should be used for real client-server communication
• MQTT should use authentication and TLS in a real deployment
• Database access should be restricted to authorized application components
""")

st.caption(
    "Important: Sensor values and air-quality classes in this prototype are simulated. "
    "They should not be used for real health or environmental decisions."
)

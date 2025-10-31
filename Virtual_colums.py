import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# ------------------------------------
# DATABASE CONNECTION
# ------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="genai",  
        database="openflights4"
    )

# ------------------------------------
# CREATE TABLE
# ------------------------------------
def init_routes_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes(
            route_id INT AUTO_INCREMENT PRIMARY KEY,
            Airline VARCHAR(10),
            Airline_ID INT,
            Source_airport VARCHAR(10),
            Source_airport_ID INT,
            Destination_airport VARCHAR(10),
            Destination_airport_ID INT,
            Codeshare VARCHAR(10),
            Equipment VARCHAR(100),
            distance_km INT,
            flight_duration INT AS (
                CASE 
                    WHEN distance_km IS NULL THEN NULL
                    ELSE ROUND((distance_km / 800) * 60)  -- assuming 800 km/h 
                END
            ) VIRTUAL,
            eco_score INT DEFAULT 0,
            stops INT DEFAULT 0,
            aircraft_type VARCHAR(10),
            distance_category VARCHAR(20) AS (
                CASE
                    WHEN distance_km IS NULL THEN 'Unknown'
                    WHEN distance_km < 1000 THEN 'Short'
                    WHEN distance_km BETWEEN 1000 AND 5000 THEN 'Medium'
                    ELSE 'Long'
                END
            ) VIRTUAL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# ------------------------------------
# LOAD DATA
# ------------------------------------
def load_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM routes;")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        cols = [
            "route_id","Airline","Airline_ID","Source_airport","Source_airport_ID",
            "Destination_airport","Destination_airport_ID","Codeshare","Equipment",
            "distance_km","flight_duration","eco_score","stops",
            "aircraft_type","distance_category"
        ]
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(rows)

# ------------------------------------
# STREAMLIT UI CONFIG
# ------------------------------------
st.set_page_config(page_title="Flight Insight Dashboard ✈", layout="wide")
st.title("Flight Insight Dashboard ✈")
st.caption("Powered by MariaDB Virtual Columns & AI Prediction Model")

# Initialize Table
init_routes_table()

# Load Data
df = load_data()

df['flight_duration'] = df['distance_km'].apply(
    lambda x: round((x / 800) * 60) if pd.notnull(x) else None
)


# ------------------------------------
# CSV UPLOAD SECTION
# ------------------------------------
st.sidebar.header("Upload & Filter Flights 📂 ")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file (matching columns)", type=["csv"])
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    # Add eco_score based on distance
    if 'distance_km' in uploaded_df.columns:
        uploaded_df['eco_score'] = uploaded_df['distance_km'].apply(
            lambda x: 5 if pd.notnull(x) and x < 1000 else 3 if pd.notnull(x) and x < 5000 else 1
        )

    df = pd.concat([df, uploaded_df], ignore_index=True)
    st.success("File uploaded successfully! ✅")

# Distance Category Filter
if not df.empty:
    category = st.sidebar.selectbox(
        "Select Distance Category", options=["All"] + sorted(df['distance_category'].dropna().unique().tolist())
    )
    if category != "All":
        df = df[df['distance_category'] == category]

# ------------------------------------
# SUMMARY STATISTICS
# ------------------------------------
st.header("📊 Flight Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Routes", len(df))
col2.metric("Average Distance (km)", f"{df['distance_km'].mean():.0f}" if not df.empty else "0")
col3.metric("Average Eco Score", int(df['eco_score'].mean()) if not df.empty else 0)

st.divider()

# ------------------------------------
# VISUALIZATIONS
# ------------------------------------
if not df.empty:
    st.header("📈 Flight Analytics")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.pie(df, names='distance_category', title='Flights by Distance Category')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        avg_df = df.groupby('distance_category')['distance_km'].mean().reset_index()
        fig2 = px.bar(avg_df, x='distance_category', y='distance_km', color='distance_category',
                      title='Average Distance by Category')
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("⚠️ No data available for visualization.")

st.divider()

# ------------------------------------
# AI PREDICTION MODEL
# ------------------------------------
st.header(" Predict Flight Duration (AI Model)")

if not df.empty:
    # Create clean dataset for model
    df_model = df[['distance_km', 'flight_duration']].dropna()

    if not df_model.empty:
        X = df_model[['distance_km']]
        y = df_model['flight_duration']

        model = LinearRegression()
        model.fit(X, y)

        user_distance = st.number_input("Enter flight distance (in km):", min_value=100, max_value=10000, step=100)
        if st.button("Predict Duration"):
            predicted = model.predict(np.array([[user_distance]]))[0]
            st.success(f"🕒 Predicted Flight Duration: {predicted:.2f} minutes")
    else:
        st.warning("⚠️ Not enough valid data for AI prediction.")
else:
    st.warning("⚠️ No flight data available yet.")

# ------------------------------------
# FALLBACK RULE-BASED ESTIMATION
# ------------------------------------
st.subheader("Quick Estimation (IF AI FAILED)")
user_distance_rule = st.number_input("Estimate duration using average speed (800 km/h):", min_value=100, max_value=10000, step=100)
if st.button("Estimate Duration (Rule-based)"):
    estimated = (user_distance_rule / 800) * 60
    st.info(f"✈️ Estimated Flight Duration: {estimated:.2f} minutes")

st.divider()

# ------------------------------------
# ADDITIONAL INSIGHTS
# ------------------------------------
if not df.empty:
    st.header("🌍 Additional Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 Longest Flights")
        st.dataframe(df.sort_values(by="distance_km", ascending=False).head(5))
    with col2:
        st.subheader("Top 5 Shortest Flights")
        st.dataframe(df.sort_values(by="distance_km", ascending=True).head(5))
else:
    st.info("Upload a CSV to explore flight data.")

st.caption("Developed by Aravind RS — Powered by MariaDB Virtual Columns ")

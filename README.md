# Flight Insight Dashboard

**Flight Insight Dashboard** is a data-driven web application that visualizes airline routes, predicts flight durations using AI, and evaluates environmental impact scores (Eco Score) based on distance (distance calculated using virtual columns) and aircraft efficiency.

---

## ✈️ Overview

This project demonstrates how **MariaDB** can be used as a powerful analytical database for managing aviation route data.  
It leverages **virtual columns** to calculate derived information such as flight duration(calculated using AI), distance categories, and eco scores without redundant data storage.

---

## ⚙️ Features

- **Flight Routes Database**  
  Stores airline route data (source, destination, aircraft type, stops, etc.) in MariaDB.

- **🧮 Virtual Columns**  
  Automatically calculates:
  - `distance_category`: Short / Medium / Long
  - `flight_duration`: AI-predicted duration (based on distance which is calculated using virtual columns)
  - `eco_score`: Efficiency score derived from flight distance

- **🤖 AI Flight Duration Prediction**  
  Uses a **Linear Regression Model** to estimate flight time from distance data.

- **📈 Dashboard Analytics**  
  Displays flight details, route insights, and environmental ratings.

---


## AI Model

The system trains a **Linear Regression** model to predict flight duration:

```python
# Prepare model
df_model = df[['distance_km', 'flight_duration']].dropna()
X = df_model[['distance_km']]
y = df_model['flight_duration']

# Train the model
model.fit(X, y)

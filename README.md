# Flight Insight Dashboard

**Flight Insight Dashboard** is a data-driven web application that visualizes airline routes, predicts flight durations using AI, and evaluates environmental impact scores (Eco Score) based on distance (distance calculated using virtual columns) and aircraft efficiency.

---

## Overview

This project demonstrates how **MariaDB** can be used as a powerful analytical database for managing aviation route data.  
It leverages **virtual columns** to calculate derived information such as flight duration(calculated using AI), distance categories, and eco scores without redundant data storage.

---

## Features

- **Flight Routes Database**  
  Stores airline route data (source, destination, aircraft type, stops, etc.) in MariaDB.

- ** Virtual Columns**  
  Automatically calculates:
  - `distance_category`: Short / Medium / Long
  - `flight_duration`: AI-predicted duration (based on distance which is calculated using virtual columns)
  - `eco_score`: Efficiency score derived from flight distance

- **🤖AI Flight Duration Prediction**  
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

#To prevent missing data issues:

df = df.dropna(subset=['distance_km'])

#To calculate Eco Score:

df['eco_score'] = df['distance_km'].apply(
    lambda x: 5 if x < 1000 else 3 if x < 5000 else 1
)
```
## How to Run / Implement This Project

### Install Dependencies

- Requires python 3.12+ version and Then install required packages:
- pip install -r requirements.txt

### Set Up MariaDB

#### If hosting in Locally ( LocalHost) :
- Install the latest version of MariaDB.
- Create a database, for example openflights : CREATE DATABASE openflights;
- Create the routes table using the structure defined in temporal.py.
- Download the openflights dataset from browser and load the data into the database or you can add data one by one.
- clone the repository and use the code ( Virtual_columns.py) ,update the database connection and run the file using the command "streamlit run <module_name>.py".

#### If hosting in skysql (Online) :
- Create a SkySQL account and set up a database service.
- Create the routes table with the structure as defined in source code and load the routes dataset. (or you can add data one by one)
- Create a Streamlit Cloud account to host the web app online.
- Use the virtual_columns_network.py code and update the connection credentials to your SkySQL database.
- Deploy the Streamlit app via Streamlit Cloud for online access. 
---
### I have deployed the project using SkySQL’s free tier. The website is currently working fine as of October 31, 2025, but I am not certain whether it will remain active during the evaluation period.
### website link : 

## Author

Developed for the **MariaDB Hackathon** by ARAVIND R S

---

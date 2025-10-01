# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- Load trained model ---
model = joblib.load("house_price_model.pkl")

# --- Load dataset to get unique values for categorical features ---
df = pd.read_csv("house prices.csv")

# Preprocess location options
location_counts = df['location'].value_counts()
top_n = 50
top_locations = location_counts.head(top_n).index.tolist()
locations = top_locations + ["Other"]

# Sidebar - User Inputs
st.sidebar.header("Enter Property Details")

bhk = st.sidebar.selectbox("BHK", [1,2,3,4,5,6])
bathroom = st.sidebar.selectbox("Bathroom", [1,2,3,4,5,6])
balcony = st.sidebar.selectbox("Balcony", [0,1,2,3,4,5])
current_floor = st.sidebar.slider("Current Floor", 0, 50, 1)
carpet_area = st.sidebar.number_input("Carpet Area (sqft)", min_value=100, max_value=10000, value=500)
location = st.sidebar.selectbox("Location", locations)
status = st.sidebar.selectbox("Status", df['Status'].dropna().unique())
transaction = st.sidebar.selectbox("Transaction Type", df['Transaction'].dropna().unique())
furnishing = st.sidebar.selectbox("Furnishing", df['Furnishing'].dropna().unique())

# Compute price per sqft (optional display)
price_per_sqft_default = 0  # we don't have actual price yet
price_per_sqft = price_per_sqft_default

# --- Prepare input for model ---
# One-hot encode categorical features same as training
input_dict = {
    "BHK": bhk,
    "Bathroom": bathroom,
    "Balcony": balcony,
    "Current_Floor": current_floor,
    "Carpet_Area_sqft": carpet_area,
    "Price_Per_Sqft": price_per_sqft,  # dummy, model will adjust
}

# Handle categorical features
categorical_features = ["location_grouped", "Status", "Transaction", "Furnishing"]
for cat in categorical_features:
    for val in df[cat.replace("_grouped","")].dropna().unique():
        col_name = f"{cat}_{val}" if cat != "location_grouped" else f"{cat}_{val}"
        input_dict[col_name] = 1 if ((cat=="location_grouped" and location==val) or (cat!="location_grouped" and locals()[cat.lower()] == val)) else 0

# Convert to DataFrame
input_df = pd.DataFrame([input_dict])

# --- Prediction ---
if st.button("Predict House Price"):
    price_pred = model.predict(input_df)[0]
    st.success(f"🏠 Estimated House Price: ₹ {price_pred:,.0f}")
    st.info(f"Price per sqft (approx.): ₹ {price_pred/carpet_area:,.0f} per sqft")

# --- Footer ---
st.markdown("---")
st.markdown("Developed using **Random Forest** & **Streamlit**")

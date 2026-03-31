import streamlit as st
import joblib
import numpy as np

st.title("🏠 House Price Predictor (Model Comparison)")

# Load all models (DON'T overwrite)
ridge_model = joblib.load("../models/ridge.pkl")
linear_model = joblib.load("../models/linear.pkl")
lasso_model = joblib.load("../models/lasso.pkl")

# Inputs
area = st.number_input("Living Area (sqft)", min_value=300, max_value=10000)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5)

if st.button("Predict Price"):
    features = np.array([[area, bedrooms, bathrooms]])

    # Predictions from all models
    linear_pred = linear_model.predict(features)[0]
    ridge_pred = ridge_model.predict(features)[0]
    lasso_pred = lasso_model.predict(features)[0]

    st.subheader("📊 Model Predictions")

    st.write(f"🔹 Linear Regression: ${linear_pred:,.2f}")
    st.write(f"🔹 Ridge Regression: ${ridge_pred:,.2f}")
    st.write(f"🔹 Lasso Regression: ${lasso_pred:,.2f}")

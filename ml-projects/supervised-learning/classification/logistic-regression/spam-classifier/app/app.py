import streamlit as st
import pickle

model = pickle.load(open("../models/model.pkl", "rb"))
vectorizer = pickle.load(open("../models/vectorizer.pkl", "rb"))

st.title("Spam Classifier")

msg = st.text_area("Enter message")

if st.button("Predict"):
    vec = vectorizer.transform([msg])
    result = model.predict(vec)[0]
    st.write("Spam" if result == 1 else "Not Spam")

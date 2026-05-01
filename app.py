import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    sheet_ID = "133p_AZdXgB3YUstAlOrn25tOJuplWbuGkx9KYwW9O7M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_ID}/export?format=csv"

    data = pd.read_csv(url)
    return data

df = load_data()

st.write("Test data", df)
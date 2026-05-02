import streamlit as st
import pandas as pd

@st.cache_data
def load_data(gid):
    sheet_ID = "133p_AZdXgB3YUstAlOrn25tOJuplWbuGkx9KYwW9O7M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_ID}/export?format=csv&gid={gid}"

    data = pd.read_csv(url)
    return data

def create_standings(data):
    standings = data.groupby(['Player', 'Outcome']).size().unstack(fill_value=0)
    #checks if collumn is empty
    cols = ['w', 'l', 't']
    existing_cols = [c for c in cols if c in standings.columns]
    standings = standings[existing_cols]

    return standings.reset_index()

games = load_data(0)
standings = create_standings(games)
st.table(standings)
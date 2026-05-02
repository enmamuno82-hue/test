import streamlit as st
import pandas as pd

@st.cache_data
def load_data(gid):
    sheet_ID = "133p_AZdXgB3YUstAlOrn25tOJuplWbuGkx9KYwW9O7M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_ID}/export?format=csv&gid={gid}"

    data = pd.read_csv(url)
    return data

def create_standings(data):
    standings = data.groupby(['PlayerID', 'Outcome']).size().unstack(fill_value=0)
    standings = standings.reset_index()

    col = ['PlayerID', 'w', 'l', 't']
    for c in col:
        if c not in standings.columns:
            col.remove(c)
    standings = standings[col].reset_index()



    standings = standings.sort_values(by='w', ascending=False)
    return standings.reset_index(drop=True)

games = load_data(0)
players = load_data(1430924563)
standings = create_standings(games)
st.table(standings)
st.table(players)
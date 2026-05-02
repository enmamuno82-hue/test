import streamlit as st
import pandas as pd

@st.cache_data
def load_data(gid):
    sheet_ID = "133p_AZdXgB3YUstAlOrn25tOJuplWbuGkx9KYwW9O7M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_ID}/export?format=csv&gid={gid}"

    data = pd.read_csv(url)
    return data

def create_standings(data, pdata):
    standings = data.groupby(['PlayerID', 'Outcome']).size().unstack(fill_value=0)
    standings = standings.reset_index()

    col = ['PlayerID', 'w', 'l', 't']
    for c in col:
        if c not in standings.columns:
            col.remove(c)
    standings = standings[col].reset_index()

    standings = standings.merge(pdata[['PlayerID', 'Name']], on='PlayerID', how='left')
    standings['Player'] = standings['Name'] + "\n(" + standings['PlayerID'].astype(str) + ")"

    col.remove('PlayerID')
    standings['GP'] = standings[col].sum(axis=1)
    standings['Win %'] = (standings['w'] / standings['GP']).round(2)

    final_order = ['Player', 'GP', 'Win %'] + col
    standings = standings[final_order].sort_values(by='w', ascending=False)
    return standings.reset_index(drop=True)

games = load_data(0)
players = load_data(1430924563)
standings = create_standings(games, players)
st.table(standings)
st.table(players)
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
    standings['Player'] = standings['Name']

    col.remove('PlayerID')
    standings['GP'] = standings[col].sum(axis=1)
    standings['Win %'] = (standings['w'] / standings['GP']).round(3)

    forder = []
    if 'w' in col:
        standings = standings.rename(columns={'w': 'Wins'})
        forder = forder + ['Wins']
    if 'l' in col:
        standings = standings.rename(columns={'l': 'Losses'})
        forder = forder + ['Losses']
    if 't' in col:
        standings = standings.rename(columns={'t': 'Draws'})
        forder = forder + ['Draws']

    forder = ['Player', 'GP', 'Win %'] + forder + ['PlayerID']
    standings = standings[forder].sort_values(by='Wins', ascending=False)
    standings.insert(0, 'Seed', range(1, len(standings) + 1))

    base_url = 'https://7mj8sspzd6qkm2qloaxshl.streamlit.app'
    standings['Profile_Link'] = base_url + "/?player_id=" + standings['PlayerID'].astype(str)

    return standings.reset_index(drop=True)

games = load_data(0)
players = load_data(1430924563)
standings = create_standings(games, players)

st.title("Chess Tournament Leaderboard")
st.dataframe(
    standings,
    column_config={
        "PlayerID": None,
        "Profile_Link": st.column_config.LinkColumn("View", display_text="🔗 Profile"),
        "Win %": st.column_config.NumberColumn(format="%.3f")
    },
    hide_index=True,
)
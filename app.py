import streamlit as st
import pandas as pd

@st.cache_data
def load_data(gid):
    sheet_ID = "133p_AZdXgB3YUstAlOrn25tOJuplWbuGkx9KYwW9O7M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_ID}/export?format=csv&gid={gid}"

    data = pd.read_csv(url)
    return data

def find_seas(data):
    filtered = data.sort_values(by='Season', ascending=False)

    season = filtered['Season'].iat[0]

    return filtered[filtered['Season'] == season].reset_index(drop=True)

def create_standings(data, pdata):
    standings = data.groupby(['PlayerID', 'Outcome']).size().unstack(fill_value=0)
    standings = standings.reset_index()

    col = ['PlayerID', 'w', 'l', 't']
    for c in col:
        if c not in standings.columns:
            col.remove(c)
    standings = standings[col].reset_index()

    ids = standings['PlayerID'].tolist()
    nids = []

    for num in ids:
        name = pdata[pdata['PlayerID'] == num]
        nids.append(name['Name'].iat[0])

    standings['Player'] = nids

    col.remove('PlayerID')
    standings['GP'] = standings[col].sum(axis=1)
    standings['Win %'] = ((standings['w'] / standings['GP']) * 100).astype(str) + "%"

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

    forder = ['Seed'] + forder

    standings = standings[forder].reset_index(drop=True)

    st.dataframe(
        standings,
        column_config={
            "PlayerID": None,
        },
        hide_index=True,
    )


def player_profile(data, pdata):
    pid = st.query_params["player_id"]

    player_row = pdata[pdata['PlayerID'].astype(str) == str(pid)]

    if not player_row.empty:
        player_name = player_row.iloc[0]['Name']
        st.title(f"👤 {player_name}")
        
        st.subheader("Game History")
    else:
        st.error("Player not found.")

def lookup(pdata, cpid):
    selected_name = st.session_state.get(f"search_{cpid}")

    if selected_name is None:
        return

    if selected_name != "--- Select a Player ---":
        selected_id = pdata[pdata['Name'] == selected_name.split()[0]]['PlayerID']
        
        st.query_params["player_id"] = selected_id
        del st.session_state[f"search_{cpid}"]
        st.rerun()

def sidebr():

    if st.button("Standings"):
        del st.query_params['player_id']
        st.rerun()

games = load_data(0)
players = load_data(1430924563)
seasons = load_data(985399788)

if "player_id" in st.query_params:
    cpid = st.query_params["player_id"]

    with st.sidebar:
        names_list = ["--- Select a Player ---"] + [f"{row['Name']} {row['PlayerID']}" for _, row in players.iterrows()]
        selected_name = st.sidebar.selectbox("Player Lookup", options=names_list, index=0,key=f"search_{cpid}", on_change=lookup(players, cpid))
        sidebr()

    if st.button("⬅️ Back"):
        del st.query_params['player_id']
        del st.session_state[f"search_{cpid}"]
        st.rerun()
    
    player_profile(games, players)


else:
    with st.sidebar:
        names_list = ["--- Select a Player ---"] + [f"{row['Name']} {row['PlayerID']}" for _, row in players.iterrows()]
        selected_name = st.sidebar.selectbox("Player Lookup", options=names_list, index=0,key=f"search_h", on_change=lookup(players, "h"))
        sidebr()

    regular = games[games['Game'] == "regular"]
    filtered = find_seas(regular)

    season = filtered['Season'].iat[0]
    sfilt = seasons[seasons['Seasonnum'] == season]


    st.title("Chess Tournament Leaderboard")
    st.title(sfilt['Seasonname'].iat[0])
    standings = create_standings(filtered, players)

